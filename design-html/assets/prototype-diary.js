/* Diary collection: lists, drafts, editor, detail and replies share stable IDs. */
(() => {
  const UI=window.PrototypeUI, page=location.pathname.split('/').pop().slice(0,7), KEY='dujia-prototype-records';
  const screen=document.querySelector('.screen'), params=new URLSearchParams(location.search), recordId=params.get('id');
  const nickname=()=>UI.read('dujia-profile',{}).nickname||'小满';
  const date=value=>{const parsed=new Date(value);return Number.isNaN(parsed.getTime())?'日期未记录':parsed.toLocaleDateString('zh-CN');};
  const records=window.PrototypeRecords.all;
  const find=()=>records().find(r=>r.id===(recordId|| (page==='m03-p07'?'sample-diary-3':'sample-diary-1'))&&r.type==='diary');
  const put=window.PrototypeRecords.put,route=window.PrototypeRecords.route;
  document.querySelectorAll('.back').forEach(b=>b.addEventListener('click',()=>page==='m03-p06'?UI.go('m03-p02.html',{replace:true}):page==='m03-p07'||page==='m03-p08'?UI.go('m03-p06.html',{replace:true}):UI.back('m03-p06.html')));
  function unavailable(blocked=false){screen.classList.add('prototype-diary-missing');const box=UI.components.state({kind:'error',title:blocked?'这篇日记暂不可见':'这篇日记已经不在了',message:'内容可能已被删除，回到日记列表可以继续记录。',action:'返回日记列表',onAction:()=>UI.go('m03-p06.html',{force:true})});box.classList.add('prototype-diary-state');screen.append(box);}
  if(page==='m03-p05'){
    const form=document.querySelector('#diary'), existing=recordId?find():null;
    if(recordId&&!existing){unavailable();return;}if(existing&&!PrototypePreferences.canView('record',existing)){unavailable(true);return;}
    let image=existing?.image||null,sampleImage=!!existing?.sampleImage,reading=false;
    const anniversaries=UI.read('dujia-prototype-anniversaries',[]),anniversary=Array.isArray(anniversaries)?anniversaries.find(v=>v.id===params.get('anniversary')):null;
    form.elements.title.value=existing?.title||(anniversary?anniversary.name+'的记录':'');form.elements.title.placeholder='给今天起个名字';form.elements.title.maxLength=60;
    form.elements.body.value=existing?.body||'';form.elements.body.maxLength=5000;
    for(const field of [form.elements.title,form.elements.body])field.addEventListener('input',()=>{if(field.getAttribute('aria-invalid')==='true')UI.fieldError(field,'');});
    if(existing){form.elements.mood.value=existing.mood;form.elements.visibility.value=existing.visibility;}else form.elements.visibility.value=window.PrototypePreferences?.privacy().scope==='仅自己可见'?'private':'shared';if(window.PrototypePreferences?.privacy().shared===false){const sharedOption=form.querySelector('[name=visibility][value=shared],option[value=shared]');if(sharedOption)sharedOption.disabled=true;if(!existing)form.elements.visibility.value='private';}
    const preview=document.querySelector('#preview'), photo=document.querySelector('#preview-image'), file=document.querySelector('#file');
    function paintImage(){preview.hidden=!image;preview.style.display=image?'block':'none';photo.style.background=image&&!sampleImage?`url("${image}") center/cover`:'';}
    paintImage();
    const values=()=>JSON.stringify({title:form.elements.title.value,body:form.elements.body.value,mood:form.elements.mood.value,visibility:form.elements.visibility.value,image,reading});
    const leave=UI.guard(form,{fallback:existing?route(existing):'m03-p06.html',value:values,onDiscard:()=>imageReader.cancel()});
    document.querySelector('#remove').onclick=()=>{image=null;sampleImage=false;imageReader.cancel();file.value='';paintImage();};
    document.querySelector('#add-photo').onclick=()=>file.click();
    const imageReader=window.PrototypeRecords.imageInput(file,'diary-image',{
      onValue:value=>{image=value;sampleImage=false;paintImage();},
      onError:error=>{UI.toast(error.message+'，原照片仍保留','error');file.value='';},
      onBusy:value=>{reading=value;}
    });
    let saving=false;
    async function save(status,button){
      if(saving)return;if(reading){UI.toast('照片正在读取，请稍候');return;}
      const title=form.elements.title.value.trim(),body=form.elements.body.value.trim();
      if(!title){UI.fieldError(form.elements.title,'请填写日记标题');form.elements.title.focus();return;}
      if(status==='published'&&!body){UI.fieldError(form.elements.body,'请写下今天的故事');form.elements.body.focus();return;}
      saving=true;document.querySelectorAll('#top-save,#diary .submit').forEach(b=>{if(b!==button)b.disabled=true;});
      await UI.busy(button,status==='draft'?'保存草稿中…':'保存中…',async()=>{
        if(UI.failNext('diary-save'))throw new Error('日记没有保存成功，请重试，内容仍保留');
        const current=existing?UI.currentItem(KEY,existing):null;if(existing&&!current)return false;if(current&&!PrototypePreferences.canView('record',current))throw new Error('这篇日记暂不可见，当前输入仍保留');
        const item={...current,id:existing?.id||'diary-'+crypto.randomUUID(),type:'diary',title,body,mood:form.elements.mood.value,visibility:form.elements.visibility.value,status,image,sampleImage,author:current?.author||nickname(),createdAt:current?.createdAt||Date.now(),updatedAt:Date.now(),comments:current?.comments||[],anniversaryId:current?.anniversaryId||anniversary?.id||null};
        if(!put(item))return false;leave.commit();UI.toast(status==='draft'?'草稿已保存':'日记已保存','success');
        if(existing?.status!=='published'||status!=='published')sessionStorage.setItem('dujia-diary-list-state',JSON.stringify({tab:status==='draft'?'draft':'all',visibility:'all'}));
        return UI.go(existing?.status==='published'&&status==='published'?route(item):'m03-p06.html',{force:true});
      });
      saving=false;document.querySelectorAll('#top-save,#diary .submit').forEach(b=>b.disabled=false);
    }
    document.querySelector('#top-save').textContent='存草稿';document.querySelector('#top-save').onclick=()=>save('draft',document.querySelector('#top-save'));
    form.addEventListener('submit',event=>{event.preventDefault();save('published',form.querySelector('.submit'));});
    form.dataset.prototypeReady='true';
  }
  if(page==='m03-p06'){
    document.querySelectorAll('.card').forEach(e=>e.remove());document.querySelector('.month').textContent='珍藏每一天';
    const list=document.createElement('section');list.className='prototype-diary-list';list.setAttribute('aria-label','日记列表');screen.append(list);
    let state;try{state=JSON.parse(sessionStorage.getItem('dujia-diary-list-state')||'null');}catch{}
    let tab=state?.tab||'all',visibility=state?.visibility||'all';
    const persist=()=>sessionStorage.setItem('dujia-diary-list-state',JSON.stringify({tab,visibility}));
    function render(){
      list.replaceChildren();const all=PrototypePreferences.visibleRecords().filter(r=>r.type==='diary');
      document.querySelectorAll('[data-tab]').forEach(button=>{const selected=button.dataset.tab===tab;button.classList.toggle('active',selected);button.setAttribute('aria-selected',String(selected));if(button.dataset.tab==='draft')button.textContent='草稿 '+all.filter(r=>r.status==='draft').length;});
      const data=all.filter(r=>(tab==='draft'?r.status==='draft':r.status!=='draft')&&(visibility==='all'||r.visibility===visibility));
      document.querySelector('#filter').setAttribute('aria-label',visibility==='all'?'筛选日记':'筛选日记，已有筛选');
      if(!data.length){const box=UI.components.state({title:visibility!=='all'?'没有符合条件的日记':tab==='draft'?'还没有草稿':'还没有日记',message:'从今天的小事开始，留下一页故事。',action:visibility!=='all'?'清除筛选':'写第一篇日记',onAction:()=>{if(visibility!=='all'){visibility='all';persist();render();}else UI.go('m03-p05.html');}});box.classList.add('prototype-diary-empty');list.append(box);return;}
      for(const item of data){const button=UI.components.card({content:[],onClick:()=>UI.go(route(item))});button.classList.add('prototype-diary-card');const title=document.createElement('strong');title.textContent=item.title;const body=document.createElement('p');body.textContent=item.body||'还没有写完，继续记录吧';const meta=document.createElement('small');meta.textContent=`${item.author} · ${date(item.date??item.createdAt)} · ${item.visibility==='private'?'仅自己可见':'共同可见'}`;button.append(title,body,meta);window.PrototypeRecordPresentation?.decorate(button,item,'diary');list.append(button);}
    }
    document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{tab=b.dataset.tab;persist();render();});
    document.querySelector('.write').onclick=()=>UI.go('m03-p05.html');
    document.querySelector('#filter').onclick=async()=>{const label=document.createElement('label');label.textContent='可见范围';const select=document.createElement('select');select.setAttribute('aria-label','可见范围');for(const [value,name]of[['all','全部'],['shared','共同可见'],['private','仅自己可见']]){const opt=document.createElement('option');opt.value=value;opt.textContent=name;select.append(opt);}select.value=visibility;label.append(select);const result=await UI.sheet({title:'筛选日记',content:label,actions:[{label:'应用筛选',value:'apply'},{label:'清除筛选',value:'clear'}]});if(result){visibility=result==='clear'?'all':select.value;persist();render();}};
    const refresh=document.createElement('button');refresh.className='prototype-diary-refresh';refresh.type='button';refresh.textContent='↻';refresh.setAttribute('aria-label','刷新日记');screen.append(refresh);
    let loading=false;
    async function load(){
      if(loading)return;loading=true;refresh.disabled=true;list.replaceChildren();list.setAttribute('aria-busy','true');list.append(UI.components.loading({mode:'skeleton',label:'正在打开日记…'}));
      await new Promise(resolve=>setTimeout(resolve,400));list.removeAttribute('aria-busy');loading=false;refresh.disabled=false;
      if(UI.failNext('diary-load')){list.replaceChildren();const box=UI.components.state({kind:'error',title:'日记暂时打不开',message:'已经保存的内容还在，可以再试一次。',action:'重新加载日记',onAction:load});box.classList.add('prototype-diary-empty');list.append(box);return;}
      render();
    }
    refresh.onclick=load;load();
  }
  if(page==='m03-p07'||page==='m03-p08'){
    let item=find();if(!item){unavailable();return;}if(!PrototypePreferences.canView('record',item)){unavailable(true);return;}
    if(recordId&&(item.status==='draft'||(item.visibility==='private')!==(page==='m03-p07'))){UI.go(route(item),{replace:true,force:true});return;}
    document.querySelector('.title').textContent=item.title;document.querySelector('.meta').textContent=`${item.author} · ${date(item.date??item.createdAt)} · ${item.visibility==='private'?'仅自己可见':'共同可见'}`;const body=document.querySelector('.body-text');body.textContent=item.body;body.tabIndex=0;body.setAttribute('role','region');body.setAttribute('aria-label','日记正文');
    const photo=document.querySelector('.photo');
    if(!item.image){photo.classList.add('prototype-diary-no-photo');photo.style.background='#fffaf0';photo.removeAttribute('role');photo.removeAttribute('aria-label');photo.textContent='这一页只留下文字';}
    else if(!item.sampleImage){photo.classList.add('prototype-diary-real-photo');photo.style.background=`url("${item.image}") center/cover`;photo.setAttribute('aria-label','这篇日记保存的照片');}
    document.querySelector('.edit').onclick=()=>UI.go('m03-p05.html?id='+encodeURIComponent(item.id));
    let more=document.querySelector('#more');if(!more){more=document.createElement('button');more.id='more';more.className='prototype-diary-more';more.textContent='•••';more.setAttribute('aria-label','更多操作');screen.append(more);}
    more.onclick=async()=>{
      const action=await UI.sheet({title:'日记操作',actions:[{label:'删除日记',value:'delete',danger:true}]});
      if(action!=='delete')return;const confirmed=await UI.modal({title:'删除这篇日记？',message:'日记和其中的留言将一起删除。',cancel:'取消',confirm:'确认删除', danger: true});if(!confirmed)return;
      await UI.busy(more,'删除中…',async()=>{if(UI.failNext('diary-delete'))throw new Error('删除没有完成，请重试');if(!UI.write(KEY,records().filter(r=>r.id!==item.id)))return false;return UI.go('m03-p06.html',{force:true});});
    };
    if(page==='m03-p08'){
      const form=document.querySelector('#message'),input=document.querySelector('#reply'),comments=document.querySelector('[aria-label=留言]');input.maxLength=300;if(window.PrototypePreferences?.privacy().replies===false){input.disabled=true;form.querySelector('[type=submit]').disabled=true;input.placeholder='新的回应已关闭';}
      comments.classList.add('prototype-diary-comments');const replyLeave=UI.guard(form,{fallback:'m03-p06.html'});document.querySelector('#emoji').disabled=input.disabled;
      function paintComments(){comments.replaceChildren();if(!item.comments?.length){const text=document.createElement('p');text.textContent='还没有留言，留下一句温柔的话吧';comments.append(text);}for(const reply of item.comments||[]){const article=document.createElement('article'),author=document.createElement('b'),body=document.createElement('p');const name=typeof reply.author==='string'&&reply.author.trim()?reply.author:'访客',avatar=UI.components.avatar({name}),heading=document.createElement('div');heading.className='prototype-comment-author';avatar.setAttribute('aria-hidden','true');author.textContent=name;body.textContent=reply.text;heading.append(avatar,author);article.append(heading,body);comments.append(article);}}
      paintComments();document.querySelector('#emoji').onclick=()=>{input.value=(input.value+' ❤️').slice(0,300);input.focus();};
      form.addEventListener('submit',event=>{event.preventDefault();if(window.PrototypePreferences?.privacy().replies===false){UI.toast('新的回应已关闭');return;}const text=input.value.trim();if(!text){UI.fieldError(input,'请先写一句话');input.focus();return;}UI.busy(form.querySelector('[type=submit]'),'发送中…',()=>{if(UI.failNext('diary-comment'))throw new Error('留言没有发送成功，请重试');const latest=records().find(r=>r.id===item.id);if(!latest){UI.toast('这篇日记已被删除','error');return false;}if(!PrototypePreferences.sharedContent('record',latest)){UI.toast('这篇日记不再共同可见，未发送文字保留','error');return false;}const next={...latest,comments:[...(latest.comments||[]),{id:crypto.randomUUID(),author:nickname(),text,createdAt:Date.now()}]};if(!put(next))return false;item=next;input.value='';replyLeave.commit();paintComments();UI.toast('留言已保存','success');return true;});});
      form.dataset.prototypeReady='true';
    }
  }
})();
