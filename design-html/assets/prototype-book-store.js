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
  const sources=book=>PrototypePreferences.bookSources(book),source=(reference,book)=>PrototypePreferences.bookSource(reference,book),pageView=(page,book)=>PrototypePreferences.bookPageView(page,book);
  const ref=v=>({kind:v.kind,id:v.id});
  function savePage(id,page,expectedPage) {
    const book=requireBook(id);
    if(expectedPage!==undefined&&JSON.stringify(book.pages.find(v=>v.id===page.id)||null)!==JSON.stringify(expectedPage))throw new Error('书页已在另一处更新或删除；当前输入保留，请核对最新内容');
    if(page.source&&!source(page.source,book))throw new Error('素材已不再共同可见，请重新选择');
    if(page.title!==undefined&&(!page.title.trim()||page.title.length>100))throw new Error('书页标题需为1至100字');
    if((page.body||'').length>500)throw new Error('书页正文最多500字');
    if(page.photoSource&&!source(page.photoSource,book))throw new Error('照片已不可见，请重新选择');
    if(page.template==='照片故事'&&!(page.photos||[]).length)throw new Error('请至少选择一张共同照片');if((page.photos||[]).length>3)throw new Error('照片故事页最多三张照片');
    for(const photo of page.photos||[]){if(!source(photo.source,book)?.image)throw new Error('照片已不可见，请替换或移除');const crop=photo.crop||{x:50,y:50,zoom:1};if(!Number.isFinite(crop.x)||crop.x<0||crop.x>100||!Number.isFinite(crop.y)||crop.y<0||crop.y>100||!Number.isFinite(crop.zoom)||crop.zoom<1||crop.zoom>2)throw new Error('裁剪参数无效，请重新裁剪');}
    if(page.date!==undefined&&!D.parse(page.date))throw new Error('请填写有效的YYYY-MM-DD日期');
    const saved={...page,id:page.id||'page-'+crypto.randomUUID()},index=book.pages.findIndex(v=>v.id===saved.id);
    if(saved.source&&source(saved.source,book))delete saved.sourceUnavailable;
    if(index<0)book.pages.push(saved);else book.pages[index]=saved;
    if(!book.chapters.length)book.chapters.push({id:'chapter-'+crypto.randomUUID(),name:'我们的故事'});
    saved.chapterId=saved.chapterId||book.chapters[0].id;
    return put(book,'book-page')?saved:null;
  }
  const sameSource=(a,b)=>a?.kind===b?.kind&&a?.id===b?.id;
  const pending=book=>(book.selected||[]).filter(ref=>!book.pages.some(page=>sameSource(page.source,ref))&&!(book.skipped||[]).some(v=>sameSource(v,ref)));
  const skipSource=(id,ref)=>change(id,book=>{book.skipped=book.skipped||[];if(!book.skipped.some(v=>sameSource(v,ref)))book.skipped.push(ref);},'book-skip');
  function structure(id,chapters,pages,expectedUpdatedAt){return change(id,book=>{
    if(expectedUpdatedAt!==undefined&&book.updatedAt!==expectedUpdatedAt)throw new Error('回忆册已在另一处更新；当前编排保留，请核对最新内容再保存');
    if(new Set(chapters.map(v=>v.id)).size!==chapters.length||chapters.some(v=>!v.id||!v.name.trim()||v.name.length>20))throw new Error('章节需要不同ID和1至20字名称');
    if(new Set(pages.map(v=>v.id)).size!==pages.length||pages.some(v=>!v.id||!chapters.some(c=>c.id===v.chapterId)))throw new Error('每页必须属于一个现有章节');
    const removed=book.pages.filter(v=>!pages.some(p=>p.id===v.id));
    book.selected=(book.selected||[]).filter(ref=>!removed.some(v=>sameSource(v.source,ref))||pages.some(v=>sameSource(v.source,ref)));
    book.chapters=chapters;book.pages=chapters.flatMap(chapter=>pages.filter(v=>v.chapterId===chapter.id));book.status='published';
    book.bookmarks=(book.bookmarks||[]).filter(pageId=>pages.some(v=>v.id===pageId));if(book.lastPage&&!pages.some(v=>v.id===book.lastPage))book.lastPage=book.pages[0]?.id||null;
  },'book-publish');}
  const bookmark=(id,pageId)=>change(id,book=>{if(!book.pages.some(v=>v.id===pageId))throw new Error('书页不存在');const list=book.bookmarks||[];book.bookmarks=list.includes(pageId)?list.filter(v=>v!==pageId):[...list,pageId];},'book-bookmark');
  const read=(id,pageId)=>change(id,book=>{if(!book.pages.some(v=>v.id===pageId))throw new Error('书页不存在');book.lastPage=pageId;},'book-read');
  function supplement(id,pageId,data){return change(id,book=>{const page=book.pages.find(v=>v.id===pageId);if(!page||pageView(page,book).blocked)throw new Error('这页已不可见，请返回目录');if(!PrototypePreferences.privacy().replies)throw new Error('共同回应已关闭，请在隐私设置中开启');if((data.text||'').length>500)throw new Error('补页文字最多500字');if(data.kind==='写几句话'&&!data.text?.trim())throw new Error('请写下补页文字');if(data.kind==='送一个表情'&&!data.emoji)throw new Error('请选择表情');if(data.kind==='附上一张照片'&&!data.image)throw new Error('请先附上可以打开的照片');if(data.image&&!/^data:image\//.test(data.image))throw new Error('照片尚未读取完成');page.supplements=page.supplements||[];page.supplements.push({...data,id:crypto.randomUUID(),author:PrototypePreferences.profile().nickname,date:D.today().iso});},'book-supplement');}
  const exported=id=>PrototypePreferences.bookExport(requireBook(id));
  function download(id){if(UI.failNext('book-export'))throw new Error('导出未完成，请重试');const book=exported(id),a=document.createElement('a'),url=URL.createObjectURL(new Blob([JSON.stringify({format:'dujia-book-v1',book},null,2)],{type:'application/json'}));a.href=url;a.download=book.name+'.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  window.PrototypeBooks={key:KEY,all,find,requireBook,put,change,remove,month,draft,sources,ref,source,pageView,savePage,sameSource,pending,skipSource,structure,bookmark,read,supplement,exported,download};
})();
