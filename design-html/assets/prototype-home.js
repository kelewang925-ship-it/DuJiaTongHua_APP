/* Home and search consume the same records as diary lists and details. */
(() => {
  const UI=window.PrototypeUI,R=window.PrototypeRecords,page=location.pathname.split('/').pop().slice(0,7),screen=document.querySelector('.screen');
  const published=()=>R.all().filter(r=>r.status!=='draft');
  if(page==='m03-p01'||page==='m03-p02'){
    {
      const filled=published().length>0;
      if((page==='m03-p01'&&filled)||(page==='m03-p02'&&!filled)){UI.go(filled?'m03-p02.html':'m03-p01.html',{replace:true,force:true});return;}
    }
    document.querySelector('.date').textContent=new Date().toLocaleDateString('zh-CN',{month:'long',day:'numeric',weekday:'long'});
    const reading=document.querySelector('.reading');if(reading){const books=PrototypePreferences.books().filter(v=>v.status==='published'&&!v.archived).map(v=>({...v,lastPage:v.pages.some(p=>p.id===v.lastPage)?v.lastPage:null})).sort((a,b)=>(b.updatedAt||b.createdAt)-(a.updatedAt||a.createdAt)),book=books.find(v=>v.lastPage&&v.pages.some(p=>p.id===v.lastPage))||books[0];reading.title=book?book.name:'创建回忆册';reading.querySelector('strong').textContent=book?book.name:'故事从第一本回忆册开始';reading.querySelector('small').textContent=book?(book.lastPage?'上次读到第 '+(book.pages.findIndex(p=>p.id===book.lastPage)+1)+' 页':'从目录开始阅读'):'亲手挑选共同片段，整理成册';reading.querySelector('em').textContent=book?'继续阅读 ›':'创建回忆册 ›';reading.onclick=()=>UI.go(book?('m08-p'+(book.lastPage?'16':'15')+'.html?id='+encodeURIComponent(book.id)+(book.lastPage?'&page='+encodeURIComponent(book.lastPage):'')):'m08-p01.html');}
    const anniversaryEntry=document.querySelector('.moment'),dates=window.PrototypeDates;
    if(anniversaryEntry&&dates){
      const stored=UI.read('dujia-prototype-anniversaries',[]);
      const upcoming=(Array.isArray(stored)?stored:[]).map(item=>({item,occurrence:dates.occurrence(item)})).filter(row=>row.occurrence&&row.occurrence.days>=0).sort((a,b)=>a.occurrence.days-b.occurrence.days)[0];
      anniversaryEntry.querySelector('small').textContent=upcoming?`${upcoming.item.name} · ${upcoming.occurrence.days===0?'今天':upcoming.occurrence.days+' 天后'}`:'添加纪念日，记住值得期待的日子';
      anniversaryEntry.querySelector('span').textContent=upcoming?'查看纪念日 ›':'管理纪念日 ›';
      anniversaryEntry.onclick=()=>UI.go(upcoming?`m04-p${upcoming.occurrence.days===0?'11':'10'}.html?id=${encodeURIComponent(upcoming.item.id)}`:'m04-p07.html');
    }
    const pair=UI.read('dujia-prototype-relationship')||{},metValue=pair.profile?.met,match=typeof metValue==='string'&&metValue.match(/(\d{4})\D+(\d{1,2})\D+(\d{1,2})/),met=match&&dates?.parse(dates.iso(+match[1],+match[2],+match[3]));
    let start=pair.bound?met:null,caption='我们已经一起走过';
    if(pair.bound&&!start&&typeof pair.acceptedAt==='number'&&Number.isFinite(pair.acceptedAt)){const at=new Date(pair.acceptedAt);if(Number.isFinite(at.getTime()))start=dates?.parse(dates.iso(at.getFullYear(),at.getMonth()+1,at.getDate()));caption='我们已关联';}
    const counter=document.querySelector('.hero-copy strong'),copy=document.querySelectorAll('.hero-copy p');
    if(counter){counter.textContent=start?Math.max(0,Math.floor((dates.today().time-start.time)/86400000)):'—';if(copy[0])copy[0].textContent=start?caption:pair.bound?'相识日期待补充':'等待一起记录';if(copy[1])copy[1].textContent=start?'天':'';}
    if(page==='m03-p02'){
      const section=document.querySelector('.recent');section.replaceChildren();section.classList.add('prototype-home-recent');
      for(const item of published().sort((a,b)=>(b.updatedAt||b.createdAt)-(a.updatedAt||a.createdAt)).slice(0,3)){
        const button=document.createElement('button');button.className='prototype-home-record';const title=document.createElement('strong');title.textContent=item.title;const meta=document.createElement('small');meta.textContent=`${item.author||'小满'} · ${item.visibility==='private'?'仅自己可见':'共同可见'}`;button.append(title,meta);button.onclick=()=>UI.go(R.route(item));section.append(button);
      }
    }
  }
  if(page==='m03-p03'||page==='m03-p04'){
    const form=document.querySelector('#search'),query=document.querySelector('#query');query.maxLength=100;
    query.value=new URLSearchParams(location.search).get('q')||sessionStorage.getItem('dujia-prototype-last-query')||'';
    if(page==='m03-p03')query.focus();
    function submit(){const text=query.value.trim();if(!text){UI.fieldError(query,'请输入想找的关键词');query.focus();return;}sessionStorage.setItem('dujia-prototype-last-query',text);let recent=UI.read('dujia-prototype-search-history',[]);if(!Array.isArray(recent))recent=[];UI.write('dujia-prototype-search-history',[text,...recent.filter(v=>v!==text)].slice(0,6));UI.go('m03-p04.html?q='+encodeURIComponent(text),{replace:page==='m03-p04'});}
    form.addEventListener('submit',e=>{e.preventDefault();submit();});form.dataset.prototypeReady='true';
    const clear=form.querySelector('button');clear.onclick=()=>{query.value='';query.focus();if(page==='m03-p04'){sessionStorage.removeItem('dujia-prototype-last-query');UI.go('m03-p03.html');}};
    if(page==='m03-p03'){
      const history=UI.read('dujia-prototype-search-history',[]),chips=document.querySelector('.chips');
      if(Array.isArray(history)&&history.length){chips.replaceChildren();for(const text of history){const b=document.createElement('button');b.type='button';b.dataset.query=text;b.textContent=text;b.className='ui-hit-text';chips.append(b);}}
      document.querySelectorAll('[data-query]').forEach(b=>b.onclick=()=>{query.value=b.dataset.query;submit();});
    }else{
      document.querySelectorAll('.section-title,.diary-result,.photo-results,.moment-result').forEach(e=>e.remove());
      const list=document.createElement('section');list.className='prototype-search-results';list.setAttribute('aria-label','搜索结果');screen.append(list);
      async function load(){
        list.replaceChildren();list.setAttribute('aria-busy','true');const loading=document.createElement('p');loading.setAttribute('role','status');loading.textContent='正在翻找回忆…';list.append(loading);await new Promise(resolve=>setTimeout(resolve,400));list.removeAttribute('aria-busy');list.replaceChildren();
        if(UI.failNext('record-search')){const text=document.createElement('p');text.textContent='暂时无法查找，请再试一次';const retry=document.createElement('button');retry.textContent='重试搜索';retry.onclick=load;list.append(text,retry);return;}
        const text=query.value.trim().toLocaleLowerCase();const data=published().filter(item=>['diary','photo'].includes(item.type)&&(!text||(text==='日记'&&item.type==='diary')||(text==='照片'&&item.type==='photo')||[item.title,item.body,item.caption,...(item.tags||[])].join(' ').toLocaleLowerCase().includes(text)));
        const heading=document.createElement('h2');heading.textContent=data.length?`找到 ${data.length} 条记录`:'没有找到相关记录';list.append(heading);
        if(!data.length){const reset=document.createElement('button');reset.textContent='重新搜索';reset.onclick=()=>UI.go('m03-p03.html');list.append(reset);}
        for(const item of data){const button=document.createElement('button');button.className='prototype-diary-card';const title=document.createElement('strong');title.textContent=item.title;const excerpt=document.createElement('p');excerpt.textContent=item.body||item.caption||'';const meta=document.createElement('small');meta.textContent=item.visibility==='private'?'仅自己可见':'共同可见';button.append(title,excerpt,meta);button.onclick=()=>UI.go(R.route(item));list.append(button);}
      }
      load();
    }
  }
})();
