/* Single local relationship and invite fixture, consumed across all nine state pages. */
(() => {
  const UI = window.PrototypeUI, id = location.pathname.split('/').pop().slice(0, 7);
  const PAIR = 'dujia-prototype-relationship', INVITE = 'dujia-prototype-invite';
  const code = 'XH7K9M2Q', display = value => value.slice(0, 4) + '-' + value.slice(4);
  const home = () => UI.read('dujia-prototype-records', []).length ? 'm03-p02.html' : 'm03-p01.html';
  function invitation() {
    let value = UI.read(INVITE);
    if (!value?.code || value.expiresAt <= Date.now() || value.status === 'accepted') {
      value = {code, expiresAt: Date.now() + 86400000, status: 'pending', partner: '阿舟'};
      if (!UI.write(INVITE, value)) return null;
    }
    return value;
  }
  async function copy(value) {
    try {
      if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(value);
      else {
        const field = document.createElement('textarea'); field.value = value; field.style.cssText = 'position:fixed;opacity:0'; document.body.append(field); field.select();
        const copied = document.execCommand('copy'); field.remove(); if (!copied) throw new Error('copy unavailable');
      }
      UI.toast('已复制', 'success'); return true;
    } catch { await UI.modal({title: '可以手动复制', message: value + '\n复制后发送给 TA，或者重新允许剪贴板访问。'}); return false; }
  }
  function saveCard(invite) {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="860" height="540"><rect width="100%" height="100%" rx="42" fill="#fff7ef"/><rect x="25" y="25" width="810" height="490" rx="30" fill="none" stroke="#dc9e9c" stroke-width="4"/><text x="430" y="150" text-anchor="middle" font-size="48" fill="#754832">独家童话邀请函</text><text x="430" y="330" text-anchor="middle" font-size="90" fill="#a4454b" font-family="Georgia">${display(invite.code)}</text><text x="430" y="440" text-anchor="middle" font-size="30" fill="#946f5b">邀请 TA 一起收藏每一段日常</text></svg>`;
    const url = URL.createObjectURL(new Blob([svg], {type: 'image/svg+xml'})); const link = document.createElement('a'); link.href = url; link.download = '独家童话邀请卡.svg'; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    UI.toast('邀请卡已准备下载');
  }
  async function bind(inviteCode = code) {
    if (UI.read(PAIR)?.bound) { await UI.go('m02-p09.html', {force: true}); return false; }
    if (UI.failNext('bind')) throw new Error('关联没有完成，请重试');
    const pair = {id: 'pair-' + crypto.randomUUID(), bound: true, partner: '阿舟', acceptedAt: Date.now(), usedInvitation: inviteCode, profile: UI.read(PAIR)?.profile || {}};
    if (!UI.write(PAIR, pair)) return false;
    const invite = UI.read(INVITE); if (invite?.code === inviteCode) UI.write(INVITE, {...invite, status: 'accepted'});
    UI.toast('故事有了我们', 'success'); return UI.go('m02-p05.html', {force: true});
  }
  if (id === 'm02-p01') {
    document.querySelectorAll('.choice').forEach(button => button.addEventListener('click', () => UI.go(UI.read(PAIR)?.bound ? 'm02-p09.html' : button.classList.contains('invite') ? 'm02-p02.html' : 'm02-p03.html')));
  }
  if (id === 'm02-p02') {
    const invite = invitation();
    if (invite) document.querySelector('#code').textContent = display(invite.code);
    document.querySelector('#copy').addEventListener('click', () => invite && copy(display(invite.code)));
    document.querySelector('#save').addEventListener('click', () => invite && saveCard(invite));
    document.querySelector('#share').addEventListener('click', async () => {
      if (!invite) { UI.toast('未能准备邀请码，请返回重试', 'error'); return; }
      const selected = await UI.sheet({title: '分享邀请', message: '复制邀请链接后，可以粘贴给 TA。', actions: [{label: '复制邀请链接', value: 'copy'}, {label: '保存邀请卡', value: 'save'}, {label: '查看邀请进度', value: 'wait'}]});
      if (selected === 'copy') await copy(new URL('m02-p03.html?code=' + invite.code, location.href).href);
      if (selected === 'save') saveCard(invite);
      if (selected === 'wait') {
        if (!UI.write(INVITE, {...invite, status: 'pending', autoAt: Date.now() + 1600})) return;
        UI.go('m02-p07.html');
      }
    });
  }
  if (id === 'm02-p03') {
    const form = document.querySelector('#invite'), fields = [...form.querySelectorAll('.code input')], error = document.querySelector('#error'); form.noValidate = true;
    const initial = (new URLSearchParams(location.search).get('code') || code).replace(/[^a-z0-9]/gi, '').toUpperCase();
    fields.forEach((field, index) => {
      field.maxLength = 2; field.value = initial.slice(index * 2, index * 2 + 2); field.setAttribute('aria-label', `第 ${index + 1} 组邀请码，两位`);
      field.style.fontSize = 'clamp(14px,4.2cqw,18px)';
      field.addEventListener('input', () => { field.value = field.value.replace(/[^a-z0-9]/gi, '').slice(0, 2).toUpperCase(); UI.fieldError(field, '', error); if (field.value.length === 2 && index < 3) fields[index + 1].focus(); });
      field.addEventListener('keydown', event => { if (event.key === 'Backspace' && !field.value && index > 0) fields[index - 1].focus(); });
      field.addEventListener('paste', event => { event.preventDefault(); const value = event.clipboardData.getData('text').replace(/[^a-z0-9]/gi, '').slice(0, 8).toUpperCase(); fields.forEach((f, i) => { f.value = value.slice(i * 2, i * 2 + 2); UI.fieldError(f, '', error); }); fields[Math.min(Math.floor(value.length / 2), 3)].focus(); });
    });
    form.querySelector('.code').setAttribute('aria-label', '八位邀请码，每组两位');
    const leave = UI.guard(form, {fallback:'m02-p01.html'});
    form.addEventListener('submit', async event => {
      event.preventDefault(); const value = fields.map(e => e.value).join('');
      if (value.length !== 8) { UI.fieldError(fields.find(e => e.value.length < 2), '请输入完整的八位邀请码', error); return; }
      await UI.busy(form.querySelector('.preview'), '查看中…', async () => {
        if (UI.failNext('invite')) throw new Error('邀请暂时打不开，请重试');
        if (UI.read(PAIR)?.bound) { leave.commit(); return UI.go('m02-p09.html', {force:true}); }
        const invite = UI.read(INVITE);
        if (invite?.code === value && (invite.expiresAt <= Date.now() || ['accepted','expired'].includes(invite.status))) { leave.commit(); return UI.go('m02-p08.html', {force:true}); }
        if (value !== (invite?.code || code)) { UI.fieldError(fields[0], '邀请码没有找到，请核对或请 TA 重新分享', error); return false; }
        sessionStorage.setItem('dujia-prototype-incoming-invite', value); leave.commit(); return UI.go('m02-p04.html', {force:true});
      });
    });
  }
  if (id === 'm02-p04') {
    document.querySelector('.confirm').addEventListener('click', () => UI.busy(document.querySelector('.confirm'), '关联中…', () => bind(sessionStorage.getItem('dujia-prototype-incoming-invite') || code)));
    document.querySelectorAll('button:not(.confirm):not(.back)').forEach(button => button.addEventListener('click', () => { sessionStorage.removeItem('dujia-prototype-incoming-invite'); UI.go('m02-p01.html'); }));
  }
  if (id === 'm02-p05') {
    const pair=UI.read(PAIR),profile=UI.read('dujia-profile',{});
    document.querySelector('.names .pink').textContent=profile.nickname||'小满';
    document.querySelector('.names .green').textContent=pair?.partner||'阿舟';
    document.querySelector('.date strong').textContent=new Date(pair?.acceptedAt||Date.now()).toLocaleDateString('zh-CN',{year:'numeric',month:'long',day:'numeric'});
    document.querySelector('.primary').addEventListener('click', () => UI.go('m03-p05.html'));
    document.querySelector('.secondary').addEventListener('click', () => UI.go('m02-p06.html'));
    const footer=document.createElement('footer');footer.className='prototype-relationship-home';
    footer.append(UI.components.button('先逛逛我们的首页',()=>UI.go(home(),{replace:true}),{variant:'text'}));
    document.body.append(footer);
  }
  if (id === 'm02-p06') {
    const form = document.querySelector('#profile'); form.noValidate = true;
    const fields = ['nickname','met','anniversary']; const profile = UI.read(PAIR)?.profile;
    fields.forEach(name => { const saved = profile?.[name] || localStorage.getItem('dujia-profile-' + name); if (saved) form.elements[name].value = saved; });
    form.elements.nickname.maxLength = 20;
    const leave = UI.guard(form, {fallback: 'm02-p05.html'});
    function dateValue(text) { const m = text.match(/(\d{4})\D+(\d{1,2})\D+(\d{1,2})/); return m ? `${m[1]}-${m[2].padStart(2,'0')}-${m[3].padStart(2,'0')}` : ''; }
    function dateValid(text) { const value = dateValue(text); if (!value) return false; const [y,m,d] = value.split('-').map(Number); const date = new Date(y,m-1,d); return date.getFullYear() === y && date.getMonth() === m-1 && date.getDate() === d && date <= new Date(); }
    form.elements.met.readOnly = true;
    form.elements.met.addEventListener('click', async () => {
      const label = document.createElement('label'); label.textContent = '相遇日期'; const input = document.createElement('input'); input.type = 'date'; input.setAttribute('aria-label', '选择相遇日期'); input.value = dateValue(form.elements.met.value); label.append(input);
      const selected = await UI.sheet({title: '选择相遇日期', content: label, actions: [{label: '使用这个日期', value: 'apply'}]});
      if (selected === 'apply') {
        if (!dateValid(input.value)) { UI.fieldError(form.elements.met, '请选择有效的过去日期'); return; }
        const [y,m,d] = input.value.split('-'); form.elements.met.value = `${y}年${Number(m)}月${Number(d)}日`; form.elements.met.dispatchEvent(new Event('input', {bubbles:true}));
      }
    });
    form.elements.anniversary.readOnly = true;
    form.elements.anniversary.addEventListener('click', async () => {
      const content = document.createElement('div'), repeat = document.createElement('select'), date = document.createElement('input');
      repeat.setAttribute('aria-label', '纪念日重复周期');
      for (const [value,name] of [['monthly','每月'],['yearly','每年']]) { const option = document.createElement('option'); option.value = value; option.textContent = name; repeat.append(option); }
      date.type = 'date'; date.setAttribute('aria-label', '纪念日期'); date.value = dateValue(form.elements.met.value); content.append(repeat,date);
      const selected = await UI.sheet({title: '选择共同纪念日', content, actions: [{label: '使用这个纪念日', value:'apply'}]});
      if (selected === 'apply' && date.value) { const [,m,d] = date.value.split('-'); form.elements.anniversary.value = repeat.value === 'monthly' ? `每月 ${Number(d)} 日` : `每年 ${Number(m)} 月 ${Number(d)} 日`; }
    });
    form.addEventListener('submit', async event => {
      event.preventDefault(); const data = Object.fromEntries(fields.map(name => [name, form.elements[name].value.trim()]));
      if (!data.nickname || !dateValid(data.met) || !data.anniversary) { UI.fieldError(form.elements[!data.nickname ? 'nickname' : !dateValid(data.met) ? 'met' : 'anniversary'], '请填写昵称和有效的纪念日期'); return; }
      await UI.busy(document.querySelector('.save'), '保存中…', async () => {
        if (UI.failNext('profile')) throw new Error('资料没有保存成功，请重试');
        const pair = UI.read(PAIR, {bound:false}); if (!UI.write(PAIR, {...pair, profile:data})) return false;
        fields.forEach(name => { try { localStorage.setItem('dujia-profile-' + name, data[name]); } catch {} });
        UI.toast('小资料已保存', 'success'); leave.commit(); return UI.go(pair.bound ? 'm02-p05.html' : 'm02-p01.html', {force:true});
      });
    });
  }
  if (id === 'm02-p07') {
    let invite = UI.read(INVITE) || invitation();
    let processing = false, paused = false;
    document.querySelector('#remind').addEventListener('click', () => UI.busy(document.querySelector('#remind'), paused ? '重新查看中…' : '提醒中…', () => {
      if (UI.failNext('remind')) throw new Error('提醒没有完成，请重试');
      if (invite) { invite = {...invite, autoAt:Date.now()+1600}; if (!UI.write(INVITE, invite)) return false; }
      paused = false; UI.toast('已提醒 TA 查看邀请'); return true;
    }));
    document.querySelector('#copy').addEventListener('click', () => invite && copy(new URL('m02-p03.html?code='+invite.code, location.href).href));
    const timer = setInterval(async () => {
      const response = sessionStorage.getItem('dujia-prototype-peer-response') || 'accept';
      if (!invite?.autoAt || paused || processing || response === 'manual' || Date.now() < invite.autoAt) return;
      processing = true;
      if (response === 'expired' || invite.expiresAt <= Date.now()) {
        if (!UI.write(INVITE, {...invite, status:'expired', expiresAt:Math.min(invite.expiresAt,Date.now())})) { paused=true; processing=false; return; }
        clearInterval(timer); UI.go('m02-p08.html'); return;
      }
      try { const saved = await bind(invite.code); if (saved || UI.read(PAIR)?.bound) clearInterval(timer); else paused = true; }
      catch (error) { UI.toast(error.message, 'error'); paused = true; document.querySelector('#remind').textContent = '重试等待确认'; }
      finally { processing = false; }
    }, 250);
    addEventListener('pagehide', () => clearInterval(timer), {once:true});
  }
  if (id === 'm02-p08') {
    document.querySelector('.again').addEventListener('click', () => { localStorage.removeItem(INVITE); UI.go('m02-p01.html'); });
    document.querySelector('.reenter').addEventListener('click', () => UI.go('m02-p03.html'));
  }
  if (id === 'm02-p09') document.querySelector('.primary').addEventListener('click', () => UI.go(home()));
  document.querySelectorAll('form').forEach(form => { form.dataset.prototypeReady = 'true'; });
})();
