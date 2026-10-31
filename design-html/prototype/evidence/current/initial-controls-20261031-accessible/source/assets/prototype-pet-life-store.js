/* Catalog, growth and settings operations extend the one shared pet document. */
(() => {
 const Pet=PrototypePet,UI=PrototypeUI,R=PrototypeRecords,P=PrototypePreferences,D=PrototypeDates;
 const catalog=[
  {id:'scarf',name:'小花围巾',type:'outfit',group:'配饰',rule:'weekly',hint:'本周3次照顾奖励'},
  {id:'bow',name:'格纹蝴蝶结',type:'outfit',group:'配饰',coins:20},
  {id:'star-bow',name:'星星领结',type:'outfit',group:'配饰',rule:'affinity',hint:'亲密度160'},
  {id:'peach-hat',name:'蜜桃帽子',type:'outfit',group:'配饰',rule:'story',hint:'记录一页成长故事'},
  {id:'crown',name:'星光皇冠',type:'outfit',group:'配饰',stars:30},
  {id:'cape',name:'雨天小斗篷',type:'outfit',group:'衣服',rule:'care7',hint:'照顾7个不同日期'},
  {id:'vest',name:'暖暖小马甲',type:'outfit',group:'衣服',coins:20},
  {id:'bell',name:'晚安铃铛',type:'outfit',group:'小物',rule:'feed20',hint:'喂食20次'},
  {id:'flower-rug',name:'花朵地毯',type:'room',group:'地毯',free:true},
  {id:'plaid-rug',name:'格纹地毯',type:'room',group:'地毯',coins:20},
  {id:'moon-rug',name:'月亮地毯',type:'room',group:'地毯',rule:'affinity',hint:'亲密度160'},
  {id:'picnic-rug',name:'野餐垫',type:'room',group:'地毯',rule:'care7',hint:'照顾7个不同日期'},
  {id:'wood-bed',name:'木质小床',type:'room',group:'小床',free:true},
  {id:'cream-bed',name:'奶油小床',type:'room',group:'小床',coins:20},
  {id:'flower-wall',name:'花朵墙饰',type:'room',group:'墙饰',free:true},
  {id:'frame-wall',name:'回忆相框',type:'room',group:'墙饰',rule:'story',hint:'记录一页成长故事'},
  {id:'vase',name:'花朵花瓶',type:'room',group:'摆件',free:true},
  {id:'lamp',name:'纪念日星灯',type:'room',group:'摆件',stars:20}
 ];
 const expectedId=Pet.read()?.id,find=id=>catalog.find(v=>v.id===id),ready=()=>{const pet=Pet.read();if(pet?.status!=='active')throw new Error('请先完成共同领养');if(pet.id!==expectedId)throw new Error('宠物已经发生变化，请重新打开后再操作');return pet;};
 const active=()=>{ready();return Pet.active();};
 const defaults={地毯:'花朵地毯',小床:'木质小床',墙饰:'花朵墙饰',摆件:'花朵花瓶'};
 const room=pet=>({...defaults,...pet.room}),settings=pet=>({reminder:true,time:'20:30',notice:true,stories:true,...pet.settings});
 const count=(pet,type)=>pet.logs.filter(v=>v.type===type).length;
 const careDays=pet=>new Set(pet.logs.filter(v=>['play','feed','water','room','note'].includes(v.type)).map(v=>v.date)).size;
 const owns=(pet,item)=>!!item&&(item.free||(item.type==='outfit'?pet.owned||[]:pet.ownedRoom||[]).includes(item.name));
 function allowed(pet,item){return !item.rule||item.rule==='affinity'&&pet.affinity>=160||item.rule==='story'&&count(pet,'note')>0||item.rule==='care7'&&careDays(pet)>=7||item.rule==='feed20'&&count(pet,'feed')>=20;}
 const label=(pet,item)=>owns(pet,item)?'已拥有':item.coins?'金币'+item.coins:item.stars?'星星'+item.stars:item.hint;
 function acquire(id){const pet=active(),item=find(id);if(!item)throw new Error('这个物品不存在');if(owns(pet,item))return true;if(!allowed(pet,item))throw new Error(item.hint||'请先满足解锁条件');if((item.coins||0)>pet.coins||(item.stars||0)>pet.stars)return {low:true};pet.coins-=item.coins||0;pet.stars-=item.stars||0;const key=item.type==='outfit'?'owned':'ownedRoom';pet[key]=pet[key]||[];pet[key].push(item.name);Pet.log(pet,'unlock','获得了'+item.name,{itemId:item.id,story:false});return Pet.commit(pet,'pet-unlock');}
 function equip(name){const pet=active(),item=catalog.find(v=>v.name===name&&v.type==='outfit');if(name&&(!item||!owns(pet,item)))throw new Error('请先解锁这件装扮');if(pet.outfit===name)return true;pet.outfit=name;Pet.log(pet,'outfit',name?'穿上了'+name:'收起了身上的装扮',{itemId:item?.id||null});return Pet.commit(pet,'pet-outfit');}
 function saveRoom(draft){const pet=active(),before=room(pet),next={};for(const group of Object.keys(defaults)){const item=catalog.find(v=>v.name===draft[group]&&v.type==='room'&&v.group===group);if(!item||!owns(pet,item))throw new Error('请先解锁'+group+'中的物品');next[group]=item.name;}const changes=Object.keys(next).filter(group=>before[group]!==next[group]).map(group=>next[group]);pet.room=next;const entry=Pet.log(pet,'room',changes.length?'更换了'+changes.join('、'):'整理了小屋',{before,after:next});pet.lastRoom=entry.id;return Pet.commit(pet,'pet-room')?{id:entry.id}:null;}
 function sources(){const records=P.sharedRecords().map(v=>({id:v.id,kind:'record',title:v.title,body:v.body||v.caption||'',url:R.route(v)})),values=key=>{const v=UI.read(key,[]);return Array.isArray(v)?v:[];};return [...records,...P.sharedMoments().map(v=>({id:v.id,kind:'moment',title:v.name,body:v.story||'',url:'m04-p03.html?id='+encodeURIComponent(v.id)})),...values('dujia-prototype-anniversaries').filter(v=>v.visibility!=='private'&&v.status!=='draft'&&D.parse(v.date)).map(v=>({id:v.id,kind:'anniversary',title:v.name,body:v.date,url:(D.occurrence(v)?.days===0?'m04-p11':'m04-p10')+'.html?id='+encodeURIComponent(v.id)}))];}
 function story(entry){if(!entry)return null;if(entry.sourceId){const source=sources().find(v=>v.id===entry.sourceId&&v.kind===(entry.sourceKind||'record'));if(!source)return {...entry,text:'关联内容不可见',blocked:true,comments:[]};return {...entry,text:source.title,body:source.body,url:source.url,blocked:false};}return {...entry,body:entry.text,blocked:false};}
 const stories=pet=>pet.logs.filter(v=>v.story!==false&&['adopt','play','feed','water','room','outfit','note','source'].includes(v.type)).map(story);
 function addStory(text){const pet=active();if(!text.trim()||text.trim().length>500)throw new Error('请填写1至500字的成长故事');Pet.log(pet,'note',text.trim(),{story:true});return Pet.commit(pet,'pet-story');}
 function link(id,kind='record'){const pet=active(),source=sources().find(v=>v.id===id&&v.kind===kind);if(!source)throw new Error('这段共同记录已经不可见，请重新选择');if(pet.logs.some(v=>v.sourceId===id&&(v.sourceKind||'record')===kind))throw new Error('这段记录已经关联过了');Pet.log(pet,'source','关联了共同记录',{sourceId:id,sourceKind:kind,story:true});return Pet.commit(pet,'pet-link');}
 function reply(id,text){const pet=active(),entry=pet.logs.find(v=>v.id===id);if(!entry||story(entry).blocked)throw new Error('这段故事已不可见');if(!P.privacy().replies)throw new Error('回应已关闭，可以在隐私设置中开启');if(!text.trim()||text.trim().length>300)throw new Error('请填写1至300字的回应');entry.comments=entry.comments||[];entry.comments.push({id:crypto.randomUUID(),author:Pet.actor(),text:text.trim(),at:Date.now()});return Pet.commit(pet,'pet-reply');}
 function achievements(pet){const values=[['meet','第一次见面',1,1,5],['play10','玩到天黑',count(pet,'play'),10,10],['feed20','默契喂食',count(pet,'feed'),20,10],['room','小屋变新了',count(pet,'room'),1,5],['care7','照顾7天',careDays(pet),7,15],['affinity','亲密搭档',pet.affinity,160,20],['days30','陪伴30天',Pet.days(pet),30,30]];return values.map(([id,name,progress,target,reward])=>({id,name,progress,target,reward,done:progress>=target,claimed:pet.claims.includes('achievement:'+id)}));}
 function achievementClaim(id){const pet=active(),item=achievements(pet).find(v=>v.id===id);if(!item||!item.done)throw new Error('还没有达成这项成就');if(item.claimed)throw new Error('这份成就奖励已经领取');pet.stars+=item.reward;pet.claims.push('achievement:'+id);Pet.log(pet,'reward','成就「'+item.name+'」奖励星星 ×'+item.reward,{achievementId:id,story:false});return Pet.commit(pet,'pet-achievement');}
 function setting(key,value){const pet=ready();if(!['reminder','notice','stories','time'].includes(key))throw new Error('设置项不存在');if(key==='time'?!/^([01]\d|2[0-3]):[0-5]\d$/.test(value):typeof value!=='boolean')throw new Error('请输入有效设置');pet.settings={...settings(pet),[key]:value};return Pet.commit(pet,'pet-setting');}
 function care(on){const pet=ready();if(on&&!UI.read('dujia-prototype-relationship',{})?.bound)throw new Error('请先重新关联另一半，再恢复共同照顾');if(pet.care===on)return true;pet.care=on;Pet.log(pet,on?'resume':'pause',on?'重新开始共同照顾':'暂停了共同照顾',{story:false});return Pet.commit(pet,'pet-care');}
 function rename(name){const pet=ready();if(!name.trim()||name.trim().length>12)throw new Error('名字需为1至12字');pet.name=name.trim();return Pet.commit(pet,'pet-rename');}
 const remove=()=>{ready();if(UI.failNext('pet-delete'))throw new Error('删除未完成，请重试');return UI.write(Pet.key,null);};
 function exported(){const pet=ready(),logs=pet.logs.map(entry=>{const view=story(entry);if(view.blocked)return {id:entry.id,type:entry.type,date:entry.date,text:'关联内容不可见',sourceId:entry.sourceId};return {...entry,...(entry.sourceId?{text:view.text,body:view.body}:{})};});return {format:'dujia-pet-memories-v1',id:pet.id,name:pet.name,kind:pet.kind,adoptedDate:pet.adoptedDate,days:Pet.days(pet),care:pet.care,stats:{energy:pet.energy,satiety:pet.satiety,mood:pet.mood,affinity:pet.affinity},inventory:{food:pet.food,gifts:pet.gifts,coins:pet.coins,stars:pet.stars,owned:pet.owned,ownedRoom:pet.ownedRoom||[]},outfit:pet.outfit,room:room(pet),settings:settings(pet),logs};}
 function download(){if(UI.failNext('pet-export'))throw new Error('导出未完成，请重试');const pet=ready(),a=document.createElement('a'),url=URL.createObjectURL(new Blob([JSON.stringify(exported(),null,2)],{type:'application/json'}));a.href=url;a.download=pet.name+'成长记录.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);return true;}
 window.PrototypePetLife={catalog,find,room,settings,count,careDays,owns,allowed,label,acquire,equip,saveRoom,sources,story,stories,addStory,link,reply,achievements,achievementClaim,setting,care,rename,remove,exported,download};
})();
