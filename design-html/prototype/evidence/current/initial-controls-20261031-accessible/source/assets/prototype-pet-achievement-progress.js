/* Display only: the existing achievement model owns all counts, targets, rewards and claims. */
(() => {
  function paint(row,item){
    row.classList.add('pet-achievement-row');row.dataset.achievement=item.id;
    const value=Math.max(0,Math.min(item.progress,item.target));
    const title=document.createElement('b');title.className='pet-achievement-title';title.textContent=item.name;
    const count=document.createElement('span');count.className='pet-achievement-value';count.textContent=value+' / '+item.target;
    const status=item.claimed?'奖励已领取':item.done?'已达成':'进行中';
    const progress=document.createElement('progress');progress.max=item.target;progress.value=value;progress.setAttribute('aria-label',item.name);progress.setAttribute('aria-valuetext',value+' / '+item.target+' · '+status);
    const state=document.createElement('small');state.className='pet-achievement-state';state.textContent=status;
    row.replaceChildren(title,count,progress,state);
  }
  window.PrototypePetAchievementProgress={paint};
})();
