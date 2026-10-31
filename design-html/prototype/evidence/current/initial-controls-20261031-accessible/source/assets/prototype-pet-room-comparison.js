/* Render the selected save log's snapshots; missing historical values stay unknown. */
(() => {
  function paint(screen,entry,pet){
    const panel=document.createElement('section');panel.className='pet-room-comparison';panel.setAttribute('aria-label','这次保存的布置前后对比');
    for(const [key,title] of [['before','布置前'],['after','布置后']]){
      const figure=document.createElement('section');figure.dataset.snapshot=key;
      const heading=document.createElement('h3');heading.textContent=title;figure.append(heading);
      const raw=entry[key]||{},known={},labels=document.createElement('div');labels.className='pet-room-snapshot-labels';
      for(const group of ['地毯','小床','墙饰','摆件']){
        const item=PrototypePetLife.catalog.find(v=>v.type==='room'&&v.group===group&&v.name===raw[group]);
        if(item)known[group]=item.name;
        const label=document.createElement('span');label.textContent=group+'：'+(item?item.name:'未记录');labels.append(label);
      }
      if(Object.keys(known).length){const svg=PrototypePetDraftPreview.room(pet,known);svg.setAttribute('aria-label',title+' · '+Object.values(known).join('、')+' · 保存快照示意');figure.append(svg);}
      else{const empty=document.createElement('div');empty.className='pet-room-snapshot-missing';empty.textContent='这次记录未保存布置快照';figure.append(empty);}
      figure.append(labels);panel.append(figure);
    }
    screen.querySelector('.pet-room-comparison')?.remove();screen.append(panel);
    for(const selector of ['.before','.after','.person.a','.person.b','.note'])screen.querySelector(selector).hidden=true;
    screen.querySelector('.art-top').setAttribute('aria-hidden','true');screen.querySelector('.art-top').removeAttribute('role');
    screen.querySelector('.receipt').textContent=entry.actor+' · '+entry.date+' 保存';
  }
  window.PrototypePetRoomComparison={paint};
})();
