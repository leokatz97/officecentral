(function () {
  'use strict';

  function onScroll() {
    var header = document.querySelector('.bbi .header');
    if (!header) return;
    if (window.scrollY > 40) header.classList.add('is-scrolled');
    else header.classList.remove('is-scrolled');
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var modal = document.querySelector('.bbi-quote-modal');
  if (!modal) return;

  var backdrop = modal.querySelector('.modal-backdrop');
  var ctxLabel = modal.querySelector('[data-quote-context-label]');
  var ctxInput = modal.querySelector('[data-quote-context-input]');
  var successState = modal.querySelector('.success-state');
  var form = modal.querySelector('.form');
  var formContainer = modal.querySelector('.form-container');

  function openModal(label, placeholder) {
    if (ctxLabel) ctxLabel.textContent = label || 'Request a quote';
    if (ctxInput && placeholder) ctxInput.setAttribute('placeholder', placeholder);
    modal.setAttribute('data-open', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modal.removeAttribute('data-open');
    document.body.style.overflow = '';
    if (successState) successState.style.display = 'none';
    if (formContainer) formContainer.style.display = '';
    if (form) form.reset();
  }

  document.addEventListener('click', function (e) {
    var trigger = e.target.closest('[data-quote-trigger]');
    if (trigger) {
      e.preventDefault();
      openModal(trigger.getAttribute('data-quote-label'), trigger.getAttribute('data-quote-placeholder'));
      return;
    }
    if (e.target.closest('.modal-close')) {
      closeModal();
      return;
    }
    // Click inside the modal dialog — do nothing (don't close)
    if (e.target.closest('.modal')) return;
    // Click on the backdrop itself (outside the dialog) — close
    if (e.target.closest('.modal-backdrop')) {
      closeModal();
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modal.getAttribute('data-open') === 'true') closeModal();
  });

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (formContainer) formContainer.style.display = 'none';
      if (successState) successState.style.display = 'block';
    });
  }
})();