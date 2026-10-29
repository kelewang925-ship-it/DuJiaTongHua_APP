"""Current organizer menu results, candidate transactions and retained business suites."""
import json,traceback
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from book_test_helpers import seed,go,fixture,records,value
from verify_book_v2_reconciliation import ROOT,dependencies,sha

old=declarations('verify_book_structure.py')
def store(p):return p.evaluate('({...localStorage})')
def ready(p):expect(p.locator('.screen')).to_have_attribute('aria-busy','false');p.evaluate('document.fonts.ready')
def sample():
    book=fixture();book['chapters']=[dict(id='c'+str(i),name='第'+str(i+1)+'章') for i in range(3)]
    book['pages']=[dict(id='p'+str(i),chapterId='c'+str(i),template='日记摘录',title='片段'+str(i+1),body='这页的实际正文',date='2026-10-05') for i in range(3)]
    return book
def setup(p):seed(p,books=[sample()],records=records());go(p,13,'?id=book-state');ready(p)
def chapter(p,name):p.get_by_role('button',name='章节操作「'+name+'」',exact=True).click()
def page(p,name):p.get_by_role('button',name='页面操作「'+name+'」',exact=True).click()
def save(p):p.locator('.save').click();p.wait_for_url('**/m08-p14.html*');ready(p)
def run(p,name):
    setup(p);before=store(p)
    if name in ['chapter-up-save','chapter-down-save']:
        chapter(p,'第2章');p.get_by_role('button',name='上移章节' if name=='chapter-up-save' else '下移章节',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
        wanted=['第2章','第1章','第3章'] if name=='chapter-up-save' else ['第1章','第3章','第2章']
        assert p.locator('.v2-chapter-heading h2').all_text_contents()==wanted;assert store(p)==before;save(p);assert [c['name'] for c in value(p)[0]['chapters']]==wanted
        assert sorted(x['id'] for x in value(p)[0]['pages'])==['p0','p1','p2'];return
    if name=='chapter-rename-save':
        chapter(p,'第2章');p.get_by_role('button',name='修改章节名',exact=True).click();field=p.get_by_role('textbox',name='章节名',exact=True);field.fill('新的第二章');p.get_by_role('button',name='保存章节名',exact=True).click();expect(p.get_by_role('button',name='章节操作「新的第二章」',exact=True)).to_be_visible();assert store(p)==before;save(p);assert value(p)[0]['chapters'][1]['name']=='新的第二章';assert value(p)[0]['name']=='共同测试册';return
    if name=='chapter-add-validation-save':
        p.locator('.add').click();field=p.get_by_role('textbox',name='章节名',exact=True);p.get_by_role('button',name='保存章节',exact=True).click();expect(field).to_have_attribute('aria-invalid','true');expect(p.locator('dialog[open]')).to_have_count(1);assert store(p)==before
        field.fill('新章节');p.get_by_role('button',name='保存章节',exact=True).click();expect(p.get_by_role('button',name='章节操作「新章节」',exact=True)).to_be_visible();assert store(p)==before;save(p);assert len(value(p)[0]['chapters'])==4 and value(p)[0]['chapters'][-1]['name']=='新章节';return
    if name=='chapter-rename-cancel':
        chapter(p,'第2章');p.get_by_role('button',name='修改章节名',exact=True).click();p.get_by_role('textbox',name='章节名',exact=True).fill('不应该保存');p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('.v2-chapter-heading')).not_to_contain_text('不应该保存');assert store(p)==before;return
    if name=='chapter-boundary-feedback':
        for label,action in [('第1章','上移章节'),('第3章','下移章节')]:
            chapter(p,label);p.get_by_role('button',name=action,exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('已经在章节边界');expect(p.locator('dialog')).to_have_count(0)
        assert p.locator('.v2-chapter-heading h2').all_text_contents()==['第1章','第2章','第3章'];assert store(p)==before;return
    if name=='page-boundary-feedback':
        for action in ['上移一页','下移一页']:
            page(p,'片段1');p.get_by_role('button',name=action,exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('已经在本章边界');expect(p.locator('dialog')).to_have_count(0)
        assert p.locator('.book-page-row').all_text_contents()==['片段1','片段2','片段3'];assert store(p)==before;return
    if name=='page-target-cancel':
        page(p,'片段1');p.get_by_role('button',name='移动到另一章',exact=True).click();expect(p.locator('dialog h2')).to_have_text('选择目标章节');p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert store(p)==before;assert p.locator('.v2-page-grid').first.locator('.book-page-row').all_text_contents()==['片段1'];return
    raise AssertionError(name)

CASES=['chapter-up-save','chapter-down-save','chapter-rename-save','chapter-add-validation-save','chapter-rename-cancel','chapter-boundary-feedback','page-boundary-feedback','page-target-cancel']
RETAINED={'selected-sources-sequential-no-duplicates':'multi_source','chapter-move-delete-cancel-failure-retry':'chapter_move_delete','page-order-delete-bookmark-cleanup':'reorder_and_delete_page','structure-cross-tab-conflict-preserves-local-draft':'conflict','hidden-source-skip-failure-retry-no-fake-pages':'skip_hidden_source'}
def main():
    out=ROOT/'evidence/current/book-v2-hidden-structure';out.mkdir(parents=True,exist_ok=True);files=dependencies();rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for name in CASES+list(RETAINED):
            c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);p.set_default_navigation_timeout(15000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(case=name,passed=False)
            try:
                if name in RETAINED:old[RETAINED[name]](p)
                else:run(p,name)
                assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc();p.screenshot(path=str(out/(name+'.png')),full_page=True)
            row.update(errors=errors,effective=p.url);rows.append(row);c.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True)
        b.close()
    data=dict(dependency_files=files,producer_sha256=sha(__import__('pathlib').Path(__file__)),helpers_sha256=sha(ROOT/'book_test_helpers.py'),retained_suite_sha256=sha(ROOT/'verify_book_structure.py'),browser=version,viewport=[390,844],locale='zh-CN',timezone='Asia/Shanghai',scope='13 named current organizer/source-arrangement business executions. Five existing suite functions freshly executed; not five cached results.',results=rows)
    (out/'results.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Hidden structure outcomes:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
