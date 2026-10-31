/* Uncommitted chapter/page arrangement, persisted in one guarded transaction. */
(() => {
 function render(ctx,current){
  const {UI,B,all,id,book,text,go,bind,button,panel,row,blank,back,edit}=ctx;
  back(6);all('.chapter,.rows,.number').forEach(e=>e.hidden=true);
  let chapters=structuredClone(current.chapters),pages=structuredClone(current.pages);
  const list=panel('book-panel book-structure'),guard=UI.guard(document.querySelector('.screen'),{fallback:'m08-p15.html?id='+id,value:()=>JSON.stringify([chapters,pages])});
  const moveChapter=(chapter,direction)=>{const index=chapters.indexOf(chapter),target=index+direction;if(target<0||target>=chapters.length){UI.toast('已经在章节边界');return;}[chapters[index],chapters[target]]=[chapters[target],chapters[index]];paint();};
  async function chapterMenu(chapter){
   const action=await UI.sheet({title:chapter.name+' · 章节操作',actions:[{label:'修改章节名',value:'rename'},{label:'上移章节',value:'up'},{label:'下移章节',value:'down'},{label:'删除章节',value:'delete',danger:true}]});
   if(action==='rename')return edit('章节名','章节名',chapter.name,name=>{chapter.name=name;paint();return true;});
   if(action==='up')moveChapter(chapter,-1);if(action==='down')moveChapter(chapter,1);
   if(action==='delete'){const contents=pages.filter(v=>v.chapterId===chapter.id);if(!await UI.modal({title:'删除「'+chapter.name+'」？',message:contents.length?'这个章节包含 '+contents.length+' 页，确认后会一起移除。原始共同记录保留；保存排列后才生效。':'空章节会从编排中移除；保存排列后才生效。',confirm:'确认删除章节', danger: true,cancel:'取消'}))return;chapters=chapters.filter(v=>v.id!==chapter.id);pages=pages.filter(v=>v.chapterId!==chapter.id);paint();}
  }
  async function pageMenu(page){
   const title=B.pageView(page,book()).title,action=await UI.sheet({title:title+' · 页面操作',actions:[{label:'上移一页',value:'up'},{label:'下移一页',value:'down'},{label:'移动到另一章',value:'chapter'},{label:'删除书页',value:'delete',danger:true}]});
   if(['up','down'].includes(action)){const group=pages.filter(v=>v.chapterId===page.chapterId),index=group.indexOf(page),target=group[index+(action==='up'?-1:1)];if(!target){UI.toast('已经在本章边界');return;}const a=pages.indexOf(page),b=pages.indexOf(target);[pages[a],pages[b]]=[pages[b],pages[a]];paint();}
   if(action==='chapter'){const others=chapters.filter(v=>v.id!==page.chapterId);if(!others.length){UI.toast('先新增另一章，再移动书页','info');return;}const chapterId=await UI.sheet({title:'选择目标章节',actions:others.map(v=>({label:v.name,value:v.id}))});if(!chapterId)return;page.chapterId=chapterId;pages=pages.filter(v=>v.id!==page.id);pages.push(page);paint();}
   if(action==='delete'){if(!await UI.modal({title:'删除「'+title+'」？',message:'书页、它的补页和书签将从这本册移除；原始共同记录保留。保存排列后才生效。',confirm:'确认删除书页', danger: true,cancel:'取消'}))return;pages=pages.filter(v=>v.id!==page.id);paint();}
  }
  function paint(){
   list.replaceChildren();if(!chapters.length)blank(list,'从第一章开始','空白册可以先保存，随后添加章节和页面。');
   const pending=B.pending(current);if(pending.length)row(list,'继续编排 '+pending.length+' 份素材',()=>go(7)).className='book-continue-materials';
   for(const chapter of chapters){const heading=document.createElement('div');heading.className='v2-chapter-heading';const h=document.createElement('h2');h.textContent=chapter.name;heading.append(h);list.append(heading);const chapterAction=row(heading,'···',()=>chapterMenu(chapter));chapterAction.setAttribute('aria-label','章节操作「'+chapter.name+'」');chapterAction.className='book-structure-menu';const grid=document.createElement('div');grid.className='v2-page-grid';list.append(grid);
    for(const page of pages.filter(v=>v.chapterId===chapter.id)){
     const view=B.pageView(page,book()),tile=document.createElement('article');tile.className='v2-page-tile';tile.dataset.pageId=page.id;grid.append(tile);
     const content=row(tile,'',()=>{if(Date.now()-lastDrag<400)return;go(PrototypeBookEditors.editorPage(page),{page:page.id});});content.className='book-page-row';content.dataset.pageId=page.id;content.setAttribute('aria-label',view.title);
     const preview=document.createElement('div');preview.className='v2-page-thumbnail';const image=view.images?.[0]?.image||view.image;
     preview.setAttribute('aria-hidden','true');if(image){const img=document.createElement('img');img.src=image;img.alt='';img.onerror=()=>{preview.dataset.copy='照片暂时无法打开';preview.replaceChildren();};preview.append(img);}else preview.dataset.copy=(view.blocked?'关联内容不可见':view.body||'写下我们的故事').slice(0,48);
     const title=document.createElement('span');title.className='v2-page-caption';title.textContent=view.title;content.append(preview,title);
     const number=document.createElement('span');number.className='v2-page-number';number.textContent=String(pages.indexOf(page)+1).padStart(2,'0');tile.append(number);
     const menu=row(tile,'···',()=>pageMenu(page));menu.className='book-structure-menu';menu.setAttribute('aria-label','页面操作「'+view.title+'」');
     tile.draggable=true;tile.ondragstart=e=>{dragged=page;tile.dataset.dragging='true';e.dataTransfer.setData('text/plain',page.id);e.dataTransfer.effectAllowed='move';};tile.ondragend=()=>{dragged=null;lastDrag=Date.now();tile.removeAttribute('data-dragging');};
     tile.ondragover=e=>{if(dragged&&dragged.chapterId===page.chapterId&&dragged!==page){e.preventDefault();tile.dataset.drop='true';}};tile.ondragleave=()=>tile.removeAttribute('data-drop');tile.ondrop=e=>{e.preventDefault();reorder(dragged,page);};
     let timer,touching=false,target=null;tile.addEventListener('touchstart',e=>{if(e.target.closest('.book-structure-menu')||e.touches.length!==1)return;timer=setTimeout(()=>{dragged=page;touching=true;tile.dataset.dragging='true';},350);},{passive:true});
     tile.addEventListener('touchmove',e=>{if(!touching){clearTimeout(timer);return;}e.preventDefault();const touch=e.touches[0];target=document.elementFromPoint(touch.clientX,touch.clientY)?.closest('.v2-page-tile');for(const el of grid.children)el.removeAttribute('data-drop');if(target&&target!==tile)target.dataset.drop='true';},{passive:false});
     const end=()=>{clearTimeout(timer);if(touching){lastDrag=Date.now();const destination=pages.find(p=>p.id===target?.dataset.pageId);if(destination)reorder(dragged,destination);tile.removeAttribute('data-dragging');touching=false;dragged=null;}};tile.addEventListener('touchend',end);tile.addEventListener('touchcancel',()=>{clearTimeout(timer);touching=false;dragged=null;tile.removeAttribute('data-dragging');});
    }
   }
  }
  let dragged=null,lastDrag=0;
  window.PrototypeBookStructure.refreshView=paint;
  function reorder(from,to){if(!from||!to||from===to||from.chapterId!==to.chapterId)return;const origin=pages.indexOf(from),target=pages.indexOf(to);pages.splice(origin,1);pages.splice(target,0,from);lastDrag=Date.now();paint();}
  bind('.add',()=>edit('章节','章节名','',name=>{chapters.push({id:'chapter-'+crypto.randomUUID(),name});paint();return true;}));
  bind('.save',()=>UI.busy(document.querySelector('.save'),'保存排列…',()=>{if(!B.structure(id,chapters,pages,current.updatedAt))return false;guard.commit();return go(14);}));
  const addPage=button('＋ 添加回忆',()=>go(8));document.querySelector('.v2-actions')?.prepend(addPage);const save=document.querySelector('.save'),header=document.querySelector('.v2-header');if(header&&save){header.lastElementChild.replaceWith(save);save.style.fontSize='14px';save.style.padding='6px';}const note=document.createElement('p');note.className='v2-structure-note';note.textContent='改动将在保存后生效';list.before(note);paint();
 }
 window.PrototypeBookStructure={render};
})();
