/* Read-only result illustrations from actual saved play/reward text. */
(() => {
  const NS='http://www.w3.org/2000/svg';
  const symbols={
    '摸摸头':'<path d="M39 65V33c0-9 12-9 12 0v15-30c0-9 12-9 12 0v30-23c0-9 12-9 12 0v26-14c0-9 12-9 12 0v32c0 34-48 43-58 14L17 64c-6-11 4-18 12-8Z"/>',
    '丢球球':'<circle cx="60" cy="60" r="38"/><path d="M22 60h76M60 22c-28 17-28 59 0 76M60 22c28 17 28 59 0 76" fill="none"/>',
    '讲故事':'<path d="M14 26q24-15 46 0 22-15 46 0v66q-22-15-46 0-22-15-46 0Z"/><path d="M60 26v66M23 42l26 2m-26 13 26 2m-26 13 26 2m23-30 25-2m-25 17 25-2m-25 17 25-2" fill="none"/>',
    '送小礼物':'<path d="M21 49h78v54H21ZM15 34h90v18H15Z"/><path d="M60 34V103M60 34C9 36 25-5 60 34c35-39 51 2 0 0" fill="none"/>',
    '主粮':'<path d="M27 20h66l8 85H19Z"/><ellipse cx="60" cy="65" rx="18" ry="13"/><path d="M29 30h62M48 64l12-8 12 8-12 9Z" fill="none"/>',
    '礼物':'<path d="M21 49h78v54H21ZM15 34h90v18H15Z"/><path d="M60 34V103M60 34C9 36 25-5 60 34c35-39 51 2 0 0" fill="none"/>',
    '爱心小饼干':'<path d="M60 97C-18 49 24 2 60 35 96 2 138 49 60 97Z"/><circle cx="42" cy="48" r="3"/><circle cx="74" cy="55" r="3"/><circle cx="56" cy="75" r="3"/>',
    '金币':'<circle cx="60" cy="60" r="43"/><circle cx="60" cy="60" r="34"/><path d="m60 37 19 23-19 23-19-23Z"/>',
    '星星':'<path d="m60 12 14 29 33 5-24 23 6 33-29-16-29 16 6-33-24-23 33-5Z"/>',
    '记录':'<rect x="25" y="13" width="70" height="95" rx="8"/><path d="M40 34h40M40 52h40M40 70h40M40 88h20" fill="none"/>'
  };
  function node(tag,attrs={}){const e=document.createElementNS(NS,tag);for(const [key,value] of Object.entries(attrs))e.setAttribute(key,value);return e;}
  function icon(name,x,y,size){let svg;if(name==='小花围巾')svg=PrototypePetItemPreview.create({id:'scarf'},'小花围巾');else{svg=node('svg',{viewBox:'0 0 120 120'});svg.innerHTML=symbols[name]||symbols.记录;}for(const [key,value] of Object.entries({x,y,width:size,height:size,'data-result-symbol':name,'aria-hidden':'true'}))svg.setAttribute(key,value);svg.removeAttribute('role');svg.removeAttribute('aria-label');return svg;}
  function paint(screen,pet,result){
    const action=Number(screen.dataset.petPage)===5,svg=node('svg',{viewBox:'0 0 300 180',role:'img','aria-label':(action?'本次互动：':'本次奖励：')+result.text+' · 示意图'});
    if(action){const body=PrototypePetDraftPreview.petPicture(pet.kind);body.setAttribute('transform','translate(36 40) scale(1.12)');svg.append(body);svg.append(icon(symbols[result.text]?result.text:'记录',result.text==='摸摸头'?65:173,result.text==='摸摸头'?0:42,result.text==='摸摸头'?69:105));}
    else{const names=['主粮','礼物','爱心小饼干','金币','星星','小花围巾'].filter(name=>result.text.includes(name));if(!names.length)names.push('记录');names.forEach((name,i)=>svg.append(icon(name,names.length===1?85:35+i*135,25,130)));}
    if(action){
      screen.querySelector('.piece').hidden=true;screen.querySelector('.pet-result-week')?.remove();const weekly=document.createElement('section');weekly.className='pet-result-week';const label=document.createElement('span');label.textContent='本周照顾 '+PrototypePet.weekCount(pet)+' / 3 次';const progress=document.createElement('progress');progress.max=3;progress.value=Math.min(3,PrototypePet.weekCount(pet));progress.setAttribute('aria-label','本周照顾奖励进度');weekly.append(label,progress);screen.append(weekly);
    }
    let panel=screen.querySelector('.pet-result-illustration');if(!panel){panel=document.createElement('section');panel.className='pet-result-illustration';screen.append(panel);}const title=document.createElement('h2');title.textContent=action?result.text+' · 互动示意':'本次领取的奖励示意';panel.replaceChildren(title,svg);const art=screen.querySelector('.art-hero');art.setAttribute('aria-hidden','true');art.removeAttribute('role');
  }
  window.PrototypePetResultIllustration={paint};
})();
