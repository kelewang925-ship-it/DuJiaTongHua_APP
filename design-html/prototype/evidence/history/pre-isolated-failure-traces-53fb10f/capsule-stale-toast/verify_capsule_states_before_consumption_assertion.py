from pathlib import Path
import json
from playwright.sync_api import sync_playwright,expect
OUT=Path(__file__).resolve().parent/'evidence/current';URL='http://127.0.0.1:8765/pages/'
def go(p,name,query=''):p.goto(URL+name+'.html'+query)
def seed(p,status='sealed'):
 go(p,'m04-p12');p.evaluate('(status)=>{sessionStorage.setItem("dujia-prototype-today","2026-10-05");localStorage.setItem("dujia-prototype-moments","[]");localStorage.setItem("dujia-prototype-capsules",JSON.stringify([{id:"test",name:"给未来的信",message:"不应提前展示的信",opening:"2026-10-06",status,reminder:true}]))}',status)
def gates(p):
 seed(p);go(p,'m04-p14','?id=test');p.wait_for_url('**/m04-p15.html?id=test');assert '不应提前展示的信' not in p.locator('body').inner_text();expect(p.get_by_role('button',name='打开这份心意',exact=True)).to_have_count(0);go(p,'m04-p13','?id=test');p.wait_for_url('**/m04-p15.html?id=test');go(p,'m04-p15','?id=absent');expect(p.locator('.prototype-capsule-state').get_by_role('button',name='返回胶囊列表',exact=True)).to_be_visible()
def form(p):
 seed(p,'draft');go(p,'m04-p13','?id=test');p.locator('[name=message]').fill('长'*2050);expect(p.locator('[name=message]')).to_have_value('长'*2000);p.locator('[name=opening]').click();p.locator('dialog input[type=date]').fill('2026-10-04');p.get_by_role('button',name='使用这个日期',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);p.get_by_role('button',name='封存这份心意',exact=True).click();expect(p.locator('[name=opening]')).to_have_attribute('aria-invalid','true');p.locator('[name=opening]').click();p.locator('dialog input[type=date]').fill('2026-10-06');p.get_by_role('button',name='使用这个日期',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0)
 p.evaluate('(()=>{window.restoreWrite=Storage.prototype.setItem;Storage.prototype.setItem=function(key,value){if(key==="dujia-prototype-capsules")throw new DOMException("full","QuotaExceededError");return window.restoreWrite.call(this,key,value)}})()');p.get_by_role('button',name='封存这份心意',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('不足');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-capsules"))[0].status')=='draft';p.evaluate('(()=>{Storage.prototype.setItem=window.restoreWrite})()');p.get_by_role('button',name='封存这份心意',exact=True).click();p.wait_for_url('**/m04-p15.html?id=test')
def image(p):
 seed(p,'draft');go(p,'m04-p13','?id=test');p.locator('#photo').set_input_files({'name':'bad.txt','mimeType':'text/plain','buffer':b'bad'});expect(p.locator('.prototype-toast')).to_contain_text('图片');expect(p.locator('.prototype-capsule-preview')).not_to_be_visible()
 from PIL import Image
 from io import BytesIO
 stream=BytesIO();Image.new('RGB',(30,20),'blue').save(stream,format='PNG');data={'name':'blue.png','mimeType':'image/png','buffer':stream.getvalue()};p.locator('#photo').set_input_files(data);expect(p.locator('.prototype-capsule-preview')).to_be_visible();p.get_by_role('button',name='暂存草稿',exact=True).click();p.wait_for_url('**/m04-p12.html');go(p,'m04-p13','?id=test');expect(p.locator('.prototype-capsule-preview')).to_be_visible();p.get_by_role('button',name='移除照片',exact=True).click();expect(p.locator('.prototype-capsule-preview')).not_to_be_visible();p.locator('.back').click();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0)
def failures(p):
 seed(p);go(p,'m04-p15','?id=test');p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","capsule-toggle")');p.locator('.reminder input').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');expect(p.locator('.reminder input')).to_be_checked();p.locator('#more').click();p.get_by_role('button',name='删除胶囊',exact=True).click();p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","capsule-delete")');p.get_by_role('button',name='确认删除',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-capsules")).length')==1;p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","capsule-load")');go(p,'m04-p12');p.get_by_role('button',name='重试加载胶囊',exact=True).click();expect(p.locator('.cards')).to_contain_text('给未来的信');p.evaluate('localStorage.setItem("dujia-prototype-capsules","[]")');p.get_by_role('button',name='刷新胶囊',exact=True).click();expect(p.locator('.cards')).to_contain_text('还没有等待开启的胶囊')
def collect(p):
 seed(p,'opened');go(p,'m04-p14','?id=test');p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","capsule-collect")');p.locator('#collect').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-moments")).length')==0;p.locator('#collect').click();p.wait_for_url('**/m04-p03.html?id=*');go(p,'m04-p14','?id=test');p.locator('#collect').click();p.wait_for_url('**/m04-p03.html?id=*');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-moments")).length')==1
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'sealed-gates-missing':gates,'long-past-quota-retry':form,'photo-draft-remove-dirty':image,'toggle-delete-load-failures':failures,'collect-failure-idempotence':collect}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':repr(e)[:1500]}
  row.update(errors=errors,final_url=p.url);rows.append(row);p.screenshot(path=str(OUT/f'capsule-state-{name}.png'),full_page=True);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
(OUT/'capsule-state-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
