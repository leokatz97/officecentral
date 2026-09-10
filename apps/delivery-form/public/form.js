// Delivery Information form. Brand comes from the URL path (/schoolhouse, /brant, ...).
(function () {
  'use strict';

  const slug = location.pathname.replace(/^\/+|\/+$/g, '') || 'schoolhouse';
  const els = {
    mark: document.getElementById('brandMark'),
    name: document.getElementById('brandName'),
    tag: document.getElementById('brandTag'),
    form: document.getElementById('deliveryForm'),
    fields: document.getElementById('fields'),
    formError: document.getElementById('formError'),
    submitBtn: document.getElementById('submitBtn'),
    done: document.getElementById('done'),
    doneNote: document.getElementById('doneNote'),
    doneSummary: document.getElementById('doneSummary'),
    againBtn: document.getElementById('againBtn'),
    loadError: document.getElementById('loadError'),
    intro: document.getElementById('intro'),
  };

  let brand = null;
  let fields = [];
  let OTHER = 'Other';
  const REP_KEY = 'df.lastRep';

  function initials(name) {
    return name.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toUpperCase();
  }

  function optionsFor(field) {
    return field.optionsFrom ? brand[field.optionsFrom] : field.options || [];
  }

  function el(tag, attrs, children) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === 'text') node.textContent = v;
      else if (k === 'html') node.innerHTML = v;
      else if (v !== null && v !== undefined && v !== false) node.setAttribute(k, v === true ? '' : v);
    }
    for (const c of children || []) node.append(c);
    return node;
  }

  function renderField(field) {
    const id = `f_${field.key}`;
    const wrap = el('div', { class: 'field', 'data-key': field.key });
    const label = el('label', { class: 'field__label', for: id, text: field.label });
    if (field.required) label.append(el('span', { class: 'req', 'aria-hidden': 'true', text: '*' }));
    wrap.append(label);

    let control;
    if (field.type === 'select') {
      control = el('select', { class: 'control', id, name: field.key, required: field.required });
      control.append(el('option', { value: '', text: field.required ? 'Choose one…' : 'Choose one (optional)' }));
      for (const opt of optionsFor(field)) control.append(el('option', { value: opt, text: opt }));
      if (field.allowOther) {
        control.append(el('option', { value: OTHER, text: 'Other' }));
        const otherId = `${id}_other`;
        const otherBox = el('div', { class: 'other-box', hidden: true }, [
          el('label', { class: 'visually-hidden', for: otherId, text: `${field.label} (other)` }),
          el('input', { class: 'control', id: otherId, name: `${field.key}Other`, type: 'text', placeholder: 'Please describe' }),
        ]);
        control.addEventListener('change', () => {
          otherBox.hidden = control.value !== OTHER;
          if (!otherBox.hidden) otherBox.querySelector('input').focus();
        });
        wrap.append(control, otherBox);
      } else {
        wrap.append(control);
      }
    } else if (field.type === 'textarea') {
      control = el('textarea', { class: 'control', id, name: field.key, rows: 4, required: field.required });
      wrap.append(control);
    } else {
      const auto = { email: 'email', tel: 'tel' }[field.type] || 'off';
      control = el('input', {
        class: 'control', id, name: field.key, type: field.type, required: field.required,
        autocomplete: auto, inputmode: field.type === 'tel' ? 'tel' : null, placeholder: field.placeholder || null,
        // Install dates are in the future; keep the calendar from offering the past.
        min: field.type === 'date' ? new Date().toISOString().slice(0, 10) : null,
      });
      wrap.append(control);
    }
    wrap.append(el('div', { class: 'field__error', role: 'alert', hidden: true }));
    return wrap;
  }

  function setErrors(errors) {
    for (const wrap of els.fields.querySelectorAll('.field')) {
      const key = wrap.dataset.key;
      const msg = errors[key];
      const box = wrap.querySelector('.field__error');
      wrap.classList.toggle('field--error', Boolean(msg));
      box.hidden = !msg;
      box.textContent = msg || '';
      const control = wrap.querySelector('.control');
      if (control) control.setAttribute('aria-invalid', msg ? 'true' : 'false');
    }
    const first = els.fields.querySelector('.field--error .control');
    if (first) first.focus();
  }

  function clientValidate(data) {
    const errors = {};
    for (const f of fields) {
      const v = (data[f.key] || '').trim();
      if (f.required && !v) errors[f.key] = 'This one is required.';
      else if (f.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) errors[f.key] = 'That email address does not look right.';
      else if (f.type === 'select' && f.allowOther && v === OTHER && !(data[`${f.key}Other`] || '').trim()) errors[f.key] = 'Please describe the "Other" choice.';
      else if (f.type === 'date' && v && !/^\d{4}-\d{2}-\d{2}$/.test(v)) errors[f.key] = 'Please pick a date from the calendar.';
    }
    return errors;
  }

  function fmtDate(v) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(v)) return v;
    return new Date(`${v}T00:00:00Z`).toLocaleDateString('en-CA', { timeZone: 'UTC', weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
  }

  function displayValue(field, data) {
    const v = (data[field.key] || '').trim();
    if (field.type === 'select' && field.allowOther && v === OTHER) return `Other: ${(data[`${field.key}Other`] || '').trim()}`;
    if (field.type === 'date') return fmtDate(v);
    return v;
  }

  async function submit(event) {
    event.preventDefault();
    els.formError.hidden = true;
    const data = Object.fromEntries(new FormData(els.form).entries());
    const errors = clientValidate(data);
    if (Object.keys(errors).length) return setErrors(errors);
    setErrors({});

    els.submitBtn.disabled = true;
    els.submitBtn.textContent = 'Sending…';
    try {
      const res = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ brand: brand.slug, ...data }),
      });
      const json = await res.json().catch(() => ({}));
      if (res.status === 422 && json.errors) return setErrors(json.errors);
      if (!res.ok || !json.ok) throw new Error(json.error || 'Something went wrong. Please try again.');

      try { localStorage.setItem(REP_KEY, data.rep || ''); } catch (_) {}
      showDone(data, json);
    } catch (err) {
      els.formError.textContent = err.message || 'Something went wrong. Please try again.';
      els.formError.hidden = false;
      els.formError.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } finally {
      els.submitBtn.disabled = false;
      els.submitBtn.textContent = 'Send delivery info';
    }
  }

  function showDone(data, result) {
    els.doneSummary.replaceChildren();
    for (const f of fields) {
      const v = displayValue(f, data);
      if (!v) continue;
      els.doneSummary.append(el('div', {}, [el('dt', { text: f.label }), el('dd', { text: v })]));
    }
    els.doneNote.textContent = result.emailed
      ? `Emailed to the ${brand.shortName} delivery team and saved for the office.`
      : 'Saved for the office. The email is not switched on yet, so the office will see it in the admin view.';
    els.form.hidden = true;
    els.intro.hidden = true;
    els.done.hidden = false;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function reset() {
    els.form.reset();
    for (const box of els.fields.querySelectorAll('.other-box')) box.hidden = true;
    setErrors({});
    restoreRep();
    els.done.hidden = true;
    els.intro.hidden = false;
    els.form.hidden = false;
    window.scrollTo({ top: 0 });
    const first = els.fields.querySelector('.control');
    if (first) first.focus();
  }

  function restoreRep() {
    try {
      const last = localStorage.getItem(REP_KEY);
      const select = document.getElementById('f_rep');
      if (last && select && [...select.options].some((o) => o.value === last)) select.value = last;
    } catch (_) {}
  }

  async function init() {
    try {
      const res = await fetch('/api/brands');
      if (!res.ok) throw new Error('bad status');
      const json = await res.json();
      brand = json.brands.find((b) => b.slug === slug);
      fields = json.fields;
      OTHER = json.other || OTHER;
      if (!brand) {
        els.name.textContent = 'Form not found';
        els.loadError.innerHTML = 'This link is not one of the delivery forms. <a href="/">See the list of forms</a>.';
        els.loadError.hidden = false;
        els.intro.hidden = true;
        return;
      }
    } catch (err) {
      els.name.textContent = 'Could not load';
      els.loadError.textContent = 'The form could not load. Check your connection and refresh the page.';
      els.loadError.hidden = false;
      return;
    }

    document.documentElement.style.setProperty('--accent', brand.accent);
    document.title = `${brand.shortName} Delivery Information`;
    els.mark.textContent = initials(brand.name);
    els.name.textContent = brand.name;
    els.tag.textContent = brand.tagline;

    els.fields.replaceChildren(...fields.map(renderField));
    restoreRep();
    els.form.hidden = false;
    els.form.addEventListener('submit', submit);
    els.againBtn.addEventListener('click', reset);
  }

  init();
})();
