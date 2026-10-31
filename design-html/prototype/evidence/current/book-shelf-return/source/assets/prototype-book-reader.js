/* One DOM reading scene: measured content fragments, stable anchors and curved paper. */
(() => {
  const V=PrototypeBookV2,{node,action}=V;
  function render(ctx,initial,route){
    const {UI,B,screen,params,id,go}=ctx;
    if(!initial.pages.length){go(15);return;}
    let book=initial,fragments=[],index=0,mode='book',large=false,disposed=false,turn=null,drag=null,resizeTimer,ignoreScrollUntil=0,opening=false,closing=false;
    const openFromCover=params.get('open')==='cover';
    let currentPage=book.pages.find(p=>p.id===params.get('page'))||book.pages.find(p=>p.id===book.lastPage)||book.pages[0];
    let anchor={pageId:currentPage.id,offset:0};
    if(!params.has('page')||params.get('page')===book.lastAnchor?.pageId)anchor={...anchor,...book.lastAnchor};
    if(params.has('offset'))anchor.offset=Math.max(0,Number(params.get('offset'))||0);
    if(params.has('block'))anchor.block=Math.max(0,Number(params.get('block'))||0);
    const reduced=()=>matchMedia('(prefers-reduced-motion:reduce)').matches;
    screen.classList.add('v2-reader');screen.replaceChildren();
    const header=node('header','v2-header'),stage=node('section','v2-book-stage'),sheets=node('div','v2-reader-sheets book-reading-area book-reading-images'),footer=node('footer','v2-reader-footer'),nav=node('nav','v2-reader-navigation'),tools=node('nav','v2-reader-tools');
    const title=node('span','v2-reader-title',book.name),back=action('‹ 书架',closeBook,'back'),more=action('···',menu,'v2-reader-more');more.setAttribute('aria-label','阅读设置与工具');
    header.append(back,title,more);stage.setAttribute('aria-label','回忆书页');stage.tabIndex=0;stage.append(sheets);
    const previous=action('‹',()=>navigate(-1),'v2-previous-page'),count=action('',null, 'page-count'),next=action('›',()=>navigate(1),'next-page');previous.setAttribute('aria-label','上一页');next.setAttribute('aria-label','下一页');count.onclick=directory;
    const continuation=node('span','v2-continuation'),status=node('p','v2-reader-status'),hint=node('p','v2-reader-hint');status.setAttribute('role','status');status.setAttribute('aria-live','polite');hint.id='book-reply-hint';
    const toc=action('☷ 目录',directory,'toc'),bookmark=action('♧ 书签',toggleBookmark,'bookmark'),supplement=action('＋ 留一张补页',()=>go(18,{page:activePage().id}),'v2-add-supplement');bookmark.setAttribute('aria-pressed','false');supplement.setAttribute('aria-describedby',hint.id);
    nav.append(previous,count,next);tools.append(toc,bookmark,supplement);footer.append(nav,continuation,tools,hint,status);screen.append(header,stage,footer);
    const measure=node('div','v2-measurer');measure.setAttribute('aria-hidden','true');measure.inert=true;screen.append(measure);
    const api={refresh,onStorage};PrototypeBookReader.active=api;

    function activePage(){return book.pages.find(p=>p.id===(fragments[index]?.pageId||anchor.pageId))||book.pages[0];}
    function viewOf(page){return B.pageView(page,book);}
    function updateBook(){const latest=B.find(id);if(!latest){dispose();go(1,{},null);return false;}book=latest;return true;}
    function dimensions(){
      const double=mode==='book'&&stage.clientWidth>=584&&stage.clientHeight>=268;
      screen.classList.toggle('v2-double-page',double);
      const height=Math.max(160,stage.clientHeight-28);screen.style.setProperty('--reader-photo-height',Math.max(64,Math.min(190,height*.34))+'px');
      return {width:(stage.clientWidth-(double?40:32))/(double?2:1),height,double};
    }
    function pageBlocks(page){
      const view=viewOf(page),blocks=[];
      const images=view.images?.length?view.images:view.image?[{image:view.image,crop:{x:50,y:50,zoom:1}}]:[];
      for(const item of images)blocks.push({type:'image',...item});
      const body=view.blocked?'关联内容已不可见，独立编写文字仍保留。\n'+(page.body||''):view.body||'';
      if(body)blocks.push({type:'body',text:body,offset:0});
      if(page.message)blocks.push({type:'message',text:page.message});
      if(page.stickers?.length)blocks.push({type:'stickers',text:page.stickers.join(' ')});
      return blocks;
    }
    function blockElement(block,interactive=true){
      if(block.type!=='image')return node('p',block.type==='body'?'copy':block.type==='message'?'v2-page-message':'v2-page-stickers',block.text);
      const frame=node('div','book-photo-frame v2-reader-photo');PrototypeBookEditors.frame(frame,block.image,block.crop);
      if(interactive){const zoom=action('放大照片',()=>showImage(block),'v2-image-zoom');frame.append(zoom);}
      return frame;
    }
    function paper(fragment,interactive=true){
      const page=book.pages.find(p=>p.id===fragment.pageId),view=viewOf(page),p=node('article','v2-paper');p.dataset.pageId=page.id;
      const heading=node('header','v2-paper-heading'),h=node('h2','page-title',view.title),date=node('p','date',view.date);
      h.tabIndex=0;heading.append(h,date);p.append(heading);
      const content=node('div','v2-paper-content');for(const b of fragment.blocks)content.append(blockElement(b,interactive));p.append(content);
      const folio=node('small','v2-folio',String(book.pages.indexOf(page)+1).padStart(2,'0')+(fragment.part>0?' · 续':''));p.append(folio);
      if(interactive){
        if(view.url){const source=action('查看原始共同记录',()=>UI.go(view.url),'v2-source-link');p.append(source);}
        if(view.supplements.length){const note=action('查看补页 · '+view.supplements.length,()=>showSupplements(page),'book-inline-button v2-supplement-tab');p.append(note);}
      }
      return p;
    }
    function fits(fragment,dims){
      const p=paper(fragment,false);p.style.width=dims.width+'px';p.style.height=dims.height+'px';measure.replaceChildren(p);
      const box=p.querySelector('.v2-paper-content'),last=box.lastElementChild;
      return !last||last.getBoundingClientRect().bottom<=box.getBoundingClientRect().bottom+.5;
    }
    function paginate(){
      const dims=dimensions(),result=[];
      for(const page of book.pages){
        const pages=[],blocks=pageBlocks(page);let part={pageId:page.id,blocks:[],part:0,offset:0,block:0};
        const flush=()=>{pages.push(part);part={pageId:page.id,blocks:[],part:pages.length,offset:0,block:0};};
        for(const [blockIndex,original] of blocks.entries()){
          if(original.type==='image'){
            const candidate={...part,blocks:[...part.blocks,original]};
            if(part.blocks.length&&!fits(candidate,dims))flush();
            if(!part.blocks.length)part.block=blockIndex;part.blocks.push(original);continue;
          }
          let rest=original.text,offset=0;
          while(rest.length){
            const candidate={...part,blocks:[...part.blocks,{...original,text:rest,offset}]};
            if(fits(candidate,dims)){if(!part.blocks.length){part.block=blockIndex;part.offset=offset;}part.blocks.push({...original,text:rest,offset});break;}
            let low=0,high=rest.length;
            while(low<high){const mid=Math.ceil((low+high)/2);if(fits({...part,blocks:[...part.blocks,{...original,text:rest.slice(0,mid),offset}]},dims))low=mid;else high=mid-1;}
            if(low<1&&part.blocks.length){flush();continue;}
            const length=Math.max(1,low);if(!part.blocks.length){part.block=blockIndex;part.offset=offset;}part.blocks.push({...original,text:rest.slice(0,length),offset});offset+=length;rest=rest.slice(length);flush();
          }
        }
        if(part.blocks.length||!pages.length)flush();
        pages.forEach(p=>p.parts=pages.length);result.push(...pages);
      }
      measure.replaceChildren();fragments=result;
      const candidates=fragments.map((f,i)=>({f,i})).filter(v=>v.f.pageId===anchor.pageId);
      index=candidates.filter(v=>v.f.block<(anchor.block||0)||v.f.block===(anchor.block||0)&&v.f.offset<=(anchor.offset||0)).at(-1)?.i??candidates[0]?.i??0;
    }
    function draw(at=index){
      sheets.replaceChildren();const dims=dimensions(),shown=fragments.slice(at,at+(dims.double?2:1));
      for(const f of shown)sheets.append(paper(f));
      if(dims.double&&shown.length===1)sheets.append(node('article','v2-paper v2-end-paper','故事，还在继续。'));
    }
    function sync(useFragmentAnchor=true){
      const f=fragments[index];if(!f)return;currentPage=activePage();if(useFragmentAnchor||f.pageId!==anchor.pageId)anchor={pageId:f.pageId,offset:f.offset,block:f.block};
      const current=book.pages.indexOf(currentPage)+1,other=screen.classList.contains('v2-double-page')?book.pages.findIndex(p=>p.id===fragments[index+1]?.pageId)+1:current;
      count.textContent='第 '+current+(other>current?'–'+other:'')+' / '+book.pages.length+' 页';count.setAttribute('aria-label','当前'+count.textContent+'，打开目录');
      continuation.textContent=f.parts>1?'本页 '+(f.part+1)+' / '+f.parts:'';continuation.style.visibility=f.parts>1?'visible':'hidden';continuation.setAttribute('aria-hidden',String(f.parts<=1));
      previous.disabled=index===0;next.disabled=index+(screen.classList.contains('v2-double-page')?2:1)>=fragments.length;bookmark.setAttribute('aria-pressed',String((book.bookmarks||[]).includes(f.pageId)));
      const view=viewOf(currentPage),allowed=!view.blocked&&PrototypePreferences.privacy().replies;
      supplement.disabled=!allowed;supplement.title=allowed?'':view.blocked?'关联内容已不可见':'共同回应已关闭';
      hint.textContent=allowed?'':view.blocked?'关联回忆不可见，暂不能添加补页。':'共同回应已关闭，可在隐私设置中开启。';
      const url=new URL(location.href);url.searchParams.set('page',anchor.pageId);url.searchParams.set('offset',String(anchor.offset||0));url.searchParams.set('block',String(anchor.block||0));url.searchParams.delete('open');history.replaceState(history.state,'',url);
      params.set('page',anchor.pageId);params.set('offset',String(anchor.offset||0));params.set('block',String(anchor.block||0));
    }
    function remember(){
      const b=B.find(id);if(!b)return;
      if(b.lastPage===anchor.pageId&&b.lastAnchor?.offset===anchor.offset&&b.lastAnchor?.block===anchor.block&&b.lastAnchor?.pageId===anchor.pageId)return;
      try{if(!B.read(id,anchor.pageId,anchor))throw new Error('阅读位置未保存');status.textContent='';book=B.find(id)||book;}
      catch(e){status.replaceChildren(node('span','','阅读位置未保存 · '),action('重试',remember));UI.toast(e.message||'阅读位置未保存','error');}
    }
    function refresh(persist=true){
      if(disposed||!updateBook())return;cancelTurn();paginate();draw();sync(false);if(persist)remember();
      if(mode==='continuous')drawContinuous();
    }
    function destination(direction){const step=screen.classList.contains('v2-double-page')?2:1;return direction>0?(index+step>=fragments.length?index:index+step):Math.max(0,index-step);}

    function buildTurn(direction){
      const to=destination(direction);if(to===index)return null;
      const existing=[...sheets.querySelectorAll('.v2-paper')],double=screen.classList.contains('v2-double-page'),source=direction===1?existing.at(-1):existing[0];if(!source)return null;
      const r=source.getBoundingClientRect(),sr=stage.getBoundingClientRect(),overlay=node('div','v2-turn-overlay');overlay.setAttribute('aria-hidden','true');overlay.inert=true;
      const clone=source.cloneNode(true),reverse=paper(fragments[to+(double&&direction<0?1:0)]||fragments[to],false);clone.querySelectorAll('[id]').forEach(e=>e.removeAttribute('id'));
      const width=r.width,height=r.height,pieces=[],segments=12;
      overlay.style.cssText=`left:${r.left-sr.left}px;top:${r.top-sr.top}px;width:${width}px;height:${height}px;`;
      for(let i=0;i<segments;i++){
        const slice=node('div','v2-turn-slice'),front=node('div','v2-turn-front'),backFace=node('div','v2-turn-back');
        slice.style.width=(width/segments+.7)+'px';slice.style.height=height+'px';
        const sample=direction===1?i:segments-1-i,copy=clone.cloneNode(true),reverseCopy=reverse.cloneNode(true);copy.style.cssText=`position:absolute;width:${width}px;height:${height}px;left:${-sample*width/segments}px;top:0;`;front.append(copy);
        reverseCopy.style.cssText=`position:absolute;width:${width}px;height:${height}px;left:${-(segments-1-sample)*width/segments}px;top:0;`;backFace.append(reverseCopy);slice.style.transformOrigin=direction===1?'left center':'right center';slice.append(front,backFace);overlay.append(slice);pieces.push(slice);
      }
      draw(to);if(double){const retained=direction===1?existing[0]:existing.at(-1);sheets.children[direction===1?0:1].replaceWith(retained);}sheets.inert=true;sheets.setAttribute('aria-hidden','true');stage.append(overlay);stage.classList.add('v2-turning');
      return {direction,to,from:index,overlay,pieces,width,height,progress:0,frame:0};
    }
    function paintTurn(p){
      if(!turn)return;turn.progress=p;
      const {width,pieces,direction}=turn,step=width/pieces.length;let x=0,z=0;
      for(let i=0;i<pieces.length;i++){
        const u=(i+.5)/pieces.length,angle=Math.PI*p+Math.sin(Math.PI*p)*(.9*(u-.5)),sign=direction===1?-1:1;
        const x0=x,z0=z;x+=Math.cos(angle)*step;z+=Math.sin(angle)*step;
        const px=direction===1?x0:width-x0-step;
        pieces[i].style.transform=`translate3d(${px}px,0,${z0}px) rotateY(${sign*angle*180/Math.PI}deg)`;
        pieces[i].style.setProperty('--slice-shade',String(Math.min(.26,Math.abs(Math.sin(angle))*.22)));
      }
      turn.overlay.style.opacity=p>.96?String((1-p)/.04):'1';
    }
    function finishTurn(commit){
      if(!turn)return;const to=turn.to;cancelAnimationFrame(turn.frame);turn.overlay.remove();turn=null;stage.classList.remove('v2-turning');sheets.inert=false;sheets.removeAttribute('aria-hidden');
      if(commit)index=to;draw();sync();if(commit)remember();
    }
    function animateTurn(commit){
      if(!turn)return;const start=turn.progress,end=commit?1:0,duration=reduced()?0:Math.max(100,Math.abs(end-start)*330),time=performance.now(),active=turn;
      const tick=now=>{if(turn!==active)return;const t=duration?Math.min(1,(now-time)/duration):1;paintTurn(start+(end-start)*(1-Math.pow(1-t,3)));if(t<1)turn.frame=requestAnimationFrame(tick);else finishTurn(commit);};tick(time);
    }
    function cancelTurn(){drag=null;if(turn)finishTurn(false);}
    function navigate(direction){
      if(mode==='continuous'){stage.scrollBy({top:direction*stage.clientHeight*.8,behavior:reduced()?'instant':'smooth'});return;}
      if(turn||opening||closing)return;if(!updateBook())return;
      const to=destination(direction);if(to===index){UI.toast(direction>0?'已经读到最后一页':'已经是第一页');return;}
      if(reduced()){index=to;draw();sync();remember();return;}
      turn=buildTurn(direction);if(turn)animateTurn(true);
    }
    function pointerDown(e){
      if(mode!=='book'||turn||opening||closing||e.button!==0||e.target.closest('button,a,input,textarea')||getSelection()?.toString())return;
      if(e.clientX<24||e.clientX>innerWidth-24)return;
      drag={x:e.clientX,y:e.clientY,id:e.pointerId,time:performance.now(),locked:false};
    }
    function pointerMove(e){
      if(!drag||drag.id!==e.pointerId)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;
      if(!drag.locked){if(Math.abs(dy)>12&&Math.abs(dy)>Math.abs(dx)){drag=null;return;}if(Math.abs(dx)<12||Math.abs(dx)<Math.abs(dy)*1.4)return;
        const direction=dx<0?1:-1;turn=buildTurn(direction);if(!turn){drag=null;return;}drag.locked=true;stage.setPointerCapture(e.pointerId);
      }
      e.preventDefault();paintTurn(Math.min(.98,Math.max(0,(turn.direction===1?-dx:dx)/turn.width)));
    }
    function pointerUp(e){
      if(!drag||drag.id!==e.pointerId)return;const d=drag;drag=null;
      if(stage.hasPointerCapture(e.pointerId))stage.releasePointerCapture(e.pointerId);
      if(turn){const speed=Math.abs(e.clientX-d.x)/(performance.now()-d.time);animateTurn(turn.progress>=.25||turn.progress>.09&&speed>.65);}
    }
    stage.addEventListener('pointerdown',pointerDown);stage.addEventListener('pointermove',pointerMove);stage.addEventListener('pointerup',pointerUp);stage.addEventListener('pointercancel',()=>{drag=null;if(turn)animateTurn(false);});
    stage.addEventListener('keydown',e=>{if(e.target.closest('button,a,input,textarea'))return;if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();navigate(e.key==='ArrowRight'?1:-1);}});
    stage.addEventListener('click',e=>{if(e.target!==stage&&e.target!==sheets&&!e.target.matches('.v2-paper,.v2-paper-content'))return;screen.classList.toggle('v2-controls-hidden');});

    async function directory(){
      cancelTurn();const wrap=node('div'),tabs=node('div','v2-sheet-tabs'),list=node('div','v2-sheet-list');let kind='章节';
      function paint(){
        list.replaceChildren();for(const e of tabs.children)e.setAttribute('aria-pressed',String(e.textContent===kind));
        const pages=kind==='书签'?book.pages.filter(p=>(book.bookmarks||[]).includes(p.id)):book.pages;
        if(!pages.length)list.append(node('p','','还没有书签，可在阅读页点击书签。'));
        for(const chapter of book.chapters){const group=pages.filter(p=>p.chapterId===chapter.id);if(!group.length)continue;list.append(node('h3','',chapter.name));
          for(const page of group){const v=viewOf(page),button=action(v.title,async()=>{await UI.back();anchor={pageId:page.id,offset:0};refresh();if(mode==='continuous')document.querySelector(`[data-continuous-page="${CSS.escape(page.id)}"]`)?.scrollIntoView({block:'start'});});
            button.setAttribute('aria-current',String(page.id===activePage().id));if(kind==='缩略图'){const image=v.images?.[0]?.image||v.image;if(image){const img=node('img');img.src=image;img.alt='';button.prepend(img);}}
            list.append(button);
          }
        }
      }
      for(const label of ['章节','缩略图','书签'])tabs.append(action(label,()=>{kind=label;paint();}));wrap.append(tabs,list);paint();
      UI.sheet({title:'回忆册目录',content:wrap,actions:[]});
    }
    function toggleBookmark(){
      const page=activePage();UI.busy(bookmark,'保存书签…',()=>{const saved=B.bookmark(id,page.id);if(!saved)return false;book=saved;sync();UI.toast('书签已更新','success');return true;});
    }
    async function showImage(block){
      cancelTurn();const image=node('img','v2-full-image');image.src=block.image;image.alt='共同回忆照片，原图';
      const form=node('div','v2-image-viewer'),label=node('label','','缩放照片'),range=node('input');range.type='range';range.min=1;range.max=3;range.step=.1;range.value=1;range.setAttribute('aria-label','照片缩放');
      const scroll=node('div','v2-image-scroll');scroll.append(image);range.oninput=()=>{image.style.width=Number(range.value)*100+'%';};label.append(range);form.append(scroll,label);
      await UI.modal({title:'共同回忆照片',content:form,confirm:'返回阅读'});
    }
    async function showSupplements(page){
      cancelTurn();const wrap=node('div','v2-sheet-list right-copy book-supplement-images'),view=viewOf(page);
      if(view.blocked){UI.toast('关联内容已不可见','error');return;}
      for(const s of view.supplements){const entry=node('article','v2-note-paper');entry.append(node('p','',s.text||s.emoji||''),node('p','v2-note-author',s.author+' · '+s.date));if(s.image){const box=node('div','book-photo-frame');PrototypeBookEditors.frame(box,s.image);entry.append(box);}wrap.append(entry);}
      if(!view.supplements.length)wrap.append(node('p','','还没有补页。'));
      await UI.sheet({title:'我们的补页',content:wrap,actions:[]});
    }
    async function menu(){
      cancelTurn();const picked=await UI.sheet({title:'阅读设置与工具',actions:[{label:mode==='book'?'大字连续阅读':'实体翻书阅读',value:'mode'},{label:large?'标准字号':'放大字号',value:'type'},{label:'整理书页',value:'organize'},{label:'封面与主题',value:'cover'},{label:'管理这本回忆册',value:'manage'},{label:'返回书架',value:'shelf'}]});
      if(picked==='mode'){mode=mode==='book'?'continuous':'book';screen.classList.toggle('v2-continuous',mode==='continuous');large=mode==='continuous';screen.classList.toggle('v2-large-type',large);refresh();}
      if(picked==='type'){large=!large;screen.classList.toggle('v2-large-type',large);refresh();}
      const returnTo={returnPage:anchor.pageId,returnOffset:anchor.offset,returnBlock:anchor.block||0};
      if(picked==='organize')go(13,returnTo);if(picked==='cover')go(5,{origin:'manage',...returnTo});if(picked==='manage')go(21,returnTo);if(picked==='shelf')closeBook();
    }
    function textY(element,offset){const text=element.firstChild;if(!text||text.nodeType!==Node.TEXT_NODE)return element.getBoundingClientRect().top;const range=document.createRange(),at=Math.min(text.length,Math.max(0,offset||0));range.setStart(text,at);range.setEnd(text,Math.min(text.length,at+1));return range.getBoundingClientRect().top;}
    function textOffset(element,y){const text=element.firstChild;if(!text||text.nodeType!==Node.TEXT_NODE)return 0;let low=0,high=text.length;while(low<high){const mid=Math.floor((low+high)/2);if(textY(element,mid)<y)low=mid+1;else high=mid;}return low;}
    function drawContinuous(){
      ignoreScrollUntil=performance.now()+500;
      const container=node('div','v2-continuous-content');
      for(const page of book.pages){const article=node('article','v2-continuous-page');article.dataset.continuousPage=page.id;const view=viewOf(page);article.append(node('h2','',view.title),node('p','date',view.date));for(const [i,block]of pageBlocks(page).entries()){const e=blockElement(block);e.dataset.blockIndex=i;article.append(e);}if(view.supplements.length)article.append(action('查看补页',()=>showSupplements(page)));container.append(article);}
      sheets.replaceChildren(container);requestAnimationFrame(()=>{const page=container.querySelector(`[data-continuous-page="${CSS.escape(anchor.pageId)}"]`),block=page?.querySelector(`[data-block-index="${anchor.block||0}"]`);if(!page)return;const y=block&&anchor.offset?textY(block,anchor.offset):page.getBoundingClientRect().top;stage.scrollTop+=y-stage.getBoundingClientRect().top-20;});
    }
    let scrollTimer;
    stage.addEventListener('scroll',()=>{if(mode!=='continuous'||performance.now()<ignoreScrollUntil)return;clearTimeout(scrollTimer);scrollTimer=setTimeout(()=>{const top=stage.getBoundingClientRect().top+20,pages=[...sheets.querySelectorAll('[data-continuous-page]')],selected=pages.filter(e=>e.getBoundingClientRect().top<=top).at(-1)||pages[0];if(!selected)return;const block=[...selected.querySelectorAll('[data-block-index]')].find(e=>e.getBoundingClientRect().bottom>top);anchor={pageId:selected.dataset.continuousPage,offset:block?textOffset(block,top):0,block:Number(block?.dataset.blockIndex)||0};index=fragments.findIndex(f=>f.pageId===anchor.pageId);sync(false);remember();},180);},{passive:true});
    function animatedCover(kind){const cover=node('div','v2-opening-cover '+kind),paper=sheets.querySelector('.v2-paper');cover.setAttribute('aria-hidden','true');cover.inert=true;V.cover(cover,book);if(paper){const rect=paper.getBoundingClientRect(),parent=stage.getBoundingClientRect();cover.style.cssText=`left:${rect.left-parent.left}px;top:${rect.top-parent.top}px;width:${rect.width}px;height:${rect.height}px;`;}stage.append(cover);return cover;}
    async function closeBook(){if(closing)return;closing=true;cancelTurn();if(!reduced()){animatedCover('v2-cover-closing');await new Promise(r=>setTimeout(r,380));}dispose();go(1,{},null);}
    function onStorage(e){
      if(!e.key||[B.key,'dujia-prototype-records','dujia-prototype-moments','dujia-prototype-capsules','dujia-prototype-works','dujia-prototype-pet','dujia-privacy','dujia-prototype-privacy','dujia-prototype-relationship'].includes(e.key)){
        cancelTurn();const dialog=document.querySelector('dialog[open]');if(dialog)UI.back();refresh(false);
      }
    }
    let observedSize=stage.clientWidth+'x'+stage.clientHeight;
    const resize=()=>{cancelTurn();clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>refresh(false),100);},observer=new ResizeObserver(()=>{const nextSize=stage.clientWidth+'x'+stage.clientHeight;if(nextSize===observedSize)return;observedSize=nextSize;resize();});
    function dispose(){disposed=true;cancelTurn();clearTimeout(resizeTimer);clearTimeout(scrollTimer);observer.disconnect();removeEventListener('resize',resize);removeEventListener('storage',onStorage);if(PrototypeBookReader.active===api)PrototypeBookReader.active=null;}
    addEventListener('resize',resize);addEventListener('storage',onStorage);addEventListener('pagehide',dispose,{once:true});
    addEventListener('pageshow',event=>{if(event.persisted)location.reload();});
    refresh();observedSize=stage.clientWidth+'x'+stage.clientHeight;observer.observe(stage);
    if(openFromCover&&!reduced()){opening=true;const cover=animatedCover('v2-cover-opening');setTimeout(()=>{cover.remove();opening=false;},400);}
    if(route===20)setTimeout(()=>showSupplements(activePage()),100);
  }
  window.PrototypeBookReader={render,active:null};
})();
