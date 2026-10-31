/* Display-only calendar: the existing controller/date helper owns occurrence logic. */
(() => {
  const screen=document.querySelector('.screen[aria-label="纪念日管理"]');
  const root=screen?.querySelector('#anniversary-calendar'),pill=screen?.querySelector('.date-pill');
  if(!root||!pill)return;
  function paint(){
    const date=PrototypeDates.parse(pill.textContent.trim());
    if(!date){
      const caption=document.createElement('figcaption');caption.className='calendar-month';caption.textContent='日期待确认';
      root.replaceChildren(caption);delete root.dataset.date;root.dataset.unavailable='true';
      root.setAttribute('aria-label','纪念日日期待确认');root.hidden=false;screen.dataset.anniversaryCalendar='true';return;
    }
    if(root.dataset.date===date.iso)return;
    delete root.dataset.unavailable;
    const caption=document.createElement('figcaption');caption.className='calendar-month';caption.textContent=date.y+'.'+String(date.month).padStart(2,'0');
    const week=document.createElement('div');week.className='calendar-week';
    for(const name of ['一','二','三','四','五','六','日']){const cell=document.createElement('span');cell.textContent=name;week.append(cell);}
    const grid=document.createElement('div');grid.className='calendar-grid';
    const first=(new Date(Date.UTC(date.y,date.month-1,1)).getUTCDay()+6)%7;
    const days=new Date(Date.UTC(date.y,date.month,0)).getUTCDate(),cells=Math.ceil((first+days)/7)*7;
    grid.style.gridTemplateRows='repeat('+cells/7+',minmax(0,1fr))';
    for(let index=0;index<cells;index++){
      const cell=document.createElement('span'),day=index-first+1;
      if(day>0&&day<=days){cell.dataset.day=String(day);cell.textContent=String(day);if(day===date.day)cell.dataset.selected='true';}
      grid.append(cell);
    }
    root.replaceChildren(caption,week,grid);root.dataset.date=date.iso;
    root.setAttribute('aria-label',date.y+'年'+date.month+'月'+date.day+'日纪念日');
    root.hidden=false;screen.dataset.anniversaryCalendar='true';
  }
  const observer=new MutationObserver(paint),observe=()=>observer.observe(pill,{childList:true,characterData:true,subtree:true});
  observe();addEventListener('pagehide',()=>observer.disconnect());
  addEventListener('pageshow',event=>{if(event.persisted){observe();paint();}});paint();
})();
