/* Small native helpers for the HTML prototype. No network or framework. */
(() => {
  let toastTimer;
  let activeModal;
  const text = (tag, content, className) => {
    const node = document.createElement(tag);
    node.textContent = content;
    if (className) node.className = className;
    return node;
  };
  function toast(message, kind = 'info') {
    let node = document.querySelector('.prototype-toast');
    if (!node) {
      node = text('div', '', 'prototype-toast');
      node.setAttribute('role', 'status');
      node.setAttribute('aria-live', 'polite');
      document.body.append(node);
    }
    clearTimeout(toastTimer);
    node.textContent = message;
    node.dataset.kind = kind;
    node.dataset.visible = 'true';
    toastTimer = setTimeout(() => { node.dataset.visible = 'false'; }, 2600);
  }
  function modal({title, message, confirm = '知道了', cancel = null}) {
    if (activeModal) activeModal();
    const trigger = document.activeElement;
    const dialog = document.createElement('dialog');
    dialog.className = 'prototype-modal';
    dialog.setAttribute('aria-labelledby', 'prototype-modal-title');
    dialog.setAttribute('aria-describedby', 'prototype-modal-message');
    const heading = text('h2', title); heading.id = 'prototype-modal-title';
    const copy = text('p', message); copy.id = 'prototype-modal-message';
    const actions = document.createElement('div'); actions.className = 'prototype-modal-actions';
    dialog.append(heading, copy, actions);
    document.body.append(dialog);
    return new Promise(resolve => {
      let settled = false;
      function close(value = false) {
        if (settled) return;
        settled = true;
        dialog.close(); dialog.remove(); activeModal = null;
        if (trigger?.isConnected) trigger.focus();
        resolve(value);
      }
      activeModal = close;
      if (cancel) {
        const button = text('button', cancel); button.type = 'button';
        button.addEventListener('click', () => close(false)); actions.append(button);
      }
      const button = text('button', confirm); button.type = 'button'; button.dataset.primary = 'true';
      button.addEventListener('click', () => close(true)); actions.append(button);
      dialog.addEventListener('cancel', event => { event.preventDefault(); close(false); });
      dialog.addEventListener('keydown', event => {
        if (event.key !== 'Tab') return;
        const controls = [...dialog.querySelectorAll('button,input,textarea,select,a[href]')].filter(e => !e.disabled && e.getClientRects().length);
        const first = controls[0], last = controls[controls.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      });
      dialog.addEventListener('click', event => {
        if (event.target !== dialog) return;
        const r = dialog.getBoundingClientRect();
        if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) close(false);
      });
      dialog.showModal(); actions.querySelector('button').focus();
    });
  }
  async function busy(button, label, operation) {
    if (button.disabled) return false;
    const original = button.textContent;
    button.disabled = true; button.setAttribute('aria-busy', 'true'); button.textContent = label;
    try { await new Promise(resolve => setTimeout(resolve, 550)); return await operation(); }
    catch (error) { toast(error.message || '操作没有完成，请再试一次', 'error'); return false; }
    finally { button.disabled = false; button.removeAttribute('aria-busy'); button.textContent = original; }
  }
  function back(fallback) {
    let source;
    try { source = new URL(document.referrer); } catch {}
    if (source?.origin === location.origin && /\/pages\/m\d{2}-p\d{2}\.html$/.test(source.pathname) && history.length > 1) history.back();
    else location.href = fallback;
  }
  function read(key, fallback = null) {
    try { const value = localStorage.getItem(key); return value === null ? fallback : JSON.parse(value); }
    catch { return fallback; }
  }
  function write(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); return true; }
    catch { toast('本地空间不足，未能保存。请整理空间后再试', 'error'); return false; }
  }
  window.PrototypeUI = {toast, modal, busy, back, read, write};
})();
