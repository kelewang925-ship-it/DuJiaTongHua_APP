from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright,expect
parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');args=parser.parse_args();OUT=Path(__file__).resolve().parent/'evidence'/('baseline' if args.baseline else 'current');OUT.mkdir(parents=True,exist_ok=True)
URL='http://127.0.0.1:8765/pages/'
def go(p,id):p.goto(URL+id+'.html')
def setup(p):
 go(p,'m04-p07');p.evaluate('localStorage.setItem("dujia-prototype-anniversaries","[]");localStorage.setItem("dujia-prototype-records","[]");localStorage.setItem("dujia-prototype-moments",JSON.stringify([{id:"linked-moment",name:"星空时刻",date:"2026-01-03",type:"旅行",story:"一起看星星",comments:[]}]))');p.reload();p.wait_for_url('**/m04-p08.html')
def create(p):
 go(p,'m04-p09');p.locator('[name=name]').fill('星星纪念日');p.locator('[name=date]').click();p.locator('dialog input[type=date]').fill('2026-12-24');p.get_by_role('button',name='使用这个日期',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);p.locator('[name=moment]').select_option('linked-moment');p.locator('.submit').click();p.wait_for_url('**/m04-p07.html')
def crud(p):
 setup(p);create(p);p.locator('.entries').get_by_role('button',name='星星纪念日',exact=False).click();p.wait_for_url('**/m04-p10.html?id=*');expect(p.locator('h1')).to_have_text('星星纪念日');p.get_by_role('button',name='星空时刻',exact=False).click();p.wait_for_url('**/m04-p03.html?id=linked-moment');p.go_back();p.wait_for_url('**/m04-p10.html?id=*');p.get_by_role('button',name='编辑纪念日',exact=True).click();p.wait_for_url('**/m04-p09.html?id=*');p.locator('[name=name]').fill('重新命名的纪念日');p.locator('.submit').click();p.wait_for_url('**/m04-p10.html?id=*');p.reload();expect(p.locator('h1')).to_have_text('重新命名的纪念日');p.locator('#more').click();p.get_by_role('button',name='删除纪念日',exact=True).click();p.get_by_role('button',name='确认删除',exact=True).click();p.wait_for_url('**/m04-p08.html');p.reload();assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-anniversaries")).length')==0
def failure_toggle(p):
 setup(p);go(p,'m04-p09');p.locator('[name=name]').fill('保存失败保留');p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","anniversary-save")');p.locator('.submit').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-anniversaries")).length')==0;p.locator('.back').click();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);p.locator('.submit').click();p.wait_for_url('**/m04-p07.html');p.get_by_role('switch').click();expect(p.get_by_role('switch')).to_have_attribute('aria-checked','false');p.reload();expect(p.get_by_role('switch')).to_have_attribute('aria-checked','false');p.get_by_role('switch').click();expect(p.get_by_role('switch')).to_have_attribute('aria-checked','true')
def today_record(p):
 setup(p);p.evaluate('sessionStorage.setItem("dujia-prototype-today","2026-12-24")');create(p);p.locator('.entries').get_by_role('button',name='星星纪念日',exact=False).click();p.wait_for_url('**/m04-p11.html?id=*');expect(p.locator('h1')).to_have_text('星星纪念日');p.get_by_role('button',name='一起留下今天的记录',exact=True).click();p.wait_for_url('**/m03-p05.html?anniversary=*');p.locator('[name=body]').fill('今天一起许愿');p.locator('.submit').click();p.wait_for_url('**/m03-p06.html');go(p,'m04-p07');p.locator('.entries').get_by_role('button',name='星星纪念日',exact=False).click();p.wait_for_url('**/m04-p11.html?id=*');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records"))[0].anniversaryId');go(p,'m03-p02');expect(p.locator('.moment')).to_contain_text('星星纪念日');expect(p.locator('.moment')).to_contain_text('今天');p.locator('.moment').click();p.wait_for_url('**/m04-p11.html?id=*')
results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'create-related-edit-delete':crud,'save-failure-dirty-toggle':failure_toggle,'today-create-associated-record':today_record}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':repr(e)[:1500]}
  row.update(errors=errors,final_url=p.url);results.append(row);p.screenshot(path=str(OUT/f'anniversary-{name}.png'),full_page=True);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
(OUT/'anniversary-flow-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');raise SystemExit(0 if all(r['passed'] for r in results) else 1)
