"""Memory-book V2 browser contracts; isolated context, never alters a user's library."""
from pathlib import Path
import json, sys, traceback
from playwright.sync_api import sync_playwright, expect
from book_test_helpers import seed, go, fixture, records, value

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'evidence' / ('baseline' if '--baseline' in sys.argv else 'current') / 'book-v2'
OUT.mkdir(parents=True, exist_ok=True)

def books():
    result = []
    for i, name in enumerate(['我们的夏天', '第一次旅行', '小小日常']):
        b = fixture('volume-' + str(i))
        b.update(name=name, theme=['花园午后', '旅行手札', '暖灯日常'][i])
        b['pages'] = [dict(id=f'v{i}-p{n}', chapterId='chapter-state', template='日记摘录', title=f'夏日片段 {n+1}', body='傍晚的风很温柔，和你一起看晚霞。\n每个普通的日子，都值得好好收藏。', date='2026-10-04') for n in range(4)]
        b['lastPage'] = b['pages'][1]['id']
        result.append(b)
    return result

def ready(p):
    p.wait_for_function("document.querySelector('.screen')?.getAttribute('aria-busy')==='false'")
    p.evaluate('document.fonts.ready')

def shelf(p):
    seed(p, books=books()); go(p, 1); ready(p)
    rail=p.locator('.v2-shelf-rail'); expect(rail).to_be_visible()
    assert rail.evaluate('(e)=>e.scrollWidth>e.clientWidth')
    rail.evaluate('(e)=>e.scrollTo({left:e.scrollWidth,behavior:"instant"})')
    expect(p.locator('.continue-book')).to_have_text('小小日常')
    p.locator('.continue-link').click(); p.wait_for_url('**/m08-p16.html*id=volume-2*'); ready(p)
    assert 'v2-p1' in p.url

def reader(p):
    seed(p, books=books()); go(p,16,'?id=volume-0&page=v0-p0');ready(p)
    expect(p.locator('.v2-reader')).to_be_visible()
    p.evaluate('window.__readerDocument=12345')
    p.locator('.next-page').click()
    expect(p.locator('.page-count')).to_contain_text('2 / 4')
    assert p.evaluate('window.__readerDocument')==12345
    assert value(p)[0]['lastPage']=='v0-p1'
    p.locator('.bookmark').click()
    expect(p.locator('.bookmark')).to_have_attribute('aria-pressed','true')
    p.reload(); ready(p)
    expect(p.locator('.page-count')).to_contain_text('2 / 4')

def long_content(p):
    b=books()[0];b['pages'][0]['body']='长段落仍然需要清晰地读完。'*180
    seed(p,books=[b]);go(p,16,'?id=volume-0&page=v0-p0');ready(p)
    expect(p.locator('.v2-reader')).to_be_visible()
    assert p.locator('.v2-paper').first.evaluate('(e)=>parseFloat(getComputedStyle(e.querySelector(".copy")).fontSize)>=16')
    assert p.locator('.v2-continuation').is_visible()
    before=p.locator('.page-count').inner_text()
    p.locator('.next-page').click()
    expect(p.locator('.v2-continuation')).to_contain_text('2 /')
    assert p.locator('.page-count').inner_text()==before
    p.locator('.v2-reader-more').click();p.get_by_role('button',name='大字连续阅读',exact=True).click()
    expect(p.locator('.v2-reader')).to_have_class(__import__('re').compile('v2-continuous'))
    assert '长段落仍然需要清晰地读完。'*180 in p.locator('.v2-continuous-content').inner_text()

def cancel_drag(p):
    seed(p,books=books());go(p,16,'?id=volume-0&page=v0-p0');ready(p)
    box=p.locator('.v2-book-stage').bounding_box();x=box['x']+box['width']*.65;y=box['y']+box['height']*.5
    p.mouse.move(x,y);p.mouse.down();p.mouse.move(x-25,y,steps=4);p.mouse.up()
    p.wait_for_timeout(350)
    assert value(p)[0]['lastPage']=='v0-p0'
    expect(p.locator('.page-count')).to_contain_text('1 / 4')

def directory(p):
    seed(p,books=books());go(p,16,'?id=volume-0&page=v0-p0');ready(p)
    p.locator('.toc').click();expect(p.locator('dialog[open]')).to_be_visible()
    p.get_by_role('button',name='夏日片段 4',exact=False).click()
    expect(p.locator('.page-count')).to_contain_text('4 / 4')
    assert value(p)[0]['lastPage']=='v0-p3'

def privacy(p):
    b=fixture();seed(p,books=[b],records=records());go(p,16,'?id=book-state&page=page-state');ready(p)
    expect(p.locator('.v2-reader')).to_contain_text('SOURCE-SECRET')
    p.evaluate("()=>{const r=JSON.parse(localStorage.getItem('dujia-prototype-records'));r[0].visibility='private';localStorage.setItem('dujia-prototype-records',JSON.stringify(r));window.dispatchEvent(new StorageEvent('storage',{key:'dujia-prototype-records'}));}")
    expect(p.locator('.v2-reader')).not_to_contain_text('SOURCE-SECRET')
    expect(p.locator('.v2-reader')).to_contain_text('关联内容')

def organizer(p):
    seed(p,books=books());go(p,13,'?id=volume-0');ready(p)
    expect(p.locator('.v2-page-grid')).to_be_visible()
    assert p.locator('.book-page-row').count()==4
    p.get_by_role('button',name='页面操作「夏日片段 1」',exact=True).click()
    p.get_by_role('button',name='下移一页',exact=True).click()
    expect(p.locator('.book-page-row').first).to_contain_text('夏日片段 2')
    assert value(p)[0]['pages'][0]['id']=='v0-p0'
    p.locator('.save').click();p.wait_for_url('**/m08-p14.html*')
    assert value(p)[0]['pages'][0]['id']=='v0-p1'

def cover_privacy(p):
    b=fixture();b['coverPhoto']={'kind':'photo','id':'photo-private'}
    rs=records()+[dict(id='photo-private',type='photo',title='共同封面',body='',date='2026-10-04',visibility='shared',status='published',image='../assets/book-v2/garden.webp',author='小满')]
    seed(p,books=[b],records=rs);go(p,5,'?id=book-state');ready(p)
    expect(p.locator('.book-cover-preview img')).to_have_count(1)
    peer=p.context.new_page();peer.goto(p.url);peer.wait_for_timeout(500)
    peer.evaluate("()=>{const rs=JSON.parse(localStorage.getItem('dujia-prototype-records'));rs.find(r=>r.id==='photo-private').visibility='private';localStorage.setItem('dujia-prototype-records',JSON.stringify(rs));}")
    expect(p.locator('.book-cover-preview img')).to_have_count(0)
    peer.close()

def mode_anchor(p):
    b=books()[0];b['pages'][0]['body']='长段落仍然需要清晰地读完。'*150
    seed(p,books=[b]);go(p,16,'?id=volume-0&page=v0-p0');ready(p)
    p.locator('.next-page').click();expect(p.locator('.v2-continuation')).to_contain_text('2 /')
    saved=value(p)[0]['lastAnchor'];assert saved['offset']>0
    p.locator('.v2-reader-more').click();p.get_by_role('button',name='大字连续阅读',exact=True).click()
    p.wait_for_timeout(500)
    p.locator('.v2-reader-more').click();p.get_by_role('button',name='实体翻书阅读',exact=True).click()
    p.wait_for_timeout(250)
    assert value(p)[0]['lastAnchor']==saved,(saved,value(p)[0]['lastAnchor'])
    expect(p.locator('.v2-continuation')).to_contain_text('2 /')

def message_continuation(p):
    b=books()[0];b['pages'][0].update(title='很长的标题'*20,body='',message='想把这一刻好好记住'*10)
    seed(p,books=[b]);p.set_viewport_size({'width':320,'height':568});go(p,16,'?id=volume-0&page=v0-p0');ready(p)
    assert p.locator('.v2-reader-sheets .v2-paper-content').first.evaluate('(e)=>e.scrollHeight<=e.clientHeight+2')
    text=p.locator('.v2-reader-sheets .v2-page-message').inner_text()
    while p.locator('.v2-continuation').is_visible():
        label=p.locator('.v2-continuation').inner_text();part,total=map(int,label.replace('本页 ','').split(' / '))
        if part==total:break
        p.locator('.next-page').click();expect(p.locator('.v2-continuation')).not_to_have_text(label)
        text+=p.locator('.v2-reader-sheets .v2-page-message').inner_text()
    assert text==b['pages'][0]['message']

def edit_returns_to_reader(p):
    seed(p,books=books());go(p,16,'?id=volume-0&page=v0-p2');ready(p)
    p.locator('.v2-reader-more').click();p.get_by_role('button',name='整理书页',exact=True).click();p.wait_for_url('**/m08-p13.html*');ready(p)
    p.locator('.save').click();p.wait_for_url('**/m08-p16.html*');ready(p)
    expect(p.locator('.page-count')).to_contain_text('3 / 4');assert value(p)[0]['lastPage']=='v0-p2'

CASES={'shelf-scroll-select-continue':shelf,'reader-same-document-bookmark-reload':reader,'long-content-continuation-large-type':long_content,'short-drag-cancels':cancel_drag,'directory-jump':directory,'privacy-clears-visible-content':privacy,'organizer-transaction':organizer,'cover-privacy-across-windows':cover_privacy,'mode-switch-preserves-anchor':mode_anchor,'long-message-continuation':message_continuation,'organizer-returns-to-reading-position':edit_returns_to_reader}
def main():
    cases=CASES
    if '--case' in sys.argv:
        name=sys.argv[sys.argv.index('--case')+1];cases={name:CASES[name]}
    rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for name, run in cases.items():
            context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
            p=context.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:
                run(p);assert not errors,errors
                p.screenshot(path=str(OUT/(name+'.png')),full_page=True)
                row={'case':name,'passed':True}
            except Exception:
                row={'case':name,'passed':False,'failure':traceback.format_exc()[-2000:]}
            row['errors']=errors;rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);context.close()
        browser.close()
    (OUT/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return 0 if all(r['passed'] for r in rows) else 1

if __name__=='__main__':raise SystemExit(main())
