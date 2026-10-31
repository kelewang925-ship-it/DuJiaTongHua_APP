"""Conditional reader bookmarks and actual cross-tab library changes."""
import argparse,json,traceback
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,go
from verify_book_v2_hidden_reading import fixture,library,ready,store,run as previous_run
from verify_book_v2_reconciliation import ROOT,DEMO,dependencies,sha

LIBRARY=['rename-published','rename-draft','archive-published','delete-draft','add-draft','publish-draft','unrelated-category','closed-listener']
BOOKMARKS=['choose','cancel','escape','empty']

def mutate(p,kind):
    other=p.context.new_page();other.goto('http://127.0.0.1:8765/prototype/review.html')
    other.evaluate('''kind=>{let books=JSON.parse(localStorage.getItem('dujia-prototype-books'));const first=books[0],draft=books[1];
      if(kind==='rename-published')first.name='另一半改好的夏天';
      if(kind==='rename-draft')draft.name='共同旅行的新名字';
      if(kind==='archive-published')first.archived=true;
      if(kind==='delete-draft')books=books.filter(v=>v.id!==draft.id);
      if(kind==='add-draft'){const extra=structuredClone(draft);extra.id='new-peer-draft';extra.name='另一半新增的草稿';books.push(extra);}
      if(kind==='publish-draft')draft.status='published';
      if(kind==='unrelated-category')books[2].name='另一半改好的归档';
      if(kind==='closed-listener')first.name='关闭后更新的夏天';
      localStorage.setItem('dujia-prototype-books',JSON.stringify(books));}''',kind)
    return other

def library_case(p,name):
    library(p);dialog=p.locator('dialog[open]');tab='草稿' if name in ['rename-draft','delete-draft','add-draft','publish-draft'] else '已成册';dialog.get_by_role('button',name=tab,exact=True).click();before_page=p.url
    if name=='closed-listener':
        dialog.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.v2-shelf-more')).to_be_focused()
        with p.expect_navigation(wait_until='load'):other=mutate(p,name)
        ready(p);expect(p.locator('.continue-book')).to_have_text('关闭后更新的夏天');expect(p.locator('dialog')).to_have_count(0);other.close();return
    dialog.locator('.v2-all-books button').first.focus();other=mutate(p,name);expect(p.locator('.prototype-toast')).to_contain_text('共同数据已更新');before=store(p)
    expect(dialog.get_by_role('button',name=tab,exact=True)).to_have_attribute('aria-pressed','true');assert p.url==before_page
    if name in ['delete-draft','publish-draft','archive-published']:
        expect(dialog.locator('.v2-all-books button')).to_have_count(0);expect(dialog.get_by_role('button',name=tab,exact=True)).to_be_focused()
    elif name in ['rename-published','rename-draft']:
        title='另一半改好的夏天' if name=='rename-published' else '共同旅行的新名字';button=dialog.get_by_role('button',name=title+' · '+tab,exact=True);expect(button).to_be_visible();expect(button).to_be_focused();button.click();p.wait_for_url('**/m08-p'+('15' if name=='rename-published' else '04')+'.html*');ready(p);assert parse_qs(urlparse(p.url).query)['id']==['volume-0' if name=='rename-published' else 'volume-1'];assert store(p)==before;other.close();return
    elif name=='add-draft':expect(dialog.get_by_role('button',name='另一半新增的草稿 · 草稿',exact=True)).to_be_visible();expect(dialog.locator('.v2-all-books button')).to_have_count(2)
    else:expect(dialog.locator('.v2-all-books button')).to_have_count(1);expect(dialog.get_by_role('button',name='我们的夏天 · 已成册',exact=True)).to_be_visible()
    assert store(p)==before;dialog.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.v2-shelf-more')).to_be_focused();other.close()

def bookmark_case(p,name):
    book=fixture['books']()[0];book['bookmarks']=[] if name=='empty' else ['v0-p2','v0-p3'];seed(p,books=[book]);go(p,17,'?id=volume-0&page=v0-p1');ready(p);before=store(p);trigger=p.locator('.tools button').nth(1);trigger.click();dialog=p.locator('dialog[open]');expect(dialog.get_by_role('heading',name='我的书签',exact=True)).to_be_visible()
    if name=='choose':
        expect(dialog.get_by_role('button',name='夏日片段 3',exact=True)).to_be_visible();expect(dialog.get_by_role('button',name='夏日片段 4',exact=True)).to_be_visible();dialog.get_by_role('button',name='夏日片段 4',exact=True).click();p.wait_for_url('**/m08-p16.html*');ready(p);assert parse_qs(urlparse(p.url).query)['page']==['v0-p3'];expect(p.locator('.page-count')).to_contain_text('4 / 4');actual=p.evaluate('PrototypeBooks.find("volume-0")');assert actual['lastPage']=='v0-p3' and actual['bookmarks']==['v0-p2','v0-p3'];return
    if name=='empty':expect(dialog).to_contain_text('还没有书签');expect(dialog.get_by_role('button')).to_have_count(1)
    if name=='escape':p.keyboard.press('Escape')
    else:dialog.get_by_role('button',name='取消',exact=True).click()
    expect(p.locator('dialog')).to_have_count(0);expect(trigger).to_be_focused();assert store(p)==before

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['baseline','current'],required=True);args=ap.parse_args();out=ROOT/f'evidence/{args.stage}/book-conditional-menus';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists();deps=dependencies();cases=[(kind,name,390) for kind,names in [('library',LIBRARY),('bookmark',BOOKMARKS)] for name in names]
    if args.stage=='current':cases=[(kind,name,w) for w in [320,390,430] for kind,names in [('library',LIBRARY),('bookmark',BOOKMARKS)] for name in names]+[('regression',name,390) for name in ['library-tabs','library-open-published','library-open-draft','library-open-archive','library-empty-draft-archive','library-cancel']]
    rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,name,w in cases:
            c=b.new_context(viewport={'width':w,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row={'kind':kind,'case':name,'width':w,'passed':False}
            try:
                (library_case if kind=='library' else bookmark_case if kind=='bookmark' else previous_run)(p,name);assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc();p.screenshot(path=str(out/(kind+'-'+name+'-'+str(w)+'.png')),full_page=True)
            row['errors']=errors;row['effective']=p.url;rows.append(row);c.close();assert dependencies()==deps;print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+name+' '+str(w),flush=True)
        b.close()
    report={'dependencies':deps,'producer_sha256':sha(Path(__file__)),'fixture_sha256':{n:sha(ROOT/n) for n in ['book_test_helpers.py','verify_book_v2.py','verify_book_controls.py','verify_book_v2_hidden_reading.py']},'browser':version,'results':rows};(out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':
        (out/'producer.py').write_bytes(Path(__file__).read_bytes());(out/'prototype-book-v2.js').write_bytes((DEMO/'assets/prototype-book-v2.js').read_bytes())
    print(sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
