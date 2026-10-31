/* Account verification states. Codes and identities are local prototype fixtures. */
(() => {
  const UI = window.PrototypeUI;
  const id = location.pathname.split('/').pop().slice(0, 7);
  const KEY = 'dujia-prototype-challenge';
  const DEMO_CODE = '284631';
  const countdowns = new WeakMap();
  const phoneValue = field => field.value.replace(/\s/g, '');
  const phoneValid = field => UI.fieldError(field, /^1\d{10}$/.test(phoneValue(field)) ? '' : '请输入有效的 11 位手机号');
  const passwordValid = field => UI.fieldError(field, /^(?=.*[A-Za-z])(?=.*\d).{8,20}$/.test(field.value) ? '' : '密码需为 8–20 位，包含字母和数字');
  let challengeInvalid=false;
  const readChallenge = () => {
    challengeInvalid=false;
    try {
      const raw=sessionStorage.getItem(KEY);if(raw===null)return null;
      const value=JSON.parse(raw);
      if(!value||typeof value!=='object'||Array.isArray(value)||!['register','recovery'].includes(value.purpose)||typeof value.phone!=='string'||!/^1\d{10}$/.test(value.phone)||typeof value.code!=='string'||!/^\d{6}$/.test(value.code)||!Number.isFinite(value.expiresAt)||['resendAt'].some(k=>Object.hasOwn(value,k)&&!Number.isFinite(value[k]))||['verified','completeRegistration'].some(k=>Object.hasOwn(value,k)&&typeof value[k]!=='boolean')||(Object.hasOwn(value,'nickname')&&typeof value.nickname!=='string')){challengeInvalid=true;return null;}
      return value;
    } catch {challengeInvalid=true;return null;}
  };
  const putChallenge = value => {try{sessionStorage.setItem(KEY,JSON.stringify(value));}catch{throw new Error('验证资料未能保存，请检查浏览器存储后重试');}};
  function issue(purpose, phone, data = {}) {
    const next = {...data, purpose, phone, code: DEMO_CODE, expiresAt: Date.now() + 600000, resendAt: Date.now() + 48000, verified: false};
    putChallenge(next); return next;
  }
  function codeValid(value, challenge, purpose = null) {
    return challenge && (!purpose || challenge.purpose === purpose) && challenge.expiresAt > Date.now() && value === challenge.code;
  }
  function submissionChallenge(expected) {
    const current=readChallenge();
    if(!current||JSON.stringify(current)!==JSON.stringify(expected)||current.expiresAt<=Date.now()){UI.toast(current?.expiresAt<=Date.now()?'验证已过期，请重新获取验证码':'验证资料已变化，请确认后重新提交','error');return null;}
    return current;
  }
  function setupEyes() {
    document.querySelectorAll('.eye').forEach(button => button.addEventListener('click', () => {
      const field = button.dataset.target ? document.getElementById(button.dataset.target) : document.querySelector('#password');
      field.type = field.type === 'password' ? 'text' : 'password';
      button.setAttribute('aria-label', field.type === 'password' ? '显示密码' : '隐藏密码');
    }));
  }
  function bindCheck(field, check) {
    field.addEventListener('blur', () => check(field));
    field.addEventListener('input', () => { if (field.getAttribute('aria-invalid') === 'true') check(field); });
  }
  function protect(form) { form.noValidate = true; return UI.guard(form, {fallback: id === 'm01-p03' ? 'm01-p01.html' : id === 'm01-p04' ? 'm01-p02.html' : 'm01-p04.html'}); }
  function countdown(button) {
    clearInterval(countdowns.get(button));
    const original = button.id === 'resend' ? '重新获取验证码' : '获取验证码';
    const update = () => {
      const challenge = readChallenge();
      const seconds = Math.max(0, Math.ceil(((challenge?.resendAt || 0) - Date.now()) / 1000));
      button.disabled = seconds > 0; button.textContent = seconds ? `${seconds} 秒后重发` : original;
    };
    update(); const timer = setInterval(update, 1000); countdowns.set(button, timer); addEventListener('pagehide', () => clearInterval(timer), {once: true});
    addEventListener('pageshow', event => { if (event.persisted) countdown(button); }, {once:true});
  }
  async function finishRegistration(challenge) {
    if (UI.failNext('register')) throw new Error('创建没有完成，请重试，填写内容仍在');
    const profile = {...UI.read('dujia-profile', {}), nickname: challenge.nickname || '小满'};
    const changes=[['dujia-profile',profile],['dujia-prototype-session',{loggedIn:true,phone:challenge.phone}]];
    for(const key of ['records','moments','anniversaries','capsules','works','books']){const storageKey='dujia-prototype-'+key;if(localStorage.getItem(storageKey)===null)changes.push([storageKey,[]]);}
    if(!window.PrototypePreferences.transaction(changes))return false;
    sessionStorage.removeItem(KEY); sessionStorage.removeItem('dujia-prototype-register-draft');
    UI.toast('故事从这一页开始', 'success');
    return UI.go('m02-p01.html', {force: true});
  }
  async function send(button, purpose, field, data = {}) {
    if (!phoneValid(field)) { field.focus(); return null; }
    let next;
    const success = await UI.busy(button, '准备中…', () => {
      if (UI.failNext('send-code')) throw new Error('验证码未能准备好，请再试一次');
      next = issue(purpose, phoneValue(field), data);
      UI.toast('演示验证码：' + DEMO_CODE); return true;
    });
    if (success) countdown(button);
    return success ? next : null;
  }
  document.querySelectorAll('a[href="#"]').forEach(link => link.addEventListener('click', event => {
    event.preventDefault();
    UI.modal({title: link.textContent, message: '这是本地交互原型，填写的资料仅保存在当前浏览器。\n此处提供阅读、确认与返回的交互示例，正式协议与隐私政策由项目提供。'});
  }));
  setupEyes();
  if (id === 'm01-p03') {
    const form = document.querySelector('#register'), leave = protect(form);
    const nickname = form.elements.nickname, phone = form.elements.phone, password = form.elements.password, code = form.elements.code;
    nickname.maxLength = 20; password.maxLength = 20; code.maxLength = 6;
    let saved; try { saved = JSON.parse(sessionStorage.getItem('dujia-prototype-register-draft') || 'null'); } catch {}
    if (saved) { nickname.value = saved.nickname || ''; phone.value = saved.phone || ''; }
    const nickValid = field => UI.fieldError(field, field.value.trim() ? '' : '请给自己起个昵称');
    bindCheck(nickname, nickValid); bindCheck(phone, phoneValid); bindCheck(password, passwordValid);
    code.addEventListener('input', () => { code.value = code.value.replace(/\D/g, '').slice(0, 6); code.setAttribute('aria-invalid', 'false'); });
    document.querySelector('#send-code').addEventListener('click', () => send(document.querySelector('#send-code'), 'register', phone, {nickname: nickname.value.trim(), completeRegistration: false}));
    form.addEventListener('submit', async event => {
      event.preventDefault();
      for (const [field, check] of [[nickname, nickValid], [phone, phoneValid], [password, passwordValid]]) if (!check(field)) { field.focus(); return; }
      const agree = form.querySelector('input[type=checkbox]');
      if (!agree.checked) { UI.fieldError(agree, '请先阅读并同意协议'); agree.focus(); return; }
      sessionStorage.setItem('dujia-prototype-register-draft', JSON.stringify({nickname: nickname.value.trim(), phone: phoneValue(phone)}));
      const button = form.querySelector('.submit');
      await UI.busy(button, '创建中…', async () => {
        let challenge = readChallenge();
        if (code.value) {
          if (!challenge || challenge.phone !== phoneValue(phone) || !codeValid(code.value, challenge, 'register')) { UI.fieldError(code, '验证码不正确或已过期，请重新获取'); return false; }
          return finishRegistration({...challenge, nickname: nickname.value.trim()});
        }
        challenge = issue('register', phoneValue(phone), {nickname: nickname.value.trim(), completeRegistration: true});
        leave.commit(); return UI.go('m01-p07.html', {force: true});
      });
    });
    leave.commit();
  }
  if (id === 'm01-p04') {
    const form = document.querySelector('#recovery'), leave = protect(form), phone = form.elements.phone, code = form.elements.code;
    code.maxLength = 6; bindCheck(phone, phoneValid);
    document.querySelector('#send').addEventListener('click', () => send(document.querySelector('#send'), 'recovery', phone));
    form.addEventListener('submit', async event => {
      event.preventDefault(); if (!phoneValid(phone)) { phone.focus(); return; }
      await UI.busy(form.querySelector('.next'), '验证中…', async () => {
        if (UI.failNext('verify')) throw new Error('暂时无法验证，请重试');
        if (code.value) {
          const challenge = readChallenge();
          if (challenge?.phone !== phoneValue(phone) || !codeValid(code.value.trim(), challenge, 'recovery')) { UI.fieldError(code, '验证码不正确或已过期'); return false; }
          putChallenge({...challenge, verified: true}); leave.commit(); return UI.go('m01-p05.html', {force: true});
        }
        issue('recovery', phoneValue(phone)); leave.commit(); return UI.go('m01-p07.html', {force: true});
      });
    });
  }
  if (id === 'm01-p07') {
    const form = document.querySelector('#verify-form'); form.noValidate = true;
    const fields = [...form.querySelectorAll('.code input')], existing = readChallenge();
    if(challengeInvalid){
      const screen=document.querySelector('.screen')||document.querySelector('main');screen.classList.add('prototype-verification-error');screen.setAttribute('aria-label','手机验证资料恢复');
      screen.replaceChildren(UI.components.header({title:'手机验证',onBack:()=>UI.back('m01-p02.html')}),UI.components.state({kind:'error',title:'验证资料无法读取',message:'原始验证资料仍保留。请重新填写手机号并获取验证码。',action:'去注册',onAction:()=>UI.go('m01-p03.html')}),UI.components.button('找回密码',()=>UI.go('m01-p04.html'),{variant:'text'}));
      return;
    }
    const challenge = existing || issue('recovery', '13812345678');
    const error = document.createElement('p'); error.className = 'prototype-code-error'; form.append(error);
    document.querySelector('.subtitle').textContent = '验证码已准备好 · ' + challenge.phone.slice(0, 3) + ' **** ' + challenge.phone.slice(-4);
    if (existing) fields.forEach(e => { e.value = ''; });
    fields.forEach((field, index) => {
      field.addEventListener('input', () => { field.value = field.value.replace(/\D/g, '').slice(0, 1); if (field.value && index < 5) fields[index + 1].focus(); });
      field.addEventListener('keydown', event => { if (event.key === 'Backspace' && !field.value && index > 0) fields[index - 1].focus(); });
      field.addEventListener('paste', event => { event.preventDefault(); const value = event.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6); [...value].forEach((c, i) => { fields[i].value = c; }); fields[Math.min(value.length, 5)].focus(); });
    });
    const resend = document.querySelector('#resend'); countdown(resend);
    resend.addEventListener('click', async () => {
      const success = await UI.busy(resend, '准备中…', () => { if (UI.failNext('send-code')) throw new Error('验证码未能准备好，请重试'); const current = readChallenge(); if(!current)throw new Error('验证资料已失效，请重新填写手机号获取验证码'); issue(current.purpose, current.phone, current); UI.toast('演示验证码：' + DEMO_CODE); return true; });
      if (success) {
        fields.forEach(field => { field.value = ''; UI.fieldError(field, '', error); });
        countdown(resend); fields[0].focus();
      }
    });
    document.querySelector('#switch').addEventListener('click', async () => {
      const selected = await UI.sheet({title: '换一种验证方式', actions: [{label: '重新填写手机号', value: 'phone'}, {label: '查看演示验证码', value: 'code'}]});
      if (selected === 'phone') UI.go(challenge.purpose === 'register' ? 'm01-p03.html' : 'm01-p04.html');
      if (selected === 'code') UI.modal({title: '演示验证码', message: DEMO_CODE + '\n仅用于此交互原型，10 分钟内有效。'});
    });
    form.addEventListener('submit', async event => {
      event.preventDefault(); const value = fields.map(e => e.value).join(''), current = readChallenge();
      if (value.length !== 6 || !codeValid(value, current)) { UI.fieldError(fields.find(e => !e.value) || fields[0], current?.expiresAt <= Date.now() ? '验证码已过期，请重新获取' : '验证码不正确，请检查六位数字', error); return; }
      UI.fieldError(null, '', error);
      await UI.busy(form.querySelector('.verify'), '验证中…', async () => {
        if (UI.failNext('verify')) throw new Error('验证没有完成，请重试');
        const latest=submissionChallenge(current);if(!latest)return false;
        if(latest.purpose==='register'&&latest.completeRegistration)return finishRegistration(latest);
        putChallenge({...latest,verified:true});
        if (latest.purpose === 'register') return UI.go('m01-p03.html', {force: true});
        return UI.go('m01-p05.html', {force: true});
      });
    });
  }
  if (id === 'm01-p05') {
    const form = document.querySelector('#reset'), leave = protect(form), password = form.elements.password, confirm = form.elements.confirm;
    bindCheck(password, passwordValid);
    form.addEventListener('submit', async event => {
      event.preventDefault(); if (!passwordValid(password)) { password.focus(); return; }
      if (password.value !== confirm.value) { UI.fieldError(confirm, '两次输入的密码不一致'); return; }
      const challenge = readChallenge();
      if (!challenge?.verified || challenge.purpose !== 'recovery' || challenge.expiresAt <= Date.now()) { await UI.modal({title: '先验证你的手机号', message: '验证后才能更换故事书的钥匙。', confirm: '去验证', cancel: '继续填写'}).then(go => { if (go) UI.go('m01-p04.html'); }); return; }
      await UI.busy(form.querySelector('.submit'), '重置中…', async () => {
        if(!submissionChallenge(challenge))return false;
        if (UI.failNext('reset')) throw new Error('重置没有完成，请重试');
        sessionStorage.setItem('dujia-prototype-reset-complete', String(Date.now())); sessionStorage.removeItem(KEY);
        leave.commit(); return UI.go('m01-p08.html', {force: true});
      });
    });
  }
  if (id === 'm01-p06') {
    const form = document.querySelector('#retry-form'), password = form.querySelector('#password'), button = form.querySelector('.retry'), error = form.querySelector('#error');
    form.noValidate = true; error.setAttribute('role', 'alert');
    let left = Number(sessionStorage.getItem('dujia-prototype-login-attempts') || 4);
    function render() { button.disabled = left <= 0; error.textContent = left > 0 ? `密码错误，还可以尝试 ${left} 次` : '尝试次数已用完，请找回密码'; }
    render();
    form.addEventListener('submit', async event => {
      event.preventDefault(); if (left <= 0) return;
      if (password.value.length < 8 || UI.failNext('credentials')) { left--; sessionStorage.setItem('dujia-prototype-login-attempts', String(left)); password.value = ''; render(); return; }
      await UI.busy(button, '登录中…', async () => {
        if (UI.failNext('login')) throw new Error('暂时无法登录，请重试');
        const phone = sessionStorage.getItem('dujia-prototype-login-phone') || '13812345678';
        if (!await window.PrototypePreferences.login(phone)) return false;
        sessionStorage.removeItem('dujia-prototype-login-attempts'); return UI.go(UI.read('dujia-prototype-relationship')?.bound ? 'm03-p01.html' : 'm02-p01.html', {force: true});
      });
    });
  }
  document.querySelectorAll('form').forEach(form => { form.dataset.prototypeReady = 'true'; });
})();
