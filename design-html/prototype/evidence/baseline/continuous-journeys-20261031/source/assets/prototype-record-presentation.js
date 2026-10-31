/* Presentation only: decorate the existing Card without replacing its handlers or data. */
(() => {
  const variants={'m03-p02':'home','m03-p04':'search','m03-p06':'diary','m03-p10':'album'};
  const variant=variants[location.pathname.split('/').pop()?.slice(0,7)];
  if(variant)document.querySelector('.screen').dataset.recordCollection=variant;

  function decorate(button,item,variant){
    if(button.dataset.recordPresentation)return;
    button.dataset.recordPresentation=variant;
    button.dataset.recordId=item.id;
    // Decorative images and paper lines must not change the original accessible name.
    if(!button.hasAttribute('aria-label'))button.setAttribute('aria-label',Array.from(button.children,child=>child.textContent.trim()).filter(Boolean).join(' '));
    if(variant==='album')return; // Keep the album's existing image error callback intact.
    const image=typeof item.image==='string'&&item.image&&window.PrototypePreferences.canView('record',item)?item.image:null;
    if(variant==='diary'&&!image)return;
    const preview=document.createElement('span');preview.className='record-preview';preview.setAttribute('aria-hidden','true');preview.dataset.kind=image?'image':'note';
    if(image){
      const img=document.createElement('img');img.alt='';img.decoding='async';
      if(item.sampleImage)img.classList.add('prototype-photo-sample-thumb');
      img.addEventListener('error',()=>{img.hidden=true;preview.dataset.kind='unavailable';});
      img.src=image;preview.append(img);
    }
    if(variant==='diary')button.querySelector('strong').after(preview);
    else{
      const copy=document.createElement('span');copy.className='record-card-copy';copy.append(...button.childNodes);button.append(preview,copy);
    }
  }
  window.PrototypeRecordPresentation={decorate};
})();
