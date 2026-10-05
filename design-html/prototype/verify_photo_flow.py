from pathlib import Path
import argparse,base64,json
from playwright.sync_api import sync_playwright,expect
parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');args=parser.parse_args()
OUT=Path(__file__).resolve().parent/'evidence'/('baseline' if args.baseline else 'current');OUT.mkdir(parents=True,exist_ok=True)
URL='http://127.0.0.1:8765/pages/'
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jB2kAAAAASUVORK5CYII=')
def go(p,id):p.goto(URL+id+'.html')
def empty(p):go(p,'m03-p10');p.evaluate('localStorage.setItem("dujia-prototype-records","[]")');p.reload();p.wait_for_url('**/m03-p09.html')
def fill(p,private=False):
 go(p,'m03-p11');p.locator('#file').set_input_files({'name':'memory.png','mimeType':'image/png','buffer':PNG});expect(p.locator('#selected')).to_be_visible();p.locator('[name=caption]').fill('旅行时的星星');p.locator('[name=tag]').fill('旅行')
 if private:p.locator('[value=private]').check()
def crud(p):
 empty(p);fill(p);p.locator('.submit').click();p.wait_for_url('**/m03-p10.html');p.get_by_role('button',name='旅行时的星星',exact=False).click();p.wait_for_url('**/m03-p12.html?id=*');expect(p.locator('.caption')).to_have_text('旅行时的星星');p.reload();expect(p.locator('.caption')).to_have_text('旅行时的星星')
 p.locator('.edit').click();p.wait_for_url('**/m03-p11.html?id=*');p.locator('[name=caption]').fill('旅行中的晚霞');p.locator('#done').click();p.wait_for_url('**/m03-p12.html?id=*');expect(p.locator('.caption')).to_have_text('旅行中的晚霞')
 p.locator('#more').click();p.get_by_role('button',name='删除照片',exact=True).click();p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0)
 p.locator('#more').click();p.get_by_role('button',name='删除照片',exact=True).click();p.get_by_role('button',name='确认删除',exact=True).click();p.wait_for_url('**/m03-p09.html');p.reload();assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records")).length')==0
def failure(p):
 empty(p);go(p,'m03-p11');p.locator('.submit').click();expect(p.locator('.prototype-toast')).to_contain_text('选择照片')
 p.locator('#file').set_input_files({'name':'broken.png','mimeType':'image/png','buffer':b'broken'});expect(p.locator('.prototype-toast')).to_contain_text('无法打开');fill(p);p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","photo-save")');p.locator('.submit').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.locator('[name=caption]').input_value()=='旅行时的星星';assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records")).length')==0
 p.locator('.back').click();expect(p.locator('dialog[open]')).to_be_visible();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);p.locator('.submit').click();p.wait_for_url('**/m03-p10.html')
def privacy_search(p):
 empty(p);fill(p,True);p.locator('.submit').click();p.wait_for_url('**/m03-p10.html');p.get_by_role('tab',name='共同可见',exact=True).click();expect(p.get_by_text('没有符合条件的照片',exact=True)).to_be_visible();p.get_by_role('button',name='清除筛选',exact=True).click();p.get_by_role('button',name='旅行时的星星',exact=False).click();p.wait_for_url('**/m03-p12.html?id=*');assert p.locator('#message').is_hidden()
 go(p,'m03-p03');p.locator('#query').fill('星星');p.locator('#query').press('Enter');p.wait_for_url('**/m03-p04.html?q=*');p.get_by_role('button',name='旅行时的星星',exact=False).click();p.wait_for_url('**/m03-p12.html?id=*')
results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'upload-edit-delete':crud,'validation-image-save-dirty-retry':failure,'private-filter-search':privacy_search}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':str(e)[:1200]}
  row.update(errors=errors,final_url=p.url);results.append(row);p.screenshot(path=str(OUT/f'photo-{name}.png'),full_page=True);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
(OUT/'photo-flow-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');raise SystemExit(0 if all(r['passed'] for r in results) else 1)
