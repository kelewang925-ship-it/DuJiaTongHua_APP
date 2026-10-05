from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright,expect
ap=argparse.ArgumentParser();ap.add_argument('--baseline',action='store_true');args=ap.parse_args()
OUT=Path(__file__).resolve().parent/'evidence'/('baseline' if args.baseline else 'current');OUT.mkdir(parents=True,exist_ok=True)
URL='http://127.0.0.1:8765/'
def go(p,n):p.goto(URL+f'pages/m07-p{n:02}.html')
def seed(p):
 go(p,4);p.evaluate('localStorage.clear();sessionStorage.clear();localStorage.setItem("dujia-prototype-relationship",JSON.stringify({bound:true,partner:"阿舟"}));localStorage.setItem("dujia-profile",JSON.stringify({nickname:"小满"}))');p.reload()
def adopt(p):
 seed(p);p.locator('.adopt').click();p.wait_for_url('**/m07-p02.html');p.locator('#pet-name').fill('团团');p.locator('#invite').click();p.wait_for_url('**/m07-p01.html');p.goto(URL+'prototype/review.html');p.get_by_role('button',name='另一半同意领养',exact=True).click();p.wait_for_url('**/m07-p03.html');expect(p.locator('.title')).to_have_text('团团的小屋');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet")).status')=='active'
def adoption_interaction(p):
 adopt(p);p.locator('.actions button').first.click();p.wait_for_url('**/m07-p06.html');p.locator('.option').nth(1).click();p.locator('#play').click();p.wait_for_url('**/m07-p05.html*');expect(p.locator('.gain.three')).to_contain_text('-12');p.locator('.home').click();p.wait_for_url('**/m07-p03.html');expect(p.locator('.stats strong').nth(1)).to_have_text('70');expect(p.locator('.stats strong').nth(3)).to_have_text('3');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet")).logs.filter(x=>x.type==="play").length')==1
def feed_and_tasks(p):
 adopt(p);go(p,8);p.locator('.foods button').nth(2).click();p.locator('#feed').click();expect(p.locator('#stock2')).to_have_text('0');expect(p.locator('#satiety')).to_have_text('96');p.locator('#feed').click();p.wait_for_url('**/m07-p09.html*');expect(p.locator('.empty')).to_contain_text('草莓布丁');p.locator('.task').click();p.wait_for_url('**/m07-p11.html');p.get_by_role('button',name='领取喂食奖励',exact=True).click();p.wait_for_url('**/m07-p10.html*');expect(p.locator('.reward')).to_contain_text('金币');go(p,11);expect(p.get_by_role('button',name='喂食奖励已领取',exact=True)).to_be_disabled();p.get_by_role('button',name='给宠物添水',exact=True).click();expect(p.get_by_role('button',name='领取添水奖励',exact=True)).to_be_visible();p.get_by_role('button',name='领取添水奖励',exact=True).click();p.wait_for_url('**/m07-p10.html*');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet")).food[0]')==13
def weekly_claim(p):
 adopt(p);go(p,6);p.locator('#play').click();p.wait_for_url('**/m07-p05.html*');go(p,8);p.locator('#feed').click();expect(p.locator('#stock0')).to_have_text('11');go(p,11);p.get_by_role('button',name='给宠物添水',exact=True).click();expect(p.get_by_role('button',name='领取添水奖励',exact=True)).to_be_visible();p.locator('.tabs button').nth(1).click();p.get_by_role('button',name='领取本周奖励',exact=True).click();p.wait_for_url('**/m07-p10.html*');expect(p.locator('.reward')).to_contain_text('小花围巾');go(p,11);p.locator('.tabs button').nth(1).click();expect(p.get_by_role('button',name='本周奖励已领取',exact=True)).to_be_disabled();pet=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet"))');assert pet['owned'].count('小花围巾')==1
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'adoption-peer-interaction-home':adoption_interaction,'feeding-empty-task-inventory':feed_and_tasks,'weekly-idempotent-reward':weekly_claim}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':repr(e)[:1600]}
  row.update(errors=errors,final_url=p.url);rows.append(row);(OUT/'pet-flow-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
