/* Small shared record repository; keeps unrelated record types when editing one. */
(() => {
  const KEY='dujia-prototype-records',UI=window.PrototypeUI;
  let repairInProgress=false,recoveryOpen=false,lastPromptRaw,button;
  const object=value=>value&&typeof value==='object'&&!Array.isArray(value);
  const nonempty=value=>typeof value==='string'&&value.trim().length>0;
  function analyze(raw){
    const result={raw,items:[],issues:[]};if(raw===null)return result;
    let values;try{values=JSON.parse(raw);}catch{result.issues.push('记录文件暂时无法解析');return result;}
    if(!Array.isArray(values)){result.issues.push('记录集合的格式不正确');return result;}
    const ids=new Set();
    for(const [index,item] of values.entries()){
      if(!object(item)||!nonempty(item.id)||!['diary','photo'].includes(item.type)||typeof item.title!=='string'||ids.has(item.id)||['body','caption','author','mood','date','image'].some(k=>item[k]!=null&&typeof item[k]!=='string')||item.visibility!=null&&!['private','shared'].includes(item.visibility)||item.status!=null&&!['draft','published'].includes(item.status)||['createdAt','updatedAt'].some(k=>item[k]!=null&&(!Number.isFinite(item[k])||typeof item[k]!=='number'))){result.issues.push('第'+(index+1)+'条记录暂时无法读取');continue;}
      ids.add(item.id);let next=item;
      if(item.tags!=null&&(!Array.isArray(item.tags)||item.tags.some(v=>typeof v!=='string'))){next={...next,tags:Array.isArray(item.tags)?item.tags.filter(v=>typeof v==='string'):[]};result.issues.push('第'+(index+1)+'条记录有无法读取的标签');}
      if(item.comments!=null){
        const seen=new Set(),comments=Array.isArray(item.comments)?item.comments.filter(v=>{if(!object(v)||!nonempty(v.id)||typeof v.author!=='string'||typeof v.text!=='string'||seen.has(v.id)||v.createdAt!=null&&!Number.isFinite(v.createdAt))return false;seen.add(v.id);return true;}):[];
        if(!Array.isArray(item.comments)||comments.length!==item.comments.length){next={...next,comments};result.issues.push('第'+(index+1)+'条记录有无法读取的回应');}
      }
      result.items.push(next);
    }
    return result;
  }
  function inspect(){try{return analyze(localStorage.getItem(KEY));}catch{return {raw:null,items:[],issues:['浏览器暂时无法访问本地记录'],unavailable:true};}}
  function downloadOriginal(raw,name='独家童话原始记录.json'){
    const url=URL.createObjectURL(new Blob([raw],{type:'application/json;charset=utf-8'})),link=document.createElement('a');
    link.href=url;link.download=name;try{link.click();}finally{setTimeout(()=>URL.revokeObjectURL(url),1000);}
  }
  async function showArchives(){
    while(true){
      let keys;try{keys=Object.keys(localStorage).filter(key=>/^dujia-prototype-(record|account|work|tag)-recovery-/.test(key)).sort();}
      catch{UI.toast('暂时无法读取原始副本，请检查存储设置后重试','error');return;}
      const picked=await UI.sheet({title:'恢复原始副本',message:keys.length?`本机保留了 ${keys.length} 份原始副本。\n副本可能包含私人记录，仅供你下载检查，不会导入或覆盖当前记录。`:'还没有恢复副本。记录恢复时保存的原始内容会出现在这里。',cancel:'关闭',actions:keys.map((key,index)=>({label:'原始副本 '+(index+1),value:key}))});
      if(!picked)return;
      let stored;try{stored=localStorage.getItem(picked);}catch{UI.toast('暂时无法读取这个副本，请重试','error');return;}
      if(stored===null){UI.toast('副本已不存在，请重新选择','error');continue;}
      let raw=stored,damaged=false;try{const value=JSON.parse(stored);if(typeof value==='string')raw=value;else damaged=true;}catch{damaged=true;}
      const health=analyze(raw),chosen=await UI.modal({title:'原始副本',message:(damaged?'副本格式无法解析，将下载存储中的完整原文。':picked.startsWith('dujia-prototype-tag-recovery-')?'标签完整原始内容，仅供本地检查。':picked.startsWith('dujia-prototype-work-recovery-')?'工坊作品完整原始内容，仅供本地检查。':picked.startsWith('dujia-prototype-account-recovery-')?'个人、关系、登录或邀请资料原始内容，仅供本地检查。':`可读取 ${health.items.length} 条记录${health.issues.length?'，部分内容仍无法读取':''}。`)+`\n原文共 ${raw.length} 个字符，可能包含私人内容。下载不会改变当前记录。`,confirm:'下载原始副本',cancel:'关闭'});
      if(!chosen)return;
      try{downloadOriginal(raw,'独家童话原始副本-'+picked.slice(-8)+'.json');}catch{UI.toast('下载未能开始，请重新打开副本重试','error');}
      return;
    }
  }
  function observe(state){
    if(!state.issues.length){button?.remove();button=null;lastPromptRaw=undefined;return;}
    if(!button){button=UI.components.button('恢复记录',()=>showRecovery(),{variant:'secondary'});button.classList.add('prototype-record-recovery');button.setAttribute('aria-label','恢复记录');document.body.append(button);}
    if(lastPromptRaw!==state.raw){lastPromptRaw=state.raw;queueMicrotask(()=>{if(!UI.hasAccountProblem?.())showRecovery();});}
  }
  async function showRecovery(){
    if(UI.hasAccountProblem?.()){await UI.recoverAccount();return;}
    if(recoveryOpen)return;recoveryOpen=true;
    try{
      while(true){
        const state=inspect();if(!state.issues.length){observe(state);return;}
        const action=await UI.modal({title:'记录需要恢复',message:state.unavailable?'浏览器暂时无法访问本地记录，请检查存储设置或重新检查。':`原始内容仍完整保留，当前可读取 ${state.items.length} 条记录。\n部分内容暂时无法读取。可以先导出原始内容，或保留副本后恢复可读记录。`,cancel:'稍后处理',actions:[{label:'导出原始记录',value:'export',disabled:!!state.unavailable},{label:'恢复可读记录',value:'repair',disabled:!!state.unavailable},{label:'重新检查',value:'retry'}]});
        if(!action)return;
        if(action==='export'){
          downloadOriginal(state.raw);continue;
        }
        if(action==='retry'){
          const current=inspect();
          if(!current.issues.length){observe(current);await UI.go(location.href,{replace:true});return;}
          continue;
        }
        const confirmed=await UI.modal({title:'保留原始副本并恢复？',message:`先完整保存原始副本，再恢复 ${state.items.length} 条可读记录。\n暂时无法读取的内容仍保留在副本中。${state.items.length?'':'当前无法解析出可读记录，确认后将从空列表重新开始。'}`,cancel:'取消',confirm:'确认恢复', danger: true});
        if(!confirmed)continue;
        if(localStorage.getItem(KEY)!==state.raw){UI.toast('记录已在其他页面更新，请重新检查','error');observe(inspect());return;}
        const archive='dujia-prototype-record-recovery-'+crypto.randomUUID();
        if(!UI.write(archive,state.raw))return;
        if(localStorage.getItem(KEY)!==state.raw){UI.toast('记录已在其他页面更新，请重新检查','error');observe(inspect());return;}
        repairInProgress=true;let saved;try{saved=UI.write(KEY,state.items);}finally{repairInProgress=false;}
        if(!saved)return;
        UI.toast('已保留原始副本并恢复记录','success');observe(inspect());await UI.go(location.href,{replace:true});return;
      }
    }finally{recoveryOpen=false;}
  }
  UI.protectStorage(KEY,value=>{
    if(repairInProgress)return true;
    const current=inspect();observe(current);
    if(current.issues.length){UI.toast('请先恢复记录，原始内容尚未改变','error');return false;}
    if(analyze(JSON.stringify(value)).issues.length){UI.toast('记录格式不完整，尚未保存','error');return false;}
    return true;
  });
  const all=()=>{const state=inspect();observe(state);return state.items;};
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
  window.PrototypeRecords={all,find,put,remove,route,readImage,health:inspect,recover:showRecovery,showArchives,initialized:()=>localStorage.getItem(KEY)!==null};
})();
