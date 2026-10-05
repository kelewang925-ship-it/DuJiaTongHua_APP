from pathlib import Path
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,go,fixture,records,value,fail
OUT=Path(__file__).resolve().parent/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current')
IMAGE='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="80" height="100"><rect width="80" height="100" fill="%239abc87"/></svg>'
def setup(p):
 b=fixture();r=records()+[dict(id='cover-photo',type='photo',title='封面共同照片',image=IMAGE,date='2026-10-04',visibility='shared',status='published')];seed(p,books=[b],records=r)
def pick(p):
 p.locator('.toggle').click();p.get_by_role('button',name='封面共同照片',exact=False).click();expect(p.locator('dialog[open]')).to_have_count(0)
def actual_cover(p):
 setup(p);go(p,5,'?id=book-state');pick(p);expect(p.locator('.book-cover-photo img')).to_have_attribute('src',IMAGE);p.locator('[data-theme="旅行手札"]').click();expect(p.locator('.screen')).to_have_attribute('data-book-theme','旅行手札');p.locator('.next').click();p.wait_for_url('**/m08-p06.html*');assert value(p)[0]['theme']=='旅行手札';go(p,15,'?id=book-state');expect(p.locator('.book-cover-photo img')).to_have_attribute('src',IMAGE);expect(p.locator('.screen')).to_have_attribute('data-book-theme','旅行手札');go(p,16,'?id=book-state&page=page-state');assert p.locator('.book-reading-area').evaluate('e=>getComputedStyle(e).backgroundColor')=='rgb(240, 239, 226)';go(p,1);expect(p.locator('.books img')).to_have_attribute('src',IMAGE)
def invisible_and_retry(p):
 setup(p);go(p,5,'?id=book-state');pick(p);p.evaluate("()=>{const rows=JSON.parse(localStorage.getItem('dujia-prototype-records'));rows[1].visibility='private';localStorage.setItem('dujia-prototype-records',JSON.stringify(rows));}");p.locator('.next').click();expect(p.locator('.prototype-toast')).to_contain_text('封面照片已不可见');assert value(p)[0]['coverPhoto'] is False;p.locator('.toggle').click();p.locator('[data-theme="暖灯日常"]').click();fail(p,'book-theme');p.locator('.next').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');expect(p.locator('.screen')).to_have_attribute('data-book-theme','暖灯日常');assert value(p)[0]['theme']=='花园午后';p.locator('.next').click();p.wait_for_url('**/m08-p06.html*');assert value(p)[0]['theme']=='暖灯日常'
def manage_return(p):
 setup(p);go(p,21,'?id=book-state');p.get_by_role('button',name='修改主题与封面',exact=True).click();p.wait_for_url('**/m08-p05.html*');pick(p);p.locator('.next').click();p.wait_for_url('**/m08-p21.html*');expect(p.locator('.book-cover-photo img')).to_have_attribute('src',IMAGE);go(p,15,'?id=book-state');p.evaluate("()=>{const rows=JSON.parse(localStorage.getItem('dujia-prototype-records'));rows[1].visibility='private';localStorage.setItem('dujia-prototype-records',JSON.stringify(rows));}");p.reload();expect(p.locator('.book-cover-photo img')).to_have_count(0);expect(p.locator('.book-cover-photo')).to_contain_text('照片已不可见');assert p.evaluate("PrototypeBooks.exported('book-state').coverPhoto") is False
def live_cover_privacy(p):
 setup(p);go(p,5,'?id=book-state');pick(p);p.locator('[data-theme="暖灯日常"]').click();other=p.context.new_page();other.goto('http://127.0.0.1:8765/prototype/review.html');other.evaluate("()=>{const rows=JSON.parse(localStorage.getItem('dujia-prototype-records'));rows[1].visibility='private';localStorage.setItem('dujia-prototype-records',JSON.stringify(rows));}");expect(p.locator('.book-cover-photo img')).to_have_count(0);expect(p.locator('.book-cover-photo')).to_contain_text('照片已不可见');expect(p.locator('.screen')).to_have_attribute('data-book-theme','暖灯日常');assert value(p)[0]['theme']=='花园午后';other.close()

rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'cover-theme-shelf-toc-reading':actual_cover,'cover-private-save-reject-and-theme-failure-retry':invisible_and_retry,'manage-cover-return-and-private-mask':manage_return,'live-private-cover-mask-preserves-theme-draft':live_cover_privacy}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-2000:]}
  row.update(errors=errors,url=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
OUT.mkdir(parents=True,exist_ok=True);(OUT/'book-cover-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['passed'] for v in rows) else 1)
