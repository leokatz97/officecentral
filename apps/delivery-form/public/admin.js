// Admin view: sign in, list submissions, mark handled, export CSV.
(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const views = { login: $('loginView'), setup: $('setupView'), app: $('appView') };
  let brands = [];
  let fields = [];
  let submissions = [];
  let status = {};
  const openRows = new Set();

  function show(name) {
    for (const [k, v] of Object.entries(views)) v.hidden = k !== name;
    $('headerActions').hidden = name !== 'app';
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

  const fmtDate = (iso) => {
    const d = new Date(iso);
    return d.toLocaleString('en-CA', { timeZone: 'America/Toronto', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  };
  const brandOf = (slug) => brands.find((b) => b.slug === slug) || { name: slug, shortName: slug, accent: '#666' };
  const repName = (rep) => (rep || '').split(' (')[0];

  async function api(path, options) {
    const res = await fetch(path, { credentials: 'same-origin', ...options });
    const json = await res.json().catch(() => ({}));
    return { res, json };
  }

  // ---- sign in ----
  $('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = $('loginBtn');
    const err = $('loginError');
    err.hidden = true;
    btn.disabled = true;
    try {
      const { res, json } = await api('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: $('password').value }),
      });
      if (!res.ok) throw new Error(json.error || 'Could not sign in.');
      $('password').value = '';
      await boot();
    } catch (e2) {
      err.textContent = e2.message;
      err.hidden = false;
    } finally {
      btn.disabled = false;
    }
  });

  $('logoutBtn').addEventListener('click', async () => {
    await api('/api/admin/logout', { method: 'POST' });
    show('login');
  });
  $('refreshBtn').addEventListener('click', load);
  $('exportBtn').addEventListener('click', exportCsv);
  for (const id of ['search', 'brandFilter', 'repFilter', 'showHandled']) $(id).addEventListener('input', render);

  // ---- setup guidance ----
  function setupSteps() {
    const items = [];
    if (!status.store) items.push('<li><strong>Storage is off.</strong> In Vercel: open the project → <em>Storage</em> → <em>Create Database</em> → <em>Blob</em> → connect it. Then redeploy.</li>');
    if (!status.mail) items.push('<li><strong>Email is off.</strong> In Vercel: project → <em>Settings</em> → <em>Environment Variables</em>. Add <code>SMTP_USER</code> (the Gmail address that sends) and <code>SMTP_PASS</code> (a Gmail App Password). Then redeploy.</li>');
    return items;
  }

  function renderSetupNotice() {
    const box = $('setupNotice');
    const items = setupSteps();
    if (!items.length) {
      box.replaceChildren();
      return;
    }
    const lead = items.length > 1 ? 'Almost ready. Two switches to flip in Vercel:' : 'Almost ready. One switch to flip in Vercel:';
    box.innerHTML = `<div class="notice notice--warn"><strong>${lead}</strong><ol>${items.join('')}</ol></div>`;
  }

  // ---- data ----
  async function boot() {
    const { json: st } = await api('/api/admin/status');
    status = st || {};
    if (!status.adminPassword) {
      views.setup.innerHTML = `<div class="notice notice--warn"><strong>Admin password not set up yet.</strong>
        In Vercel: project → <em>Settings</em> → <em>Environment Variables</em> → add <code>ADMIN_PASSWORD</code> (at least 6 characters) → redeploy. Then come back here and sign in.</div>`;
      show('setup');
      return;
    }
    if (!status.authed) {
      show('login');
      setTimeout(() => $('password').focus(), 0);
      return;
    }
    if (!brands.length) {
      const { json } = await api('/api/brands');
      brands = json.brands || [];
      fields = json.fields || [];
      const bf = $('brandFilter');
      for (const b of brands) bf.append(el('option', { value: b.slug, text: b.shortName }));
    }
    show('app');
    renderSetupNotice();
    await load();
  }

  async function load() {
    $('refreshBtn').disabled = true;
    try {
      const { res, json } = await api('/api/admin/submissions');
      if (res.status === 401) return show('login');
      if (!res.ok) throw new Error(json.error || 'Could not load.');
      submissions = json.submissions || [];
      const reps = [...new Set(submissions.map((s) => s.values.rep).filter(Boolean))].sort();
      const rf = $('repFilter');
      const current = rf.value;
      rf.replaceChildren(el('option', { value: '', text: 'All reps' }), ...reps.map((r) => el('option', { value: r, text: repName(r) })));
      rf.value = reps.includes(current) ? current : '';
      render();
    } catch (err) {
      $('rows').replaceChildren();
      $('empty').textContent = err.message;
      $('empty').hidden = false;
    } finally {
      $('refreshBtn').disabled = false;
    }
  }

  function filtered() {
    const q = $('search').value.trim().toLowerCase();
    const brand = $('brandFilter').value;
    const rep = $('repFilter').value;
    const showHandled = $('showHandled').checked;
    return submissions.filter((s) => {
      if (brand && s.brand !== brand) return false;
      if (rep && s.values.rep !== rep) return false;
      if (!showHandled && s.handled) return false;
      if (q) {
        const hay = Object.values(s.values).join(' ').toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
  }

  function emailPill(s) {
    const map = {
      sent: ['pill--ok', 'Sent'],
      failed: ['pill--danger', 'Failed'],
      pending: ['pill--warn', 'Pending'],
      'not-configured': ['pill--muted', 'Not set up'],
    };
    const [cls, label] = map[s.email && s.email.status] || ['pill--muted', '—'];
    const pill = el('span', { class: `pill ${cls}`, text: label });
    if (s.email && s.email.error) pill.title = s.email.error;
    return pill;
  }

  function render() {
    const list = filtered();
    const weekAgo = Date.now() - 7 * 86400000;
    const stats = [
      ['Total', submissions.length],
      ['This week', submissions.filter((s) => new Date(s.submittedAt).getTime() > weekAgo).length],
      ['Waiting on office', submissions.filter((s) => !s.handled).length],
      ['Email failed', submissions.filter((s) => s.email && s.email.status === 'failed').length],
    ];
    $('stats').replaceChildren(...stats.map(([label, n]) => el('div', { class: 'stat' }, [el('div', { class: 'stat__label', text: label }), el('div', { class: 'stat__num', text: String(n) })])));

    const rows = $('rows');
    rows.replaceChildren();
    const empty = $('empty');
    if (!list.length) {
      empty.textContent = submissions.length
        ? 'Nothing matches those filters.'
        : status.store
          ? 'No forms submitted yet. Share a form link with the reps to get started.'
          : 'Storage is not connected yet, so nothing can be listed here.';
      empty.hidden = false;
      return;
    }
    empty.hidden = true;

    for (const s of list) {
      const b = brandOf(s.brand);
      const v = s.values;
      const tr = el('tr', { class: s.handled ? 'is-handled' : '', 'data-id': s.id, tabindex: '0', 'aria-expanded': openRows.has(s.id) ? 'true' : 'false' });
      tr.append(
        el('td', { class: 'num', text: fmtDate(s.submittedAt) }),
        el('td', {}, [el('span', { class: 'pill pill--brand', style: `--pill-accent:${b.accent}`, text: b.shortName })]),
        el('td', { text: repName(v.rep) }),
        el('td', { class: 'num', text: v.quote || '—' }),
        el('td', { class: 'cell-wrap', text: v.customer || '—' }),
        el('td', { class: 'cell-wrap' }, [el('div', { text: v.contactName || '—' }), el('div', { class: 'muted', text: v.contactPhone || '' })]),
        el('td', { text: v.floor || '—' }),
        el('td', { text: v.delivery || '—' }),
        el('td', {}, [emailPill(s)]),
      );
      const check = el('label', { class: 'check' }, [el('input', { type: 'checkbox' }), el('span', { class: 'muted', text: s.handled ? 'Done' : 'Open' })]);
      check.querySelector('input').checked = Boolean(s.handled);
      check.addEventListener('click', (e) => e.stopPropagation());
      check.querySelector('input').addEventListener('change', (e) => toggleHandled(s, e.target));
      tr.append(el('td', {}, [check]));
      tr.addEventListener('click', () => toggleDetail(s.id));
      tr.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleDetail(s.id); }
      });
      rows.append(tr);
      if (openRows.has(s.id)) rows.append(detailRow(s));
    }
  }

  function detailRow(s) {
    const dl = el('dl', { class: 'detail__grid' });
    for (const f of fields) {
      dl.append(el('div', {}, [el('dt', { text: f.label }), el('dd', { text: s.values[f.key] || '—' })]));
    }
    const emailTo = s.email ? [...(s.email.to || []), ...(s.email.cc || []).map((c) => `${c} (cc)`)].join(', ') : '—';
    dl.append(el('div', {}, [el('dt', { text: 'Emailed to' }), el('dd', { text: emailTo })]));
    if (s.email && s.email.error) dl.append(el('div', {}, [el('dt', { text: 'Email error' }), el('dd', { text: s.email.error })]));
    if (s.handledAt) dl.append(el('div', {}, [el('dt', { text: 'Marked handled' }), el('dd', { text: fmtDate(s.handledAt) })]));
    return el('tr', { class: 'detail' }, [el('td', { colspan: '10' }, [dl])]);
  }

  function toggleDetail(id) {
    if (openRows.has(id)) openRows.delete(id);
    else openRows.add(id);
    render();
  }

  async function toggleHandled(s, checkbox) {
    const wanted = checkbox.checked;
    checkbox.disabled = true;
    try {
      const { res, json } = await api('/api/admin/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: s.id, handled: wanted }),
      });
      if (!res.ok) throw new Error(json.error || 'Could not save.');
      Object.assign(s, json.submission);
    } catch (err) {
      alert(err.message);
      checkbox.checked = !wanted;
    } finally {
      checkbox.disabled = false;
      render();
    }
  }

  function exportCsv() {
    const list = filtered();
    const head = ['Submitted', 'Company', ...fields.map((f) => f.label), 'Email status', 'Handled'];
    const esc = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
    const lines = [head.map(esc).join(',')];
    for (const s of list) {
      lines.push([
        new Date(s.submittedAt).toLocaleString('en-CA', { timeZone: 'America/Toronto' }),
        brandOf(s.brand).name,
        ...fields.map((f) => s.values[f.key] || ''),
        s.email ? s.email.status : '',
        s.handled ? 'Yes' : 'No',
      ].map(esc).join(','));
    }
    const blob = new Blob(['﻿' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `delivery-forms-${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.append(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(a.href);
  }

  boot();
})();
