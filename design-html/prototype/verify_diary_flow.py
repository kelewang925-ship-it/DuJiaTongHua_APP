"""Diary user flows prove displayed data, context and durable mutations."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright,expect
parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');args=parser.parse_args()
OUT=Path(__file__).resolve().parent/'evidence'/('baseline' if args.baseline else 'current');OUT.mkdir(parents=True,exist_ok=True)
def go(p,id):p.goto('http://127.0.0.1:8765/pages/'+id+'.html')
def empty(p):go(p,'m03-p06');p.evaluate('localStorage.setItem("dujia-prototype-records","[]")');p.reload()
def create(p,title='星星下的晚餐',private=False):
 go(p,'m03-p05');p.locator('[name=title]').fill(title);p.locator('[name=body]').fill('一起做饭，收藏今天的小幸福。')
 if private:p.locator('[value=private]').check()
 p.locator('#diary .submit').click();p.wait_for_url('**/m03-p06.html',timeout=4000)
def crud(p):
 empty(p);expect(p.get_by_text('还没有日记',exact=True)).to_be_visible();create(p)
 p.get_by_role('button',name='星星下的晚餐',exact=False).click();p.wait_for_url('**/m03-p08.html?id=*')
 expect(p.locator('.body-text')).to_contain_text('一起做饭');p.locator('.edit').click();p.wait_for_url('**/m03-p05.html?id=*')
 assert p.locator('[name=title]').input_value()=='星星下的晚餐';p.locator('[name=title]').fill('修改后的晚餐');p.locator('#diary .submit').click();p.wait_for_url('**/m03-p08.html?id=*')
 expect(p.locator('h1')).to_have_text('修改后的晚餐');p.reload();expect(p.locator('h1')).to_have_text('修改后的晚餐')
 p.get_by_role('button',name='更多操作').click();p.get_by_role('button',name='删除日记',exact=True).click();p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0)
 expect(p.locator('h1')).to_have_text('修改后的晚餐');p.get_by_role('button',name='更多操作').click();p.get_by_role('button',name='删除日记',exact=True).click();p.get_by_role('button',name='确认删除',exact=True).click();p.wait_for_url('**/m03-p06.html')
 p.reload();expect(p.get_by_text('还没有日记',exact=True)).to_be_visible();go(p,'m03-p02');p.wait_for_url('**/m03-p01.html')
def failed_save(p):
 empty(p);go(p,'m03-p05');p.locator('[name=title]').fill('失败不丢');p.locator('[name=body]').fill('仍然保留内容');p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","diary-save")')
 p.locator('#diary .submit').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.locator('[name=title]').input_value()=='失败不丢';assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records")).length')==0
 p.locator('.back').click();expect(p.locator('dialog[open]')).to_be_visible();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0)
 p.locator('#diary .submit').click();p.wait_for_url('**/m03-p06.html');expect(p.get_by_role('button',name='失败不丢',exact=False)).to_be_visible()
def draft_filter(p):
 empty(p);go(p,'m03-p05');p.locator('[name=title]').fill('未完成的信');p.locator('#top-save').click();p.wait_for_url('**/m03-p06.html');p.locator('[data-tab=draft]').click()
 p.get_by_role('button',name='未完成的信',exact=False).click();p.wait_for_url('**/m03-p05.html?id=*');assert p.locator('[name=title]').input_value()=='未完成的信'
 p.locator('[name=body]').fill('写好了');p.locator('#diary .submit').click();p.wait_for_url('**/m03-p06.html');p.locator('[data-tab=all]').click();p.locator('#filter').click();p.get_by_label('可见范围').select_option('private');p.get_by_role('button',name='应用筛选',exact=True).click();expect(p.get_by_text('没有符合条件的日记',exact=True)).to_be_visible()
 p.get_by_role('button',name='清除筛选',exact=True).click();expect(p.get_by_role('button',name='未完成的信',exact=False)).to_be_visible()
def comments_privacy(p):
 empty(p);create(p);p.get_by_role('button',name='星星下的晚餐',exact=False).click();p.wait_for_url('**/m03-p08.html?id=*');p.locator('#reply').fill('明天也一起做饭');p.get_by_role('button',name='发送留言').click();expect(p.locator('[aria-label=留言]')).to_contain_text('明天也一起做饭');p.reload();expect(p.locator('[aria-label=留言]')).to_contain_text('明天也一起做饭')
 create(p,'自己的小秘密',True);p.get_by_role('button',name='自己的小秘密',exact=False).click();p.wait_for_url('**/m03-p07.html?id=*');assert p.locator('#message').count()==0;expect(p.locator('h1')).to_have_text('自己的小秘密')
results=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'create-edit-delete':crud,'save-failure-dirty-retry':failed_save,'draft-publish-filter':draft_filter,'comments-and-privacy':comments_privacy}.items():
  c=browser.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':str(e)[:1500]}
  row.update(errors=errors,final_url=p.url);results.append(row);p.screenshot(path=str(OUT/f'diary-{name}.png'),full_page=True);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 browser.close()
(OUT/'diary-flow-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in results) else 1)
