"""Execute library, reader-menu, directory, zoom and supplement hidden behavior."""
import json,re,traceback
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,go,value
from audit_hidden_overlays import declarations
from verify_book_v2_reconciliation import ROOT,dependencies,sha

fixture=declarations('verify_book_v2.py')
legacy=declarations('verify_book_controls.py')
def ready(p):
    expect(p.locator('.screen')).to_have_attribute('aria-busy','false');p.evaluate('document.fonts.ready')
def store(p):return p.evaluate('({...localStorage})')
def samples():
    books=fixture['books']();books[1].update(name='未完成的旅行',status='draft');books[2].update(name='收好的日常',archived=True)
    return books
def library(p):
    seed(p,books=samples());go(p,1);ready(p);p.locator('.v2-shelf-more').click();expect(p.locator('dialog h2')).to_have_text('全部回忆册')
def reader(p,bookmark=False,supplement=False):
    book=fixture['books']()[0];book['chapters'].append(dict(id='chapter-two',name='第二章'));book['pages'][2]['chapterId']='chapter-two';book['pages'][3]['chapterId']='chapter-two'
    if bookmark:book['bookmarks']=['v0-p2']
    if supplement:book['pages'][1]['supplements']=[dict(id='reply-1',text='这是一张真实补页',author='小满',date='2026-10-05',kind='写几句话')]
    seed(p,books=[book]);go(p,16,'?id=volume-0&page=v0-p1');ready(p)
    p.evaluate('window.__hiddenReadingDocument=2718')
def assert_read(p,before,wanted='v0-p1'):
    after=store(p);a=json.loads(before['dujia-prototype-books']);b=json.loads(after['dujia-prototype-books']);book=b[0]
    assert book['lastPage']==wanted and book['lastAnchor']==dict(pageId=wanted,offset=0,block=0),book.get('lastAnchor')
    for rows in [a,b]:
        for key in ['lastPage','lastAnchor','updatedAt']:rows[0].pop(key,None)
    left={**before,'dujia-prototype-books':a};right={**after,'dujia-prototype-books':b};assert left==right
def open_menu(p):p.locator('.v2-reader-more').click();expect(p.locator('dialog h2')).to_have_text('阅读设置与工具')
def open_directory(p):p.locator('.toc').click();expect(p.locator('dialog h2')).to_have_text('回忆册目录')

def run(p,name):
    if name.startswith('library-'):
        library(p);before=store(p);dialog=p.locator('dialog[open]')
        if name=='library-tabs':
            for label,title in [('已成册','我们的夏天'),('草稿','未完成的旅行'),('归档','收好的日常')]:
                button=dialog.get_by_role('button',name=label,exact=True);button.click();expect(button).to_have_attribute('aria-pressed','true');expect(dialog.locator('.v2-all-books button')).to_have_count(1);expect(dialog.get_by_role('button',name=title+' · '+label,exact=True)).to_be_visible()
        elif name=='library-empty-draft-archive':
            p.evaluate('()=>{const b=JSON.parse(localStorage.getItem("dujia-prototype-books"));localStorage.setItem("dujia-prototype-books",JSON.stringify(b.slice(0,1)))}');before=store(p)
            for label,message in [('草稿','还没有未完成的回忆册'),('归档','还没有归档的回忆册')]:
                dialog.get_by_role('button',name=label,exact=True).click();expect(dialog.locator('.v2-all-books')).to_have_text(message);expect(dialog.locator('.v2-all-books button')).to_have_count(0)
        elif name=='library-cancel':
            dialog.get_by_role('button',name='草稿',exact=True).click();dialog.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.v2-shelf-more')).to_be_focused()
        else:
            label,title,id,target={'library-open-published':('已成册','我们的夏天','volume-0',15),'library-open-draft':('草稿','未完成的旅行','volume-1',4),'library-open-archive':('归档','收好的日常','volume-2',21)}[name]
            dialog.get_by_role('button',name=label,exact=True).click();dialog.get_by_role('button',name=title+' · '+label,exact=True).click();p.wait_for_url('**/m08-p'+str(target).zfill(2)+'.html*');ready(p);assert parse_qs(urlparse(p.url).query)['id']==[id]
            if target==4:expect(p.locator('.book-name')).to_have_value(title)
            if target==21:expect(p.locator('.archive')).to_have_text('取消归档回忆册')
        assert store(p)==before;return
    if name=='zoom-privacy-refresh':
        legacy['seed'](p,'m08-p16');p.get_by_role('button',name='放大照片',exact=True).click();expect(p.locator('dialog .v2-full-image')).to_be_visible()
        peer=p.context.new_page();peer.goto('http://127.0.0.1:8765/prototype/review.html');peer.evaluate('()=>{const rs=JSON.parse(localStorage.getItem("dujia-prototype-records"));rs.find(r=>r.id==="audit-photo").visibility="private";localStorage.setItem("dujia-prototype-records",JSON.stringify(rs))}')
        expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.v2-reader')).to_contain_text('关联内容');expect(p.locator('.v2-reader-photo img')).to_have_count(0);peer.close();return
    if name=='zoom-controls-return':
        legacy['seed'](p,'m08-p16');before=store(p);p.evaluate('window.__hiddenReadingDocument=2718');p.get_by_role('button',name='放大照片',exact=True).click();slider=p.get_by_role('slider',name='照片缩放',exact=True);slider.focus();slider.press('End');expect(slider).to_have_value('3');expect(p.locator('dialog .v2-full-image')).to_have_css('width',re.compile(r'.+px'))
        assert p.locator('dialog .v2-full-image').evaluate('e=>e.style.width')=='300%';slider.press('Home');expect(slider).to_have_value('1');assert p.locator('dialog .v2-full-image').evaluate('e=>e.style.width')=='100%'
        p.get_by_role('button',name='返回阅读',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert p.evaluate('window.__hiddenReadingDocument')==2718;assert store(p)==before;return
    reader(p,bookmark=name=='directory-bookmarked-page',supplement=name=='supplements-populated');before=store(p)
    if name.startswith('menu-'):
        open_menu(p)
        if name=='menu-mode-roundtrip':
            p.get_by_role('button',name='大字连续阅读',exact=True).click();expect(p.locator('.screen')).to_have_class(re.compile('v2-continuous'));expect(p.locator('.v2-continuous-page')).to_have_count(4)
            open_menu(p);p.get_by_role('button',name='实体翻书阅读',exact=True).click();expect(p.locator('.screen')).not_to_have_class(re.compile('v2-continuous'))
        elif name=='menu-type-roundtrip':
            initial=p.locator('.v2-reader-sheets .copy').first.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)');p.get_by_role('button',name='放大字号',exact=True).click();expect(p.locator('.screen')).to_have_class(re.compile('v2-large-type'));assert p.locator('.v2-reader-sheets .copy').first.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')>initial
            open_menu(p);p.get_by_role('button',name='标准字号',exact=True).click();expect(p.locator('.screen')).not_to_have_class(re.compile('v2-large-type'))
        elif name=='menu-cancel':
            p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.v2-reader-more')).to_be_focused()
        else:
            label,target={'menu-organize':('整理书页',13),'menu-cover':('封面与主题',5),'menu-manage':('管理这本回忆册',21),'menu-shelf':('返回书架',1)}[name]
            p.get_by_role('button',name=label,exact=True).click();p.wait_for_url('**/m08-p'+str(target).zfill(2)+'.html*');ready(p)
            if target!=1:
                query=parse_qs(urlparse(p.url).query);assert query['id']==['volume-0'] and query['returnPage']==['v0-p1'] and query['returnOffset']==['0'] and query['returnBlock']==['0'],query
            assert_read(p,before);return
        assert p.evaluate('window.__hiddenReadingDocument')==2718;assert_read(p,before);return
    if name.startswith('directory-'):
        open_directory(p);dialog=p.locator('dialog[open]')
        if name=='directory-empty-bookmarks':
            dialog.get_by_role('button',name='书签',exact=True).click();expect(dialog.locator('.v2-sheet-list')).to_have_text('还没有书签，可在阅读页点击书签。');assert_read(p,before);return
        if name=='directory-cancel':
            dialog.get_by_role('button',name='缩略图',exact=True).click();dialog.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.toc')).to_be_focused();assert_read(p,before);return
        tab={'directory-chapter-page':'章节','directory-thumbnail-page':'缩略图','directory-bookmarked-page':'书签'}[name]
        button=dialog.get_by_role('button',name=tab,exact=True);button.click();expect(button).to_have_attribute('aria-pressed','true')
        target=2 if name=='directory-bookmarked-page' else 3;dialog.get_by_role('button',name='夏日片段 '+str(target+1),exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.page-count')).to_contain_text(str(target+1)+' / 4');assert_read(p,before,'v0-p'+str(target));assert p.evaluate('window.__hiddenReadingDocument')==2718;return
    if name.startswith('supplements-'):
        go(p,20,'?id=volume-0&page=v0-p1');ready(p);expect(p.locator('dialog h2')).to_have_text('我们的补页')
        expect(p.locator('dialog')).to_contain_text('这是一张真实补页' if name=='supplements-populated' else '还没有补页。')
        if name=='supplements-populated':expect(p.locator('dialog')).to_contain_text('小满 · 2026-10-05')
        p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert_read(p,before);return
    raise AssertionError(name)

CASES=['library-tabs','library-open-published','library-open-draft','library-open-archive','library-empty-draft-archive','library-cancel','menu-mode-roundtrip','menu-type-roundtrip','menu-organize','menu-cover','menu-manage','menu-shelf','menu-cancel','directory-chapter-page','directory-thumbnail-page','directory-bookmarked-page','directory-empty-bookmarks','directory-cancel','zoom-controls-return','zoom-privacy-refresh','supplements-empty','supplements-populated']
def main():
    out=ROOT/'evidence/current/book-v2-hidden-reading';out.mkdir(parents=True,exist_ok=True);files=dependencies();rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for name in CASES:
            c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(case=name,passed=False)
            try:run(p,name);assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc();p.screenshot(path=str(out/(name+'.png')),full_page=True)
            row.update(errors=errors,effective=p.url);rows.append(row);c.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True)
        b.close()
    data=dict(dependency_files=files,producer_sha256=sha(Path(__file__)),helpers_sha256=sha(ROOT/'book_test_helpers.py'),fixtures_sha256={f:sha(ROOT/f) for f in ['verify_book_controls.py','verify_book_v2.py']},browser=version,viewport=[390,844],locale='zh-CN',timezone='Asia/Shanghai',scope='22 named current hidden library/reader business outcomes only; organizer and editor hidden actions remain separate.',results=rows)
    (out/'results.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Hidden reading outcomes:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
