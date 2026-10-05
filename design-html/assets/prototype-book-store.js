/* Small book repository. Source content is resolved at read time. */
(() => {
  const UI=PrototypeUI,R=PrototypeRecords,D=PrototypeDates,KEY='dujia-prototype-books';
  const all=()=>{const rows=UI.read(KEY,[]);return Array.isArray(rows)?rows:[];};
  const find=id=>all().find(v=>v.id===id);
  const requireBook=id=>{const book=find(id);if(!book)throw new Error('这本回忆册已不存在，请返回书架');return book;};
  function put(book,operation='book-save') {
    if(UI.failNext(operation))throw new Error('保存未完成，请保留输入后重试');
    const rows=all(),index=rows.findIndex(v=>v.id===book.id),next={...book,updatedAt:Date.now()};
    if(index<0)rows.unshift(next);else rows[index]=next;
    return UI.write(KEY,rows)?next:null;
  }
  function change(id,fn,operation){const book=requireBook(id);fn(book);return put(book,operation);}
  function remove(id){requireBook(id);if(UI.failNext('book-delete'))throw new Error('删除未完成，请重试');return UI.write(KEY,all().filter(v=>v.id!==id));}
  const month=value=>/^[1-9]\d{3}\.(0[1-9]|1[0-2])$/.test(value);
  function draft({name,dates,start}) {
    if(!name.trim()||name.trim().length>20)throw new Error('书名需为1至20字');
    if(!dates.every(month)||dates[0]>dates[1])throw new Error('请填写有效的起止月份，例如2026.10');
    return {id:'book-'+crypto.randomUUID(),name:name.trim(),dates,start,theme:'花园午后',coverPhoto:false,status:'draft',chapters:[],pages:[],selected:[],bookmarks:[],lastPage:null,archived:false,createdAt:Date.now()};
  }
  const values=key=>{const rows=UI.read(key,[]);return Array.isArray(rows)?rows:[];};
  function sources(book=null) {
    const records=R.all().filter(v=>v.status!=='draft'&&v.visibility==='shared');
    const result=records.map(v=>({kind:v.type,id:v.id,title:v.title,body:v.body||v.caption||'',image:v.image||null,date:v.date,url:R.route(v)}));
    for(const v of values('dujia-prototype-moments').filter(v=>v.visibility!=='private'&&v.status!=='draft'))result.push({kind:'moment',id:v.id,title:v.name,body:v.story||'',image:v.cover||null,date:v.date,url:'m04-p03.html?id='+encodeURIComponent(v.id)});
    for(const v of values('dujia-prototype-works').filter(v=>v.status==='ready')) {
      if(v.sourceKind!=='free'&&v.sourceIds?.length&&!v.sourceIds.every(id=>v.sourceKind==='moment'?result.some(s=>s.kind==='moment'&&s.id===id):records.some(s=>s.id===id)))continue;
      result.push({kind:'work',id:v.id,title:v.name,body:v.story||'',image:records.find(s=>v.sourceIds?.includes(s.id))?.image||null,date:new Date(v.completedAt||v.createdAt).toISOString().slice(0,10),url:'m05-p08.html?id='+encodeURIComponent(v.id)});
    }
    const pet=UI.read('dujia-prototype-pet');
    if(pet?.status==='active'&&window.PrototypePetLife)for(const entry of PrototypePetLife.stories(pet).filter(v=>!v.blocked))result.push({kind:'pet',id:pet.id+':'+entry.id,title:entry.text,body:entry.body||entry.text,date:entry.date,url:'m07-p19.html?id='+encodeURIComponent(entry.id)});
    return result.filter(v=>{if(!book)return true;const m=(v.date||'').slice(0,7).replace('-','.');return month(m)&&m>=book.dates[0]&&m<=book.dates[1];});
  }
  const ref=v=>({kind:v.kind,id:v.id});
  const source=(reference,book)=>reference?sources(book).find(v=>v.kind===reference.kind&&v.id===reference.id):null;
  function pageView(page,book) {
    const linked=page.source?source(page.source,book):null,blocked=!!page.source&&!linked;
    return {...page,title:page.title??linked?.title??(blocked?'关联内容不可见':'新的一页'),body:page.body??linked?.body??'',date:page.date??linked?.date??D.today().iso,image:page.image??linked?.image??null,blocked,url:linked?.url||null,supplements:blocked?[]:page.supplements||[]};
  }
  function savePage(id,page) {
    const book=requireBook(id);
    if(page.source&&!source(page.source,book))throw new Error('素材已不再共同可见，请重新选择');
    if(page.title!==undefined&&(!page.title.trim()||page.title.length>100))throw new Error('书页标题需为1至100字');
    if((page.body||'').length>500)throw new Error('书页正文最多500字');
    const saved={...page,id:page.id||'page-'+crypto.randomUUID()},index=book.pages.findIndex(v=>v.id===saved.id);
    if(index<0)book.pages.push(saved);else book.pages[index]=saved;
    if(!book.chapters.length)book.chapters.push({id:'chapter-'+crypto.randomUUID(),name:'我们的故事'});
    saved.chapterId=saved.chapterId||book.chapters[0].id;
    return put(book,'book-page')?saved:null;
  }
  function structure(id,chapters,pages){return change(id,book=>{book.chapters=chapters;book.pages=pages;book.status='published';},'book-publish');}
  const bookmark=(id,pageId)=>change(id,book=>{if(!book.pages.some(v=>v.id===pageId))throw new Error('书页不存在');const list=book.bookmarks||[];book.bookmarks=list.includes(pageId)?list.filter(v=>v!==pageId):[...list,pageId];},'book-bookmark');
  const read=(id,pageId)=>change(id,book=>{if(!book.pages.some(v=>v.id===pageId))throw new Error('书页不存在');book.lastPage=pageId;},'book-read');
  function supplement(id,pageId,data){return change(id,book=>{const page=book.pages.find(v=>v.id===pageId);if(!page||pageView(page,book).blocked)throw new Error('这页已不可见，请返回目录');if(!data.text?.trim()&&!data.image&&!data.emoji)throw new Error('请写文字、选择表情或附上照片');page.supplements=page.supplements||[];page.supplements.push({...data,id:crypto.randomUUID(),author:PrototypePreferences.profile().nickname,date:D.today().iso});},'book-supplement');}
  function exported(id){const book=requireBook(id);return {...book,selected:[],pages:book.pages.map(page=>{const view=pageView(page,book);if(view.blocked)return {id:page.id,chapterId:page.chapterId,template:page.template,source:page.source,title:page.title||'关联内容不可见',body:page.body||'',date:page.date||'',supplements:[]};return {...page,title:view.title,body:view.body,date:view.date,image:view.image};})};}
  function download(id){if(UI.failNext('book-export'))throw new Error('导出未完成，请重试');const book=exported(id),a=document.createElement('a'),url=URL.createObjectURL(new Blob([JSON.stringify({format:'dujia-book-v1',book},null,2)],{type:'application/json'}));a.href=url;a.download=book.name+'.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  window.PrototypeBooks={key:KEY,all,find,requireBook,put,change,remove,month,draft,sources,ref,source,pageView,savePage,structure,bookmark,read,supplement,exported,download};
})();
