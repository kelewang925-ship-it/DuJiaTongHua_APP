/* Calendar days use UTC arithmetic to avoid daylight-saving hour drift. */
(() => {
 const DAY=86400000;
 function parse(value){const m=String(value).match(/^(\d{4})-(\d{2})-(\d{2})$/);if(!m)return null;const[y,month,day]=m.slice(1).map(Number),time=Date.UTC(y,month-1,day),date=new Date(time);return y>=1900&&y<=9999&&date.getUTCFullYear()===y&&date.getUTCMonth()===month-1&&date.getUTCDate()===day?{y,month,day,time,iso:value}:null;}
 const iso=(y,m,d)=>`${y}-${String(m).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
 function today(){const override=parse(sessionStorage.getItem('dujia-prototype-today'));if(override)return override;const now=new Date();return parse(iso(now.getFullYear(),now.getMonth()+1,now.getDate()));}
 const add=(value,days)=>{const date=new Date(value.time+days*DAY);return parse(iso(date.getUTCFullYear(),date.getUTCMonth()+1,date.getUTCDate()));};
 function occurrence(item){const base=parse(item.date),now=today();if(!base)return null;let result=base;if(item.repeat){let year=Math.max(base.y,now.y);const candidate=y=>parse(iso(y,base.month,Math.min(base.day,new Date(Date.UTC(y,base.month,0)).getUTCDate())));result=candidate(year);if(result.time<now.time)result=candidate(year+1);}return {...result,days:Math.round((result.time-now.time)/DAY)};}
 window.PrototypeDates={parse,today,add,iso,occurrence};
})();
