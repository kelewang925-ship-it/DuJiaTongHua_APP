"""Home reflects real diaries and search resolves the selected ID."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright,expect
parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');args=parser.parse_args()
OUT=Path(__file__).resolve().parent/'evidence'/('baseline' if args.baseline else 'current');OUT.mkdir(parents=True,exist_ok=True)
URL='http://127.0.0.1:8765/pages/'
def first(p):
 p.goto(URL+'m03-p02.html');p.evaluate('localStorage.setItem("dujia-prototype-records","[]")');p.reload();p.wait_for_url('**/m03-p01.html')
 p.get_by_role('button',name='写日记',exact=True).click();p.wait_for_url('**/m03-p05.html');p.locator('[name=title]').fill('首页的星星');p.locator('[name=body]').fill('一起度过的夜晚');p.locator('.submit').click();p.wait_for_url('**/m03-p06.html')
 p.goto(URL+'m03-p01.html');p.wait_for_url('**/m03-p02.html');p.get_by_role('button',name='首页的星星',exact=False).click();p.wait_for_url('**/m03-p08.html?id=*');expect(p.locator('h1')).to_have_text('首页的星星')
def search(p):
 p.goto(URL+'m03-p03.html');p.evaluate('localStorage.setItem("dujia-prototype-records",JSON.stringify([{id:"search-first",type:"diary",title:"星星和晚餐",body:"烛光与饭菜",status:"published",visibility:"shared",author:"小满",createdAt:Date.now(),comments:[]},{id:"search-private",type:"diary",title:"烛光下的秘密",body:"自己的想法",status:"published",visibility:"private",author:"小满",createdAt:Date.now(),comments:[]}]))')
 p.locator('#query').fill('烛光');p.locator('#query').press('Enter');p.wait_for_url('**/m03-p04.html?q=*');p.get_by_role('button',name='星星和晚餐',exact=False).click();p.wait_for_url('**/m03-p08.html?id=search-first');expect(p.locator('h1')).to_have_text('星星和晚餐')
 p.go_back();p.wait_for_url('**/m03-p04.html?q=*');p.get_by_role('button',name='烛光下的秘密',exact=False).click();p.wait_for_url('**/m03-p07.html?id=search-private');expect(p.locator('h1')).to_have_text('烛光下的秘密')
def no_results(p):
 p.goto(URL+'m03-p03.html');p.evaluate('localStorage.setItem("dujia-prototype-records","[]")');p.locator('#query').fill('不存在');p.locator('#query').press('Enter');p.wait_for_url('**/m03-p04.html?q=*');expect(p.get_by_text('没有找到相关记录',exact=True)).to_be_visible();p.get_by_role('button',name='重新搜索',exact=True).click();p.wait_for_url('**/m03-p03.html');assert p.locator('#query').input_value()=='不存在'
results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'first-use-home-updates':first,'search-selects-record':search,'empty-search-recovery':no_results}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':str(e)[:1000]}
  row.update(errors=errors,final_url=p.url);results.append(row);p.screenshot(path=str(OUT/f'home-{name}.png'),full_page=True);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
(OUT/'home-diary-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in results) else 1)
