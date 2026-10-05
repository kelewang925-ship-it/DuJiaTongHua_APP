from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,go,BASE,value,fail,fixture,records

OUT=Path(__file__).resolve().parent/'evidence/current'

def create_validation_dirty_failure(p):
 seed(p);go(p,4);p.locator('.next').click();expect(p.get_by_label('书名',exact=True)).to_have_attribute('aria-invalid','true');p.get_by_label('书名',exact=True).fill('保留的书名');p.get_by_label('结束月份',exact=True).fill('2026.09');p.locator('.next').click();expect(p.get_by_label('结束月份',exact=True)).to_have_attribute('aria-invalid','true');p.get_by_label('结束月份',exact=True).fill('2026.10');p.locator('.back').click();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.get_by_label('书名',exact=True)).to_have_value('保留的书名');fail(p,'book-create');p.locator('.next').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');assert value(p)==[];p.locator('.next').click();p.wait_for_url('**/m08-p05.html*');assert value(p)[0]['name']=='保留的书名'

def theme_dirty_failure(p):
 seed(p,books=[fixture()]);go(p,5,'?id=book-state');p.get_by_role('button',name='旅行手札',exact=True).click();p.locator('.back').click();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.get_by_role('button',name='旅行手札',exact=True)).to_have_attribute('aria-pressed','true');fail(p,'book-theme');p.locator('.next').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');assert value(p)[0]['theme']=='花园午后';p.locator('.next').click();p.wait_for_url('**/m08-p06.html*');assert value(p)[0]['theme']=='旅行手札'

def page_failure_permission(p):
 seed(p,books=[fixture()],records=records());go(p,9,'?id=book-state&page=page-state');expect(p.locator('#excerpt')).to_have_value('SOURCE-SECRET');p.locator('#excerpt').fill('独立编写的文字');fail(p,'book-page');p.locator('.done').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');expect(p.locator('#excerpt')).to_have_value('独立编写的文字');assert 'body' not in value(p)[0]['pages'][0];p.locator('.done').click();p.wait_for_url('**/m08-p13.html*');assert value(p)[0]['pages'][0]['body']=='独立编写的文字';p.evaluate("()=>{const rows=JSON.parse(localStorage.getItem('dujia-prototype-records'));rows[0].visibility='private';localStorage.setItem('dujia-prototype-records',JSON.stringify(rows));}");go(p,16,'?id=book-state&page=page-state');expect(p.locator('.copy')).to_contain_text('已不可见');expect(p.locator('.copy')).to_contain_text('独立编写的文字');expect(p.locator('.copy')).not_to_contain_text('SOURCE-SECRET');dump=p.evaluate("JSON.stringify(PrototypeBooks.exported('book-state'))");assert 'SOURCE-SECRET' not in dump and '独立编写的文字' in dump

def delete_cancel_failure_two_ids(p):
 first=fixture();second=fixture('second-book');seed(p,books=[first,second]);go(p,21,'?id=book-state');p.locator('.show-delete').click();p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);assert len(value(p))==2;fail(p,'book-delete');p.locator('.show-delete').click();p.get_by_role('button',name='确认删除',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('删除未完成');assert len(value(p))==2;p.locator('.show-delete').click();p.get_by_role('button',name='确认删除',exact=True).click();p.wait_for_url('**/m08-p01.html*');expect(p.locator('.books button')).to_have_count(1);assert [v['id'] for v in value(p)]==['second-book']

def load_retry_bookmark(p):
 seed(p,books=[fixture()],records=records());fail(p,'book-load');go(p,16,'?id=book-state&page=page-state');p.get_by_role('button',name='重新加载',exact=True).click();expect(p.locator('.book-load')).to_have_count(0);fail(p,'book-bookmark');p.locator('.bookmark').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');assert value(p)[0]['bookmarks']==[];p.locator('.bookmark').click();expect(p.locator('.bookmark')).to_have_attribute('aria-pressed','true');p.reload();expect(p.locator('.bookmark')).to_have_attribute('aria-pressed','true');assert value(p)[0]['lastPage']=='page-state'

def rename_archive_export(p):
 seed(p,books=[fixture()],records=records());go(p,21,'?id=book-state');p.locator('.rename').click();p.get_by_role('textbox',name='回忆册名称',exact=True).fill('改名后的册');p.get_by_role('button',name='保存书名',exact=True).click();expect(p.locator('.book-name')).to_have_text('改名后的册');p.locator('.archive').click();expect(p.locator('.archive')).to_have_text('取消归档回忆册');assert value(p)[0]['archived'];p.locator('.archive').click();expect(p.locator('.archive')).to_have_text('归档回忆册')
 with p.expect_download() as download:p.get_by_role('button',name='导出这本回忆册',exact=True).click()
 doc=json.loads(Path(download.value.path()).read_text(encoding='utf-8'));assert doc['format']=='dujia-book-v1' and doc['book']['name']=='改名后的册' and doc['book']['pages'][0]['body']=='SOURCE-SECRET'

rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'create-validation-dirty-save-retry':create_validation_dirty_failure,'theme-dirty-failure':theme_dirty_failure,'page-save-failure-source-private-independent-text':page_failure_permission,'delete-cancel-failure-stable-id':delete_cancel_failure_two_ids,'load-retry-bookmark-persistence':load_retry_bookmark,'rename-archive-real-export':rename_archive_export}.items():
  c=b.new_context(viewport={'width':390,'height':844},accept_downloads=True);p=c.new_page();p.set_default_timeout(5000);p.set_default_navigation_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-2200:]}
  row.update(errors=errors,final_url=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
OUT.mkdir(parents=True,exist_ok=True);(OUT/'book-state-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['passed'] for v in rows) else 1)
