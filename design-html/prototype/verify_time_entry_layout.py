"""Added reminder and today-record controls at five widths, without covering original art."""
import json,traceback
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import ROOT,BASE,source,store
OUT=ROOT/'evidence/current';files=source();rows=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,360,390,414,430]:
  for page in ['m04-p01','m04-p02','m04-p11']:
   c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   try:
    p.goto(BASE+'prototype/review.html');title='很长的纪念日共同日记标题'*5;moment=dict(id='layout-moment',name='真实时刻',date='2026-10-06',story='原画面保持',comments=[],related=[]);ann=dict(id='layout-ann',name='今天的约定',date='2026-10-06',repeat=True,enabled=True,reminderDays=0);record=dict(id='layout-diary',type='diary',title=title,body='来自真实关联的正文',status='published',visibility='shared',anniversaryId=ann['id'],createdAt=1791217800000,comments=[])
    records=[record,dict(record,id='private-diary',title='私密日记',visibility='private'),dict(record,id='draft-diary',title='未发布日记',status='draft')]
    p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem("dujia-prototype-"+k,JSON.stringify(v));}',dict(moments=[moment]if page=='m04-p01'else[],records=records if page=='m04-p11'else[],anniversaries=[ann]if page=='m04-p11'else[],capsules=[],works=[],**{'reminder-reads':[]}))
    p.goto(BASE+'pages/'+page+'.html'+('?id=layout-ann'if page=='m04-p11'else''));p.evaluate('document.fonts.ready');p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")');before=store(p)
    if page=='m04-p11':expect(p.locator('.prototype-anniversary-today-records button')).to_have_count(1);button=p.get_by_role('button',name=title,exact=True)
    else:button=p.get_by_role('button',name='共同提醒',exact=True)
    button.scroll_into_view_if_needed();button.focus();metrics=button.evaluate('(b)=>{const r=b.getBoundingClientRect(),s=document.querySelector(".screen").getBoundingClientRect(),h=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {x:r.x,right:r.right,y:r.y,bottom:r.bottom,height:r.height,hit:b===h||b.contains(h),outsideArt:!document.querySelector(".screen").contains(b),screenWidth:s.width,overflow:document.documentElement.scrollWidth>innerWidth,focused:document.activeElement===b}}')
    assert metrics['outsideArt']and metrics['screenWidth']==min(width,431)and not metrics['overflow']and metrics['height']>=44 and metrics['hit']and metrics['focused']and metrics['x']>=0 and metrics['right']<=width+1,metrics
    if width in [320,390]:p.screenshot(path=str(OUT/f'time-entry-{page}-{width}.png'),full_page=True)
    button.press('Enter');p.wait_for_url('**/'+('m03-p08.html?id=layout-diary'if page=='m04-p11'else'm04-p06.html'));assert store(p)==before;assert not errors;row=dict(passed=True,metrics=metrics)
   except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
   row.update(page=page,width=width,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+page+' '+str(width),flush=True);c.close()
 b.close()
assert files==source();(OUT/'time-entry-layout-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
