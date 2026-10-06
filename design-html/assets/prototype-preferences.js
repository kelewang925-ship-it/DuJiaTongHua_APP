/* Shared local preferences and export contracts; no remote account service. */
(() => {
 const UI=window.PrototypeUI;
 const records=()=>window.PrototypeRecords?.all()||array('dujia-prototype-records');
 const object=(key,defaults)=>{const value=UI.read(key);return {...defaults,...(value&&typeof value==='object'&&!Array.isArray(value)?value:{})};};
 const privacy=()=>object('dujia-privacy',{scope:'共同可见',shared:true,space:true,replies:true,reminders:true});
 const notifications=()=>object('dujia-notifications',{all:true,replies:true,moments:true,capsule:true,workshop:true});
 const profile=()=>object('dujia-profile',{nickname:'小满',saying:'把平凡的日子写成童话',birthday:'',color:'#f0b59d',avatar:null,aliases:[]});
 const preferences=()=>object('dujia-prototype-preferences',{reduceMotion:false,language:'zh-CN',twoFactor:false,autoBackup:false});
 const enabled=kind=>notifications().all&&notifications()[kind]!==false&&(kind!=='replies'||privacy().reminders);
 const array=key=>{const data=UI.read(key,[]);return Array.isArray(data)?data:[];};
 const own=record=>!record.author||[profile().nickname,...(Array.isArray(profile().aliases)?profile().aliases:[])].includes(record.author);
 function petSnapshot(){const pet=UI.read('dujia-prototype-pet');if(!pet?.id)return null;return {...pet,logs:(pet.logs||[]).map(entry=>{if(!entry.sourceId)return entry;const kind=entry.sourceKind||'record',values=kind==='record'?records():array(kind==='moment'?'dujia-prototype-moments':'dujia-prototype-anniversaries'),source=values.find(v=>v.id===entry.sourceId&&v.status!=='draft'&&(kind==='record'?v.visibility==='shared':v.visibility!=='private'));return source?entry:{id:entry.id,type:entry.type,date:entry.date,sourceId:entry.sourceId,sourceKind:kind,text:'关联内容不可见',story:entry.story};})};}
  function recordDate(record){if(record.date)return record.date;if(typeof record.createdAt!=='number'||!Number.isFinite(record.createdAt))return '';const date=new Date(record.createdAt);if(!Number.isFinite(date.getTime()))return '';return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;}
  function bookSources(book=null) {
    const sharedRecords=records().filter(v=>v.status!=='draft'&&v.visibility==='shared');
    const result=sharedRecords.map(v=>({kind:v.type,id:v.id,title:v.title,body:v.body||v.caption||'',image:v.image||null,date:recordDate(v),url:window.PrototypeRecords?.route(v)||((v.type==='photo'?'m03-p12':'m03-p08')+'.html?id='+encodeURIComponent(v.id))}));
    for(const v of array('dujia-prototype-moments').filter(v=>v.visibility!=='private'&&v.status!=='draft'))result.push({kind:'moment',id:v.id,title:v.name,body:v.story||'',image:v.cover||null,date:v.date,url:'m04-p03.html?id='+encodeURIComponent(v.id)});
    for(const v of array('dujia-prototype-works').filter(v=>v.status==='ready')) {
      if(v.sourceKind!=='free'&&v.sourceIds?.length&&!v.sourceIds.every(id=>v.sourceKind==='moment'?result.some(s=>s.kind==='moment'&&s.id===id):sharedRecords.some(s=>s.id===id)))continue;
      const completed=new Date(v.completedAt||v.createdAt);if(!Number.isFinite(completed.getTime()))continue;
      result.push({kind:'work',id:v.id,title:v.name,body:v.story||'',image:sharedRecords.find(s=>v.sourceIds?.includes(s.id))?.image||null,date:completed.toISOString().slice(0,10),url:'m05-p08.html?id='+encodeURIComponent(v.id)});
    }
    const pet=UI.read('dujia-prototype-pet');
    if(pet?.status==='active')for(const entry of (Array.isArray(pet.logs)?pet.logs:[]).filter(v=>v.story!==false&&['adopt','play','feed','water','room','outfit','note','source'].includes(v.type))){
      let title=entry.text,body=entry.text;
      if(entry.sourceId){const kind=entry.sourceKind||'record',linked=kind==='record'?sharedRecords.find(v=>v.id===entry.sourceId):array(kind==='moment'?'dujia-prototype-moments':'dujia-prototype-anniversaries').find(v=>v.id===entry.sourceId&&v.visibility!=='private'&&v.status!=='draft');if(!linked)continue;if(kind==='anniversary'){const date=new Date(linked.date+'T00:00:00Z');if(!Number.isFinite(date.getTime())||date.toISOString().slice(0,10)!==linked.date||Number(String(linked.date).slice(0,4))<1900)continue;}title=linked.title||linked.name;body=linked.body||linked.caption||linked.story||(kind==='anniversary'?linked.date:'');}
      result.push({kind:'pet',id:pet.id+':'+entry.id,title,body,date:entry.date,url:'m07-p19.html?id='+encodeURIComponent(entry.id)});
    }
    return result.filter(v=>{if(!book)return true;const m=(v.date||'').slice(0,7).replace('-','.');return /^\d{4}\.(0[1-9]|1[0-2])$/.test(m)&&Array.isArray(book.dates)&&m>=book.dates[0]&&m<=book.dates[1];});
  }
  const bookSource=(reference,book)=>reference?bookSources(book).find(v=>v.kind===reference.kind&&v.id===reference.id):null;
  function bookPageView(page,book) {
    const linked=page.source?bookSource(page.source,book):null,blocked=!!page.sourceUnavailable||!!page.source&&!linked;
    const images=blocked?[]:(page.photos||[]).map(photo=>{const value=bookSource(photo.source,book);return value?.image?{image:value.image,crop:photo.crop||{x:50,y:50,zoom:1}}:null;}).filter(Boolean);
    const photo=page.photoSource?bookSource(page.photoSource,book):null;
    return {...page,title:page.title??linked?.title??(blocked?'关联内容不可见':'新的一页'),body:page.body??linked?.body??'',date:page.date??linked?.date??(window.PrototypeDates?.today().iso||new Date().toLocaleDateString('en-CA')),image:blocked?null:photo?.image??linked?.image??null,images,blocked,url:linked?.url||null,supplements:blocked?[]:page.supplements||[]};
  }
  function bookExport(book){return {...book,selected:[],skipped:[],coverPhoto:bookSource(book.coverPhoto,book)?book.coverPhoto:false,pages:book.pages.map(page=>{const view=bookPageView(page,book);if(view.blocked)return {id:page.id,chapterId:page.chapterId,template:page.template,source:page.source,title:page.title||'关联内容不可见',body:page.body||'',date:page.date||'',supplements:[]};return {...page,title:view.title,body:view.body,date:view.date,image:view.image,images:view.images,photos:(page.photos||[]).filter(v=>bookSource(v.source,book)?.image)};})};}
  const books=()=>array('dujia-prototype-books').filter(v=>v?.id&&Array.isArray(v.pages)&&Array.isArray(v.chapters));
  const bookSnapshot=(shared=false)=>books().filter(v=>!shared||v.status==='published').map(bookExport);
 function snapshot(shared=false){return {format:'dujia-prototype-backup-v1',createdAt:Date.now(),scope:shared?'shared':'accessible',world:UI.read('dujia-prototype-relationship',{})?.profile||{},pet:petSnapshot(),books:bookSnapshot(shared),tags:tags().filter(v=>!shared||v.scope==='shared'),records:records().filter(v=>shared?v.visibility==='shared'&&v.status!=='draft':v.visibility!=='private'||own(v)),moments:array('dujia-prototype-moments').filter(v=>!shared||v.visibility!=='private'&&v.status!=='draft'),anniversaries:array('dujia-prototype-anniversaries').filter(v=>!shared||v.visibility!=='private'&&v.status!=='draft'),capsules:array('dujia-prototype-capsules').filter(v=>!shared||v.status==='opened'&&v.visibility!=='private'),works:array('dujia-prototype-works').filter(v=>!shared||bookSources().some(source=>source.kind==='work'&&source.id===v.id)),...(!shared?{profile:profile(),privacy:privacy(),notifications:notifications(),preferences:preferences(),feedback:UI.read('dujia-feedback-draft',''),membership:UI.read('dujia-prototype-membership')}:{} )};}
 const backupInputs=['dujia-prototype-records','dujia-prototype-moments','dujia-prototype-anniversaries','dujia-prototype-capsules','dujia-prototype-works','dujia-prototype-pet','dujia-prototype-books','dujia-prototype-tags','dujia-prototype-relationship','dujia-profile'];
 function backupHealth(){
  const issues=[],raw={};
  try{
   for(const key of backupInputs)raw[key]=localStorage.getItem(key);
   if(UI.hasAccountProblem())issues.push('资料');
   if(window.PrototypeRecords?.health().issues.length)issues.push('记录');
   if(UI.workHealth().issues.length)issues.push('作品');
   if(tagHealth().issues.length)issues.push('标签');
   for(const [key,name]of [['moments','时刻'],['anniversaries','纪念日'],['capsules','胶囊']])if(UI.collectionHealth('dujia-prototype-'+key).issues.length)issues.push(name);
   for(const [key,name]of [['pet','宠物'],['books','回忆册']])if(UI.collectionHealth('dujia-prototype-'+key).issues.length)issues.push(name);
   return {issues,raw};
  }catch{return {issues:['本地存储'],raw,unavailable:true};}
 }
 function backup(automatic=false){
  const state=backupHealth(),prefix=automatic?'内容已保存，但备份未更新。':'备份未更新。';
  if(state.issues.length){UI.toast(prefix+'请先恢复'+state.issues.join('、')+'；不会替换现有备份','error');return false;}
  try{
   const previous=localStorage.getItem('dujia-prototype-backup'),value=JSON.stringify(snapshot(true));
   if(backupInputs.some(key=>localStorage.getItem(key)!==state.raw[key])||localStorage.getItem('dujia-prototype-backup')!==previous){UI.toast(prefix+'数据已在其他页面变化，请重新备份；不会替换现有备份','error');return false;}
   localStorage.setItem('dujia-prototype-backup',value);return true;
  }catch{UI.toast(prefix+'请检查本地存储或整理空间后重试；不会替换现有备份','error');return false;}
 }
 const contentKeys=['dujia-prototype-records','dujia-prototype-moments','dujia-prototype-anniversaries','dujia-prototype-capsules','dujia-prototype-works','dujia-prototype-pet','dujia-prototype-books'];
 function afterWrite(key){if(![...contentKeys,'dujia-prototype-relationship'].includes(key)||!preferences().autoBackup)return;backup(true);}
 function transaction(changes){if(changes.some(([key,value])=>!UI.canWrite(key,value)))return false;const previous=changes.map(([key])=>[key,localStorage.getItem(key)]);try{for(const[key,value]of changes)localStorage.setItem(key,JSON.stringify(value));for(const[key]of changes)afterWrite(key);return true;}catch{for(const[key,value]of previous){try{if(value===null)localStorage.removeItem(key);else localStorage.setItem(key,value);}catch{}}UI.toast('本地空间不足，未能更新，请重试','error');return false;}}
 const TAG_KEY='dujia-prototype-tags';
 let tagRecoveryOpen=false,tagRepairing=false,tagButton,tagPromptRaw;
 function analyzeTags(raw){
  const state={raw,items:[],issues:[]};if(raw===null)return state;
  let values;try{values=JSON.parse(raw);}catch{state.issues.push('标签文件暂时无法解析');return state;}
  if(!Array.isArray(values)){state.issues.push('标签集合格式不正确');return state;}
  const ids=new Set(),names=new Set();
  for(const value of values){
   if(!value||typeof value!=='object'||Array.isArray(value)||typeof value.id!=='string'||!value.id.trim()||typeof value.name!=='string'||!value.name.trim()||ids.has(value.id)||names.has(value.name.trim().toLocaleLowerCase())){state.issues.push('部分标签暂时无法读取');continue;}
   ids.add(value.id);names.add(value.name.trim().toLocaleLowerCase());const item={...value};
   if(!['personal','shared'].includes(item.scope)){item.scope='personal';state.issues.push('标签范围暂时无法读取，将恢复为我的标签');}
   state.items.push(item);
  }
  return state;
 }
 function tagHealth(){try{return analyzeTags(localStorage.getItem(TAG_KEY));}catch{return {raw:null,items:[],issues:['浏览器暂时无法访问标签'],unavailable:true};}}
 function observeTags(){
  if(document.readyState==='loading')return;
  const state=tagHealth();if(!state.issues.length){tagButton?.remove();tagButton=null;tagPromptRaw=undefined;return;}
  if(!tagButton){tagButton=UI.components.button('恢复标签',recoverTags,{variant:'secondary'});tagButton.classList.add('prototype-tag-recovery');document.body.append(tagButton);}
  if(UI.hasAccountProblem())return;
  if(window.PrototypeRecords?.health().issues.length){window.PrototypeRecords.all();return;}
  if(UI.workHealth().issues.length){UI.read('dujia-prototype-works');return;}
  if(tagPromptRaw!==state.raw&&!document.querySelector('dialog[open]')){tagPromptRaw=state.raw;queueMicrotask(recoverTags);}
 }
 async function recoverTags(){
  if(UI.hasAccountProblem())return UI.recoverAccount();
  if(window.PrototypeRecords?.health().issues.length)return window.PrototypeRecords.recover();
  if(UI.workHealth().issues.length)return UI.recoverWorks();
  if(tagRecoveryOpen)return;tagRecoveryOpen=true;
  try{while(true){
   const state=tagHealth();if(!state.issues.length){observeTags();return;}
   const action=await UI.modal({title:'标签需要恢复',message:state.unavailable?'暂时无法访问标签，请检查浏览器存储设置或重新检查。':`原始标签仍完整保留，可读取 ${state.items.length} 个。恢复前暂停标签保存和删除，避免覆盖原文。记录中的标签文字不会被删除。`,cancel:'稍后处理',actions:[{label:'导出原始标签',value:'export',disabled:!!state.unavailable},{label:'恢复可读标签',value:'repair',disabled:!!state.unavailable},{label:'重新检查',value:'retry'}]});
   if(!action)return;
   if(action==='export'){const url=URL.createObjectURL(new Blob([state.raw],{type:'application/json;charset=utf-8'})),link=document.createElement('a');link.href=url;link.download='独家童话标签原始内容.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);continue;}
   if(action==='retry'){if(!tagHealth().issues.length){observeTags();await UI.go(location.href,{replace:true});return;}continue;}
   if(!await UI.modal({title:'保留原始副本并恢复标签？',message:`先完整保存原文，再恢复 ${state.items.length} 个可读标签。无法读取的标签仍保留在副本中；无效范围恢复为我的标签。记录本身及其中的标签文字不变。${state.items.length?'':'当前无法读取标签，之后可重新创建或从记录中查看。'}`,cancel:'取消',confirm:'确认恢复',danger:true}))continue;
   if(localStorage.getItem(TAG_KEY)!==state.raw){UI.toast('标签已在其他页面更新，请重新检查','error');observeTags();return;}
   if(!UI.write('dujia-prototype-tag-recovery-'+crypto.randomUUID(),state.raw))return;
   if(localStorage.getItem(TAG_KEY)!==state.raw){UI.toast('标签已在保存副本期间更新，尚未替换','error');observeTags();return;}
   tagRepairing=true;let saved;try{saved=UI.write(TAG_KEY,state.items);}finally{tagRepairing=false;}
   if(!saved)return;
   UI.toast('已保留原始副本并恢复标签','success');observeTags();await UI.go(location.href,{replace:true});return;
  }}catch{UI.toast('暂时无法恢复标签，原文仍保留，请重试','error');}finally{tagRecoveryOpen=false;}
 }
 UI.protectStorage(TAG_KEY,value=>{
  if(!tagRepairing&&tagHealth().issues.length){observeTags();UI.toast('请先恢复标签，原始内容尚未改变','error');return false;}
  if(analyzeTags(JSON.stringify(value)).issues.length){UI.toast('标签格式不完整，尚未保存','error');return false;}
  return true;
 });
 function tags(){const state=tagHealth();if(state.issues.length)observeTags();const base=[['日常','personal'],['旅行','personal'],['想念','personal'],['美食','personal'],['春日野餐','shared'],['第一次旅行','shared'],['我们的家','shared']],data=state.raw===null&&!state.unavailable?base.map(([name,scope],index)=>({id:'tag-'+index,name,scope})):[...state.items];for(const record of records().filter(v=>v.visibility!=='private'||own(v)))for(const name of record.tags||[])if(name.trim()&&!data.some(v=>v.name.trim().toLocaleLowerCase()===name.trim().toLocaleLowerCase()))data.push({id:'tag-auto-'+encodeURIComponent(name),name,scope:record.visibility==='shared'?'shared':'personal'});return data;}
 function initializeTags(){const state=tagHealth();return state.raw===null&&!state.unavailable?UI.write(TAG_KEY,tags()):!state.issues.length;}
 function tagUpdate(item,remove=false){const old=tags().find(v=>v.id===item.id),data=tags().filter(v=>v.id!==item.id);if(!remove)data.push(item);const updatedRecords=records().map(record=>record.visibility==='private'&&!own(record)?record:({...record,tags:[...new Set((record.tags||[]).flatMap(name=>name===old?.name?remove?[]:[item.name]:[name]))]}));return transaction([['dujia-prototype-tags',data],['dujia-prototype-records',updatedRecords]]);}
 function logout(){if(!UI.write('dujia-prototype-session',{...UI.read('dujia-prototype-session',{}),loggedIn:false}))return false;sessionStorage.removeItem('dujia-prototype-challenge');return UI.go('m01-p01.html',{force:true});}
 async function login(phone){
  if(!preferences().twoFactor)return UI.write('dujia-prototype-session',{loggedIn:true,phone});
  let allowed=false;const expiresAt=Date.now()+600000,form=document.createElement('form'),label=document.createElement('label'),input=document.createElement('input'),button=document.createElement('button');form.className='prototype-two-factor-form';label.textContent='演示验证码 284631';input.type='text';input.inputMode='numeric';input.maxLength=6;input.setAttribute('aria-label','两步验证码');button.type='submit';button.textContent='验证并登录';label.append(input);form.append(label,button);form.addEventListener('submit',event=>{event.preventDefault();if(input.value!=='284631'||Date.now()>expiresAt){UI.fieldError(input,'验证码不正确或已过期，请重新登录');return;}UI.busy(button,'验证中…',async()=>{if(UI.failNext('two-factor-verify'))throw new Error('验证未完成，请重试');if(!UI.write('dujia-prototype-session',{loggedIn:true,phone}))return false;allowed=true;await UI.back();return true;});});await UI.sheet({title:'两步验证',message:'此处验证本地演示代码，不会发送短信。',content:form,actions:[]});return allowed;
 }
 const cacheKeys=['dujia-prototype-search-history','dujia-prototype-last-query','dujia-diary-list-state','dujia-photo-album-state'];
 function bytes(){let total=0;for(let i=0;i<localStorage.length;i++){const key=localStorage.key(i);if(/^(dujia-|fairy-)/.test(key))total+=(key.length+(localStorage.getItem(key)||'').length)*2;}return total;}
 function cacheBytes(){return cacheKeys.reduce((total,key)=>total+((localStorage.getItem(key)||'').length+(sessionStorage.getItem(key)||'').length)*2,0);}
 function clearCache(){for(const key of cacheKeys){localStorage.removeItem(key);sessionStorage.removeItem(key);}return true;}
 function deleteAccount(){if(UI.failNext('settings-account-delete'))throw new Error('注销演示未完成，请重试');const keys=[];for(let i=0;i<localStorage.length;i++){const key=localStorage.key(i);if(/^(dujia-|fairy-)/.test(key))keys.push(key);}for(const key of keys)localStorage.removeItem(key);for(const key of contentKeys)localStorage.setItem(key,key==='dujia-prototype-pet'?'null':'[]');const sessionKeys=[];for(let i=0;i<sessionStorage.length;i++){const key=sessionStorage.key(i);if(/^(dujia-|fairy-)/.test(key))sessionKeys.push(key);}for(const key of sessionKeys)sessionStorage.removeItem(key);return UI.go('m01-p01.html',{force:true});}
 window.PrototypePreferences={books,bookSources,bookSource,bookPageView,bookExport,bookSnapshot,privacy,notifications,profile,preferences,enabled,own,snapshot,backup,backupHealth,afterWrite,transaction,tags,tagUpdate,tagHealth,recoverTags,initializeTags,logout,login,bytes,cacheBytes,clearCache,deleteAccount};
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',observeTags,{once:true});else queueMicrotask(observeTags);
 addEventListener('storage',event=>{if(event.key===TAG_KEY||event.key===null)observeTags();});
})();
