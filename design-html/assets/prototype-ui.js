/* Small native helpers for the HTML prototype. No network or framework. */
(() => {
  let toastTimer;
  let activeModal;
  let pendingPop;
  let navigationGuard;
  document.documentElement.dataset.prototypeReduceMotion=String(read('dujia-prototype-preferences',{})?.reduceMotion===true);
  const reducedMotion=()=>matchMedia('(prefers-reduced-motion:reduce)').matches||read('dujia-prototype-preferences',{})?.reduceMotion===true;
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
    node.setAttribute('role', kind === 'error' ? 'alert' : 'status');
    node.dataset.kind = kind;
    node.dataset.visible = 'true';
    toastTimer = setTimeout(() => { node.dataset.visible = 'false'; }, 2600);
  }
  let fieldSequence = 0;
  function componentButton(label, onClick, {variant = 'primary', disabled = false, name = null} = {}) {
    const button = text('button', label, 'prototype-component-button');
    button.type = 'button'; button.dataset.variant = variant; button.disabled = disabled;
    if (name) button.setAttribute('aria-label', name);
    if (onClick) button.addEventListener('click', onClick);
    return button;
  }
  function componentField({label, name = '', value = '', placeholder = '', multiline = false, type = 'text', maxLength = null, disabled = false, required = false}) {
    const root = text('label', '', 'prototype-component-field'), id = 'prototype-field-' + ++fieldSequence;
    const input = document.createElement(multiline ? 'textarea' : 'input'), error = text('p', '', 'prototype-component-error');
    if (!multiline) input.type = type;
    input.id = id; input.name = name; input.value = value; input.placeholder = placeholder; input.disabled = disabled; input.required = required;
    if (maxLength !== null) input.maxLength = maxLength;
    error.id = id + '-error'; error.hidden = true; error.setAttribute('role', 'alert');
    const caption = text('span', label); caption.id = id + '-label';
    input.setAttribute('aria-labelledby', caption.id); input.setAttribute('aria-describedby', error.id); root.append(caption, input, error);
    const setError = message => fieldError(input, message, error);
    input.addEventListener('input', () => setError(''));
    return {root, input, error, setError};
  }
  function componentCard({title, message = '', onClick = null, selected = null}) {
    const root = document.createElement(onClick ? 'button' : 'article'); root.className = 'prototype-component-card';
    root.append(text('h2', title), text('p', message));
    if (onClick) { root.type = 'button'; root.addEventListener('click', onClick); }
    if (onClick && selected !== null) root.setAttribute('aria-pressed', String(selected));
    return root;
  }
  function componentHeader({title, onBack = null, action = null, transparent = false}) {
    const root = text('header', '', 'prototype-component-header'); root.dataset.transparent = String(transparent);
    if (onBack) root.append(componentButton('←', onBack, {variant: 'icon', name: '返回'}));
    root.append(text('h1', title)); if (action) root.append(action); return root;
  }
  function componentState({kind = 'empty', title, message = '', action = null, onAction = null}) {
    const root = text('section', '', 'prototype-component-state'); root.dataset.kind = kind;
    root.setAttribute('role', kind === 'error' ? 'alert' : 'region'); if (kind !== 'error') root.setAttribute('aria-label', title);
    const symbol = text('span', kind === 'error' ? '!' : '♡', 'prototype-component-symbol'); symbol.setAttribute('aria-hidden', 'true');
    root.append(symbol, text('h2', title), text('p', message));
    if (action && onAction) root.append(componentButton(action, onAction, {variant: kind === 'error' ? 'secondary' : 'primary'}));
    return root;
  }
  function componentLoading({mode = 'skeleton', label = '正在加载…', value = 0} = {}) {
    const root = text('section', '', 'prototype-component-loading'); root.setAttribute('role', 'status'); root.setAttribute('aria-live', 'polite'); root.append(text('p', label));
    if (mode === 'progress') { const progress = document.createElement('progress'); progress.max = 100; progress.value = Math.max(0, Math.min(100, value)); progress.setAttribute('aria-label', label); root.append(progress); }
    else if (mode === 'spinner') { const spinner = text('span', '', 'prototype-component-spinner'); spinner.setAttribute('aria-hidden', 'true'); root.append(spinner); }
    else for (let i = 0; i < 3; i++) { const line = text('div', '', 'prototype-component-skeleton'); line.setAttribute('aria-hidden', 'true'); root.append(line); }
    return root;
  }
  function componentAvatar({name, src = null}) {
    const root = text('span', '', 'prototype-component-avatar'); root.setAttribute('role', 'img'); root.setAttribute('aria-label', name);
    const initials = text('span', [...name][0] || '♡'); initials.setAttribute('aria-hidden', 'true'); root.append(initials);
    if (src) { const image = document.createElement('img'); image.alt = ''; image.src = src; image.onerror = () => image.remove(); root.append(image); }
    return root;
  }
  function componentTag({label, selected = false, disabled = false, onChange = null}) {
    const button = componentButton(label, () => { const next = button.getAttribute('aria-pressed') !== 'true'; button.setAttribute('aria-pressed', String(next)); if (onChange) onChange(next); }, {variant: 'secondary', disabled});
    button.classList.add('prototype-component-tag'); button.setAttribute('aria-pressed', String(selected)); return button;
  }
  function componentDivider() { return text('hr', '', 'prototype-component-divider'); }
  async function modal({title, message = '', confirm = '知道了', cancel = null, content = null, actions: choices = null, sheet = false, beforeClose = null}) {
    if (activeModal) { await activeModal(false); if (activeModal) return null; }
    const trigger = document.activeElement;
    const dialog = document.createElement('dialog');
    dialog.className = 'prototype-modal' + (sheet ? ' prototype-sheet' : '');
    dialog.setAttribute('aria-labelledby', 'prototype-modal-title');
    dialog.setAttribute('aria-describedby', 'prototype-modal-message');
    const heading = text('h2', title); heading.id = 'prototype-modal-title';
    const copy = text('p', message); copy.id = 'prototype-modal-message';
    const actions = document.createElement('div'); actions.className = 'prototype-modal-actions';
    if (sheet) {
      const handle = document.createElement('div'); handle.className = 'prototype-sheet-handle'; handle.setAttribute('aria-hidden', 'true'); dialog.append(handle);
      let start = null, distance = 0;
      handle.addEventListener('pointerdown', event => { start = event.clientY; distance = 0; handle.setPointerCapture(event.pointerId); });
      handle.addEventListener('pointermove', event => { if (start === null) return; distance = Math.max(0, event.clientY - start); dialog.style.transform = `translateY(${distance}px)`; });
      const release = () => { if (start === null) return; start = null; dialog.style.transform = ''; if (distance > 80) activeModal(null); };
      handle.addEventListener('pointerup', release); handle.addEventListener('pointercancel', () => { start = null; dialog.style.transform = ''; });
    }
    dialog.append(heading);
    if (message) dialog.append(copy);
    else dialog.removeAttribute('aria-describedby');
    if (content) dialog.append(content);
    dialog.append(actions);
    document.body.append(dialog);
    const marker = 'dialog-' + Date.now();
    history.pushState({...history.state, prototypeOverlay: marker}, '', location.href);
    return new Promise(resolve => {
      let settled = false;
      let closing;
      let checking;
      function close(value = sheet ? null : false, fromHistory = false) {
        if (settled) return closing;
        if (checking) return checking;
        if (beforeClose) {
          checking = (async () => {
            const allowed = await beforeClose(value);
            checking = null;
            if (!allowed) {
              if (history.state?.prototypeOverlay !== marker) history.pushState({...history.state, prototypeOverlay: marker}, '', location.href);
              return false;
            }
            return finish(value, fromHistory);
          })();
          return checking;
        }
        return finish(value, fromHistory);
      }
      function finish(value, fromHistory) {
        if (settled) return closing;
        settled = true;
        closing = new Promise(done => {
          dialog.classList.add('prototype-closing');
          const reduced = reducedMotion();
          setTimeout(() => {
            dialog.close(); dialog.remove(); activeModal = null;
            if (trigger?.isConnected) trigger.focus();
            const complete = () => { resolve(value); done(value); };
            if (!fromHistory && history.state?.prototypeOverlay === marker) { pendingPop = complete; history.back(); }
            else complete();
          }, reduced ? 0 : sheet ? 220 : 160);
        });
        return closing;
      }
      activeModal = close;
      if (cancel && !sheet) {
        const button = componentButton(cancel, null, {variant: 'secondary'});
        button.addEventListener('click', () => close(false)); actions.append(button);
      }
      if (choices) choices.forEach((choice, index) => {
        const button = componentButton(choice.label, null, {variant: choice.danger ? 'danger' : 'secondary', disabled: !!choice.disabled});
        if (choice.danger) button.dataset.danger = 'true';
        button.addEventListener('click', () => close(choice.value === undefined ? index : choice.value)); actions.append(button);
      });
      else {
        const button = componentButton(confirm, null); button.dataset.primary = 'true';
        button.addEventListener('click', () => close(true)); actions.append(button);
      }
      if (sheet && cancel) {
        const button = componentButton(cancel, null, {variant: 'text'}); button.dataset.cancel = 'true';
        button.addEventListener('click', () => close(null)); actions.append(button);
      }
      dialog.addEventListener('cancel', event => { event.preventDefault(); close(); });
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
        if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) close();
      });
      dialog.showModal(); actions.querySelector('button').focus();
    });
  }
  const sheet = options => modal({...options, sheet: true, cancel: options.cancel || '取消'});
  function snapshot(form) {
    return JSON.stringify([...form.querySelectorAll('input,textarea,select')].map(e => [e.name || e.id, e.type === 'file' ? [...e.files].map(f => f.name) : e.type === 'checkbox' || e.type === 'radio' ? e.checked : e.value]));
  }
  function protectSheet(form) {
    let baseline = snapshot(form);
    return {
      commit: () => { baseline = snapshot(form); },
      beforeClose: () => {
        if (snapshot(form) === baseline) return true;
        const focus = document.activeElement, warning = text('section', '', 'prototype-sheet-discard');
        warning.setAttribute('role', 'alert');
        const heading = text('h3', '是否放弃当前修改？'), copy = text('p', '当前输入还没有保存。');
        const keep = text('button', '继续编辑'), drop = text('button', '放弃修改');
        keep.type = drop.type = 'button'; drop.dataset.danger = 'true';
        warning.append(heading, copy, keep, drop); form.after(warning); form.hidden = true; keep.focus();
        return new Promise(resolve => {
          const done = discard => { warning.remove(); form.hidden = false; if (!discard && focus?.isConnected) focus.focus(); resolve(discard); };
          keep.onclick = () => done(false); drop.onclick = () => done(true);
        });
      }
    };
  }
  function guard(form, {fallback, value = () => snapshot(form)} = {}) {
    let baseline = value();
    const state = {dirty: () => value() !== baseline, commit: () => { baseline = value(); }, fallback};
    navigationGuard = state;
    history.replaceState({...history.state, prototypeAnchor: true}, '', location.href);
    history.pushState({...history.state, prototypeGuard: true}, '', location.href);
    return state;
  }
  async function canLeave() {
    if (!navigationGuard?.dirty()) return true;
    const discard = await modal({title: '是否放弃当前修改？', message: '还没有保存的内容会被放弃。', cancel: '继续编辑', confirm: '放弃修改'});
    if (discard) navigationGuard.commit();
    return discard;
  }
  async function go(url, {replace = false, force = false} = {}) {
    if (!force && !await canLeave()) return false;
    if (force) navigationGuard?.commit();
    replace ? location.replace(url) : location.assign(url);
    return true;
  }
  async function busy(button, label, operation) {
    if (button.disabled) return false;
    const original = [...button.childNodes];
    button.disabled = true; button.setAttribute('aria-busy', 'true'); button.textContent = label;
    try { await new Promise(resolve => setTimeout(resolve, 550)); return await operation(); }
    catch (error) { toast(error.message || '操作没有完成，请再试一次', 'error'); return false; }
    finally { button.disabled = false; button.removeAttribute('aria-busy'); button.replaceChildren(...original); }
  }
  function performBack(fallback, fromPop = false) {
    let source;
    try { source = new URL(document.referrer); } catch {}
    if (source?.origin === location.origin && /\/pages\/m\d{2}-p\d{2}\.html$/.test(source.pathname) && history.length > 1) history.go(!fromPop && history.state?.prototypeGuard ? -2 : -1);
    else location.replace(fallback);
  }
  async function back(fallback) {
    if (activeModal) { await activeModal(); return; }
    if (await canLeave()) performBack(fallback);
  }
  addEventListener('popstate', async () => {
    if (pendingPop) { const complete = pendingPop; pendingPop = null; complete(); return; }
    if (activeModal) { await activeModal(undefined, true); return; }
    if (navigationGuard && history.state?.prototypeAnchor) {
      const allowed = await canLeave();
      if (allowed) performBack(navigationGuard.fallback, true);
      else history.pushState({...history.state, prototypeGuard: true}, '', location.href);
    }
  });
  addEventListener('beforeunload', event => { if (navigationGuard?.dirty()) { event.preventDefault(); event.returnValue = ''; } });
  document.addEventListener('click', event => {
    const anchor = event.target.closest('a[href]');
    if (!navigationGuard || !anchor || event.defaultPrevented || anchor.getAttribute('href').startsWith('#') || anchor.download || anchor.target) return;
    const url = new URL(anchor.href);
    if (url.origin !== location.origin) return;
    event.preventDefault(); go(url.href);
  });
  function failNext(operation) {
    if (sessionStorage.getItem('dujia-prototype-fail-next') !== operation) return false;
    sessionStorage.removeItem('dujia-prototype-fail-next'); return true;
  }
  function fieldError(field, message, existing = null) {
    field?.setAttribute('aria-invalid', String(!!message));
    if (existing) { existing.textContent = message; existing.setAttribute('role', 'alert'); existing.hidden = !message; if (message) existing.style.display = 'block'; }
    else if (message) toast(message, 'error');
    return !message;
  }
  function notReady(form) {
    if (form.dataset.prototypeReady === 'true') return;
    modal({title: '页面没有加载完成', message: '重新加载后可以继续填写，当前操作尚未提交。', confirm: '重新加载', cancel: '取消'}).then(reload => { if (reload) location.reload(); });
  }
  function read(key, fallback = null) {
    try { const value = localStorage.getItem(key); return value === null ? fallback : JSON.parse(value); }
    catch { return fallback; }
  }
  const storageGuards=new Map();
  const canWrite=(key,value)=>!storageGuards.has(key)||storageGuards.get(key)(value);
  const protectStorage=(key,check)=>storageGuards.set(key,check);
  function write(key, value) {
    try { if(!canWrite(key,value))return false;localStorage.setItem(key, JSON.stringify(value));window.PrototypePreferences?.afterWrite(key);return true; }
    catch { toast('本地空间不足，未能保存。请整理空间后再试', 'error'); return false; }
  }
  function primaryNav() {
    const page=location.pathname.split('/').pop()?.slice(0,7),groups=[
      {key:'home',pages:['m03-p01','m03-p02'],label:'首页',href:'m03-p02.html',path:'M3 10 12 3l9 7M5 9v12h14V9M9 21v-8h6v8'},
      {key:'moments',pages:['m04-p01','m04-p02'],label:'重要时刻',href:'m04-p01.html',path:'M12 20S3 15 3 8a5 5 0 0 1 9-3 5 5 0 0 1 9 3c0 7-9 12-9 12Z'},
      {key:'work',pages:['m05-p01'],label:'工坊',href:'m05-p01.html',path:'m4 20 13-13 3 3L7 23ZM15 3V1m6 5h2M5 4 3 2m7 4V4'},
      {key:'pet',pages:['m07-p01','m07-p03','m07-p04'],label:'宠物',href:'m07-p03.html',path:'M7 13c-3 3-4 7 0 8 2 1 3-1 5-1s3 2 5 1c4-1 3-5 0-8-3-3-7-3-10 0ZM4 6a2 3 0 1 0 0 .1M9 3a2 3 0 1 0 0 .1M15 3a2 3 0 1 0 0 .1M20 6a2 3 0 1 0 0 .1'},
      {key:'me',pages:['m06-p01'],label:'我的',href:'m06-p01.html',path:'M16 6a4 4 0 1 1-8 0 4 4 0 0 1 8 0ZM4 21v-3a8 8 0 0 1 16 0v3'}
    ],active=groups.find(group=>group.pages.includes(page));
    if(!active||document.querySelector('.prototype-primary-nav'))return;
    const nav=document.createElement('nav');nav.className='prototype-primary-nav';nav.setAttribute('aria-label','主导航');document.body.classList.add('prototype-primary-page');
    for(const tab of groups){const button=document.createElement('button');button.type='button';button.dataset.target=tab.href;button.setAttribute('aria-label',tab.label);if(tab.key===active.key)button.setAttribute('aria-current','page');
      const icon=document.createElementNS('http://www.w3.org/2000/svg','svg'),path=document.createElementNS('http://www.w3.org/2000/svg','path');icon.setAttribute('viewBox','0 0 24 24');icon.setAttribute('aria-hidden','true');path.setAttribute('d',tab.path);icon.append(path);const label=document.createElement('span');label.textContent=tab.label;button.append(icon,label);
      button.onclick=()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true});nav.append(button);
    }
    document.body.append(nav);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',primaryNav,{once:true});else primaryNav();
  window.PrototypeUI = {toast, modal, sheet, busy, back, go, guard, protectSheet, read, write, canWrite,protectStorage,failNext, fieldError, notReady,primaryNav,components:{button:componentButton,field:componentField,card:componentCard,header:componentHeader,state:componentState,loading:componentLoading,avatar:componentAvatar,tag:componentTag,divider:componentDivider}};
})();
