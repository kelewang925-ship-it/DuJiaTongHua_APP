"""Organizer downward move and empty-book recovery through actual UI controls."""
import json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from book_test_helpers import seed,go,fixture,records,value
from verify_book_v2_reconciliation import ROOT,dependencies,sha

legacy=declarations('verify_book_controls.py')
def store(p):return p.evaluate('({...localStorage})')
def ready(p):expect(p.locator('.screen')).to_have_attribute('aria-busy','false')
def run(p,name):
    if name=='page-down-save':
        legacy['seed'](p,'m08-p13');before=store(p);p.get_by_role('button',name='页面操作「共同日记」',exact=True).click();p.get_by_role('button',name='下移一页',exact=True).click();expect(p.locator('.book-page-row').first).to_have_text('共同照片');assert store(p)==before
        p.locator('.save').click();p.wait_for_url('**/m08-p14.html*');assert [v['id'] for v in value(p)[0]['pages']]==['page-second','page-state','page-third']
    else:
        book=fixture();book['bookmarks']=['page-state'];book['lastPage']='page-state';book['lastAnchor']=dict(pageId='page-state',offset=0,block=0);seed(p,books=[book],records=records());go(p,13,'?id=book-state');ready(p);before=store(p)
        if name=='move-without-other-chapter-feedback':
            p.get_by_role('button',name='页面操作「共同正文」',exact=True).click();p.get_by_role('button',name='移动到另一章',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.prototype-toast')).to_contain_text('先新增另一章，再移动书页');assert store(p)==before;return
        p.get_by_role('button',name='章节操作「第一章」',exact=True).click();p.get_by_role('button',name='删除章节',exact=True).click();p.get_by_role('button',name='确认删除章节',exact=True).click();expect(p.locator('.book-page-row')).to_have_count(0);assert store(p)==before
        p.locator('.save').click();p.wait_for_url('**/m08-p14.html*');saved=value(p)[0];assert saved['chapters']==[] and saved['pages']==[] and saved['bookmarks']==[] and saved['lastPage'] is None and 'lastAnchor' not in saved
        p.locator('.read').click();p.wait_for_url('**/m08-p15.html*');ready(p);expect(p.locator('.start')).to_be_disabled();p.get_by_role('button',name='添加书页',exact=True).click();p.wait_for_url('**/m08-p08.html*');ready(p)
    left=dict(before);right=store(p);left.pop('dujia-prototype-books');right.pop('dujia-prototype-books');assert left==right

CASES=['page-down-save','move-without-other-chapter-feedback','delete-last-chapter-empty-cta']
def main():
    out=ROOT/'evidence/current/book-v2-hidden-edges';out.mkdir(parents=True,exist_ok=True);files=dependencies();rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for name in CASES:
            c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(case=name,passed=False)
            try:run(p,name);assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc();p.screenshot(path=str(out/(name+'.png')),full_page=True)
            row.update(errors=errors,effective=p.url);rows.append(row);c.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps(dict(dependency_files=files,producer_sha256=sha(Path(__file__)),fixture_sha256=sha(ROOT/'verify_book_controls.py'),helpers_sha256=sha(ROOT/'book_test_helpers.py'),browser=version,scope='Three current organizer/empty-recovery outcomes only; original records are retained.',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Hidden edge outcomes:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
