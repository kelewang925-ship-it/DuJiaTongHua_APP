/* Local-only capsules; sealed content is not rendered before opening. */
(() => {
 const UI=window.PrototypeUI,D=window.PrototypeDates,KEY='dujia-prototype-capsules';
 const all=()=>{const data=UI.read(KEY,[]);return Array.isArray(data)?data:[];},find=id=>all().find(item=>item.id===id);
 function put(item){const data=all(),index=data.findIndex(v=>v.id===item.id);if(index<0)data.unshift(item);else data[index]=item;return UI.write(KEY,data);}
 const days=item=>{const date=D.parse(item.opening);return date?Math.round((date.time-D.today().time)/86400000):null;};
 const route=item=>(item.status==='draft'?'m04-p13':item.status==='opened'?'m04-p14':'m04-p15')+'.html?id='+encodeURIComponent(item.id);
 const notices=()=>all().filter(item=>item.status==='sealed'&&item.reminder&&days(item)!==null&&days(item)<=0).map(item=>({id:'capsule:'+item.id+':'+item.opening,kind:'capsule',targetId:item.id,title:item.name+'可以开启了',body:'到了约定的日子，看看当时留下的心意吧',url:route(item)}));
 window.PrototypeCapsules={all,find,put,days,route,notices,key:KEY};
})();
