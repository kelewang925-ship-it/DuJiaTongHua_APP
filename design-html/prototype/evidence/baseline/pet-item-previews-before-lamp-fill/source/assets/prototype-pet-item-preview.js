/* Native vector item illustrations. All ownership and availability come from the shared model. */
(() => {
  const shapes={
    scarf:'<path d="M20 30 60 44 100 30 88 62 60 100 32 62Z"/><path d="m27 42 33 13 33-13M60 55v33"/><circle cx="60" cy="66" r="7"/>',
    bow:'<path d="M51 51C22 20 10 30 17 60c-6 32 12 38 35 9m16-18c29-31 41-21 34 9 6 32-12 38-35 9"/><rect x="49" y="47" width="21" height="28" rx="7"/>',
    'star-bow':'<path d="M50 51 15 30v57l35-17m20-19 35-21v57L70 70"/><path d="m60 41 6 12 14 2-10 10 2 14-12-7-12 7 2-14-10-10 14-2Z"/>',
    'peach-hat':'<path d="M22 68c0-53 76-53 76 0Z"/><path d="M12 68h96v14H12Zm31-42c8-8 27-8 35 0"/><path d="M58 33c-13-12-25 14-10 24l10 6 11-6c15-10 3-36-11-24Z"/>',
    crown:'<path d="m15 39 24 19 21-37 21 37 24-19-12 51H27Z"/><path d="M28 78h64v17H28Z"/><circle cx="60" cy="65" r="7"/>',
    cape:'<path d="M40 31c0-21 40-21 40 0l27 65H13Z"/><path d="M40 31c5 14 35 14 40 0M60 44v48"/><circle cx="60" cy="49" r="5"/>',
    vest:'<path d="M40 20 18 39l14 20v41h56V59l14-20-22-19c-3 20-37 20-40 0Z"/><path d="M60 39v61M41 70h10m18 0h10"/><circle cx="66" cy="58" r="2"/>',
    bell:'<path d="M30 82c15-11 2-35 17-47 7-7 19-7 26 0 15 12 2 36 17 47Z"/><path d="M21 82h78v9H21Z"/><circle cx="60" cy="26" r="8"/><circle cx="60" cy="98" r="7"/>',
    'flower-rug':'<ellipse cx="60" cy="70" rx="48" ry="29"/><ellipse cx="60" cy="70" rx="39" ry="21"/><path d="M60 58c-20-20-25 10-10 12-15 15 9 27 13 8 18 13 32-12 12-14 1-17-18-20-15-6Z"/>',
    'plaid-rug':'<ellipse cx="60" cy="70" rx="48" ry="29"/><path d="M27 51v38m18-45v52m18-53v55m18-52v47M17 61h85M13 76h93M25 89h71"/>',
    'moon-rug':'<ellipse cx="60" cy="70" rx="48" ry="29"/><path d="M72 49c-33-7-36 42-3 41-17-8-14-29 3-41Z"/><path d="m84 55 2 4 5 1-4 4 1 5-4-2-4 2 1-5-4-4 5-1Z"/>',
    'picnic-rug':'<path d="M22 37h76l12 61H10Z"/><path d="m35 37-6 61m27-61-1 61m23-61 5 61M19 55h83M15 76h91"/>',
    'wood-bed':'<path d="M15 44c0-33 35-33 35 0h55v45H15Z"/><path d="M15 60h90M21 89v14m77-14v14"/><rect x="24" y="46" width="24" height="14" rx="5"/>',
    'cream-bed':'<rect x="13" y="45" width="94" height="48" rx="18"/><path d="M17 49c0-41 86-41 86 0M20 71h80m-78 22v10m76-10v10"/><rect x="36" y="45" width="48" height="22" rx="10"/>',
    'flower-wall':'<rect x="20" y="17" width="80" height="88" rx="7"/><path d="M60 89V55m0 19-19-9m19 1 18-12"/><circle cx="60" cy="47" r="11"/><circle cx="48" cy="36" r="10"/><circle cx="72" cy="36" r="10"/><circle cx="60" cy="25" r="9"/>',
    'frame-wall':'<rect x="18" y="16" width="84" height="90" rx="4"/><rect x="27" y="25" width="66" height="72" rx="2"/><path d="m29 89 24-26 14 12 23-32M53 58c-26-12-9-33 0-19 9-14 26 7 0 19Z"/>',
    vase:'<path d="M47 55c8 17-21 30-14 43 9 13 45 13 54 0 7-13-22-26-14-43Z"/><path d="M60 55V24m0 16L39 24m21 16 20-17"/><circle cx="39" cy="21" r="10"/><circle cx="61" cy="17" r="10"/><circle cx="82" cy="20" r="10"/>',
    lamp:'<path d="M30 101V34c0-30 56-30 56 0v9M18 101h52v9H18Z"/><path d="m86 40 5 11 13 2-9 9 2 13-11-6-11 6 2-13-9-9 13-2Z"/>'
  };
  function paint(screen,item,pet){
    const L=PrototypePetLife,n=Number(screen.dataset.petPage),state=L.owns(pet,item)?'已拥有':L.allowed(pet,item)&&pet.coins>=(item.coins||0)&&pet.stars>=(item.stars||0)?'可解锁':'未解锁';
    const card=document.createElement('section');card.className='pet-item-preview';card.dataset.state=state;
    const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 120 120');svg.setAttribute('role','img');svg.setAttribute('aria-label',item.name+' · '+state+' · 物品示意');svg.innerHTML=shapes[item.id];card.append(svg);
    if(n===13){screen.querySelector('.legend').hidden=true;card.append(screen.querySelector('.crown'));screen.querySelector('.art-middle').setAttribute('aria-label',pet.name+'的换装氛围插画');}
    else{
      screen.querySelector('.stars').hidden=true;screen.querySelector('.art-top').setAttribute('aria-label','小熊在房间读书与星灯装饰示意');
      const caption=document.createElement('p');caption.className='pet-room-art-caption';caption.textContent='小屋氛围示意 · 所选物品见下方';screen.append(caption);
    }
    const label=document.createElement('p');label.className='pet-item-state';label.textContent=state;card.append(label);screen.append(card);
  }
  window.PrototypePetItemPreview={paint};
})();
