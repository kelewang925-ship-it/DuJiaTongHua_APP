/* Small shared record repository; keeps unrelated record types when editing one. */
(() => {
  const KEY='dujia-prototype-records',UI=window.PrototypeUI;
  const all=()=>{const value=UI.read(KEY,[]);return Array.isArray(value)?value:[];};
  const find=(id,type)=>all().find(item=>item.id===id&&(!type||item.type===type));
  function put(item){const items=all(),index=items.findIndex(r=>r.id===item.id);if(index<0)items.unshift(item);else items[index]=item;return UI.write(KEY,items);}
  const remove=id=>UI.write(KEY,all().filter(r=>r.id!==id));
  const route=item=>(item.type==='photo'?'m03-p12':item.status==='draft'?'m03-p05':item.visibility==='private'?'m03-p07':'m03-p08')+'.html?id='+encodeURIComponent(item.id);
  async function readImage(file,operation){
    if(!file?.type.startsWith('image/')||file.size>1500000)throw new Error('请选择小于 1.5MB 的图片');
    if(UI.failNext(operation))throw new Error('图片读取失败，请重新选择');
    const value=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=()=>reject(new Error('图片读取失败，请重新选择'));reader.readAsDataURL(file);});
    await new Promise((resolve,reject)=>{const image=new Image();image.onload=resolve;image.onerror=()=>reject(new Error('图片无法打开，请重新选择'));image.src=value;});
    return value;
  }
  window.PrototypeRecords={all,find,put,remove,route,readImage,initialized:()=>localStorage.getItem(KEY)!==null};
})();
