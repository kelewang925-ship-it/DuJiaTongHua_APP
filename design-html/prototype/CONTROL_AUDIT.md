# 全量控件行为审计基线

基于全部页面源代码和隔离浏览器注册事件观察生成。每项列出已观察的绑定及处理代码；存在绑定不等于业务流程已闭环。所有项仍需要真实点击/输入流程验收。

| 页面 | 序号 | 名称 | 当前行为类型 | 已绑定处理 | 待验证 |
| --- | ---: | --- | --- | --- | --- |
| m01-p01 | 1 | 登录并开始 | 页面跳转 | location.href='m01-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m01-p01 | 2 | 创建账号 | 页面跳转 | location.href='m01-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m01-p02 | 1 | 返回 | 函数调用/需核对上下文 | history.back(); | 跨页数据/返回/异常/触发条件 |
| m01-p02 | 2 | 手机号 | 输入/键盘、提示反馈 | event=>{event.preventDefault();show('这是设计稿 HTML 演示，未连接登录接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p02 | 3 | password | 输入/键盘、提示反馈 | event=>{event.preventDefault();show('这是设计稿 HTML 演示，未连接登录接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p02 | 4 | 显示密码 | 状态/内容变化 | ; ()=>{const input=document.querySelector('#password');input.type=input.type==='password'?'text':'password';document.querySelector('#eye').setAttribute('aria-label',input.type==='password'?'显示密码':'隐藏密码')} | 跨页数据/返回/异常/触发条件 |
| m01-p02 | 5 | 忘记密码？ | 提示反馈 | ; event=>{event.preventDefault();show(item.dataset.message)} | 跨页数据/返回/异常/触发条件 |
| m01-p02 | 6 | 登录并回到故事里 | 提示反馈 | ; ; event=>{event.preventDefault();show('这是设计稿 HTML 演示，未连接登录接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p02 | 7 | 创建账号 | 提示反馈 | ; event=>{event.preventDefault();show(item.dataset.message)} | 跨页数据/返回/异常/触发条件 |
| m01-p02 | 8 | 《用户协议》 | 提示反馈 | ; event=>{event.preventDefault();show(item.dataset.message)} | 跨页数据/返回/异常/触发条件 |
| m01-p02 | 9 | 《隐私政策》 | 提示反馈 | ; event=>{event.preventDefault();show(item.dataset.message)} | 跨页数据/返回/异常/触发条件 |
| m01-p03 | 1 | 返回欢迎页 | 页面跳转 | location.href='m01-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m01-p03 | 2 | 昵称 | 输入/键盘、提示反馈 | event=>{event.preventDefault();show('这是设计稿演示，暂未连接注册接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p03 | 3 | 手机号 | 输入/键盘、提示反馈 | event=>{event.preventDefault();show('这是设计稿演示，暂未连接注册接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p03 | 4 | 验证码 | 输入/键盘、提示反馈 | event=>{event.preventDefault();show('这是设计稿演示，暂未连接注册接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p03 | 5 | 获取验证码 | 提示反馈 | ; ()=>show('这是设计稿演示，暂未发送验证码。') | 跨页数据/返回/异常/触发条件 |
| m01-p03 | 6 | 登录密码 | 输入/键盘、提示反馈 | event=>{event.preventDefault();show('这是设计稿演示，暂未连接注册接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p03 | 7 | 显示密码 | 状态/内容变化 | ; ()=>{const field=document.querySelector('#password');field.type=field.type==='password'?'text':'password';document.querySelector('#eye').setAttribute('aria-label',field.type==='password'?'显示密码':'隐藏密码')} | 跨页数据/返回/异常/触发条件 |
| m01-p03 | 8 | INPUT | 勾选/切换、提示反馈 | event=>{event.preventDefault();show('这是设计稿演示，暂未连接注册接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p03 | 9 | 《用户协议》 | 提示反馈 | event=>{event.preventDefault();show('这是设计稿演示，暂未连接注册接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p03 | 10 | 《隐私政策》 | 提示反馈 | event=>{event.preventDefault();show('这是设计稿演示，暂未连接注册接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p03 | 11 | 创建账号 | 提示反馈 | ; ; event=>{event.preventDefault();show('这是设计稿演示，暂未连接注册接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p03 | 12 | 去登录 | 页面跳转、提示反馈 | event=>{event.preventDefault();show('这是设计稿演示，暂未连接注册接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p04 | 1 | 返回 | 页面跳转 | location.href='m01-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m01-p04 | 2 | 手机号 | 输入/键盘、页面跳转 | event=>{event.preventDefault();location.href='m01-p05.html'} | 跨页数据/返回/异常/触发条件 |
| m01-p04 | 3 | 验证码 | 输入/键盘、页面跳转 | event=>{event.preventDefault();location.href='m01-p05.html'} | 跨页数据/返回/异常/触发条件 |
| m01-p04 | 4 | 获取验证码 | 提示反馈 | ; ()=>show('这是设计稿演示，暂未发送验证码。') | 跨页数据/返回/异常/触发条件 |
| m01-p04 | 5 | 下一步 | 页面跳转 | ; ; event=>{event.preventDefault();location.href='m01-p05.html'} | 跨页数据/返回/异常/触发条件 |
| m01-p04 | 6 | 返回登录 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m01-p05 | 1 | 返回找回密码 | 页面跳转 | location.href='m01-p04.html'; | 跨页数据/返回/异常/触发条件 |
| m01-p05 | 2 | 输入新密码 | 输入/键盘、状态/内容变化、提示反馈 | event=>{event.preventDefault();const p=document.querySelector('#password').value,c=document.querySelector('#confirm').value;if(p!==c){show('两次输入的密码不一致');return}if(!/[A-Za-z]/.test(p)／／!/[0-9]/.test(p)){show('密码需要包含字母和数字');return}show('这是设计稿演示，暂未连接密码重置接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p05 | 3 | 显示新密码 | 状态/内容变化 | ; ()=>{const input=document.getElementById(button.dataset.target);input.type=input.type==='password'?'text':'password';button.setAttribute('aria-label',input.type==='password'?'显示密码':'隐藏密码')} | 跨页数据/返回/异常/触发条件 |
| m01-p05 | 4 | 再次输入新密码 | 输入/键盘、状态/内容变化、提示反馈 | event=>{event.preventDefault();const p=document.querySelector('#password').value,c=document.querySelector('#confirm').value;if(p!==c){show('两次输入的密码不一致');return}if(!/[A-Za-z]/.test(p)／／!/[0-9]/.test(p)){show('密码需要包含字母和数字');return}show('这是设计稿演示，暂未连接密码重置接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p05 | 5 | 显示确认密码 | 状态/内容变化 | ; ()=>{const input=document.getElementById(button.dataset.target);input.type=input.type==='password'?'text':'password';button.setAttribute('aria-label',input.type==='password'?'显示密码':'隐藏密码')} | 跨页数据/返回/异常/触发条件 |
| m01-p05 | 6 | 确认并重置 | 状态/内容变化、提示反馈 | ; ; event=>{event.preventDefault();const p=document.querySelector('#password').value,c=document.querySelector('#confirm').value;if(p!==c){show('两次输入的密码不一致');return}if(!/[A-Za-z]/.test(p)／／!/[0-9]/.test(p)){show('密码需要包含字母和数字');return}show('这是设计稿演示，暂未连接密码重置接口。')} | 跨页数据/返回/异常/触发条件 |
| m01-p06 | 1 | 返回 | 页面跳转 | location.href='m01-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m01-p06 | 2 | 密码 | 输入/键盘、状态/内容变化 | event=>{event.preventDefault();left=Math.max(0,left-1);document.querySelector('#error').textContent=left?`密码错误，还可以尝试 ${left} 次`:'尝试次数已用完，请找回密码';document.querySelector('#password').value='';if(!left)document.querySelector('.retry').disabled=true} | 跨页数据/返回/异常/触发条件 |
| m01-p06 | 3 | 显示密码 | 状态/内容变化 | ; ()=>{const input=document.querySelector('#password');input.type=input.type==='password'?'text':'password';document.querySelector('.eye').setAttribute('aria-label',input.type==='password'?'显示密码':'隐藏密码')} | 跨页数据/返回/异常/触发条件 |
| m01-p06 | 4 | 再试一次 | 状态/内容变化 | ; ; event=>{event.preventDefault();left=Math.max(0,left-1);document.querySelector('#error').textContent=left?`密码错误，还可以尝试 ${left} 次`:'尝试次数已用完，请找回密码';document.querySelector('#password').value='';if(!left)document.querySelector('.retry').disabled=true} | 跨页数据/返回/异常/触发条件 |
| m01-p06 | 5 | 找回密码 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m01-p07 | 1 | 返回 | 函数调用/需核对上下文 | history.back(); | 跨页数据/返回/异常/触发条件 |
| m01-p07 | 2 | 第 1 位验证码 | 输入/键盘、状态/内容变化、分享/复制/导出 | ; ()=>{input.value=input.value.replace(/\D/g,'').slice(0,1);if(input.value&&index<5)inputs[index+1].focus()}; event=>{if(event.key==='Backspace'&&!input.value&&index>0)inputs[index-1].focus()}; event=>{event.preventDefault();const digits=event.clipboardData.getData('text').replace(/\D/g,'').slice(0,6);[...digits].forEach((digit,i)=>{if(inputs[i])inputs[i].value=digit});inputs[Math.min(digits.length,5)].focus()} | 跨页数据/返回/异常/触发条件 |
| m01-p07 | 3 | 第 2 位验证码 | 输入/键盘、状态/内容变化、分享/复制/导出 | ; ()=>{input.value=input.value.replace(/\D/g,'').slice(0,1);if(input.value&&index<5)inputs[index+1].focus()}; event=>{if(event.key==='Backspace'&&!input.value&&index>0)inputs[index-1].focus()}; event=>{event.preventDefault();const digits=event.clipboardData.getData('text').replace(/\D/g,'').slice(0,6);[...digits].forEach((digit,i)=>{if(inputs[i])inputs[i].value=digit});inputs[Math.min(digits.length,5)].focus()} | 跨页数据/返回/异常/触发条件 |
| m01-p07 | 4 | 第 3 位验证码 | 输入/键盘、状态/内容变化、分享/复制/导出 | ; ()=>{input.value=input.value.replace(/\D/g,'').slice(0,1);if(input.value&&index<5)inputs[index+1].focus()}; event=>{if(event.key==='Backspace'&&!input.value&&index>0)inputs[index-1].focus()}; event=>{event.preventDefault();const digits=event.clipboardData.getData('text').replace(/\D/g,'').slice(0,6);[...digits].forEach((digit,i)=>{if(inputs[i])inputs[i].value=digit});inputs[Math.min(digits.length,5)].focus()} | 跨页数据/返回/异常/触发条件 |
| m01-p07 | 5 | 第 4 位验证码 | 输入/键盘、状态/内容变化、分享/复制/导出 | ; ()=>{input.value=input.value.replace(/\D/g,'').slice(0,1);if(input.value&&index<5)inputs[index+1].focus()}; event=>{if(event.key==='Backspace'&&!input.value&&index>0)inputs[index-1].focus()}; event=>{event.preventDefault();const digits=event.clipboardData.getData('text').replace(/\D/g,'').slice(0,6);[...digits].forEach((digit,i)=>{if(inputs[i])inputs[i].value=digit});inputs[Math.min(digits.length,5)].focus()} | 跨页数据/返回/异常/触发条件 |
| m01-p07 | 6 | 第 5 位验证码 | 输入/键盘、状态/内容变化、分享/复制/导出 | ; ()=>{input.value=input.value.replace(/\D/g,'').slice(0,1);if(input.value&&index<5)inputs[index+1].focus()}; event=>{if(event.key==='Backspace'&&!input.value&&index>0)inputs[index-1].focus()}; event=>{event.preventDefault();const digits=event.clipboardData.getData('text').replace(/\D/g,'').slice(0,6);[...digits].forEach((digit,i)=>{if(inputs[i])inputs[i].value=digit});inputs[Math.min(digits.length,5)].focus()} | 跨页数据/返回/异常/触发条件 |
| m01-p07 | 7 | 第 6 位验证码 | 输入/键盘、状态/内容变化、分享/复制/导出 | ; ()=>{input.value=input.value.replace(/\D/g,'').slice(0,1);if(input.value&&index<5)inputs[index+1].focus()}; event=>{if(event.key==='Backspace'&&!input.value&&index>0)inputs[index-1].focus()}; event=>{event.preventDefault();const digits=event.clipboardData.getData('text').replace(/\D/g,'').slice(0,6);[...digits].forEach((digit,i)=>{if(inputs[i])inputs[i].value=digit});inputs[Math.min(digits.length,5)].focus()} | 跨页数据/返回/异常/触发条件 |
| m01-p07 | 8 | 验证并继续 | 状态/内容变化、提示反馈 | ; ; event=>{event.preventDefault();show(inputs.every(input=>input.value)?'这是设计稿演示，暂未连接验证码接口。':'请输入完整的六位验证码')} | 跨页数据/返回/异常/触发条件 |
| m01-p07 | 9 | 48 秒后可重新获取 | 提示反馈 | ; ()=>show(seconds?'请等待倒计时结束':'这是设计稿演示，暂未发送验证码。') | 跨页数据/返回/异常/触发条件 |
| m01-p07 | 10 | 没收到验证码？换个方式 | 提示反馈 | ; ()=>show('其他验证方式尚未接入。') | 跨页数据/返回/异常/触发条件 |
| m01-p08 | 1 | 返回登录 | 页面跳转 | location.href='m01-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p01 | 1 | 邀请 TA 加入 生成专属邀请码 | 页面跳转 | location.href='m02-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p01 | 2 | 输入 TA 的邀请码 接受一份特别邀请 | 页面跳转 | location.href='m02-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p02 | 1 | ✦ 复制邀请码 ✦ | 状态/内容变化、提示反馈、分享/复制/导出 | ; async function copy(){try{await navigator.clipboard.writeText(code);show('邀请码已复制')}catch{const input=document.createElement('textarea');input.value=code;document.body.append(input);input.select();document.execCommand('copy');input.remove();show('邀请码已复制')}} | 跨页数据/返回/异常/触发条件 |
| m02-p02 | 2 | 发送给微信好友 | 提示反馈、分享/复制/导出 | ; async()=>{if(navigator.share){show('正在打开分享面板…');try{await navigator.share({title:'独家童话邀请函',text:`邀请你一起写我们的故事，邀请码：${code}`})}catch{await copy();show('邀请码已复制，可粘贴发送给 TA')}}else{await copy();show('邀请码已复制，可粘贴发送给 TA')}} | 跨页数据/返回/异常/触发条件 |
| m02-p02 | 3 | 保存邀请卡 | 分享/复制/导出 | ; ()=>{const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="860" height="540"><rect width="100%" height="100%" rx="42" fill="#fff7ef"/><rect x="25" y="25" width="810" height="490" rx="30" fill="none" stroke="#dc9e9c" stroke-width="4"/><text x="430" y="150" text-anchor="middle" font-size="48" fill="#754832">独家童话邀请函</text><text x="430" y="330" text-anchor="middle" font-size="90" fill="#a4454b" font-family="Georgia">${code}</text><text x="430" y="440" text-anchor="middle" font-size="30" fill="#946f5b">邀请 TA 一起收藏每一段日常</text></svg>`;const url=URL.createObjectURL(new Blob([svg],{type:'image/svg | 跨页数据/返回/异常/触发条件 |
| m02-p03 | 1 | 返回 | 页面跳转 | location.href='m02-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p03 | 2 | 第 1 位邀请码 | 输入/键盘、状态/内容变化、分享/复制/导出 | ; ()=>{input.value=input.value.replace(/[^a-z0-9]/gi,'').slice(0,1).toUpperCase();if(input.value&&index<3)inputs[index+1].focus()}; event=>{if(event.key==='Backspace'&&!input.value&&index>0)inputs[index-1].focus()}; event=>{event.preventDefault();[...event.clipboardData.getData('text').replace(/[^a-z0-9]/gi,'').slice(0,4).toUpperCase()].forEach((char,i)=>inputs[i].value=char)} | 跨页数据/返回/异常/触发条件 |
| m02-p03 | 3 | 第 2 位邀请码 | 输入/键盘、状态/内容变化、分享/复制/导出 | ; ()=>{input.value=input.value.replace(/[^a-z0-9]/gi,'').slice(0,1).toUpperCase();if(input.value&&index<3)inputs[index+1].focus()}; event=>{if(event.key==='Backspace'&&!input.value&&index>0)inputs[index-1].focus()}; event=>{event.preventDefault();[...event.clipboardData.getData('text').replace(/[^a-z0-9]/gi,'').slice(0,4).toUpperCase()].forEach((char,i)=>inputs[i].value=char)} | 跨页数据/返回/异常/触发条件 |
| m02-p03 | 4 | 第 3 位邀请码 | 输入/键盘、状态/内容变化、分享/复制/导出 | ; ()=>{input.value=input.value.replace(/[^a-z0-9]/gi,'').slice(0,1).toUpperCase();if(input.value&&index<3)inputs[index+1].focus()}; event=>{if(event.key==='Backspace'&&!input.value&&index>0)inputs[index-1].focus()}; event=>{event.preventDefault();[...event.clipboardData.getData('text').replace(/[^a-z0-9]/gi,'').slice(0,4).toUpperCase()].forEach((char,i)=>inputs[i].value=char)} | 跨页数据/返回/异常/触发条件 |
| m02-p03 | 5 | 第 4 位邀请码 | 输入/键盘、状态/内容变化、分享/复制/导出 | ; ()=>{input.value=input.value.replace(/[^a-z0-9]/gi,'').slice(0,1).toUpperCase();if(input.value&&index<3)inputs[index+1].focus()}; event=>{if(event.key==='Backspace'&&!input.value&&index>0)inputs[index-1].focus()}; event=>{event.preventDefault();[...event.clipboardData.getData('text').replace(/[^a-z0-9]/gi,'').slice(0,4).toUpperCase()].forEach((char,i)=>inputs[i].value=char)} | 跨页数据/返回/异常/触发条件 |
| m02-p03 | 6 | 查看邀请内容 | 页面跳转、状态/内容变化 | ; ; event=>{event.preventDefault();if(inputs.some(input=>!input.value)){document.querySelector('#error').style.display='block';return}location.href='m02-p04.html'} | 跨页数据/返回/异常/触发条件 |
| m02-p03 | 7 | 请让 TA 分享给你 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m02-p04 | 1 | 返回 | 页面跳转 | location.href='m02-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p04 | 2 | 确认建立关系 | 页面跳转 | location.href='m02-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p04 | 3 | 暂不接受 | 页面跳转 | location.href='m02-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p05 | 1 | 去写第一篇共同日记 ♡ | 页面跳转 | location.href='m03-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p05 | 2 | 完善情侣资料 | 页面跳转 | location.href='m02-p06.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p06 | 1 | 返回 | 页面跳转 | location.href='m02-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p06 | 2 | 情侣昵称 | 输入/键盘、状态/内容变化、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();for(const input of form.elements){if(input.name)localStorage.setItem('dujia-profile-'+input.name,input.value)}toast.textContent='小资料已保存在当前浏览器';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2500)} | 跨页数据/返回/异常/触发条件 |
| m02-p06 | 3 | 相遇日期 | 输入/键盘、状态/内容变化、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();for(const input of form.elements){if(input.name)localStorage.setItem('dujia-profile-'+input.name,input.value)}toast.textContent='小资料已保存在当前浏览器';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2500)} | 跨页数据/返回/异常/触发条件 |
| m02-p06 | 4 | 共同纪念日 | 输入/键盘、状态/内容变化、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();for(const input of form.elements){if(input.name)localStorage.setItem('dujia-profile-'+input.name,input.value)}toast.textContent='小资料已保存在当前浏览器';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2500)} | 跨页数据/返回/异常/触发条件 |
| m02-p06 | 5 | 保存小资料 | 状态/内容变化、提交/本地保存候选、提示反馈 | ; ; event=>{event.preventDefault();for(const input of form.elements){if(input.name)localStorage.setItem('dujia-profile-'+input.name,input.value)}toast.textContent='小资料已保存在当前浏览器';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2500)} | 跨页数据/返回/异常/触发条件 |
| m02-p07 | 1 | 提醒 TA 看看 | 提示反馈 | ; ()=>show('这是设计稿演示，暂未发送提醒。') | 跨页数据/返回/异常/触发条件 |
| m02-p07 | 2 | 复制邀请链接 | 页面跳转、状态/内容变化、提示反馈、分享/复制/导出 | ; async()=>{const link=new URL('m02-p03.html?code=XH7K-9M2Q',location.href).href;try{await navigator.clipboard.writeText(link);show('邀请链接已复制')}catch{const input=document.createElement('textarea');input.value=link;document.body.append(input);input.select();document.execCommand('copy');input.remove();show('邀请链接已复制')}} | 跨页数据/返回/异常/触发条件 |
| m02-p08 | 1 | 请 TA 重新邀请 | 页面跳转 | location.href='m02-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p08 | 2 | 重新输入邀请码 | 页面跳转 | location.href='m02-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p09 | 1 | 回到我们的首页 | 页面跳转 | location.href='m03-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m02-p09 | 2 | 查看关系设置 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m03-p01 | 1 | 搜索共同记录 | 页面跳转 | location.href='m03-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p01 | 2 | 写日记 | 页面跳转 | location.href='m03-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p01 | 3 | 添加照片 | 页面跳转 | location.href='m03-p11.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p01 | 4 | 去童话工坊，把回忆变成故事 › | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m03-p02 | 1 | 搜索共同记录 | 页面跳转 | location.href='m03-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p02 | 2 | 写日记 记录心情 | 页面跳转 | location.href='m03-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p02 | 3 | 添加照片 珍藏瞬间 | 页面跳转 | location.href='m03-p11.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p02 | 4 | 去童话工坊，把回忆变成故事 › | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m03-p02 | 5 | 查看全部 › | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m03-p02 | 6 | 晚霞散步 今天 20:12 | 页面跳转 | location.href='m03-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p02 | 7 | 今天因为一件小事笑了好久 小满记录 | 页面跳转 | location.href='m03-p06.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p02 | 8 | 阿舟回应了你的日记 ♡ 刚刚 | 页面跳转 | location.href='m03-p06.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p02 | 9 | 继续翻阅我们的故事 3D 日记本 · 上次读到第 18 页 继续阅读 › | 页面跳转 | location.href='m08-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p02 | 10 | 下一件重要时刻 我们的恋爱纪念日 · 18 天后 查看重要时刻 › | 页面跳转 | location.href='m04-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p03 | 1 | 返回首页 | 页面跳转 | location.href='m03-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p03 | 2 | 搜索关键词 | 输入/键盘、页面跳转、状态/内容变化 | event=>{event.preventDefault();if(q.value.trim())location.href='m03-p04.html?q='+encodeURIComponent(q.value.trim())} | 跨页数据/返回/异常/触发条件 |
| m03-p03 | 3 | 清除搜索 | 状态/内容变化 | ; ()=>{q.value='';q.focus()} | 跨页数据/返回/异常/触发条件 |
| m03-p03 | 4 | 晚霞 | 页面跳转、状态/内容变化 | ; ()=>{q.value=button.dataset.query;location.href='m03-p04.html?q='+encodeURIComponent(q.value)} | 跨页数据/返回/异常/触发条件 |
| m03-p03 | 5 | 火锅 | 页面跳转、状态/内容变化 | ; ()=>{q.value=button.dataset.query;location.href='m03-p04.html?q='+encodeURIComponent(q.value)} | 跨页数据/返回/异常/触发条件 |
| m03-p03 | 6 | 旅行 | 页面跳转、状态/内容变化 | ; ()=>{q.value=button.dataset.query;location.href='m03-p04.html?q='+encodeURIComponent(q.value)} | 跨页数据/返回/异常/触发条件 |
| m03-p03 | 7 | 日记 | 页面跳转、状态/内容变化 | ; ()=>{q.value=button.dataset.query;location.href='m03-p04.html?q='+encodeURIComponent(q.value)} | 跨页数据/返回/异常/触发条件 |
| m03-p03 | 8 | 照片 | 页面跳转、状态/内容变化 | ; ()=>{q.value=button.dataset.query;location.href='m03-p04.html?q='+encodeURIComponent(q.value)} | 跨页数据/返回/异常/触发条件 |
| m03-p03 | 9 | 旅行 | 页面跳转、状态/内容变化 | ; ()=>{q.value=button.dataset.query;location.href='m03-p04.html?q='+encodeURIComponent(q.value)} | 跨页数据/返回/异常/触发条件 |
| m03-p03 | 10 | 纪念日 | 页面跳转、状态/内容变化 | ; ()=>{q.value=button.dataset.query;location.href='m03-p04.html?q='+encodeURIComponent(q.value)} | 跨页数据/返回/异常/触发条件 |
| m03-p04 | 1 | 返回搜索 | 页面跳转 | location.href='m03-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p04 | 2 | 搜索关键词 | 输入/键盘、页面跳转、状态/内容变化 | event=>{event.preventDefault();location.href='m03-p04.html?q='+encodeURIComponent(query.value)} | 跨页数据/返回/异常/触发条件 |
| m03-p04 | 3 | 清除 | 页面跳转 | location.href='m03-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p04 | 4 | 今天的晚霞像橘子汽水 小满 · 9 月 1 日 · 共同可见 | 页面跳转 | location.href='m03-p06.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p04 | 5 | 查看海边晚霞照片 | 页面跳转 | location.href='m03-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p04 | 6 | 查看栏杆边的晚霞照片 | 页面跳转 | location.href='m03-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p04 | 7 | 第一次一起看晚霞　› | 页面跳转 | location.href='m04-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p05 | 1 | 返回首页 | 页面跳转 | location.href='m03-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p05 | 2 | 保存 | 提交/本地保存候选、提示反馈 | ; function save(){const data=Object.fromEntries(new FormData(form));localStorage.setItem('dujia-diary-draft',JSON.stringify(data));show('日记已保存在当前浏览器')} | 跨页数据/返回/异常/触发条件 |
| m03-p05 | 3 | 日记标题 | 输入/键盘、提交/本地保存候选 | event=>{event.preventDefault();save()} | 跨页数据/返回/异常/触发条件 |
| m03-p05 | 4 | 今天的心情 | 原生选择器、提交/本地保存候选 | event=>{event.preventDefault();save()} | 跨页数据/返回/异常/触发条件 |
| m03-p05 | 5 | 日记正文 | 输入/键盘、提交/本地保存候选 | event=>{event.preventDefault();save()} | 跨页数据/返回/异常/触发条件 |
| m03-p05 | 6 | 移除照片 | 状态/内容变化 | ; ()=>{document.querySelector('#preview').style.display='none'} | 跨页数据/返回/异常/触发条件 |
| m03-p05 | 7 | 添加照片 | 函数调用/需核对上下文 | ; ()=>document.querySelector('#file').click() | 跨页数据/返回/异常/触发条件 |
| m03-p05 | 8 | file | 文件选择、状态/内容变化 | ; event=>{const file=event.target.files[0];if(!file)return;document.querySelector('#preview').style.display='block';document.querySelector('#preview-image').style.background=`url('${URL.createObjectURL(file)}') center/cover`} | 跨页数据/返回/异常/触发条件 |
| m03-p05 | 9 | visibility | 勾选/切换、提交/本地保存候选 | event=>{event.preventDefault();save()} | 跨页数据/返回/异常/触发条件 |
| m03-p05 | 10 | visibility | 勾选/切换、提交/本地保存候选 | event=>{event.preventDefault();save()} | 跨页数据/返回/异常/触发条件 |
| m03-p05 | 11 | 保存日记 | 提交/本地保存候选 | ; ; event=>{event.preventDefault();save()} | 跨页数据/返回/异常/触发条件 |
| m03-p06 | 1 | 返回首页 | 页面跳转 | location.href='m03-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p06 | 2 | 筛选日记 | 提示反馈 | ; ()=>show('日记筛选将在完整交互阶段接入') | 跨页数据/返回/异常/触发条件 |
| m03-p06 | 3 | 全部 | 状态/内容变化、提示反馈 | ; ()=>{document.querySelectorAll('[data-tab]').forEach(item=>{item.classList.toggle('active',item===button);item.setAttribute('aria-selected',String(item===button))});show(button.dataset.tab==='draft'?'草稿列表将在完整交互阶段接入':'显示全部日记')} | 跨页数据/返回/异常/触发条件 |
| m03-p06 | 4 | 草稿 2 | 状态/内容变化、提示反馈 | ; ()=>{document.querySelectorAll('[data-tab]').forEach(item=>{item.classList.toggle('active',item===button);item.setAttribute('aria-selected',String(item===button))});show(button.dataset.tab==='draft'?'草稿列表将在完整交互阶段接入':'显示全部日记')} | 跨页数据/返回/异常/触发条件 |
| m03-p06 | 5 | 今天因为一件小事笑了好久 开心 小满 · 共同可见 阿舟回应了 | 页面跳转 | location.href='m03-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p06 | 6 | 雨天的火锅 阿舟 · 共同可见 | 页面跳转 | location.href='m03-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p06 | 7 | 仅自己可见 | 页面跳转 | location.href='m03-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p06 | 8 | 写日记 | 页面跳转 | location.href='m03-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p07 | 1 | 返回日记列表 | 页面跳转 | location.href='m03-p06.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p07 | 2 | 编辑日记 | 页面跳转 | location.href='m03-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p07 | 3 | 更多操作 | 状态/内容变化、提示反馈 | ; ()=>{toast.textContent='这是日记详情的 HTML 演示';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2500)} | 跨页数据/返回/异常/触发条件 |
| m03-p08 | 1 | 返回日记列表 | 页面跳转 | location.href='m03-p06.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p08 | 2 | 编辑日记 | 页面跳转 | location.href='m03-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p08 | 3 | 给 TA 留一句话 | 输入/键盘、状态/内容变化、提示反馈 | event=>{event.preventDefault();const value=document.querySelector('#reply').value.trim();if(!value)return;show('留言已保存在当前演示会话');document.querySelector('#reply').value=''} | 跨页数据/返回/异常/触发条件 |
| m03-p08 | 4 | 添加表情 | 状态/内容变化 | ; ()=>{document.querySelector('#reply').value+=' ❤️';document.querySelector('#reply').focus()} | 跨页数据/返回/异常/触发条件 |
| m03-p08 | 5 | 发送留言 | 状态/内容变化、提示反馈 | ; ; event=>{event.preventDefault();const value=document.querySelector('#reply').value.trim();if(!value)return;show('留言已保存在当前演示会话');document.querySelector('#reply').value=''} | 跨页数据/返回/异常/触发条件 |
| m03-p09 | 1 | 返回首页 | 页面跳转 | location.href='m03-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p09 | 2 | 添加第一张照片 | 页面跳转 | location.href='m03-p11.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p09 | 3 | 从系统相册选择 | 页面跳转 | location.href='m03-p11.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p10 | 1 | 返回首页 | 页面跳转 | location.href='m03-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p10 | 2 | 筛选照片 | 状态/内容变化、提示反馈 | ; ()=>{const toast=document.querySelector('#toast');toast.textContent='这是相册筛选的 HTML 演示';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2500)} | 跨页数据/返回/异常/触发条件 |
| m03-p10 | 3 | 全部 | 状态/内容变化 | ; ()=>{tabs.forEach(item=>{item.classList.toggle('active',item===button);item.setAttribute('aria-selected',String(item===button))})} | 跨页数据/返回/异常/触发条件 |
| m03-p10 | 4 | 共同可见 | 状态/内容变化 | ; ()=>{tabs.forEach(item=>{item.classList.toggle('active',item===button);item.setAttribute('aria-selected',String(item===button))})} | 跨页数据/返回/异常/触发条件 |
| m03-p10 | 5 | 旅行 | 状态/内容变化 | ; ()=>{tabs.forEach(item=>{item.classList.toggle('active',item===button);item.setAttribute('aria-selected',String(item===button))})} | 跨页数据/返回/异常/触发条件 |
| m03-p10 | 6 | 晚霞散步 | 页面跳转 | location.href='m03-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p10 | 7 | 火锅 | 页面跳转 | location.href='m03-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p10 | 8 | 玫瑰花 | 页面跳转 | location.href='m03-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p10 | 9 | 雨天窗户 | 页面跳转 | location.href='m03-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p10 | 10 | 情侣合照 | 页面跳转 | location.href='m03-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p10 | 11 | 宠物爪子 | 页面跳转 | location.href='m03-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p10 | 12 | ＋ 添加照片 | 页面跳转 | location.href='m03-p11.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p11 | 1 | 返回相册 | 页面跳转 | location.href='m03-p10.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p11 | 2 | 完成 | 提交/本地保存候选、提示反馈 | ; function save(){localStorage.setItem('dujia-photo-draft',JSON.stringify(Object.fromEntries(new FormData(form))));show('照片信息已保存在当前浏览器')} | 跨页数据/返回/异常/触发条件 |
| m03-p11 | 3 | 更换照片 | 函数调用/需核对上下文 | ; ()=>file.click() | 跨页数据/返回/异常/触发条件 |
| m03-p11 | 4 | file | 文件选择、状态/内容变化 | ; ()=>{if(!file.files[0])return;image.src=URL.createObjectURL(file.files[0]);image.style.display='block'} | 跨页数据/返回/异常/触发条件 |
| m03-p11 | 5 | 照片心情 | 输入/键盘、提交/本地保存候选 | event=>{event.preventDefault();save()} | 跨页数据/返回/异常/触发条件 |
| m03-p11 | 6 | 照片日期 | 输入/键盘、提交/本地保存候选 | event=>{event.preventDefault();save()} | 跨页数据/返回/异常/触发条件 |
| m03-p11 | 7 | 照片标签 | 输入/键盘、提交/本地保存候选 | event=>{event.preventDefault();save()} | 跨页数据/返回/异常/触发条件 |
| m03-p11 | 8 | 添加标签 | 状态/内容变化 | ; ()=>{const tag=form.elements.tag;tag.value=tag.value?tag.value+'、':'';tag.focus()} | 跨页数据/返回/异常/触发条件 |
| m03-p11 | 9 | visibility | 勾选/切换、提交/本地保存候选 | event=>{event.preventDefault();save()} | 跨页数据/返回/异常/触发条件 |
| m03-p11 | 10 | visibility | 勾选/切换、提交/本地保存候选 | event=>{event.preventDefault();save()} | 跨页数据/返回/异常/触发条件 |
| m03-p11 | 11 | 保存照片 | 提交/本地保存候选 | ; ; event=>{event.preventDefault();save()} | 跨页数据/返回/异常/触发条件 |
| m03-p12 | 1 | 返回照片相册 | 页面跳转 | location.href='m03-p10.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p12 | 2 | 编辑照片 | 页面跳转 | location.href='m03-p11.html'; | 跨页数据/返回/异常/触发条件 |
| m03-p12 | 3 | 给 TA 留一句话 | 输入/键盘、状态/内容变化、提示反馈 | event=>{event.preventDefault();const value=document.querySelector('#reply').value.trim();if(!value)return;show('留言已保存在当前演示会话');document.querySelector('#reply').value=''} | 跨页数据/返回/异常/触发条件 |
| m03-p12 | 4 | 添加表情 | 状态/内容变化 | ; ()=>{document.querySelector('#reply').value+=' ❤️';document.querySelector('#reply').focus()} | 跨页数据/返回/异常/触发条件 |
| m03-p12 | 5 | 发送留言 | 状态/内容变化、提示反馈 | ; ; event=>{event.preventDefault();const value=document.querySelector('#reply').value.trim();if(!value)return;show('留言已保存在当前演示会话');document.querySelector('#reply').value=''} | 跨页数据/返回/异常/触发条件 |
| m04-p01 | 1 | 查看纪念日 | 页面跳转 | location.href='m04-p07.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p01 | 2 | 第一次旅行 | 页面跳转 | location.href='m04-p10.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p01 | 3 | 查看全部 › | 状态/内容变化、提示反馈 | ; ()=>{const toast=document.querySelector('#toast');toast.textContent='当前显示全部重要章节';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2500)} | 跨页数据/返回/异常/触发条件 |
| m04-p01 | 4 | 春日野餐  2024.04.13 | 页面跳转 | location.href='m04-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p01 | 5 | 第一次一起做饭  2024.05.20 | 页面跳转 | location.href='m04-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p01 | 6 | 纪念日 | 页面跳转 | location.href='m04-p07.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p01 | 7 | 时光胶囊 | 页面跳转 | location.href='m04-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p01 | 8 | 悄悄留言 | 页面跳转 | location.href='m04-p16.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p02 | 1 | 从共同记录中收录 | 状态/内容变化、提示反馈 | ; ()=>{const toast=document.querySelector('#toast');toast.textContent='请先选择一条共同记录';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2600)} | 跨页数据/返回/异常/触发条件 |
| m04-p02 | 2 | 新建重要时刻 | 页面跳转 | location.href='m04-p04.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p03 | 1 | 返回重要时刻 | 页面跳转 | location.href='m04-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p03 | 2 | 野餐日记 前往共同记录查看 | 页面跳转 | location.href='m03-p08.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p03 | 3 | 12 张照片 前往共同记录查看 | 页面跳转 | location.href='m03-p10.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p03 | 4 | 悄悄留言 3 条 | 页面跳转 | location.href='m04-p16.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p04 | 1 | 返回重要时刻 | 页面跳转 | location.href='m04-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p04 | 2 | 添加封面 | 函数调用/需核对上下文 | ; ()=>document.querySelector('#cover-file').click() | 跨页数据/返回/异常/触发条件 |
| m04-p04 | 3 | cover-file | 文件选择、状态/内容变化 | ; event=>{const file=event.target.files[0];if(!file)return;const image=document.querySelector('#cover-preview');image.src=URL.createObjectURL(file);image.style.display='block';document.querySelector('#cover-label').style.display='none'} | 跨页数据/返回/异常/触发条件 |
| m04-p04 | 4 | name | 输入/键盘、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();localStorage.setItem('dujia-moment-draft',JSON.stringify(Object.fromEntries(new FormData(form))));show('重要时刻已保存到当前浏览器')} | 跨页数据/返回/异常/触发条件 |
| m04-p04 | 5 | 发生日期 | 输入/键盘、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();localStorage.setItem('dujia-moment-draft',JSON.stringify(Object.fromEntries(new FormData(form))));show('重要时刻已保存到当前浏览器')} | 跨页数据/返回/异常/触发条件 |
| m04-p04 | 6 | type | 勾选/切换、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();localStorage.setItem('dujia-moment-draft',JSON.stringify(Object.fromEntries(new FormData(form))));show('重要时刻已保存到当前浏览器')} | 跨页数据/返回/异常/触发条件 |
| m04-p04 | 7 | type | 勾选/切换、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();localStorage.setItem('dujia-moment-draft',JSON.stringify(Object.fromEntries(new FormData(form))));show('重要时刻已保存到当前浏览器')} | 跨页数据/返回/异常/触发条件 |
| m04-p04 | 8 | type | 勾选/切换、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();localStorage.setItem('dujia-moment-draft',JSON.stringify(Object.fromEntries(new FormData(form))));show('重要时刻已保存到当前浏览器')} | 跨页数据/返回/异常/触发条件 |
| m04-p04 | 9 | type | 勾选/切换、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();localStorage.setItem('dujia-moment-draft',JSON.stringify(Object.fromEntries(new FormData(form))));show('重要时刻已保存到当前浏览器')} | 跨页数据/返回/异常/触发条件 |
| m04-p04 | 10 | 记录这个时刻背后的故事… | 输入/键盘、状态/内容变化 | ; ()=>document.querySelector('#counter').textContent=story.value.length+'/200' | 跨页数据/返回/异常/触发条件 |
| m04-p04 | 11 | 从共同记录中选择 | 提示反馈 | ; ()=>show('请从共同日记和相册中选择关联记录') | 跨页数据/返回/异常/触发条件 |
| m04-p04 | 12 | 保存到时刻册 | 提交/本地保存候选、提示反馈 | ; ; event=>{event.preventDefault();localStorage.setItem('dujia-moment-draft',JSON.stringify(Object.fromEntries(new FormData(form))));show('重要时刻已保存到当前浏览器')} | 跨页数据/返回/异常/触发条件 |
| m04-p05 | 1 | 返回重要时刻 | 页面跳转 | location.href='m04-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p05 | 2 | 我们的纪念日还有 3 天 一起为 9 月 12 日留一段记录吧 | 页面跳转 | location.href='m04-p10.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p05 | 3 | 时光胶囊明天开启 写给未来的信，明天见 | 页面跳转 | location.href='m04-p15.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p05 | 4 | 春日野餐 · 重要时刻提醒 这一页已经收藏 1 年 | 页面跳转 | location.href='m04-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p05 | 5 | 每月记录提醒 本月的我们，值得一段记录 | 状态/内容变化、提示反馈 | ; ()=>{const toast=document.querySelector('#toast');toast.textContent='这条提醒已读';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2500)} | 跨页数据/返回/异常/触发条件 |
| m04-p06 | 1 | 返回重要时刻 | 页面跳转 | location.href='m04-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p06 | 2 | 去看看重要时刻 | 页面跳转 | location.href='m04-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p07 | 1 | 返回重要时刻 | 页面跳转 | location.href='m04-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p07 | 2 | 添加纪念日 | 页面跳转 | location.href='m04-p09.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p07 | 3 | 9 月 12 日 | 页面跳转 | location.href='m04-p10.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p07 | 4 | 相识纪念日 每年 9 月 12 日 | 页面跳转 | location.href='m04-p10.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p07 | 5 | 相识纪念日提醒 | 状态/内容变化 | ; ()=>{const on=button.getAttribute('aria-checked')!=='true';button.setAttribute('aria-checked',String(on));button.textContent=on?'已提醒':'未提醒'} | 跨页数据/返回/异常/触发条件 |
| m04-p07 | 6 | 第一次旅行 每年 6 月 18 日 | 页面跳转 | location.href='m04-p10.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p07 | 7 | 第一次旅行提醒 | 状态/内容变化 | ; ()=>{const on=button.getAttribute('aria-checked')!=='true';button.setAttribute('aria-checked',String(on));button.textContent=on?'已提醒':'未提醒'} | 跨页数据/返回/异常/触发条件 |
| m04-p07 | 8 | 添加纪念日 | 页面跳转 | location.href='m04-p09.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p08 | 1 | 返回重要时刻 | 页面跳转 | location.href='m04-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p08 | 2 | 添加第一个纪念日 | 页面跳转 | location.href='m04-p09.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p09 | 1 | 返回纪念日列表 | 页面跳转 | location.href='m04-p07.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p09 | 2 | name | 输入/键盘、状态/内容变化、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();const form=event.currentTarget;localStorage.setItem('dujia-anniversary-draft',JSON.stringify(Object.fromEntries(new FormData(form))));const toast=document.querySelector('#toast');toast.textContent='纪念日已保存在当前浏览器';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2600)} | 跨页数据/返回/异常/触发条件 |
| m04-p09 | 3 | 纪念日日期 | 输入/键盘、状态/内容变化、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();const form=event.currentTarget;localStorage.setItem('dujia-anniversary-draft',JSON.stringify(Object.fromEntries(new FormData(form))));const toast=document.querySelector('#toast');toast.textContent='纪念日已保存在当前浏览器';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2600)} | 跨页数据/返回/异常/触发条件 |
| m04-p09 | 4 | 提前 3 天 提前 1 天 当天 不提醒 | 原生选择器、状态/内容变化、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();const form=event.currentTarget;localStorage.setItem('dujia-anniversary-draft',JSON.stringify(Object.fromEntries(new FormData(form))));const toast=document.querySelector('#toast');toast.textContent='纪念日已保存在当前浏览器';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2600)} | 跨页数据/返回/异常/触发条件 |
| m04-p09 | 5 | 每年重复 | 勾选/切换、状态/内容变化、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();const form=event.currentTarget;localStorage.setItem('dujia-anniversary-draft',JSON.stringify(Object.fromEntries(new FormData(form))));const toast=document.querySelector('#toast');toast.textContent='纪念日已保存在当前浏览器';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2600)} | 跨页数据/返回/异常/触发条件 |
| m04-p09 | 6 | 可选 · 关联一段章节 春日野餐 第一次旅行 | 原生选择器、状态/内容变化、提交/本地保存候选、提示反馈 | event=>{event.preventDefault();const form=event.currentTarget;localStorage.setItem('dujia-anniversary-draft',JSON.stringify(Object.fromEntries(new FormData(form))));const toast=document.querySelector('#toast');toast.textContent='纪念日已保存在当前浏览器';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2600)} | 跨页数据/返回/异常/触发条件 |
| m04-p09 | 7 | 保存纪念日 | 状态/内容变化、提交/本地保存候选、提示反馈 | ; ; event=>{event.preventDefault();const form=event.currentTarget;localStorage.setItem('dujia-anniversary-draft',JSON.stringify(Object.fromEntries(new FormData(form))));const toast=document.querySelector('#toast');toast.textContent='纪念日已保存在当前浏览器';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2600)} | 跨页数据/返回/异常/触发条件 |
| m04-p10 | 1 | 返回纪念日 | 页面跳转 | location.href='m04-p07.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p10 | 2 | 春日野餐 | 页面跳转 | location.href='m04-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p10 | 3 | 那年九月的日记 | 页面跳转 | location.href='m03-p08.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p10 | 4 | 写下新的共同记录 | 页面跳转 | location.href='m03-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p11 | 1 | 一起留下今天的记录 | 页面跳转 | location.href='m03-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p11 | 2 | 查看这个时刻 | 页面跳转 | location.href='m04-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p12 | 1 | 返回重要时刻 | 页面跳转 | location.href='m04-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p12 | 2 | 新建时光胶囊 | 页面跳转 | location.href='m04-p13.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p12 | 3 | 等待开启 | 状态/内容变化 | ; ()=>{document.querySelectorAll('[role="tab"]').forEach(item=>{item.classList.toggle('active',item===tab);item.setAttribute('aria-selected',String(item===tab))});document.querySelectorAll('.card').forEach(card=>{card.style.opacity=tab.textContent==='等待开启'?card.dataset.state==='waiting'?'1':'.65':card.dataset.state==='opened'?'1':'.65'})} | 跨页数据/返回/异常/触发条件 |
| m04-p12 | 4 | 已经开启 | 状态/内容变化 | ; ()=>{document.querySelectorAll('[role="tab"]').forEach(item=>{item.classList.toggle('active',item===tab);item.setAttribute('aria-selected',String(item===tab))});document.querySelectorAll('.card').forEach(card=>{card.style.opacity=tab.textContent==='等待开启'?card.dataset.state==='waiting'?'1':'.65':card.dataset.state==='opened'?'1':'.65'})} | 跨页数据/返回/异常/触发条件 |
| m04-p12 | 5 | 写给一周年的我们 2026.09.12 开启 还有 10 天 | 页面跳转 | location.href='m04-p15.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p12 | 6 | 下一个春天再见 2026.09.12 开启 还有 10 天 | 页面跳转 | location.href='m04-p15.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p12 | 7 | 去年写给今天的信 已开启 | 页面跳转 | location.href='m04-p14.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p12 | 8 | ＋ 新建时光胶囊 | 页面跳转 | location.href='m04-p13.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p13 | 1 | 返回胶囊列表 | 页面跳转 | location.href='m04-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p13 | 2 | name | 输入/键盘、提交/本地保存候选 | event=>{event.preventDefault();save('sealed')} | 跨页数据/返回/异常/触发条件 |
| m04-p13 | 3 | message | 输入/键盘、提交/本地保存候选 | event=>{event.preventDefault();save('sealed')} | 跨页数据/返回/异常/触发条件 |
| m04-p13 | 4 | 添加照片 | 函数调用/需核对上下文 | document.querySelector('#photo').click(); | 跨页数据/返回/异常/触发条件 |
| m04-p13 | 5 | photo | 文件选择、状态/内容变化 | ; event=>{document.querySelector('#chosen').textContent=event.target.files.length+' 张照片已选择'} | 跨页数据/返回/异常/触发条件 |
| m04-p13 | 6 | opening | 输入/键盘、提交/本地保存候选 | event=>{event.preventDefault();save('sealed')} | 跨页数据/返回/异常/触发条件 |
| m04-p13 | 7 | 开启提醒 | 勾选/切换、提交/本地保存候选 | event=>{event.preventDefault();save('sealed')} | 跨页数据/返回/异常/触发条件 |
| m04-p13 | 8 | 暂存草稿 | 提交/本地保存候选 | ; ()=>save('draft') | 跨页数据/返回/异常/触发条件 |
| m04-p13 | 9 | 封存这份心意 | 提交/本地保存候选 | ; ; event=>{event.preventDefault();save('sealed')} | 跨页数据/返回/异常/触发条件 |
| m04-p14 | 1 | 返回胶囊列表 | 页面跳转 | location.href='m04-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p14 | 2 | 把这一刻收录进重要时刻 | 状态/内容变化、提示反馈 | ; ()=>{const toast=document.querySelector('#toast');toast.textContent='已加入重要时刻演示收藏';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2500)} | 跨页数据/返回/异常/触发条件 |
| m04-p15 | 1 | 返回胶囊列表 | 页面跳转 | location.href='m04-p12.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p15 | 2 | 开启当天提醒我 | 勾选/切换 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m04-p16 | 1 | 返回重要时刻 | 页面跳转 | location.href='m04-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p16 | 2 | 查看原记录 › | 页面跳转 | location.href='m03-p08.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p16 | 3 | 查看原记录 › | 页面跳转 | location.href='m04-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p16 | 4 | 查看原记录 › | 页面跳转 | location.href='m03-p08.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p17 | 1 | 返回重要时刻 | 页面跳转 | location.href='m04-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m04-p17 | 2 | 去看看共同记录 | 页面跳转 | location.href='m03-p06.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p01 | 1 | 做成童话漫画 把回忆画成专属故事 留下一格格心动瞬间 | 页面跳转 | location.href='m05-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p01 | 2 | 制作回忆影片 让重要时刻动起来 在光影里重温感动 | 页面跳转 | location.href='m05-p05.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p01 | 3 | 查看全部 › | 页面跳转 | location.href='m05-p09.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p01 | 4 | 已完成 海边的那天 2024.05.20 | 页面跳转 | location.href='m05-p08.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p01 | 5 | 草稿 雨后的晚餐 编辑于 2024.05.18 | 页面跳转 | location.href='m05-p08.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p01 | 6 | 开始一次创作 | 页面跳转 | location.href='m05-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p02 | 1 | 返回童话工坊 | 页面跳转 | location.href='m05-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p02 | 2 | 共同日记 2026.08.28 · 阿梨写下 | 状态/内容变化 | ; ()=>{chosen.setAttribute('aria-pressed','false');button.setAttribute('aria-pressed','true');chosen=button} | 跨页数据/返回/异常/触发条件 |
| m05-p02 | 3 | 相册照片 | 状态/内容变化 | ; ()=>{chosen.setAttribute('aria-pressed','false');button.setAttribute('aria-pressed','true');chosen=button} | 跨页数据/返回/异常/触发条件 |
| m05-p02 | 4 | 重要时刻 第一次一起看海 | 状态/内容变化 | ; ()=>{chosen.setAttribute('aria-pressed','false');button.setAttribute('aria-pressed','true');chosen=button} | 跨页数据/返回/异常/触发条件 |
| m05-p02 | 5 | 自由写一段回忆 | 状态/内容变化 | ; ()=>{chosen.setAttribute('aria-pressed','false');button.setAttribute('aria-pressed','true');chosen=button} | 跨页数据/返回/异常/触发条件 |
| m05-p02 | 6 | 用这些素材开始 | 函数调用/需核对上下文 | ; ()=>location.href=chosen.dataset.next | 跨页数据/返回/异常/触发条件 |
| m05-p03 | 1 | 返回素材选择 | 页面跳转 | location.href='m05-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p03 | 2 | 回忆内容 | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m05-p03 | 3 | 编辑 | 函数调用/需核对上下文 | document.querySelector('#story').focus(); | 跨页数据/返回/异常/触发条件 |
| m05-p03 | 4 | 暖暖水彩 | 状态/内容变化 | ; ()=>{document.querySelectorAll(group+' button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))} | 跨页数据/返回/异常/触发条件 |
| m05-p03 | 5 | 复古漫画 | 状态/内容变化 | ; ()=>{document.querySelectorAll(group+' button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))} | 跨页数据/返回/异常/触发条件 |
| m05-p03 | 6 | 轻柔铅笔 | 状态/内容变化 | ; ()=>{document.querySelectorAll(group+' button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))} | 跨页数据/返回/异常/触发条件 |
| m05-p03 | 7 | 温柔叙事 贴近日常，细腻温暖 | 状态/内容变化 | ; ()=>{document.querySelectorAll(group+' button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))} | 跨页数据/返回/异常/触发条件 |
| m05-p03 | 8 | 电影感 光影氛围，节奏张力 | 状态/内容变化 | ; ()=>{document.querySelectorAll(group+' button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))} | 跨页数据/返回/异常/触发条件 |
| m05-p03 | 9 | 默默 & 小满 可爱自然 · 清新温柔 | 页面跳转 | location.href='m05-p10.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p03 | 10 | 生成童话漫画 | 页面跳转、状态/内容变化、提交/本地保存候选 | ; ()=>{localStorage.setItem('dujia-comic-story',document.querySelector('#story').value);location.href='m05-p06.html'} | 跨页数据/返回/异常/触发条件 |
| m05-p04 | 1 | 返回素材选择 | 页面跳转 | location.href='m05-p02.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p04 | 2 | 晚霞海边照片 | 状态/内容变化 | ; ()=>{button.setAttribute('aria-pressed',String(button.getAttribute('aria-pressed')!=='true'));document.querySelector('#photo-count').textContent=document.querySelectorAll('.photos button[aria-pressed=true]').length} | 跨页数据/返回/异常/触发条件 |
| m05-p04 | 3 | 烟花合照 | 状态/内容变化 | ; ()=>{button.setAttribute('aria-pressed',String(button.getAttribute('aria-pressed')!=='true'));document.querySelector('#photo-count').textContent=document.querySelectorAll('.photos button[aria-pressed=true]').length} | 跨页数据/返回/异常/触发条件 |
| m05-p04 | 4 | 牵手散步照片 | 状态/内容变化 | ; ()=>{button.setAttribute('aria-pressed',String(button.getAttribute('aria-pressed')!=='true'));document.querySelector('#photo-count').textContent=document.querySelectorAll('.photos button[aria-pressed=true]').length} | 跨页数据/返回/异常/触发条件 |
| m05-p04 | 5 | 补充这段故事 | 输入/键盘、状态/内容变化 | ; ()=>document.querySelector('#counter').textContent=story.value.length+'/50' | 跨页数据/返回/异常/触发条件 |
| m05-p04 | 6 | 水彩 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.styles button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))} | 跨页数据/返回/异常/触发条件 |
| m05-p04 | 7 | 素描 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.styles button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))} | 跨页数据/返回/异常/触发条件 |
| m05-p04 | 8 | 清新插画 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.styles button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))} | 跨页数据/返回/异常/触发条件 |
| m05-p04 | 9 | 油画 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.styles button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))} | 跨页数据/返回/异常/触发条件 |
| m05-p04 | 10 | 他  阳光温柔 | 页面跳转 | location.href='m05-p10.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p04 | 11 | 她  温柔爱笑 | 页面跳转 | location.href='m05-p10.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p04 | 12 | 生成童话漫画 | 页面跳转、状态/内容变化、提交/本地保存候选 | ; ()=>{localStorage.setItem('dujia-comic-photo-story',story.value);location.href='m05-p06.html'} | 跨页数据/返回/异常/触发条件 |
| m05-p05 | 1 | 返回工坊 | 页面跳转 | location.href='m05-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p05 | 2 | 日记 那天的日落  2023年05月20日 | 状态/内容变化 | ; ()=>document.querySelectorAll('.clip').forEach(item=>item.setAttribute('aria-current',String(item===button))) | 跨页数据/返回/异常/触发条件 |
| m05-p05 | 3 | 照片 海边笑起来  2023年08月14日 | 状态/内容变化 | ; ()=>document.querySelectorAll('.clip').forEach(item=>item.setAttribute('aria-current',String(item===button))) | 跨页数据/返回/异常/触发条件 |
| m05-p05 | 4 | 重要时刻 第一次旅行  2023年10月03日 | 状态/内容变化 | ; ()=>document.querySelectorAll('.clip').forEach(item=>item.setAttribute('aria-current',String(item===button))) | 跨页数据/返回/异常/触发条件 |
| m05-p05 | 5 | 影片旁白 | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m05-p05 | 6 | 试听晚风和海浪 | 状态/内容变化、提示反馈 | ; ()=>{const toast=document.querySelector('#toast');toast.textContent='当前演示没有音频文件';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2500)} | 跨页数据/返回/异常/触发条件 |
| m05-p05 | 7 | 温柔手帐 | 状态/内容变化 | ; ()=>document.querySelectorAll('.moods button').forEach(item=>item.setAttribute('aria-pressed',String(item===button))) | 跨页数据/返回/异常/触发条件 |
| m05-p05 | 8 | 治愈暖光 | 状态/内容变化 | ; ()=>document.querySelectorAll('.moods button').forEach(item=>item.setAttribute('aria-pressed',String(item===button))) | 跨页数据/返回/异常/触发条件 |
| m05-p05 | 9 | 清新自然 | 状态/内容变化 | ; ()=>document.querySelectorAll('.moods button').forEach(item=>item.setAttribute('aria-pressed',String(item===button))) | 跨页数据/返回/异常/触发条件 |
| m05-p05 | 10 | 生成回忆影片 | 页面跳转、状态/内容变化、提交/本地保存候选 | ; ()=>{localStorage.setItem('dujia-film-narration',document.querySelector('#narration').value);location.href='m05-p06.html'} | 跨页数据/返回/异常/触发条件 |
| m05-p06 | 1 | 返回童话工坊 | 页面跳转 | location.href='m05-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p07 | 1 | 调整内容 | 页面跳转 | location.href='m05-p03.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p07 | 2 | 重新生成 | 页面跳转 | location.href='m05-p06.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p07 | 3 | 先回到童话工坊 ♡ | 页面跳转 | location.href='m05-p01.html'; | 跨页数据/返回/异常/触发条件 |
| m05-p08 | 1 | 返回我的创作 | 页面跳转 | location.href='m05-p09.html'; ; | 跨页数据/返回/异常/触发条件 |
| m05-p08 | 2 | 第1页 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.thumbs button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));document.querySelector('#page-count').textContent=`${index+1} / 8`;}; | 跨页数据/返回/异常/触发条件 |
| m05-p08 | 3 | 第2页 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.thumbs button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));document.querySelector('#page-count').textContent=`${index+1} / 8`;}; | 跨页数据/返回/异常/触发条件 |
| m05-p08 | 4 | 第3页 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.thumbs button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));document.querySelector('#page-count').textContent=`${index+1} / 8`;}; | 跨页数据/返回/异常/触发条件 |
| m05-p08 | 5 | 第4页 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.thumbs button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));document.querySelector('#page-count').textContent=`${index+1} / 8`;}; | 跨页数据/返回/异常/触发条件 |
| m05-p08 | 6 | 第5页 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.thumbs button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));document.querySelector('#page-count').textContent=`${index+1} / 8`;}; | 跨页数据/返回/异常/触发条件 |
| m05-p08 | 7 | 第6页 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.thumbs button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));document.querySelector('#page-count').textContent=`${index+1} / 8`;}; | 跨页数据/返回/异常/触发条件 |
| m05-p08 | 8 | 第7页 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.thumbs button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));document.querySelector('#page-count').textContent=`${index+1} / 8`;}; | 跨页数据/返回/异常/触发条件 |
| m05-p08 | 9 | 第8页 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.thumbs button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));document.querySelector('#page-count').textContent=`${index+1} / 8`;}; | 跨页数据/返回/异常/触发条件 |
| m05-p08 | 10 | 保存到共同相册 | 提交/本地保存候选、提示反馈 | ; ()=>{localStorage.setItem('dujia-comic-saved','true');notify('已保存到共同相册')}; | 跨页数据/返回/异常/触发条件 |
| m05-p08 | 11 | 给另一半看看 | 提示反馈、分享/复制/导出 | ; async()=>{if(navigator.share){try{await navigator.share({title:'海边的那天',url:location.href})}catch{}}else notify('可复制当前页面链接分享')}; | 跨页数据/返回/异常/触发条件 |
| m05-p08 | 12 | 重新生成 | 页面跳转 | location.href='m05-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m05-p09 | 1 | 收藏夹 | 函数调用/需核对上下文 | selectTab('漫画'); ; | 跨页数据/返回/异常/触发条件 |
| m05-p09 | 2 | 全部 | 函数调用/需核对上下文 | ; ()=>selectTab(item.dataset.tab); | 跨页数据/返回/异常/触发条件 |
| m05-p09 | 3 | 漫画 | 函数调用/需核对上下文 | ; ()=>selectTab(item.dataset.tab); | 跨页数据/返回/异常/触发条件 |
| m05-p09 | 4 | 影片 | 函数调用/需核对上下文 | ; ()=>selectTab(item.dataset.tab); | 跨页数据/返回/异常/触发条件 |
| m05-p09 | 5 | 草稿 | 函数调用/需核对上下文 | ; ()=>selectTab(item.dataset.tab); | 跨页数据/返回/异常/触发条件 |
| m05-p09 | 6 | 海边的那天  已收藏  漫画 | 页面跳转 | location.href='m05-p08.html'; ; | 跨页数据/返回/异常/触发条件 |
| m05-p09 | 7 | 晚风里的告白  影片 | 页面跳转 | location.href='m05-p05.html'; ; | 跨页数据/返回/异常/触发条件 |
| m05-p09 | 8 | Our Memories 正在把回忆 装订成册 65%  制作中 慢慢来，都是我们 最珍贵的时光 ♡ | 页面跳转 | location.href='m05-p06.html'; ; | 跨页数据/返回/异常/触发条件 |
| m05-p09 | 9 | 雨后的晚餐  草稿 继续编辑 › | 页面跳转 | location.href='m05-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m05-p09 | 10 | 开始创作 | 页面跳转 | location.href='m05-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m05-p10 | 1 | 返回童话工坊 | 页面跳转 | location.href='m05-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m05-p10 | 2 | appearance | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m05-p10 | 3 | outfit | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m05-p10 | 4 | mood | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m05-p10 | 5 | object | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m05-p10 | 6 | 更新我们的主角 | 状态/内容变化、提交/本地保存候选、提示反馈 | ; ()=>{localStorage.setItem(key,JSON.stringify(Object.fromEntries(inputs.map(input=>[input.id,input.value]))));const toast=document.querySelector('#toast');toast.textContent='主角设定已更新';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2200)}; | 跨页数据/返回/异常/触发条件 |
| m06-p01 | 1 | 小满 ♡ 已与阿舟关联 ♡ | 页面跳转 | location.href='m06-p02.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p01 | 2 | 我们的小世界 一起管理共同资料 | 页面跳转 | location.href='m06-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p01 | 3 | 草稿箱 | 页面跳转 | location.href='m06-p04.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p01 | 4 | 标签管理 | 页面跳转 | location.href='m06-p05.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p01 | 5 | 童话会员 | 页面跳转 | location.href='m06-p06.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p01 | 6 | 设置 | 页面跳转 | location.href='m06-p07.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p01 | 7 | 帮助与关于 | 页面跳转 | location.href='m06-p12.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p02 | 1 | 返回我的与设置 | 页面跳转 | location.href='m06-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p02 | 2 | 更换头像 | 文件选择、状态/内容变化 | ; event=>{const file=event.target.files?.[0];if(!file)return;const reader=new FileReader();reader.onload=()=>{avatarData=String(reader.result);preview.src=avatarData;preview.style.display='block'};reader.readAsDataURL(file)} | 跨页数据/返回/异常/触发条件 |
| m06-p02 | 3 | 更换头像 | 函数调用/需核对上下文 | document.querySelector('#avatar').click(); ; | 跨页数据/返回/异常/触发条件 |
| m06-p02 | 4 | nickname | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m06-p02 | 5 | birthday | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m06-p02 | 6 | saying | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m06-p02 | 7 | color | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m06-p02 | 8 | 保存资料 | 状态/内容变化、提交/本地保存候选、提示反馈 | ; ()=>{localStorage.setItem(key,JSON.stringify(Object.fromEntries(fields.map(name=>[name,document.getElementById(name).value]))));if(avatarData){try{localStorage.setItem('dujia-avatar',avatarData)}catch{}}const toast=document.querySelector('#toast');toast.textContent='个人资料已保存';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2200)}; | 跨页数据/返回/异常/触发条件 |
| m06-p03 | 1 | 返回我的与设置 | 页面跳转 | location.href='m06-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p03 | 2 | 共同昵称 小满与阿舟 | 函数调用/需核对上下文 | editNickname(); ; | 跨页数据/返回/异常/触发条件 |
| m06-p03 | 3 | 共同头像 | 页面跳转 | location.href='m06-p02.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p03 | 4 | 共同空间设置 哪些记录邀请对方一起看 | 页面跳转 | location.href='m06-p09.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p03 | 5 | 关联状态 | 提示反馈 | notify('我们的关联状态：已关联'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p03 | 6 | 解除关联 | 提示反馈 | notify('解除关联需要双方确认'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p04 | 1 | 返回我的与设置 | 页面跳转 | location.href='m06-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p04 | 2 | 雨天的电影 刚刚保存 仅自己可见草稿 | 页面跳转 | location.href='m05-p05.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p04 | 3 | 给未来的一封信 昨天 仅自己可见草稿 | 页面跳转 | location.href='m05-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p04 | 4 | 旅行计划 8 月 28 日 共同记录草稿 | 页面跳转 | location.href='m05-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p05 | 1 | 返回我的与设置 | 页面跳转 | location.href='m06-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p05 | 2 | 新建标签 | 函数调用/需核对上下文 | addTag(); ; | 跨页数据/返回/异常/触发条件 |
| m06-p05 | 3 | 日常 | 函数调用/需核对上下文 | editTag(this); ; | 跨页数据/返回/异常/触发条件 |
| m06-p05 | 4 | 旅行 | 函数调用/需核对上下文 | editTag(this); ; | 跨页数据/返回/异常/触发条件 |
| m06-p05 | 5 | 想念 | 函数调用/需核对上下文 | editTag(this); ; | 跨页数据/返回/异常/触发条件 |
| m06-p05 | 6 | 美食 | 函数调用/需核对上下文 | editTag(this); ; | 跨页数据/返回/异常/触发条件 |
| m06-p05 | 7 | 春日野餐 | 函数调用/需核对上下文 | editTag(this); ; | 跨页数据/返回/异常/触发条件 |
| m06-p05 | 8 | 第一次旅行 | 函数调用/需核对上下文 | editTag(this); ; | 跨页数据/返回/异常/触发条件 |
| m06-p05 | 9 | 我们的家 | 函数调用/需核对上下文 | editTag(this); ; | 跨页数据/返回/异常/触发条件 |
| m06-p05 | 10 | 新建标签 | 函数调用/需核对上下文 | addTag(); ; | 跨页数据/返回/异常/触发条件 |
| m06-p06 | 1 | 返回我的与设置 | 页面跳转 | location.href='m06-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p06 | 2 | 开通童话会员 | 提示反馈 | notify('会员开通演示：当前未接入支付'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p06 | 3 | 查看会员说明 › | 提示反馈 | notify('会员说明：更多时光胶囊、更大照片空间及专属装扮'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p07 | 1 | 返回我的与设置 | 页面跳转 | location.href='m06-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p07 | 2 | 账号与安全 | 页面跳转 | location.href='m06-p08.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p07 | 3 | 隐私与共同可见 | 页面跳转 | location.href='m06-p09.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p07 | 4 | 通知设置 | 页面跳转 | location.href='m06-p10.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p07 | 5 | 数据与存储 | 页面跳转 | location.href='m06-p11.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p07 | 6 | 显示与外观 | 提示反馈 | notify('当前使用原稿的温暖手帐外观'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p07 | 7 | 语言 | 提示反馈 | notify('当前语言：简体中文'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p07 | 8 | 退出登录 | 页面跳转、弹窗/确认 | if(confirm('退出当前登录？'))location.href='m01-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p08 | 1 | 返回设置 | 页面跳转 | location.href='m06-p07.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p08 | 2 | 修改密码 | 弹窗/确认 | prompt('修改密码：请输入新密码'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p08 | 3 | 绑定手机 | 弹窗/确认 | prompt('绑定手机：请输入手机号'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p08 | 4 | 登录设备 当前设备安全 | 函数调用/需核对上下文 | alert('当前设备安全'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p08 | 5 | 两步验证 | 函数调用/需核对上下文 | alert('两步验证设置将在账号服务接入后开放'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p08 | 6 | 退出登录 | 页面跳转、弹窗/确认 | if(confirm('退出当前登录？'))location.href='m01-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p08 | 7 | 注销账号 | 函数调用/需核对上下文 | alert('账号注销需要完成身份确认'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p09 | 1 | 返回设置 | 页面跳转 | location.href='m06-p07.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p09 | 2 | 默认可见范围 仅自己可见 | 提交/本地保存候选 | ; ()=>{settings.scope=settings.scope==='仅自己可见'?'共同可见':'仅自己可见';save()}; | 跨页数据/返回/异常/触发条件 |
| m06-p09 | 3 | 共同可见 | 提交/本地保存候选 | ; ()=>{settings[button.dataset.key]=!settings[button.dataset.key];save()}; | 跨页数据/返回/异常/触发条件 |
| m06-p09 | 4 | 共同空间 | 提交/本地保存候选 | ; ()=>{settings[button.dataset.key]=!settings[button.dataset.key];save()}; | 跨页数据/返回/异常/触发条件 |
| m06-p09 | 5 | 另一半回应 | 提交/本地保存候选 | ; ()=>{settings[button.dataset.key]=!settings[button.dataset.key];save()}; | 跨页数据/返回/异常/触发条件 |
| m06-p09 | 6 | 相关提醒 | 提交/本地保存候选 | ; ()=>{settings[button.dataset.key]=!settings[button.dataset.key];save()}; | 跨页数据/返回/异常/触发条件 |
| m06-p10 | 1 | 返回设置 | 页面跳转 | location.href='m06-p07.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p10 | 2 | 另一半回应 | 提交/本地保存候选 | ; ()=>{settings[button.dataset.key]=!settings[button.dataset.key];localStorage.setItem(key,JSON.stringify(settings));render()}; | 跨页数据/返回/异常/触发条件 |
| m06-p10 | 3 | 重要时刻 | 提交/本地保存候选 | ; ()=>{settings[button.dataset.key]=!settings[button.dataset.key];localStorage.setItem(key,JSON.stringify(settings));render()}; | 跨页数据/返回/异常/触发条件 |
| m06-p10 | 4 | 时光胶囊 | 提交/本地保存候选 | ; ()=>{settings[button.dataset.key]=!settings[button.dataset.key];localStorage.setItem(key,JSON.stringify(settings));render()}; | 跨页数据/返回/异常/触发条件 |
| m06-p10 | 5 | 工坊完成 | 提交/本地保存候选 | ; ()=>{settings[button.dataset.key]=!settings[button.dataset.key];localStorage.setItem(key,JSON.stringify(settings));render()}; | 跨页数据/返回/异常/触发条件 |
| m06-p10 | 6 | 通知总开关 | 提交/本地保存候选 | ; ()=>{settings[button.dataset.key]=!settings[button.dataset.key];localStorage.setItem(key,JSON.stringify(settings));render()}; | 跨页数据/返回/异常/触发条件 |
| m06-p11 | 1 | 返回设置 | 页面跳转 | location.href='m06-p07.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p11 | 2 | 导出我的记录 | 提示反馈、分享/复制/导出 | ; ()=>{const data={profile:localStorage.getItem('dujia-profile'),privacy:localStorage.getItem('dujia-privacy'),notifications:localStorage.getItem('dujia-notifications')};const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const link=document.createElement('a');link.href=url;link.download='dujia-records.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);notify('已导出本地演示资料')}; | 跨页数据/返回/异常/触发条件 |
| m06-p11 | 3 | 共同记录备份 | 提交/本地保存候选、提示反馈 | ; ()=>{localStorage.setItem('dujia-last-backup',new Date().toISOString());notify('共同记录备份已创建')}; | 跨页数据/返回/异常/触发条件 |
| m06-p11 | 4 | 自动备份 | 状态/内容变化、提交/本地保存候选 | ; ()=>{const value=auto.getAttribute('aria-checked')!=='true';auto.setAttribute('aria-checked',String(value));localStorage.setItem('dujia-auto-backup',String(value))}; | 跨页数据/返回/异常/触发条件 |
| m06-p11 | 5 | 存储空间管理 | 提示反馈 | notify('存储空间：1.2 GB / 5 GB'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p11 | 6 | 清理缓存 128 MB | 状态/内容变化、提示反馈 | ; ()=>{document.querySelector('#cache span').textContent='0 MB';notify('演示缓存已清理')}; | 跨页数据/返回/异常/触发条件 |
| m06-p12 | 1 | 返回我的与设置 | 页面跳转 | location.href='m06-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m06-p12 | 2 | 使用帮助 | 提示反馈 | notify('使用帮助：从首页记录你们的日常，在工坊创作专属作品'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p12 | 3 | 意见反馈 | 函数调用/需核对上下文 | feedback(); ; | 跨页数据/返回/异常/触发条件 |
| m06-p12 | 4 | 隐私政策 | 提示反馈 | notify('隐私政策：你的私人记录由你决定是否共同可见'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p12 | 5 | 用户协议 | 提示反馈 | notify('用户协议：请爱护共同空间中的每一段回忆'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p12 | 6 | 检查更新 | 提示反馈 | notify('当前已是最新版本'); ; | 跨页数据/返回/异常/触发条件 |
| m06-p12 | 7 | 关于独家童话 | 提示反馈 | notify('独家童话 1.0.0 · 把平凡的日子写成童话'); ; | 跨页数据/返回/异常/触发条件 |
| m07-p01 | 1 | 提醒 TA 看看 › | 状态/内容变化、提示反馈 | ; ()=>{const toast=document.querySelector('#toast');toast.textContent='已提醒阿舟查看领养邀请';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2200)}; | 跨页数据/返回/异常/触发条件 |
| m07-p01 | 2 | 暂时返回 | 页面跳转 | location.href='m03-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p02 | 1 | 小狗 | 状态/内容变化 | ; ()=>{kind=button.dataset.kind;document.querySelectorAll('.pet').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p02 | 2 | 小猫 | 状态/内容变化 | ; ()=>{kind=button.dataset.kind;document.querySelectorAll('.pet').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p02 | 3 | 小兔 | 状态/内容变化 | ; ()=>{kind=button.dataset.kind;document.querySelectorAll('.pet').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p02 | 4 | 小狐狸 | 状态/内容变化 | ; ()=>{kind=button.dataset.kind;document.querySelectorAll('.pet').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p02 | 5 | pet-name | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m07-p02 | 6 | 邀请 TA 一起领养 | 页面跳转、状态/内容变化、提交/本地保存候选 | ; ()=>{const name=document.querySelector('#pet-name').value.trim();if(!name){document.querySelector('#pet-name').focus();return}localStorage.setItem('dujia-pet',JSON.stringify({kind,name}));location.href='m07-p01.html'}; | 跨页数据/返回/异常/触发条件 |
| m07-p03 | 1 | 互动 | 页面跳转 | location.href='m07-p06.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p03 | 2 | 喂食 | 页面跳转 | location.href='m07-p08.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p03 | 3 | 任务 | 页面跳转 | location.href='m07-p10.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p03 | 4 | 装扮 | 页面跳转 | location.href='m07-p12.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p03 | 5 | 布置小屋 | 页面跳转 | location.href='m07-p15.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p03 | 6 | 成长故事 | 页面跳转 | location.href='m07-p18.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p03 | 7 | 成就图鉴 | 页面跳转 | location.href='m07-p21.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p03 | 8 | 去互动 › | 页面跳转 | location.href='m07-p06.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p04 | 1 | 照顾指南 | 提示反馈 | notify('一起喂食、互动和布置小屋，照顾你们的小伙伴'); ; | 跨页数据/返回/异常/触发条件 |
| m07-p04 | 2 | 宠物日记 | 提示反馈 | notify('领养后可以记录宠物日记'); ; | 跨页数据/返回/异常/触发条件 |
| m07-p04 | 3 | 领养糯米 | 页面跳转 | location.href='m07-p02.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p04 | 4 | 先看看照顾指南 | 提示反馈 | notify('每天照顾、陪伴与记录，都会成为你们的共同故事'); ; | 跨页数据/返回/异常/触发条件 |
| m07-p05 | 1 | 再玩一次 | 页面跳转 | location.href='m07-p06.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p05 | 2 | 回到小屋 | 页面跳转 | location.href='m07-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p06 | 1 | 摸摸头 精力 -5 · 亲密 +3 | 状态/内容变化 | ; ()=>{selected=button;document.querySelectorAll('.option').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p06 | 2 | 丢球球 精力 -12 · 心情 +8 | 状态/内容变化 | ; ()=>{selected=button;document.querySelectorAll('.option').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p06 | 3 | 讲故事 精力 -8 · 亲密 +6 | 状态/内容变化 | ; ()=>{selected=button;document.querySelectorAll('.option').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p06 | 4 | 送小礼物 消耗 1 份礼物 | 状态/内容变化 | ; ()=>{selected=button;document.querySelectorAll('.option').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p06 | 5 | 和糯米互动 | 页面跳转、提交/本地保存候选 | ; ()=>{const energy=Number(localStorage.getItem('dujia-pet-energy')??82);if(energy<Number(selected.dataset.energy)){location.href='m07-p07.html';return}localStorage.setItem('dujia-pet-energy',String(energy-Number(selected.dataset.energy)));location.href='m07-p05.html'}; | 跨页数据/返回/异常/触发条件 |
| m07-p07 | 1 | 宠物空间 | 页面跳转 | location.href='m07-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p07 | 2 | 成长日记 | 页面跳转 | location.href='m07-p18.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p07 | 3 | 去喂食补充精力 › | 页面跳转 | location.href='m07-p08.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p08 | 1 | 香香狗粮 ×12  饱食 +12 | 状态/内容变化 | ; ()=>{selected=Number(button.dataset.index);document.querySelectorAll('.foods button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p08 | 2 | 爱心小饼干 ×5  饱食 +8 · 心情 +2 | 状态/内容变化 | ; ()=>{selected=Number(button.dataset.index);document.querySelectorAll('.foods button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p08 | 3 | 草莓布丁 ×1  饱食 +20 · 心情 +5 | 状态/内容变化 | ; ()=>{selected=Number(button.dataset.index);document.querySelectorAll('.foods button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p08 | 4 | 喂给糯米 | 页面跳转、状态/内容变化、提交/本地保存候选、提示反馈 | ; ()=>{if(stock[selected]<=0){location.href='m07-p09.html';return}stock[selected]--;satiety=Math.min(100,satiety+[12,8,20][selected]);localStorage.setItem('dujia-food-stock',JSON.stringify(stock));localStorage.setItem('dujia-pet-satiety',String(satiety));const toast=document.querySelector('#toast');toast.textContent='糯米吃得很开心！';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2300);render()}; | 跨页数据/返回/异常/触发条件 |
| m07-p08 | 5 | 去获得更多食物 › | 页面跳转 | location.href='m07-p10.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p09 | 1 | 宠物空间 | 页面跳转 | location.href='m07-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p09 | 2 | 去做任务 | 页面跳转 | location.href='m07-p10.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p10 | 1 | 去给糯米换上 | 页面跳转 | location.href='m07-p12.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p11 | 1 | 每日任务 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.tabs button').forEach(item=>item.setAttribute('aria-selected',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p11 | 2 | 本周约定 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.tabs button').forEach(item=>item.setAttribute('aria-selected',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p11 | 3 | 完成陪糯米互动 | 页面跳转 | location.href='m07-p06.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p11 | 4 | 完成整理小屋 | 页面跳转 | location.href='m07-p15.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p11 | 5 | 去完成下一件事 | 页面跳转 | location.href='m07-p06.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p12 | 1 | 返回宠物小屋 | 页面跳转 | location.href='m07-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p12 | 2 | 衣服 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.tabs button').forEach(item=>item.setAttribute('aria-selected',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p12 | 3 | 配饰 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.tabs button').forEach(item=>item.setAttribute('aria-selected',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p12 | 4 | 小物 | 状态/内容变化 | ; ()=>{document.querySelectorAll('.tabs button').forEach(item=>item.setAttribute('aria-selected',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p12 | 5 | 小花围巾 已拥有 | 状态/内容变化、提示反馈 | ; ()=>{if(button.classList.contains('locked')){notify('这件配饰尚未解锁');return}selected=button;document.querySelectorAll('.item').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p12 | 6 | 格纹蝴蝶结 已拥有 | 状态/内容变化、提示反馈 | ; ()=>{if(button.classList.contains('locked')){notify('这件配饰尚未解锁');return}selected=button;document.querySelectorAll('.item').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p12 | 7 | 星星领结 亲密度 160 | 状态/内容变化、提示反馈 | ; ()=>{if(button.classList.contains('locked')){notify('这件配饰尚未解锁');return}selected=button;document.querySelectorAll('.item').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p12 | 8 | 蜜桃帽子 完成故事解锁 | 状态/内容变化、提示反馈 | ; ()=>{if(button.classList.contains('locked')){notify('这件配饰尚未解锁');return}selected=button;document.querySelectorAll('.item').forEach(item=>item.setAttribute('aria-pressed',String(item===button)))}; | 跨页数据/返回/异常/触发条件 |
| m07-p12 | 9 | 保存这身搭配 | 提交/本地保存候选、提示反馈 | ; ()=>{localStorage.setItem('dujia-pet-outfit',selected.dataset.name);notify('已保存：'+selected.dataset.name)}; | 跨页数据/返回/异常/触发条件 |
| m07-p13 | 1 | 宠物空间 | 页面跳转 | location.href='m07-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p13 | 2 | 去做任务 | 页面跳转 | location.href='m07-p11.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p14 | 1 | 继续布置 | 页面跳转 | location.href='m07-p15.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p14 | 2 | 回到小屋 | 页面跳转 | location.href='m07-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p15 | 1 | 地毯 | 状态/内容变化、提示反馈 | ()=>{if(b.dataset.tab!=='地毯'){tell('“'+b.dataset.tab+'”布置即将开放');return}document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'))}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p15 | 2 | 小床 | 状态/内容变化、提示反馈 | ()=>{if(b.dataset.tab!=='地毯'){tell('“'+b.dataset.tab+'”布置即将开放');return}document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'))}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p15 | 3 | 墙饰 | 状态/内容变化、提示反馈 | ()=>{if(b.dataset.tab!=='地毯'){tell('“'+b.dataset.tab+'”布置即将开放');return}document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'))}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p15 | 4 | 摆件 | 状态/内容变化、提示反馈 | ()=>{if(b.dataset.tab!=='地毯'){tell('“'+b.dataset.tab+'”布置即将开放');return}document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'))}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p15 | 5 | 花朵地毯 已使用 | 状态/内容变化、提交/本地保存候选、提示反馈 | ()=>{if(b.dataset.locked){tell(b.dataset.locked+'后可解锁');return}document.querySelectorAll('.cards button').forEach(x=>{x.setAttribute('aria-pressed',x===b?'true':'false');if(!x.dataset.locked)x.querySelector('small').textContent=x===b?'已选中':'可使用'});localStorage.setItem('fairy-room-rug',b.dataset.item)}; | 跨页数据/返回/异常/触发条件 |
| m07-p15 | 6 | 格纹地毯 可使用 | 状态/内容变化、提交/本地保存候选、提示反馈 | ()=>{if(b.dataset.locked){tell(b.dataset.locked+'后可解锁');return}document.querySelectorAll('.cards button').forEach(x=>{x.setAttribute('aria-pressed',x===b?'true':'false');if(!x.dataset.locked)x.querySelector('small').textContent=x===b?'已选中':'可使用'});localStorage.setItem('fairy-room-rug',b.dataset.item)}; | 跨页数据/返回/异常/触发条件 |
| m07-p15 | 7 | 月亮地毯 亲密度 150 | 状态/内容变化、提交/本地保存候选、提示反馈 | ()=>{if(b.dataset.locked){tell(b.dataset.locked+'后可解锁');return}document.querySelectorAll('.cards button').forEach(x=>{x.setAttribute('aria-pressed',x===b?'true':'false');if(!x.dataset.locked)x.querySelector('small').textContent=x===b?'已选中':'可使用'});localStorage.setItem('fairy-room-rug',b.dataset.item)}; | 跨页数据/返回/异常/触发条件 |
| m07-p15 | 8 | 野餐垫  成就解锁 | 状态/内容变化、提交/本地保存候选、提示反馈 | ()=>{if(b.dataset.locked){tell(b.dataset.locked+'后可解锁');return}document.querySelectorAll('.cards button').forEach(x=>{x.setAttribute('aria-pressed',x===b?'true':'false');if(!x.dataset.locked)x.querySelector('small').textContent=x===b?'已选中':'可使用'});localStorage.setItem('fairy-room-rug',b.dataset.item)}; | 跨页数据/返回/异常/触发条件 |
| m07-p15 | 9 | 保存小屋布置 | 页面跳转、提交/本地保存候选 | ()=>{localStorage.setItem('fairy-room-saved',new Date().toISOString());location.href='m07-p14.html'}; | 跨页数据/返回/异常/触发条件 |
| m07-p16 | 1 | 宠物空间 | 页面跳转 | location.href='m07-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p16 | 2 | 去完成任务 | 页面跳转 | location.href='m07-p11.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p17 | 1 | 宠物空间 | 页面跳转 | location.href='m07-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p17 | 2 | 返回宠物空间 | 页面跳转 | location.href='m07-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p18 | 1 | 查看这一页 › | 页面跳转 | location.href='m07-p19.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p19 | 1 | 写下今天的下一页 | 页面跳转 | location.href='m07-p20.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p20 | 1 | 宠物空间 | 页面跳转 | location.href='m07-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p20 | 2 | 领取奖励 | 状态/内容变化、提交/本地保存候选 | ()=>{localStorage.setItem('fairy-achievement-30','1');b.textContent='已领取奖励'}; | 跨页数据/返回/异常/触发条件 |
| m07-p21 | 1 | 第一次见面  已点亮 | 状态/内容变化 | ()=>{t.textContent=b.dataset.name+' · '+b.querySelector('small').textContent;t.style.display='block';setTimeout(()=>t.style.display='none',2200)}; | 跨页数据/返回/异常/触发条件 |
| m07-p21 | 2 | 默契喂食  已点亮 | 状态/内容变化 | ()=>{t.textContent=b.dataset.name+' · '+b.querySelector('small').textContent;t.style.display='block';setTimeout(()=>t.style.display='none',2200)}; | 跨页数据/返回/异常/触发条件 |
| m07-p21 | 3 | 玩到天黑  已点亮 | 状态/内容变化 | ()=>{t.textContent=b.dataset.name+' · '+b.querySelector('small').textContent;t.style.display='block';setTimeout(()=>t.style.display='none',2200)}; | 跨页数据/返回/异常/触发条件 |
| m07-p21 | 4 | 小屋变新了  已点亮 | 状态/内容变化 | ()=>{t.textContent=b.dataset.name+' · '+b.querySelector('small').textContent;t.style.display='block';setTimeout(()=>t.style.display='none',2200)}; | 跨页数据/返回/异常/触发条件 |
| m07-p21 | 5 | 连续照顾 7 天 进度 5 / 7 | 状态/内容变化 | ()=>{t.textContent=b.dataset.name+' · '+b.querySelector('small').textContent;t.style.display='block';setTimeout(()=>t.style.display='none',2200)}; | 跨页数据/返回/异常/触发条件 |
| m07-p21 | 6 | 亲密搭档 亲密度 128 / 160 | 状态/内容变化 | ()=>{t.textContent=b.dataset.name+' · '+b.querySelector('small').textContent;t.style.display='block';setTimeout(()=>t.style.display='none',2200)}; | 跨页数据/返回/异常/触发条件 |
| m07-p21 | 7 | 去完成今天的照顾 | 页面跳转 | location.href='m07-p11.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p22 | 1 | 装扮 | 页面跳转、状态/内容变化 | ()=>{if(b.dataset.tab==='小屋'){location.href='m07-p15.html';return}if(b.dataset.tab==='纪念物'){location.href='m07-p21.html';return}document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'))}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p22 | 2 | 小屋 | 页面跳转、状态/内容变化 | ()=>{if(b.dataset.tab==='小屋'){location.href='m07-p15.html';return}if(b.dataset.tab==='纪念物'){location.href='m07-p21.html';return}document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'))}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p22 | 3 | 纪念物 | 页面跳转、状态/内容变化 | ()=>{if(b.dataset.tab==='小屋'){location.href='m07-p15.html';return}if(b.dataset.tab==='纪念物'){location.href='m07-p21.html';return}document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'))}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p22 | 4 | 小花围巾 已拥有 | 状态/内容变化、提示反馈 | ()=>tell(b.dataset.name+' · '+b.querySelector('small').textContent); | 跨页数据/返回/异常/触发条件 |
| m07-p22 | 5 | 格纹蝴蝶结 已拥有 | 状态/内容变化、提示反馈 | ()=>tell(b.dataset.name+' · '+b.querySelector('small').textContent); | 跨页数据/返回/异常/触发条件 |
| m07-p22 | 6 | 星星领结 亲密度 160 | 状态/内容变化、提示反馈 | ()=>tell(b.dataset.name+' · '+b.querySelector('small').textContent); | 跨页数据/返回/异常/触发条件 |
| m07-p22 | 7 | 蜜桃帽子 成长故事解锁 | 状态/内容变化、提示反馈 | ()=>tell(b.dataset.name+' · '+b.querySelector('small').textContent); | 跨页数据/返回/异常/触发条件 |
| m07-p22 | 8 | 雨天小斗篷  连续照顾 7 天 | 状态/内容变化、提示反馈 | ()=>tell(b.dataset.name+' · '+b.querySelector('small').textContent); | 跨页数据/返回/异常/触发条件 |
| m07-p22 | 9 | 晚安铃铛  未知 | 状态/内容变化、提示反馈 | ()=>tell(b.dataset.name+' · '+b.querySelector('small').textContent); | 跨页数据/返回/异常/触发条件 |
| m07-p23 | 1 | 返回图鉴 | 页面跳转 | location.href='m07-p22.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p23 | 2 | 去换上 | 页面跳转、状态/内容变化、提交/本地保存候选 | ()=>{localStorage.setItem('fairy-pet-outfit','小花围巾');document.getElementById('wearState').textContent='已穿戴';location.href='m07-p12.html'}; | 跨页数据/返回/异常/触发条件 |
| m07-p23 | 3 | 返回图鉴 | 页面跳转 | location.href='m07-p22.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p24 | 1 | 先导出成长记录 | 分享/复制/导出 | ()=>{const data={title:'糯米的成长故事',day:27,memories:['初次相遇','第一次学会握手','小屋有了新地毯','今天也被好好照顾']};const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));a.download='糯米成长记录.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p24 | 2 | 暂时解除共同照顾 | 状态/内容变化、提示反馈 | ()=>{document.querySelector('.toast').textContent='请在正式应用中完成共同照顾关系变更';document.querySelector('.toast').style.display='block'}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p24 | 3 | 我再想想，返回 | 页面跳转 | location.href='m07-p25.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p25 | 1 | 返回宠物空间 | 页面跳转 | location.href='m07-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p25 | 2 | 共同提醒 每天 20:30 | 状态/内容变化、提交/本地保存候选、提示反馈、弹窗/确认 | ()=>{const v=prompt('每天提醒时间（HH:MM）','20:30');if(v&&/^([01]\d／2[0-3]):[0-5]\d$/.test(v)){document.querySelector('#time small').textContent='每天 '+v;localStorage.setItem('fairy-pet-remind-time',v)}else if(v)tell('请输入 HH:MM 格式')}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p25 | 3 | 共同提醒 | 状态/内容变化、提交/本地保存候选 | ()=>{const on=b.getAttribute('aria-checked')!=='true';b.setAttribute('aria-checked',String(on));b.classList.toggle('off',!on);localStorage.setItem(key,String(on))}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p25 | 4 | 照顾通知 | 函数调用/需核对上下文 | ()=>document.querySelector('.s2').click(); ; | 跨页数据/返回/异常/触发条件 |
| m07-p25 | 5 | 照顾通知 | 状态/内容变化、提交/本地保存候选 | ()=>{const on=b.getAttribute('aria-checked')!=='true';b.setAttribute('aria-checked',String(on));b.classList.toggle('off',!on);localStorage.setItem(key,String(on))}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p25 | 6 | 成长故事自动收录 | 函数调用/需核对上下文 | ()=>document.querySelector('.s3').click(); ; | 跨页数据/返回/异常/触发条件 |
| m07-p25 | 7 | 成长故事自动收录 | 状态/内容变化、提交/本地保存候选 | ()=>{const on=b.getAttribute('aria-checked')!=='true';b.setAttribute('aria-checked',String(on));b.classList.toggle('off',!on);localStorage.setItem(key,String(on))}; ; | 跨页数据/返回/异常/触发条件 |
| m07-p25 | 8 | 导出糯米的成长记录 | 页面跳转 | ()=>location.href='m07-p24.html'; ; | 跨页数据/返回/异常/触发条件 |
| m07-p25 | 9 | 仅我们可见说明 | 提示反馈 | ()=>tell('糯米的成长故事仅对共同照顾的两人可见'); ; | 跨页数据/返回/异常/触发条件 |
| m07-p25 | 10 | 暂时解除共同照顾 不会删除糯米与共同回忆 | 页面跳转 | location.href='m07-p24.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p01 | 1 | 我们的夏天 | 页面跳转 | location.href='m08-p04.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p01 | 2 | 第一次旅行 | 页面跳转 | location.href='m08-p04.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p01 | 3 | 小小日常 | 页面跳转 | location.href='m08-p04.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p01 | 4 | 继续阅读 › | 页面跳转 | location.href='m08-p04.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p01 | 5 | 新建回忆册 | 页面跳转 | location.href='m08-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p02 | 1 | 返回 | 页面跳转 | location.href='m08-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p02 | 2 | 新建第一本回忆册 | 页面跳转 | location.href='m08-p03.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p03 | 1 | 返回回忆册 | 页面跳转 | location.href='m08-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p03 | 2 | 查看并确认素材 | 页面跳转 | location.href='m08-p05.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p03 | 3 | 暂不创建 | 页面跳转 | location.href='m08-p04.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p04 | 1 | 返回 | 页面跳转 | location.href='m08-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p04 | 2 | 书名 | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p04 | 3 | 开始月份 | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p04 | 4 | 结束月份 | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p04 | 5 | 从共同素材开始 | 状态/内容变化 | ()=>document.querySelectorAll('.options button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false')); | 跨页数据/返回/异常/触发条件 |
| m08-p04 | 6 | 空白回忆册 | 状态/内容变化 | ()=>document.querySelectorAll('.options button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false')); | 跨页数据/返回/异常/触发条件 |
| m08-p04 | 7 | 下一步：选择主题 | 页面跳转、状态/内容变化、提交/本地保存候选、提示反馈 | ()=>{const name=document.querySelector('.book-name').value.trim();const dates=[...document.querySelectorAll('.dates input')].map(x=>x.value);if(!name／／!dates[0]／／!dates[1]／／dates[0]>dates[1]／／!/^\d{4}\.(0[1-9]／1[0-2])$/.test(dates[0])／／!/^\d{4}\.(0[1-9]／1[0-2])$/.test(dates[1])){const t=document.querySelector('.toast');t.textContent='请填写书名与有效的日期范围';t.style.display='block';return}localStorage.setItem('fairy-memory-draft',JSON.stringify({name,dates,start:document.querySelector('.options button[aria-pressed=true]').dataset.start}));location.href='m08-p05.html'}; | 跨页数据/返回/异常/触发条件 |
| m08-p05 | 1 | 返回上一步 | 页面跳转 | location.href='m08-p04.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p05 | 2 | 花园午后 | 状态/内容变化 | ()=>document.querySelectorAll('.themes button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false')); | 跨页数据/返回/异常/触发条件 |
| m08-p05 | 3 | 旅行手札 | 状态/内容变化 | ()=>document.querySelectorAll('.themes button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false')); | 跨页数据/返回/异常/触发条件 |
| m08-p05 | 4 | 暖灯日常 | 状态/内容变化 | ()=>document.querySelectorAll('.themes button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false')); | 跨页数据/返回/异常/触发条件 |
| m08-p05 | 5 | 使用封面照片 | 状态/内容变化 | ()=>toggle.setAttribute('aria-checked',toggle.getAttribute('aria-checked')==='true'?'false':'true'); ; | 跨页数据/返回/异常/触发条件 |
| m08-p05 | 6 | 下一步：选择素材 | 页面跳转、提交/本地保存候选 | ()=>{localStorage.setItem('fairy-memory-theme',document.querySelector('.themes button[aria-pressed=true]').dataset.theme);localStorage.setItem('fairy-memory-cover-photo',toggle.getAttribute('aria-checked'));location.href='m08-p06.html'}; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 1 | 返回上一步 | 页面跳转 | location.href='m08-p05.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 2 | 全部 | 状态/内容变化 | ()=>{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'));items.forEach(x=>x.style.display=b.dataset.type==='全部'／／x.dataset.type===b.dataset.type?'block':'none')}; ; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 3 | 日记 | 状态/内容变化 | ()=>{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'));items.forEach(x=>x.style.display=b.dataset.type==='全部'／／x.dataset.type===b.dataset.type?'block':'none')}; ; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 4 | 照片 | 状态/内容变化 | ()=>{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'));items.forEach(x=>x.style.display=b.dataset.type==='全部'／／x.dataset.type===b.dataset.type?'block':'none')}; ; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 5 | 时刻 | 状态/内容变化 | ()=>{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'));items.forEach(x=>x.style.display=b.dataset.type==='全部'／／x.dataset.type===b.dataset.type?'block':'none')}; ; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 6 | 工坊 | 状态/内容变化 | ()=>{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'));items.forEach(x=>x.style.display=b.dataset.type==='全部'／／x.dataset.type===b.dataset.type?'block':'none')}; ; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 7 | 宠物 | 状态/内容变化 | ()=>{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'));items.forEach(x=>x.style.display=b.dataset.type==='全部'／／x.dataset.type===b.dataset.type?'block':'none')}; ; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 8 | 晚霞散步 今天的晚霞 把天空染成了橘粉色， 我们手牵手走在江边， 好像时间都慢了下来。 2024.05.18 晚霞散步  日记 2024.05.18　20:47  共同可见 | 状态/内容变化 | ()=>{b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');update()}; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 9 | 一起看日落  照片 2024.04.21　18:36  共同可见 | 状态/内容变化 | ()=>{b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');update()}; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 10 | 厦门之旅 第一次旅行  重要时刻 2023.10.03 – 10.06  共同可见 | 状态/内容变化 | ()=>{b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');update()}; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 11 | 鼓浪屿的风 都温柔 手作明信片  工坊作品 2024.02.14　15:22  共同可见 | 状态/内容变化 | ()=>{b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');update()}; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 12 | 团子学会握手  宠物 2024.03.09　11:08  共同可见 | 状态/内容变化 | ()=>{b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');update()}; | 跨页数据/返回/异常/触发条件 |
| m08-p06 | 13 | 开始编排 | 页面跳转、状态/内容变化、提交/本地保存候选、提示反馈 | ()=>{const selected=items.filter(x=>x.getAttribute('aria-pressed')==='true').map(x=>x.dataset.title);if(!selected.length){const t=document.querySelector('.toast');t.textContent='请至少选择一份共同素材';t.style.display='block';return}localStorage.setItem('fairy-memory-selected',JSON.stringify(selected));location.href='m08-p07.html'}; | 跨页数据/返回/异常/触发条件 |
| m08-p07 | 1 | 返回素材选择 | 页面跳转 | location.href='m08-p06.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p07 | 2 | 暂不放入 | 页面跳转 | location.href='m08-p06.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p07 | 3 | 放入回忆册 | 页面跳转 | location.href='m08-p08.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p08 | 1 | 返回素材预览 | 页面跳转 | location.href='m08-p07.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p08 | 2 | 2024.04.21　周日 今天一起去了海边， 风很温柔，你在笑， 我也觉得整个世界 都亮了起来。 日记摘录 | 状态/内容变化 | ()=>document.querySelectorAll('.templates button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false')); | 跨页数据/返回/异常/触发条件 |
| m08-p08 | 3 | 那天的晚霞 好美呀～ 照片故事 | 状态/内容变化 | ()=>document.querySelectorAll('.templates button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false')); | 跨页数据/返回/异常/触发条件 |
| m08-p08 | 4 | 我们的重要时刻 2023.05.20 第一次约会 2023.08.10 一起旅行 2024.02.14 确定关系 重要时刻 | 状态/内容变化 | ()=>document.querySelectorAll('.templates button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false')); | 跨页数据/返回/异常/触发条件 |
| m08-p08 | 5 | 一起完成的小作品 工坊作品 | 状态/内容变化 | ()=>document.querySelectorAll('.templates button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false')); | 跨页数据/返回/异常/触发条件 |
| m08-p08 | 6 | 小家伙的成长日记 2个月　　 6个月　　 1岁 宠物成长 | 状态/内容变化 | ()=>document.querySelectorAll('.templates button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false')); | 跨页数据/返回/异常/触发条件 |
| m08-p08 | 7 | · 第三章 · 平凡的日子 也闪闪发光 章节扉页 | 状态/内容变化 | ()=>document.querySelectorAll('.templates button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false')); | 跨页数据/返回/异常/触发条件 |
| m08-p08 | 8 | 使用这个模板 | 页面跳转、提交/本地保存候选 | ()=>{localStorage.setItem('fairy-memory-template',document.querySelector('.templates button[aria-pressed=true]').dataset.template);location.href='m08-p09.html'}; | 跨页数据/返回/异常/触发条件 |
| m08-p09 | 1 | 返回版式选择 | 页面跳转 | location.href='m08-p08.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p09 | 2 | page-title | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p09 | 3 | excerpt | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p09 | 4 | date | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p09 | 5 | message | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p09 | 6 | 换摘录 换一段日记 | 提示反馈 | ()=>tell('可直接编辑书页中的摘录文字'); | 跨页数据/返回/异常/触发条件 |
| m08-p09 | 7 | 换照片 换一张照片 | 页面跳转 | ()=>location.href='m08-p06.html'; | 跨页数据/返回/异常/触发条件 |
| m08-p09 | 8 | 换版式 换一种排版 | 页面跳转 | ()=>location.href='m08-p08.html'; | 跨页数据/返回/异常/触发条件 |
| m08-p09 | 9 | 完成这一页 | 页面跳转、状态/内容变化、提交/本地保存候选、提示反馈 | ()=>{const data={title:document.getElementById('page-title').value.trim(),excerpt:document.getElementById('excerpt').value.trim(),date:document.getElementById('date').value.trim(),message:document.getElementById('message').value.trim()};if(!data.title){tell('请填写书页标题');return}localStorage.setItem('fairy-memory-page',JSON.stringify(data));location.href='m08-p10.html'}; | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 1 | 返回 | 页面跳转 | location.href='m08-p08.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 2 | 预览 | 页面跳转 | location.href='m08-p13.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 3 | 书页标题 | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 4 | 书页日期 | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 5 | 裁剪/替换 | 提示反馈 | ()=>tell('从素材页选择要替换的照片'); | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 6 | 裁剪/替换 | 提示反馈 | ()=>tell('从素材页选择要替换的照片'); | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 7 | 裁剪/替换 | 提示反馈 | ()=>tell('从素材页选择要替换的照片'); | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 8 | 这一页的想法 | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 9 | 完成这一页 | 页面跳转、状态/内容变化、提交/本地保存候选 | ()=>{localStorage.setItem('fairy-memory-photo-page',JSON.stringify({title:document.querySelector('.page-title').value,date:document.querySelector('.date').value,caption:note.value}));location.href='m08-p13.html'}; | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 10 | 添加照片 | 页面跳转、提示反馈 | ()=>b.dataset.tool==='更换模板'?location.href='m08-p08.html':tell(b.dataset.tool+'可在正式应用中使用'); | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 11 | 添加文字 | 页面跳转、提示反馈 | ()=>b.dataset.tool==='更换模板'?location.href='m08-p08.html':tell(b.dataset.tool+'可在正式应用中使用'); | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 12 | 添加贴纸 | 页面跳转、提示反馈 | ()=>b.dataset.tool==='更换模板'?location.href='m08-p08.html':tell(b.dataset.tool+'可在正式应用中使用'); | 跨页数据/返回/异常/触发条件 |
| m08-p10 | 13 | 更换模板 | 页面跳转、提示反馈 | ()=>b.dataset.tool==='更换模板'?location.href='m08-p08.html':tell(b.dataset.tool+'可在正式应用中使用'); | 跨页数据/返回/异常/触发条件 |
| m08-p11 | 1 | 返回版式选择 | 页面跳转 | location.href='m08-p08.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p11 | 2 | 时刻主题 | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p11 | 3 | 日期 | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p11 | 4 | 更换照片 | 提示反馈 | ()=>tell('请在素材页选择新的共同照片'); | 跨页数据/返回/异常/触发条件 |
| m08-p11 | 5 | 选择时刻 › | 页面跳转 | ()=>location.href='m08-p06.html'; | 跨页数据/返回/异常/触发条件 |
| m08-p11 | 6 | 添加一句话 | 状态/内容变化、弹窗/确认 | ()=>{const v=prompt('添加一句话',document.getElementById('quote').innerText);if(v)document.getElementById('quote').textContent='“'+v.replace(/[“”]/g,'')+'”'}; | 跨页数据/返回/异常/触发条件 |
| m08-p11 | 7 | 完成这一页 ♡ | 页面跳转、状态/内容变化、提交/本地保存候选 | ()=>{localStorage.setItem('fairy-memory-moment',JSON.stringify({title:document.querySelector('.moment').value,date:document.querySelector('.date').value,quote:document.getElementById('quote').innerText}));location.href='m08-p13.html'}; | 跨页数据/返回/异常/触发条件 |
| m08-p12 | 1 | 返回版式选择 | 页面跳转 | location.href='m08-p08.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p12 | 2 | 工坊作品 | 状态/内容变化、提示反馈 | ()=>{if(b.dataset.tab==='工坊作品'){tell('工坊作品可在素材页选择');return}document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'))}; ; | 跨页数据/返回/异常/触发条件 |
| m08-p12 | 3 | 宠物成长 | 状态/内容变化、提示反馈 | ()=>{if(b.dataset.tab==='工坊作品'){tell('工坊作品可在素材页选择');return}document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b?'true':'false'))}; ; | 跨页数据/返回/异常/触发条件 |
| m08-p12 | 4 | 成长说明 | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p12 | 5 | 换内容 | 提示反馈 | ()=>{if(b.dataset.action==='添加说明'){document.querySelector('.caption').focus();return}tell(b.dataset.action+'可在素材页选择')}; | 跨页数据/返回/异常/触发条件 |
| m08-p12 | 6 | 换照片 | 提示反馈 | ()=>{if(b.dataset.action==='添加说明'){document.querySelector('.caption').focus();return}tell(b.dataset.action+'可在素材页选择')}; | 跨页数据/返回/异常/触发条件 |
| m08-p12 | 7 | 添加说明 | 提示反馈 | ()=>{if(b.dataset.action==='添加说明'){document.querySelector('.caption').focus();return}tell(b.dataset.action+'可在素材页选择')}; | 跨页数据/返回/异常/触发条件 |
| m08-p12 | 8 | 完成这一页 | 页面跳转、状态/内容变化、提交/本地保存候选 | ()=>{localStorage.setItem('fairy-memory-pet-page',document.querySelector('.caption').value);location.href='m08-p13.html'}; | 跨页数据/返回/异常/触发条件 |
| m08-p13 | 1 | 返回编排 | 页面跳转 | location.href='m08-p09.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p13 | 2 | 01 初遇的心动 | 状态/内容变化、提示反馈 | ()=>{const next=b.nextElementSibling;if(next){b.parentNode.insertBefore(next,b);[...b.parentNode.children].forEach((x,i)=>x.querySelector('strong').textContent=String(i+1).padStart(2,'0'));tell('已调整书页顺序')}else tell('已是本章最后一页')}; | 跨页数据/返回/异常/触发条件 |
| m08-p13 | 3 | 02 一起看日落 | 状态/内容变化、提示反馈 | ()=>{const next=b.nextElementSibling;if(next){b.parentNode.insertBefore(next,b);[...b.parentNode.children].forEach((x,i)=>x.querySelector('strong').textContent=String(i+1).padStart(2,'0'));tell('已调整书页顺序')}else tell('已是本章最后一页')}; | 跨页数据/返回/异常/触发条件 |
| m08-p13 | 4 | 03 记录小美好 | 状态/内容变化、提示反馈 | ()=>{const next=b.nextElementSibling;if(next){b.parentNode.insertBefore(next,b);[...b.parentNode.children].forEach((x,i)=>x.querySelector('strong').textContent=String(i+1).padStart(2,'0'));tell('已调整书页顺序')}else tell('已是本章最后一页')}; | 跨页数据/返回/异常/触发条件 |
| m08-p13 | 5 | 01 夏夜的摩天轮 | 状态/内容变化、提示反馈 | ()=>{const next=b.nextElementSibling;if(next){b.parentNode.insertBefore(next,b);[...b.parentNode.children].forEach((x,i)=>x.querySelector('strong').textContent=String(i+1).padStart(2,'0'));tell('已调整书页顺序')}else tell('已是本章最后一页')}; | 跨页数据/返回/异常/触发条件 |
| m08-p13 | 6 | 02 烟花下的约定 | 状态/内容变化、提示反馈 | ()=>{const next=b.nextElementSibling;if(next){b.parentNode.insertBefore(next,b);[...b.parentNode.children].forEach((x,i)=>x.querySelector('strong').textContent=String(i+1).padStart(2,'0'));tell('已调整书页顺序')}else tell('已是本章最后一页')}; | 跨页数据/返回/异常/触发条件 |
| m08-p13 | 7 | 03 星空下的悄悄话 | 状态/内容变化、提示反馈 | ()=>{const next=b.nextElementSibling;if(next){b.parentNode.insertBefore(next,b);[...b.parentNode.children].forEach((x,i)=>x.querySelector('strong').textContent=String(i+1).padStart(2,'0'));tell('已调整书页顺序')}else tell('已是本章最后一页')}; | 跨页数据/返回/异常/触发条件 |
| m08-p13 | 8 | 新增章节 | 提示反馈 | ()=>tell('新章节可在正式应用中添加'); | 跨页数据/返回/异常/触发条件 |
| m08-p13 | 9 | 保存排列 | 页面跳转、提交/本地保存候选 | ()=>{localStorage.setItem('fairy-memory-order',JSON.stringify([...document.querySelectorAll('.rows button')].map(x=>x.dataset.title)));location.href='m08-p14.html'}; | 跨页数据/返回/异常/触发条件 |
| m08-p14 | 1 | 开始翻阅 | 页面跳转 | location.href='m08-p15.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p14 | 2 | 继续整理 | 页面跳转 | location.href='m08-p13.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 1 | 返回书架 | 页面跳转 | location.href='m08-p01.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 2 | 1. 那天，阳光刚刚好 1 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 3 | 2. 一起吃的第一支冰淇淋 2 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 4 | 3. 藏在风里的喜欢 3 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 5 | 4. 我们的第一张合照 有补页 4 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 6 | 5. 你笑起来真好看 5 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 7 | 6. 夏天的傍晚，晚风很温柔 6 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 8 | 7. 海边的日落与你 7 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 9 | 8. 烟花下许的愿 8 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 10 | 9. 手牵手，走很长很长的路 9 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 11 | 10. 属于我们的歌单 10 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 12 | 11. 一起看过的星星 11 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 13 | 12. 八月，未完待续 12 | 页面跳转 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p15 | 14 | 从第 1 页开始 → | 页面跳转 | location.href='m08-p16.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p16 | 1 | 返回 | 页面跳转 | location.href='m08-p15.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p16 | 2 | 目录 | 页面跳转 | location.href='m08-p17.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p16 | 3 | 书签 | 状态/内容变化、提交/本地保存候选 | ()=>{const yes=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',String(yes));localStorage.setItem('fairy-memory-bookmark-6',String(yes))}; | 跨页数据/返回/异常/触发条件 |
| m08-p16 | 4 | 下一页 | 页面跳转 | location.href='m08-p18.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p17 | 1 | 返回阅读 | 页面跳转 | location.href='m08-p16.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p17 | 2 | 目录 查看全书目录和章节 | 页面跳转 | location.href='m08-p15.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p17 | 3 | 书签 查看和管理我的书签 | 页面跳转 | location.href='m08-p19.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p17 | 4 | 添加补页 在书中添加新的补充页 | 页面跳转 | location.href='m08-p18.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p17 | 5 | 整理这本书 调整页序、重命名、导出等 | 页面跳转 | location.href='m08-p13.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p17 | 6 | 更多设置 阅读偏好、背景音乐等设置 | 页面跳转 | location.href='m08-p21.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p18 | 1 | 返回阅读 | 页面跳转 | location.href='m08-p16.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p18 | 2 | 回到目录 | 页面跳转 | location.href='m08-p15.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p18 | 3 | 写几句话 记录此刻的想法与心情 | 状态/内容变化 | ()=>{selected=b.dataset.kind;document.querySelectorAll('.choices button').forEach(x=>{x.style.color=x===b?'#c26852':'#57341e';x.setAttribute('aria-pressed',String(x===b))})}; | 跨页数据/返回/异常/触发条件 |
| m08-p18 | 4 | 送一个表情 用一个表情传达你的心意 | 状态/内容变化 | ()=>{selected=b.dataset.kind;document.querySelectorAll('.choices button').forEach(x=>{x.style.color=x===b?'#c26852':'#57341e';x.setAttribute('aria-pressed',String(x===b))})}; | 跨页数据/返回/异常/触发条件 |
| m08-p18 | 5 | 附上一张照片 用一张照片定格这份回忆 | 状态/内容变化 | ()=>{selected=b.dataset.kind;document.querySelectorAll('.choices button').forEach(x=>{x.style.color=x===b?'#c26852':'#57341e';x.setAttribute('aria-pressed',String(x===b))})}; | 跨页数据/返回/异常/触发条件 |
| m08-p18 | 6 | 选择回应方式 | 页面跳转、提交/本地保存候选 | ()=>{localStorage.setItem('fairy-memory-supplement-kind',selected);location.href='m08-p19.html'}; | 跨页数据/返回/异常/触发条件 |
| m08-p19 | 1 | 返回补页选择 | 页面跳转 | location.href='m08-p18.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p19 | 2 | 补页文字 | 输入/键盘 | 原生输入；关联行为见源页面 | 跨页数据/返回/异常/触发条件 |
| m08-p19 | 3 | 爱心 | 状态/内容变化 | ()=>{emoji=b.dataset.emoji;showEmoji(b);document.querySelectorAll('.emojis button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))}; | 跨页数据/返回/异常/触发条件 |
| m08-p19 | 4 | 星星 | 状态/内容变化 | ()=>{emoji=b.dataset.emoji;showEmoji(b);document.querySelectorAll('.emojis button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))}; | 跨页数据/返回/异常/触发条件 |
| m08-p19 | 5 | 微笑 | 状态/内容变化 | ()=>{emoji=b.dataset.emoji;showEmoji(b);document.querySelectorAll('.emojis button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))}; | 跨页数据/返回/异常/触发条件 |
| m08-p19 | 6 | 花朵 | 状态/内容变化 | ()=>{emoji=b.dataset.emoji;showEmoji(b);document.querySelectorAll('.emojis button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))}; | 跨页数据/返回/异常/触发条件 |
| m08-p19 | 7 | INPUT | 文件选择、状态/内容变化 | e=>{if(e.target.files.length)document.querySelector('.photo-label').textContent='♥ 已附上照片 ♥'}; | 跨页数据/返回/异常/触发条件 |
| m08-p19 | 8 | 放进回忆书 | 页面跳转、状态/内容变化、提交/本地保存候选 | ()=>{localStorage.setItem('fairy-memory-supplement',JSON.stringify({text:document.querySelector('.message').value,emoji,photo:!!document.querySelector('.photo input').files.length}));location.href='m08-p20.html'}; | 跨页数据/返回/异常/触发条件 |
| m08-p20 | 1 | 返回阅读工具 | 页面跳转 | location.href='m08-p17.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p20 | 2 | 目录 | 页面跳转 | location.href='m08-p15.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p20 | 3 | 书签 | 状态/内容变化、提交/本地保存候选 | ()=>{const yes=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',String(yes));localStorage.setItem('fairy-memory-bookmark-7',String(yes))}; | 跨页数据/返回/异常/触发条件 |
| m08-p21 | 1 | 返回阅读 | 页面跳转 | location.href='m08-p17.html'; ; | 跨页数据/返回/异常/触发条件 |
| m08-p21 | 2 | 修改书名与封面 | 状态/内容变化、提交/本地保存候选、弹窗/确认 | ()=>{if(document.querySelector('.edit-name'))return;const input=document.createElement('input');input.className='edit-name';input.maxLength=20;input.value=book.textContent;input.setAttribute('aria-label','回忆册名称');book.after(input);book.classList.add('hidden');input.focus();input.select();input.onkeydown=e=>{if(e.key==='Enter')input.blur()};input.onblur=()=>{const name=input.value.trim()／／'我们的夏天';book.textContent=name;document.querySelector('.cover-title').textContent=name;document.querySelector('.dialog-title').textContent=`确定删除《${name}》？`;localStorage.setItem('fairy-memory-book-name',name);bo | 跨页数据/返回/异常/触发条件 |
| m08-p21 | 3 | 整理页序 | 页面跳转 | location.href='m08-p13.html'; | 跨页数据/返回/异常/触发条件 |
| m08-p21 | 4 | 归档回忆册 | 状态/内容变化、提交/本地保存候选 | e=>{const archived=e.currentTarget.dataset.archived!=='true';e.currentTarget.dataset.archived=String(archived);e.currentTarget.textContent=archived?'取消归档回忆册':'归档回忆册';localStorage.setItem('fairy-memory-book-archived',String(archived))}; | 跨页数据/返回/异常/触发条件 |
| m08-p21 | 5 | 删除这本回忆册 | 函数调用/需核对上下文 | ()=>showDialog(true); | 跨页数据/返回/异常/触发条件 |
| m08-p21 | 6 | 取消 | 函数调用/需核对上下文 | ()=>showDialog(false); | 跨页数据/返回/异常/触发条件 |
| m08-p21 | 7 | 确认删除 | 页面跳转 | ()=>{localStorage.removeItem('fairy-memory-book-name');localStorage.removeItem('fairy-memory-book-archived');localStorage.removeItem('fairy-memory-supplement');location.href='m08-p02.html'}; | 跨页数据/返回/异常/触发条件 |
