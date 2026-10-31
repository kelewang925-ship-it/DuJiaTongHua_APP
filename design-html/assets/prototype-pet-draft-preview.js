/* Read-only draft schematics. Selection, ownership, save and dirty guards stay in the controller. */
(() => {
  const NS='http://www.w3.org/2000/svg';
  function node(tag,attrs={}){const e=document.createElementNS(NS,tag);for(const [key,value] of Object.entries(attrs))e.setAttribute(key,value);return e;}
  function petPicture(kind){
    const group=node('g',{'data-preview-kind':kind});
    const ears={小狗:'M38 30C8 4 7 58 28 62L42 43M82 30c30-26 31 28 10 32L78 43',小猫:'M28 38 24 5 52 25M68 25 96 5 92 38',小兔:'M38 30C10-20 50-20 51 27M69 27C70-20 110-20 82 30',小狐狸:'M27 42 18 4 53 27M67 27 102 4 93 42'};
    group.append(node('ellipse',{cx:60,cy:91,rx:31,ry:25,fill:'#e5c9a0'}),node('path',{d:ears[kind]||ears.小狗,fill:'#dfbd92'}),node('ellipse',{cx:60,cy:48,rx:37,ry:30,fill:'#f0dec1'}),node('ellipse',{cx:60,cy:59,rx:22,ry:14,fill:'#fff5df'}),node('circle',{cx:47,cy:45,r:3,fill:'#684320'}),node('circle',{cx:73,cy:45,r:3,fill:'#684320'}),node('path',{d:'m56 55 4 4 4-4Zm4 4v6m-8-2q8 8 16 0',fill:'none'}));
    return group;
  }
  function itemPicture(item,x,y,width,height){const svg=PrototypePetItemPreview.create(item,item.name+' · 物品示意');for(const [key,value] of Object.entries({x,y,width,height,'data-preview-item':item.id,'aria-hidden':'true'}))svg.setAttribute(key,value);svg.removeAttribute('role');svg.removeAttribute('aria-label');return svg;}
  function outfit(pet,selected){
    const svg=node('svg',{viewBox:'0 0 240 150',role:'img','aria-label':pet.kind+' · 试穿：'+(selected||'不佩戴')+' · 示意图'}),body=petPicture(pet.kind);body.setAttribute('transform','translate(60 20)');svg.append(body);
    const item=PrototypePetLife.catalog.find(v=>v.type==='outfit'&&v.name===selected);
    if(item){const head=['peach-hat','crown'].includes(item.id),clothes=item.group==='衣服';svg.append(itemPicture(item,head?88:clothes?83:97,head?0:clothes?80:76,head?64:clothes?74:46,head?52:clothes?65:46));}
    return svg;
  }
  function room(pet,draft){
    const svg=node('svg',{viewBox:'0 0 360 215',role:'img','aria-label':'小屋布置预览 · '+Object.values(draft).join('、')+' · 示意图'});
    svg.append(node('rect',{x:3,y:3,width:354,height:208,rx:15,fill:'#fff4df'}),node('path',{d:'M3 135h354M270 4v131l86 76',fill:'none',stroke:'#dfc9a9'}));
    const positions={地毯:[82,116,176,95],小床:[15,80,110,100],墙饰:[123,10,76,85],摆件:[270,57,75,103]};
    for(const [group,name] of Object.entries(draft)){const item=PrototypePetLife.catalog.find(v=>v.type==='room'&&v.name===name);if(item)svg.append(itemPicture(item,...positions[group]));}
    const body=petPicture(pet.kind);body.setAttribute('transform','translate(158 77) scale(.65)');svg.append(body);return svg;
  }
  function paint(screen,pet,draft){
    const n=Number(screen.dataset.petPage);let panel=screen.querySelector('.pet-draft-preview');if(!panel){panel=document.createElement('section');panel.className='pet-draft-preview';screen.append(panel);}
    const title=document.createElement('h2');title.textContent=n===12?'试穿示意 · 保存后生效':'布置示意 · 保存后生效';
    const caption=document.createElement('div');caption.className='pet-draft-caption';
    if(n===12){caption.textContent=draft||'不佩戴';panel.replaceChildren(title,outfit(pet,draft),caption);screen.querySelector('.art-closet').setAttribute('aria-hidden','true');screen.querySelector('.art-closet').removeAttribute('role');screen.querySelector('.closet-name').hidden=true;}
    else{for(const [group,name] of Object.entries(draft)){const label=document.createElement('span');label.textContent=group+'：'+name;caption.append(label);}panel.replaceChildren(title,room(pet,draft),caption);screen.querySelector('.art-top').setAttribute('aria-hidden','true');screen.querySelector('.art-top').removeAttribute('role');screen.querySelector('.plaque').hidden=true;}
  }
  window.PrototypePetDraftPreview={paint,room,petPicture};
})();
