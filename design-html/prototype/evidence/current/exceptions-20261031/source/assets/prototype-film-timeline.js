/* Native timeline decoration; source selection, removal and storage stay in the workshop controller. */
(() => {
  function reset(clips){clips.dataset.filmCount='0';}
  function decorate(button,record,kind,clips){
    const index=clips.querySelectorAll('.film-clip').length+1;
    button.classList.add('film-clip');button.dataset.sourceId=record.id;
    const sequence=document.createElement('span');sequence.className='film-sequence';sequence.textContent=index;sequence.setAttribute('aria-hidden','true');
    const preview=document.createElement('span');preview.className='film-preview';preview.dataset.kind=record.image?'image':'note';preview.setAttribute('aria-hidden','true');
    if(record.image){
      const img=document.createElement('img');img.alt='';img.decoding='async';img.addEventListener('error',()=>{img.hidden=true;preview.dataset.kind='unavailable';});img.src=record.image;preview.append(img);
    }
    const copy=document.createElement('span');copy.className='film-copy';copy.setAttribute('aria-hidden','true');
    const tag=document.createElement('small');tag.className='film-kind';tag.textContent={diary:'日记',photo:'照片',moment:'重要时刻'}[kind]||'共同片段';
    const title=document.createElement('b');title.textContent=record.title;
    const meta=document.createElement('small');meta.className='film-meta';meta.textContent=(record.date||'日期未记录')+' · 移除';
    copy.append(tag,title,meta);button.replaceChildren(sequence,preview,copy);
  }
  function finish(clips){
    const count=clips.querySelectorAll('.film-clip').length;clips.dataset.filmCount=count;
    if(!count){const hint=document.createElement('p');hint.className='film-empty';hint.textContent='还没有可用片段，先选择共同素材。';clips.append(hint);}
  }
  window.PrototypeFilmTimeline={reset,decorate,finish};
})();
