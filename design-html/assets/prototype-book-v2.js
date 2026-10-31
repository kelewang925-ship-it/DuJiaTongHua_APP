/* Presentation helpers shared only by the 21 memory-book routes. */
(() => {
  const UI=PrototypeUI, B=PrototypeBooks;
  const node=(tag,cls='',text='')=>{const e=document.createElement(tag);e.className=cls;e.textContent=text;return e;};
  const action=(label,fn,cls='')=>{const b=node('button',cls,label);b.type='button';b.onclick=fn;return b;};
  const selectedKey='dujia-book-shelf-selection', covers=new Map();

  function cover(container,book){
    covers.set(container,{id:book.id,theme:book.theme,coverPhoto:book.coverPhoto});container.replaceChildren();container.classList.add('book-cover-photo');container.dataset.theme=book.theme;
    const title=node('strong','',book.name),theme=node('small','',book.theme),image=book.coverPhoto?B.source(book.coverPhoto,book)?.image:null;
    container.append(title,theme);
    if(image){const box=node('div','book-cover-image');PrototypeBookEditors.frame(box,image);container.append(box);}
    else container.append(node('span','book-cover-mark'+(book.coverPhoto?' book-cover-unavailable':''),book.coverPhoto?'封面照片暂不可见':'♡'));
  }
  function refreshCovers(){for(const [e,proposal]of covers){if(!e.isConnected){covers.delete(e);continue;}const book=B.find(proposal.id);if(book)cover(e,{...book,theme:proposal.theme,coverPhoto:proposal.coverPhoto});else e.replaceChildren(node('span','','回忆册已不存在'));}}

  async function library(go,initial='已成册'){
    const wrap=node('div'),tabs=node('div','v2-sheet-tabs'),grid=node('div','v2-all-books');let kind=initial;
    const paint=()=>{
      const focused=grid.contains(document.activeElement)?document.activeElement.closest('button')?.dataset.bookId:null;
      grid.replaceChildren();for(const t of tabs.children)t.setAttribute('aria-pressed',String(t.textContent===kind));
      const books=B.all().filter(b=>kind==='草稿'?b.status==='draft'&&!b.archived:kind==='归档'?b.archived:b.status==='published'&&!b.archived);
      if(!books.length)grid.append(node('p','',kind==='草稿'?'还没有未完成的回忆册':kind==='归档'?'还没有归档的回忆册':'还没有已成册的故事'));
      for(const b of books){const item=action(b.name,async()=>{await UI.back();go(b.archived?21:b.status==='draft'?4:15,{},b.id);});item.dataset.bookId=b.id;item.setAttribute('aria-label',b.name+' · '+kind);cover(item,b);grid.append(item);}
      if(focused)([...grid.children].find(e=>e.dataset.bookId===focused)||[...tabs.children].find(e=>e.textContent===kind))?.focus();
    };
    for(const label of ['已成册','草稿','归档'])tabs.append(action(label,()=>{kind=label;paint();}));wrap.append(tabs,grid);paint();
    const onStorage=event=>{if(event.key===B.key&&wrap.isConnected)paint();};
    addEventListener('storage',onStorage);
    try{return await UI.sheet({title:'全部回忆册',content:wrap,actions:[]});}
    finally{removeEventListener('storage',onStorage);}
  }

  function shelf(ctx){
    const {screen,go}=ctx,books=B.all().filter(b=>b.status==='published'&&!b.archived);
    if(!books.length){UI.go('m08-p02.html',{replace:true,force:true});return;}
    screen.classList.add('v2-shelf');screen.replaceChildren();
    const header=node('header','v2-header'),content=node('section','v2-content'),footer=node('footer','v2-actions'),extras=node('div','v2-extras');
    header.append(action('‹ 首页',()=>UI.go('m03-p02.html'),'back'),node('span','','回忆册'),action('···',()=>library(go),'v2-shelf-more'));header.firstChild.setAttribute('aria-label','返回首页');
    const intro=node('div','v2-intro');intro.append(node('p','v2-eyebrow','OUR MEMORY BOOK'),node('h1','','我们的故事，装订成册'),node('p','v2-description','每一页，都有我们。'));
    const top=node('div','v2-shelf-top');top.append(action('全部回忆册 ›',()=>library(go)),node('span','v2-shelf-count'));
    const rail=node('div','v2-shelf-rail books');rail.setAttribute('aria-label','左右滑动选择回忆册');rail.tabIndex=0;
    const meta=node('div','v2-shelf-meta'),name=node('h2','continue-book'),count=node('p','v2-shelf-count'),progress=node('p','continue-page');meta.append(name,count,progress);
    const step=node('nav','v2-shelf-step'),position=node('span'),tools=node('div','v2-shelf-tools');let selected=0,settle;
    let saved;try{saved=sessionStorage.getItem(selectedKey);}catch{}
    const preferred=books.findIndex(b=>b.id===saved);if(preferred>=0)selected=preferred;else selected=Math.max(0,books.reduce((best,b,i)=>b.lastPage&&(b.updatedAt||0)>(books[best].updatedAt||0)?i:best,0));
    const current=()=>B.find(books[selected].id),read=fromCover=>{const b=current();if(!b){UI.toast('回忆册已不存在，请重新选择','error');return;}if(!b.pages.length){go(15,{},b.id);return;}const page=fromCover?b.pages[0].id:b.pages.find(p=>p.id===b.lastPage)?.id||b.pages[0].id;go(16,{page,...fromCover?{open:'cover'}:{}},b.id);};
    const next=action('继续翻阅 →',()=>read(false),'continue-link v2-primary');
    function paint(index){
      selected=index;const b=current();if(!b)return;
      [...rail.children].forEach((e,i)=>e.setAttribute('aria-current',String(i===index)));
      name.textContent=b.name;count.textContent=b.pages.length+' 页 · '+b.chapters.length+' 个章节';
      const at=b.pages.findIndex(p=>p.id===b.lastPage);progress.textContent=at>=0?'上次读到第 '+(at+1)+' 页':'从第一页，开始我们的故事';next.textContent=at>=0?'继续翻阅 →':'开始翻阅 →';
      position.textContent=(selected+1)+' / '+books.length;top.lastChild.textContent=books.length+' 本回忆册';step.firstChild.disabled=selected===0;step.lastChild.disabled=selected===books.length-1;
      try{sessionStorage.setItem(selectedKey,b.id);}catch{}
    }
    function center(index,behavior='smooth'){index=Math.max(0,Math.min(books.length-1,index));paint(index);const item=rail.children[index];rail.scrollTo({left:item.offsetLeft-(rail.clientWidth-item.clientWidth)/2,behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':behavior});}
    step.append(action('‹',()=>center(selected-1)),position,action('›',()=>center(selected+1)));step.firstChild.setAttribute('aria-label','上一本回忆册');step.lastChild.setAttribute('aria-label','下一本回忆册');
    for(const [i,b]of books.entries()){const card=node('div','v2-shelf-card');card.dataset.bookId=b.id;const entry=action(b.name,()=>{if(i!==selected){center(i);return;}screen.classList.add('v2-book-opening');read(true);});entry.setAttribute('aria-label','从封面打开《'+b.name+'》');cover(entry,b);card.append(entry);rail.append(card);}
    rail.addEventListener('scroll',()=>{clearTimeout(settle);settle=setTimeout(()=>{const centerX=rail.getBoundingClientRect().left+rail.clientWidth/2;let nearest=0,distance=Infinity;[...rail.children].forEach((e,i)=>{const r=e.getBoundingClientRect(),d=Math.abs(r.left+r.width/2-centerX);if(d<distance){nearest=i;distance=d;}});paint(nearest);},90);},{passive:true});
    rail.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight'].includes(e.key))return;e.preventDefault();center(selected+(e.key==='ArrowRight'?1:-1));});
    tools.append(action('封面',()=>go(5,{origin:'manage'},current().id)),action('整理',()=>go(13,{},current().id)));footer.append(next,action('＋ 新建回忆册',()=>go(4,{},null),'new'));extras.append(action('本月推荐',()=>go(3,{},null)),action('归档与草稿',()=>library(go,'草稿')));
    content.append(intro,top,rail,meta,step,tools);screen.append(header,content,footer,extras);paint(selected);requestAnimationFrame(()=>center(selected,'instant'));
  }

  function enhance(n,screen){
    const content=screen.querySelector('.v2-content'),slot=screen.querySelector('.v2-photo-slot');
    if(slot)for(const e of content.querySelectorAll('.book-photo-preview,.book-moment-photo,.book-supplement-preview'))slot.append(e);
    if([9,10,11,12].includes(n)){
      let preview=screen.querySelector('.v2-live-preview');if(!preview){preview=node('div','v2-live-preview');preview.setAttribute('aria-label','书页实时预览');content.querySelector('.v2-intro')?.after(preview);}
      const title=screen.querySelector('#page-title,input.page-title,.moment'),body=screen.querySelector('#excerpt,.caption'),heading=screen.querySelector('.pet-name'),story=screen.querySelector('.milestone');
      const paint=()=>{preview.replaceChildren(node('h2','',title?.value||heading?.textContent||'新的一页'),node('p','',body?.value||story?.textContent||'你的故事，会在这里慢慢展开。'));};
      title?.addEventListener('input',paint);body?.addEventListener('input',paint);paint();
      const observer=new MutationObserver(paint);observer.observe(document.body,{childList:true});if(heading)observer.observe(heading,{childList:true});if(story)observer.observe(story,{childList:true});addEventListener('pagehide',()=>observer.disconnect(),{once:true});
      const keyboard=()=>{const inset=Math.max(0,innerHeight-(visualViewport?.height||innerHeight)-(visualViewport?.offsetTop||0));screen.classList.toggle('v2-keyboard',inset>120);screen.style.setProperty('--v2-keyboard-inset',inset+'px');};
      visualViewport?.addEventListener('resize',keyboard);addEventListener('pagehide',()=>visualViewport?.removeEventListener('resize',keyboard),{once:true});
      screen.addEventListener('focusin',e=>{if(e.target.matches('input,textarea'))setTimeout(()=>e.target.scrollIntoView({block:'nearest',behavior:'smooth'}),180);});
    }
  }
  PrototypeBookEditors.cover=cover;
  PrototypeBookEditors.refreshCovers=refreshCovers;
  window.PrototypeBookV2={node,action,cover,refreshCovers,shelf,library,enhance};
})();
