# 当前控件行为观察

> 全页观察截至 aed142d 阶段；登录/邀请恢复后的最新专项和回归见SESSION_INVITE_IMPLEMENTATION.md。本文件不代表最新源码全页终验。

运行源码指纹：`9ad1a540e95bfe58f15c28708317235dc1bec81d1fb323ddef4cd365b7fceaa0`；日期固定为2026-10-05的观察fixture，不是当前设备日期。绑定观察不等于实际执行。

以下保留实际处理代码、原生操作和literal出口，尚待逐项执行、返回与异常验证。全局委托只作为候选，不能自动判为有效。

| 请求页 | 场景 | 实际页 | 控件 | 可用 | 当前处理／出口 |
| --- | --- | --- | --- | --- | --- |
| m01-p01 | empty | m01-p01 | 登录并开始 | 可用 | PrototypeUI.go('m01-p02.html') |
| m01-p01 | empty | m01-p01 | 创建账号 | 可用 | PrototypeUI.go('m01-p03.html') |
| m01-p01 | populated | m01-p01 | 登录并开始 | 可用 | PrototypeUI.go('m01-p02.html') |
| m01-p01 | populated | m01-p01 | 创建账号 | 可用 | PrototypeUI.go('m01-p03.html') |
| m01-p02 | empty | m01-p02 | 返回 | 可用 | PrototypeUI.back('m01-p01.html') |
| m01-p02 | empty | m01-p02 | 手机号 | 可用 | 原生输入/选择器 |
| m01-p02 | empty | m01-p02 | 密码 | 可用 | 原生输入/选择器 |
| m01-p02 | empty | m01-p02 | 显示密码 | 可用 | event => {      password.type = password.type === 'password' ? 'text' : 'password';      event.currentTarget.setAttribute('aria-label', password.type === 'password' ? '显示密码' : '隐藏密码');    } |
| m01-p02 | empty | m01-p02 | 忘记密码？ | 可用 | () => { location.href = 'm01-p04.html'; } |
| m01-p02 | empty | m01-p02 | 登录并回到故事里 | 可用 | 委托候选/待复核 |
| m01-p02 | empty | m01-p02 | 创建账号 | 可用 | () => { location.href = 'm01-p03.html'; } |
| m01-p02 | empty | m01-p02 | 《用户协议》 | 可用 | # |
| m01-p02 | empty | m01-p02 | 《隐私政策》 | 可用 | # |
| m01-p02 | populated | m01-p02 | 返回 | 可用 | PrototypeUI.back('m01-p01.html') |
| m01-p02 | populated | m01-p02 | 手机号 | 可用 | 原生输入/选择器 |
| m01-p02 | populated | m01-p02 | 密码 | 可用 | 原生输入/选择器 |
| m01-p02 | populated | m01-p02 | 显示密码 | 可用 | event => {      password.type = password.type === 'password' ? 'text' : 'password';      event.currentTarget.setAttribute('aria-label', password.type === 'password' ? '显示密码' : '隐藏密码');    } |
| m01-p02 | populated | m01-p02 | 忘记密码？ | 可用 | () => { location.href = 'm01-p04.html'; } |
| m01-p02 | populated | m01-p02 | 登录并回到故事里 | 可用 | 委托候选/待复核 |
| m01-p02 | populated | m01-p02 | 创建账号 | 可用 | () => { location.href = 'm01-p03.html'; } |
| m01-p02 | populated | m01-p02 | 《用户协议》 | 可用 | # |
| m01-p02 | populated | m01-p02 | 《隐私政策》 | 可用 | # |
| m01-p03 | empty | m01-p03 | 返回欢迎页 | 可用 | PrototypeUI.back('m01-p01.html') |
| m01-p03 | empty | m01-p03 | 昵称 | 可用 | 原生输入/选择器 |
| m01-p03 | empty | m01-p03 | 手机号 | 可用 | 原生输入/选择器 |
| m01-p03 | empty | m01-p03 | 验证码 | 可用 | 原生输入/选择器 |
| m01-p03 | empty | m01-p03 | 获取验证码 | 可用 | () => send(document.querySelector('#send-code'), 'register', phone, {nickname: nickname.value.trim(), completeRegistration: false}) |
| m01-p03 | empty | m01-p03 | 登录密码 | 可用 | 原生输入/选择器 |
| m01-p03 | empty | m01-p03 | 显示密码 | 可用 | () => {        const field = button.dataset.target ? document.getElementById(button.dataset.target) : document.querySelector('#password');        field.type = field.type === 'password' ? 'text' : 'password';        button.setAttribute('aria-label', field.type === 'password' ? '显示密码' : '隐藏密码');      } |
| m01-p03 | empty | m01-p03 | INPUT | 可用 | 原生输入/选择器 |
| m01-p03 | empty | m01-p03 | 《用户协议》 | 可用 | # |
| m01-p03 | empty | m01-p03 | 《隐私政策》 | 可用 | # |
| m01-p03 | empty | m01-p03 | 创建账号 | 可用 | 委托候选/待复核 |
| m01-p03 | empty | m01-p03 | 去登录 | 可用 | m01-p02.html |
| m01-p03 | populated | m01-p03 | 返回欢迎页 | 可用 | PrototypeUI.back('m01-p01.html') |
| m01-p03 | populated | m01-p03 | 昵称 | 可用 | 原生输入/选择器 |
| m01-p03 | populated | m01-p03 | 手机号 | 可用 | 原生输入/选择器 |
| m01-p03 | populated | m01-p03 | 验证码 | 可用 | 原生输入/选择器 |
| m01-p03 | populated | m01-p03 | 获取验证码 | 可用 | () => send(document.querySelector('#send-code'), 'register', phone, {nickname: nickname.value.trim(), completeRegistration: false}) |
| m01-p03 | populated | m01-p03 | 登录密码 | 可用 | 原生输入/选择器 |
| m01-p03 | populated | m01-p03 | 显示密码 | 可用 | () => {        const field = button.dataset.target ? document.getElementById(button.dataset.target) : document.querySelector('#password');        field.type = field.type === 'password' ? 'text' : 'password';        button.setAttribute('aria-label', field.type === 'password' ? '显示密码' : '隐藏密码');      } |
| m01-p03 | populated | m01-p03 | INPUT | 可用 | 原生输入/选择器 |
| m01-p03 | populated | m01-p03 | 《用户协议》 | 可用 | # |
| m01-p03 | populated | m01-p03 | 《隐私政策》 | 可用 | # |
| m01-p03 | populated | m01-p03 | 创建账号 | 可用 | 委托候选/待复核 |
| m01-p03 | populated | m01-p03 | 去登录 | 可用 | m01-p02.html |
| m01-p04 | empty | m01-p04 | 返回 | 可用 | PrototypeUI.back('m01-p02.html') |
| m01-p04 | empty | m01-p04 | 手机号 | 可用 | 原生输入/选择器 |
| m01-p04 | empty | m01-p04 | 验证码 | 可用 | 原生输入/选择器 |
| m01-p04 | empty | m01-p04 | 获取验证码 | 可用 | () => send(document.querySelector('#send'), 'recovery', phone) |
| m01-p04 | empty | m01-p04 | 下一步 | 可用 | 委托候选/待复核 |
| m01-p04 | empty | m01-p04 | 返回登录 | 可用 | m01-p02.html |
| m01-p04 | populated | m01-p04 | 返回 | 可用 | PrototypeUI.back('m01-p02.html') |
| m01-p04 | populated | m01-p04 | 手机号 | 可用 | 原生输入/选择器 |
| m01-p04 | populated | m01-p04 | 验证码 | 可用 | 原生输入/选择器 |
| m01-p04 | populated | m01-p04 | 获取验证码 | 可用 | () => send(document.querySelector('#send'), 'recovery', phone) |
| m01-p04 | populated | m01-p04 | 下一步 | 可用 | 委托候选/待复核 |
| m01-p04 | populated | m01-p04 | 返回登录 | 可用 | m01-p02.html |
| m01-p05 | empty | m01-p05 | 返回找回密码 | 可用 | PrototypeUI.back('m01-p04.html') |
| m01-p05 | empty | m01-p05 | 输入新密码 | 可用 | 原生输入/选择器 |
| m01-p05 | empty | m01-p05 | 显示新密码 | 可用 | () => {        const field = button.dataset.target ? document.getElementById(button.dataset.target) : document.querySelector('#password');        field.type = field.type === 'password' ? 'text' : 'password';        button.setAttribute('aria-label', field.type === 'password' ? '显示密码' : '隐藏密码');      } |
| m01-p05 | empty | m01-p05 | 再次输入新密码 | 可用 | 原生输入/选择器 |
| m01-p05 | empty | m01-p05 | 显示确认密码 | 可用 | () => {        const field = button.dataset.target ? document.getElementById(button.dataset.target) : document.querySelector('#password');        field.type = field.type === 'password' ? 'text' : 'password';        button.setAttribute('aria-label', field.type === 'password' ? '显示密码' : '隐藏密码');      } |
| m01-p05 | empty | m01-p05 | 确认并重置 | 可用 | 委托候选/待复核 |
| m01-p05 | populated | m01-p05 | 返回找回密码 | 可用 | PrototypeUI.back('m01-p04.html') |
| m01-p05 | populated | m01-p05 | 输入新密码 | 可用 | 原生输入/选择器 |
| m01-p05 | populated | m01-p05 | 显示新密码 | 可用 | () => {        const field = button.dataset.target ? document.getElementById(button.dataset.target) : document.querySelector('#password');        field.type = field.type === 'password' ? 'text' : 'password';        button.setAttribute('aria-label', field.type === 'password' ? '显示密码' : '隐藏密码');      } |
| m01-p05 | populated | m01-p05 | 再次输入新密码 | 可用 | 原生输入/选择器 |
| m01-p05 | populated | m01-p05 | 显示确认密码 | 可用 | () => {        const field = button.dataset.target ? document.getElementById(button.dataset.target) : document.querySelector('#password');        field.type = field.type === 'password' ? 'text' : 'password';        button.setAttribute('aria-label', field.type === 'password' ? '显示密码' : '隐藏密码');      } |
| m01-p05 | populated | m01-p05 | 确认并重置 | 可用 | 委托候选/待复核 |
| m01-p06 | empty | m01-p06 | 返回 | 可用 | PrototypeUI.back('m01-p02.html') |
| m01-p06 | empty | m01-p06 | 密码 | 可用 | 原生输入/选择器 |
| m01-p06 | empty | m01-p06 | 显示密码 | 可用 | () => {        const field = button.dataset.target ? document.getElementById(button.dataset.target) : document.querySelector('#password');        field.type = field.type === 'password' ? 'text' : 'password';        button.setAttribute('aria-label', field.type === 'password' ? '显示密码' : '隐藏密码');      } |
| m01-p06 | empty | m01-p06 | 再试一次 | 可用 | 委托候选/待复核 |
| m01-p06 | empty | m01-p06 | 找回密码 | 可用 | m01-p04.html |
| m01-p06 | populated | m01-p06 | 返回 | 可用 | PrototypeUI.back('m01-p02.html') |
| m01-p06 | populated | m01-p06 | 密码 | 可用 | 原生输入/选择器 |
| m01-p06 | populated | m01-p06 | 显示密码 | 可用 | () => {        const field = button.dataset.target ? document.getElementById(button.dataset.target) : document.querySelector('#password');        field.type = field.type === 'password' ? 'text' : 'password';        button.setAttribute('aria-label', field.type === 'password' ? '显示密码' : '隐藏密码');      } |
| m01-p06 | populated | m01-p06 | 再试一次 | 可用 | 委托候选/待复核 |
| m01-p06 | populated | m01-p06 | 找回密码 | 可用 | m01-p04.html |
| m01-p07 | empty | m01-p07 | 返回 | 可用 | PrototypeUI.back('m01-p04.html') |
| m01-p07 | empty | m01-p07 | 第 1 位验证码 | 可用 | 原生输入/选择器 |
| m01-p07 | empty | m01-p07 | 第 2 位验证码 | 可用 | 原生输入/选择器 |
| m01-p07 | empty | m01-p07 | 第 3 位验证码 | 可用 | 原生输入/选择器 |
| m01-p07 | empty | m01-p07 | 第 4 位验证码 | 可用 | 原生输入/选择器 |
| m01-p07 | empty | m01-p07 | 第 5 位验证码 | 可用 | 原生输入/选择器 |
| m01-p07 | empty | m01-p07 | 第 6 位验证码 | 可用 | 原生输入/选择器 |
| m01-p07 | empty | m01-p07 | 验证并继续 | 可用 | 委托候选/待复核 |
| m01-p07 | empty | m01-p07 | 48 秒后重发 | 隐藏/禁用 | async () => {        const success = await UI.busy(resend, '准备中…', () => { if (UI.failNext('send-code')) throw new Error('验证码未能准备好，请重试'); const current = readChallenge(); issue(current.purpose, current.phone, current); UI.toast('演示验证码：' + DEMO_CODE); return true; });        if (success) {          fields.forEach(field => { field.value = ''; UI.fieldError(field, '', error); });          countdown(resend); fields[0].focus();        }      } |
| m01-p07 | empty | m01-p07 | 没收到验证码？换个方式 | 可用 | async () => {        const selected = await UI.sheet({title: '换一种验证方式', actions: [{label: '重新填写手机号', value: 'phone'}, {label: '查看演示验证码', value: 'code'}]});        if (selected === 'phone') UI.go(challenge.purpose === 'register' ? 'm01-p03.html' : 'm01-p04.html');        if (selected === 'code') UI.modal({title: '演示验证码', message: DEMO_CODE + '\n仅用于此交互原型，10 分钟内有效。'});      } |
| m01-p07 | populated | m01-p07 | 返回 | 可用 | PrototypeUI.back('m01-p04.html') |
| m01-p07 | populated | m01-p07 | 第 1 位验证码 | 可用 | 原生输入/选择器 |
| m01-p07 | populated | m01-p07 | 第 2 位验证码 | 可用 | 原生输入/选择器 |
| m01-p07 | populated | m01-p07 | 第 3 位验证码 | 可用 | 原生输入/选择器 |
| m01-p07 | populated | m01-p07 | 第 4 位验证码 | 可用 | 原生输入/选择器 |
| m01-p07 | populated | m01-p07 | 第 5 位验证码 | 可用 | 原生输入/选择器 |
| m01-p07 | populated | m01-p07 | 第 6 位验证码 | 可用 | 原生输入/选择器 |
| m01-p07 | populated | m01-p07 | 验证并继续 | 可用 | 委托候选/待复核 |
| m01-p07 | populated | m01-p07 | 47 秒后重发 | 隐藏/禁用 | async () => {        const success = await UI.busy(resend, '准备中…', () => { if (UI.failNext('send-code')) throw new Error('验证码未能准备好，请重试'); const current = readChallenge(); issue(current.purpose, current.phone, current); UI.toast('演示验证码：' + DEMO_CODE); return true; });        if (success) {          fields.forEach(field => { field.value = ''; UI.fieldError(field, '', error); });          countdown(resend); fields[0].focus();        }      } |
| m01-p07 | populated | m01-p07 | 没收到验证码？换个方式 | 可用 | async () => {        const selected = await UI.sheet({title: '换一种验证方式', actions: [{label: '重新填写手机号', value: 'phone'}, {label: '查看演示验证码', value: 'code'}]});        if (selected === 'phone') UI.go(challenge.purpose === 'register' ? 'm01-p03.html' : 'm01-p04.html');        if (selected === 'code') UI.modal({title: '演示验证码', message: DEMO_CODE + '\n仅用于此交互原型，10 分钟内有效。'});      } |
| m01-p08 | empty | m01-p08 | 返回登录 | 可用 | PrototypeUI.go('m01-p02.html') |
| m01-p08 | populated | m01-p08 | 返回登录 | 可用 | PrototypeUI.go('m01-p02.html') |
| m02-p01 | empty | m02-p01 | 返回登录 | 可用 | PrototypeUI.back('m01-p02.html') |
| m02-p01 | empty | m02-p01 | 邀请 TA 加入 生成专属邀请码 | 可用 | () => UI.go(UI.read(PAIR)?.bound ? 'm02-p09.html' : button.classList.contains('invite') ? 'm02-p02.html' : 'm02-p03.html') |
| m02-p01 | empty | m02-p01 | 输入 TA 的邀请码 接受一份特别邀请 | 可用 | () => UI.go(UI.read(PAIR)?.bound ? 'm02-p09.html' : button.classList.contains('invite') ? 'm02-p02.html' : 'm02-p03.html') |
| m02-p01 | populated | m02-p01 | 返回登录 | 可用 | PrototypeUI.back('m01-p02.html') |
| m02-p01 | populated | m02-p01 | 邀请 TA 加入 生成专属邀请码 | 可用 | () => UI.go(UI.read(PAIR)?.bound ? 'm02-p09.html' : button.classList.contains('invite') ? 'm02-p02.html' : 'm02-p03.html') |
| m02-p01 | populated | m02-p01 | 输入 TA 的邀请码 接受一份特别邀请 | 可用 | () => UI.go(UI.read(PAIR)?.bound ? 'm02-p09.html' : button.classList.contains('invite') ? 'm02-p02.html' : 'm02-p03.html') |
| m02-p02 | empty | m02-p02 | 返回建立关系 | 可用 | PrototypeUI.back('m02-p01.html') |
| m02-p02 | empty | m02-p02 | ✦ 复制邀请码 ✦ | 可用 | () => invite && copy(display(invite.code)) |
| m02-p02 | empty | m02-p02 | 发送给微信好友 | 可用 | async () => {       if (!invite) { UI.toast('未能准备邀请码，请返回重试', 'error'); return; }       const selected = await UI.sheet({title: '分享邀请', message: '复制邀请链接后，可以粘贴给 TA。', actions: [{label: '复制邀请链接', value: 'copy'}, {label: '保存邀请卡', value: 'save'}, {label: '查看邀请进度', value: 'wait'}]});       if (selected === 'copy') await copy(new URL('m02-p03.html?code=' + invite.code, location.href).href);       if (selected === 'save') saveCard(invite);       if (selected === 'wait') {         if (!UI.write(INVITE, {...invite, status: 'pending', autoAt: Date.now() + 1600})) return;         UI.go('m02-p07.html'); |
| m02-p02 | empty | m02-p02 | 保存邀请卡 | 可用 | () => invite && saveCard(invite) |
| m02-p02 | populated | m02-p02 | 返回建立关系 | 可用 | PrototypeUI.back('m02-p01.html') |
| m02-p02 | populated | m02-p02 | ✦ 复制邀请码 ✦ | 可用 | () => invite && copy(display(invite.code)) |
| m02-p02 | populated | m02-p02 | 发送给微信好友 | 可用 | async () => {       if (!invite) { UI.toast('未能准备邀请码，请返回重试', 'error'); return; }       const selected = await UI.sheet({title: '分享邀请', message: '复制邀请链接后，可以粘贴给 TA。', actions: [{label: '复制邀请链接', value: 'copy'}, {label: '保存邀请卡', value: 'save'}, {label: '查看邀请进度', value: 'wait'}]});       if (selected === 'copy') await copy(new URL('m02-p03.html?code=' + invite.code, location.href).href);       if (selected === 'save') saveCard(invite);       if (selected === 'wait') {         if (!UI.write(INVITE, {...invite, status: 'pending', autoAt: Date.now() + 1600})) return;         UI.go('m02-p07.html'); |
| m02-p02 | populated | m02-p02 | 保存邀请卡 | 可用 | () => invite && saveCard(invite) |
| m02-p03 | empty | m02-p03 | 返回 | 可用 | PrototypeUI.back('m02-p01.html') |
| m02-p03 | empty | m02-p03 | 第 1 组邀请码，两位 | 可用 | 原生输入/选择器 |
| m02-p03 | empty | m02-p03 | 第 2 组邀请码，两位 | 可用 | 原生输入/选择器 |
| m02-p03 | empty | m02-p03 | 第 3 组邀请码，两位 | 可用 | 原生输入/选择器 |
| m02-p03 | empty | m02-p03 | 第 4 组邀请码，两位 | 可用 | 原生输入/选择器 |
| m02-p03 | empty | m02-p03 | 查看邀请内容 | 可用 | 委托候选/待复核 |
| m02-p03 | empty | m02-p03 | 请让 TA 分享给你 | 可用 | m02-p01.html |
| m02-p03 | populated | m02-p03 | 返回 | 可用 | PrototypeUI.back('m02-p01.html') |
| m02-p03 | populated | m02-p03 | 第 1 组邀请码，两位 | 可用 | 原生输入/选择器 |
| m02-p03 | populated | m02-p03 | 第 2 组邀请码，两位 | 可用 | 原生输入/选择器 |
| m02-p03 | populated | m02-p03 | 第 3 组邀请码，两位 | 可用 | 原生输入/选择器 |
| m02-p03 | populated | m02-p03 | 第 4 组邀请码，两位 | 可用 | 原生输入/选择器 |
| m02-p03 | populated | m02-p03 | 查看邀请内容 | 可用 | 委托候选/待复核 |
| m02-p03 | populated | m02-p03 | 请让 TA 分享给你 | 可用 | m02-p01.html |
| m02-p04 | empty | m02-p04 | 返回 | 可用 | PrototypeUI.back('m02-p03.html') |
| m02-p04 | empty | m02-p04 | 确认建立关系 | 可用 | () => UI.busy(document.querySelector('.confirm'), '关联中…', () => bind(sessionStorage.getItem('dujia-prototype-incoming-invite') ／／ code)) |
| m02-p04 | empty | m02-p04 | 暂不接受 | 可用 | () => { sessionStorage.removeItem('dujia-prototype-incoming-invite'); UI.go('m02-p01.html'); } |
| m02-p04 | populated | m02-p04 | 返回 | 可用 | PrototypeUI.back('m02-p03.html') |
| m02-p04 | populated | m02-p04 | 确认建立关系 | 可用 | () => UI.busy(document.querySelector('.confirm'), '关联中…', () => bind(sessionStorage.getItem('dujia-prototype-incoming-invite') ／／ code)) |
| m02-p04 | populated | m02-p04 | 暂不接受 | 可用 | () => { sessionStorage.removeItem('dujia-prototype-incoming-invite'); UI.go('m02-p01.html'); } |
| m02-p05 | empty | m02-p05 | 去写第一篇共同日记 ♡ | 可用 | () => UI.go('m03-p05.html') |
| m02-p05 | empty | m02-p05 | 完善情侣资料 | 可用 | () => UI.go('m02-p06.html') |
| m02-p05 | empty | m02-p05 | 先逛逛我们的首页 | 可用 | ()=>UI.go(home(),{replace:true}) |
| m02-p05 | populated | m02-p05 | 去写第一篇共同日记 ♡ | 可用 | () => UI.go('m03-p05.html') |
| m02-p05 | populated | m02-p05 | 完善情侣资料 | 可用 | () => UI.go('m02-p06.html') |
| m02-p05 | populated | m02-p05 | 先逛逛我们的首页 | 可用 | ()=>UI.go(home(),{replace:true}) |
| m02-p06 | empty | m02-p06 | 返回 | 可用 | PrototypeUI.back('m02-p05.html') |
| m02-p06 | empty | m02-p06 | 情侣昵称 | 可用 | 原生输入/选择器 |
| m02-p06 | empty | m02-p06 | 相遇日期 | 可用 | 原生输入/选择器 |
| m02-p06 | empty | m02-p06 | 共同纪念日 | 可用 | 原生输入/选择器 |
| m02-p06 | empty | m02-p06 | 保存小资料 | 可用 | 委托候选/待复核 |
| m02-p06 | populated | m02-p06 | 返回 | 可用 | PrototypeUI.back('m02-p05.html') |
| m02-p06 | populated | m02-p06 | 情侣昵称 | 可用 | 原生输入/选择器 |
| m02-p06 | populated | m02-p06 | 相遇日期 | 可用 | 原生输入/选择器 |
| m02-p06 | populated | m02-p06 | 共同纪念日 | 可用 | 原生输入/选择器 |
| m02-p06 | populated | m02-p06 | 保存小资料 | 可用 | 委托候选/待复核 |
| m02-p07 | empty | m02-p07 | 返回邀请卡 | 可用 | PrototypeUI.back('m02-p02.html') |
| m02-p07 | empty | m02-p07 | 提醒 TA 看看 | 可用 | () => UI.busy(document.querySelector('#remind'), paused ? '重新查看中…' : '提醒中…', () => {       if (UI.failNext('remind')) throw new Error('提醒没有完成，请重试');       if (invite) { invite = {...invite, autoAt:Date.now()+1600}; if (!UI.write(INVITE, invite)) return false; }       paused = false; UI.toast('已提醒 TA 查看邀请'); return true;     }) |
| m02-p07 | empty | m02-p07 | 复制邀请链接 | 可用 | () => invite && copy(new URL('m02-p03.html?code='+invite.code, location.href).href) |
| m02-p07 | populated | m02-p07 | 返回邀请卡 | 可用 | PrototypeUI.back('m02-p02.html') |
| m02-p07 | populated | m02-p07 | 提醒 TA 看看 | 可用 | () => UI.busy(document.querySelector('#remind'), paused ? '重新查看中…' : '提醒中…', () => {       if (UI.failNext('remind')) throw new Error('提醒没有完成，请重试');       if (invite) { invite = {...invite, autoAt:Date.now()+1600}; if (!UI.write(INVITE, invite)) return false; }       paused = false; UI.toast('已提醒 TA 查看邀请'); return true;     }) |
| m02-p07 | populated | m02-p07 | 复制邀请链接 | 可用 | () => invite && copy(new URL('m02-p03.html?code='+invite.code, location.href).href) |
| m02-p08 | empty | m02-p08 | 请 TA 重新邀请 | 可用 | () => { localStorage.removeItem(INVITE); UI.go('m02-p01.html'); } |
| m02-p08 | empty | m02-p08 | 重新输入邀请码 | 可用 | () => UI.go('m02-p03.html') |
| m02-p08 | populated | m02-p08 | 请 TA 重新邀请 | 可用 | () => { localStorage.removeItem(INVITE); UI.go('m02-p01.html'); } |
| m02-p08 | populated | m02-p08 | 重新输入邀请码 | 可用 | () => UI.go('m02-p03.html') |
| m02-p09 | empty | m02-p09 | 回到我们的首页 | 可用 | () => UI.go(home()) |
| m02-p09 | empty | m02-p09 | 查看关系设置 | 可用 | m02-p06.html |
| m02-p09 | populated | m02-p09 | 回到我们的首页 | 可用 | () => UI.go(home()) |
| m02-p09 | populated | m02-p09 | 查看关系设置 | 可用 | m02-p06.html |
| m03-p01 | empty | m03-p01 | 搜索共同记录 | 可用 | PrototypeUI.go('m03-p03.html') |
| m03-p01 | empty | m03-p01 | 写日记 | 可用 | PrototypeUI.go('m03-p05.html') |
| m03-p01 | empty | m03-p01 | 添加照片 | 可用 | PrototypeUI.go('m03-p11.html') |
| m03-p01 | empty | m03-p01 | 去童话工坊，把回忆变成故事 › | 可用 | m05-p01.html |
| m03-p01 | empty | m03-p01 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p01 | empty | m03-p01 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p01 | empty | m03-p01 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p01 | empty | m03-p01 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p01 | empty | m03-p01 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p01 | populated | m03-p02 | 搜索共同记录 | 可用 | PrototypeUI.go('m03-p03.html') |
| m03-p01 | populated | m03-p02 | 写日记 记录心情 | 可用 | PrototypeUI.go('m03-p05.html') |
| m03-p01 | populated | m03-p02 | 添加照片 珍藏瞬间 | 可用 | PrototypeUI.go('m03-p11.html') |
| m03-p01 | populated | m03-p02 | 去童话工坊，把回忆变成故事 › | 可用 | m05-p01.html |
| m03-p01 | populated | m03-p02 | 查看全部 › | 可用 | m03-p06.html |
| m03-p01 | populated | m03-p02 | 共同日记 小满 · 共同可见 | 可用 | ()=>UI.go(R.route(item)) |
| m03-p01 | populated | m03-p02 | 自己的日记 小满 · 仅自己可见 | 可用 | ()=>UI.go(R.route(item)) |
| m03-p01 | populated | m03-p02 | 共同照片 小满 · 共同可见 | 可用 | ()=>UI.go(R.route(item)) |
| m03-p01 | populated | m03-p02 | 共同测试册 从目录开始阅读 继续阅读 › | 可用 | PrototypeUI.go('m08-p01.html') |
| m03-p01 | populated | m03-p02 | 下一件重要时刻 今天的纪念日 · 今天 查看纪念日 › | 可用 | PrototypeUI.go('m04-p01.html') |
| m03-p01 | populated | m03-p02 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p01 | populated | m03-p02 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p01 | populated | m03-p02 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p01 | populated | m03-p02 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p01 | populated | m03-p02 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p02 | empty | m03-p01 | 搜索共同记录 | 可用 | PrototypeUI.go('m03-p03.html') |
| m03-p02 | empty | m03-p01 | 写日记 | 可用 | PrototypeUI.go('m03-p05.html') |
| m03-p02 | empty | m03-p01 | 添加照片 | 可用 | PrototypeUI.go('m03-p11.html') |
| m03-p02 | empty | m03-p01 | 去童话工坊，把回忆变成故事 › | 可用 | m05-p01.html |
| m03-p02 | empty | m03-p01 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p02 | empty | m03-p01 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p02 | empty | m03-p01 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p02 | empty | m03-p01 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p02 | empty | m03-p01 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p02 | populated | m03-p02 | 搜索共同记录 | 可用 | PrototypeUI.go('m03-p03.html') |
| m03-p02 | populated | m03-p02 | 写日记 记录心情 | 可用 | PrototypeUI.go('m03-p05.html') |
| m03-p02 | populated | m03-p02 | 添加照片 珍藏瞬间 | 可用 | PrototypeUI.go('m03-p11.html') |
| m03-p02 | populated | m03-p02 | 去童话工坊，把回忆变成故事 › | 可用 | m05-p01.html |
| m03-p02 | populated | m03-p02 | 查看全部 › | 可用 | m03-p06.html |
| m03-p02 | populated | m03-p02 | 共同日记 小满 · 共同可见 | 可用 | ()=>UI.go(R.route(item)) |
| m03-p02 | populated | m03-p02 | 自己的日记 小满 · 仅自己可见 | 可用 | ()=>UI.go(R.route(item)) |
| m03-p02 | populated | m03-p02 | 共同照片 小满 · 共同可见 | 可用 | ()=>UI.go(R.route(item)) |
| m03-p02 | populated | m03-p02 | 共同测试册 从目录开始阅读 继续阅读 › | 可用 | PrototypeUI.go('m08-p01.html') |
| m03-p02 | populated | m03-p02 | 下一件重要时刻 今天的纪念日 · 今天 查看纪念日 › | 可用 | PrototypeUI.go('m04-p01.html') |
| m03-p02 | populated | m03-p02 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p02 | populated | m03-p02 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p02 | populated | m03-p02 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p02 | populated | m03-p02 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p02 | populated | m03-p02 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m03-p03 | empty | m03-p03 | 返回首页 | 可用 | PrototypeUI.back('m03-p02.html') |
| m03-p03 | empty | m03-p03 | 搜索关键词 | 可用 | 原生输入/选择器 |
| m03-p03 | empty | m03-p03 | 清除搜索 | 可用 | ()=>{query.value='';query.focus();if(page==='m03-p04'){sessionStorage.removeItem('dujia-prototype-last-query');UI.go('m03-p03.html');}} |
| m03-p03 | empty | m03-p03 | 晚霞 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | empty | m03-p03 | 火锅 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | empty | m03-p03 | 旅行 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | empty | m03-p03 | 日记 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | empty | m03-p03 | 照片 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | empty | m03-p03 | 旅行 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | empty | m03-p03 | 纪念日 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | populated | m03-p03 | 返回首页 | 可用 | PrototypeUI.back('m03-p02.html') |
| m03-p03 | populated | m03-p03 | 搜索关键词 | 可用 | 原生输入/选择器 |
| m03-p03 | populated | m03-p03 | 清除搜索 | 可用 | ()=>{query.value='';query.focus();if(page==='m03-p04'){sessionStorage.removeItem('dujia-prototype-last-query');UI.go('m03-p03.html');}} |
| m03-p03 | populated | m03-p03 | 晚霞 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | populated | m03-p03 | 火锅 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | populated | m03-p03 | 旅行 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | populated | m03-p03 | 日记 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | populated | m03-p03 | 照片 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | populated | m03-p03 | 旅行 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p03 | populated | m03-p03 | 纪念日 | 可用 | ()=>{query.value=b.dataset.query;submit();} |
| m03-p04 | empty | m03-p04 | 返回搜索 | 可用 | PrototypeUI.back('m03-p03.html') |
| m03-p04 | empty | m03-p04 | 搜索关键词 | 可用 | 原生输入/选择器 |
| m03-p04 | empty | m03-p04 | 清除 | 可用 | PrototypeUI.go('m03-p03.html') |
| m03-p04 | empty | m03-p04 | 重新搜索 | 可用 | ()=>UI.go('m03-p03.html') |
| m03-p04 | populated | m03-p04 | 返回搜索 | 可用 | PrototypeUI.back('m03-p03.html') |
| m03-p04 | populated | m03-p04 | 搜索关键词 | 可用 | 原生输入/选择器 |
| m03-p04 | populated | m03-p04 | 清除 | 可用 | PrototypeUI.go('m03-p03.html') |
| m03-p04 | populated | m03-p04 | 共同日记  真正可编辑的共同正文  共同可见 | 可用 | ()=>UI.go(R.route(item)) |
| m03-p04 | populated | m03-p04 | 自己的日记  独立私密正文  仅自己可见 | 可用 | ()=>UI.go(R.route(item)) |
| m03-p04 | populated | m03-p04 | 共同照片  共同可见 | 可用 | ()=>UI.go(R.route(item)) |
| m03-p05 | empty | m03-p05 | 返回首页 | 可用 | ()=>page==='m03-p06'?UI.go('m03-p02.html',{replace:true}):page==='m03-p07'／／page==='m03-p08'?UI.go('m03-p06.html',{replace:true}):UI.back('m03-p06.html') |
| m03-p05 | empty | m03-p05 | 存草稿 | 可用 | ()=>save('draft',document.querySelector('#top-save')) |
| m03-p05 | empty | m03-p05 | 日记标题 | 可用 | 原生输入/选择器 |
| m03-p05 | empty | m03-p05 | 今天的心情 | 可用 | 原生输入/选择器 |
| m03-p05 | empty | m03-p05 | 日记正文 | 可用 | 原生输入/选择器 |
| m03-p05 | empty | m03-p05 | 移除照片 | 隐藏/禁用 | ()=>{image=null;sampleImage=false;file.value='';paintImage();} |
| m03-p05 | empty | m03-p05 | 添加照片 | 可用 | ()=>file.click() |
| m03-p05 | empty | m03-p05 | file | 隐藏/禁用 | 原生输入/选择器 |
| m03-p05 | empty | m03-p05 | visibility | 可用 | 原生输入/选择器 |
| m03-p05 | empty | m03-p05 | visibility | 可用 | 原生输入/选择器 |
| m03-p05 | empty | m03-p05 | 保存日记 | 可用 | 委托候选/待复核 |
| m03-p05 | populated | m03-p05 | 返回首页 | 可用 | ()=>page==='m03-p06'?UI.go('m03-p02.html',{replace:true}):page==='m03-p07'／／page==='m03-p08'?UI.go('m03-p06.html',{replace:true}):UI.back('m03-p06.html') |
| m03-p05 | populated | m03-p05 | 存草稿 | 可用 | ()=>save('draft',document.querySelector('#top-save')) |
| m03-p05 | populated | m03-p05 | 日记标题 | 可用 | 原生输入/选择器 |
| m03-p05 | populated | m03-p05 | 今天的心情 | 可用 | 原生输入/选择器 |
| m03-p05 | populated | m03-p05 | 日记正文 | 可用 | 原生输入/选择器 |
| m03-p05 | populated | m03-p05 | 移除照片 | 隐藏/禁用 | ()=>{image=null;sampleImage=false;file.value='';paintImage();} |
| m03-p05 | populated | m03-p05 | 添加照片 | 可用 | ()=>file.click() |
| m03-p05 | populated | m03-p05 | file | 隐藏/禁用 | 原生输入/选择器 |
| m03-p05 | populated | m03-p05 | visibility | 可用 | 原生输入/选择器 |
| m03-p05 | populated | m03-p05 | visibility | 可用 | 原生输入/选择器 |
| m03-p05 | populated | m03-p05 | 保存日记 | 可用 | 委托候选/待复核 |
| m03-p06 | empty | m03-p06 | 返回首页 | 可用 | ()=>page==='m03-p06'?UI.go('m03-p02.html',{replace:true}):page==='m03-p07'／／page==='m03-p08'?UI.go('m03-p06.html',{replace:true}):UI.back('m03-p06.html') |
| m03-p06 | empty | m03-p06 | 筛选日记 | 可用 | async()=>{const label=document.createElement('label');label.textContent='可见范围';const select=document.createElement('select');select.setAttribute('aria-label','可见范围');for(const [value,name]of[['all','全部'],['shared','共同可见'],['private','仅自己可见']]){const opt=document.createElement('option');opt.value=value;opt.textContent=name;select.append(opt);}select.value=visibility;label.append(select);const result=await UI.sheet({title:'筛选日记',content:label,actions:[{label:'应用筛选',value:'apply'},{label:'清除筛选',value:'clear'}]});if(result){visibility=result==='clear'?'all':select.value;persist();render();}} |
| m03-p06 | empty | m03-p06 | 全部 | 可用 | ()=>{tab=b.dataset.tab;persist();render();} |
| m03-p06 | empty | m03-p06 | 草稿 0 | 可用 | ()=>{tab=b.dataset.tab;persist();render();} |
| m03-p06 | empty | m03-p06 | 写日记 | 可用 | ()=>UI.go('m03-p05.html') |
| m03-p06 | empty | m03-p06 | 写第一篇日记 | 可用 | ()=>{if(visibility!=='all'){visibility='all';persist();render();}else UI.go('m03-p05.html');} |
| m03-p06 | empty | m03-p06 | 刷新日记 | 可用 | async function load(){       if(loading)return;loading=true;refresh.disabled=true;list.replaceChildren();list.setAttribute('aria-busy','true');const message=document.createElement('p');message.setAttribute('role','status');message.textContent='正在打开日记…';list.append(message);       await new Promise(resolve=>setTimeout(resolve,400));list.removeAttribute('aria-busy');loading=false;refresh.disabled=false;       if(UI.failNext('diary-load')){list.replaceChildren();const box=document.createElement('div');box.className='prototype-diary-empty';const title=document.createElement('h2');title.textContent |
| m03-p06 | populated | m03-p06 | 返回首页 | 可用 | ()=>page==='m03-p06'?UI.go('m03-p02.html',{replace:true}):page==='m03-p07'／／page==='m03-p08'?UI.go('m03-p06.html',{replace:true}):UI.back('m03-p06.html') |
| m03-p06 | populated | m03-p06 | 筛选日记 | 可用 | async()=>{const label=document.createElement('label');label.textContent='可见范围';const select=document.createElement('select');select.setAttribute('aria-label','可见范围');for(const [value,name]of[['all','全部'],['shared','共同可见'],['private','仅自己可见']]){const opt=document.createElement('option');opt.value=value;opt.textContent=name;select.append(opt);}select.value=visibility;label.append(select);const result=await UI.sheet({title:'筛选日记',content:label,actions:[{label:'应用筛选',value:'apply'},{label:'清除筛选',value:'clear'}]});if(result){visibility=result==='clear'?'all':select.value;persist();render();}} |
| m03-p06 | populated | m03-p06 | 全部 | 可用 | ()=>{tab=b.dataset.tab;persist();render();} |
| m03-p06 | populated | m03-p06 | 草稿 0 | 可用 | ()=>{tab=b.dataset.tab;persist();render();} |
| m03-p06 | populated | m03-p06 | 写日记 | 可用 | ()=>UI.go('m03-p05.html') |
| m03-p06 | populated | m03-p06 | 共同日记  真正可编辑的共同正文  小满 · Invalid Date · 共同可见 | 可用 | ()=>UI.go(route(item)) |
| m03-p06 | populated | m03-p06 | 自己的日记  独立私密正文  小满 · Invalid Date · 仅自己可见 | 可用 | ()=>UI.go(route(item)) |
| m03-p06 | populated | m03-p06 | 刷新日记 | 可用 | async function load(){       if(loading)return;loading=true;refresh.disabled=true;list.replaceChildren();list.setAttribute('aria-busy','true');const message=document.createElement('p');message.setAttribute('role','status');message.textContent='正在打开日记…';list.append(message);       await new Promise(resolve=>setTimeout(resolve,400));list.removeAttribute('aria-busy');loading=false;refresh.disabled=false;       if(UI.failNext('diary-load')){list.replaceChildren();const box=document.createElement('div');box.className='prototype-diary-empty';const title=document.createElement('h2');title.textContent |
| m03-p07 | empty | m03-p07 | 返回日记列表 | 可用 | ()=>page==='m03-p06'?UI.go('m03-p02.html',{replace:true}):page==='m03-p07'／／page==='m03-p08'?UI.go('m03-p06.html',{replace:true}):UI.back('m03-p06.html') |
| m03-p07 | empty | m03-p07 | 编辑日记 | 隐藏/禁用 | 委托候选/待复核 |
| m03-p07 | empty | m03-p07 | 更多操作 | 隐藏/禁用 | 委托候选/待复核 |
| m03-p07 | empty | m03-p07 | 返回日记列表 | 可用 | ()=>UI.go('m03-p06.html',{force:true}) |
| m03-p07 | populated | m03-p07 | 返回日记列表 | 可用 | ()=>page==='m03-p06'?UI.go('m03-p02.html',{replace:true}):page==='m03-p07'／／page==='m03-p08'?UI.go('m03-p06.html',{replace:true}):UI.back('m03-p06.html') |
| m03-p07 | populated | m03-p07 | 编辑日记 | 可用 | ()=>UI.go('m03-p05.html?id='+encodeURIComponent(item.id)) |
| m03-p07 | populated | m03-p07 | 更多操作 | 可用 | async()=>{       const action=await UI.sheet({title:'日记操作',actions:[{label:'删除日记',value:'delete',danger:true}]});       if(action!=='delete')return;const confirmed=await UI.modal({title:'删除这篇日记？',message:'日记和其中的留言将一起删除。',cancel:'取消',confirm:'确认删除'});if(!confirmed)return;       await UI.busy(more,'删除中…',async()=>{if(UI.failNext('diary-delete'))throw new Error('删除没有完成，请重试');if(!UI.write(KEY,records().filter(r=>r.id!==item.id)))return false;return UI.go('m03-p06.html',{force:true});});     } |
| m03-p08 | empty | m03-p08 | 返回日记列表 | 可用 | ()=>page==='m03-p06'?UI.go('m03-p02.html',{replace:true}):page==='m03-p07'／／page==='m03-p08'?UI.go('m03-p06.html',{replace:true}):UI.back('m03-p06.html') |
| m03-p08 | empty | m03-p08 | 编辑日记 | 隐藏/禁用 | 委托候选/待复核 |
| m03-p08 | empty | m03-p08 | 给 TA 留一句话 | 隐藏/禁用 | 原生输入/选择器 |
| m03-p08 | empty | m03-p08 | 添加表情 | 隐藏/禁用 | 委托候选/待复核 |
| m03-p08 | empty | m03-p08 | 发送留言 | 隐藏/禁用 | 委托候选/待复核 |
| m03-p08 | empty | m03-p08 | 返回日记列表 | 可用 | ()=>UI.go('m03-p06.html',{force:true}) |
| m03-p08 | populated | m03-p08 | 返回日记列表 | 可用 | ()=>page==='m03-p06'?UI.go('m03-p02.html',{replace:true}):page==='m03-p07'／／page==='m03-p08'?UI.go('m03-p06.html',{replace:true}):UI.back('m03-p06.html') |
| m03-p08 | populated | m03-p08 | 编辑日记 | 可用 | ()=>UI.go('m03-p05.html?id='+encodeURIComponent(item.id)) |
| m03-p08 | populated | m03-p08 | 给 TA 留一句话 | 可用 | 原生输入/选择器 |
| m03-p08 | populated | m03-p08 | 添加表情 | 可用 | ()=>{input.value=(input.value+' ❤️').slice(0,300);input.focus();} |
| m03-p08 | populated | m03-p08 | 发送留言 | 可用 | 委托候选/待复核 |
| m03-p08 | populated | m03-p08 | 更多操作 | 可用 | async()=>{       const action=await UI.sheet({title:'日记操作',actions:[{label:'删除日记',value:'delete',danger:true}]});       if(action!=='delete')return;const confirmed=await UI.modal({title:'删除这篇日记？',message:'日记和其中的留言将一起删除。',cancel:'取消',confirm:'确认删除'});if(!confirmed)return;       await UI.busy(more,'删除中…',async()=>{if(UI.failNext('diary-delete'))throw new Error('删除没有完成，请重试');if(!UI.write(KEY,records().filter(r=>r.id!==item.id)))return false;return UI.go('m03-p06.html',{force:true});});     } |
| m03-p09 | empty | m03-p09 | 返回首页 | 可用 | ()=>UI.back(['m03-p09','m03-p10'].includes(page)?'m03-p02.html':'m03-p10.html') |
| m03-p09 | empty | m03-p09 | 添加第一张照片 | 可用 | ()=>UI.go('m03-p11.html') |
| m03-p09 | empty | m03-p09 | 从系统相册选择 | 可用 | ()=>UI.go('m03-p11.html') |
| m03-p09 | populated | m03-p10 | 返回首页 | 可用 | ()=>UI.back(['m03-p09','m03-p10'].includes(page)?'m03-p02.html':'m03-p10.html') |
| m03-p09 | populated | m03-p10 | 筛选照片 | 可用 | async()=>{const select=document.createElement('select');select.setAttribute('aria-label','照片可见范围');for(const[v,label]of[['all','全部'],['shared','共同可见'],['private','仅自己可见']]){const option=document.createElement('option');option.value=v;option.textContent=label;select.append(option);}select.value=visibility;const action=await UI.sheet({title:'筛选照片',content:select,actions:[{label:'应用筛选',value:'apply'},{label:'清除筛选',value:'clear'}]});if(action){visibility=action==='clear'?'all':select.value;if(action==='clear')tab=0;persist();render();}} |
| m03-p09 | populated | m03-p10 | 全部 | 可用 | ()=>{tab=i;persist();render();} |
| m03-p09 | populated | m03-p10 | 共同可见 | 可用 | ()=>{tab=i;persist();render();} |
| m03-p09 | populated | m03-p10 | 旅行 | 可用 | ()=>{tab=i;persist();render();} |
| m03-p09 | populated | m03-p10 | 共同照片 | 可用 | ()=>UI.go(R.route(item)) |
| m03-p09 | populated | m03-p10 | ＋ 添加照片 | 可用 | ()=>UI.go('m03-p11.html') |
| m03-p09 | populated | m03-p10 | 刷新相册 | 可用 | async function load(){if(loading)return;loading=true;refresh.disabled=true;grid.replaceChildren();grid.setAttribute('aria-busy','true');const text=document.createElement('p');text.textContent='正在打开相册…';text.setAttribute('role','status');grid.append(text);await new Promise(resolve=>setTimeout(resolve,400));grid.removeAttribute('aria-busy');loading=false;refresh.disabled=false;if(UI.failNext('photo-load')){grid.replaceChildren();const box=document.createElement('div');box.className='prototype-photo-empty';const title=document.createElement('h2');title.textContent='相册暂时打不开';const retry=document.c |
| m03-p10 | empty | m03-p09 | 返回首页 | 可用 | ()=>UI.back(['m03-p09','m03-p10'].includes(page)?'m03-p02.html':'m03-p10.html') |
| m03-p10 | empty | m03-p09 | 添加第一张照片 | 可用 | ()=>UI.go('m03-p11.html') |
| m03-p10 | empty | m03-p09 | 从系统相册选择 | 可用 | ()=>UI.go('m03-p11.html') |
| m03-p10 | populated | m03-p10 | 返回首页 | 可用 | ()=>UI.back(['m03-p09','m03-p10'].includes(page)?'m03-p02.html':'m03-p10.html') |
| m03-p10 | populated | m03-p10 | 筛选照片 | 可用 | async()=>{const select=document.createElement('select');select.setAttribute('aria-label','照片可见范围');for(const[v,label]of[['all','全部'],['shared','共同可见'],['private','仅自己可见']]){const option=document.createElement('option');option.value=v;option.textContent=label;select.append(option);}select.value=visibility;const action=await UI.sheet({title:'筛选照片',content:select,actions:[{label:'应用筛选',value:'apply'},{label:'清除筛选',value:'clear'}]});if(action){visibility=action==='clear'?'all':select.value;if(action==='clear')tab=0;persist();render();}} |
| m03-p10 | populated | m03-p10 | 全部 | 可用 | ()=>{tab=i;persist();render();} |
| m03-p10 | populated | m03-p10 | 共同可见 | 可用 | ()=>{tab=i;persist();render();} |
| m03-p10 | populated | m03-p10 | 旅行 | 可用 | ()=>{tab=i;persist();render();} |
| m03-p10 | populated | m03-p10 | 共同照片 | 可用 | ()=>UI.go(R.route(item)) |
| m03-p10 | populated | m03-p10 | ＋ 添加照片 | 可用 | ()=>UI.go('m03-p11.html') |
| m03-p10 | populated | m03-p10 | 刷新相册 | 可用 | async function load(){if(loading)return;loading=true;refresh.disabled=true;grid.replaceChildren();grid.setAttribute('aria-busy','true');const text=document.createElement('p');text.textContent='正在打开相册…';text.setAttribute('role','status');grid.append(text);await new Promise(resolve=>setTimeout(resolve,400));grid.removeAttribute('aria-busy');loading=false;refresh.disabled=false;if(UI.failNext('photo-load')){grid.replaceChildren();const box=document.createElement('div');box.className='prototype-photo-empty';const title=document.createElement('h2');title.textContent='相册暂时打不开';const retry=document.c |
| m03-p11 | empty | m03-p11 | 返回相册 | 可用 | ()=>UI.back(['m03-p09','m03-p10'].includes(page)?'m03-p02.html':'m03-p10.html') |
| m03-p11 | empty | m03-p11 | 完成 | 可用 | ()=>save(document.querySelector('#done')) |
| m03-p11 | empty | m03-p11 | 选择照片 | 可用 | ()=>file.click() |
| m03-p11 | empty | m03-p11 | file | 隐藏/禁用 | 原生输入/选择器 |
| m03-p11 | empty | m03-p11 | 照片心情 | 可用 | 原生输入/选择器 |
| m03-p11 | empty | m03-p11 | 照片日期 | 可用 | async()=>{const label=document.createElement('label');label.textContent='照片日期';const input=document.createElement('input');input.type='date';input.value=form.elements.date.value;input.setAttribute('aria-label','选择照片日期');label.append(input);const action=await UI.sheet({title:'选择照片日期',content:label,actions:[{label:'使用这个日期',value:'apply'}]});if(action==='apply'){if(!input.value／／new Date(input.value+'T00:00:00')>new Date()){UI.toast('请选择有效的过去日期','error');return;}form.elements.date.value=input.value;}} |
| m03-p11 | empty | m03-p11 | 照片标签 | 可用 | 原生输入/选择器 |
| m03-p11 | empty | m03-p11 | 添加标签 | 可用 | async()=>{const label=document.createElement('label');label.textContent='标签，用顿号分隔';const input=document.createElement('input');input.type='text';input.maxLength=100;input.value=form.elements.tag.value;input.setAttribute('aria-label','编辑照片标签');label.append(input);const action=await UI.sheet({title:'照片标签',content:label,actions:[{label:'使用这些标签',value:'apply'}]});if(action==='apply')form.elements.tag.value=input.value;} |
| m03-p11 | empty | m03-p11 | visibility | 可用 | 原生输入/选择器 |
| m03-p11 | empty | m03-p11 | visibility | 可用 | 原生输入/选择器 |
| m03-p11 | empty | m03-p11 | 保存照片 | 可用 | 委托候选/待复核 |
| m03-p11 | populated | m03-p11 | 返回相册 | 可用 | ()=>UI.back(['m03-p09','m03-p10'].includes(page)?'m03-p02.html':'m03-p10.html') |
| m03-p11 | populated | m03-p11 | 完成 | 可用 | ()=>save(document.querySelector('#done')) |
| m03-p11 | populated | m03-p11 | 更换照片 | 可用 | ()=>file.click() |
| m03-p11 | populated | m03-p11 | file | 隐藏/禁用 | 原生输入/选择器 |
| m03-p11 | populated | m03-p11 | 照片心情 | 可用 | 原生输入/选择器 |
| m03-p11 | populated | m03-p11 | 照片日期 | 可用 | async()=>{const label=document.createElement('label');label.textContent='照片日期';const input=document.createElement('input');input.type='date';input.value=form.elements.date.value;input.setAttribute('aria-label','选择照片日期');label.append(input);const action=await UI.sheet({title:'选择照片日期',content:label,actions:[{label:'使用这个日期',value:'apply'}]});if(action==='apply'){if(!input.value／／new Date(input.value+'T00:00:00')>new Date()){UI.toast('请选择有效的过去日期','error');return;}form.elements.date.value=input.value;}} |
| m03-p11 | populated | m03-p11 | 照片标签 | 可用 | 原生输入/选择器 |
| m03-p11 | populated | m03-p11 | 添加标签 | 可用 | async()=>{const label=document.createElement('label');label.textContent='标签，用顿号分隔';const input=document.createElement('input');input.type='text';input.maxLength=100;input.value=form.elements.tag.value;input.setAttribute('aria-label','编辑照片标签');label.append(input);const action=await UI.sheet({title:'照片标签',content:label,actions:[{label:'使用这些标签',value:'apply'}]});if(action==='apply')form.elements.tag.value=input.value;} |
| m03-p11 | populated | m03-p11 | visibility | 可用 | 原生输入/选择器 |
| m03-p11 | populated | m03-p11 | visibility | 可用 | 原生输入/选择器 |
| m03-p11 | populated | m03-p11 | 保存照片 | 可用 | 委托候选/待复核 |
| m03-p12 | empty | m03-p12 | 返回照片相册 | 可用 | ()=>UI.back(['m03-p09','m03-p10'].includes(page)?'m03-p02.html':'m03-p10.html') |
| m03-p12 | empty | m03-p12 | 编辑照片 | 隐藏/禁用 | 委托候选/待复核 |
| m03-p12 | empty | m03-p12 | 给 TA 留一句话 | 隐藏/禁用 | 原生输入/选择器 |
| m03-p12 | empty | m03-p12 | 添加表情 | 隐藏/禁用 | 委托候选/待复核 |
| m03-p12 | empty | m03-p12 | 发送留言 | 隐藏/禁用 | 委托候选/待复核 |
| m03-p12 | empty | m03-p12 | 返回相册 | 可用 | ()=>UI.go('m03-p10.html',{force:true}) |
| m03-p12 | populated | m03-p12 | 返回照片相册 | 可用 | ()=>UI.back(['m03-p09','m03-p10'].includes(page)?'m03-p02.html':'m03-p10.html') |
| m03-p12 | populated | m03-p12 | 编辑照片 | 可用 | ()=>UI.go('m03-p11.html?id='+encodeURIComponent(item.id)) |
| m03-p12 | populated | m03-p12 | 给 TA 留一句话 | 可用 | 原生输入/选择器 |
| m03-p12 | populated | m03-p12 | 添加表情 | 可用 | ()=>{input.value=(input.value+' ❤️').slice(0,300);input.focus();} |
| m03-p12 | populated | m03-p12 | 发送留言 | 可用 | 委托候选/待复核 |
| m03-p12 | populated | m03-p12 | 更多操作 | 可用 | async()=>{const action=await UI.sheet({title:'照片操作',actions:[{label:'删除照片',value:'delete',danger:true}]});if(action!=='delete'／／!await UI.modal({title:'删除这张照片？',message:'照片和其中的留言将一起删除。',confirm:'确认删除',cancel:'取消'}))return;UI.busy(more,'删除中…',()=>{if(UI.failNext('photo-delete'))throw new Error('删除没有完成，请重试');if(!R.remove(item.id))return false;return goAlbum();});} |
| m04-p01 | empty | m04-p02 | 从共同记录中收录 | 可用 | ()=>UI.go('m04-p04.html?choose=1') |
| m04-p01 | empty | m04-p02 | 新建重要时刻 | 可用 | ()=>UI.go('m04-p04.html') |
| m04-p01 | empty | m04-p02 | 纪念日 | 可用 | ()=>UI.go(UI.read('dujia-prototype-anniversaries',[]).length?'m04-p07.html':'m04-p08.html') |
| m04-p01 | empty | m04-p02 | 时光胶囊 | 可用 | ()=>UI.go('m04-p12.html') |
| m04-p01 | empty | m04-p02 | 悄悄留言 | 可用 | ()=>UI.go(replies().length?'m04-p16.html':'m04-p17.html') |
| m04-p01 | empty | m04-p02 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p01 | empty | m04-p02 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p01 | empty | m04-p02 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p01 | empty | m04-p02 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p01 | empty | m04-p02 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p01 | populated | m04-p01 | 查看纪念日 | 可用 | ()=>UI.go(UI.read('dujia-prototype-anniversaries',[]).length?'m04-p07.html':'m04-p08.html') |
| m04-p01 | populated | m04-p01 | 珍藏一个新时刻 | 可用 | ()=>UI.go(next?route(next):'m04-p04.html') |
| m04-p01 | populated | m04-p01 | 查看全部 › | 可用 | ()=>{expanded=!expanded;document.querySelector('#see-all').textContent=expanded?'收起章节':'查看全部 ›';paint();} |
| m04-p01 | populated | m04-p01 | 共同重要时刻 2026-10-04 | 可用 | ()=>UI.go(route(item)) |
| m04-p01 | populated | m04-p01 | 纪念日 | 可用 | ()=>UI.go(UI.read('dujia-prototype-anniversaries',[]).length?'m04-p07.html':'m04-p08.html') |
| m04-p01 | populated | m04-p01 | 时光胶囊 | 可用 | ()=>UI.go('m04-p12.html') |
| m04-p01 | populated | m04-p01 | 悄悄留言 | 可用 | ()=>UI.go(replies().length?'m04-p16.html':'m04-p17.html') |
| m04-p01 | populated | m04-p01 | 新建重要时刻 | 可用 | ()=>UI.go('m04-p04.html') |
| m04-p01 | populated | m04-p01 | 刷新时刻册 | 可用 | async function load(){if(loading)return;loading=true;refresh.disabled=true;document.querySelector('#see-all').disabled=true;cards.replaceChildren();cards.setAttribute('aria-busy','true');const message=document.createElement('p');message.textContent='正在打开时刻册…';message.setAttribute('role','status');cards.append(message);await new Promise(resolve=>setTimeout(resolve,400));loading=false;refresh.disabled=false;document.querySelector('#see-all').disabled=false;cards.removeAttribute('aria-busy');if(UI.failNext('moment-load')){cards.replaceChildren();const box=document.createElement('div');box.classNa |
| m04-p01 | populated | m04-p01 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p01 | populated | m04-p01 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p01 | populated | m04-p01 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p01 | populated | m04-p01 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p01 | populated | m04-p01 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p02 | empty | m04-p02 | 从共同记录中收录 | 可用 | ()=>UI.go('m04-p04.html?choose=1') |
| m04-p02 | empty | m04-p02 | 新建重要时刻 | 可用 | ()=>UI.go('m04-p04.html') |
| m04-p02 | empty | m04-p02 | 纪念日 | 可用 | ()=>UI.go(UI.read('dujia-prototype-anniversaries',[]).length?'m04-p07.html':'m04-p08.html') |
| m04-p02 | empty | m04-p02 | 时光胶囊 | 可用 | ()=>UI.go('m04-p12.html') |
| m04-p02 | empty | m04-p02 | 悄悄留言 | 可用 | ()=>UI.go(replies().length?'m04-p16.html':'m04-p17.html') |
| m04-p02 | empty | m04-p02 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p02 | empty | m04-p02 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p02 | empty | m04-p02 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p02 | empty | m04-p02 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p02 | empty | m04-p02 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p02 | populated | m04-p01 | 查看纪念日 | 可用 | ()=>UI.go(UI.read('dujia-prototype-anniversaries',[]).length?'m04-p07.html':'m04-p08.html') |
| m04-p02 | populated | m04-p01 | 珍藏一个新时刻 | 可用 | ()=>UI.go(next?route(next):'m04-p04.html') |
| m04-p02 | populated | m04-p01 | 查看全部 › | 可用 | ()=>{expanded=!expanded;document.querySelector('#see-all').textContent=expanded?'收起章节':'查看全部 ›';paint();} |
| m04-p02 | populated | m04-p01 | 共同重要时刻 2026-10-04 | 可用 | ()=>UI.go(route(item)) |
| m04-p02 | populated | m04-p01 | 纪念日 | 可用 | ()=>UI.go(UI.read('dujia-prototype-anniversaries',[]).length?'m04-p07.html':'m04-p08.html') |
| m04-p02 | populated | m04-p01 | 时光胶囊 | 可用 | ()=>UI.go('m04-p12.html') |
| m04-p02 | populated | m04-p01 | 悄悄留言 | 可用 | ()=>UI.go(replies().length?'m04-p16.html':'m04-p17.html') |
| m04-p02 | populated | m04-p01 | 新建重要时刻 | 可用 | ()=>UI.go('m04-p04.html') |
| m04-p02 | populated | m04-p01 | 刷新时刻册 | 可用 | async function load(){if(loading)return;loading=true;refresh.disabled=true;document.querySelector('#see-all').disabled=true;cards.replaceChildren();cards.setAttribute('aria-busy','true');const message=document.createElement('p');message.textContent='正在打开时刻册…';message.setAttribute('role','status');cards.append(message);await new Promise(resolve=>setTimeout(resolve,400));loading=false;refresh.disabled=false;document.querySelector('#see-all').disabled=false;cards.removeAttribute('aria-busy');if(UI.failNext('moment-load')){cards.replaceChildren();const box=document.createElement('div');box.classNa |
| m04-p02 | populated | m04-p01 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p02 | populated | m04-p01 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p02 | populated | m04-p01 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p02 | populated | m04-p01 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p02 | populated | m04-p01 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m04-p03 | empty | m04-p03 | 返回重要时刻 | 可用 | ()=>UI.back(page==='m04-p04'&&id&&find(id)?route(find(id)):home()) |
| m04-p03 | empty | m04-p03 | 野餐日记前往共同记录查看 | 隐藏/禁用 | 委托候选/待复核 |
| m04-p03 | empty | m04-p03 | 12 张照片前往共同记录查看 | 隐藏/禁用 | 委托候选/待复核 |
| m04-p03 | empty | m04-p03 | 悄悄留言 3 条 | 隐藏/禁用 | 委托候选/待复核 |
| m04-p03 | empty | m04-p03 | 返回时刻册 | 可用 | ()=>UI.go(home(),{force:true}) |
| m04-p03 | populated | m04-p03 | 返回重要时刻 | 可用 | ()=>UI.back(page==='m04-p04'&&id&&find(id)?route(find(id)):home()) |
| m04-p03 | populated | m04-p03 | 悄悄留言 0 条 | 可用 | ()=>{const box=document.createElement('div');for(const comment of item.comments／／[]){const p=document.createElement('p');p.textContent=comment.author+'：'+comment.text;box.append(p);}const form=document.createElement('form'),input=document.createElement('textarea'),button=document.createElement('button');form.className='prototype-moment-reply-form';input.maxLength=300;input.setAttribute('aria-label','回应这个时刻');button.type='submit';button.textContent='发送回应';if(window.PrototypePreferences?.privacy().replies===false){input.disabled=true;button.disabled=true;input.placeholder='新的回应已关闭';}form.append( |
| m04-p03 | populated | m04-p03 | 编辑时刻 | 可用 | ()=>UI.go('m04-p04.html?id='+encodeURIComponent(item.id)) |
| m04-p03 | populated | m04-p03 | 更多操作 | 可用 | async()=>{const action=await UI.sheet({title:'时刻操作',actions:[{label:'删除重要时刻',value:'delete',danger:true}]});if(action!=='delete'／／!await UI.modal({title:'删除这个时刻？',message:'时刻及其中的留言将删除，关联的日记和照片仍保留。',confirm:'确认删除',cancel:'取消'}))return;UI.busy(more,'删除中…',()=>{if(UI.failNext('moment-delete'))throw new Error('删除没有完成，请重试');if(!UI.write(KEY,all().filter(v=>v.id!==item.id)))return false;return UI.go(home(),{force:true});});} |
| m04-p04 | empty | m04-p04 | 返回重要时刻 | 可用 | ()=>UI.back(page==='m04-p04'&&id&&find(id)?route(find(id)):home()) |
| m04-p04 | empty | m04-p04 | 添加封面 | 可用 | ()=>file.click() |
| m04-p04 | empty | m04-p04 | cover-file | 隐藏/禁用 | 原生输入/选择器 |
| m04-p04 | empty | m04-p04 | name | 可用 | 原生输入/选择器 |
| m04-p04 | empty | m04-p04 | 发生日期 | 可用 | async()=>{const input=document.createElement('input');input.type='date';input.value=form.elements.date.value;input.setAttribute('aria-label','选择发生日期');const action=await UI.sheet({title:'发生日期',content:input,actions:[{label:'使用这个日期',value:'apply'}]});if(action==='apply'&&input.value)form.elements.date.value=input.value;} |
| m04-p04 | empty | m04-p04 | type | 可用 | 原生输入/选择器 |
| m04-p04 | empty | m04-p04 | type | 可用 | 原生输入/选择器 |
| m04-p04 | empty | m04-p04 | type | 可用 | 原生输入/选择器 |
| m04-p04 | empty | m04-p04 | type | 可用 | 原生输入/选择器 |
| m04-p04 | empty | m04-p04 | 记录这个时刻背后的故事… | 可用 | 原生输入/选择器 |
| m04-p04 | empty | m04-p04 | 关联共同记录，已选 0 条 | 可用 | async function choose(){const box=document.createElement('div'),records=R.all().filter(v=>v.visibility==='shared'&&v.status!=='draft');if(!records.length){box.textContent='还没有共同记录，可以先写日记或添加照片。';const create=await UI.modal({title:'选择共同记录',content:box,confirm:'去写日记',cancel:'继续创建时刻'});if(create)UI.go('m03-p05.html');return;}for(const record of records){const row=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.value=record.id;input.checked=selected.includes(record.id);row.className='prototype-record-choice';row.append(input,document.createTextNode( |
| m04-p04 | empty | m04-p04 | 保存到时刻册 | 可用 | 委托候选/待复核 |
| m04-p04 | populated | m04-p04 | 返回重要时刻 | 可用 | ()=>UI.back(page==='m04-p04'&&id&&find(id)?route(find(id)):home()) |
| m04-p04 | populated | m04-p04 | 添加封面 | 可用 | ()=>file.click() |
| m04-p04 | populated | m04-p04 | cover-file | 隐藏/禁用 | 原生输入/选择器 |
| m04-p04 | populated | m04-p04 | name | 可用 | 原生输入/选择器 |
| m04-p04 | populated | m04-p04 | 发生日期 | 可用 | async()=>{const input=document.createElement('input');input.type='date';input.value=form.elements.date.value;input.setAttribute('aria-label','选择发生日期');const action=await UI.sheet({title:'发生日期',content:input,actions:[{label:'使用这个日期',value:'apply'}]});if(action==='apply'&&input.value)form.elements.date.value=input.value;} |
| m04-p04 | populated | m04-p04 | type | 可用 | 原生输入/选择器 |
| m04-p04 | populated | m04-p04 | type | 可用 | 原生输入/选择器 |
| m04-p04 | populated | m04-p04 | type | 可用 | 原生输入/选择器 |
| m04-p04 | populated | m04-p04 | type | 可用 | 原生输入/选择器 |
| m04-p04 | populated | m04-p04 | 记录这个时刻背后的故事… | 可用 | 原生输入/选择器 |
| m04-p04 | populated | m04-p04 | 关联共同记录，已选 0 条 | 可用 | async function choose(){const box=document.createElement('div'),records=R.all().filter(v=>v.visibility==='shared'&&v.status!=='draft');if(!records.length){box.textContent='还没有共同记录，可以先写日记或添加照片。';const create=await UI.modal({title:'选择共同记录',content:box,confirm:'去写日记',cancel:'继续创建时刻'});if(create)UI.go('m03-p05.html');return;}for(const record of records){const row=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.value=record.id;input.checked=selected.includes(record.id);row.className='prototype-record-choice';row.append(input,document.createTextNode( |
| m04-p04 | populated | m04-p04 | 保存到时刻册 | 可用 | 委托候选/待复核 |
| m04-p05 | empty | m04-p06 | 返回重要时刻 | 可用 | ()=>UI.back(['m04-p05','m04-p06','m04-p07','m04-p08'].includes(page)?'m04-p01.html':page==='m04-p09'&&id&&find(id)?route(find(id)):list()) |
| m04-p05 | empty | m04-p06 | 去看看重要时刻 | 可用 | ()=>UI.go('m04-p01.html') |
| m04-p05 | populated | m04-p05 | 返回重要时刻 | 可用 | ()=>UI.back(['m04-p05','m04-p06','m04-p07','m04-p08'].includes(page)?'m04-p01.html':page==='m04-p09'&&id&&find(id)?route(find(id)):list()) |
| m04-p05 | populated | m04-p05 | 实际工坊作品已完成  去看看这段回忆的创作吧 | 可用 | ()=>{const saved=UI.read(READ,[]),data=Array.isArray(saved)?saved:[];if(!UI.write(READ,[...data.filter(v=>v.id!==notice.id),{...notice,read:true,readAt:Date.now()}]))return;UI.go(notice.url);} |
| m04-p06 | empty | m04-p06 | 返回重要时刻 | 可用 | ()=>UI.back(['m04-p05','m04-p06','m04-p07','m04-p08'].includes(page)?'m04-p01.html':page==='m04-p09'&&id&&find(id)?route(find(id)):list()) |
| m04-p06 | empty | m04-p06 | 去看看重要时刻 | 可用 | ()=>UI.go('m04-p01.html') |
| m04-p06 | populated | m04-p05 | 返回重要时刻 | 可用 | ()=>UI.back(['m04-p05','m04-p06','m04-p07','m04-p08'].includes(page)?'m04-p01.html':page==='m04-p09'&&id&&find(id)?route(find(id)):list()) |
| m04-p06 | populated | m04-p05 | 实际工坊作品已完成  去看看这段回忆的创作吧 | 可用 | ()=>{const saved=UI.read(READ,[]),data=Array.isArray(saved)?saved:[];if(!UI.write(READ,[...data.filter(v=>v.id!==notice.id),{...notice,read:true,readAt:Date.now()}]))return;UI.go(notice.url);} |
| m04-p07 | empty | m04-p08 | 返回重要时刻 | 可用 | ()=>UI.back(['m04-p05','m04-p06','m04-p07','m04-p08'].includes(page)?'m04-p01.html':page==='m04-p09'&&id&&find(id)?route(find(id)):list()) |
| m04-p07 | empty | m04-p08 | 添加第一个纪念日 | 可用 | ()=>UI.go('m04-p09.html') |
| m04-p07 | populated | m04-p07 | 返回重要时刻 | 可用 | ()=>UI.back(['m04-p05','m04-p06','m04-p07','m04-p08'].includes(page)?'m04-p01.html':page==='m04-p09'&&id&&find(id)?route(find(id)):list()) |
| m04-p07 | populated | m04-p07 | 添加纪念日 | 可用 | ()=>UI.go('m04-p09.html') |
| m04-p07 | populated | m04-p07 | 2026-10-05 | 可用 | ()=>UI.go(route(first)) |
| m04-p07 | populated | m04-p07 | 今天的纪念日 每年 2026-10-05 | 可用 | ()=>UI.go(route(item)) |
| m04-p07 | populated | m04-p07 | 今天的纪念日提醒 | 可用 | ()=>UI.busy(toggle,'更新中…',()=>{if(UI.failNext('anniversary-toggle'))throw new Error('提醒设置未更新，请重试');if(!put({...item,enabled:!item.enabled}))return false;render();return true;}) |
| m04-p07 | populated | m04-p07 | 未来的纪念日 每年 2026-12-24 | 可用 | ()=>UI.go(route(item)) |
| m04-p07 | populated | m04-p07 | 未来的纪念日提醒 | 可用 | ()=>UI.busy(toggle,'更新中…',()=>{if(UI.failNext('anniversary-toggle'))throw new Error('提醒设置未更新，请重试');if(!put({...item,enabled:!item.enabled}))return false;render();return true;}) |
| m04-p07 | populated | m04-p07 | 添加纪念日 | 可用 | ()=>UI.go('m04-p09.html') |
| m04-p07 | populated | m04-p07 | 刷新纪念日 | 可用 | async function load(){if(loading)return;loading=true;refresh.disabled=true;entries.replaceChildren();entries.setAttribute('aria-busy','true');const text=document.createElement('p');text.textContent='正在打开纪念日…';text.setAttribute('role','status');entries.append(text);await new Promise(resolve=>setTimeout(resolve,400));loading=false;refresh.disabled=false;entries.removeAttribute('aria-busy');if(UI.failNext('anniversary-load')){entries.replaceChildren();const h=document.createElement('h2');h.textContent='纪念日暂时打不开';const retry=document.createElement('button');retry.textContent='重试加载纪念日';retry.onclic |
| m04-p08 | empty | m04-p08 | 返回重要时刻 | 可用 | ()=>UI.back(['m04-p05','m04-p06','m04-p07','m04-p08'].includes(page)?'m04-p01.html':page==='m04-p09'&&id&&find(id)?route(find(id)):list()) |
| m04-p08 | empty | m04-p08 | 添加第一个纪念日 | 可用 | ()=>UI.go('m04-p09.html') |
| m04-p08 | populated | m04-p07 | 返回重要时刻 | 可用 | ()=>UI.back(['m04-p05','m04-p06','m04-p07','m04-p08'].includes(page)?'m04-p01.html':page==='m04-p09'&&id&&find(id)?route(find(id)):list()) |
| m04-p08 | populated | m04-p07 | 添加纪念日 | 可用 | ()=>UI.go('m04-p09.html') |
| m04-p08 | populated | m04-p07 | 2026-10-05 | 可用 | ()=>UI.go(route(first)) |
| m04-p08 | populated | m04-p07 | 今天的纪念日 每年 2026-10-05 | 可用 | ()=>UI.go(route(item)) |
| m04-p08 | populated | m04-p07 | 今天的纪念日提醒 | 可用 | ()=>UI.busy(toggle,'更新中…',()=>{if(UI.failNext('anniversary-toggle'))throw new Error('提醒设置未更新，请重试');if(!put({...item,enabled:!item.enabled}))return false;render();return true;}) |
| m04-p08 | populated | m04-p07 | 未来的纪念日 每年 2026-12-24 | 可用 | ()=>UI.go(route(item)) |
| m04-p08 | populated | m04-p07 | 未来的纪念日提醒 | 可用 | ()=>UI.busy(toggle,'更新中…',()=>{if(UI.failNext('anniversary-toggle'))throw new Error('提醒设置未更新，请重试');if(!put({...item,enabled:!item.enabled}))return false;render();return true;}) |
| m04-p08 | populated | m04-p07 | 添加纪念日 | 可用 | ()=>UI.go('m04-p09.html') |
| m04-p08 | populated | m04-p07 | 刷新纪念日 | 可用 | async function load(){if(loading)return;loading=true;refresh.disabled=true;entries.replaceChildren();entries.setAttribute('aria-busy','true');const text=document.createElement('p');text.textContent='正在打开纪念日…';text.setAttribute('role','status');entries.append(text);await new Promise(resolve=>setTimeout(resolve,400));loading=false;refresh.disabled=false;entries.removeAttribute('aria-busy');if(UI.failNext('anniversary-load')){entries.replaceChildren();const h=document.createElement('h2');h.textContent='纪念日暂时打不开';const retry=document.createElement('button');retry.textContent='重试加载纪念日';retry.onclic |
| m04-p09 | empty | m04-p09 | 返回纪念日列表 | 可用 | ()=>UI.back(['m04-p05','m04-p06','m04-p07','m04-p08'].includes(page)?'m04-p01.html':page==='m04-p09'&&id&&find(id)?route(find(id)):list()) |
| m04-p09 | empty | m04-p09 | name | 可用 | 原生输入/选择器 |
| m04-p09 | empty | m04-p09 | 纪念日日期 | 可用 | async()=>{const input=document.createElement('input');input.type='date';input.value=form.elements.date.value;input.min='1900-01-01';input.setAttribute('aria-label','选择纪念日日期');const action=await UI.sheet({title:'纪念日日期',content:input,actions:[{label:'使用这个日期',value:'apply'}]});if(action==='apply'){if(!D.parse(input.value)){UI.fieldError(form.elements.date,'请选择有效日期');return;}form.elements.date.value=input.value;}} |
| m04-p09 | empty | m04-p09 | 提前 3 天 提前 1 天 当天 不提醒 | 可用 | 原生输入/选择器 |
| m04-p09 | empty | m04-p09 | 每年重复 | 可用 | 原生输入/选择器 |
| m04-p09 | empty | m04-p09 | 可选 · 关联一段章节 | 可用 | 原生输入/选择器 |
| m04-p09 | empty | m04-p09 | 保存纪念日 | 可用 | 委托候选/待复核 |
| m04-p09 | populated | m04-p09 | 返回纪念日列表 | 可用 | ()=>UI.back(['m04-p05','m04-p06','m04-p07','m04-p08'].includes(page)?'m04-p01.html':page==='m04-p09'&&id&&find(id)?route(find(id)):list()) |
| m04-p09 | populated | m04-p09 | name | 可用 | 原生输入/选择器 |
| m04-p09 | populated | m04-p09 | 纪念日日期 | 可用 | async()=>{const input=document.createElement('input');input.type='date';input.value=form.elements.date.value;input.min='1900-01-01';input.setAttribute('aria-label','选择纪念日日期');const action=await UI.sheet({title:'纪念日日期',content:input,actions:[{label:'使用这个日期',value:'apply'}]});if(action==='apply'){if(!D.parse(input.value)){UI.fieldError(form.elements.date,'请选择有效日期');return;}form.elements.date.value=input.value;}} |
| m04-p09 | populated | m04-p09 | 提前 3 天 提前 1 天 当天 不提醒 | 可用 | 原生输入/选择器 |
| m04-p09 | populated | m04-p09 | 每年重复 | 可用 | 原生输入/选择器 |
| m04-p09 | populated | m04-p09 | 可选 · 关联一段章节 共同重要时刻 | 可用 | 原生输入/选择器 |
| m04-p09 | populated | m04-p09 | 保存纪念日 | 可用 | 委托候选/待复核 |
| m04-p10 | empty | m04-p10 | 返回纪念日 | 可用 | ()=>UI.back(['m04-p05','m04-p06','m04-p07','m04-p08'].includes(page)?'m04-p01.html':page==='m04-p09'&&id&&find(id)?route(find(id)):list()) |
| m04-p10 | empty | m04-p10 | 春日野餐 | 隐藏/禁用 | 委托候选/待复核 |
| m04-p10 | empty | m04-p10 | 那年九月的日记 | 隐藏/禁用 | 委托候选/待复核 |
| m04-p10 | empty | m04-p10 | 写下新的共同记录 | 隐藏/禁用 | 委托候选/待复核 |
| m04-p10 | empty | m04-p10 | 返回纪念日列表 | 可用 | ()=>UI.go(list(),{force:true}) |
| m04-p10 | populated | m04-p10 | 返回纪念日 | 可用 | ()=>UI.back(['m04-p05','m04-p06','m04-p07','m04-p08'].includes(page)?'m04-p01.html':page==='m04-p09'&&id&&find(id)?route(find(id)):list()) |
| m04-p10 | populated | m04-p10 | 共同重要时刻 | 可用 | ()=>UI.go('m04-p03.html?id='+encodeURIComponent(moment.id)) |
| m04-p10 | populated | m04-p10 | 写下新的共同记录 | 可用 | ()=>UI.go(recordURL) |
| m04-p10 | populated | m04-p10 | 编辑纪念日 | 可用 | ()=>UI.go('m04-p09.html?id='+encodeURIComponent(item.id)) |
| m04-p10 | populated | m04-p10 | 更多操作 | 可用 | async()=>{const action=await UI.sheet({title:'纪念日操作',actions:[{label:'删除纪念日',value:'delete',danger:true}]});if(action!=='delete'／／!await UI.modal({title:'删除这个纪念日？',message:'相关时刻和日记仍保留。',confirm:'确认删除',cancel:'取消'}))return;UI.busy(more,'删除中…',()=>{if(UI.failNext('anniversary-delete'))throw new Error('删除没有完成，请重试');if(!UI.write(KEY,all().filter(v=>v.id!==item.id)))return false;return UI.go(list(),{force:true});});} |
| m04-p11 | empty | m04-p11 | 一起留下今天的记录 | 隐藏/禁用 | 委托候选/待复核 |
| m04-p11 | empty | m04-p11 | 查看这个时刻 | 隐藏/禁用 | 委托候选/待复核 |
| m04-p11 | empty | m04-p11 | 返回纪念日列表 | 可用 | ()=>UI.go(list(),{force:true}) |
| m04-p11 | populated | m04-p11 | 一起留下今天的记录 | 可用 | ()=>UI.go(recordURL) |
| m04-p11 | populated | m04-p11 | 关联一个重要时刻 | 可用 | ()=>UI.go(moment?'m04-p03.html?id='+encodeURIComponent(moment.id):'m04-p09.html?id='+encodeURIComponent(item.id)) |
| m04-p11 | populated | m04-p11 | 返回纪念日列表 | 可用 | ()=>UI.back(list()) |
| m04-p11 | populated | m04-p11 | 编辑纪念日 | 可用 | ()=>UI.go('m04-p09.html?id='+encodeURIComponent(item.id)) |
| m04-p11 | populated | m04-p11 | 更多操作 | 可用 | async()=>{const action=await UI.sheet({title:'纪念日操作',actions:[{label:'删除纪念日',value:'delete',danger:true}]});if(action!=='delete'／／!await UI.modal({title:'删除这个纪念日？',message:'相关时刻和日记仍保留。',confirm:'确认删除',cancel:'取消'}))return;UI.busy(more,'删除中…',()=>{if(UI.failNext('anniversary-delete'))throw new Error('删除没有完成，请重试');if(!UI.write(KEY,all().filter(v=>v.id!==item.id)))return false;return UI.go(list(),{force:true});});} |
| m04-p12 | empty | m04-p12 | 返回重要时刻 | 可用 | ()=>UI.back(page==='m04-p12'?'m04-p01.html':home) |
| m04-p12 | empty | m04-p12 | 新建时光胶囊 | 可用 | ()=>UI.go('m04-p13.html') |
| m04-p12 | empty | m04-p12 | 等待开启 | 可用 | ()=>{selected=['sealed','opened','draft'][i];if(!loading)paint();} |
| m04-p12 | empty | m04-p12 | 已经开启 | 可用 | ()=>{selected=['sealed','opened','draft'][i];if(!loading)paint();} |
| m04-p12 | empty | m04-p12 | 草稿 | 可用 | ()=>{selected=['sealed','opened','draft'][i];if(!loading)paint();} |
| m04-p12 | empty | m04-p12 | 写给未来的我们 | 可用 | ()=>UI.go('m04-p13.html') |
| m04-p12 | empty | m04-p12 | ＋ 新建时光胶囊 | 可用 | ()=>UI.go('m04-p13.html') |
| m04-p12 | empty | m04-p12 | 刷新胶囊 | 可用 | async function load(){if(loading)return;loading=true;cards.setAttribute('aria-busy','true');cards.textContent='正在打开胶囊架…';await new Promise(r=>setTimeout(r,400));loading=false;cards.removeAttribute('aria-busy');if(UI.failNext('capsule-load')){cards.replaceChildren();const p=document.createElement('p');p.textContent='胶囊架暂时打不开';const retry=document.createElement('button');retry.textContent='重试加载胶囊';retry.onclick=load;cards.append(p,retry);}else paint();} |
| m04-p12 | populated | m04-p12 | 返回重要时刻 | 可用 | ()=>UI.back(page==='m04-p12'?'m04-p01.html':home) |
| m04-p12 | populated | m04-p12 | 新建时光胶囊 | 可用 | ()=>UI.go('m04-p13.html') |
| m04-p12 | populated | m04-p12 | 等待开启 | 可用 | ()=>{selected=['sealed','opened','draft'][i];if(!loading)paint();} |
| m04-p12 | populated | m04-p12 | 已经开启 | 可用 | ()=>{selected=['sealed','opened','draft'][i];if(!loading)paint();} |
| m04-p12 | populated | m04-p12 | 草稿 | 可用 | ()=>{selected=['sealed','opened','draft'][i];if(!loading)paint();} |
| m04-p12 | populated | m04-p12 | 未来的信 2026-12-24 · 还有 80 天 | 可用 | ()=>UI.go(C.route(item)) |
| m04-p12 | populated | m04-p12 | ＋ 新建时光胶囊 | 可用 | ()=>UI.go('m04-p13.html') |
| m04-p12 | populated | m04-p12 | 刷新胶囊 | 可用 | async function load(){if(loading)return;loading=true;cards.setAttribute('aria-busy','true');cards.textContent='正在打开胶囊架…';await new Promise(r=>setTimeout(r,400));loading=false;cards.removeAttribute('aria-busy');if(UI.failNext('capsule-load')){cards.replaceChildren();const p=document.createElement('p');p.textContent='胶囊架暂时打不开';const retry=document.createElement('button');retry.textContent='重试加载胶囊';retry.onclick=load;cards.append(p,retry);}else paint();} |
| m04-p13 | empty | m04-p13 | 返回胶囊列表 | 可用 | ()=>UI.back(page==='m04-p12'?'m04-p01.html':home) |
| m04-p13 | empty | m04-p13 | name | 可用 | 原生输入/选择器 |
| m04-p13 | empty | m04-p13 | message | 可用 | 原生输入/选择器 |
| m04-p13 | empty | m04-p13 | 添加照片 | 可用 | ()=>file.click() |
| m04-p13 | empty | m04-p13 | photo | 隐藏/禁用 | 原生输入/选择器 |
| m04-p13 | empty | m04-p13 | opening | 可用 | async()=>{const input=document.createElement('input');input.type='date';input.value=form.elements.opening.value;input.min=D.today().iso;input.setAttribute('aria-label','胶囊开启日期');const action=await UI.sheet({title:'开启日期',content:input,actions:[{label:'使用这个日期',value:'apply'}]});if(action==='apply'){if(!D.parse(input.value)){UI.fieldError(form.elements.opening,'请选择有效日期');return;}form.elements.opening.value=input.value;UI.fieldError(form.elements.opening,'');}} |
| m04-p13 | empty | m04-p13 | 开启提醒 | 可用 | 原生输入/选择器 |
| m04-p13 | empty | m04-p13 | 暂存草稿 | 可用 | ()=>save('draft',buttons[0]) |
| m04-p13 | empty | m04-p13 | 封存这份心意 | 可用 | 委托候选/待复核 |
| m04-p13 | empty | m04-p13 | 移除照片 | 隐藏/禁用 | ()=>{photo=null;file.value='';paint();} |
| m04-p13 | populated | m04-p13 | 返回胶囊列表 | 可用 | ()=>UI.back(page==='m04-p12'?'m04-p01.html':home) |
| m04-p13 | populated | m04-p13 | name | 可用 | 原生输入/选择器 |
| m04-p13 | populated | m04-p13 | message | 可用 | 原生输入/选择器 |
| m04-p13 | populated | m04-p13 | 添加照片 | 可用 | ()=>file.click() |
| m04-p13 | populated | m04-p13 | photo | 隐藏/禁用 | 原生输入/选择器 |
| m04-p13 | populated | m04-p13 | opening | 可用 | async()=>{const input=document.createElement('input');input.type='date';input.value=form.elements.opening.value;input.min=D.today().iso;input.setAttribute('aria-label','胶囊开启日期');const action=await UI.sheet({title:'开启日期',content:input,actions:[{label:'使用这个日期',value:'apply'}]});if(action==='apply'){if(!D.parse(input.value)){UI.fieldError(form.elements.opening,'请选择有效日期');return;}form.elements.opening.value=input.value;UI.fieldError(form.elements.opening,'');}} |
| m04-p13 | populated | m04-p13 | 开启提醒 | 可用 | 原生输入/选择器 |
| m04-p13 | populated | m04-p13 | 暂存草稿 | 可用 | ()=>save('draft',buttons[0]) |
| m04-p13 | populated | m04-p13 | 封存这份心意 | 可用 | 委托候选/待复核 |
| m04-p13 | populated | m04-p13 | 移除照片 | 隐藏/禁用 | ()=>{photo=null;file.value='';paint();} |
| m04-p14 | empty | m04-p14 | 返回胶囊列表 | 可用 | ()=>UI.back(page==='m04-p12'?'m04-p01.html':home) |
| m04-p14 | empty | m04-p14 | 把这一刻收录进重要时刻 | 隐藏/禁用 | 委托候选/待复核 |
| m04-p14 | empty | m04-p14 | 返回胶囊列表 | 可用 | ()=>UI.go(home,{force:true}) |
| m04-p14 | populated | m04-p14 | 返回胶囊列表 | 可用 | ()=>UI.back(page==='m04-p12'?'m04-p01.html':home) |
| m04-p14 | populated | m04-p14 | 把这一刻收录进重要时刻 | 可用 | ()=>UI.busy(document.querySelector('#collect'),'收录中…',()=>{if(UI.failNext('capsule-collect'))throw new Error('收录未完成，请重试');const values=UI.read('dujia-prototype-moments',[]),data=Array.isArray(values)?values:[],momentId=item.momentId／／'capsule-moment-'+item.id;let moment=data.find(v=>v.id===momentId);if(!moment){moment={id:momentId,name:item.name,date:D.today().iso,type:'纪念',story:item.message.slice(0,200),cover:item.photo,related:[],comments:[],capsuleId:item.id,createdAt:Date.now(),updatedAt:Date.now()};if(!UI.write('dujia-prototype-moments',[moment,...data]))return false;}if(!C.put({...item, |
| m04-p14 | populated | m04-p14 | 更多胶囊操作 | 可用 | async()=>{const action=await UI.sheet({title:'胶囊操作',actions:[{label:'删除胶囊',value:'delete',danger:true}]});if(action!=='delete'／／!await UI.modal({title:'删除这个胶囊？',message:'这份信件和照片会从本地胶囊架移除。',confirm:'确认删除',cancel:'取消'}))return;UI.busy(more,'删除中…',()=>{if(UI.failNext('capsule-delete'))throw new Error('删除未完成，请重试');if(!UI.write(C.key,C.all().filter(v=>v.id!==item.id)))return false;return UI.go(home,{force:true});});} |
| m04-p15 | empty | m04-p15 | 返回胶囊列表 | 可用 | ()=>UI.back(page==='m04-p12'?'m04-p01.html':home) |
| m04-p15 | empty | m04-p15 | 开启当天提醒我 | 隐藏/禁用 | 原生输入/选择器 |
| m04-p15 | empty | m04-p15 | 返回胶囊列表 | 可用 | ()=>UI.go(home,{force:true}) |
| m04-p15 | populated | m04-p15 | 返回胶囊列表 | 可用 | ()=>UI.back(page==='m04-p12'?'m04-p01.html':home) |
| m04-p15 | populated | m04-p15 | 开启当天提醒我 | 可用 | ()=>{const desired=reminder.checked;reminder.checked=item.reminder;UI.busy(reminder,'',()=>{if(UI.failNext('capsule-toggle'))throw new Error('提醒未更新，请重试');if(!C.put({...item,reminder:desired}))return false;item.reminder=desired;reminder.checked=desired;return true;});} |
| m04-p15 | populated | m04-p15 | 更多胶囊操作 | 可用 | async()=>{const action=await UI.sheet({title:'胶囊操作',actions:[{label:'删除胶囊',value:'delete',danger:true}]});if(action!=='delete'／／!await UI.modal({title:'删除这个胶囊？',message:'这份信件和照片会从本地胶囊架移除。',confirm:'确认删除',cancel:'取消'}))return;UI.busy(more,'删除中…',()=>{if(UI.failNext('capsule-delete'))throw new Error('删除未完成，请重试');if(!UI.write(C.key,C.all().filter(v=>v.id!==item.id)))return false;return UI.go(home,{force:true});});} |
| m04-p16 | empty | m04-p17 | 返回重要时刻 | 可用 | ()=>UI.back(page==='m04-p04'&&id&&find(id)?route(find(id)):home()) |
| m04-p16 | empty | m04-p17 | 去看看共同记录 | 可用 | ()=>UI.go('m03-p06.html') |
| m04-p16 | populated | m04-p17 | 返回重要时刻 | 可用 | ()=>UI.back(page==='m04-p04'&&id&&find(id)?route(find(id)):home()) |
| m04-p16 | populated | m04-p17 | 去看看共同记录 | 可用 | ()=>UI.go('m03-p06.html') |
| m04-p17 | empty | m04-p17 | 返回重要时刻 | 可用 | ()=>UI.back(page==='m04-p04'&&id&&find(id)?route(find(id)):home()) |
| m04-p17 | empty | m04-p17 | 去看看共同记录 | 可用 | ()=>UI.go('m03-p06.html') |
| m04-p17 | populated | m04-p17 | 返回重要时刻 | 可用 | ()=>UI.back(page==='m04-p04'&&id&&find(id)?route(find(id)):home()) |
| m04-p17 | populated | m04-p17 | 去看看共同记录 | 可用 | ()=>UI.go('m03-p06.html') |
| m05-p01 | empty | m05-p01 | 做成童话漫画 把回忆画成专属故事 留下一格格心动瞬间 | 可用 | ()=>UI.go(i?'m05-p05.html':'m05-p02.html') |
| m05-p01 | empty | m05-p01 | 制作回忆影片 让重要时刻动起来 在光影里重温感动 | 可用 | ()=>UI.go(i?'m05-p05.html':'m05-p02.html') |
| m05-p01 | empty | m05-p01 | 查看全部 › | 可用 | ()=>UI.go('m05-p09.html') |
| m05-p01 | empty | m05-p01 | 开始一次创作 | 可用 | ()=>UI.go('m05-p02.html') |
| m05-p01 | empty | m05-p01 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m05-p01 | empty | m05-p01 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m05-p01 | empty | m05-p01 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m05-p01 | empty | m05-p01 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m05-p01 | empty | m05-p01 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m05-p01 | populated | m05-p01 | 做成童话漫画 把回忆画成专属故事 留下一格格心动瞬间 | 可用 | ()=>UI.go(i?'m05-p05.html':'m05-p02.html') |
| m05-p01 | populated | m05-p01 | 制作回忆影片 让重要时刻动起来 在光影里重温感动 | 可用 | ()=>UI.go(i?'m05-p05.html':'m05-p02.html') |
| m05-p01 | populated | m05-p01 | 查看全部 › | 可用 | ()=>UI.go('m05-p09.html') |
| m05-p01 | populated | m05-p01 | 实际工坊作品 已完成 | 可用 | ()=>go(item) |
| m05-p01 | populated | m05-p01 | 开始一次创作 | 可用 | ()=>UI.go('m05-p02.html') |
| m05-p01 | populated | m05-p01 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m05-p01 | populated | m05-p01 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m05-p01 | populated | m05-p01 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m05-p01 | populated | m05-p01 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m05-p01 | populated | m05-p01 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m05-p02 | empty | m05-p02 | 返回童话工坊 | 可用 | ()=>UI.back(fallback) |
| m05-p02 | empty | m05-p02 | 共同日记 | 可用 | ()=>{kind=sourceKind;options.forEach(v=>v.setAttribute('aria-pressed',String(v===b)));} |
| m05-p02 | empty | m05-p02 | 相册照片 | 可用 | ()=>{kind=sourceKind;options.forEach(v=>v.setAttribute('aria-pressed',String(v===b)));} |
| m05-p02 | empty | m05-p02 | 重要时刻 | 可用 | ()=>{kind=sourceKind;options.forEach(v=>v.setAttribute('aria-pressed',String(v===b)));} |
| m05-p02 | empty | m05-p02 | 自由写一段回忆 | 可用 | ()=>{kind=sourceKind;options.forEach(v=>v.setAttribute('aria-pressed',String(v===b)));} |
| m05-p02 | empty | m05-p02 | 用这些素材开始 | 可用 | async()=>{const selected=kind==='free'?[]:await choose(kind,kind==='photo');if(selected===null)return;const item=W.draft('comic',kind,selected);if(W.put(item))UI.go(W.editor(item));} |
| m05-p02 | populated | m05-p02 | 返回童话工坊 | 可用 | ()=>UI.back(fallback) |
| m05-p02 | populated | m05-p02 | 共同日记 | 可用 | ()=>{kind=sourceKind;options.forEach(v=>v.setAttribute('aria-pressed',String(v===b)));} |
| m05-p02 | populated | m05-p02 | 相册照片 | 可用 | ()=>{kind=sourceKind;options.forEach(v=>v.setAttribute('aria-pressed',String(v===b)));} |
| m05-p02 | populated | m05-p02 | 重要时刻 | 可用 | ()=>{kind=sourceKind;options.forEach(v=>v.setAttribute('aria-pressed',String(v===b)));} |
| m05-p02 | populated | m05-p02 | 自由写一段回忆 | 可用 | ()=>{kind=sourceKind;options.forEach(v=>v.setAttribute('aria-pressed',String(v===b)));} |
| m05-p02 | populated | m05-p02 | 用这些素材开始 | 可用 | async()=>{const selected=kind==='free'?[]:await choose(kind,kind==='photo');if(selected===null)return;const item=W.draft('comic',kind,selected);if(W.put(item))UI.go(W.editor(item));} |
| m05-p03 | empty | m05-p03 | 返回素材选择 | 可用 | ()=>UI.back(fallback) |
| m05-p03 | empty | m05-p03 | 回忆内容 | 可用 | 原生输入/选择器 |
| m05-p03 | empty | m05-p03 | 编辑 | 可用 | ()=>input.focus() |
| m05-p03 | empty | m05-p03 | 暖暖水彩 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p03 | empty | m05-p03 | 复古漫画 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p03 | empty | m05-p03 | 轻柔铅笔 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p03 | empty | m05-p03 | 温柔叙事 贴近日常，细腻温暖 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p03 | empty | m05-p03 | 电影感 光影氛围，节奏张力 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p03 | empty | m05-p03 | 默默 & 小满 可爱自然 · 清新温柔 | 可用 | function characters(){if(!W.put(value()))return;leave.commit();UI.go('m05-p10.html?work='+encodeURIComponent(item.id),{force:true});} |
| m05-p03 | empty | m05-p03 | 生成童话漫画 | 可用 | ()=>{if(!input.value.trim()){UI.fieldError(input,'请写下这段回忆');input.focus();return;}if(page==='m05-p04'&&!sourceIds.length){UI.toast('请选择至少一张共同照片','error');return;}UI.busy(document.querySelector('#generate'),'提交中…',()=>{if(UI.failNext('work-save'))throw new Error('创作未保存，请重试');if(!W.start(value()))return false;leave.commit();return UI.go('m05-p06.html?id='+encodeURIComponent(item.id),{force:true});});} |
| m05-p03 | empty | m05-p03 | 暂存创作草稿 | 可用 | ()=>UI.busy(saveDraft,'保存中…',()=>{if(UI.failNext('work-save'))throw new Error('创作草稿未保存，请重试');if(!W.put(value()))return false;leave.commit();return UI.go('m05-p09.html',{force:true});}) |
| m05-p03 | empty | m05-p03 | 创作草稿操作 | 可用 | ()=>deleteWork(item) |
| m05-p03 | populated | m05-p03 | 返回素材选择 | 可用 | ()=>UI.back(fallback) |
| m05-p03 | populated | m05-p03 | 回忆内容 | 可用 | 原生输入/选择器 |
| m05-p03 | populated | m05-p03 | 编辑 | 可用 | ()=>input.focus() |
| m05-p03 | populated | m05-p03 | 暖暖水彩 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p03 | populated | m05-p03 | 复古漫画 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p03 | populated | m05-p03 | 轻柔铅笔 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p03 | populated | m05-p03 | 温柔叙事 贴近日常，细腻温暖 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p03 | populated | m05-p03 | 电影感 光影氛围，节奏张力 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p03 | populated | m05-p03 | 默默 & 小满 可爱自然 · 清新温柔 | 可用 | function characters(){if(!W.put(value()))return;leave.commit();UI.go('m05-p10.html?work='+encodeURIComponent(item.id),{force:true});} |
| m05-p03 | populated | m05-p03 | 生成童话漫画 | 可用 | ()=>{if(!input.value.trim()){UI.fieldError(input,'请写下这段回忆');input.focus();return;}if(page==='m05-p04'&&!sourceIds.length){UI.toast('请选择至少一张共同照片','error');return;}UI.busy(document.querySelector('#generate'),'提交中…',()=>{if(UI.failNext('work-save'))throw new Error('创作未保存，请重试');if(!W.start(value()))return false;leave.commit();return UI.go('m05-p06.html?id='+encodeURIComponent(item.id),{force:true});});} |
| m05-p03 | populated | m05-p03 | 暂存创作草稿 | 可用 | ()=>UI.busy(saveDraft,'保存中…',()=>{if(UI.failNext('work-save'))throw new Error('创作草稿未保存，请重试');if(!W.put(value()))return false;leave.commit();return UI.go('m05-p09.html',{force:true});}) |
| m05-p03 | populated | m05-p03 | 创作草稿操作 | 可用 | ()=>deleteWork(item) |
| m05-p04 | empty | m05-p04 | 返回素材选择 | 可用 | ()=>UI.back(fallback) |
| m05-p04 | empty | m05-p04 | 补充这段故事 | 可用 | 原生输入/选择器 |
| m05-p04 | empty | m05-p04 | 水彩 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p04 | empty | m05-p04 | 素描 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p04 | empty | m05-p04 | 清新插画 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p04 | empty | m05-p04 | 油画 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p04 | empty | m05-p04 | 他  阳光温柔 | 可用 | function characters(){if(!W.put(value()))return;leave.commit();UI.go('m05-p10.html?work='+encodeURIComponent(item.id),{force:true});} |
| m05-p04 | empty | m05-p04 | 她  温柔爱笑 | 可用 | function characters(){if(!W.put(value()))return;leave.commit();UI.go('m05-p10.html?work='+encodeURIComponent(item.id),{force:true});} |
| m05-p04 | empty | m05-p04 | 生成童话漫画 | 可用 | ()=>{if(!input.value.trim()){UI.fieldError(input,'请写下这段回忆');input.focus();return;}if(page==='m05-p04'&&!sourceIds.length){UI.toast('请选择至少一张共同照片','error');return;}UI.busy(document.querySelector('#generate'),'提交中…',()=>{if(UI.failNext('work-save'))throw new Error('创作未保存，请重试');if(!W.start(value()))return false;leave.commit();return UI.go('m05-p06.html?id='+encodeURIComponent(item.id),{force:true});});} |
| m05-p04 | empty | m05-p04 | 暂存创作草稿 | 可用 | ()=>UI.busy(saveDraft,'保存中…',()=>{if(UI.failNext('work-save'))throw new Error('创作草稿未保存，请重试');if(!W.put(value()))return false;leave.commit();return UI.go('m05-p09.html',{force:true});}) |
| m05-p04 | empty | m05-p04 | 创作草稿操作 | 可用 | ()=>deleteWork(item) |
| m05-p04 | empty | m05-p04 | 选择照片 | 可用 | async()=>{const data=await choose('photo',true,sourceIds);if(data){item.sourceIds=data.map(v=>v.id);sourceIds=[...item.sourceIds];paintPhotos();}} |
| m05-p04 | populated | m05-p03 | 返回素材选择 | 可用 | ()=>UI.back(fallback) |
| m05-p04 | populated | m05-p03 | 回忆内容 | 可用 | 原生输入/选择器 |
| m05-p04 | populated | m05-p03 | 编辑 | 可用 | ()=>input.focus() |
| m05-p04 | populated | m05-p03 | 暖暖水彩 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p04 | populated | m05-p03 | 复古漫画 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p04 | populated | m05-p03 | 轻柔铅笔 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p04 | populated | m05-p03 | 温柔叙事 贴近日常，细腻温暖 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p04 | populated | m05-p03 | 电影感 光影氛围，节奏张力 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p04 | populated | m05-p03 | 默默 & 小满 可爱自然 · 清新温柔 | 可用 | function characters(){if(!W.put(value()))return;leave.commit();UI.go('m05-p10.html?work='+encodeURIComponent(item.id),{force:true});} |
| m05-p04 | populated | m05-p03 | 生成童话漫画 | 可用 | ()=>{if(!input.value.trim()){UI.fieldError(input,'请写下这段回忆');input.focus();return;}if(page==='m05-p04'&&!sourceIds.length){UI.toast('请选择至少一张共同照片','error');return;}UI.busy(document.querySelector('#generate'),'提交中…',()=>{if(UI.failNext('work-save'))throw new Error('创作未保存，请重试');if(!W.start(value()))return false;leave.commit();return UI.go('m05-p06.html?id='+encodeURIComponent(item.id),{force:true});});} |
| m05-p04 | populated | m05-p03 | 暂存创作草稿 | 可用 | ()=>UI.busy(saveDraft,'保存中…',()=>{if(UI.failNext('work-save'))throw new Error('创作草稿未保存，请重试');if(!W.put(value()))return false;leave.commit();return UI.go('m05-p09.html',{force:true});}) |
| m05-p04 | populated | m05-p03 | 创作草稿操作 | 可用 | ()=>deleteWork(item) |
| m05-p05 | empty | m05-p05 | 返回工坊 | 可用 | ()=>UI.back(fallback) |
| m05-p05 | empty | m05-p05 | 选择共同片段 | 可用 | async()=>{const kinds=await UI.sheet({title:'片段类型',actions:[{label:'共同日记',value:'diary'},{label:'相册照片',value:'photo'},{label:'重要时刻',value:'moment'}]});if(!kinds)return;const data=await choose(kinds,true);if(data){item.sourceKind=kinds;sourceIds=data.map(v=>v.id);item.sourceIds=[...sourceIds];paintClips();}} |
| m05-p05 | empty | m05-p05 | 影片旁白 | 可用 | 原生输入/选择器 |
| m05-p05 | empty | m05-p05 | 试听演示音轨 | 可用 | async()=>{if(audio){await audio.close();audio=null;play.setAttribute('aria-label','试听演示音轨');return;}try{audio=new(window.AudioContext／／window.webkitAudioContext)();for(let i=0;i<6;i++){const osc=audio.createOscillator(),gain=audio.createGain();osc.frequency.value=[261,329,392,329,293,261][i];gain.gain.setValueAtTime(.04,audio.currentTime+i*.4);gain.gain.exponentialRampToValueAtTime(.001,audio.currentTime+i*.4+.35);osc.connect(gain);gain.connect(audio.destination);osc.start(audio.currentTime+i*.4);osc.stop(audio.currentTime+i*.4+.36);}play.setAttribute('aria-label','停止试听');setTimeout(async()=>{ |
| m05-p05 | empty | m05-p05 | 温柔手帐 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p05 | empty | m05-p05 | 治愈暖光 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p05 | empty | m05-p05 | 清新自然 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p05 | empty | m05-p05 | 生成回忆影片 | 可用 | ()=>{if(!input.value.trim()){UI.fieldError(input,'请写下这段回忆');input.focus();return;}if(page==='m05-p04'&&!sourceIds.length){UI.toast('请选择至少一张共同照片','error');return;}UI.busy(document.querySelector('#generate'),'提交中…',()=>{if(UI.failNext('work-save'))throw new Error('创作未保存，请重试');if(!W.start(value()))return false;leave.commit();return UI.go('m05-p06.html?id='+encodeURIComponent(item.id),{force:true});});} |
| m05-p05 | empty | m05-p05 | 暂存创作草稿 | 可用 | ()=>UI.busy(saveDraft,'保存中…',()=>{if(UI.failNext('work-save'))throw new Error('创作草稿未保存，请重试');if(!W.put(value()))return false;leave.commit();return UI.go('m05-p09.html',{force:true});}) |
| m05-p05 | empty | m05-p05 | 创作草稿操作 | 可用 | ()=>deleteWork(item) |
| m05-p05 | populated | m05-p03 | 返回素材选择 | 可用 | ()=>UI.back(fallback) |
| m05-p05 | populated | m05-p03 | 回忆内容 | 可用 | 原生输入/选择器 |
| m05-p05 | populated | m05-p03 | 编辑 | 可用 | ()=>input.focus() |
| m05-p05 | populated | m05-p03 | 暖暖水彩 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p05 | populated | m05-p03 | 复古漫画 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p05 | populated | m05-p03 | 轻柔铅笔 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p05 | populated | m05-p03 | 温柔叙事 贴近日常，细腻温暖 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p05 | populated | m05-p03 | 电影感 光影氛围，节奏张力 | 可用 | ()=>{const value=(b.querySelector('b')?.textContent／／b.childNodes[0]?.textContent／／b.textContent).trim();paint(value);change(value);} |
| m05-p05 | populated | m05-p03 | 默默 & 小满 可爱自然 · 清新温柔 | 可用 | function characters(){if(!W.put(value()))return;leave.commit();UI.go('m05-p10.html?work='+encodeURIComponent(item.id),{force:true});} |
| m05-p05 | populated | m05-p03 | 生成童话漫画 | 可用 | ()=>{if(!input.value.trim()){UI.fieldError(input,'请写下这段回忆');input.focus();return;}if(page==='m05-p04'&&!sourceIds.length){UI.toast('请选择至少一张共同照片','error');return;}UI.busy(document.querySelector('#generate'),'提交中…',()=>{if(UI.failNext('work-save'))throw new Error('创作未保存，请重试');if(!W.start(value()))return false;leave.commit();return UI.go('m05-p06.html?id='+encodeURIComponent(item.id),{force:true});});} |
| m05-p05 | populated | m05-p03 | 暂存创作草稿 | 可用 | ()=>UI.busy(saveDraft,'保存中…',()=>{if(UI.failNext('work-save'))throw new Error('创作草稿未保存，请重试');if(!W.put(value()))return false;leave.commit();return UI.go('m05-p09.html',{force:true});}) |
| m05-p05 | populated | m05-p03 | 创作草稿操作 | 可用 | ()=>deleteWork(item) |
| m05-p06 | empty | m05-p06 | 返回童话工坊 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p06 | empty | m05-p06 | 返回我的创作 | 可用 | ()=>UI.go('m05-p09.html',{force:true}) |
| m05-p06 | populated | m05-p08 | 返回我的创作 | 可用 | ()=>UI.back(fallback) |
| m05-p06 | populated | m05-p08 | 第1页 | 可用 | ()=>{current=i;paint();} |
| m05-p06 | populated | m05-p08 | 第2页 | 可用 | ()=>{current=i;paint();} |
| m05-p06 | populated | m05-p08 | 第3页 | 可用 | ()=>{current=i;paint();} |
| m05-p06 | populated | m05-p08 | 第4页 | 可用 | ()=>{current=i;paint();} |
| m05-p06 | populated | m05-p08 | 第5页 | 可用 | ()=>{current=i;paint();} |
| m05-p06 | populated | m05-p08 | 第6页 | 可用 | ()=>{current=i;paint();} |
| m05-p06 | populated | m05-p08 | 第7页 | 可用 | ()=>{current=i;paint();} |
| m05-p06 | populated | m05-p08 | 第8页 | 可用 | ()=>{current=i;paint();} |
| m05-p06 | populated | m05-p08 | 保存到共同相册 | 可用 | ()=>UI.busy(document.querySelector('#save'),'保存图片中…',async()=>{if(UI.failNext('work-album'))throw new Error('图片未保存，请重试');if(await W.album(item))UI.toast('已保存到共同相册','success');}) |
| m05-p06 | populated | m05-p08 | 给另一半看看 | 可用 | async()=>{const link=make('input');link.value=location.href;link.readOnly=true;link.setAttribute('aria-label','当前原型作品链接');const result=await UI.sheet({title:'给另一半看看',message:'此链接仅在同一台设备的本地原型数据中可查看。',content:link,actions:[{label:'复制作品链接',value:'copy'}]});if(result==='copy'){try{await navigator.clipboard.writeText(link.value);UI.toast('作品链接已复制','success');}catch{UI.modal({title:'复制作品链接',message:'请选中下方链接并复制。',content:link,confirm:'关闭'});link.select();}}} |
| m05-p06 | populated | m05-p08 | 重新生成 | 可用 | ()=>UI.go(W.editor(item)) |
| m05-p06 | populated | m05-p08 | 更多作品操作 | 可用 | ()=>deleteWork(item) |
| m05-p07 | empty | m05-p07 | 调整内容 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p07 | empty | m05-p07 | 重新生成 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p07 | empty | m05-p07 | 先回到童话工坊 ♡ | 隐藏/禁用 | 委托候选/待复核 |
| m05-p07 | empty | m05-p07 | 返回我的创作 | 可用 | ()=>UI.go('m05-p09.html',{force:true}) |
| m05-p07 | populated | m05-p08 | 返回我的创作 | 可用 | ()=>UI.back(fallback) |
| m05-p07 | populated | m05-p08 | 第1页 | 可用 | ()=>{current=i;paint();} |
| m05-p07 | populated | m05-p08 | 第2页 | 可用 | ()=>{current=i;paint();} |
| m05-p07 | populated | m05-p08 | 第3页 | 可用 | ()=>{current=i;paint();} |
| m05-p07 | populated | m05-p08 | 第4页 | 可用 | ()=>{current=i;paint();} |
| m05-p07 | populated | m05-p08 | 第5页 | 可用 | ()=>{current=i;paint();} |
| m05-p07 | populated | m05-p08 | 第6页 | 可用 | ()=>{current=i;paint();} |
| m05-p07 | populated | m05-p08 | 第7页 | 可用 | ()=>{current=i;paint();} |
| m05-p07 | populated | m05-p08 | 第8页 | 可用 | ()=>{current=i;paint();} |
| m05-p07 | populated | m05-p08 | 保存到共同相册 | 可用 | ()=>UI.busy(document.querySelector('#save'),'保存图片中…',async()=>{if(UI.failNext('work-album'))throw new Error('图片未保存，请重试');if(await W.album(item))UI.toast('已保存到共同相册','success');}) |
| m05-p07 | populated | m05-p08 | 给另一半看看 | 可用 | async()=>{const link=make('input');link.value=location.href;link.readOnly=true;link.setAttribute('aria-label','当前原型作品链接');const result=await UI.sheet({title:'给另一半看看',message:'此链接仅在同一台设备的本地原型数据中可查看。',content:link,actions:[{label:'复制作品链接',value:'copy'}]});if(result==='copy'){try{await navigator.clipboard.writeText(link.value);UI.toast('作品链接已复制','success');}catch{UI.modal({title:'复制作品链接',message:'请选中下方链接并复制。',content:link,confirm:'关闭'});link.select();}}} |
| m05-p07 | populated | m05-p08 | 重新生成 | 可用 | ()=>UI.go(W.editor(item)) |
| m05-p07 | populated | m05-p08 | 更多作品操作 | 可用 | ()=>deleteWork(item) |
| m05-p08 | empty | m05-p08 | 返回我的创作 | 可用 | ()=>UI.back('m05-p09.html') |
| m05-p08 | empty | m05-p08 | 第1页 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p08 | empty | m05-p08 | 第2页 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p08 | empty | m05-p08 | 第3页 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p08 | empty | m05-p08 | 第4页 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p08 | empty | m05-p08 | 第5页 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p08 | empty | m05-p08 | 第6页 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p08 | empty | m05-p08 | 第7页 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p08 | empty | m05-p08 | 第8页 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p08 | empty | m05-p08 | 保存到共同相册 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p08 | empty | m05-p08 | 给另一半看看 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p08 | empty | m05-p08 | 重新生成 | 隐藏/禁用 | 委托候选/待复核 |
| m05-p08 | empty | m05-p08 | 返回我的创作 | 可用 | ()=>UI.go('m05-p09.html',{force:true}) |
| m05-p08 | populated | m05-p08 | 返回我的创作 | 可用 | ()=>UI.back(fallback) |
| m05-p08 | populated | m05-p08 | 第1页 | 可用 | ()=>{current=i;paint();} |
| m05-p08 | populated | m05-p08 | 第2页 | 可用 | ()=>{current=i;paint();} |
| m05-p08 | populated | m05-p08 | 第3页 | 可用 | ()=>{current=i;paint();} |
| m05-p08 | populated | m05-p08 | 第4页 | 可用 | ()=>{current=i;paint();} |
| m05-p08 | populated | m05-p08 | 第5页 | 可用 | ()=>{current=i;paint();} |
| m05-p08 | populated | m05-p08 | 第6页 | 可用 | ()=>{current=i;paint();} |
| m05-p08 | populated | m05-p08 | 第7页 | 可用 | ()=>{current=i;paint();} |
| m05-p08 | populated | m05-p08 | 第8页 | 可用 | ()=>{current=i;paint();} |
| m05-p08 | populated | m05-p08 | 保存到共同相册 | 可用 | ()=>UI.busy(document.querySelector('#save'),'保存图片中…',async()=>{if(UI.failNext('work-album'))throw new Error('图片未保存，请重试');if(await W.album(item))UI.toast('已保存到共同相册','success');}) |
| m05-p08 | populated | m05-p08 | 给另一半看看 | 可用 | async()=>{const link=make('input');link.value=location.href;link.readOnly=true;link.setAttribute('aria-label','当前原型作品链接');const result=await UI.sheet({title:'给另一半看看',message:'此链接仅在同一台设备的本地原型数据中可查看。',content:link,actions:[{label:'复制作品链接',value:'copy'}]});if(result==='copy'){try{await navigator.clipboard.writeText(link.value);UI.toast('作品链接已复制','success');}catch{UI.modal({title:'复制作品链接',message:'请选中下方链接并复制。',content:link,confirm:'关闭'});link.select();}}} |
| m05-p08 | populated | m05-p08 | 重新生成 | 可用 | ()=>UI.go(W.editor(item)) |
| m05-p08 | populated | m05-p08 | 更多作品操作 | 可用 | ()=>deleteWork(item) |
| m05-p09 | empty | m05-p09 | 收藏夹 | 可用 | ()=>{favorites=!favorites;paint();} |
| m05-p09 | empty | m05-p09 | 全部 | 可用 | ()=>{tab=b.dataset.tab;paint();} |
| m05-p09 | empty | m05-p09 | 漫画 | 可用 | ()=>{tab=b.dataset.tab;paint();} |
| m05-p09 | empty | m05-p09 | 影片 | 可用 | ()=>{tab=b.dataset.tab;paint();} |
| m05-p09 | empty | m05-p09 | 草稿 | 可用 | ()=>{tab=b.dataset.tab;paint();} |
| m05-p09 | empty | m05-p09 | 开始创作 | 可用 | ()=>UI.go('m05-p02.html') |
| m05-p09 | empty | m05-p09 | 开始一次创作 | 可用 | ()=>{if(favorites){favorites=false;paint();}else UI.go('m05-p02.html');} |
| m05-p09 | empty | m05-p09 | 返回童话工坊 | 可用 | ()=>UI.back('m05-p01.html') |
| m05-p09 | empty | m05-p09 | 刷新我的创作 | 可用 | async function load(){if(loading)return;loading=true;refresh.disabled=true;list.setAttribute('aria-busy','true');list.textContent='正在翻开创作集…';await new Promise(resolve=>setTimeout(resolve,400));loading=false;refresh.disabled=false;list.removeAttribute('aria-busy');if(UI.failNext('work-load')){list.replaceChildren();const retry=make('button','重试加载创作');retry.onclick=load;list.append(make('p','创作集暂时打不开'),retry);}else paint();} |
| m05-p09 | populated | m05-p09 | 收藏夹 | 可用 | ()=>{favorites=!favorites;paint();} |
| m05-p09 | populated | m05-p09 | 全部 | 可用 | ()=>{tab=b.dataset.tab;paint();} |
| m05-p09 | populated | m05-p09 | 漫画 | 可用 | ()=>{tab=b.dataset.tab;paint();} |
| m05-p09 | populated | m05-p09 | 影片 | 可用 | ()=>{tab=b.dataset.tab;paint();} |
| m05-p09 | populated | m05-p09 | 草稿 | 可用 | ()=>{tab=b.dataset.tab;paint();} |
| m05-p09 | populated | m05-p09 | 开始创作 | 可用 | ()=>UI.go('m05-p02.html') |
| m05-p09 | populated | m05-p09 | 实际工坊作品 漫画 · 已完成 | 可用 | ()=>go(item) |
| m05-p09 | populated | m05-p09 | 返回童话工坊 | 可用 | ()=>UI.back('m05-p01.html') |
| m05-p09 | populated | m05-p09 | 刷新我的创作 | 可用 | async function load(){if(loading)return;loading=true;refresh.disabled=true;list.setAttribute('aria-busy','true');list.textContent='正在翻开创作集…';await new Promise(resolve=>setTimeout(resolve,400));loading=false;refresh.disabled=false;list.removeAttribute('aria-busy');if(UI.failNext('work-load')){list.replaceChildren();const retry=make('button','重试加载创作');retry.onclick=load;list.append(make('p','创作集暂时打不开'),retry);}else paint();} |
| m05-p10 | empty | m05-p10 | 返回童话工坊 | 可用 | ()=>UI.back(fallback) |
| m05-p10 | empty | m05-p10 | appearance | 可用 | 原生输入/选择器 |
| m05-p10 | empty | m05-p10 | outfit | 可用 | 原生输入/选择器 |
| m05-p10 | empty | m05-p10 | mood | 可用 | 原生输入/选择器 |
| m05-p10 | empty | m05-p10 | object | 可用 | 原生输入/选择器 |
| m05-p10 | empty | m05-p10 | 更新我们的主角 | 可用 | ()=>UI.busy(document.querySelector('#save'),'保存设定…',()=>{const empty=inputs.find(v=>!v.value.trim());if(empty){UI.fieldError(empty,'请填写这项主角设定');empty.focus();return false;}if(UI.failNext('work-characters'))throw new Error('主角设定未保存，请重试');if(!UI.write('dujia-characters',Object.fromEntries(inputs.map(v=>[v.id,v.value.trim()]))))return false;leave.commit();if(work)return UI.go(W.editor(work),{force:true});UI.toast('主角设定已更新','success');return true;}) |
| m05-p10 | populated | m05-p10 | 返回童话工坊 | 可用 | ()=>UI.back(fallback) |
| m05-p10 | populated | m05-p10 | appearance | 可用 | 原生输入/选择器 |
| m05-p10 | populated | m05-p10 | outfit | 可用 | 原生输入/选择器 |
| m05-p10 | populated | m05-p10 | mood | 可用 | 原生输入/选择器 |
| m05-p10 | populated | m05-p10 | object | 可用 | 原生输入/选择器 |
| m05-p10 | populated | m05-p10 | 更新我们的主角 | 可用 | ()=>UI.busy(document.querySelector('#save'),'保存设定…',()=>{const empty=inputs.find(v=>!v.value.trim());if(empty){UI.fieldError(empty,'请填写这项主角设定');empty.focus();return false;}if(UI.failNext('work-characters'))throw new Error('主角设定未保存，请重试');if(!UI.write('dujia-characters',Object.fromEntries(inputs.map(v=>[v.id,v.value.trim()]))))return false;leave.commit();if(work)return UI.go(W.editor(work),{force:true});UI.toast('主角设定已更新','success');return true;}) |
| m06-p01 | empty | m06-p01 | 小满 ♡ 尚未关联，邀请 TA 一起记录 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | empty | m06-p01 | 我们的小世界 一起管理共同资料 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | empty | m06-p01 | 草稿箱 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | empty | m06-p01 | 标签管理 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | empty | m06-p01 | 童话会员 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | empty | m06-p01 | 设置 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | empty | m06-p01 | 帮助与关于 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | empty | m06-p01 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m06-p01 | empty | m06-p01 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m06-p01 | empty | m06-p01 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m06-p01 | empty | m06-p01 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m06-p01 | empty | m06-p01 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m06-p01 | populated | m06-p01 | 小满 ♡ 已与阿舟关联 ♡ | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | populated | m06-p01 | 我们的小世界 一起管理共同资料 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | populated | m06-p01 | 草稿箱 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | populated | m06-p01 | 标签管理 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | populated | m06-p01 | 童话会员 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | populated | m06-p01 | 设置 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | populated | m06-p01 | 帮助与关于 | 可用 | ()=>UI.go(url+'.html') |
| m06-p01 | populated | m06-p01 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m06-p01 | populated | m06-p01 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m06-p01 | populated | m06-p01 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m06-p01 | populated | m06-p01 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m06-p01 | populated | m06-p01 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m06-p02 | empty | m06-p02 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p02 | empty | m06-p02 | 更换头像 | 可用 | async event=>{const file=event.target.files[0];if(!file)return;reading=true;try{avatar=await R.readImage(file,'settings-avatar');paint();}catch(error){UI.toast(error.message,'error');}finally{reading=false;event.target.value='';}} |
| m06-p02 | empty | m06-p02 | 更换头像 | 可用 | ()=>document.querySelector('#avatar').click() |
| m06-p02 | empty | m06-p02 | nickname | 可用 | 原生输入/选择器 |
| m06-p02 | empty | m06-p02 | birthday | 可用 | async()=>{const input=make('input');input.type='date';input.value=D.parse(birthday.value)?.iso／／'';input.max=D.today().iso;input.setAttribute('aria-label','选择生日');const action=await UI.sheet({title:'你的生日',content:input,actions:[{label:'使用这个生日',value:'apply'},{label:'不填写生日',value:'clear'}]});if(action==='clear')birthday.value='';if(action==='apply'){const date=D.parse(input.value);if(!date／／date.time>D.today().time){UI.fieldError(birthday,'请选择有效的过去日期');return;}birthday.value=date.iso;}} |
| m06-p02 | empty | m06-p02 | saying | 可用 | 原生输入/选择器 |
| m06-p02 | empty | m06-p02 | color | 可用 | 原生输入/选择器 |
| m06-p02 | empty | m06-p02 | 保存资料 | 可用 | ()=>{if(reading){UI.toast('头像正在读取，请稍候');return;}const nickname=document.querySelector('#nickname').value.trim();if(!nickname){UI.fieldError(document.querySelector('#nickname'),'请填写昵称');return;}UI.busy(document.querySelector('#save'),'保存中…',()=>{if(UI.failNext('settings-profile'))throw new Error('个人资料未保存，请重试');const next={...saved,...Object.fromEntries(fields.map(key=>[key,document.querySelector('#'+key).value.trim()])),avatar,aliases:[...new Set([...(Array.isArray(saved.aliases)?saved.aliases:[]),saved.nickname])],updatedAt:Date.now()};if(!UI.write('dujia-profile',next))return false;leave.comm |
| m06-p02 | populated | m06-p02 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p02 | populated | m06-p02 | 更换头像 | 可用 | async event=>{const file=event.target.files[0];if(!file)return;reading=true;try{avatar=await R.readImage(file,'settings-avatar');paint();}catch(error){UI.toast(error.message,'error');}finally{reading=false;event.target.value='';}} |
| m06-p02 | populated | m06-p02 | 更换头像 | 可用 | ()=>document.querySelector('#avatar').click() |
| m06-p02 | populated | m06-p02 | nickname | 可用 | 原生输入/选择器 |
| m06-p02 | populated | m06-p02 | birthday | 可用 | async()=>{const input=make('input');input.type='date';input.value=D.parse(birthday.value)?.iso／／'';input.max=D.today().iso;input.setAttribute('aria-label','选择生日');const action=await UI.sheet({title:'你的生日',content:input,actions:[{label:'使用这个生日',value:'apply'},{label:'不填写生日',value:'clear'}]});if(action==='clear')birthday.value='';if(action==='apply'){const date=D.parse(input.value);if(!date／／date.time>D.today().time){UI.fieldError(birthday,'请选择有效的过去日期');return;}birthday.value=date.iso;}} |
| m06-p02 | populated | m06-p02 | saying | 可用 | 原生输入/选择器 |
| m06-p02 | populated | m06-p02 | color | 可用 | 原生输入/选择器 |
| m06-p02 | populated | m06-p02 | 保存资料 | 可用 | ()=>{if(reading){UI.toast('头像正在读取，请稍候');return;}const nickname=document.querySelector('#nickname').value.trim();if(!nickname){UI.fieldError(document.querySelector('#nickname'),'请填写昵称');return;}UI.busy(document.querySelector('#save'),'保存中…',()=>{if(UI.failNext('settings-profile'))throw new Error('个人资料未保存，请重试');const next={...saved,...Object.fromEntries(fields.map(key=>[key,document.querySelector('#'+key).value.trim()])),avatar,aliases:[...new Set([...(Array.isArray(saved.aliases)?saved.aliases:[]),saved.nickname])],updatedAt:Date.now()};if(!UI.write('dujia-profile',next))return false;leave.comm |
| m06-p03 | empty | m06-p03 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p03 | empty | m06-p03 | 共同昵称 共同小屋 | 可用 | async()=>{if(!await manage())return;edit({title:'共同昵称',fields:[{key:'name',label:'共同昵称',value:value.profile?.nickname,max:40}],operation:'settings-world',save:inputs=>{const name=inputs.name.value.trim();if(!name){UI.fieldError(inputs.name,'请填写共同昵称');return false;}const next={...value,profile:{...value.profile,nickname:name}};if(!UI.write('dujia-prototype-relationship',next))return false;value=next;paint();return true;}});} |
| m06-p03 | empty | m06-p03 | 共同头像 | 可用 | async()=>{if(await manage())upload.click();} |
| m06-p03 | empty | m06-p03 | 共同空间设置 哪些记录邀请对方一起看 | 可用 | ()=>UI.go('m06-p09.html') |
| m06-p03 | empty | m06-p03 | 关联状态 | 可用 | ()=>UI.modal({title:'关联状态',message:value.bound?value.unlinkPending?'解除请求等待另一半确认。':'当前已与 '+value.partner+' 关联。':'当前未关联另一半。',confirm:'知道了'}) |
| m06-p03 | empty | m06-p03 | 解除关联 | 隐藏/禁用 | async()=>{if(!await UI.modal({title:'请求解除关联？',message:'等待另一半确认后解除，本机记录仍保留。',confirm:'请求解除关联',cancel:'取消'}))return;UI.busy(document.querySelector('.unlink'),'提交中…',()=>{if(UI.failNext('settings-unlink'))throw new Error('解除请求未提交，请重试');const next={...value,unlinkPending:{id:crypto.randomUUID(),createdAt:Date.now()}};if(!UI.write('dujia-prototype-relationship',next))return false;value=next;paint();return true;}).then(()=>paint());} |
| m06-p03 | empty | m06-p03 | INPUT | 隐藏/禁用 | async()=>{try{const avatar=await R.readImage(upload.files[0],'settings-world-avatar');const next={...value,profile:{...value.profile,avatar}};if(UI.write('dujia-prototype-relationship',next)){value=next;document.querySelector('.portrait').textContent='共同头像 · 已设置';UI.toast('共同头像已保存','success');}}catch(error){UI.toast(error.message,'error');}finally{upload.value='';}} |
| m06-p03 | populated | m06-p03 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p03 | populated | m06-p03 | 共同昵称 共同小屋 | 可用 | async()=>{if(!await manage())return;edit({title:'共同昵称',fields:[{key:'name',label:'共同昵称',value:value.profile?.nickname,max:40}],operation:'settings-world',save:inputs=>{const name=inputs.name.value.trim();if(!name){UI.fieldError(inputs.name,'请填写共同昵称');return false;}const next={...value,profile:{...value.profile,nickname:name}};if(!UI.write('dujia-prototype-relationship',next))return false;value=next;paint();return true;}});} |
| m06-p03 | populated | m06-p03 | 共同头像 | 可用 | async()=>{if(await manage())upload.click();} |
| m06-p03 | populated | m06-p03 | 共同空间设置 哪些记录邀请对方一起看 | 可用 | ()=>UI.go('m06-p09.html') |
| m06-p03 | populated | m06-p03 | 关联状态 | 可用 | ()=>UI.modal({title:'关联状态',message:value.bound?value.unlinkPending?'解除请求等待另一半确认。':'当前已与 '+value.partner+' 关联。':'当前未关联另一半。',confirm:'知道了'}) |
| m06-p03 | populated | m06-p03 | 解除关联 | 可用 | async()=>{if(!await UI.modal({title:'请求解除关联？',message:'等待另一半确认后解除，本机记录仍保留。',confirm:'请求解除关联',cancel:'取消'}))return;UI.busy(document.querySelector('.unlink'),'提交中…',()=>{if(UI.failNext('settings-unlink'))throw new Error('解除请求未提交，请重试');const next={...value,unlinkPending:{id:crypto.randomUUID(),createdAt:Date.now()}};if(!UI.write('dujia-prototype-relationship',next))return false;value=next;paint();return true;}).then(()=>paint());} |
| m06-p03 | populated | m06-p03 | INPUT | 隐藏/禁用 | async()=>{try{const avatar=await R.readImage(upload.files[0],'settings-world-avatar');const next={...value,profile:{...value.profile,avatar}};if(UI.write('dujia-prototype-relationship',next)){value=next;document.querySelector('.portrait').textContent='共同头像 · 已设置';UI.toast('共同头像已保存','success');}}catch(error){UI.toast(error.message,'error');}finally{upload.value='';}} |
| m06-p04 | empty | m06-p04 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p04 | empty | m06-p04 | 写第一篇日记 | 可用 | ()=>UI.go('m03-p05.html') |
| m06-p04 | empty | m06-p04 | 刷新草稿箱 | 可用 | async function load(){if(loading)return;loading=true;refresh.disabled=true;list.setAttribute('aria-busy','true');list.textContent='正在收拾草稿箱…';await new Promise(r=>setTimeout(r,400));loading=false;refresh.disabled=false;list.removeAttribute('aria-busy');if(UI.failNext('settings-drafts-load')){const retry=make('button','重试加载草稿');retry.onclick=load;list.replaceChildren(make('p','草稿箱暂时打不开'),retry);}else paint();} |
| m06-p04 | populated | m06-p04 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p04 | populated | m06-p04 | 写第一篇日记 | 可用 | ()=>UI.go('m03-p05.html') |
| m06-p04 | populated | m06-p04 | 刷新草稿箱 | 可用 | async function load(){if(loading)return;loading=true;refresh.disabled=true;list.setAttribute('aria-busy','true');list.textContent='正在收拾草稿箱…';await new Promise(r=>setTimeout(r,400));loading=false;refresh.disabled=false;list.removeAttribute('aria-busy');if(UI.failNext('settings-drafts-load')){const retry=make('button','重试加载草稿');retry.onclick=load;list.replaceChildren(make('p','草稿箱暂时打不开'),retry);}else paint();} |
| m06-p05 | empty | m06-p05 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p05 | empty | m06-p05 | 新建标签 | 可用 | ()=>editTag() |
| m06-p05 | empty | m06-p05 | 新建标签 | 可用 | ()=>editTag() |
| m06-p05 | empty | m06-p05 | 日常 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | empty | m06-p05 | 旅行 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | empty | m06-p05 | 想念 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | empty | m06-p05 | 美食 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | empty | m06-p05 | 春日野餐 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | empty | m06-p05 | 第一次旅行 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | empty | m06-p05 | 我们的家 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | populated | m06-p05 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p05 | populated | m06-p05 | 新建标签 | 可用 | ()=>editTag() |
| m06-p05 | populated | m06-p05 | 新建标签 | 可用 | ()=>editTag() |
| m06-p05 | populated | m06-p05 | 日常 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | populated | m06-p05 | 旅行 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | populated | m06-p05 | 想念 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | populated | m06-p05 | 美食 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | populated | m06-p05 | 春日野餐 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | populated | m06-p05 | 第一次旅行 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p05 | populated | m06-p05 | 我们的家 | 可用 | async()=>{const action=await UI.sheet({title:item.name,actions:[{label:'编辑标签',value:'edit'},{label:'删除标签',value:'delete',danger:true}]});if(action==='edit')editTag(item);if(action==='delete'&&await UI.modal({title:'删除这个标签？',message:'会移除记录中的标签文字，记录本身仍保留。',confirm:'确认删除',cancel:'取消'})){if(UI.failNext('settings-tag')){UI.toast('标签没有删除，请重试','error');return;}if(P.tagUpdate(item,true))paint();}} |
| m06-p06 | empty | m06-p06 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p06 | empty | m06-p06 | 开通童话会员 | 可用 | async()=>{if(!await UI.modal({title:'开通演示会员？',message:'仅演示开通状态，不收费、不自动续费，也不改变浏览器容量。',confirm:'开通演示会员',cancel:'取消'}))return;UI.busy(document.querySelector('.open'),'开通中…',()=>{if(UI.failNext('settings-member'))throw new Error('演示会员未开通，请重试');if(!UI.write('dujia-prototype-membership',{expiresAt:Date.now()+30*86400000,createdAt:Date.now()}))return false;paint();return true;}).then(paint);} |
| m06-p06 | empty | m06-p06 | 查看会员说明 › | 可用 | ()=>UI.modal({title:'童话会员说明',message:'设计方案包含更多胶囊、更大照片空间及专属装扮。本地原型仅演示开通流程，权益配额待正式服务实现。'}) |
| m06-p06 | populated | m06-p06 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p06 | populated | m06-p06 | 开通童话会员 | 可用 | async()=>{if(!await UI.modal({title:'开通演示会员？',message:'仅演示开通状态，不收费、不自动续费，也不改变浏览器容量。',confirm:'开通演示会员',cancel:'取消'}))return;UI.busy(document.querySelector('.open'),'开通中…',()=>{if(UI.failNext('settings-member'))throw new Error('演示会员未开通，请重试');if(!UI.write('dujia-prototype-membership',{expiresAt:Date.now()+30*86400000,createdAt:Date.now()}))return false;paint();return true;}).then(paint);} |
| m06-p06 | populated | m06-p06 | 查看会员说明 › | 可用 | ()=>UI.modal({title:'童话会员说明',message:'设计方案包含更多胶囊、更大照片空间及专属装扮。本地原型仅演示开通流程，权益配额待正式服务实现。'}) |
| m06-p07 | empty | m06-p07 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p07 | empty | m06-p07 | 账号与安全 | 可用 | ()=>UI.go(url+'.html') |
| m06-p07 | empty | m06-p07 | 隐私与共同可见 | 可用 | ()=>UI.go(url+'.html') |
| m06-p07 | empty | m06-p07 | 通知设置 | 可用 | ()=>UI.go(url+'.html') |
| m06-p07 | empty | m06-p07 | 数据与存储 | 可用 | ()=>UI.go(url+'.html') |
| m06-p07 | empty | m06-p07 | 显示与外观 | 可用 | ()=>edit({title:'显示与外观',fields:[{key:'motion',label:'动效',type:'select',value:P.preferences().reduceMotion?'reduce':'normal',options:[['normal','跟随原稿'],['reduce','减少动态效果']]}],save:inputs=>{if(!UI.write('dujia-prototype-preferences',{...P.preferences(),reduceMotion:inputs.motion.value==='reduce'}))return false;document.documentElement.dataset.prototypeReduceMotion=String(inputs.motion.value==='reduce');return true;}}) |
| m06-p07 | empty | m06-p07 | 语言 | 可用 | async()=>{const action=await UI.sheet({title:'语言',actions:[{label:'简体中文',value:'zh-CN'},{label:'English · 尚无译稿',value:'en',disabled:true}]});if(action&&UI.write('dujia-prototype-preferences',{...P.preferences(),language:action}))UI.toast('已使用简体中文','success');} |
| m06-p07 | empty | m06-p07 | 退出登录 | 可用 | ()=>logout(document.querySelector('.logout')) |
| m06-p07 | populated | m06-p07 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p07 | populated | m06-p07 | 账号与安全 | 可用 | ()=>UI.go(url+'.html') |
| m06-p07 | populated | m06-p07 | 隐私与共同可见 | 可用 | ()=>UI.go(url+'.html') |
| m06-p07 | populated | m06-p07 | 通知设置 | 可用 | ()=>UI.go(url+'.html') |
| m06-p07 | populated | m06-p07 | 数据与存储 | 可用 | ()=>UI.go(url+'.html') |
| m06-p07 | populated | m06-p07 | 显示与外观 | 可用 | ()=>edit({title:'显示与外观',fields:[{key:'motion',label:'动效',type:'select',value:P.preferences().reduceMotion?'reduce':'normal',options:[['normal','跟随原稿'],['reduce','减少动态效果']]}],save:inputs=>{if(!UI.write('dujia-prototype-preferences',{...P.preferences(),reduceMotion:inputs.motion.value==='reduce'}))return false;document.documentElement.dataset.prototypeReduceMotion=String(inputs.motion.value==='reduce');return true;}}) |
| m06-p07 | populated | m06-p07 | 语言 | 可用 | async()=>{const action=await UI.sheet({title:'语言',actions:[{label:'简体中文',value:'zh-CN'},{label:'English · 尚无译稿',value:'en',disabled:true}]});if(action&&UI.write('dujia-prototype-preferences',{...P.preferences(),language:action}))UI.toast('已使用简体中文','success');} |
| m06-p07 | populated | m06-p07 | 退出登录 | 可用 | ()=>logout(document.querySelector('.logout')) |
| m06-p08 | empty | m06-p08 | 返回设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p08 | empty | m06-p08 | 修改密码 | 可用 | ()=>UI.go('m01-p04.html') |
| m06-p08 | empty | m06-p08 | 绑定手机 | 可用 | ()=>edit({title:'绑定手机（本地演示）',fields:[{key:'phone',label:'手机号',value:session().phone,max:11},{key:'code',label:'演示验证码 284631',max:6}],operation:'settings-phone',save:inputs=>{if(!/^1\d{10}$/.test(inputs.phone.value)){UI.fieldError(inputs.phone,'请输入11位手机号');return false;}if(inputs.code.value!=='284631'){UI.fieldError(inputs.code,'验证码不正确');return false;}if(!UI.write('dujia-prototype-session',{...session(),phone:inputs.phone.value}))return false;document.querySelector('.account').textContent=inputs.phone.value.replace(/(\d{3})\d{4}(\d{4})/,'$1****$2');return true;}}) |
| m06-p08 | empty | m06-p08 | 登录设备 当前设备安全 | 可用 | ()=>UI.modal({title:'登录设备',message:'当前设备：本机浏览器\n会话状态：'+(session().loggedIn?'已登录演示账号':'未登录')+'\n本地原型没有其他设备的会话数据。'}) |
| m06-p08 | empty | m06-p08 | 两步验证 · 未开启 | 可用 | ()=>edit({title:P.preferences().twoFactor?'关闭两步验证演示':'开启两步验证演示',fields:[{key:'code',label:'演示验证码 284631',max:6}],operation:'settings-two-factor',save:inputs=>{if(inputs.code.value!=='284631'){UI.fieldError(inputs.code,'验证码不正确');return false;}if(!UI.write('dujia-prototype-preferences',{...P.preferences(),twoFactor:!P.preferences().twoFactor}))return false;paintTwoFactor();return true;}}) |
| m06-p08 | empty | m06-p08 | 退出登录 | 可用 | ()=>logout(document.querySelector('.logout')) |
| m06-p08 | empty | m06-p08 | 注销账号 | 可用 | async()=>{if(!await UI.modal({title:'注销本地演示账号？',message:'会移除本机原型资料、记录和关联。可先到数据与存储导出。',confirm:'继续身份确认',cancel:'取消'}))return;edit({title:'确认注销演示账号',fields:[{key:'code',label:'演示验证码 284631',max:6}],submit:'注销演示账号',save:inputs=>{if(inputs.code.value!=='284631'){UI.fieldError(inputs.code,'验证码不正确');return false;}return Promise.resolve(P.deleteAccount()).then(()=>'navigated');}});} |
| m06-p08 | populated | m06-p08 | 返回设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p08 | populated | m06-p08 | 修改密码 | 可用 | ()=>UI.go('m01-p04.html') |
| m06-p08 | populated | m06-p08 | 绑定手机 | 可用 | ()=>edit({title:'绑定手机（本地演示）',fields:[{key:'phone',label:'手机号',value:session().phone,max:11},{key:'code',label:'演示验证码 284631',max:6}],operation:'settings-phone',save:inputs=>{if(!/^1\d{10}$/.test(inputs.phone.value)){UI.fieldError(inputs.phone,'请输入11位手机号');return false;}if(inputs.code.value!=='284631'){UI.fieldError(inputs.code,'验证码不正确');return false;}if(!UI.write('dujia-prototype-session',{...session(),phone:inputs.phone.value}))return false;document.querySelector('.account').textContent=inputs.phone.value.replace(/(\d{3})\d{4}(\d{4})/,'$1****$2');return true;}}) |
| m06-p08 | populated | m06-p08 | 登录设备 当前设备安全 | 可用 | ()=>UI.modal({title:'登录设备',message:'当前设备：本机浏览器\n会话状态：'+(session().loggedIn?'已登录演示账号':'未登录')+'\n本地原型没有其他设备的会话数据。'}) |
| m06-p08 | populated | m06-p08 | 两步验证 · 未开启 | 可用 | ()=>edit({title:P.preferences().twoFactor?'关闭两步验证演示':'开启两步验证演示',fields:[{key:'code',label:'演示验证码 284631',max:6}],operation:'settings-two-factor',save:inputs=>{if(inputs.code.value!=='284631'){UI.fieldError(inputs.code,'验证码不正确');return false;}if(!UI.write('dujia-prototype-preferences',{...P.preferences(),twoFactor:!P.preferences().twoFactor}))return false;paintTwoFactor();return true;}}) |
| m06-p08 | populated | m06-p08 | 退出登录 | 可用 | ()=>logout(document.querySelector('.logout')) |
| m06-p08 | populated | m06-p08 | 注销账号 | 可用 | async()=>{if(!await UI.modal({title:'注销本地演示账号？',message:'会移除本机原型资料、记录和关联。可先到数据与存储导出。',confirm:'继续身份确认',cancel:'取消'}))return;edit({title:'确认注销演示账号',fields:[{key:'code',label:'演示验证码 284631',max:6}],submit:'注销演示账号',save:inputs=>{if(inputs.code.value!=='284631'){UI.fieldError(inputs.code,'验证码不正确');return false;}return Promise.resolve(P.deleteAccount()).then(()=>'navigated');}});} |
| m06-p09 | empty | m06-p09 | 返回设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p09 | empty | m06-p09 | 默认可见范围 共同可见 | 可用 | async()=>{const action=await UI.sheet({title:'新记录默认可见范围',actions:[{label:'仅自己可见',value:'仅自己可见'},{label:'共同可见',value:'共同可见',disabled:!settings.shared}]});if(action&&UI.write(key,{...settings,scope:action})){settings={...settings,scope:action};paint();}} |
| m06-p09 | empty | m06-p09 | 共同可见 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p09 | empty | m06-p09 | 共同空间 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p09 | empty | m06-p09 | 另一半回应 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p09 | empty | m06-p09 | 相关提醒 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p09 | populated | m06-p09 | 返回设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p09 | populated | m06-p09 | 默认可见范围 共同可见 | 可用 | async()=>{const action=await UI.sheet({title:'新记录默认可见范围',actions:[{label:'仅自己可见',value:'仅自己可见'},{label:'共同可见',value:'共同可见',disabled:!settings.shared}]});if(action&&UI.write(key,{...settings,scope:action})){settings={...settings,scope:action};paint();}} |
| m06-p09 | populated | m06-p09 | 共同可见 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p09 | populated | m06-p09 | 共同空间 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p09 | populated | m06-p09 | 另一半回应 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p09 | populated | m06-p09 | 相关提醒 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p10 | empty | m06-p10 | 返回设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p10 | empty | m06-p10 | 另一半回应 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p10 | empty | m06-p10 | 重要时刻 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p10 | empty | m06-p10 | 时光胶囊 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p10 | empty | m06-p10 | 工坊完成 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p10 | empty | m06-p10 | 通知总开关 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p10 | populated | m06-p10 | 返回设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p10 | populated | m06-p10 | 另一半回应 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p10 | populated | m06-p10 | 重要时刻 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p10 | populated | m06-p10 | 时光胶囊 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p10 | populated | m06-p10 | 工坊完成 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p10 | populated | m06-p10 | 通知总开关 | 可用 | ()=>UI.busy(button,'更新中…',()=>{if(UI.failNext('settings-preference'))throw new Error('设置未更新，请重试');const next={...settings,[button.dataset.key]:!settings[button.dataset.key]};if(privacyPage&&button.dataset.key==='shared'&&!next.shared)next.scope='仅自己可见';if(!UI.write(key,next))return false;settings=next;paint();return true;}).then(paint) |
| m06-p11 | empty | m06-p11 | 返回设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p11 | empty | m06-p11 | 导出我的记录 | 可用 | ()=>UI.busy(document.querySelector('#export'),'整理记录…',()=>{if(UI.failNext('settings-export'))throw new Error('导出未完成，请重试');const url=URL.createObjectURL(new Blob([JSON.stringify(P.snapshot(),null,2)],{type:'application/json'})),link=make('a');link.href=url;link.download='dujia-records.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);UI.toast('记录已准备下载','success');return true;}) |
| m06-p11 | empty | m06-p11 | 共同记录备份 | 可用 | ()=>UI.busy(document.querySelector('#backup'),'备份中…',()=>{if(UI.failNext('settings-backup'))throw new Error('备份未完成，请重试');if(P.backup()){UI.toast('共同记录备份已创建','success');paint();return true;}return false;}) |
| m06-p11 | empty | m06-p11 | 自动备份 | 可用 | ()=>{const next={...P.preferences(),autoBackup:!P.preferences().autoBackup};if(UI.write('dujia-prototype-preferences',next))paint();} |
| m06-p11 | empty | m06-p11 | 存储空间管理 | 可用 | async()=>{const action=await UI.modal({title:'本地存储空间',message:'当前演示数据约 '+format(P.bytes())+'。容量由浏览器决定。\n可以先导出记录，再整理不需要的内容；缓存清理不会删除记录或恢复副本。',cancel:'关闭',actions:[{label:'查看恢复原始副本',value:'archives'}]});if(action==='archives')await R.showArchives();} |
| m06-p11 | empty | m06-p11 | 清理缓存 0.0 KB | 可用 | async()=>{if(!await UI.modal({title:'清理浏览记录缓存？',message:'仅清理搜索历史与列表筛选，不删除记录、图片或草稿。',confirm:'确认清理',cancel:'取消'}))return;P.clearCache();paint();UI.toast('浏览记录缓存已清理','success');} |
| m06-p11 | populated | m06-p11 | 返回设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p11 | populated | m06-p11 | 导出我的记录 | 可用 | ()=>UI.busy(document.querySelector('#export'),'整理记录…',()=>{if(UI.failNext('settings-export'))throw new Error('导出未完成，请重试');const url=URL.createObjectURL(new Blob([JSON.stringify(P.snapshot(),null,2)],{type:'application/json'})),link=make('a');link.href=url;link.download='dujia-records.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);UI.toast('记录已准备下载','success');return true;}) |
| m06-p11 | populated | m06-p11 | 共同记录备份 | 可用 | ()=>UI.busy(document.querySelector('#backup'),'备份中…',()=>{if(UI.failNext('settings-backup'))throw new Error('备份未完成，请重试');if(P.backup()){UI.toast('共同记录备份已创建','success');paint();return true;}return false;}) |
| m06-p11 | populated | m06-p11 | 自动备份 | 可用 | ()=>{const next={...P.preferences(),autoBackup:!P.preferences().autoBackup};if(UI.write('dujia-prototype-preferences',next))paint();} |
| m06-p11 | populated | m06-p11 | 存储空间管理 | 可用 | async()=>{const action=await UI.modal({title:'本地存储空间',message:'当前演示数据约 '+format(P.bytes())+'。容量由浏览器决定。\n可以先导出记录，再整理不需要的内容；缓存清理不会删除记录或恢复副本。',cancel:'关闭',actions:[{label:'查看恢复原始副本',value:'archives'}]});if(action==='archives')await R.showArchives();} |
| m06-p11 | populated | m06-p11 | 清理缓存 0.0 KB | 可用 | async()=>{if(!await UI.modal({title:'清理浏览记录缓存？',message:'仅清理搜索历史与列表筛选，不删除记录、图片或草稿。',confirm:'确认清理',cancel:'取消'}))return;P.clearCache();paint();UI.toast('浏览记录缓存已清理','success');} |
| m06-p12 | empty | m06-p12 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p12 | empty | m06-p12 | 使用帮助 | 可用 | ()=>UI.modal({title:'使用帮助',message:'首页可写日记和添加照片；时刻册可关联记录、设置纪念日或封存胶囊；工坊可用共同素材创作。\n未完成内容可暂存，在草稿箱继续；数据与存储可以导出本机记录。'}) |
| m06-p12 | empty | m06-p12 | 意见反馈 | 可用 | ()=>edit({title:'意见反馈',fields:[{key:'text',label:'意见反馈',type:'textarea',max:1000,value:UI.read('dujia-feedback-draft','')}],submit:'保存反馈',operation:'settings-feedback',save:inputs=>{const text=inputs.text.value.trim();if(!text){UI.fieldError(inputs.text,'请写下反馈内容');return false;}if(!UI.write('dujia-feedback-draft',text))return false;UI.toast('反馈已保存在本机','success');return true;}}) |
| m06-p12 | empty | m06-p12 | 隐私政策 | 可用 | ()=>UI.modal({title:button.textContent,message:'这是本地交互原型，演示数据保存在本机。正式协议和隐私政策正文需由项目提供；此页用于验证阅读与关闭交互。'}) |
| m06-p12 | empty | m06-p12 | 用户协议 | 可用 | ()=>UI.modal({title:button.textContent,message:'这是本地交互原型，演示数据保存在本机。正式协议和隐私政策正文需由项目提供；此页用于验证阅读与关闭交互。'}) |
| m06-p12 | empty | m06-p12 | 检查更新 | 可用 | ()=>UI.busy(document.querySelector('.updates'),'检查中…',()=>{if(UI.failNext('settings-update'))throw new Error('版本信息暂时打不开，请重试');UI.modal({title:'版本信息',message:'当前本地原型版本 1.0.0。未连接版本服务，无法确认是否有正式版本更新。'});return true;}) |
| m06-p12 | empty | m06-p12 | 关于独家童话 | 可用 | ()=>UI.modal({title:'关于独家童话',message:'独家童话 1.0.0\n把平凡的日子写成童话。\n当前为本地交互原型。'}) |
| m06-p12 | populated | m06-p12 | 返回我的与设置 | 可用 | ()=>UI.back(['m06-p08','m06-p09','m06-p10','m06-p11'].includes(page)?'m06-p07.html':'m06-p01.html') |
| m06-p12 | populated | m06-p12 | 使用帮助 | 可用 | ()=>UI.modal({title:'使用帮助',message:'首页可写日记和添加照片；时刻册可关联记录、设置纪念日或封存胶囊；工坊可用共同素材创作。\n未完成内容可暂存，在草稿箱继续；数据与存储可以导出本机记录。'}) |
| m06-p12 | populated | m06-p12 | 意见反馈 | 可用 | ()=>edit({title:'意见反馈',fields:[{key:'text',label:'意见反馈',type:'textarea',max:1000,value:UI.read('dujia-feedback-draft','')}],submit:'保存反馈',operation:'settings-feedback',save:inputs=>{const text=inputs.text.value.trim();if(!text){UI.fieldError(inputs.text,'请写下反馈内容');return false;}if(!UI.write('dujia-feedback-draft',text))return false;UI.toast('反馈已保存在本机','success');return true;}}) |
| m06-p12 | populated | m06-p12 | 隐私政策 | 可用 | ()=>UI.modal({title:button.textContent,message:'这是本地交互原型，演示数据保存在本机。正式协议和隐私政策正文需由项目提供；此页用于验证阅读与关闭交互。'}) |
| m06-p12 | populated | m06-p12 | 用户协议 | 可用 | ()=>UI.modal({title:button.textContent,message:'这是本地交互原型，演示数据保存在本机。正式协议和隐私政策正文需由项目提供；此页用于验证阅读与关闭交互。'}) |
| m06-p12 | populated | m06-p12 | 检查更新 | 可用 | ()=>UI.busy(document.querySelector('.updates'),'检查中…',()=>{if(UI.failNext('settings-update'))throw new Error('版本信息暂时打不开，请重试');UI.modal({title:'版本信息',message:'当前本地原型版本 1.0.0。未连接版本服务，无法确认是否有正式版本更新。'});return true;}) |
| m06-p12 | populated | m06-p12 | 关于独家童话 | 可用 | ()=>UI.modal({title:'关于独家童话',message:'独家童话 1.0.0\n把平凡的日子写成童话。\n当前为本地交互原型。'}) |
| m07-p01 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p01 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p01 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p01 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p01 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p01 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p01 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p01 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p01 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p01 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p01 | populated | m07-p03 | 互动 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p01 | populated | m07-p03 | 喂食 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p01 | populated | m07-p03 | 任务 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p01 | populated | m07-p03 | 装扮 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p01 | populated | m07-p03 | 布置小屋 | 可用 | ()=>go([15,18,21][i]) |
| m07-p01 | populated | m07-p03 | 成长故事 | 可用 | ()=>go([15,18,21][i]) |
| m07-p01 | populated | m07-p03 | 成就图鉴 | 可用 | ()=>go([15,18,21][i]) |
| m07-p01 | populated | m07-p03 | 去任务 › | 可用 | ()=>go(11) |
| m07-p01 | populated | m07-p03 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p01 | populated | m07-p03 | 宠物设置 | 可用 | ()=>go(25) |
| m07-p01 | populated | m07-p03 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p01 | populated | m07-p03 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p01 | populated | m07-p03 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p01 | populated | m07-p03 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p01 | populated | m07-p03 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p02 | empty | m07-p02 | 小狗 | 可用 | ()=>{kind=b.dataset.kind;all('.pet').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p02 | empty | m07-p02 | 小猫 | 可用 | ()=>{kind=b.dataset.kind;all('.pet').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p02 | empty | m07-p02 | 小兔 | 可用 | ()=>{kind=b.dataset.kind;all('.pet').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p02 | empty | m07-p02 | 小狐狸 | 可用 | ()=>{kind=b.dataset.kind;all('.pet').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p02 | empty | m07-p02 | pet-name | 可用 | 原生输入/选择器 |
| m07-p02 | empty | m07-p02 | 邀请 TA 一起领养 | 可用 | ()=>{if(!validate()){input.focus();return;}if(!UI.read('dujia-prototype-relationship',{})?.bound){UI.modal({title:'先关联另一半',message:'共同领养需要双方确认。请先完成关系关联。',confirm:'去关联',cancel:'继续选择'}).then(ok=>ok&&UI.go('m02-p01.html'));return;}UI.busy(q('#invite'),'邀请保存中…',async()=>{if(!Pet.adopt(kind,input.value.trim()))return false;guard.commit();return go(1);});} |
| m07-p02 | empty | m07-p02 | 返回 | 可用 | ()=>UI.back('m07-p'+String(fallback).padStart(2,'0')+'.html') |
| m07-p02 | populated | m07-p03 | 互动 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p02 | populated | m07-p03 | 喂食 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p02 | populated | m07-p03 | 任务 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p02 | populated | m07-p03 | 装扮 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p02 | populated | m07-p03 | 布置小屋 | 可用 | ()=>go([15,18,21][i]) |
| m07-p02 | populated | m07-p03 | 成长故事 | 可用 | ()=>go([15,18,21][i]) |
| m07-p02 | populated | m07-p03 | 成就图鉴 | 可用 | ()=>go([15,18,21][i]) |
| m07-p02 | populated | m07-p03 | 去任务 › | 可用 | ()=>go(11) |
| m07-p02 | populated | m07-p03 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p02 | populated | m07-p03 | 宠物设置 | 可用 | ()=>go(25) |
| m07-p02 | populated | m07-p03 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p02 | populated | m07-p03 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p02 | populated | m07-p03 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p02 | populated | m07-p03 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p02 | populated | m07-p03 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p03 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p03 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p03 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p03 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p03 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p03 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p03 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p03 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p03 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p03 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p03 | populated | m07-p03 | 互动 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p03 | populated | m07-p03 | 喂食 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p03 | populated | m07-p03 | 任务 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p03 | populated | m07-p03 | 装扮 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p03 | populated | m07-p03 | 布置小屋 | 可用 | ()=>go([15,18,21][i]) |
| m07-p03 | populated | m07-p03 | 成长故事 | 可用 | ()=>go([15,18,21][i]) |
| m07-p03 | populated | m07-p03 | 成就图鉴 | 可用 | ()=>go([15,18,21][i]) |
| m07-p03 | populated | m07-p03 | 去任务 › | 可用 | ()=>go(11) |
| m07-p03 | populated | m07-p03 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p03 | populated | m07-p03 | 宠物设置 | 可用 | ()=>go(25) |
| m07-p03 | populated | m07-p03 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p03 | populated | m07-p03 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p03 | populated | m07-p03 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p03 | populated | m07-p03 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p03 | populated | m07-p03 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p04 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p04 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p04 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p04 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p04 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p04 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p04 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p04 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p04 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p04 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p04 | populated | m07-p03 | 互动 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p04 | populated | m07-p03 | 喂食 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p04 | populated | m07-p03 | 任务 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p04 | populated | m07-p03 | 装扮 | 可用 | ()=>go([6,8,11,12][i]) |
| m07-p04 | populated | m07-p03 | 布置小屋 | 可用 | ()=>go([15,18,21][i]) |
| m07-p04 | populated | m07-p03 | 成长故事 | 可用 | ()=>go([15,18,21][i]) |
| m07-p04 | populated | m07-p03 | 成就图鉴 | 可用 | ()=>go([15,18,21][i]) |
| m07-p04 | populated | m07-p03 | 去任务 › | 可用 | ()=>go(11) |
| m07-p04 | populated | m07-p03 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p04 | populated | m07-p03 | 宠物设置 | 可用 | ()=>go(25) |
| m07-p04 | populated | m07-p03 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p04 | populated | m07-p03 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p04 | populated | m07-p03 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p04 | populated | m07-p03 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p04 | populated | m07-p03 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p05 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p05 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p05 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p05 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p05 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p05 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p05 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p05 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p05 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p05 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p05 | populated | m07-p06 | 摸摸头 精力 -5 · 亲密 +3 · 心情 +2 | 可用 | ()=>{selected=i;all('.option').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p05 | populated | m07-p06 | 丢球球 精力 -12 · 亲密 +3 · 心情 +8 | 可用 | ()=>{selected=i;all('.option').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p05 | populated | m07-p06 | 讲故事 精力 -8 · 亲密 +6 · 心情 +4 | 可用 | ()=>{selected=i;all('.option').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p05 | populated | m07-p06 | 送小礼物 礼物 1 份 · 消耗1份 | 可用 | ()=>{selected=i;all('.option').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p05 | populated | m07-p06 | 和团团互动 | 可用 | ()=>UI.busy(q('#play'),'陪伴中…',async()=>{const result=Pet.interact(selected);if(result?.low)return UI.go('m07-p07.html?cost='+Pet.interactions[selected].energy);if(result?.id)return UI.go('m07-p05.html?id='+encodeURIComponent(result.id));return false;}) |
| m07-p05 | populated | m07-p06 | 返回 | 可用 | ()=>UI.back('m07-p'+String(fallback).padStart(2,'0')+'.html') |
| m07-p06 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p06 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p06 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p06 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p06 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p06 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p06 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p06 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p06 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p06 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p06 | populated | m07-p06 | 摸摸头 精力 -5 · 亲密 +3 · 心情 +2 | 可用 | ()=>{selected=i;all('.option').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p06 | populated | m07-p06 | 丢球球 精力 -12 · 亲密 +3 · 心情 +8 | 可用 | ()=>{selected=i;all('.option').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p06 | populated | m07-p06 | 讲故事 精力 -8 · 亲密 +6 · 心情 +4 | 可用 | ()=>{selected=i;all('.option').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p06 | populated | m07-p06 | 送小礼物 礼物 1 份 · 消耗1份 | 可用 | ()=>{selected=i;all('.option').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p06 | populated | m07-p06 | 和团团互动 | 可用 | ()=>UI.busy(q('#play'),'陪伴中…',async()=>{const result=Pet.interact(selected);if(result?.low)return UI.go('m07-p07.html?cost='+Pet.interactions[selected].energy);if(result?.id)return UI.go('m07-p05.html?id='+encodeURIComponent(result.id));return false;}) |
| m07-p06 | populated | m07-p06 | 返回 | 可用 | ()=>UI.back('m07-p'+String(fallback).padStart(2,'0')+'.html') |
| m07-p07 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p07 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p07 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p07 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p07 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p07 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p07 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p07 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p07 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p07 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p07 | populated | m07-p06 | 摸摸头 精力 -5 · 亲密 +3 · 心情 +2 | 可用 | ()=>{selected=i;all('.option').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p07 | populated | m07-p06 | 丢球球 精力 -12 · 亲密 +3 · 心情 +8 | 可用 | ()=>{selected=i;all('.option').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p07 | populated | m07-p06 | 讲故事 精力 -8 · 亲密 +6 · 心情 +4 | 可用 | ()=>{selected=i;all('.option').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p07 | populated | m07-p06 | 送小礼物 礼物 1 份 · 消耗1份 | 可用 | ()=>{selected=i;all('.option').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p07 | populated | m07-p06 | 和团团互动 | 可用 | ()=>UI.busy(q('#play'),'陪伴中…',async()=>{const result=Pet.interact(selected);if(result?.low)return UI.go('m07-p07.html?cost='+Pet.interactions[selected].energy);if(result?.id)return UI.go('m07-p05.html?id='+encodeURIComponent(result.id));return false;}) |
| m07-p07 | populated | m07-p06 | 返回 | 可用 | ()=>UI.back('m07-p'+String(fallback).padStart(2,'0')+'.html') |
| m07-p08 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p08 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p08 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p08 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p08 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p08 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p08 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p08 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p08 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p08 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p08 | populated | m07-p08 | 香香主粮 ×12 饱食+12 精力+15 | 可用 | ()=>{selected=i;all('.foods button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p08 | populated | m07-p08 | 爱心小饼干 ×5 饱食+8 精力+8 心情+2 | 可用 | ()=>{selected=i;all('.foods button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p08 | populated | m07-p08 | 草莓布丁 ×1 饱食+20 精力+20 心情+5 | 可用 | ()=>{selected=i;all('.foods button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p08 | populated | m07-p08 | 喂给团团 | 可用 | ()=>UI.busy(q('#feed'),'喂食中…',async()=>{const result=Pet.feed(selected);if(result?.empty)return UI.go('m07-p09.html?food='+selected);if(result?.saved){paint();UI.toast('喂食已记录，精力和饱食已更新','success');return true;}return false;}) |
| m07-p08 | populated | m07-p08 | 去获得更多食物 › | 可用 | ()=>go(11) |
| m07-p08 | populated | m07-p08 | 返回 | 可用 | ()=>UI.back('m07-p'+String(fallback).padStart(2,'0')+'.html') |
| m07-p09 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p09 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p09 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p09 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p09 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p09 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p09 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p09 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p09 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p09 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p09 | populated | m07-p08 | 香香主粮 ×12 饱食+12 精力+15 | 可用 | ()=>{selected=i;all('.foods button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p09 | populated | m07-p08 | 爱心小饼干 ×5 饱食+8 精力+8 心情+2 | 可用 | ()=>{selected=i;all('.foods button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p09 | populated | m07-p08 | 草莓布丁 ×1 饱食+20 精力+20 心情+5 | 可用 | ()=>{selected=i;all('.foods button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m07-p09 | populated | m07-p08 | 喂给团团 | 可用 | ()=>UI.busy(q('#feed'),'喂食中…',async()=>{const result=Pet.feed(selected);if(result?.empty)return UI.go('m07-p09.html?food='+selected);if(result?.saved){paint();UI.toast('喂食已记录，精力和饱食已更新','success');return true;}return false;}) |
| m07-p09 | populated | m07-p08 | 去获得更多食物 › | 可用 | ()=>go(11) |
| m07-p09 | populated | m07-p08 | 返回 | 可用 | ()=>UI.back('m07-p'+String(fallback).padStart(2,'0')+'.html') |
| m07-p10 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p10 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p10 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p10 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p10 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p10 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p10 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p10 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p10 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p10 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p10 | populated | m07-p11 | 每日任务 | 可用 | ()=>{tab=i;paintTasks();} |
| m07-p10 | populated | m07-p11 | 本周约定 | 可用 | ()=>{tab=i;paintTasks();} |
| m07-p10 | populated | m07-p11 | 完成陪团团互动 | 隐藏/禁用 | location.href='m07-p06.html' |
| m07-p10 | populated | m07-p11 | 完成整理小屋 | 隐藏/禁用 | location.href='m07-p15.html' |
| m07-p10 | populated | m07-p11 | 返回小屋 | 可用 | ()=>go(3) |
| m07-p10 | populated | m07-p11 | 返回 | 可用 | ()=>UI.back('m07-p'+String(fallback).padStart(2,'0')+'.html') |
| m07-p10 | populated | m07-p11 | 给宠物添水 | 可用 | ()=>UI.busy(b,'添水中…',async()=>{if(!Pet.water())return false;UI.toast('清水已添好','success');paintTasks();return true;}) |
| m07-p10 | populated | m07-p11 | 陪宠物互动 | 可用 | ()=>go(6) |
| m07-p10 | populated | m07-p11 | 给宠物喂食 | 可用 | ()=>go(8) |
| m07-p10 | populated | m07-p11 | 整理宠物小屋 | 可用 | ()=>go(15) |
| m07-p10 | populated | m07-p11 | 记录今天的小心情 | 可用 | function note(){const form=document.createElement('form'),label=document.createElement('label'),input=document.createElement('textarea'),save=document.createElement('button');label.textContent='今天的小心情';input.maxLength=500;input.setAttribute('aria-label','今天的小心情');label.append(input);save.type='submit';save.textContent='保存小心情';form.append(label,save);form.className='pet-note-form';const protect=UI.protectSheet(form);form.onsubmit=e=>{e.preventDefault();if(!UI.fieldError(input,input.value.trim()?'':'请填写今天的小心情'))return;UI.busy(save,'保存中…',async()=>{if(!Pet.note(input.value))return false;protect.c |
| m07-p10 | populated | m07-p11 | 再完成 3 次照顾 | 隐藏/禁用 | ()=>UI.busy(b,'领取中…',async()=>{const result=Pet.claim('weekly');if(result)return UI.go('m07-p10.html?id='+encodeURIComponent(result.id));return false;}) |
| m07-p11 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p11 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p11 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p11 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p11 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p11 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p11 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p11 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p11 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p11 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p11 | populated | m07-p11 | 每日任务 | 可用 | ()=>{tab=i;paintTasks();} |
| m07-p11 | populated | m07-p11 | 本周约定 | 可用 | ()=>{tab=i;paintTasks();} |
| m07-p11 | populated | m07-p11 | 完成陪团团互动 | 隐藏/禁用 | location.href='m07-p06.html' |
| m07-p11 | populated | m07-p11 | 完成整理小屋 | 隐藏/禁用 | location.href='m07-p15.html' |
| m07-p11 | populated | m07-p11 | 返回小屋 | 可用 | ()=>go(3) |
| m07-p11 | populated | m07-p11 | 返回 | 可用 | ()=>UI.back('m07-p'+String(fallback).padStart(2,'0')+'.html') |
| m07-p11 | populated | m07-p11 | 给宠物添水 | 可用 | ()=>UI.busy(b,'添水中…',async()=>{if(!Pet.water())return false;UI.toast('清水已添好','success');paintTasks();return true;}) |
| m07-p11 | populated | m07-p11 | 陪宠物互动 | 可用 | ()=>go(6) |
| m07-p11 | populated | m07-p11 | 给宠物喂食 | 可用 | ()=>go(8) |
| m07-p11 | populated | m07-p11 | 整理宠物小屋 | 可用 | ()=>go(15) |
| m07-p11 | populated | m07-p11 | 记录今天的小心情 | 可用 | function note(){const form=document.createElement('form'),label=document.createElement('label'),input=document.createElement('textarea'),save=document.createElement('button');label.textContent='今天的小心情';input.maxLength=500;input.setAttribute('aria-label','今天的小心情');label.append(input);save.type='submit';save.textContent='保存小心情';form.append(label,save);form.className='pet-note-form';const protect=UI.protectSheet(form);form.onsubmit=e=>{e.preventDefault();if(!UI.fieldError(input,input.value.trim()?'':'请填写今天的小心情'))return;UI.busy(save,'保存中…',async()=>{if(!Pet.note(input.value))return false;protect.c |
| m07-p11 | populated | m07-p11 | 再完成 3 次照顾 | 隐藏/禁用 | ()=>UI.busy(b,'领取中…',async()=>{const result=Pet.claim('weekly');if(result)return UI.go('m07-p10.html?id='+encodeURIComponent(result.id));return false;}) |
| m07-p12 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p12 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p12 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p12 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p12 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p12 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p12 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p12 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p12 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p12 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p12 | populated | m07-p12 | 返回宠物小屋 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p12 | populated | m07-p12 | 衣服 | 可用 | ()=>{group=b.textContent;paint();} |
| m07-p12 | populated | m07-p12 | 配饰 | 可用 | ()=>{group=b.textContent;paint();} |
| m07-p12 | populated | m07-p12 | 小物 | 可用 | ()=>{group=b.textContent;paint();} |
| m07-p12 | populated | m07-p12 | 不佩戴 | 可用 | ()=>{selected=null;paint();} |
| m07-p12 | populated | m07-p12 | 小花围巾 已拥有 | 可用 | ()=>choose(item,onChoose) |
| m07-p12 | populated | m07-p12 | 格纹蝴蝶结 金币20 | 可用 | ()=>choose(item,onChoose) |
| m07-p12 | populated | m07-p12 | 星星领结 亲密度160 | 可用 | ()=>choose(item,onChoose) |
| m07-p12 | populated | m07-p12 | 蜜桃帽子 记录一页成长故事 | 可用 | ()=>choose(item,onChoose) |
| m07-p12 | populated | m07-p12 | 星光皇冠 星星30 | 可用 | ()=>choose(item,onChoose) |
| m07-p12 | populated | m07-p12 | 保存这身搭配 | 可用 | ()=>UI.busy(q('#save'),'保存穿戴中…',()=>{if(!L.equip(selected))return false;guard.commit();UI.toast('穿戴已保存','success');paint();return true;}) |
| m07-p12 | populated | m07-p12 | 预览：不佩戴 | 隐藏/禁用 | ()=>{} |
| m07-p13 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p13 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p13 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p13 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p13 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p13 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p13 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p13 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p13 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p13 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p13 | populated | m07-p13 | 宠物空间 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p13 | populated | m07-p13 | 返回选择 | 可用 | ()=>go(can?n===13?12:15:11) |
| m07-p14 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p14 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p14 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p14 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p14 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p14 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p14 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p14 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p14 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p14 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p14 | populated | m07-p15 | 地毯 | 可用 | ()=>{group=b.dataset.tab;paint();} |
| m07-p14 | populated | m07-p15 | 小床 | 可用 | ()=>{group=b.dataset.tab;paint();} |
| m07-p14 | populated | m07-p15 | 墙饰 | 可用 | ()=>{group=b.dataset.tab;paint();} |
| m07-p14 | populated | m07-p15 | 摆件 | 可用 | ()=>{group=b.dataset.tab;paint();} |
| m07-p14 | populated | m07-p15 | 花朵地毯 已拥有 | 可用 | ()=>choose(item,onChoose) |
| m07-p14 | populated | m07-p15 | 格纹地毯 金币20 | 可用 | ()=>choose(item,onChoose) |
| m07-p14 | populated | m07-p15 | 月亮地毯 亲密度160 | 可用 | ()=>choose(item,onChoose) |
| m07-p14 | populated | m07-p15 | 野餐垫 照顾7个不同日期 | 可用 | ()=>choose(item,onChoose) |
| m07-p14 | populated | m07-p15 | 保存小屋布置 | 可用 | ()=>UI.busy(q('.save'),'保存布置中…',()=>{const result=L.saveRoom(draft);if(!result)return false;guard.commit();return go(14,'?id='+encodeURIComponent(result.id));}) |
| m07-p14 | populated | m07-p15 | 返回 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p15 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p15 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p15 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p15 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p15 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p15 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p15 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p15 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p15 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p15 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p15 | populated | m07-p15 | 地毯 | 可用 | ()=>{group=b.dataset.tab;paint();} |
| m07-p15 | populated | m07-p15 | 小床 | 可用 | ()=>{group=b.dataset.tab;paint();} |
| m07-p15 | populated | m07-p15 | 墙饰 | 可用 | ()=>{group=b.dataset.tab;paint();} |
| m07-p15 | populated | m07-p15 | 摆件 | 可用 | ()=>{group=b.dataset.tab;paint();} |
| m07-p15 | populated | m07-p15 | 花朵地毯 已拥有 | 可用 | ()=>choose(item,onChoose) |
| m07-p15 | populated | m07-p15 | 格纹地毯 金币20 | 可用 | ()=>choose(item,onChoose) |
| m07-p15 | populated | m07-p15 | 月亮地毯 亲密度160 | 可用 | ()=>choose(item,onChoose) |
| m07-p15 | populated | m07-p15 | 野餐垫 照顾7个不同日期 | 可用 | ()=>choose(item,onChoose) |
| m07-p15 | populated | m07-p15 | 保存小屋布置 | 可用 | ()=>UI.busy(q('.save'),'保存布置中…',()=>{const result=L.saveRoom(draft);if(!result)return false;guard.commit();return go(14,'?id='+encodeURIComponent(result.id));}) |
| m07-p15 | populated | m07-p15 | 返回 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p16 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p16 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p16 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p16 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p16 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p16 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p16 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p16 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p16 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p16 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p16 | populated | m07-p16 | 返回 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p16 | populated | m07-p16 | 返回选择 | 可用 | ()=>go(can?n===13?12:15:11) |
| m07-p17 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p17 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p17 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p17 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p17 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p17 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p17 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p17 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p17 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p17 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p17 | populated | m07-p19 | 写下今天的下一页 | 可用 | ()=>writeStory(()=>go(18)) |
| m07-p17 | populated | m07-p19 | 返回 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p17 | populated | m07-p19 | 回应这一页 | 可用 | ()=>edit({title:'回应',label:'回应内容',limit:300,save:text=>L.reply(entry.id,text),after:paint}) |
| m07-p18 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p18 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p18 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p18 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p18 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p18 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p18 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p18 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p18 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p18 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p18 | populated | m07-p18 | 写一页成长故事 | 可用 | ()=>writeStory(paint) |
| m07-p18 | populated | m07-p18 | 返回 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p18 | populated | m07-p18 | 2026-10-04 · 小满 实际成长故事 | 可用 | ()=>go(entry.blocked?17:19,'?id='+encodeURIComponent(entry.id)) |
| m07-p18 | populated | m07-p18 | 关联共同记录 | 可用 | async()=>{const rows=L.sources();if(!rows.length){const result=await UI.sheet({title:'还没有共同记录',message:'先发布一篇共同日记或照片，再收进宠物故事。',actions:[{label:'写共同日记',value:'diary'}]});if(result==='diary')UI.go('m03-p05.html');return;}const id=await UI.sheet({title:'关联共同记录',actions:rows.map(v=>({label:v.title,value:{id:v.id,kind:v.kind}}))});if(!id)return;const trigger=q('.pet-life-extra');UI.busy(trigger,'关联中…',()=>{if(!L.link(id.id,id.kind))return false;UI.toast('共同记录已关联','success');paint();return true;});} |
| m07-p19 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p19 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p19 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p19 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p19 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p19 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p19 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p19 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p19 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p19 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p19 | populated | m07-p19 | 写下今天的下一页 | 可用 | ()=>writeStory(()=>go(18)) |
| m07-p19 | populated | m07-p19 | 返回 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p19 | populated | m07-p19 | 回应这一页 | 可用 | ()=>edit({title:'回应',label:'回应内容',limit:300,save:text=>L.reply(entry.id,text),after:paint}) |
| m07-p20 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p20 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p20 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p20 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p20 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p20 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p20 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p20 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p20 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p20 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p20 | populated | m07-p20 | 返回 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p20 | populated | m07-p20 | 领取奖励 | 可用 | ()=>UI.busy(q('.claim'),'领取中…',()=>{if(!L.achievementClaim(id))return false;UI.toast('成就奖励已到账','success');return true;}).then(paint) |
| m07-p21 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p21 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p21 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p21 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p21 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p21 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p21 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p21 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p21 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p21 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p21 | populated | m07-p21 | 第一次见面 可领取奖励 | 可用 | ()=>go(20,'?achievement='+item.id) |
| m07-p21 | populated | m07-p21 | 玩到天黑 0 / 10 | 可用 | ()=>go(20,'?achievement='+item.id) |
| m07-p21 | populated | m07-p21 | 默契喂食 0 / 20 | 可用 | ()=>go(20,'?achievement='+item.id) |
| m07-p21 | populated | m07-p21 | 小屋变新了 0 / 1 | 可用 | ()=>go(20,'?achievement='+item.id) |
| m07-p21 | populated | m07-p21 | 照顾7天 1 / 7 | 可用 | ()=>go(20,'?achievement='+item.id) |
| m07-p21 | populated | m07-p21 | 亲密搭档 可领取奖励 | 可用 | ()=>go(20,'?achievement='+item.id) |
| m07-p21 | populated | m07-p21 | 陪伴30天 可领取奖励 | 可用 | ()=>go(20,'?achievement='+item.id) |
| m07-p21 | populated | m07-p21 | 去完成今天的照顾 | 可用 | ()=>go(11) |
| m07-p21 | populated | m07-p21 | 返回 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p21 | populated | m07-p21 | 收藏图鉴 | 可用 | ()=>go(22) |
| m07-p22 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p22 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p22 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p22 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p22 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p22 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p22 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p22 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p22 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p22 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p22 | populated | m07-p22 | 装扮 | 可用 | ()=>{group=b.dataset.tab;paint();} |
| m07-p22 | populated | m07-p22 | 小屋 | 可用 | ()=>{group=b.dataset.tab;paint();} |
| m07-p22 | populated | m07-p22 | 纪念物 | 可用 | ()=>{group=b.dataset.tab;paint();} |
| m07-p22 | populated | m07-p22 | 小花围巾 已拥有 | 可用 | ()=>go(23,'?'+(group==='纪念物'?'achievement=':'item=')+item.id) |
| m07-p22 | populated | m07-p22 | 格纹蝴蝶结 金币20 | 可用 | ()=>go(23,'?'+(group==='纪念物'?'achievement=':'item=')+item.id) |
| m07-p22 | populated | m07-p22 | 星星领结 亲密度160 | 可用 | ()=>go(23,'?'+(group==='纪念物'?'achievement=':'item=')+item.id) |
| m07-p22 | populated | m07-p22 | 蜜桃帽子 记录一页成长故事 | 可用 | ()=>go(23,'?'+(group==='纪念物'?'achievement=':'item=')+item.id) |
| m07-p22 | populated | m07-p22 | 星光皇冠 星星30 | 可用 | ()=>go(23,'?'+(group==='纪念物'?'achievement=':'item=')+item.id) |
| m07-p22 | populated | m07-p22 | 雨天小斗篷 照顾7个不同日期 | 可用 | ()=>go(23,'?'+(group==='纪念物'?'achievement=':'item=')+item.id) |
| m07-p22 | populated | m07-p22 | 暖暖小马甲 金币20 | 可用 | ()=>go(23,'?'+(group==='纪念物'?'achievement=':'item=')+item.id) |
| m07-p22 | populated | m07-p22 | 晚安铃铛 喂食20次 | 可用 | ()=>go(23,'?'+(group==='纪念物'?'achievement=':'item=')+item.id) |
| m07-p22 | populated | m07-p22 | 返回 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p22 | populated | m07-p22 | 认识小伙伴 | 可用 | async()=>{const kind=await UI.sheet({title:'四位小伙伴',message:'首期共同选择一位。当前小伙伴会保留，不会直接切换或覆盖已有成长。',actions:['小狗','小猫','小兔','小狐狸'].map(kind=>({label:kind+(Pet.read().kind===kind?' · 正在共同照顾':' · 首次领养可选'),value:kind}))});if(!kind)return;const picture=document.createElement('div');picture.className='pet-breed-picture';picture.dataset.kind=kind;picture.setAttribute('role','img');picture.setAttribute('aria-label',kind+'领养插画');await UI.modal({title:kind+' · '+(Pet.read().kind===kind?'已共同领养':'尚未领养'),message:'领养时可以选择品种和名字。这里用于了解伙伴，不会切换或覆盖已有宠物与成长记录。',content:picture,confirm:'了解了',cancel:'关闭'});} |
| m07-p23 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p23 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p23 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p23 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p23 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p23 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p23 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p23 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p23 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p23 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p23 | populated | m07-p23 | 返回图鉴 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p23 | populated | m07-p23 | 去换上 | 可用 | ()=>{if(achievement)return go(20,'?achievement='+achievement);if(!owned)return go(item.type==='room'?16:13,'?item='+item.id);if(item.type==='room')return go(15);UI.busy(wear,'保存穿戴中…',()=>{if(!L.equip(item.name))return false;return go(12);});} |
| m07-p23 | populated | m07-p23 | 返回图鉴 | 可用 | ()=>go(22) |
| m07-p24 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p24 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p24 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p24 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p24 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p24 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p24 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p24 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p24 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p24 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p24 | populated | m07-p24 | 先导出成长记录 | 可用 | ()=>UI.busy(q('#export'),'导出中…',()=>{L.download();UI.toast('成长记录已导出','success');return true;}) |
| m07-p24 | populated | m07-p24 | 暂时解除共同照顾 | 可用 | async()=>{if(!await UI.modal({title:'暂停共同照顾？',message:'宠物、库存、成长和已获得物品保留；暂停后不新增照顾记录。可以在设置中重新开始。',confirm:'确认暂停',cancel:'继续照顾'}))return;UI.busy(q('#unlink'),'暂停中…',()=>{if(!L.care(false))return false;return go(25);});} |
| m07-p24 | populated | m07-p24 | 我再想想，返回 | 可用 | ()=>go(25) |
| m07-p24 | populated | m07-p24 | 返回 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p25 | empty | m07-p04 | 照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p25 | empty | m07-p04 | 宠物日记 | 可用 | ()=>UI.modal({title:'从第一天开始记录',message:'完成共同领养后，可在任务中记录宠物小心情。',confirm:'去领养',cancel:'先看看'}).then(ok=>ok&&q('.adopt').click()) |
| m07-p25 | empty | m07-p04 | 一起领养 | 可用 | ()=>{if(pet?.status==='rejected'){const old=pet;UI.modal({title:'重新发起领养？',message:'另一半没有同意上次邀请。可以重新选择品种和名字。',confirm:'重新选择',cancel:'取消'}).then(ok=>{if(ok){if(UI.failNext('pet-adopt')){UI.toast('操作失败，请重试','error');return;}if(UI.write(Pet.key,null))go(2);}});}else go(2);} |
| m07-p25 | empty | m07-p04 | 先看看照顾指南 | 可用 | ()=>UI.modal({title:'一起照顾小伙伴',message:'另一半确认领养后开始照顾。每天可互动两次，喂食补充饱食与精力。添水、互动、喂食和记录心情可完成任务；奖励只领取一次。未登录另一半的操作通过本地评审演示，不会发送真实通知。',confirm:'知道了',cancel:'关闭'}) |
| m07-p25 | empty | m07-p04 | 返回 | 可用 | ()=>UI.back('m03-p01.html') |
| m07-p25 | empty | m07-p04 | 首页 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p25 | empty | m07-p04 | 重要时刻 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p25 | empty | m07-p04 | 工坊 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p25 | empty | m07-p04 | 宠物 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p25 | empty | m07-p04 | 我的 | 可用 | ()=>tab.key===active.key?scrollTo({top:0,behavior:'auto'}):go(tab.href,{replace:true}) |
| m07-p25 | populated | m07-p25 | 返回宠物空间 | 可用 | ()=>UI.back('m07-p'+fallback+'.html') |
| m07-p25 | populated | m07-p25 | 共同提醒 每天 20:30 · 本地提醒 | 可用 | ()=>edit({title:'提醒时间',label:'每天提醒时间',initial:L.settings(Pet.read()).time,type:'time',limit:5,save:value=>{if(!/^([01]\d／2[0-3]):[0-5]\d$/.test(value)){UI.toast('请选择有效的 HH:MM 时间','error');return false;}return L.setting('time',value);},after:paint}) |
| m07-p25 | populated | m07-p25 | 共同提醒 | 可用 | ()=>UI.busy(b,'更新中…',()=>{const key=b.dataset.key==='story'?'stories':b.dataset.key==='notice'?'notice':'reminder';if(!L.setting(key,!L.settings(Pet.read())[key]))return false;UI.toast('设置已更新','success');return true;}).then(paint) |
| m07-p25 | populated | m07-p25 | 照顾通知 | 可用 | ()=>q('.s2').click() |
| m07-p25 | populated | m07-p25 | 照顾通知 | 可用 | ()=>UI.busy(b,'更新中…',()=>{const key=b.dataset.key==='story'?'stories':b.dataset.key==='notice'?'notice':'reminder';if(!L.setting(key,!L.settings(Pet.read())[key]))return false;UI.toast('设置已更新','success');return true;}).then(paint) |
| m07-p25 | populated | m07-p25 | 成长故事自动收录 | 可用 | ()=>q('.s3').click() |
| m07-p25 | populated | m07-p25 | 成长故事自动收录 | 可用 | ()=>UI.busy(b,'更新中…',()=>{const key=b.dataset.key==='story'?'stories':b.dataset.key==='notice'?'notice':'reminder';if(!L.setting(key,!L.settings(Pet.read())[key]))return false;UI.toast('设置已更新','success');return true;}).then(paint) |
| m07-p25 | populated | m07-p25 | 导出团团的成长记录 | 可用 | ()=>UI.busy(q('#export'),'导出中…',()=>{L.download();UI.toast('成长记录已导出','success');return true;}) |
| m07-p25 | populated | m07-p25 | 仅我们可见说明 | 可用 | ()=>UI.modal({title:'仅我们可见',message:'共同宠物与成长记录仅用于当前浏览器内的双人原型。关联的日记和照片必须仍为共同可见；变为私密或删除后不再展示或导出关联正文。不会发送推送、上传或公开这些记录。',confirm:'知道了',cancel:'关闭'}) |
| m07-p25 | populated | m07-p25 | 暂时解除共同照顾 | 可用 | async()=>{const current=Pet.read();if(current.care&&UI.read('dujia-prototype-relationship',{})?.bound)return go(24);if(!UI.read('dujia-prototype-relationship',{})?.bound){if(await UI.modal({title:'先重新关联另一半',message:'宠物和原有成长仍保留，关联后可恢复照顾。',confirm:'去关联',cancel:'取消'}))UI.go('m02-p01.html');return;}if(!await UI.modal({title:'重新开始共同照顾？',message:'原有数据保留，并从现在继续新增照顾记录。',confirm:'重新开始照顾',cancel:'取消'}))return;UI.busy(q('.r6'),'恢复中…',()=>{if(!L.care(true))return false;UI.toast('已恢复共同照顾','success');return true;}).then(paint);} |
| m07-p25 | populated | m07-p25 | 更多 | 可用 | async()=>{const action=await UI.sheet({title:'宠物资料与数据',actions:[{label:'修改宠物名字',value:'rename'},{label:'永久删除宠物数据',value:'delete',danger:true}]});if(action==='rename')edit({title:'宠物名字',label:'宠物名字',initial:Pet.read().name,type:'text',limit:12,save:L.rename,after:paint});if(action==='delete')edit({title:'删除确认',confirmLabel:'永久删除',danger:true,message:'永久删除当前宠物、成长、库存和布置。普通日记和照片仍保留；删除后无法恢复。',label:'输入宠物名字确认删除',type:'text',limit:12,save:async value=>{if(value!==Pet.read().name){UI.toast('名字不一致，尚未删除','error');return false;}if(!L.remove())return false;return true;},after:()=>go(4)});} |
| m08-p01 | empty | m08-p02 | 返回 | 可用 | ()=>UI.go('m03-p02.html') |
| m08-p01 | empty | m08-p02 | 新建第一本回忆册 | 可用 | ()=>go(4,{},null) |
| m08-p01 | populated | m08-p01 | ♡ 共同测试册 花园午后 | 可用 | ()=>go(15,{},value.id) |
| m08-p01 | populated | m08-p01 | 继续阅读 › | 可用 | ()=>go(latest.lastPage?16:15,latest.lastPage?{page:latest.lastPage}:{},latest.id) |
| m08-p01 | populated | m08-p01 | 新建回忆册 | 可用 | ()=>go(4,{},null) |
| m08-p01 | populated | m08-p01 | 本月推荐 | 可用 | ()=>go(3,{},null) |
| m08-p01 | populated | m08-p01 | 归档与草稿 | 可用 | async()=>{const rows=B.all().filter(v=>v.archived／／v.status==='draft');const picked=await UI.sheet({title:'归档与草稿',message:rows.length?'选择一本继续整理或恢复。':'还没有归档或草稿。',actions:rows.map(v=>({label:v.name+' · '+(v.archived?'已归档':'草稿'),value:v.id}))});if(picked)go(B.find(picked).archived?21:4,{},picked);} |
| m08-p01 | populated | m08-p01 | 返回首页 | 可用 | ()=>UI.go('m03-p02.html') |
| m08-p02 | empty | m08-p02 | 返回 | 可用 | ()=>UI.go('m03-p02.html') |
| m08-p02 | empty | m08-p02 | 新建第一本回忆册 | 可用 | ()=>go(4,{},null) |
| m08-p02 | populated | m08-p02 | 返回 | 可用 | ()=>UI.go('m03-p02.html') |
| m08-p02 | populated | m08-p02 | 新建第一本回忆册 | 可用 | ()=>go(4,{},null) |
| m08-p03 | empty | m08-p03 | 返回回忆册 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p03 | empty | m08-p03 | 查看并确认素材 | 可用 | ()=>go(4,{recommend:'1'},null) |
| m08-p03 | empty | m08-p03 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p03 | empty | m08-p03 | 写共同日记 | 可用 | ()=>UI.go('m03-p05.html') |
| m08-p03 | populated | m08-p03 | 返回回忆册 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p03 | populated | m08-p03 | 查看并确认素材 | 可用 | ()=>go(4,{recommend:'1'},null) |
| m08-p03 | populated | m08-p03 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p03 | populated | m08-p03 | 共同日记 · 2026-10-04 | 可用 | ()=>UI.go(v.url) |
| m08-p03 | populated | m08-p03 | 共同照片 · 2026-10-04 | 可用 | ()=>UI.go(v.url) |
| m08-p03 | populated | m08-p03 | 共同重要时刻 · 2026-10-04 | 可用 | ()=>UI.go(v.url) |
| m08-p03 | populated | m08-p03 | 实际工坊作品 · 2026-10-05 | 可用 | ()=>UI.go(v.url) |
| m08-p03 | populated | m08-p03 | 实际成长故事 · 2026-10-04 | 可用 | ()=>UI.go(v.url) |
| m08-p04 | empty | m08-p04 | 返回 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p04 | empty | m08-p04 | 书名 | 可用 | 原生输入/选择器 |
| m08-p04 | empty | m08-p04 | 开始月份 | 可用 | 原生输入/选择器 |
| m08-p04 | empty | m08-p04 | 结束月份 | 可用 | 原生输入/选择器 |
| m08-p04 | empty | m08-p04 | 从共同素材开始 | 可用 | ()=>{start=e.dataset.start;paint();} |
| m08-p04 | empty | m08-p04 | 空白回忆册 | 可用 | ()=>{start=e.dataset.start;paint();} |
| m08-p04 | empty | m08-p04 | 下一步：选择主题 | 可用 | ()=>{if(!valid())return;UI.busy(q('.next'),'保存基础信息…',()=>{const data={name:q('.book-name').value.trim(),dates:all('.dates input').map(e=>e.value),start},next=current?{...B.requireBook(id),...data}:B.draft(data),saved=B.put(next,'book-create');if(!saved)return false;guard.commit();return go(5,{},saved.id);});} |
| m08-p04 | populated | m08-p04 | 返回 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p04 | populated | m08-p04 | 书名 | 可用 | 原生输入/选择器 |
| m08-p04 | populated | m08-p04 | 开始月份 | 可用 | 原生输入/选择器 |
| m08-p04 | populated | m08-p04 | 结束月份 | 可用 | 原生输入/选择器 |
| m08-p04 | populated | m08-p04 | 从共同素材开始 | 可用 | ()=>{start=e.dataset.start;paint();} |
| m08-p04 | populated | m08-p04 | 空白回忆册 | 可用 | ()=>{start=e.dataset.start;paint();} |
| m08-p04 | populated | m08-p04 | 下一步：选择主题 | 可用 | ()=>{if(!valid())return;UI.busy(q('.next'),'保存基础信息…',()=>{const data={name:q('.book-name').value.trim(),dates:all('.dates input').map(e=>e.value),start},next=current?{...B.requireBook(id),...data}:B.draft(data),saved=B.put(next,'book-create');if(!saved)return false;guard.commit();return go(5,{},saved.id);});} |
| m08-p05 | empty | m08-p05 | 返回上一步 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p05 | empty | m08-p05 | 花园午后 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p05 | empty | m08-p05 | 旅行手札 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p05 | empty | m08-p05 | 暖灯日常 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p05 | empty | m08-p05 | 使用封面照片 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p05 | empty | m08-p05 | 下一步：选择素材 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p05 | empty | m08-p05 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p05 | populated | m08-p05 | 返回上一步 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p05 | populated | m08-p05 | 花园午后 | 可用 | ()=>{theme=e.dataset.theme;paint();} |
| m08-p05 | populated | m08-p05 | 旅行手札 | 可用 | ()=>{theme=e.dataset.theme;paint();} |
| m08-p05 | populated | m08-p05 | 暖灯日常 | 可用 | ()=>{theme=e.dataset.theme;paint();} |
| m08-p05 | populated | m08-p05 | 使用封面照片 | 可用 | ()=>{if(cover){cover=false;paint();}else sourceChoice('photo',value=>{cover=value;paint();});} |
| m08-p05 | populated | m08-p05 | 下一步：选择素材 | 可用 | ()=>UI.busy(q('.next'),'保存主题…',()=>{if(cover&&!B.source(cover,book())?.image)throw new Error('封面照片已不可见，请关闭照片或重新选择');const saved=B.change(id,value=>{value.theme=theme;value.coverPhoto=cover;},'book-theme');if(!saved)return false;guard.commit();return go(managing?21:saved.start==='blank'?13:6);}) |
| m08-p06 | empty | m08-p06 | 返回上一步 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p06 | empty | m08-p06 | 全部 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p06 | empty | m08-p06 | 日记 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p06 | empty | m08-p06 | 照片 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p06 | empty | m08-p06 | 时刻 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p06 | empty | m08-p06 | 工坊 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p06 | empty | m08-p06 | 宠物 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p06 | empty | m08-p06 | 晚霞散步今天的晚霞把天空染成了橘粉色，我们手牵手走在江边，好像时间都慢了下来。2024.05.18晚霞散步日记2024.05.18　20:47共同可见 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p06 | empty | m08-p06 | 一起看日落照片2024.04.21　18:36共同可见 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p06 | empty | m08-p06 | 厦门之旅第一次旅行重要时刻2023.10.03 – 10.06共同可见 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p06 | empty | m08-p06 | 鼓浪屿的风都温柔手作明信片工坊作品2024.02.14　15:22共同可见 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p06 | empty | m08-p06 | 团子学会握手宠物2024.03.09　11:08共同可见 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p06 | empty | m08-p06 | 开始编排 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p06 | empty | m08-p06 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p06 | populated | m08-p06 | 返回上一步 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p06 | populated | m08-p06 | 全部 | 可用 | ()=>{category=e.dataset.type;paint();} |
| m08-p06 | populated | m08-p06 | 日记 | 可用 | ()=>{category=e.dataset.type;paint();} |
| m08-p06 | populated | m08-p06 | 照片 | 可用 | ()=>{category=e.dataset.type;paint();} |
| m08-p06 | populated | m08-p06 | 时刻 | 可用 | ()=>{category=e.dataset.type;paint();} |
| m08-p06 | populated | m08-p06 | 工坊 | 可用 | ()=>{category=e.dataset.type;paint();} |
| m08-p06 | populated | m08-p06 | 宠物 | 可用 | ()=>{category=e.dataset.type;paint();} |
| m08-p06 | populated | m08-p06 | 共同日记 · 日记 · 2026-10-04 | 可用 | ()=>{selected=has?selected.filter(s=>!(s.kind===ref.kind&&s.id===ref.id)):[...selected,ref];paint();} |
| m08-p06 | populated | m08-p06 | 共同照片 · 照片 · 2026-10-04 | 可用 | ()=>{selected=has?selected.filter(s=>!(s.kind===ref.kind&&s.id===ref.id)):[...selected,ref];paint();} |
| m08-p06 | populated | m08-p06 | 共同重要时刻 · 时刻 · 2026-10-04 | 可用 | ()=>{selected=has?selected.filter(s=>!(s.kind===ref.kind&&s.id===ref.id)):[...selected,ref];paint();} |
| m08-p06 | populated | m08-p06 | 实际工坊作品 · 工坊 · 2026-10-05 | 可用 | ()=>{selected=has?selected.filter(s=>!(s.kind===ref.kind&&s.id===ref.id)):[...selected,ref];paint();} |
| m08-p06 | populated | m08-p06 | 实际成长故事 · 宠物 · 2026-10-04 | 可用 | ()=>{selected=has?selected.filter(s=>!(s.kind===ref.kind&&s.id===ref.id)):[...selected,ref];paint();} |
| m08-p06 | populated | m08-p06 | 开始编排 | 可用 | ()=>{if(!selected.length){UI.toast('请至少选择一份共同素材','error');return;}UI.busy(q('.next'),'保存选择…',()=>{if(selected.some(v=>!B.source(v,book())))throw new Error('部分素材已不可见，请重新选择');if(!B.change(id,value=>{value.selected=selected;value.skipped=[];},'book-select'))return false;guard.commit();return go(7);});} |
| m08-p07 | empty | m08-p07 | 返回素材选择 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p07 | empty | m08-p07 | 暂不放入 | 隐藏/禁用 | location.href='m08-p06.html' |
| m08-p07 | empty | m08-p07 | 放入回忆册 | 隐藏/禁用 | location.href='m08-p08.html' |
| m08-p07 | empty | m08-p07 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p07 | populated | m08-p13 | 返回编排 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p07 | populated | m08-p13 | 01初遇的心动 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p07 | populated | m08-p13 | 02一起看日落 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p07 | populated | m08-p13 | 03记录小美好 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p07 | populated | m08-p13 | 01夏夜的摩天轮 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p07 | populated | m08-p13 | 02烟花下的约定 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p07 | populated | m08-p13 | 03星空下的悄悄话 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p07 | populated | m08-p13 | 新增章节 | 可用 | ()=>edit('章节','章节名','',name=>{chapters.push({id:'chapter-'+crypto.randomUUID(),name});paint();return true;}) |
| m08-p07 | populated | m08-p13 | 保存排列 | 可用 | ()=>UI.busy(document.querySelector('.save'),'保存排列…',()=>{if(!B.structure(id,chapters,pages,current.updatedAt))return false;guard.commit();return go(14);}) |
| m08-p07 | populated | m08-p13 | 章节操作「第一章」 | 可用 | ()=>chapterMenu(chapter) |
| m08-p07 | populated | m08-p13 | 共同日记 | 可用 | ()=>go(PrototypeBookEditors.editorPage(page),{page:page.id}) |
| m08-p07 | populated | m08-p13 | 页面操作「共同日记」 | 可用 | ()=>pageMenu(page) |
| m08-p07 | populated | m08-p13 | 添加书页 | 可用 | ()=>go(8) |
| m08-p08 | empty | m08-p08 | 返回素材预览 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p08 | empty | m08-p08 | 2024.04.21　周日今天一起去了海边，风很温柔，你在笑，我也觉得整个世界都亮了起来。日记摘录 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p08 | empty | m08-p08 | 那天的晚霞好美呀～照片故事 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p08 | empty | m08-p08 | 我们的重要时刻2023.05.20第一次约会2023.08.10一起旅行2024.02.14确定关系重要时刻 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p08 | empty | m08-p08 | 一起完成的小作品工坊作品 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p08 | empty | m08-p08 | 小家伙的成长日记2个月　　 6个月　　 1岁宠物成长 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p08 | empty | m08-p08 | · 第三章 ·平凡的日子也闪闪发光章节扉页 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p08 | empty | m08-p08 | 使用这个模板 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p08 | empty | m08-p08 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p08 | populated | m08-p08 | 返回素材预览 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p08 | populated | m08-p08 | 2024.04.21　周日 今天一起去了海边， 风很温柔，你在笑， 我也觉得整个世界 都亮了起来。 日记摘录 | 可用 | ()=>{template=e.dataset.template;all('.templates button').forEach(x=>x.setAttribute('aria-pressed',String(x===e)));} |
| m08-p08 | populated | m08-p08 | 那天的晚霞 好美呀～ 照片故事 | 可用 | ()=>{template=e.dataset.template;all('.templates button').forEach(x=>x.setAttribute('aria-pressed',String(x===e)));} |
| m08-p08 | populated | m08-p08 | 我们的重要时刻 2023.05.20 第一次约会 2023.08.10 一起旅行 2024.02.14 确定关系 重要时刻 | 可用 | ()=>{template=e.dataset.template;all('.templates button').forEach(x=>x.setAttribute('aria-pressed',String(x===e)));} |
| m08-p08 | populated | m08-p08 | 一起完成的小作品 工坊作品 | 可用 | ()=>{template=e.dataset.template;all('.templates button').forEach(x=>x.setAttribute('aria-pressed',String(x===e)));} |
| m08-p08 | populated | m08-p08 | 小家伙的成长日记 2个月　　 6个月　　 1岁 宠物成长 | 可用 | ()=>{template=e.dataset.template;all('.templates button').forEach(x=>x.setAttribute('aria-pressed',String(x===e)));} |
| m08-p08 | populated | m08-p08 | · 第三章 · 平凡的日子 也闪闪发光 章节扉页 | 可用 | ()=>{template=e.dataset.template;all('.templates button').forEach(x=>x.setAttribute('aria-pressed',String(x===e)));} |
| m08-p08 | populated | m08-p08 | 使用这个模板 | 可用 | ()=>{const page={source:params.get('source')／／current.selected[0]?.id,kind:params.get('kind')／／current.selected[0]?.kind,template,page:params.get('page')／／'',draft:params.get('draft')／／''};if(template==='章节扉页')return edit('章节','章节名','',name=>B.change(id,b=>b.chapters.push({id:'chapter-'+crypto.randomUUID(),name}),'book-chapter'),()=>go(13));return go(template==='日记摘录'?9:template==='照片故事'?10:template==='重要时刻'?11:12,page);} |
| m08-p09 | empty | m08-p09 | 返回版式选择 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p09 | empty | m08-p09 | page-title | 隐藏/禁用 | 原生输入/选择器 |
| m08-p09 | empty | m08-p09 | 天边被晚霞染成了温柔的橘粉色， 我们并肩走着，风也轻轻地。 | 隐藏/禁用 | 原生输入/选择器 |
| m08-p09 | empty | m08-p09 | date | 隐藏/禁用 | 原生输入/选择器 |
| m08-p09 | empty | m08-p09 | message | 隐藏/禁用 | 原生输入/选择器 |
| m08-p09 | empty | m08-p09 | 换摘录换一段日记 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p09 | empty | m08-p09 | 换照片换一张照片 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p09 | empty | m08-p09 | 换版式换一种排版 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p09 | empty | m08-p09 | 完成这一页 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p09 | empty | m08-p09 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p09 | populated | m08-p09 | 返回版式选择 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p09 | populated | m08-p09 | 书页标题 | 可用 | 原生输入/选择器 |
| m08-p09 | populated | m08-p09 | 日记摘录 | 可用 | 原生输入/选择器 |
| m08-p09 | populated | m08-p09 | 书页日期 | 可用 | 原生输入/选择器 |
| m08-p09 | populated | m08-p09 | 书页寄语 | 可用 | 原生输入/选择器 |
| m08-p09 | populated | m08-p09 | 换摘录 换一段日记 | 可用 | ()=>sourceChoice('diary',v=>{reference=v;const src=B.source(v,book());inputs.body.value=src.body;inputs.title.value=src.title;inputs.date.value=src.date;['body','title','date'].forEach(k=>{edited.delete(k);delete draft[k];});}) |
| m08-p09 | populated | m08-p09 | 换照片 换一张照片 | 可用 | ()=>sourceChoice('photo',v=>{draft.photoSource=v;UI.toast('已选择共同照片，完成这一页后保存');}) |
| m08-p09 | populated | m08-p09 | 换版式 换一种排版 | 可用 | ()=>session.stash(capture(),guard) |
| m08-p09 | populated | m08-p09 | 完成这一页 | 可用 | ()=>{if(!UI.fieldError(inputs.title,inputs.title.value.trim()?'':'请填写书页标题'))return;UI.busy(q('.done'),'保存这一页…',()=>{if(!session.save(capture(true)))return false;guard.commit();return go(13);});} |
| m08-p10 | empty | m08-p10 | 返回 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p10 | empty | m08-p10 | 预览 | 隐藏/禁用 | location.href='m08-p13.html' |
| m08-p10 | empty | m08-p10 | 书页标题 | 隐藏/禁用 | 原生输入/选择器 |
| m08-p10 | empty | m08-p10 | 书页日期 | 隐藏/禁用 | 原生输入/选择器 |
| m08-p10 | empty | m08-p10 | 裁剪/替换 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p10 | empty | m08-p10 | 裁剪/替换 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p10 | empty | m08-p10 | 裁剪/替换 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p10 | empty | m08-p10 | 这一页的想法 | 隐藏/禁用 | 原生输入/选择器 |
| m08-p10 | empty | m08-p10 | 完成这一页 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p10 | empty | m08-p10 | 添加照片 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p10 | empty | m08-p10 | 添加文字 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p10 | empty | m08-p10 | 添加贴纸 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p10 | empty | m08-p10 | 更换模板 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p10 | empty | m08-p10 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p10 | populated | m08-p10 | 返回 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p10 | populated | m08-p10 | 预览 | 可用 | ()=>UI.modal({title:fields.title.value／／'照片故事预览',message:fields.body.value,content:(()=>{const container=document.createElement('div');container.className='book-reading-images';for(const item of draft.photos){const box=document.createElement('div');box.className='book-photo-frame';frame(box,B.source(item.source,book())?.image,item.crop);container.append(box);}return container;})(),confirm:'继续编辑'}) |
| m08-p10 | populated | m08-p10 | 书页标题 | 可用 | 原生输入/选择器 |
| m08-p10 | populated | m08-p10 | 书页日期 | 可用 | 原生输入/选择器 |
| m08-p10 | populated | m08-p10 | 裁剪/替换 | 可用 | async()=>{if(!draft.photos[index])return choosePhoto(index);const choice=await UI.sheet({title:'照片'+(index+1),actions:[{label:'替换这张照片',value:'replace'},{label:'裁剪这张照片',value:'crop'},{label:'移除这张照片',value:'remove',danger:true}]});if(choice==='replace')choosePhoto(index);if(choice==='crop')cropPhoto(ctx,draft,index,paint);if(choice==='remove'){draft.photos.splice(index,1);paint();}} |
| m08-p10 | populated | m08-p10 | 裁剪/替换 | 可用 | async()=>{if(!draft.photos[index])return choosePhoto(index);const choice=await UI.sheet({title:'照片'+(index+1),actions:[{label:'替换这张照片',value:'replace'},{label:'裁剪这张照片',value:'crop'},{label:'移除这张照片',value:'remove',danger:true}]});if(choice==='replace')choosePhoto(index);if(choice==='crop')cropPhoto(ctx,draft,index,paint);if(choice==='remove'){draft.photos.splice(index,1);paint();}} |
| m08-p10 | populated | m08-p10 | 裁剪/替换 | 可用 | async()=>{if(!draft.photos[index])return choosePhoto(index);const choice=await UI.sheet({title:'照片'+(index+1),actions:[{label:'替换这张照片',value:'replace'},{label:'裁剪这张照片',value:'crop'},{label:'移除这张照片',value:'remove',danger:true}]});if(choice==='replace')choosePhoto(index);if(choice==='crop')cropPhoto(ctx,draft,index,paint);if(choice==='remove'){draft.photos.splice(index,1);paint();}} |
| m08-p10 | populated | m08-p10 | 这一页的想法 | 可用 | 原生输入/选择器 |
| m08-p10 | populated | m08-p10 | 完成这一页 | 可用 | ()=>{let valid=true;for(const [key,e]of Object.entries(fields)){const error=key==='title'&&!e.value.trim()?'请填写书页标题':key==='date'&&!D.parse(e.value)?'请填写有效YYYY-MM-DD日期':'';if(!UI.fieldError(e,error))valid=false;}if(!valid)return;UI.busy(q('.done'),'保存这一页…',()=>{if(n===11&&draft.source?.kind!=='moment')throw new Error('请先选择共同重要时刻');if(n===12&&!['work','pet'].includes(draft.source?.kind))throw new Error('请先选择实际工坊作品或宠物成长');const saved=session.save(capture(true));if(!saved)return false;guard.commit();return go(13);});} |
| m08-p10 | populated | m08-p10 | 添加照片 | 可用 | async()=>{if(b.dataset.tool==='添加照片'){if(draft.photos.length>=3){UI.toast('这一页最多三张照片','info');return;}choosePhoto();}if(b.dataset.tool==='添加文字')fields.body.focus();if(b.dataset.tool==='添加贴纸'){if(draft.stickers.length>=8){UI.toast('这一页最多八个贴纸','info');return;}const sticker=await UI.sheet({title:'选择贴纸',actions:['💗','⭐','🌸','😊'].map(v=>({label:v,value:v}))});if(sticker){draft.stickers.push(sticker);paint();}}if(b.dataset.tool==='更换模板')session.stash(capture(),guard);} |
| m08-p10 | populated | m08-p10 | 添加文字 | 可用 | async()=>{if(b.dataset.tool==='添加照片'){if(draft.photos.length>=3){UI.toast('这一页最多三张照片','info');return;}choosePhoto();}if(b.dataset.tool==='添加文字')fields.body.focus();if(b.dataset.tool==='添加贴纸'){if(draft.stickers.length>=8){UI.toast('这一页最多八个贴纸','info');return;}const sticker=await UI.sheet({title:'选择贴纸',actions:['💗','⭐','🌸','😊'].map(v=>({label:v,value:v}))});if(sticker){draft.stickers.push(sticker);paint();}}if(b.dataset.tool==='更换模板')session.stash(capture(),guard);} |
| m08-p10 | populated | m08-p10 | 添加贴纸 | 可用 | async()=>{if(b.dataset.tool==='添加照片'){if(draft.photos.length>=3){UI.toast('这一页最多三张照片','info');return;}choosePhoto();}if(b.dataset.tool==='添加文字')fields.body.focus();if(b.dataset.tool==='添加贴纸'){if(draft.stickers.length>=8){UI.toast('这一页最多八个贴纸','info');return;}const sticker=await UI.sheet({title:'选择贴纸',actions:['💗','⭐','🌸','😊'].map(v=>({label:v,value:v}))});if(sticker){draft.stickers.push(sticker);paint();}}if(b.dataset.tool==='更换模板')session.stash(capture(),guard);} |
| m08-p10 | populated | m08-p10 | 保留草稿换模板 | 可用 | async()=>{if(b.dataset.tool==='添加照片'){if(draft.photos.length>=3){UI.toast('这一页最多三张照片','info');return;}choosePhoto();}if(b.dataset.tool==='添加文字')fields.body.focus();if(b.dataset.tool==='添加贴纸'){if(draft.stickers.length>=8){UI.toast('这一页最多八个贴纸','info');return;}const sticker=await UI.sheet({title:'选择贴纸',actions:['💗','⭐','🌸','😊'].map(v=>({label:v,value:v}))});if(sticker){draft.stickers.push(sticker);paint();}}if(b.dataset.tool==='更换模板')session.stash(capture(),guard);} |
| m08-p11 | empty | m08-p11 | 返回版式选择 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p11 | empty | m08-p11 | 时刻主题 | 隐藏/禁用 | 原生输入/选择器 |
| m08-p11 | empty | m08-p11 | 日期 | 隐藏/禁用 | 原生输入/选择器 |
| m08-p11 | empty | m08-p11 | 更换照片 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p11 | empty | m08-p11 | 选择时刻 › | 隐藏/禁用 | 委托候选/待复核 |
| m08-p11 | empty | m08-p11 | 添加一句话 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p11 | empty | m08-p11 | 完成这一页 ♡ | 隐藏/禁用 | 委托候选/待复核 |
| m08-p11 | empty | m08-p11 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p11 | populated | m08-p11 | 返回版式选择 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p11 | populated | m08-p11 | 书页标题 | 可用 | 原生输入/选择器 |
| m08-p11 | populated | m08-p11 | 书页日期 | 可用 | 原生输入/选择器 |
| m08-p11 | populated | m08-p11 | 更换照片 | 可用 | ()=>sourceChoice('photo',ref=>{draft.photoSource=ref;paint();}) |
| m08-p11 | populated | m08-p11 | 选择时刻 › | 可用 | ()=>sourceChoice('moment',ref=>{draft.source=ref;const source=B.source(ref,book());fields.title.value=source.title;fields.date.value=source.date;edited.delete('title');edited.delete('date');delete draft.title;delete draft.date;text('.selected',source.title);paint();}) |
| m08-p11 | populated | m08-p11 | 添加一句话 | 可用 | ()=>edit('一句话','书页寄语',draft.message／／'',value=>{draft.message=value;text('#quote',value);return true;}) |
| m08-p11 | populated | m08-p11 | 完成这一页 ♡ | 可用 | ()=>{let valid=true;for(const [key,e]of Object.entries(fields)){const error=key==='title'&&!e.value.trim()?'请填写书页标题':key==='date'&&!D.parse(e.value)?'请填写有效YYYY-MM-DD日期':'';if(!UI.fieldError(e,error))valid=false;}if(!valid)return;UI.busy(q('.done'),'保存这一页…',()=>{if(n===11&&draft.source?.kind!=='moment')throw new Error('请先选择共同重要时刻');if(n===12&&!['work','pet'].includes(draft.source?.kind))throw new Error('请先选择实际工坊作品或宠物成长');const saved=session.save(capture(true));if(!saved)return false;guard.commit();return go(13);});} |
| m08-p11 | populated | m08-p11 | 保留草稿换模板 | 可用 | ()=>session.stash(capture(),guard) |
| m08-p12 | empty | m08-p12 | 返回版式选择 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p12 | empty | m08-p12 | 工坊作品 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p12 | empty | m08-p12 | 宠物成长 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p12 | empty | m08-p12 | 成长说明 | 隐藏/禁用 | 原生输入/选择器 |
| m08-p12 | empty | m08-p12 | 换内容 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p12 | empty | m08-p12 | 换照片 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p12 | empty | m08-p12 | 添加说明 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p12 | empty | m08-p12 | 完成这一页 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p12 | empty | m08-p12 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p12 | populated | m08-p12 | 返回版式选择 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p12 | populated | m08-p12 | 工坊作品 | 可用 | ()=>{const next=b.dataset.tab==='工坊作品'?'work':'pet';if(next===kind)return;sourceChoice(next,ref=>{kind=next;draft.source=ref;draft.template=kind==='work'?'工坊作品':'宠物成长';paint();});} |
| m08-p12 | populated | m08-p12 | 宠物成长 | 可用 | ()=>{const next=b.dataset.tab==='工坊作品'?'work':'pet';if(next===kind)return;sourceChoice(next,ref=>{kind=next;draft.source=ref;draft.template=kind==='work'?'工坊作品':'宠物成长';paint();});} |
| m08-p12 | populated | m08-p12 | 成长说明 | 可用 | 原生输入/选择器 |
| m08-p12 | populated | m08-p12 | 换内容 | 可用 | ()=>{if(b.dataset.action==='添加说明')fields.body.focus();if(b.dataset.action==='换内容')sourceChoice(kind,ref=>{draft.source=ref;paint();});if(b.dataset.action==='换照片')sourceChoice('photo',ref=>{draft.photoSource=ref;paint();});} |
| m08-p12 | populated | m08-p12 | 换照片 | 可用 | ()=>{if(b.dataset.action==='添加说明')fields.body.focus();if(b.dataset.action==='换内容')sourceChoice(kind,ref=>{draft.source=ref;paint();});if(b.dataset.action==='换照片')sourceChoice('photo',ref=>{draft.photoSource=ref;paint();});} |
| m08-p12 | populated | m08-p12 | 添加说明 | 可用 | ()=>{if(b.dataset.action==='添加说明')fields.body.focus();if(b.dataset.action==='换内容')sourceChoice(kind,ref=>{draft.source=ref;paint();});if(b.dataset.action==='换照片')sourceChoice('photo',ref=>{draft.photoSource=ref;paint();});} |
| m08-p12 | populated | m08-p12 | 完成这一页 | 可用 | ()=>{let valid=true;for(const [key,e]of Object.entries(fields)){const error=key==='title'&&!e.value.trim()?'请填写书页标题':key==='date'&&!D.parse(e.value)?'请填写有效YYYY-MM-DD日期':'';if(!UI.fieldError(e,error))valid=false;}if(!valid)return;UI.busy(q('.done'),'保存这一页…',()=>{if(n===11&&draft.source?.kind!=='moment')throw new Error('请先选择共同重要时刻');if(n===12&&!['work','pet'].includes(draft.source?.kind))throw new Error('请先选择实际工坊作品或宠物成长');const saved=session.save(capture(true));if(!saved)return false;guard.commit();return go(13);});} |
| m08-p12 | populated | m08-p12 | 保留草稿换模板 | 可用 | ()=>session.stash(capture(),guard) |
| m08-p13 | empty | m08-p13 | 返回编排 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p13 | empty | m08-p13 | 01初遇的心动 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | empty | m08-p13 | 02一起看日落 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | empty | m08-p13 | 03记录小美好 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | empty | m08-p13 | 01夏夜的摩天轮 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | empty | m08-p13 | 02烟花下的约定 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | empty | m08-p13 | 03星空下的悄悄话 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | empty | m08-p13 | 新增章节 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | empty | m08-p13 | 保存排列 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | empty | m08-p13 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p13 | populated | m08-p13 | 返回编排 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p13 | populated | m08-p13 | 01初遇的心动 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | populated | m08-p13 | 02一起看日落 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | populated | m08-p13 | 03记录小美好 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | populated | m08-p13 | 01夏夜的摩天轮 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | populated | m08-p13 | 02烟花下的约定 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | populated | m08-p13 | 03星空下的悄悄话 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p13 | populated | m08-p13 | 新增章节 | 可用 | ()=>edit('章节','章节名','',name=>{chapters.push({id:'chapter-'+crypto.randomUUID(),name});paint();return true;}) |
| m08-p13 | populated | m08-p13 | 保存排列 | 可用 | ()=>UI.busy(document.querySelector('.save'),'保存排列…',()=>{if(!B.structure(id,chapters,pages,current.updatedAt))return false;guard.commit();return go(14);}) |
| m08-p13 | populated | m08-p13 | 章节操作「第一章」 | 可用 | ()=>chapterMenu(chapter) |
| m08-p13 | populated | m08-p13 | 共同日记 | 可用 | ()=>go(PrototypeBookEditors.editorPage(page),{page:page.id}) |
| m08-p13 | populated | m08-p13 | 页面操作「共同日记」 | 可用 | ()=>pageMenu(page) |
| m08-p13 | populated | m08-p13 | 添加书页 | 可用 | ()=>go(8) |
| m08-p14 | empty | m08-p14 | 开始翻阅 | 隐藏/禁用 | location.href='m08-p15.html' |
| m08-p14 | empty | m08-p14 | 继续整理 | 隐藏/禁用 | location.href='m08-p13.html' |
| m08-p14 | empty | m08-p14 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p14 | empty | m08-p14 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p14 | populated | m08-p14 | 开始翻阅 | 可用 | ()=>go(15) |
| m08-p14 | populated | m08-p14 | 继续整理 | 可用 | ()=>go(13) |
| m08-p14 | populated | m08-p14 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p15 | empty | m08-p15 | 返回书架 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p15 | empty | m08-p15 | 1. 那天，阳光刚刚好 1 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | empty | m08-p15 | 2. 一起吃的第一支冰淇淋 2 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | empty | m08-p15 | 3. 藏在风里的喜欢 3 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | empty | m08-p15 | 4. 我们的第一张合照 有补页4 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | empty | m08-p15 | 5. 你笑起来真好看 5 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | empty | m08-p15 | 6. 夏天的傍晚，晚风很温柔 6 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | empty | m08-p15 | 7. 海边的日落与你 7 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | empty | m08-p15 | 8. 烟花下许的愿 8 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | empty | m08-p15 | 9. 手牵手，走很长很长的路 9 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | empty | m08-p15 | 10. 属于我们的歌单 10 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | empty | m08-p15 | 11. 一起看过的星星 11 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | empty | m08-p15 | 12. 八月，未完待续 12 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | empty | m08-p15 | 从第 1 页开始 → | 隐藏/禁用 | location.href='m08-p16.html' |
| m08-p15 | empty | m08-p15 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p15 | populated | m08-p15 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p15 | populated | m08-p15 | 1. 那天，阳光刚刚好 1 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | populated | m08-p15 | 2. 一起吃的第一支冰淇淋 2 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | populated | m08-p15 | 3. 藏在风里的喜欢 3 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | populated | m08-p15 | 4. 我们的第一张合照 有补页4 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | populated | m08-p15 | 5. 你笑起来真好看 5 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | populated | m08-p15 | 6. 夏天的傍晚，晚风很温柔 6 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | populated | m08-p15 | 7. 海边的日落与你 7 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | populated | m08-p15 | 8. 烟花下许的愿 8 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | populated | m08-p15 | 9. 手牵手，走很长很长的路 9 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | populated | m08-p15 | 10. 属于我们的歌单 10 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | populated | m08-p15 | 11. 一起看过的星星 11 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | populated | m08-p15 | 12. 八月，未完待续 12 | 隐藏/禁用 | m08-p16.html |
| m08-p15 | populated | m08-p15 | 从第 1 页开始 → | 可用 | ()=>go(16,{page:current.pages[0].id}) |
| m08-p15 | populated | m08-p15 | 管理这本回忆册 | 可用 | ()=>go(21) |
| m08-p15 | populated | m08-p15 | 共同日记 | 可用 | ()=>go(16,{page:page.id}) |
| m08-p16 | empty | m08-p16 | 返回 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p16 | empty | m08-p16 | 目录 | 隐藏/禁用 | location.href='m08-p17.html' |
| m08-p16 | empty | m08-p16 | 书签 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p16 | empty | m08-p16 | 下一页 | 隐藏/禁用 | location.href='m08-p18.html' |
| m08-p16 | empty | m08-p16 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p16 | populated | m08-p16 | 返回 | 可用 | ()=>go(n===20?17:15,{page:page.id}) |
| m08-p16 | populated | m08-p16 | 目录 | 可用 | ()=>go(15) |
| m08-p16 | populated | m08-p16 | 书签 | 可用 | ()=>UI.busy(bookmark,'保存书签…',()=>{const saved=B.bookmark(id,page.id);if(!saved)return false;bookmark.setAttribute('aria-pressed',String(saved.bookmarks.includes(page.id)));UI.toast('书签已更新','success');return true;}) |
| m08-p16 | populated | m08-p16 | 下一页 | 可用 | ()=>index+1<current.pages.length?go(16,{page:current.pages[index+1].id}):UI.toast('已经读到最后一页') |
| m08-p16 | populated | m08-p16 | 查看原始共同记录 | 可用 | ()=>UI.go(view.url) |
| m08-p16 | populated | m08-p16 | 阅读工具 | 可用 | ()=>go(17,{page:page.id}) |
| m08-p17 | empty | m08-p17 | 返回阅读 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p17 | empty | m08-p17 | 目录查看全书目录和章节 | 隐藏/禁用 | location.href='m08-p15.html' |
| m08-p17 | empty | m08-p17 | 书签查看和管理我的书签 | 隐藏/禁用 | location.href='m08-p19.html' |
| m08-p17 | empty | m08-p17 | 添加补页在书中添加新的补充页 | 隐藏/禁用 | location.href='m08-p18.html' |
| m08-p17 | empty | m08-p17 | 整理这本书调整页序、重命名、导出等 | 隐藏/禁用 | location.href='m08-p13.html' |
| m08-p17 | empty | m08-p17 | 更多设置阅读偏好、背景音乐等设置 | 隐藏/禁用 | location.href='m08-p21.html' |
| m08-p17 | empty | m08-p17 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p17 | populated | m08-p17 | 返回阅读 | 可用 | ()=>UI.back('m08-p16.html?id='+id+'&page='+encodeURIComponent(page.id)) |
| m08-p17 | populated | m08-p17 | 目录 查看全书目录和章节 | 可用 | ()=>go(15) |
| m08-p17 | populated | m08-p17 | 书签 查看和管理我的书签 | 可用 | async()=>{const bookmarks=book().bookmarks／／[],pages=book().pages.filter(v=>bookmarks.includes(v.id));const selected=await UI.sheet({title:'我的书签',message:pages.length?'选择一页继续阅读。':'还没有书签，可在阅读页面点击书签。',actions:pages.map(v=>({label:B.pageView(v,book()).title,value:v.id}))});if(selected)go(16,{page:selected});} |
| m08-p17 | populated | m08-p17 | 添加补页 在书中添加新的补充页 | 可用 | ()=>go(18,{page:page.id}) |
| m08-p17 | populated | m08-p17 | 整理这本书 调整页序、重命名、导出等 | 可用 | ()=>go(13) |
| m08-p17 | populated | m08-p17 | 管理这本书 · 书名、归档、导出与删除 | 可用 | ()=>go(21) |
| m08-p18 | empty | m08-p18 | 返回阅读 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p18 | empty | m08-p18 | 回到目录 | 隐藏/禁用 | location.href='m08-p15.html' |
| m08-p18 | empty | m08-p18 | 写几句话记录此刻的想法与心情 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p18 | empty | m08-p18 | 送一个表情用一个表情传达你的心意 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p18 | empty | m08-p18 | 附上一张照片用一张照片定格这份回忆 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p18 | empty | m08-p18 | 选择回应方式 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p18 | empty | m08-p18 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p18 | populated | m08-p18 | 返回阅读 | 可用 | ()=>UI.back('m08-p16.html?id='+id+'&page='+encodeURIComponent(page.id)) |
| m08-p18 | populated | m08-p18 | 回到目录 | 可用 | ()=>go(15) |
| m08-p18 | populated | m08-p18 | 写几句话 记录此刻的想法与心情 | 可用 | ()=>{kind=b.dataset.kind;all('.choices button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m08-p18 | populated | m08-p18 | 送一个表情 用一个表情传达你的心意 | 可用 | ()=>{kind=b.dataset.kind;all('.choices button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m08-p18 | populated | m08-p18 | 附上一张照片 用一张照片定格这份回忆 | 可用 | ()=>{kind=b.dataset.kind;all('.choices button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));} |
| m08-p18 | populated | m08-p18 | 选择回应方式 | 可用 | ()=>go(19,{page:page.id,kind}) |
| m08-p19 | empty | m08-p19 | 返回补页选择 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p19 | empty | m08-p19 | 补页文字 | 隐藏/禁用 | 原生输入/选择器 |
| m08-p19 | empty | m08-p19 | 爱心 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p19 | empty | m08-p19 | 星星 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p19 | empty | m08-p19 | 微笑 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p19 | empty | m08-p19 | 花朵 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p19 | empty | m08-p19 | INPUT | 隐藏/禁用 | 原生输入/选择器 |
| m08-p19 | empty | m08-p19 | 放进回忆书 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p19 | empty | m08-p19 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p19 | populated | m08-p19 | 返回补页选择 | 可用 | ()=>UI.back('m08-p16.html?id='+id+'&page='+encodeURIComponent(page.id)) |
| m08-p19 | populated | m08-p19 | 补页文字 | 可用 | 原生输入/选择器 |
| m08-p19 | populated | m08-p19 | 爱心 | 可用 | ()=>{emoji=b.dataset.emoji;all('.emojis button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));q('.emoji-preview').textContent=emoji;} |
| m08-p19 | populated | m08-p19 | 星星 | 可用 | ()=>{emoji=b.dataset.emoji;all('.emojis button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));q('.emoji-preview').textContent=emoji;} |
| m08-p19 | populated | m08-p19 | 微笑 | 可用 | ()=>{emoji=b.dataset.emoji;all('.emojis button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));q('.emoji-preview').textContent=emoji;} |
| m08-p19 | populated | m08-p19 | 花朵 | 可用 | ()=>{emoji=b.dataset.emoji;all('.emojis button').forEach(e=>e.setAttribute('aria-pressed',String(e===b)));q('.emoji-preview').textContent=emoji;} |
| m08-p19 | populated | m08-p19 | INPUT | 可用 | async()=>{if(!file.files.length)return;reading=true;q('.submit').disabled=true;text('.photo-label','正在打开照片…');try{image=await R.readImage(file.files[0],'book-image');preview.hidden=false;frame(preview,image);text('.photo-label','♥ 已附上照片 ♥');}catch(e){image=null;preview.hidden=true;file.value='';text('.photo-label','照片未读取，点击重新选择');UI.toast(e.message,'error');}finally{reading=false;q('.submit').disabled=view.blocked／／!PrototypePreferences.privacy().replies;}} |
| m08-p19 | populated | m08-p19 | 放进回忆书 | 可用 | ()=>{if(reading)return;if(kind==='写几句话'&&!UI.fieldError(input,input.value.trim()?'':'请写下补页文字'))return;UI.busy(q('.submit'),'放入回忆书…',()=>{if(!B.supplement(id,page.id,{kind,text:input.value.trim(),emoji,image}))return false;guard.commit();return go(20,{page:page.id});});} |
| m08-p20 | empty | m08-p20 | 返回阅读工具 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p20 | empty | m08-p20 | 目录 | 隐藏/禁用 | location.href='m08-p15.html' |
| m08-p20 | empty | m08-p20 | 书签 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p20 | empty | m08-p20 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p20 | populated | m08-p20 | 返回阅读工具 | 可用 | ()=>go(n===20?17:15,{page:page.id}) |
| m08-p20 | populated | m08-p20 | 目录 | 可用 | ()=>go(15) |
| m08-p20 | populated | m08-p20 | 书签 | 可用 | ()=>UI.busy(bookmark,'保存书签…',()=>{const saved=B.bookmark(id,page.id);if(!saved)return false;bookmark.setAttribute('aria-pressed',String(saved.bookmarks.includes(page.id)));UI.toast('书签已更新','success');return true;}) |
| m08-p20 | populated | m08-p20 | 查看原始共同记录 | 可用 | ()=>UI.go(view.url) |
| m08-p20 | populated | m08-p20 | 阅读工具 | 可用 | ()=>go(17,{page:page.id}) |
| m08-p21 | empty | m08-p21 | 返回阅读 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p21 | empty | m08-p21 | 修改书名与封面 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p21 | empty | m08-p21 | 整理页序 | 隐藏/禁用 | location.href='m08-p13.html' |
| m08-p21 | empty | m08-p21 | 归档回忆册 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p21 | empty | m08-p21 | 删除这本回忆册 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p21 | empty | m08-p21 | 取消 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p21 | empty | m08-p21 | 确认删除 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p21 | empty | m08-p21 | 返回书架 | 可用 | ()=>go(1,{},null) |
| m08-p21 | populated | m08-p21 | 返回阅读 | 可用 | ()=>UI.back('m08-p'+String(page).padStart(2,'0')+'.html'+(id?'?id='+encodeURIComponent(id):'')) |
| m08-p21 | populated | m08-p21 | 修改书名 | 可用 | ()=>edit('书名','回忆册名称',book().name,name=>B.change(id,b=>b.name=name,'book-rename'),()=>{text('.book-name',book().name);text('.cover-title',book().name);PrototypeBookEditors.cover(cover,book());}) |
| m08-p21 | populated | m08-p21 | 整理页序 | 可用 | ()=>go(13) |
| m08-p21 | populated | m08-p21 | 修改主题与封面 | 可用 | ()=>go(5,{origin:'manage'}) |
| m08-p21 | populated | m08-p21 | 归档回忆册 | 可用 | ()=>UI.busy(q('.archive'),'更新归档…',()=>{const value=B.change(id,b=>b.archived=!b.archived,'book-archive');if(!value)return false;UI.toast(value.archived?'已归档':'已恢复到书架','success');return true;}).then(()=>text('.archive',book().archived?'取消归档回忆册':'归档回忆册')) |
| m08-p21 | populated | m08-p21 | 删除这本回忆册 | 可用 | async()=>{if(!await UI.modal({title:'确定删除《'+book().name+'》？',message:'删除后无法恢复；原始共同记录不会删除。',confirm:'确认删除',cancel:'取消'}))return;UI.busy(q('.show-delete'),'删除中…',()=>{if(!B.remove(id))return false;UI.toast('已删除','success');return go(1,{},null);});} |
| m08-p21 | populated | m08-p21 | 取消 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p21 | populated | m08-p21 | 确认删除 | 隐藏/禁用 | 委托候选/待复核 |
| m08-p21 | populated | m08-p21 | 导出这本回忆册 | 可用 | ()=>UI.busy(q('.book-extra'),'导出中…',()=>{B.download(id);UI.toast('已导出','success');return true;}) |
