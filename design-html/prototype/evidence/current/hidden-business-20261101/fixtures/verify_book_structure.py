from pathlib import Path
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,go,fixture,records,value,fail,BASE

OUT=Path(__file__).resolve().parent/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current')
def multi_source(p):
 b=fixture();b['pages']=[];b['chapters']=[];b['selected']=[];r=records()+[dict(id='second-source',type='diary',title='第二份共同素材',body='第二份正文',date='2026-10-04',visibility='shared',status='published')];seed(p,books=[b],records=r);go(p,6,'?id=book-state');p.get_by_role('button',name='共同正文',exact=False).click();p.get_by_role('button',name='第二份共同素材',exact=False).click();p.locator('.next').click();p.wait_for_url('**/m08-p07.html*')
 for i in range(2):
  p.locator('.add').click();p.wait_for_url('**/m08-p08.html*');p.locator('.use').click();p.wait_for_url('**/m08-p09.html*');p.locator('.done').click();p.wait_for_url('**/m08-p13.html*')
  if i==0:p.get_by_role('button',name='继续编排 1 份素材',exact=True).click();p.wait_for_url('**/m08-p07.html*');expect(p.locator('.diary-title')).to_have_text('第二份共同素材')
 assert len(value(p)[0]['pages'])==2 and len({v['source']['id'] for v in value(p)[0]['pages']})==2
 expect(p.get_by_role('button',name='继续编排 1 份素材',exact=True)).to_have_count(0)

def chapter_move_delete(p):
 b=fixture();b['chapters'].append(dict(id='chapter-two',name='第二章'));seed(p,books=[b],records=records());go(p,13,'?id=book-state');p.get_by_role('button',name='页面操作「共同正文」',exact=True).click();p.get_by_role('button',name='移动到另一章',exact=True).click();p.get_by_role('button',name='第二章',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);assert value(p)[0]['pages'][0]['chapterId']=='chapter-state';p.get_by_role('button',name='章节操作「第一章」',exact=True).click();p.get_by_role('button',name='删除章节',exact=True).click();p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);p.get_by_role('button',name='章节操作「第一章」',exact=True).click();p.get_by_role('button',name='删除章节',exact=True).click();p.get_by_role('button',name='确认删除章节',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);fail(p,'book-publish');p.locator('.save').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');assert len(value(p)[0]['chapters'])==2;p.locator('.save').click();p.wait_for_url('**/m08-p14.html*');saved=value(p)[0];assert [v['id'] for v in saved['chapters']]==['chapter-two'] and saved['pages'][0]['chapterId']=='chapter-two'

def reorder_and_delete_page(p):
 b=fixture();b['pages'].append(dict(id='page-two',chapterId='chapter-state',template='日记摘录',title='独立第二页',body='正文',date='2026-10-05'));b['bookmarks']=['page-state','page-two'];b['lastPage']='page-state';seed(p,books=[b],records=records());go(p,13,'?id=book-state');p.get_by_role('button',name='页面操作「独立第二页」',exact=True).click();p.get_by_role('button',name='上移一页',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);expect(p.locator('.book-page-row').first).to_have_text('独立第二页');p.get_by_role('button',name='页面操作「共同正文」',exact=True).click();p.get_by_role('button',name='删除书页',exact=True).click();p.get_by_role('button',name='确认删除书页',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);p.locator('.save').click();p.wait_for_url('**/m08-p14.html*');saved=value(p)[0];assert [v['id'] for v in saved['pages']]==['page-two'] and saved['bookmarks']==['page-two'] and saved['lastPage']=='page-two'

def conflict(p):
 seed(p,books=[fixture()],records=records());go(p,13,'?id=book-state');p.locator('.add').click();p.get_by_role('textbox',name='章节名',exact=True).fill('本地未保存章节');p.get_by_role('button',name='保存章节',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);other=p.context.new_page();other.goto(BASE+'prototype/review.html');other.evaluate("()=>{const rows=JSON.parse(localStorage.getItem('dujia-prototype-books'));rows[0].updatedAt+=1;rows[0].name='另一窗口保存的书名';localStorage.setItem('dujia-prototype-books',JSON.stringify(rows));}");expect(p.locator('.prototype-toast')).to_contain_text('当前输入保留');p.locator('.save').click();expect(p.locator('.prototype-toast')).to_contain_text('另一处更新');assert value(p)[0]['name']=='另一窗口保存的书名' and len(value(p)[0]['chapters'])==1;expect(p.locator('.book-structure')).to_contain_text('本地未保存章节')

def skip_hidden_source(p):
 b=fixture();b['pages']=[];b['selected'].append(dict(kind='diary',id='second-source'));r=records()+[dict(id='second-source',type='diary',title='仍然共同可见的素材',body='可以编排',date='2026-10-04',visibility='shared',status='published')];r[0]['visibility']='private';seed(p,books=[b],records=r);go(p,7,'?id=book-state');expect(p.locator('.diary-title')).to_have_text('关联素材已不可见');expect(p.locator('.add')).to_be_disabled();fail(p,'book-skip');p.locator('.skip').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');assert not value(p)[0].get('skipped');p.locator('.skip').click();expect(p.locator('.diary-title')).to_have_text('仍然共同可见的素材');assert value(p)[0]['skipped']==[dict(kind='diary',id='source-state')];p.locator('.skip').click();p.wait_for_url('**/m08-p13.html*');assert len(value(p)[0]['skipped'])==2 and not value(p)[0]['pages']

rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'selected-sources-sequential-no-duplicates':multi_source,'chapter-move-delete-cancel-failure-retry':chapter_move_delete,'page-order-delete-bookmark-cleanup':reorder_and_delete_page,'structure-cross-tab-conflict-preserves-local-draft':conflict,'hidden-source-skip-failure-retry-no-fake-pages':skip_hidden_source}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(5000);p.set_default_navigation_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-2000:]}
  row.update(errors=errors,final_url=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
OUT.mkdir(parents=True,exist_ok=True);(OUT/'book-structure-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['passed'] for v in rows) else 1)
