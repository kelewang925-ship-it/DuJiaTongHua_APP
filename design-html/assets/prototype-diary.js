/* Diary collection: lists, drafts, editor, detail and replies share stable IDs. */
(() => {
  const UI=window.PrototypeUI, page=location.pathname.split('/').pop().slice(0,7), KEY='dujia-prototype-records';
  const screen=document.querySelector('.screen'), params=new URLSearchParams(location.search), recordId=params.get('id');
  const nickname=()=>UI.read('dujia-profile',{}).nickname||'小满';
  const date=value=>new Date(value).toLocaleDateString('zh-CN');
  const samples=[
    {id:'sample-diary-1',type:'diary',title:'今天因为一件小事笑了好久',body:'早上出门的时候，阿舟把伞拿反了。我们站在屋檐下笑到不行。有你在身边，普通的日子也闪闪发光呀。',visibility:'shared',mood:'很开心 ▾',status:'published',createdAt:1788220800000,author:'小满',image:'../assets/m03-p08-art.webp',sampleImage:true,comments:[]},
    {id:'sample-diary-2',type:'diary',title:'雨天的火锅',body:'雨天一起吃热热的火锅。',visibility:'shared',mood:'很幸福',status:'published',createdAt:1788134400000,author:'阿舟',comments:[]},
    {id:'sample-diary-3',type:'diary',title:'雨后的那封信',body:'雨停的时候，空气里还带着湿润的味道。我把想说的话都写在了信里。',visibility:'private',mood:'平静',status:'published',createdAt:1787875200000,author:'小满',comments:[]}
  ];
  if(localStorage.getItem(KEY)===null) UI.write(KEY,samples);
  const records=window.PrototypeRecords.all;
  const find=()=>records().find(r=>r.id===(recordId|| (page==='m03-p07'?'sample-diary-3':'sample-diary-1'))&&r.type==='diary');
  const put=window.PrototypeRecords.put,route=window.PrototypeRecords.route;
  document.querySelectorAll('.back').forEach(b=>b.addEventListener('click',()=>UI.back(page==='m03-p06'?'m03-p02.html':'m03-p06.html')));
  function unavailable(){screen.classList.add('prototype-diary-missing');const box=document.createElement('section');box.className='prototype-diary-state';const title=document.createElement('h2');title.textContent='这篇日记已经不在了';const button=document.createElement('button');button.textContent='返回日记列表';button.onclick=()=>UI.go('m03-p06.html',{force:true});box.append(title,button);screen.append(box);}
  if(page==='m03-p05'){
    const form=document.querySelector('#diary'), existing=recordId?find():null;
    if(recordId&&!existing){unavailable();return;}
    let image=existing?.image||null,sampleImage=!!existing?.sampleImage,reading=false;
    const anniversaries=UI.read('dujia-prototype-anniversaries',[]),anniversary=Array.isArray(anniversaries)?anniversaries.find(v=>v.id===params.get('anniversary')):null;
    form.elements.title.value=existing?.title||(anniversary?anniversary.name+'的记录':'');form.elements.title.placeholder='给今天起个名字';form.elements.title.maxLength=60;
    form.elements.body.value=existing?.body||'';form.elements.body.maxLength=5000;
    for(const field of [form.elements.title,form.elements.body])field.addEventListener('input',()=>{if(field.getAttribute('aria-invalid')==='true')UI.fieldError(field,'');});
    if(existing){form.elements.mood.value=existing.mood;form.elements.visibility.value=existing.visibility;}
    const preview=document.querySelector('#preview'), photo=document.querySelector('#preview-image'), file=document.querySelector('#file');
    function paintImage(){preview.hidden=!image;preview.style.display=image?'block':'none';photo.style.background=image&&!sampleImage?`url("${image}") center/cover`:'';}
    paintImage();
    const values=()=>JSON.stringify({title:form.elements.title.value,body:form.elements.body.value,mood:form.elements.mood.value,visibility:form.elements.visibility.value,image});
    const leave=UI.guard(form,{fallback:existing?route(existing):'m03-p06.html',value:values});
    document.querySelector('#remove').onclick=()=>{image=null;sampleImage=false;file.value='';paintImage();};
    document.querySelector('#add-photo').onclick=()=>file.click();
    file.addEventListener('change',async()=>{
      const chosen=file.files[0];if(!chosen)return;
      reading=true;
      try{
        image=await window.PrototypeRecords.readImage(chosen,'diary-image');sampleImage=false;paintImage();
      }catch(error){UI.toast(error.message+'，原照片仍保留','error');file.value='';}finally{reading=false;}
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
        const item={...existing,id:existing?.id||'diary-'+crypto.randomUUID(),type:'diary',title,body,mood:form.elements.mood.value,visibility:form.elements.visibility.value,status,image,sampleImage,author:existing?.author||nickname(),createdAt:existing?.createdAt||Date.now(),updatedAt:Date.now(),comments:existing?.comments||[],anniversaryId:existing?.anniversaryId||anniversary?.id||null};
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
      list.replaceChildren();const all=records().filter(r=>r.type==='diary');
      document.querySelectorAll('[data-tab]').forEach(button=>{const selected=button.dataset.tab===tab;button.classList.toggle('active',selected);button.setAttribute('aria-selected',String(selected));if(button.dataset.tab==='draft')button.textContent='草稿 '+all.filter(r=>r.status==='draft').length;});
      const data=all.filter(r=>(tab==='draft'?r.status==='draft':r.status!=='draft')&&(visibility==='all'||r.visibility===visibility));
      document.querySelector('#filter').setAttribute('aria-label',visibility==='all'?'筛选日记':'筛选日记，已有筛选');
      if(!data.length){const box=document.createElement('div');box.className='prototype-diary-empty';const heading=document.createElement('h2');heading.textContent=visibility!=='all'?'没有符合条件的日记':tab==='draft'?'还没有草稿':'还没有日记';const text=document.createElement('p');text.textContent='从今天的小事开始，留下一页故事。';const button=document.createElement('button');button.textContent=visibility!=='all'?'清除筛选':'写第一篇日记';button.onclick=()=>{if(visibility!=='all'){visibility='all';persist();render();}else UI.go('m03-p05.html');};box.append(heading,text,button);list.append(box);return;}
      for(const item of data){const button=document.createElement('button');button.className='prototype-diary-card';const title=document.createElement('strong');title.textContent=item.title;const body=document.createElement('p');body.textContent=item.body||'还没有写完，继续记录吧';const meta=document.createElement('small');meta.textContent=`${item.author} · ${date(item.createdAt)} · ${item.visibility==='private'?'仅自己可见':'共同可见'}`;button.append(title,body,meta);button.onclick=()=>UI.go(route(item));list.append(button);}
    }
    document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{tab=b.dataset.tab;persist();render();});
    document.querySelector('.write').onclick=()=>UI.go('m03-p05.html');
    document.querySelector('#filter').onclick=async()=>{const label=document.createElement('label');label.textContent='可见范围';const select=document.createElement('select');select.setAttribute('aria-label','可见范围');for(const [value,name]of[['all','全部'],['shared','共同可见'],['private','仅自己可见']]){const opt=document.createElement('option');opt.value=value;opt.textContent=name;select.append(opt);}select.value=visibility;label.append(select);const result=await UI.sheet({title:'筛选日记',content:label,actions:[{label:'应用筛选',value:'apply'},{label:'清除筛选',value:'clear'}]});if(result){visibility=result==='clear'?'all':select.value;persist();render();}};
    const refresh=document.createElement('button');refresh.className='prototype-diary-refresh';refresh.type='button';refresh.textContent='↻';refresh.setAttribute('aria-label','刷新日记');screen.append(refresh);
    let loading=false;
    async function load(){
      if(loading)return;loading=true;refresh.disabled=true;list.replaceChildren();list.setAttribute('aria-busy','true');const message=document.createElement('p');message.setAttribute('role','status');message.textContent='正在打开日记…';list.append(message);
      await new Promise(resolve=>setTimeout(resolve,400));list.removeAttribute('aria-busy');loading=false;refresh.disabled=false;
      if(UI.failNext('diary-load')){list.replaceChildren();const box=document.createElement('div');box.className='prototype-diary-empty';const title=document.createElement('h2');title.textContent='日记暂时打不开';const hint=document.createElement('p');hint.textContent='已经保存的内容还在，可以再试一次。';const retry=document.createElement('button');retry.textContent='重新加载日记';retry.onclick=load;box.append(title,hint,retry);list.append(box);return;}
      render();
    }
    refresh.onclick=load;load();
  }
  if(page==='m03-p07'||page==='m03-p08'){
    let item=find();if(!item){unavailable();return;}
    if(recordId&&(item.status==='draft'||(item.visibility==='private')!==(page==='m03-p07'))){UI.go(route(item),{replace:true,force:true});return;}
    document.querySelector('.title').textContent=item.title;document.querySelector('.meta').textContent=`${item.author} · ${date(item.createdAt)} · ${item.visibility==='private'?'仅自己可见':'共同可见'}`;const body=document.querySelector('.body-text');body.textContent=item.body;body.tabIndex=0;body.setAttribute('role','region');body.setAttribute('aria-label','日记正文');
    const photo=document.querySelector('.photo');
    if(!item.image){photo.classList.add('prototype-diary-no-photo');photo.style.background='#fffaf0';photo.removeAttribute('role');photo.removeAttribute('aria-label');photo.textContent='这一页只留下文字';}
    else if(!item.sampleImage){photo.classList.add('prototype-diary-real-photo');photo.style.background=`url("${item.image}") center/cover`;photo.setAttribute('aria-label','这篇日记保存的照片');}
    document.querySelector('.edit').onclick=()=>UI.go('m03-p05.html?id='+encodeURIComponent(item.id));
    let more=document.querySelector('#more');if(!more){more=document.createElement('button');more.id='more';more.className='prototype-diary-more';more.textContent='•••';more.setAttribute('aria-label','更多操作');screen.append(more);}
    more.onclick=async()=>{
      const action=await UI.sheet({title:'日记操作',actions:[{label:'删除日记',value:'delete',danger:true}]});
      if(action!=='delete')return;const confirmed=await UI.modal({title:'删除这篇日记？',message:'日记和其中的留言将一起删除。',cancel:'取消',confirm:'确认删除'});if(!confirmed)return;
      await UI.busy(more,'删除中…',async()=>{if(UI.failNext('diary-delete'))throw new Error('删除没有完成，请重试');if(!UI.write(KEY,records().filter(r=>r.id!==item.id)))return false;return UI.go('m03-p06.html',{force:true});});
    };
    if(page==='m03-p08'){
      const form=document.querySelector('#message'),input=document.querySelector('#reply'),comments=document.querySelector('[aria-label=留言]');input.maxLength=300;
      comments.classList.add('prototype-diary-comments');
      function paintComments(){comments.replaceChildren();if(!item.comments?.length){const text=document.createElement('p');text.textContent='还没有留言，留下一句温柔的话吧';comments.append(text);}for(const reply of item.comments||[]){const article=document.createElement('article'),author=document.createElement('b'),body=document.createElement('p');author.textContent=reply.author;body.textContent=reply.text;article.append(author,body);comments.append(article);}}
      paintComments();document.querySelector('#emoji').onclick=()=>{input.value=(input.value+' ❤️').slice(0,300);input.focus();};
      form.addEventListener('submit',event=>{event.preventDefault();const text=input.value.trim();if(!text){UI.fieldError(input,'请先写一句话');input.focus();return;}UI.busy(form.querySelector('[type=submit]'),'发送中…',()=>{if(UI.failNext('diary-comment'))throw new Error('留言没有发送成功，请重试');const latest=records().find(r=>r.id===item.id);if(!latest){UI.toast('这篇日记已被删除','error');return false;}const next={...latest,comments:[...(latest.comments||[]),{id:crypto.randomUUID(),author:nickname(),text,createdAt:Date.now()}]};if(!put(next))return false;item=next;input.value='';paintComments();UI.toast('留言已保存','success');return true;});});
      form.dataset.prototypeReady='true';
    }
  }
})();
