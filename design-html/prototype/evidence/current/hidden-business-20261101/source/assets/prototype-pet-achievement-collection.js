/* Presentation of the existing seven achievements; no model, claims or navigation writes. */
(() => {
  const ns='http://www.w3.org/2000/svg';
  function medal(){
    const svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 32 36');svg.setAttribute('aria-hidden','true');svg.classList.add('pet-achievement-medal');
    for(const [tag,attrs]of [['path',{d:'M9 21 6 34l10-5 10 5-3-13'}],['circle',{cx:16,cy:14,r:12}],['path',{d:'m16 6 2.5 5 5.5.8-4 4 .9 5.5-4.9-2.6-4.9 2.6.9-5.5-4-4 5.5-.8Z'}]]){
      const part=document.createElementNS(ns,tag);for(const[k,v]of Object.entries(attrs))part.setAttribute(k,v);svg.append(part);
    }
    return svg;
  }
  function paint(cards,summary,items){
    [...cards.children].forEach((button,index)=>{
      const item=items[index];if(!item)return;
      const label=button.textContent;window.PrototypePetAchievementProgress.paint(button,item);
      const status=item.claimed?'奖励已领取':item.done?'可领取奖励':'进行中';
      button.dataset.state=item.claimed?'claimed':item.done?'ready':'progress';button.setAttribute('aria-label',label);
      button.querySelector('.pet-achievement-state').textContent=status;
      button.querySelector('progress').setAttribute('aria-valuetext',Math.max(0,Math.min(item.progress,item.target))+' / '+item.target+' · '+status);
      button.prepend(medal());
    });
    const pending=items.find(item=>item.done&&!item.claimed),next=items.find(item=>!item.done);
    summary.hidden=false;
    summary.textContent=pending?'可领取：'+pending.name+'\n奖励星星 ×'+pending.reward+' · 点上方成就查看':next?'下一枚：'+next.name+'\n进度 '+Math.min(next.progress,next.target)+' / '+next.target+' · 奖励星星 ×'+next.reward:'成就奖励已全部领取\n'+items.length+' 枚纪念章已收藏';
  }
  window.PrototypePetAchievementCollection={paint};
})();
