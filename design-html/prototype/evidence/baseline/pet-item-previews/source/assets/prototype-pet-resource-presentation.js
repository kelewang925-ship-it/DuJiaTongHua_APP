/* Read-only requirements and owned inventory; the existing model/controller owns every action. */
(() => {
  function paint(screen,item,owned,pet){
    const n=Number(screen.dataset.petPage),L=PrototypePetLife,remaining=screen.querySelector('.remaining'),detail=screen.querySelector(n===13?'.details':'.unlock');
    if(L.owns(pet,item)){
      remaining.textContent='已拥有 · 无需再次解锁';detail.textContent='返回选择后可使用，不会重复消耗资源';
    }else if(item.coins||item.stars){
      const amount=item.coins||item.stars,balance=item.coins?pet.coins:pet.stars,unit=item.coins?'金币':'星星';
      remaining.textContent='需 '+amount+' · 还需 '+Math.max(0,amount-balance)+' '+unit+'\n当前 '+balance;
      detail.textContent=balance>=amount?'资源已足够，返回选择后确认解锁':'任务和成就可获得资源，满足条件后再解锁';
    }else{
      remaining.textContent=item.hint||'满足条件后可解锁';detail.textContent=L.allowed(pet,item)?'条件已达成，返回选择即可解锁':'完成条件后，返回选择继续';
    }
    const info=document.createElement('section');info.className='pet-resource-info';info.append(remaining,detail);screen.append(info);
    let list=n===13?screen.querySelector('div.owned'):screen.querySelector('.pet-resource-inventory');
    if(!list){list=document.createElement('section');screen.append(list);}
    list.classList.add('pet-resource-inventory');list.setAttribute('role','list');list.setAttribute('aria-label',n===13?'已拥有的装扮':'已拥有的小屋物品');list.replaceChildren();
    if(!owned.length){const empty=document.createElement('p');empty.className='pet-resource-empty';empty.textContent='还没有装扮，使用上方按钮继续选择或完成任务';list.append(empty);}
    for(const value of owned){
      const row=document.createElement('div');row.className='pet-resource-owned-item';row.setAttribute('role','listitem');
      const name=document.createElement('b');name.textContent=value.name;
      const group=document.createElement('span');group.className='pet-resource-group';group.textContent=value.group;row.append(name,group);list.append(row);
    }
    list.tabIndex=0;
  }
  window.PrototypePetResourcePresentation={paint};
})();
