"""Actual peer updates while a library is open, then return to its shelf."""
import argparse,json,traceback
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,go
from verify_book_v2_hidden_reading import samples,ready,store,library,run as previous_run
from verify_book_conditional_menus import LIBRARY,BOOKMARKS,mutate,library_case,bookmark_case
from verify_book_v2_reconciliation import ROOT,DEMO,dependencies,sha

CASES=['rename','delete-only','archive-only','publish-draft','replace-selected','progress','keep-selected']

def run(p,name):
    books=samples()
    if name=='keep-selected':books[1]['status']='published'
    seed(p,books=books);go(p,1);ready(p)
    if name=='keep-selected':
        p.locator('.v2-shelf-step button').last.click();expect(p.locator('.continue-book')).to_have_text('未完成的旅行')
    p.locator('.v2-shelf-more').click();dialog=p.locator('dialog[open]');expect(dialog.get_by_role('heading',name='全部回忆册',exact=True)).to_be_visible()
    peer=p.context.new_page();peer.goto('http://127.0.0.1:8765/prototype/review.html')
    peer.evaluate('''name=>{let b=JSON.parse(localStorage.getItem('dujia-prototype-books'));let first=b[0];
      if(name==='rename')first.name='更新后的共同夏天';
      if(name==='delete-only')b=b.filter(v=>v.id!==first.id);
      if(name==='archive-only'||name==='open-archive-after-last')first.archived=true;
      if(name==='publish-draft')b[1].status='published';
      if(name==='replace-selected'){b[1].status='published';b=b.filter(v=>v.id!==first.id);}
      if(name==='progress'){const page=structuredClone(first.pages[3]);page.id='peer-page-five';first.pages.push(page);first.lastPage='v0-p3';}
      if(name==='keep-selected'){b[2].archived=false;b[2].status='published';}
      localStorage.setItem('dujia-prototype-books',JSON.stringify(b));}''',name)
    expect(p.locator('.prototype-toast')).to_contain_text('共同数据已更新');before=store(p)
    if name=='open-archive-after-last':
        dialog.get_by_role('button',name='归档',exact=True).click();dialog.get_by_role('button',name='我们的夏天 · 归档',exact=True).click();p.wait_for_url('**/m08-p21.html*');ready(p)
        assert parse_qs(urlparse(p.url).query)['id']==['volume-0'];expect(p.locator('.archive')).to_have_text('取消归档回忆册');assert store(p)==before;peer.close();return
    # Closing must reveal the current shelf, not its stale pre-dialog snapshot.
    dialog.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
    if name in ['delete-only','archive-only']:
        p.wait_for_url('**/m08-p02.html*');ready(p);expect(p.get_by_role('button',name='新建第一本回忆册',exact=True)).to_be_visible();assert store(p)==before
        p.get_by_role('button',name='新建第一本回忆册',exact=True).click();p.wait_for_url('**/m08-p04.html*');ready(p);expect(p.locator('.book-name')).to_have_value('');assert store(p)==before;peer.close();return
    expect(p.locator('.v2-shelf-more')).to_be_focused()
    title='更新后的共同夏天' if name=='rename' else '未完成的旅行' if name in ['replace-selected','keep-selected'] else '我们的夏天'
    count=2 if name=='publish-draft' else 3 if name=='keep-selected' else 1
    expect(p.locator('.continue-book')).to_have_text(title);expect(p.locator('.v2-shelf-card')).to_have_count(count)
    expect(p.get_by_role('button',name='从封面打开《'+title+'》',exact=True)).to_be_visible();assert store(p)==before
    if name=='progress':expect(p.locator('.v2-shelf-meta .v2-shelf-count')).to_have_text('5 页 · 1 个章节');expect(p.locator('.continue-page')).to_have_text('上次读到第 4 页')
    selected='volume-1' if name in ['replace-selected','keep-selected'] else 'volume-0'
    assert p.evaluate('sessionStorage.getItem("dujia-book-shelf-selection")')==selected
    p.locator('.continue-link').click();p.wait_for_url('**/m08-p16.html*');ready(p)
    query=parse_qs(urlparse(p.url).query);assert query['id']==[selected]
    assert query['page']==['v0-p3' if name=='progress' else 'v1-p1' if selected=='volume-1' else 'v0-p1']
    peer.close()

def menu_case(p,name):
    if name!='archive-published':return library_case(p,name)
    library(p);dialog=p.locator('dialog[open]');dialog.locator('.v2-all-books button').first.focus();peer=mutate(p,name)
    expect(p.locator('.prototype-toast')).to_contain_text('共同数据已更新');before=store(p)
    expect(dialog.locator('.v2-all-books button')).to_have_count(0);expect(dialog.get_by_role('button',name='已成册',exact=True)).to_be_focused()
    dialog.get_by_role('button',name='取消',exact=True).click();p.wait_for_url('**/m08-p02.html*');ready(p)
    expect(p.get_by_role('button',name='新建第一本回忆册',exact=True)).to_be_visible();assert store(p)==before;peer.close()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args()
    out=ROOT/f'evidence/{args.stage}/book-shelf-return';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists();deps=dependencies()
    cases=[('return',n,w) for w in ([390] if args.stage=='baseline' else [320,390,430]) for n in CASES]
    if args.stage=='current':
        cases += [('return','open-archive-after-last',w) for w in [320,390,430]]
        cases += [(kind,n,w) for w in [320,390,430] for kind,names in [('library',LIBRARY),('bookmark',BOOKMARKS)] for n in names]
        cases += [('regression',n,390) for n in ['library-tabs','library-open-published','library-open-draft','library-open-archive','library-empty-draft-archive','library-cancel']]
    rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=browser.version
        for kind,name,w in cases:
            context=browser.new_context(viewport={'width':w,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=context.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row={'kind':kind,'case':name,'width':w,'passed':False}
            try:
                {'return':run,'library':menu_case,'bookmark':bookmark_case,'regression':previous_run}[kind](p,name);assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            if kind=='return' or not row['passed']:p.screenshot(path=str(out/f'{kind}-{name}-{w}.png'),full_page=True)
            row.update(errors=errors,effective=p.url);rows.append(row);context.close();assert dependencies()==deps;print(('PASS' if row['passed'] else 'FAIL'),kind,name,w,flush=True)
        browser.close()
    fixtures=['book_test_helpers.py','verify_book_v2.py','verify_book_controls.py','verify_book_v2_hidden_reading.py','verify_book_conditional_menus.py']
    value={'dependencies':deps,'producer_sha256':sha(Path(__file__)),'fixture_sha256':{n:sha(ROOT/n) for n in fixtures},'browser':version,'results':rows}
    (out/'results.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(out/'producer.py').write_bytes(Path(__file__).read_bytes())
    for n in deps:
        dest=out/'source'/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((DEMO/n).read_bytes())
    for n in fixtures:
        dest=out/'fixtures'/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((ROOT/n).read_bytes())
    print(sum(r['passed'] for r in rows),'/',len(rows));return 0 if all(r['passed'] for r in rows) else 1

if __name__=='__main__':raise SystemExit(main())
