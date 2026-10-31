/* Local-only capsules; sealed content is not rendered before opening. */
(() => {
 const UI=window.PrototypeUI,D=window.PrototypeDates,KEY='dujia-prototype-capsules';
 const all=()=>{const data=UI.read(KEY,[]);return Array.isArray(data)?data:[];},find=id=>all().find(item=>item.id===id);
 function put(item){const data=all(),index=data.findIndex(v=>v.id===item.id);if(index<0)data.unshift(item);else data[index]=item;return UI.write(KEY,data);}
 const days=item=>{const date=D.parse(item.opening);return date?Math.round((date.time-D.today().time)/86400000):null;};
 const route=item=>(item.status==='draft'?'m04-p13':item.status==='opened'?'m04-p14':'m04-p15')+'.html?id='+encodeURIComponent(item.id);
 function reschedule(id,opening,expectedRaw){
  const date=D.parse(opening);if(!date||date.time<D.today().time)throw new Error('请选择今天或未来的开启日期');
  if(UI.collectionHealth(KEY).issues.length){UI.read(KEY);UI.toast('请先恢复胶囊，日期尚未保存','error');return false;}
  if(localStorage.getItem(KEY)!==expectedRaw)throw new Error('胶囊已在另一处更新，请关闭后重新检查');
  const item=find(id);if(!item||item.status!=='sealed')throw new Error('胶囊状态已改变，请重新检查');
  if(UI.failNext('capsule-date'))throw new Error('开启日期未保存，请重试');
  return put({...item,opening:date.iso,updatedAt:Date.now()});
 }
 function open(id){
  const item=find(id);if(!item)throw new Error('胶囊已不存在，请重新检查');
  if(item.status==='opened')return item;
  if(item.status!=='sealed')throw new Error('胶囊尚未封存，不能开启');
  const remaining=days(item);if(remaining===null)throw new Error('开启日期需要修正，请重新加载');if(remaining>0)throw new Error('还未到约定的开启日期');
  if(UI.failNext('capsule-open'))throw new Error('胶囊未能开启，请重试');
  const next={...item,status:'opened',openedAt:Date.now(),updatedAt:Date.now()};return put(next)?next:false;
 }
 function setReminder(id,reminder){
  const item=find(id);if(!item||item.status!=='sealed')throw new Error('胶囊状态已改变，请重新检查');
  if(UI.failNext('capsule-toggle'))throw new Error('提醒未更新，请重试');
  return put({...item,reminder});
 }
 function collect(id){
  const item=find(id);if(!item||item.status!=='opened')throw new Error('胶囊尚未开启或已不存在，请重新检查');
  if(UI.failNext('capsule-collect'))throw new Error('收录未完成，请重试');
  const values=UI.read('dujia-prototype-moments',[]),data=Array.isArray(values)?values:[];
  let moment=data.find(v=>v.id===item.momentId&&v.capsuleId===item.id)||data.find(v=>v.capsuleId===item.id),created=false;
  if(!moment){const preferred='capsule-moment-'+item.id,momentId=data.some(v=>v.id===preferred)?'capsule-moment-'+crypto.randomUUID():preferred;moment={id:momentId,name:item.name,date:D.today().iso,type:'纪念',story:item.message.slice(0,200),cover:item.photo,related:[],comments:[],capsuleId:item.id,visibility:item.visibility==='private'?'private':'shared',status:'published',createdAt:Date.now(),updatedAt:Date.now()};created=true;}
  const changes=[[KEY,all().map(value=>value.id===item.id?{...value,momentId:moment.id}:value)]];
  if(created)changes.push(['dujia-prototype-moments',[moment,...data]]);
  return window.PrototypePreferences.transaction(changes)?moment.id:false;
 }
 const notices=()=>all().filter(item=>item.status==='sealed'&&item.reminder&&days(item)!==null&&days(item)<=0).map(item=>({id:'capsule:'+item.id+':'+item.opening,kind:'capsule',targetId:item.id,title:item.name+'可以开启了',body:'到了约定的日子，看看当时留下的心意吧',url:route(item)}));
 window.PrototypeCapsules={all,find,put,days,route,notices,reschedule,open,setReminder,collect,key:KEY};
})();
