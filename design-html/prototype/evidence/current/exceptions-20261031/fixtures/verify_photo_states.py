from pathlib import Path
import base64,json
from playwright.sync_api import sync_playwright,expect
OUT=Path(__file__).resolve().parent/'evidence/current';URL='http://127.0.0.1:8765/pages/'
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jB2kAAAAASUVORK5CYII=')
def go(p,id):p.goto(URL+id+'.html')
def fail(p,key):p.evaluate('(k)=>sessionStorage.setItem("dujia-prototype-fail-next",k)',key)
def seed(p,image=None):
 go(p,'m03-p10');p.evaluate('(image)=>localStorage.setItem("dujia-prototype-records",JSON.stringify([{id:"photo-proof",type:"photo",status:"published",title:"星星照片",caption:"今天的星星",body:"今天的星星",image,visibility:"shared",author:"小满",date:"2026-09-02",tags:["旅行"],createdAt:Date.now(),comments:[]},{id:"keep-diary",type:"diary",status:"published",title:"保留日记",body:"日记还在",visibility:"shared",createdAt:Date.now()}]))',image or 'data:image/png;base64,'+base64.b64encode(PNG).decode());p.goto(URL+'m03-p12.html?id=photo-proof')
def comments_delete(p):
 seed(p);fail(p,'photo-comment');p.locator('#reply').fill('温柔的话');p.get_by_role('button',name='发送留言').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.locator('#reply').input_value()=='温柔的话';p.get_by_role('button',name='发送留言').click();expect(p.locator('[aria-label=留言]')).to_contain_text('温柔的话');p.reload();expect(p.locator('[aria-label=留言]')).to_contain_text('温柔的话');fail(p,'photo-delete');p.locator('#more').click();p.get_by_role('button',name='删除照片',exact=True).click();p.get_by_role('button',name='确认删除',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records")).length')==2
def selectors_quota(p):
 seed(p);p.locator('.edit').click();p.wait_for_url('**/m03-p11.html?id=*');original=p.locator('[name=date]').input_value();p.locator('[name=date]').click();p.locator('dialog input[type=date]').fill('2026-01-03');p.keyboard.press('Escape');expect(p.locator('dialog[open]')).to_have_count(0);assert p.locator('[name=date]').input_value()==original
 p.locator('[name=date]').click();p.locator('dialog input[type=date]').fill('2026-01-03');p.get_by_role('button',name='使用这个日期',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);expect(p.locator('[name=date]')).to_have_value('2026-01-03');p.locator('#add-tag').click();p.get_by_label('编辑照片标签').fill('旅行、晚霞');p.get_by_role('button',name='使用这些标签',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);expect(p.locator('[name=tag]')).to_have_value('旅行、晚霞');p.locator('[name=caption]').fill('资料修改后')
 p.evaluate('()=>{window.savedSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==="dujia-prototype-records")throw new DOMException("full","QuotaExceededError");return window.savedSet.call(this,k,v)}}');p.locator('#done').click();expect(p.locator('.prototype-toast')).to_contain_text('空间不足');assert p.locator('[name=caption]').input_value()=='资料修改后';p.evaluate('()=>{Storage.prototype.setItem=window.savedSet}');p.locator('#done').click();p.wait_for_url('**/m03-p12.html?id=*');expect(p.locator('.meta')).to_contain_text('2026-01-03');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records")).find(x=>x.id==="photo-proof").tags')==['旅行','晚霞'];assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records")).some(x=>x.id==="keep-diary")')
def load_image(p):
 seed(p,'data:image/png;base64,broken');expect(p.get_by_role('button',name='重试图片',exact=True)).to_be_visible();p.locator('.edit').click();p.wait_for_url('**/m03-p11.html?id=*');p.locator('#file').set_input_files({'name':'fixed.png','mimeType':'image/png','buffer':PNG});p.locator('#done').click();p.wait_for_url('**/m03-p12.html?id=*');assert p.locator('.photo img').evaluate('e=>e.complete&&e.naturalWidth>0')
 go(p,'m03-p10');fail(p,'photo-load');p.reload();expect(p.get_by_text('相册暂时打不开',exact=True)).to_be_visible();p.get_by_role('button',name='重试加载',exact=True).click();expect(p.get_by_role('button',name='今天的星星',exact=False)).to_be_visible();p.get_by_role('button',name='刷新相册',exact=True).click();expect(p.get_by_role('button',name='今天的星星',exact=False)).to_be_visible()
def missing(p):
 go(p,'m03-p12');p.goto(URL+'m03-p12.html?id=gone');expect(p.get_by_text('这张照片已经不在了',exact=True)).to_be_visible();p.locator('.prototype-photo-state button').click();p.wait_for_url('**/m03-p09.html');expect(p.locator('.primary')).to_be_visible();p.locator('.primary').click();p.wait_for_url('**/m03-p11.html')
results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'comment-delete-failure':comments_delete,'date-tags-quota-retry':selectors_quota,'image-display-load-recovery':load_image,'missing-photo':missing}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':str(e)[:1500]}
  row.update(errors=errors,final_url=p.url);results.append(row);p.screenshot(path=str(OUT/f'photo-state-{name}.png'),full_page=True);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
(OUT/'photo-state-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');raise SystemExit(0 if all(r['passed'] for r in results) else 1)
