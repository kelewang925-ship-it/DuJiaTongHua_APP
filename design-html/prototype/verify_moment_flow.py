from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright,expect
parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');args=parser.parse_args()
OUT=Path(__file__).resolve().parent/'evidence'/('baseline' if args.baseline else 'current');OUT.mkdir(parents=True,exist_ok=True)
URL='http://127.0.0.1:8765/pages/'
def go(p,id):p.goto(URL+id+'.html')
def setup(p):
 go(p,'m04-p01');p.evaluate('localStorage.setItem("dujia-prototype-moments","[]");localStorage.setItem("dujia-prototype-records",JSON.stringify([{id:"related-diary",type:"diary",title:"旅行日记",body:"一起看星星",status:"published",visibility:"shared",author:"小满",createdAt:Date.now(),comments:[]},{id:"private-diary",type:"diary",title:"私密记录",status:"published",visibility:"private",createdAt:Date.now()}]))');p.reload();p.wait_for_url('**/m04-p02.html')
def create(p):
 go(p,'m04-p04');p.locator('[name=name]').fill('我们的星空旅行');p.locator('[name=story]').fill('山顶的晚风很温柔');p.locator('#related').click();expect(p.get_by_text('私密记录',exact=True)).to_have_count(0);p.get_by_label('旅行日记',exact=True).check();p.get_by_role('button',name='关联这些记录',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);p.locator('.submit').click();p.wait_for_url('**/m04-p01.html')
def crud(p):
 setup(p);create(p);p.locator('.cards').get_by_role('button',name='我们的星空旅行',exact=False).click();p.wait_for_url('**/m04-p03.html?id=*');expect(p.locator('.description')).to_have_text('山顶的晚风很温柔');p.get_by_role('button',name='旅行日记',exact=False).click();p.wait_for_url('**/m03-p08.html?id=related-diary');p.go_back();p.wait_for_url('**/m04-p03.html?id=*');p.get_by_role('button',name='编辑时刻',exact=True).click();p.wait_for_url('**/m04-p04.html?id=*');p.locator('[name=name]').fill('重新命名的旅行');p.locator('.submit').click();p.wait_for_url('**/m04-p03.html?id=*');p.reload();expect(p.locator('.moment-title')).to_have_text('重新命名的旅行');p.locator('#more').click();p.get_by_role('button',name='删除重要时刻',exact=True).click();p.get_by_role('button',name='确认删除',exact=True).click();p.wait_for_url('**/m04-p02.html');p.reload();expect(p.get_by_text('还没有重要时刻',exact=True)).to_be_visible()
def failure(p):
 setup(p);go(p,'m04-p04');p.locator('[name=name]').fill('失败保留的旅行');p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","moment-save")');p.locator('.submit').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.locator('[name=name]').input_value()=='失败保留的旅行';assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-moments")).length')==0;p.locator('.back').click();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);p.locator('.submit').click();p.wait_for_url('**/m04-p01.html')
def comments(p):
 setup(p);create(p);p.locator('.cards').get_by_role('button',name='我们的星空旅行',exact=False).click();p.wait_for_url('**/m04-p03.html?id=*');p.locator('.message').click();p.get_by_label('回应这个时刻').fill('下一次还要一起去');p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","moment-comment")');p.get_by_role('button',name='发送回应',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.get_by_label('回应这个时刻').input_value()=='下一次还要一起去';p.get_by_role('button',name='发送回应',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);go(p,'m04-p16');expect(p.locator('[aria-label=留言]')).to_contain_text('下一次还要一起去');p.get_by_role('button',name='查看原记录',exact=False).click();p.wait_for_url('**/m04-p03.html?id=*');p.locator('.message').click();expect(p.locator('dialog[open]')).to_contain_text('下一次还要一起去')
results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'create-related-edit-delete':crud,'save-failure-dirty-retry':failure,'reply-aggregation-failure-retry':comments}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':repr(e)[:1600]}
  row.update(errors=errors,final_url=p.url);results.append(row);p.screenshot(path=str(OUT/f'moment-{name}.png'),full_page=True);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
(OUT/'moment-flow-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');raise SystemExit(0 if all(r['passed'] for r in results) else 1)
