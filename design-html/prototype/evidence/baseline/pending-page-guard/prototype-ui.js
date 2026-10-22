/* Small native helpers for the HTML prototype. No network or framework. */
(() => {
  let toastTimer;
  let activeModal;
  let pendingPop;
  let navigationGuard;
  const formSubmissions = new WeakMap();
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
  const adaptedFields = new WeakMap(), canvasFields = new Set();
  function positionFieldError(field, error) {
    const canvas = error.parentElement, target = field.getBoundingClientRect(), area = canvas.getBoundingClientRect();
    const scale = canvas.offsetWidth / area.width, inset = 8;
    const left = Math.max(inset, Math.min((target.left - area.left) * scale, canvas.clientWidth - 160 - inset));
    error.style.left = left + 'px'; error.style.top = ((target.bottom - area.top) * scale + canvas.scrollTop + 4) + 'px';
    error.style.width = Math.min(Math.max(target.width * scale, 160), canvas.clientWidth - left - inset) + 'px';
    const controls = [...canvas.querySelectorAll('input,textarea,select,button,a,[role=button]')].filter(node => node !== field && node.getClientRects().length && getComputedStyle(node).visibility !== 'hidden' && getComputedStyle(node).opacity !== '0');
    const overlaps = () => { const r = error.getBoundingClientRect(); return controls.some(node => { const b = node.getBoundingClientRect(); return r.left < b.right && r.right > b.left && r.top < b.bottom && r.bottom > b.top; }); };
    if (overlaps()) {
      const below = error.style.top, originalWidth = error.style.width, originalLeft = error.style.left;
      const moveAbove = () => { const above = (target.top - area.top) * scale + canvas.scrollTop - error.offsetHeight - 4; if (above < inset) return false; error.style.top = above + 'px'; return !overlaps(); };
      let placed = moveAbove();
      if (!placed) {
        const width = Math.min(160, canvas.clientWidth - inset * 2); error.style.width = width + 'px';
        const candidates = [left, ...controls.flatMap(node => { const r = node.getBoundingClientRect(); return [(r.right - area.left) * scale + 4, (r.left - area.left) * scale - width - 4]; })]
          .map(value => Math.max(inset, Math.min(value, canvas.clientWidth - width - inset))).sort((a, b) => Math.abs(a - left) - Math.abs(b - left));
        for (const candidate of candidates) { error.style.left = candidate + 'px'; if (moveAbove()) { placed = true; break; } }
      }
      if (!placed) { error.style.top = below; error.style.width = originalWidth; error.style.left = originalLeft; }
    }
  }
  function componentButton(label, onClick, {variant = 'primary', disabled = false, name = null} = {}) {
    const button = text('button', label, 'prototype-component-button');
    button.type = 'button'; button.dataset.variant = variant; button.disabled = disabled;
    if (variant === 'danger') button.dataset.danger = 'true';
    if (name) button.setAttribute('aria-label', name);
    if (onClick) button.addEventListener('click', onClick);
    return button;
  }
  function componentField({label, name = '', value = '', placeholder = '', multiline = false, type = 'text', maxLength = null, disabled = false, required = false, options = null, element = null}) {
    if (element) {
      if (adaptedFields.has(element)) return adaptedFields.get(element);
      const canvas = element.closest('.screen');
      if (!canvas && !element.closest('dialog')) throw new Error('Existing fields require a screen canvas or dialog');
      let root = element;
      if (!canvas) {
        if (element.parentElement.tagName === 'LABEL') root = element.parentElement;
        else { root = text('label', '', 'prototype-component-field'); element.before(root); root.append(text('span', label || element.getAttribute('aria-label') || element.placeholder || element.name || '输入内容'), element); }
        root.classList.add('prototype-component-field');
      }
      const id = element.id || ('prototype-field-' + ++fieldSequence);
      element.id = id; element.dataset.prototypeField = canvas ? 'canvas' : 'dialog';
      if (!element.getAttribute('aria-label') && !element.getAttribute('aria-labelledby') && !element.labels?.length)
        element.setAttribute('aria-label', label || element.placeholder || element.name || '输入内容');
      const error = text('p', '', 'prototype-component-error'); error.id = 'prototype-canvas-error-' + ++fieldSequence;
      error.hidden = true; error.setAttribute('role', 'alert');
      if (canvas) { error.dataset.fieldLayout = 'canvas'; canvas.append(error); } else root.append(error);
      element.dataset.prototypeError = error.id;
      element.setAttribute('aria-describedby', [...new Set([...(element.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean), error.id])].join(' '));
      const result = {root, input: element, error, setError: message => fieldError(element, message, error)};
      adaptedFields.set(element, result); if (canvas) canvasFields.add(result);
      element.addEventListener('input', () => result.setError(''));
      return result;
    }
    const root = text('label', '', 'prototype-component-field'), id = 'prototype-field-' + ++fieldSequence;
    const input = document.createElement(options ? 'select' : multiline ? 'textarea' : 'input'), error = text('p', '', 'prototype-component-error');
    if (options) for (const [value, label] of options) { const option = text('option', label); option.value = value; input.append(option); }
    else if (!multiline) input.type = type;
    input.id = id; input.name = name; input.value = value; input.placeholder = placeholder; input.disabled = disabled; input.required = required;
    if (maxLength !== null && !options) input.maxLength = maxLength;
    error.id = id + '-error'; error.hidden = true; error.setAttribute('role', 'alert');
    const caption = text('span', label); caption.id = id + '-label';
    input.setAttribute('aria-labelledby', caption.id); input.setAttribute('aria-describedby', error.id); root.append(caption, input, error);
    const setError = message => fieldError(input, message, error);
    input.addEventListener('input', () => setError(''));
    return {root, input, error, setError};
  }
  function componentCard({title, message = '', onClick = null, selected = null, content = null}) {
    const root = document.createElement(onClick ? 'button' : 'article'); root.className = 'prototype-component-card';
    if (content !== null) root.append(...content); else root.append(text('h2', title), text('p', message));
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
  function componentTag({label, selected = false, disabled = false, onChange = null, onActivate = null}) {
    const button = componentButton(label, () => { if (selected === null) { if (onActivate) onActivate(); return; } const next = button.getAttribute('aria-pressed') !== 'true'; button.setAttribute('aria-pressed', String(next)); if (onChange) onChange(next); }, {variant: 'secondary', disabled});
    button.classList.add('prototype-component-tag'); if (selected !== null) button.setAttribute('aria-pressed', String(selected)); return button;
  }
  function componentDivider() { return text('hr', '', 'prototype-component-divider'); }
  async function modal({title, message = '', confirm = '知道了', cancel = null, content = null, actions: choices = null, sheet = false, beforeClose = null, danger = false}) {
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
    for (const field of dialog.querySelectorAll('input:not([type=hidden],[type=file],[type=color],[type=range],[type=checkbox],[type=radio]),textarea,select'))
      if (!field.closest('.prototype-component-field')) componentField({element: field});
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
        const button = componentButton(confirm, null, {variant: danger ? 'danger' : 'primary'}); if (!danger) button.dataset.primary = 'true';
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
        if (event.shiftKey && (document.activeElement === first || document.activeElement === heading)) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      });
      dialog.addEventListener('click', event => {
        if (event.target !== dialog) return;
        const r = dialog.getBoundingClientRect();
        if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) close();
      });
      const formEntry = dialog.querySelector('form') && !dialog.querySelector('[data-danger=true]');
      if (formEntry) { heading.tabIndex = -1; heading.setAttribute('autofocus', ''); }
      dialog.showModal();
      if (formEntry) { heading.focus({preventScroll: true}); dialog.scrollTop = 0; }
      else actions.querySelector('button').focus();
    });
  }
  const sheet = options => modal({...options, sheet: true, cancel: options.cancel || '取消'});
  const snapshotFieldKeys = new WeakMap(); let snapshotFieldSequence = 0;
  function snapshotFieldKey(field) {
    if (field.name) return field.name;
    if (!snapshotFieldKeys.has(field)) snapshotFieldKeys.set(field, ++snapshotFieldSequence);
    return snapshotFieldKeys.get(field);
  }
  function snapshot(form) {
    return JSON.stringify([...form.querySelectorAll('input,textarea,select')].map(e => [snapshotFieldKey(e), e.type === 'file' ? [...e.files].map(f => f.name) : e.type === 'checkbox' || e.type === 'radio' ? e.checked : e.value]));
  }
  function protectSheet(form) {
    let baseline = snapshot(form);
    return {
      commit: () => { baseline = snapshot(form); const submission = formSubmissions.get(form); if (submission) submission.committed = true; },
      beforeClose: () => {
        const submission = formSubmissions.get(form);
        if (submission && !submission.committed) {
          if (submission.started) { toast('正在完成保存，请稍候'); return false; }
          // Closing cancels the pending attempt even when the user keeps editing.
          submission.cancelled = true;
        }
        if (snapshot(form) === baseline) return true;
        const focus = document.activeElement, warning = text('section', '', 'prototype-sheet-discard');
        warning.setAttribute('role', 'alert');
        const heading = text('h3', '是否放弃当前修改？'), copy = text('p', '当前输入还没有保存。');
        const keep = componentButton('继续编辑', null, {variant: 'secondary'}), drop = componentButton('放弃修改', null, {variant: 'danger'});
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
    const state = {dirty: () => value() !== baseline, commit: () => { baseline = value(); }, fallback, complete: async url => {
      baseline = value();
      // Remove the guard sentinel and replace its anchor after a successful task.
      if (history.state?.prototypeGuard) await new Promise(resolve => { pendingPop = resolve; history.back(); });
      return go(url, {replace: true, force: true});
    }};
    navigationGuard = state;
    history.replaceState({...history.state, prototypeAnchor: true}, '', location.href);
    history.pushState({...history.state, prototypeGuard: true}, '', location.href);
    return state;
  }
  async function canLeave() {
    if (!navigationGuard?.dirty()) return true;
    const discard = await modal({title: '是否放弃当前修改？', message: '还没有保存的内容会被放弃。', cancel: '继续编辑', confirm: '放弃修改', danger: true});
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
    const original = [...button.childNodes], form = button.closest('form');
    const submission = {cancelled: false, started: false, committed: false};
    if (form) formSubmissions.set(form, submission);
    button.disabled = true; button.setAttribute('aria-busy', 'true'); button.textContent = label;
    try {
      await new Promise(resolve => setTimeout(resolve, 550));
      if (submission.cancelled || !button.isConnected) return false;
      submission.started = true;
      return await operation();
    }
    catch (error) { toast(error.message || '操作没有完成，请再试一次', 'error'); return false; }
    finally { if (form && formSubmissions.get(form) === submission) formSubmissions.delete(form); button.disabled = false; button.removeAttribute('aria-busy'); button.replaceChildren(...original); }
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
      // Restore the sentinel before awaiting the dialog, so an immediate second
      // Back cannot leave while its close/history callback is still settling.
      if (!history.state?.prototypeGuard) history.pushState({...history.state, prototypeGuard: true}, '', location.href);
      const allowed = await canLeave();
      if (allowed) performBack(navigationGuard.fallback);
      else if (!history.state?.prototypeGuard) history.pushState({...history.state, prototypeGuard: true}, '', location.href);
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
    if (!existing) existing = adaptedFields.get(field)?.error || field?.closest('.prototype-component-field')?.querySelector('.prototype-component-error') || null;
    field?.setAttribute('aria-invalid', String(!!message));
    if (existing) { existing.textContent = message; existing.setAttribute('role', 'alert'); existing.hidden = !message; if (message) { existing.style.display = 'block'; if (existing.dataset.fieldLayout === 'canvas') positionFieldError(field, existing); } }
    else if (message) toast(message, 'error');
    return !message;
  }
  function notReady(form) {
    if (form.dataset.prototypeReady === 'true') return;
    modal({title: '页面没有加载完成', message: '重新加载后可以继续填写，当前操作尚未提交。', confirm: '重新加载', cancel: '取消'}).then(reload => { if (reload) location.reload(); });
  }
  const accountKeys=['dujia-profile','dujia-prototype-relationship','dujia-prototype-session','dujia-prototype-invite'];
  let accountRecoveryOpen=false,accountRepairKey=null,accountButton,accountLastPrompt;
  const plain=value=>value&&typeof value==='object'&&!Array.isArray(value);
  function accountAnalyze(key,raw){
    const state={key,raw,value:key==='dujia-prototype-session'?{loggedIn:false}:{},issues:[]};if(raw===null)return state;
    let value;try{value=JSON.parse(raw);}catch{state.issues.push('资料暂时无法解析');return state;}
    if(!plain(value)){state.issues.push('资料格式不正确');return state;}
    const cleanProfile=input=>{
      const next={...input};
      for(const field of ['nickname','saying','birthday','color','met','anniversary'])if(Object.hasOwn(next,field)&&typeof next[field]!=='string'){delete next[field];state.issues.push('有无法读取的资料字段');}
      if(Object.hasOwn(next,'avatar')&&next.avatar!==null&&typeof next.avatar!=='string'){delete next.avatar;state.issues.push('头像格式不正确');}
      if(Object.hasOwn(next,'aliases')&&(!Array.isArray(next.aliases)||next.aliases.some(v=>typeof v!=='string'))){next.aliases=Array.isArray(next.aliases)?next.aliases.filter(v=>typeof v==='string'):[];state.issues.push('曾用昵称格式不正确');}
      return next;
    };
    state.value=key==='dujia-profile'?cleanProfile(value):{...value};
    const next=state.value;
    for(const field of ['createdAt','updatedAt',...(key==='dujia-prototype-relationship'?['acceptedAt','unlinkedAt','unlinkRejectedAt']:[])])if(Object.hasOwn(next,field)&&!Number.isFinite(next[field])){delete next[field];state.issues.push('资料时间格式不正确');}
    if(key==='dujia-prototype-relationship'){
      if(Object.hasOwn(next,'bound')&&typeof next.bound!=='boolean'){next.bound=false;state.issues.push('关联状态格式不正确');}
      for(const field of ['id','partner','usedInvitation'])if(Object.hasOwn(next,field)&&typeof next[field]!=='string'){delete next[field];if(field==='partner')next.bound=false;state.issues.push('关联资料格式不正确');}
      if(Object.hasOwn(next,'profile')){if(plain(next.profile))next.profile=cleanProfile(next.profile);else{next.profile={};state.issues.push('共同资料格式不正确');}}
      if(next.unlinkPending!=null&&!plain(next.unlinkPending)){next.unlinkPending=null;state.issues.push('解除请求格式不正确');}
    }
    if(key==='dujia-prototype-session'){
      if(Object.hasOwn(next,'loggedIn')&&typeof next.loggedIn!=='boolean'){state.issues.push('登录状态格式不正确');}
      if(Object.hasOwn(next,'phone')&&(typeof next.phone!=='string'||(next.phone!==''&&!/^1\d{10}$/.test(next.phone))||(next.loggedIn===true&&!next.phone))){delete next.phone;state.issues.push('登录手机号格式不正确');}
      if(state.issues.length)next.loggedIn=false;
    }
    if(key==='dujia-prototype-invite'){
      if(Object.hasOwn(next,'code')&&(typeof next.code!=='string'||! /^[A-Z0-9]{8}$/.test(next.code))){delete next.code;state.issues.push('邀请码格式不正确');}
      if(Object.hasOwn(next,'status')&&!['pending','accepted','expired'].includes(next.status)){next.status='expired';state.issues.push('邀请状态格式不正确');}
      for(const field of ['expiresAt','autoAt'])if(Object.hasOwn(next,field)&&!Number.isFinite(next[field])){delete next[field];state.issues.push('邀请时间格式不正确');}
      if(Object.hasOwn(next,'partner')&&typeof next.partner!=='string'){delete next.partner;state.issues.push('邀请对象格式不正确');}
      if(next.status==='pending'&&(!next.code||!Number.isFinite(next.expiresAt)))state.issues.push('邀请信息不完整');
      if(state.issues.length)next.status='expired';
    }
    return state;
  }
  function accountInspect(key){try{return accountAnalyze(key,localStorage.getItem(key));}catch{return {key,raw:null,value:{},issues:['浏览器暂时无法访问资料'],unavailable:true};}}
  const accountProblem=()=>accountKeys.map(accountInspect).find(state=>state.issues.length);
  function observeAccount(){
    const state=accountProblem();if(!state){accountButton?.remove();accountButton=null;accountLastPrompt=undefined;return;}
    if(!accountButton){accountButton=componentButton('恢复资料',()=>recoverAccount(),{variant:'secondary'});accountButton.classList.add('prototype-account-recovery');document.body.append(accountButton);}
    const signature=state.key+'\0'+state.raw;if(accountLastPrompt!==signature){accountLastPrompt=signature;queueMicrotask(()=>recoverAccount());}
  }
  async function recoverAccount(){
    if(accountRecoveryOpen)return;accountRecoveryOpen=true;
    try{while(true){
      const state=accountProblem();if(!state){observeAccount();return;}
      const name={'dujia-profile':'个人资料','dujia-prototype-relationship':'关系资料','dujia-prototype-session':'登录资料','dujia-prototype-invite':'邀请资料'}[state.key];
      const action=await modal({title:'资料需要恢复',message:state.unavailable?'浏览器暂时无法访问资料，请检查存储设置或重新检查。':name+'的部分内容暂时无法读取。原始内容仍完整保留；恢复前暂停普通保存，避免覆盖资料或写入错误身份。',cancel:'稍后处理',actions:[{label:'导出原始资料',value:'export',disabled:!!state.unavailable},{label:'恢复可读资料',value:'repair',disabled:!!state.unavailable},{label:'重新检查',value:'retry'}]});
      if(!action)return;
      if(action==='export'){
        const url=URL.createObjectURL(new Blob([state.raw],{type:'application/json;charset=utf-8'})),link=document.createElement('a');link.href=url;link.download='独家童话'+name+'原始内容.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);continue;
      }
      if(action==='retry'){if(!accountProblem()){observeAccount();await go(location.href,{replace:true});return;}continue;}
      if(!await modal({title:'保留原始副本并恢复资料？',message:(state.key==='dujia-prototype-session'?'恢复后将退出登录，请重新登录。':'')+'先完整保留原始副本，再恢复可读字段。无法读取的字段仍在副本中；缺失的资料可重新填写。当前记录和草稿不会被删除。',cancel:'取消',confirm:'确认恢复', danger: true}))continue;
      if(localStorage.getItem(state.key)!==state.raw){toast('资料已在其他页面更新，请重新检查','error');observeAccount();return;}
      if(!write('dujia-prototype-account-recovery-'+crypto.randomUUID(),state.raw))return;
      if(localStorage.getItem(state.key)!==state.raw){toast('资料已在其他页面更新，请重新检查','error');observeAccount();return;}
      accountRepairKey=state.key;let saved;try{saved=write(state.key,state.value);}finally{accountRepairKey=null;}
      if(!saved)return;
      toast('已保留原始副本并恢复资料','success');observeAccount();await go(location.href,{replace:true});return;
    }}finally{accountRecoveryOpen=false;}
  }
  const WORK_KEY='dujia-prototype-works';
  let workRecoveryOpen=false,workRecoveryButton,workPromptRaw,workRepairing=false;
  function workAnalyze(raw) {
    const state={raw,items:[],issues:[]};if(raw===null)return state;
    let items;try{items=JSON.parse(raw);}catch{state.issues.push('作品文件暂时无法解析');return state;}
    if(!Array.isArray(items)){state.issues.push('作品集合格式不正确');return state;}
    const ids=new Set();
    for(const item of items){
      if(!plain(item)||typeof item.id!=='string'||!item.id.trim()||ids.has(item.id)){state.issues.push('部分作品暂时无法读取');continue;}
      ids.add(item.id);const next={...item};
      for(const field of ['name','story'])if(typeof next[field]!=='string'){next[field]='';state.issues.push('作品文字暂时无法读取');}
      for(const [field,allowed,fallback]of [['type',['comic','film'],'comic'],['sourceKind',['free','diary','photo','moment'],'free'],['status',['draft','generating','failed','ready'],'draft']])if(!allowed.includes(next[field])){next[field]=fallback;state.issues.push('作品状态或类型暂时无法读取');}
      if(!Array.isArray(next.sourceIds)||next.sourceIds.some(v=>typeof v!=='string'||!v.trim())){next.sourceIds=Array.isArray(next.sourceIds)?next.sourceIds.filter(v=>typeof v==='string'&&v.trim()):[];state.issues.push('作品素材引用暂时无法读取');}
      for(const field of ['style','mode','mood'])if(next[field]!=null&&typeof next[field]!=='string'){delete next[field];state.issues.push('作品偏好暂时无法读取');}
      for(const field of ['favorite','willFail'])if(next[field]!=null&&typeof next[field]!=='boolean'){delete next[field];state.issues.push('作品标记暂时无法读取');}
      for(const field of ['createdAt','updatedAt','startedAt','dueAt','completedAt'])if(next[field]!=null&&!Number.isFinite(next[field])){delete next[field];state.issues.push('作品时间暂时无法读取');}
      if(next.status==='generating'&&(!Number.isFinite(next.startedAt)||!Number.isFinite(next.dueAt)||next.dueAt<next.startedAt||(item.willFail!=null&&typeof item.willFail!=='boolean'))){next.status='draft';state.issues.push('生成时间不完整，恢复为保留输入的草稿');}
      if(next.characters!=null&&(!plain(next.characters)||Object.values(next.characters).some(v=>typeof v!=='string'))){next.characters=plain(next.characters)?Object.fromEntries(Object.entries(next.characters).filter(([,v])=>typeof v==='string')):{};state.issues.push('共同主角部分字段暂时无法读取');}
      state.items.push(next);
    }
    return state;
  }
  function inspectWorks(){try{return workAnalyze(localStorage.getItem(WORK_KEY));}catch{return {raw:null,items:[],issues:['浏览器暂时无法访问作品'],unavailable:true};}}
  function observeWorks(){
    if(document.readyState==='loading')return;
    const state=inspectWorks();if(!state.issues.length){workRecoveryButton?.remove();workRecoveryButton=null;workPromptRaw=undefined;return;}
    if(!workRecoveryButton){workRecoveryButton=componentButton('恢复作品',recoverWorks,{variant:'secondary'});workRecoveryButton.classList.add('prototype-work-recovery');document.body.append(workRecoveryButton);}
    if(!accountProblem()&&window.PrototypeRecords?.health()?.issues.length){window.PrototypeRecords.all();return;}
    if(workPromptRaw!==state.raw&&!activeModal&&!accountProblem()){workPromptRaw=state.raw;queueMicrotask(recoverWorks);}
  }
  async function recoverWorks(){
    if(accountProblem())return recoverAccount();
    if(window.PrototypeRecords?.health()?.issues.length)return window.PrototypeRecords.recover();
    if(workRecoveryOpen)return;workRecoveryOpen=true;
    try{while(true){
      const state=inspectWorks();if(!state.issues.length){observeWorks();return;}
      const action=await modal({title:'作品需要恢复',message:state.unavailable?'暂时无法访问本地作品，请检查浏览器存储设置或重新检查。':`原始作品仍完整保留，可读取 ${state.items.length} 件。暂时停止保存作品，避免覆盖原文。可先导出原文，再保留副本后恢复。`,cancel:'稍后处理',actions:[{label:'导出原始作品',value:'export',disabled:!!state.unavailable},{label:'恢复可读作品',value:'repair',disabled:!!state.unavailable},{label:'重新检查',value:'retry'}]});
      if(!action)return;
      if(action==='export'){const url=URL.createObjectURL(new Blob([state.raw],{type:'application/json;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download='独家童话作品原始内容.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);continue;}
      if(action==='retry'){if(!inspectWorks().issues.length){observeWorks();await go(location.href,{replace:true});return;}continue;}
      if(!await modal({title:'保留原始副本并恢复作品？',message:`先完整保留原文，再恢复 ${state.items.length} 件可读作品。无法读取的字段仍保留在副本中；无效生成时间会保留输入为草稿，不自动生成结果。`,cancel:'取消',confirm:'确认恢复',danger:true}))continue;
      if(localStorage.getItem(WORK_KEY)!==state.raw){toast('作品已在其他页面更新，请重新检查','error');observeWorks();return;}
      if(!write('dujia-prototype-work-recovery-'+crypto.randomUUID(),state.raw))return;
      if(localStorage.getItem(WORK_KEY)!==state.raw){toast('作品已在保存副本期间更新，尚未替换','error');observeWorks();return;}
      let saved;workRepairing=true;try{saved=write(WORK_KEY,state.items);}finally{workRepairing=false;}
      if(!saved)return;
      toast('已保留原始副本并恢复作品','success');observeWorks();await go(location.href,{replace:true});return;
    }}catch{toast('暂时无法恢复作品，原文仍保留，请重试','error');}finally{workRecoveryOpen=false;}
  }
  const timeNames={'dujia-prototype-moments':'时刻','dujia-prototype-anniversaries':'纪念日','dujia-prototype-capsules':'胶囊','dujia-prototype-pet':'宠物','dujia-prototype-books':'回忆册'};
  let timeRecoveryOpen=false,timeRepairKey=null,timePrompt, timeButton;
  function structuredCollection(state,values){
    const petKey=state.key==='dujia-prototype-pet',issue=message=>state.issues.push(message);
    const id=value=>plain(value)&&typeof value.id==='string'&&!!value.id.trim();
    const textFields=(value,fields)=>{for(const field of fields){if(value[field]===undefined||value[field]===null&&['outfit','adoptedDate','lastPage','image','emoji'].includes(field))continue;if(typeof value[field]!=='string'){value[field]='';issue('文字字段暂时无法读取');}}return value;};
    const strings=(value,field)=>{if(value[field]===undefined){value[field]=[];return;}if(!Array.isArray(value[field])||value[field].some(v=>typeof v!=='string')){value[field]=Array.isArray(value[field])?value[field].filter(v=>typeof v==='string'):[];issue('列表字段暂时无法读取');}};
    const children=(values,transform,stable=true)=>{if(values===undefined)return [];if(!Array.isArray(values)){issue('内容列表格式不正确');return [];}const seen=new Set(),result=[];for(const child of values){if(!plain(child)||stable&&(!id(child)||seen.has(child.id))){issue('部分内容或重复ID暂时无法读取');continue;}if(stable)seen.add(child.id);result.push(transform({...child}));}return result;};
    const references=value=>{if(value==null||value===false)return true;return plain(value)&&typeof value.kind==='string'&&typeof value.id==='string'&&!!value.id.trim();};
    const referenceList=value=>children(value,item=>item,false).filter(item=>{if(references(item))return true;issue('关联引用暂时无法读取');return false;});
    const times=(value,fields)=>{for(const field of fields)if(value[field]!=null&&!Number.isFinite(value[field])){delete value[field];issue('时间字段暂时无法读取');}};
    if(petKey){
      state.value=null;if(values===null||Array.isArray(values)&&values.length===0)return state;
      if(!id(values)){issue('宠物格式或ID无法读取');return state;}
      const pet={...values};textFields(pet,['name','kind','requestedBy','adoptedDate','outfit','lastInteraction','lastReward','lastRoom']);
      pet.name=pet.name??'';pet.kind=pet.kind??'';
      if(!['pending','active','rejected'].includes(pet.status)){pet.status='pending';state.uncertainStatus=true;issue('领养状态无法读取，等待重新确认');}
      for(const field of ['energy','satiety','mood','affinity','gifts','coins','stars']){if(pet[field]===undefined)pet[field]=0;else if(!Number.isFinite(pet[field])||pet[field]<0||['energy','satiety','mood'].includes(field)&&pet[field]>100){pet[field]=0;issue('宠物数值无法读取，不补发资源');}}
      if(pet.food===undefined)pet.food=[0,0,0];else if(!Array.isArray(pet.food)||pet.food.length!==3||pet.food.some(v=>!Number.isInteger(v)||v<0)){pet.food=[0,1,2].map(i=>Array.isArray(pet.food)&&Number.isInteger(pet.food[i])&&pet.food[i]>=0?pet.food[i]:0);issue('食物库存无法读取，不补发食物');}
      for(const field of ['owned','ownedRoom','claims','favorites'])strings(pet,field);
      for(const field of ['room','settings']){if(pet[field]===undefined)pet[field]={};else if(!plain(pet[field])){pet[field]={};issue('宠物设置或小屋无法读取');}}
      for(const key of Object.keys(pet.room))if(typeof pet.room[key]!=='string'){delete pet.room[key];issue('小屋物品无法读取');}
      for(const field of ['reminder','notice','stories'])if(pet.settings[field]!=null&&typeof pet.settings[field]!=='boolean'){pet.settings[field]=false;issue('宠物设置开关无法读取');}
      if(pet.settings.time!=null&&(typeof pet.settings.time!=='string'||!/^([01]\d|2[0-3]):[0-5]\d$/.test(pet.settings.time))){delete pet.settings.time;pet.settings.reminder=false;issue('提醒时间无法读取，暂停提醒');}
      if(pet.care===undefined)pet.care=false;else if(typeof pet.care!=='boolean'){pet.care=false;issue('共同照顾开关无法读取，暂停照顾');}
      pet.logs=children(pet.logs,entry=>{textFields(entry,['type','text','actor','date','sourceId','sourceKind','claimKey','achievementId']);entry.type=entry.type??'';entry.text=entry.text??'';entry.date=entry.date??'';times(entry,['at']);if(entry.story!=null&&typeof entry.story!=='boolean'){entry.story=false;issue('成长故事开关无法读取');}entry.comments=children(entry.comments,comment=>{textFields(comment,['author','text']);comment.author=comment.author??'';comment.text=comment.text??'';times(comment,['at','createdAt']);return comment;});if(entry.type==='play'){const delta=entry.delta;entry.delta={};for(const field of ['energy','affinity','mood']){entry.delta[field]=plain(delta)&&Number.isFinite(delta[field])?delta[field]:0;if(delta!==undefined&&(!plain(delta)||!Number.isFinite(delta[field])))issue('互动变化无法读取');}}return entry;});
      times(pet,['requestedAt','lastReminder']);state.value=pet;state.items=[pet];return state;
    }
    if(!Array.isArray(values)){issue('回忆册集合格式不正确');return state;}
    state.items=children(values,book=>{
      textFields(book,['name','start','theme','lastPage']);book.name=book.name??'';book.theme=book.theme??'';
      if(book.dates===undefined)book.dates=['',''];else if(!Array.isArray(book.dates)||book.dates.length!==2||book.dates.some(v=>typeof v!=='string')){book.dates=['',''];issue('册月份暂时无法读取');}
      if(!['draft','published'].includes(book.status)){book.status='draft';issue('册状态无法读取，恢复为草稿');}
      if(book.archived!=null&&typeof book.archived!=='boolean'){book.archived=false;issue('归档状态无法读取');}
      if(!references(book.coverPhoto)){book.coverPhoto=false;issue('封面引用暂时无法读取');}
      book.selected=referenceList(book.selected);if(book.skipped!==undefined)book.skipped=referenceList(book.skipped);strings(book,'bookmarks');times(book,['createdAt','updatedAt']);
      book.chapters=children(book.chapters,chapter=>{textFields(chapter,['name']);chapter.name=chapter.name??'';return chapter;});
      book.pages=children(book.pages,page=>{
        textFields(page,['title','body','date','message','template','chapterId']);page.template=page.template??'日记摘录';
        if(!references(page.source)){delete page.source;page.sourceUnavailable=true;issue('书页来源引用无法读取，暂停展示关联内容');}
        if(!references(page.photoSource)){delete page.photoSource;issue('书页照片引用无法读取');}
        if(page.photos!==undefined)page.photos=children(page.photos,photo=>photo,false).filter(photo=>{if(!references(photo.source)){issue('照片来源引用无法读取');return false;}if(photo.crop!=null&&(!plain(photo.crop)||!Number.isFinite(photo.crop.x)||!Number.isFinite(photo.crop.y)||!Number.isFinite(photo.crop.zoom))){delete photo.crop;issue('照片裁剪参数无法读取');}return true;});
        if(page.supplements!==undefined)page.supplements=children(page.supplements,item=>textFields(item,['text','emoji','image','date','author','kind']),false);return page;
      });return book;
    });return state;
  }
  function collectionAnalyze(key,raw){
    const state={key,raw,items:[],issues:[]};if(key==='dujia-prototype-pet')state.value=null;if(raw===null)return state;
    let values;try{values=JSON.parse(raw);}catch{state.issues.push('内容暂时无法解析');return state;}
    if(['dujia-prototype-pet','dujia-prototype-books'].includes(key))return structuredCollection(state,values);
    if(!Array.isArray(values)){state.issues.push('集合格式不正确');return state;}
    const ids=new Set();
    for(const item of values){
      if(!plain(item)||typeof item.id!=='string'||!item.id.trim()||ids.has(item.id)){state.issues.push('部分条目暂时无法读取');continue;}
      ids.add(item.id);const next={...item},isMoment=key==='dujia-prototype-moments',isCapsule=key==='dujia-prototype-capsules';
      if(typeof next.name!=='string'){next.name='';state.issues.push('名称暂时无法读取');}
      for(const field of isMoment?['story','date','type','capsuleId']:isCapsule?['message','opening','momentId']:['date','type','momentId'])if(next[field]!=null&&typeof next[field]!=='string'){next[field]='';state.issues.push('文字或引用字段暂时无法读取');}
      for(const field of isMoment?['cover']:isCapsule?['photo']:[])if(next[field]!=null&&typeof next[field]!=='string'){next[field]=null;state.issues.push('图片暂时无法读取');}
      for(const field of ['createdAt','updatedAt',...(isCapsule?['openedAt']:[])])if(next[field]!=null&&!Number.isFinite(next[field])){delete next[field];state.issues.push('时间格式不正确');}
      for(const field of isCapsule?['reminder']:isMoment?[]:['enabled','reminder'])if(next[field]!=null&&typeof next[field]!=='boolean'){next[field]=false;state.issues.push('提醒开关格式不正确');}
      if(!isMoment&&!isCapsule){
        if(next.repeat!=null&&!['boolean','string'].includes(typeof next.repeat)){next.repeat=false;state.issues.push('重复设置格式不正确');}
        if(next.reminderDays!=null&&(!Number.isInteger(next.reminderDays)||next.reminderDays<0)){next.reminderDays=0;next.enabled=false;state.issues.push('提醒间隔格式不正确');}
      }
      if(next.visibility!=null&&!['private','shared'].includes(next.visibility)){next.visibility='private';state.issues.push('可见范围格式不正确，恢复为仅自己可见');}
      if(isCapsule&&!['draft','sealed','opened'].includes(next.status)){next.status='draft';state.issues.push('胶囊状态无法读取，恢复为草稿');}
      if(isMoment){
        if(next.status!=null&&!['draft','published'].includes(next.status)){next.status='draft';state.issues.push('时刻状态无法读取，恢复为草稿');}
        for(const field of ['related','sourceIds'])if(next[field]!=null&&(!Array.isArray(next[field])||next[field].some(v=>typeof v!=='string'||!v.trim()))){next[field]=Array.isArray(next[field])?next[field].filter(v=>typeof v==='string'&&v.trim()):[];state.issues.push('关联内容引用暂时无法读取');}
        if(next.comments!=null){const seen=new Set(),comments=[];if(Array.isArray(next.comments))for(const comment of next.comments){if(!plain(comment)||typeof comment.id!=='string'||!comment.id.trim()||seen.has(comment.id)||typeof comment.author!=='string'||typeof comment.text!=='string'||comment.createdAt!=null&&!Number.isFinite(comment.createdAt)){state.issues.push('部分回应暂时无法读取');continue;}seen.add(comment.id);if(comment.read!=null&&typeof comment.read!=='boolean'){comments.push({...comment,read:false});state.issues.push('回应已读状态无法读取');}else comments.push(comment);}else state.issues.push('回应列表格式不正确');next.comments=comments;}
      }
      state.items.push(next);
    }
    return state;
  }
  function collectionHealth(key){try{return collectionAnalyze(key,localStorage.getItem(key));}catch{return {key,raw:null,items:[],issues:['浏览器暂时无法访问内容'],unavailable:true};}}
  const timeProblem=()=>Object.keys(timeNames).map(collectionHealth).find(v=>v.issues.length);
  function observeTime(){
    if(document.readyState==='loading')return;
    const state=timeProblem();if(!state){timeButton?.remove();timeButton=null;timePrompt=undefined;return;}
    if(!timeButton){timeButton=componentButton('',()=>recoverCollection(timeProblem()?.key),{variant:'secondary'});timeButton.classList.add('prototype-time-recovery');document.body.append(timeButton);}timeButton.textContent='恢复'+timeNames[state.key];timeButton.hidden=[...document.querySelectorAll('[data-collection-recovery-key]')].some(node=>node.dataset.collectionRecoveryKey===state.key&&node.getClientRects().length&&!node.closest('[hidden]'));
    if(accountProblem())return;
    if(window.PrototypeRecords?.health().issues.length){window.PrototypeRecords.all();return;}
    if(inspectWorks().issues.length){observeWorks();return;}
    if(window.PrototypePreferences?.tagHealth().issues.length){window.PrototypePreferences.tags();return;}
    const signature=state.key+'\0'+state.raw;if(timePrompt!==signature&&!activeModal&&!timeRecoveryOpen){timePrompt=signature;queueMicrotask(()=>recoverCollection(state.key));}
  }
  async function recoverCollection(key){
    if(accountProblem())return recoverAccount();
    if(window.PrototypeRecords?.health().issues.length)return window.PrototypeRecords.recover();
    if(inspectWorks().issues.length)return recoverWorks();
    if(window.PrototypePreferences?.tagHealth().issues.length)return window.PrototypePreferences.recoverTags();
    if(timeRecoveryOpen||!timeNames[key])return;timeRecoveryOpen=true;
    try{while(true){
      const state=collectionHealth(key),name=timeNames[key];if(!state.issues.length){observeTime();return;}timePrompt=state.key+'\0'+state.raw;
      const action=await modal({title:name+'需要恢复',message:state.unavailable?'暂时无法访问本地内容，请检查存储设置或重新检查。':`原始内容仍完整保留，可读取 ${state.items.length} 条${name}。恢复前暂停该集合保存和删除，避免覆盖原文。`,cancel:'稍后处理',actions:[{label:'导出原始'+name,value:'export',disabled:!!state.unavailable},{label:'恢复可读'+name,value:'repair',disabled:!!state.unavailable},{label:'重新检查',value:'retry'}]});
      if(!action)return;
      if(action==='export'){const url=URL.createObjectURL(new Blob([state.raw],{type:'application/json;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download='独家童话'+name+'原始内容.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);continue;}
      if(action==='retry'){if(!collectionHealth(key).issues.length){observeTime();await go(location.href,{replace:true});return;}continue;}
      if(!await modal({title:'保留原始副本并恢复'+name+'？',message:`先完整保存原始副本，再恢复 ${state.items.length} 条可读内容。无法读取的字段仍在副本中；状态无法读取时，胶囊和回忆册恢复为草稿；宠物等待重新确认，不自动领养或发放奖励。关联记录本身不删除。`,cancel:'取消',confirm:'确认恢复',danger:true}))continue;
      if(localStorage.getItem(key)!==state.raw){toast('内容已在其他页面更新，请重新检查','error');observeTime();return;}
      if(!write(key+'-recovery-'+crypto.randomUUID(),state.raw))return;
      if(localStorage.getItem(key)!==state.raw){toast('内容已在保存副本期间更新，尚未替换','error');observeTime();return;}
      timeRepairKey=key;let saved;try{saved=write(key,Object.hasOwn(state,'value')?state.value:state.items);}finally{timeRepairKey=null;}if(!saved)return;
      if(state.uncertainStatus)sessionStorage.removeItem('dujia-prototype-peer-pet');toast('已保留原始副本并恢复'+name,'success');observeTime();await go(location.href,{replace:true});return;
    }}catch{toast('暂时无法恢复内容，原文仍保留，请重试','error');}finally{timeRecoveryOpen=false;if(collectionHealth(key).issues.length)observeTime();}
  }
  function collectionState(key,{title,action,fallback}){
    const damaged=collectionHealth(key).issues.length>0;
    const root=componentState({kind:damaged?'error':'empty',title:damaged?timeNames[key]+'数据需要恢复':title,message:damaged?'部分内容暂时无法读取，原始内容仍保留。先恢复可读内容，再检查这条记录。':'内容可能已被删除，返回列表可以继续浏览。',action:damaged?'恢复'+timeNames[key]:action,onAction:()=>damaged?(collectionHealth(key).issues.length?recoverCollection(key):go(location.href,{replace:true})):go(typeof fallback==='function'?fallback():fallback,{force:true})});
    if(damaged){root.dataset.collectionRecoveryKey=key;queueMicrotask(observeTime);}return root;
  }
  function collectionGuard(screen,key){if(!collectionHealth(key).issues.length)return false;screen.classList.add('prototype-collection-blocked');const state=collectionState(key,{title:'',action:'',fallback:'m03-p02.html'});state.append(componentButton('返回首页',()=>go('m03-p02.html'),{variant:'text'}));screen.replaceChildren(state);return true;}
  function read(key, fallback = null) {
    if(/^dujia-prototype-(moments|anniversaries|capsules|pet|books)$/.test(key)){const state=collectionHealth(key);if(state.issues.length)observeTime();return state.raw===null&&!state.unavailable?fallback:(key==='dujia-prototype-pet'?state.value??null:state.items);}
    if(key==='dujia-prototype-works'){const state=inspectWorks();if(state.issues.length)observeWorks();return state.raw===null&&!state.unavailable?fallback:state.items;}
    if(/^(dujia-profile|dujia-prototype-(relationship|session|invite))$/.test(key)){const state=accountInspect(key);if(state.issues.length)observeAccount();return state.raw===null&&!state.unavailable?fallback:state.value;}
    try { const value = localStorage.getItem(key); return value === null ? fallback : JSON.parse(value); }
    catch { return fallback; }
  }
  const storageGuards=new Map();
  const canWrite=(key,value)=>{
    if(timeNames[key]){if(timeRepairKey!==key&&collectionHealth(key).issues.length){observeTime();toast('请先恢复'+timeNames[key]+'，原始内容尚未改变','error');return false;}if(collectionAnalyze(key,JSON.stringify(value)).issues.length){toast('内容格式不完整，尚未保存','error');return false;}}
    if(key===WORK_KEY){if(!workRepairing&&inspectWorks().issues.length){observeWorks();toast('请先恢复作品，当前输入尚未保存','error');return false;}if(workAnalyze(JSON.stringify(value)).issues.length){toast('作品格式不完整，尚未保存','error');return false;}}
    if(key!==accountRepairKey&&!/^dujia-prototype-(record|account|work|tag|moments|anniversaries|capsules|pet|books)-recovery-/.test(key)&&accountProblem()){observeAccount();toast('请先恢复资料，当前内容尚未保存','error');return false;}
    if(accountKeys.includes(key)&&accountAnalyze(key,JSON.stringify(value)).issues.length){toast('资料格式不完整，尚未保存','error');return false;}
    return !storageGuards.has(key)||storageGuards.get(key)(value);
  };
  const protectStorage=(key,check)=>storageGuards.set(key,check);
  function write(key, value) {
    try { if(!canWrite(key,value))return false;localStorage.setItem(key, JSON.stringify(value));window.PrototypePreferences?.afterWrite(key);return true; }
    catch { toast('本地空间不足，未能保存。请整理空间后再试', 'error'); return false; }
  }
  function currentItem(key, expected) {
    const values = read(key, []);
    if (!canWrite(key, values)) return null;
    const item = Array.isArray(values) && values.find(value => value.id === expected.id);
    if (!item) throw new Error('内容已删除，当前输入仍保留；请返回列表核对');
    const fields = new Set([...Object.keys(expected), ...Object.keys(item)]);
    if ([...fields].some(field => !['comments', 'updatedAt'].includes(field) && JSON.stringify(item[field]) !== JSON.stringify(expected[field])))
      throw new Error('内容已在另一处更新，当前输入仍保留；请重新打开并核对后保存');
    return item;
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
  window.PrototypeUI = {toast, modal, sheet, busy, back, go, guard, protectSheet, read, write, currentItem, canWrite,protectStorage,failNext, fieldError, notReady,primaryNav,components:{button:componentButton,field:componentField,card:componentCard,header:componentHeader,state:componentState,loading:componentLoading,avatar:componentAvatar,tag:componentTag,divider:componentDivider}};
  window.PrototypeUI.hasAccountProblem=()=>!!accountProblem();
  window.PrototypeUI.recoverAccount=recoverAccount;
  window.PrototypeUI.workHealth=inspectWorks;
  window.PrototypeUI.recoverWorks=recoverWorks;
  window.PrototypeUI.collectionHealth=collectionHealth;
  window.PrototypeUI.recoverCollection=recoverCollection;
  function adoptCanvasFields() {
    for (const field of document.querySelectorAll('.screen input:not([type=hidden],[type=file],[type=color],[type=range],[type=checkbox],[type=radio]),.screen textarea,.screen select'))
      componentField({element: field});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', adoptCanvasFields, {once: true}); else adoptCanvasFields();
  addEventListener('resize', () => { for (const {input, error} of canvasFields) if (input.isConnected && !error.hidden) positionFieldError(input, error); });
  window.PrototypeUI.collectionState=collectionState;
  window.PrototypeUI.collectionGuard=collectionGuard;
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',observeTime,{once:true});else queueMicrotask(observeTime);
  addEventListener('storage',event=>{if(Object.hasOwn(timeNames,event.key)||event.key===null)observeTime();});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',observeWorks,{once:true});else queueMicrotask(observeWorks);
  addEventListener('storage',event=>{if(event.key===WORK_KEY||event.key===null)observeWorks();});
  queueMicrotask(observeAccount);
})();
