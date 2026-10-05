"""User-visible book contract; --baseline retains failures before implementation."""
from pathlib import Path
import json, sys, traceback
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parent
OUT=ROOT/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current')
BASE='http://127.0.0.1:8765/'

def seed(p,books=None,records=None):
    p.goto(BASE+'prototype/review.html')
    p.evaluate('''data=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem('dujia-prototype-today','2026-10-05');localStorage.setItem('dujia-prototype-books',JSON.stringify(data.books));localStorage.setItem('dujia-prototype-records',JSON.stringify(data.records));localStorage.setItem('dujia-profile',JSON.stringify({nickname:'小满'}));localStorage.setItem('dujia-prototype-relationship',JSON.stringify({bound:true,partner:'阿舟'}));}''',{'books':books or [],'records':records or []})

def go(p,n,query=''):p.goto(BASE+f'pages/m08-p{n:02}.html'+query)

def empty(p):
    seed(p);go(p,1);p.wait_for_url('**/m08-p02.html')
    expect(p.get_by_role('button',name='新建第一本回忆册',exact=True)).to_be_visible()
    p.get_by_role('button',name='新建第一本回忆册',exact=True).click();p.wait_for_url('**/m08-p04.html*')

def blank(p):
    seed(p);go(p,4)
    p.get_by_label('书名',exact=True).fill('独立测试册')
    p.get_by_label('开始月份',exact=True).fill('2026.10');p.get_by_label('结束月份',exact=True).fill('2026.10')
    p.get_by_role('button',name='空白回忆册',exact=True).click();p.locator('.next').click();p.wait_for_url('**/m08-p05.html*')
    p.locator('.next').click();p.wait_for_url('**/m08-p13.html*')
    p.locator('.save').click();p.wait_for_url('**/m08-p14.html*')
    expect(p.locator('#bookName')).to_have_text('独立测试册')
    p.locator('.read').click();p.wait_for_url('**/m08-p15.html*')
    p.locator('.back').click();p.wait_for_url('**/m08-p01.html*')
    expect(p.locator('.books button').filter(has_text='独立测试册')).to_be_visible()
    p.reload();expect(p.locator('.books button').filter(has_text='独立测试册')).to_be_visible()

def materials(p):
    records=[dict(id='book-source',type='diary',title='可放进书里的日记',body='共同走过的那条小路',visibility='shared',status='published',date='2026-10-04',author='小满')]
    seed(p,records=records);go(p,4)
    p.get_by_label('书名',exact=True).fill('真实素材册')
    p.get_by_label('开始月份',exact=True).fill('2026.10');p.get_by_label('结束月份',exact=True).fill('2026.10')
    p.locator('.next').click();p.wait_for_url('**/m08-p05.html*');p.locator('.next').click();p.wait_for_url('**/m08-p06.html*')
    source=p.get_by_role('button',name='可放进书里的日记',exact=False);expect(source).to_be_visible();source.click()
    p.locator('.next').click();p.wait_for_url('**/m08-p07.html*')
    expect(p.locator('.screen')).to_contain_text('共同走过的那条小路')
    p.locator('.add').click();p.wait_for_url('**/m08-p08.html*');p.locator('.use').click();p.wait_for_url('**/m08-p09.html*')
    expect(p.locator('#excerpt')).to_have_value('共同走过的那条小路')
    p.locator('.done').click();p.wait_for_url('**/m08-p13.html*');p.locator('.save').click();p.wait_for_url('**/m08-p14.html*')
    books=p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-books'))")
    assert len(books)==1 and len(books[0]['pages'])==1

def delete(p):
    book=dict(id='delete-book',name='唯一的一本册',dates=['2026.10','2026.10'],start='blank',theme='花园午后',coverPhoto=False,status='published',chapters=[],pages=[],bookmarks=[],lastPage=None,archived=False,createdAt=1,updatedAt=1)
    seed(p,books=[book]);go(p,21,'?id=delete-book')
    expect(p.locator('.book-name')).to_have_text('唯一的一本册')
    p.get_by_role('button',name='删除这本回忆册',exact=True).click()
    p.get_by_role('button',name='确认删除',exact=True).click();p.wait_for_url('**/m08-p02.html*')
    assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-books'))")==[]
    go(p,1);p.wait_for_url('**/m08-p02.html*')

rows=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,run in {'first-use-empty-create-entry':empty,'blank-create-shelf-reload':blank,'real-source-compose-publish':materials,'delete-no-sample-reseed':delete}.items():
        c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4000);p.set_default_navigation_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p);assert not errors,errors;row={'case':name,'passed':True}
        except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-1800:]}
        row.update(errors=errors,final_url=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
    b.close()
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'book-flow-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
