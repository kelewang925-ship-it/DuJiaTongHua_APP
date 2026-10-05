from pathlib import Path
import json,argparse
from playwright.sync_api import sync_playwright,expect
ap=argparse.ArgumentParser();ap.add_argument('--baseline',action='store_true');args=ap.parse_args()
OUT=Path(__file__).resolve().parent/'evidence'/('baseline' if args.baseline else 'current');OUT.mkdir(parents=True,exist_ok=True)
URL='http://127.0.0.1:8765/pages/'
def go(p,name):p.goto(URL+name+'.html')
def setup(p):
 go(p,'m04-p12');p.evaluate('localStorage.setItem("dujia-prototype-capsules","[]");localStorage.setItem("dujia-prototype-moments","[]");sessionStorage.setItem("dujia-prototype-today","2026-10-05")');p.reload()
def fill(p):
 go(p,'m04-p13');p.locator('[name=name]').fill('给未来的信');p.locator('[name=message]').fill('未来也要一起看星星');p.locator('[name=opening]').click();p.locator('dialog input[type=date]').fill('2026-10-06');p.get_by_role('button',name='使用这个日期',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0)
def main(p):
 setup(p);fill(p);p.get_by_role('button',name='暂存草稿',exact=True).click();p.wait_for_url('**/m04-p12.html');p.get_by_role('tab',name='草稿',exact=True).click();p.locator('.cards').get_by_role('button',name='给未来的信',exact=False).click();p.wait_for_url('**/m04-p13.html?id=*');expect(p.locator('[name=message]')).to_have_value('未来也要一起看星星');p.get_by_role('button',name='封存这份心意',exact=True).click();p.wait_for_url('**/m04-p15.html?id=*');expect(p.locator('.countdown')).to_contain_text('1');assert '未来也要一起看星星' not in p.locator('body').inner_text();p.evaluate('sessionStorage.setItem("dujia-prototype-today","2026-10-06")');p.reload();p.get_by_role('button',name='打开这份心意',exact=True).click();p.wait_for_url('**/m04-p14.html?id=*');expect(p.locator('.letter-body')).to_have_text('未来也要一起看星星');p.locator('#collect').click();p.wait_for_url('**/m04-p03.html?id=*');expect(p.get_by_role('heading',name='给未来的信',exact=True)).to_be_visible();go(p,'m04-p12');p.get_by_role('tab',name='已经开启',exact=True).click();p.locator('.cards').get_by_role('button',name='给未来的信',exact=False).click();p.locator('#collect').click();p.wait_for_url('**/m04-p03.html?id=*');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-moments")).length')==1
def failure(p):
 setup(p);fill(p);p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","capsule-save")');p.get_by_role('button',name='封存这份心意',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');expect(p.locator('[name=message]')).to_have_value('未来也要一起看星星');p.locator('.back').click();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);p.get_by_role('button',name='封存这份心意',exact=True).click();p.wait_for_url('**/m04-p15.html?id=*');p.locator('.reminder input').click();expect(p.locator('.reminder input')).not_to_be_checked();p.reload();expect(p.locator('.reminder input')).not_to_be_checked();p.locator('#more').click();p.get_by_role('button',name='删除胶囊',exact=True).click();p.get_by_role('button',name='确认删除',exact=True).click();p.wait_for_url('**/m04-p12.html');expect(p.locator('.cards')).to_contain_text('还没有等待开启的胶囊');p.reload();assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-capsules")).length')==0
def reminder(p):
 setup(p);fill(p);p.get_by_role('button',name='封存这份心意',exact=True).click();p.wait_for_url('**/m04-p15.html?id=*');p.evaluate('sessionStorage.setItem("dujia-prototype-today","2026-10-06");localStorage.setItem("dujia-prototype-anniversaries","[]")');go(p,'m04-p05');p.get_by_role('button',name='给未来的信',exact=False).click();p.wait_for_url('**/m04-p15.html?id=*');p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","capsule-open")');p.get_by_role('button',name='打开这份心意',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-capsules"))[0].status')=='sealed';p.get_by_role('button',name='打开这份心意',exact=True).click();p.wait_for_url('**/m04-p14.html?id=*')
results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'draft-seal-open-collect':main,'save-dirty-toggle-delete':failure,'reminder-open-retry':reminder}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':repr(e)[:1500]}
  row.update(errors=errors,final_url=p.url);results.append(row);p.screenshot(path=str(OUT/f'capsule-{name}.png'),full_page=True);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
(OUT/'capsule-flow-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');raise SystemExit(0 if all(r['passed'] for r in results) else 1)
