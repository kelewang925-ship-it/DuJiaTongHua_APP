"""Storage/image/delete recovery and five-width long-content controls."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright,expect
OUT=Path(__file__).resolve().parent/'evidence/current';results=[]
parser=argparse.ArgumentParser();parser.add_argument('--case');args=parser.parse_args()
URL='http://127.0.0.1:8765/pages/'
def go(p,id):p.goto(URL+id+'.html')
def setup(p):go(p,'m03-p06');p.evaluate('localStorage.setItem("dujia-prototype-records","[]")');go(p,'m03-p05');p.locator('[name=title]').fill('保存时的故事');p.locator('[name=body]').fill('记住这一刻')
def fail(p,key):p.evaluate('(k)=>sessionStorage.setItem("dujia-prototype-fail-next",k)',key)
def storage(p):
 setup(p);p.evaluate('()=>{window.originalSetItem=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==="dujia-prototype-records")throw new DOMException("full","QuotaExceededError");return window.originalSetItem.call(this,k,v)}}')
 p.locator('.submit').click();expect(p.locator('.prototype-toast')).to_contain_text('空间不足');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records")).length')==0;assert p.locator('[name=body]').input_value()=='记住这一刻'
 p.evaluate('()=>{Storage.prototype.setItem=window.originalSetItem}');p.locator('.submit').click();p.wait_for_url('**/m03-p06.html');expect(p.get_by_role('button',name='保存时的故事',exact=False)).to_be_visible()
def images(p):
 setup(p);invalid={'name':'broken.png','mimeType':'image/png','buffer':b'not an image'};p.locator('#file').set_input_files(invalid);expect(p.locator('.prototype-toast')).to_contain_text('无法打开');assert p.locator('#preview').is_hidden()
 import base64
 png=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jB2kAAAAASUVORK5CYII=')
 fail(p,'diary-image');p.locator('#file').set_input_files({'name':'one.png','mimeType':'image/png','buffer':png});expect(p.locator('.prototype-toast')).to_contain_text('读取失败');assert p.locator('#preview').is_hidden()
 p.locator('#file').set_input_files({'name':'two.png','mimeType':'image/png','buffer':png});expect(p.locator('#preview')).to_be_visible();p.locator('.submit').click();p.wait_for_url('**/m03-p06.html');p.get_by_role('button',name='保存时的故事',exact=False).click();p.wait_for_url('**/m03-p08.html?id=*');expect(p.locator('.photo')).to_have_class('photo prototype-diary-real-photo');p.reload();assert 'data:image/png' in p.locator('.photo').get_attribute('style')
def delete_comment(p):
 setup(p);p.locator('.submit').click();p.wait_for_url('**/m03-p06.html');p.get_by_role('button',name='保存时的故事',exact=False).click();p.wait_for_url('**/m03-p08.html?id=*')
 fail(p,'diary-comment');p.locator('#reply').fill('保留的留言');p.get_by_role('button',name='发送留言').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.locator('#reply').input_value()=='保留的留言';assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records"))[0].comments.length')==0
 p.get_by_role('button',name='发送留言').click();expect(p.locator('[aria-label=留言]')).to_contain_text('保留的留言');assert p.locator('#message button[type=submit] svg').count()==1,'Loading must restore the send icon';fail(p,'diary-delete');p.locator('#more').click();p.get_by_role('button',name='删除日记',exact=True).click();p.get_by_role('button',name='确认删除',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records")).length')==1
def saved_filter(p):
 setup(p);p.goto(URL+'m03-p06.html');p.locator('#filter').click();p.get_by_label('可见范围').select_option('private');p.get_by_role('button',name='应用筛选',exact=True).click();expect(p.get_by_text('没有符合条件的日记',exact=True)).to_be_visible();p.locator('.write').click();p.wait_for_url('**/m03-p05.html');p.locator('[name=title]').fill('筛选后新记录');p.locator('[name=body]').fill('共同可见的日记');p.locator('.submit').click();p.wait_for_url('**/m03-p06.html');expect(p.get_by_role('button',name='筛选后新记录',exact=False)).to_be_visible()
def missing(p):
 go(p,'m03-p08');p.goto(URL+'m03-p08.html?id=missing');expect(p.get_by_text('这篇日记已经不在了',exact=True)).to_be_visible();p.locator('.prototype-diary-state button').click();p.wait_for_url('**/m03-p06.html')
def list_failure(p):
 go(p,'m03-p06');fail(p,'diary-load');p.reload();expect(p.get_by_text('日记暂时打不开',exact=True)).to_be_visible();p.get_by_role('button',name='重新加载日记',exact=True).click();expect(p.locator('.prototype-diary-card').first).to_be_visible();p.get_by_role('button',name='刷新日记',exact=True).click();expect(p.locator('.prototype-diary-card').first).to_be_visible()
def widths(p,width):
 p.set_viewport_size({'width':width,'height':932});setup(p);p.locator('[name=title]').fill('很长的标题'*20);p.locator('[name=body]').fill('今天的故事和每一句温柔的话。'*700);assert len(p.locator('[name=title]').input_value())==60;assert len(p.locator('[name=body]').input_value())==5000
 p.locator('.submit').click();p.wait_for_url('**/m03-p06.html');p.locator('.prototype-diary-card').first.click();p.wait_for_url('**/m03-p08.html?id=*');p.evaluate('document.fonts.ready')
 assert p.evaluate('document.documentElement.scrollWidth')==width
 p.locator('.body-text').focus();p.keyboard.press('End');p.wait_for_timeout(180);assert p.locator('.body-text').evaluate('e=>e.scrollTop')>0,'Long diary body must support keyboard scrolling'
 for selector in ['.back','.edit','#more','#emoji','#message button[type=submit]']:
  metrics=p.locator(selector).evaluate('(e)=>{const r=e.getBoundingClientRect();const hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {width:r.width,height:r.height,reachable:e===hit||e.contains(hit)}}');assert metrics['reachable'],(width,selector,metrics)
 p.screenshot(path=str(OUT/f'diary-long-detail-{width}.png'),full_page=True)
 p.locator('#more').click();p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0)
def validation(p):
 go(p,'m03-p05');p.locator('.submit').click();expect(p.locator('[name=title]')).to_have_attribute('aria-invalid','true');p.locator('[name=title]').fill('只写标题');expect(p.locator('[name=title]')).to_have_attribute('aria-invalid','false');p.locator('.submit').click();expect(p.locator('[name=body]')).to_have_attribute('aria-invalid','true');p.locator('[name=body]').fill('补上正文');expect(p.locator('[name=body]')).to_have_attribute('aria-invalid','false');p.locator('.submit').click();p.wait_for_url('**/m03-p06.html')

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 cases={'field-validation-recovery':validation,'list-failure-retry-refresh':list_failure,'quota-retry':storage,'image-recovery-persistence':images,'comment-delete-failure':delete_comment,'saved-record-visible-after-filter':saved_filter,'missing-record':missing}
 for width in [320,375,390,414,430]:cases[f'long-content-{width}']=lambda p,w=width:widths(p,w)
 for name,run in cases.items():
  if args.case and name!=args.case:continue
  c=browser.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':str(e)[:1500]}
  row.update(errors=errors,final_url=p.url);results.append(row);p.screenshot(path=str(OUT/f'diary-state-{name}.png'),full_page=True);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 browser.close()
(OUT/('diary-state-results.json' if not args.case else 'diary-state-'+args.case+'.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in results) else 1)
