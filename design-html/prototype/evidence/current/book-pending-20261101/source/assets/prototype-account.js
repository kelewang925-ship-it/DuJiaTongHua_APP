/* First account-flow batch. Additional account and relationship states are audited separately. */
(() => {
  const UI = window.PrototypeUI;
  const form = document.querySelector('#form');
  if (!form) return;
  const password = document.querySelector('#password');
  const phone = form.elements.phone;
  const submit = document.querySelector('button[form="form"]');
  phone.required = true; password.required = true;
  phone.setAttribute('aria-label', '手机号'); password.setAttribute('aria-label', '密码');
  const errors = new Map();
  for (const field of [phone, password]) {
    const error = document.createElement('p');
    error.className = 'prototype-field-error'; error.id = 'prototype-error-' + field.name; error.setAttribute('role', 'alert');
    const group = field.closest('.group'); group.classList.add('prototype-input-group'); group.append(error);
    errors.set(field, error);
  }
  function validate(field) {
    let message = '';
    if (field === phone && !/^1\d{10}$/.test(phone.value.replace(/\s/g, ''))) message = '请输入有效的 11 位手机号';
    if (field === password && password.value.length < 8) message = '密码至少需要 8 位';
    const error = errors.get(field);
    field.setAttribute('aria-invalid', String(!!message));
    if (message) {
      field.setAttribute('aria-describedby', error.id);
      error.textContent = message;
    } else {
      field.removeAttribute('aria-describedby');
      error.textContent = '';
    }
    return !message;
  }
  for (const field of [phone, password]) {
    field.addEventListener('blur', () => validate(field));
    field.addEventListener('input', () => { if (field.getAttribute('aria-invalid') === 'true') validate(field); });
  }
  document.querySelector('#eye').addEventListener('click', event => {
    password.type = password.type === 'password' ? 'text' : 'password';
    event.currentTarget.setAttribute('aria-label', password.type === 'password' ? '显示密码' : '隐藏密码');
  });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const valid = [phone, password].map(validate);
    if (valid.some(value => !value)) { [phone, password][valid.indexOf(false)].focus(); return; }
    await UI.busy(submit, '登录中…', async () => {
      if (UI.failNext('credentials')) {
        sessionStorage.setItem('dujia-prototype-login-phone', phone.value.replace(/\s/g, ''));
        sessionStorage.setItem('dujia-prototype-login-attempts', '4');
        return UI.go('m01-p06.html', {force: true});
      }
      if (sessionStorage.getItem('dujia-prototype-fail-next') === 'login') {
        sessionStorage.removeItem('dujia-prototype-fail-next');
        throw new Error('登录没有完成，请检查网络后重试');
      }
      if (!await window.PrototypePreferences.login(phone.value.replace(/\s/g, ''))) return false;
      UI.toast('已进入你的故事', 'success');
      const relationship = UI.read('dujia-prototype-relationship');
      location.href = relationship?.bound ? 'm03-p01.html' : 'm02-p01.html';
      return true;
    });
  });
  document.querySelector('.forgot').addEventListener('click', () => { location.href = 'm01-p04.html'; });
  document.querySelector('.register button').addEventListener('click', () => { location.href = 'm01-p03.html'; });
  document.querySelectorAll('.terms a').forEach(link => link.addEventListener('click', event => {
    event.preventDefault();
    UI.modal({title: link.textContent, message: '这是本地交互原型，账号、验证码与操作结果均为模拟。\n填写的演示资料仅保存在当前浏览器；此页用于确认阅读与返回交互。\n正式使用前需提供经审核的完整协议与隐私政策。'});
  }));
  form.dataset.prototypeReady = 'true';
})();
