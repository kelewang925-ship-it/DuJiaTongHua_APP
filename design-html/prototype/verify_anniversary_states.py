from pathlib import Path
import json
from datetime import date
from playwright.sync_api import sync_playwright,expect
OUT=Path(__file__).resolve().parent/'evidence/current';URL='http://127.0.0.1:8765/pages/'
def go(p,id):p.goto(URL+id+'.html')
def fail(p,key):p.evaluate('(k)=>sessionStorage.setItem("dujia-prototype-fail-next",k)',key)
def seed(p):
 go(p,'m04-p09');p.evaluate('sessionStorage.setItem("dujia-prototype-today","2026-12-21");localStorage.setItem("dujia-prototype-anniversaries",JSON.stringify([{id:"ann-proof",name:"星空纪念日",date:"2026-12-24",repeat:true,enabled:true,reminderDays:3,momentId:null}]))');go(p,'m04-p07')
def dates(p):
 go(p,'m04-p09');p.evaluate('sessionStorage.setItem("dujia-prototype-today","2025-02-28")');assert p.evaluate('PrototypeDates.occurrence({date:"2024-02-29",repeat:true}).iso')=='2025-02-28';assert p.evaluate('PrototypeDates.occurrence({date:"2024-02-29",repeat:true}).days')==0;assert p.evaluate('PrototypeDates.parse("2026-02-29")') is None
 p.evaluate('sessionStorage.setItem("dujia-prototype-today","2025-03-01")');assert p.evaluate('PrototypeDates.occurrence({date:"2024-02-29",repeat:true}).iso')=='2026-02-28';assert p.evaluate('PrototypeDates.occurrence({date:"2024-02-29",repeat:true}).days')==(date(2026,2,28)-date(2025,3,1)).days
 p.evaluate('sessionStorage.setItem("dujia-prototype-today","2026-03-08")');assert p.evaluate('PrototypeDates.occurrence({date:"2026-03-09",repeat:false}).days')==1
 p.evaluate('localStorage.setItem("dujia-prototype-anniversaries",JSON.stringify([{id:"past",name:"过去的一天",date:"2026-03-01",repeat:false,enabled:false,reminderDays:0}]))');p.goto(URL+'m04-p10.html?id=past');expect(p.locator('.still')).to_have_text('已经过');expect(p.locator('.number')).to_have_text('7')
def toggle_load_delete(p):
 seed(p);fail(p,'anniversary-toggle');p.get_by_role('switch').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');expect(p.get_by_role('switch')).to_have_attribute('aria-checked','true');p.get_by_role('switch').click();expect(p.get_by_role('switch')).to_have_attribute('aria-checked','false');p.reload();expect(p.get_by_role('switch')).to_have_attribute('aria-checked','false');fail(p,'anniversary-load');p.reload();expect(p.get_by_text('纪念日暂时打不开',exact=True)).to_be_visible();p.get_by_role('button',name='重试加载纪念日',exact=True).click();expect(p.locator('.entries')).to_contain_text('星空纪念日');p.get_by_role('button',name='刷新纪念日',exact=True).click();expect(p.locator('.entries')).to_contain_text('星空纪念日');p.locator('.entries').get_by_role('button',name='星空纪念日',exact=False).click();p.wait_for_url('**/m04-p10.html?id=*');fail(p,'anniversary-delete');p.locator('#more').click();p.get_by_role('button',name='删除纪念日',exact=True).click();p.get_by_role('button',name='确认删除',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-anniversaries")).length')==1
def quota_date(p):
 seed(p);p.goto(URL+'m04-p09.html?id=ann-proof');original=p.locator('[name=date]').input_value();p.locator('[name=date]').click();p.locator('dialog input[type=date]').fill('2026-12-25');p.keyboard.press('Escape');expect(p.locator('dialog[open]')).to_have_count(0);assert p.locator('[name=date]').input_value()==original;p.locator('[name=name]').fill('很长的纪念日名称'*20);assert len(p.locator('[name=name]').input_value())==40
 p.evaluate('()=>{window.savedSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==="dujia-prototype-anniversaries")throw new DOMException("full","QuotaExceededError");return window.savedSet.call(this,k,v)}}');p.locator('.submit').click();expect(p.locator('.prototype-toast')).to_contain_text('空间不足');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-anniversaries"))[0].name')=='星空纪念日';p.evaluate('()=>{Storage.prototype.setItem=window.savedSet}');p.locator('.submit').click();p.wait_for_url('**/m04-p10.html?id=*')
def reminders(p):
 seed(p);go(p,'m04-p05');p.get_by_role('button',name='星空纪念日还有 3 天',exact=False).click();p.wait_for_url('**/m04-p10.html?id=ann-proof');go(p,'m04-p05');expect(p.get_by_role('button',name='星空纪念日还有 3 天 · 已读',exact=False)).to_be_visible();p.evaluate('localStorage.setItem("dujia-prototype-anniversaries","[]")');p.reload();p.wait_for_url('**/m04-p06.html');expect(p.get_by_text('暂时没有新提醒',exact=True)).to_be_visible()
def missing(p):
 seed(p);p.goto(URL+'m04-p10.html?id=gone');expect(p.get_by_text('这个纪念日已经不在了',exact=True)).to_be_visible();p.locator('.prototype-anniversary-state button').click();p.wait_for_url('**/m04-p07.html')
def back(p):
 seed(p);go(p,'m04-p07');p.locator('.back').click();p.wait_for_url('**/m04-p01.html')
def refresh_empty(p):
 seed(p);expect(p.locator('.entries')).to_contain_text('星空纪念日');p.evaluate('localStorage.setItem("dujia-prototype-anniversaries","[]")');p.get_by_role('button',name='刷新纪念日',exact=True).click();p.wait_for_url('**/m04-p08.html');expect(p.get_by_text('还没有纪念日',exact=True)).to_be_visible()
results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'calendar-leap-past':dates,'toggle-load-delete-failure':toggle_load_delete,'date-cancel-long-quota':quota_date,'reminders-read-and-empty':reminders,'missing-anniversary':missing,'list-back-parent':back,'refresh-after-external-delete':refresh_empty}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':repr(e)[:1800]}
  row.update(errors=errors,final_url=p.url);results.append(row);p.screenshot(path=str(OUT/f'anniversary-state-{name}.png'),full_page=True);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
(OUT/'anniversary-state-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');raise SystemExit(0 if all(r['passed'] for r in results) else 1)
