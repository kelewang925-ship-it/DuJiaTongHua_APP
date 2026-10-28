"""V2-specific integration/animation contracts replacing obsolete scroll-reader selectors."""
from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,go,value,fail,fixture,records
from verify_book_v2 import books,ready

OUT=Path(__file__).resolve().parent/'evidence/current/book-v2';OUT.mkdir(exist_ok=True)

def supplements(p):
    seed(p,books=[fixture()],records=records());go(p,16,'?id=book-state&page=page-state');ready(p)
    p.locator('.v2-add-supplement').click();p.wait_for_url('**/m08-p18.html*');p.locator('.next').click();p.wait_for_url('**/m08-p19.html*');ready(p)
    p.get_by_label('补页文字',exact=True).fill('这是我的真实补页');fail(p,'book-supplement');p.locator('.submit').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');assert not value(p)[0]['pages'][0].get('supplements')
    p.locator('.submit').click();p.wait_for_url('**/m08-p20.html*');expect(p.locator('.right-copy')).to_contain_text('这是我的真实补页')
    go(p,18,'?id=book-state&page=page-state');ready(p);p.locator('[data-kind=送一个表情]').click();p.locator('.next').click();p.wait_for_url('**/m08-p19.html*');ready(p);p.get_by_role('button',name='星星',exact=True).click();p.locator('.submit').click();p.wait_for_url('**/m08-p20.html*');expect(p.locator('.right-copy')).to_contain_text('⭐')
    go(p,18,'?id=book-state&page=page-state');ready(p);p.locator('[data-kind=附上一张照片]').click();p.locator('.next').click();p.wait_for_url('**/m08-p19.html*');ready(p)
    p.locator('input[type=file]').set_input_files(str(Path(__file__).resolve().parents[1]/'assets/book-v2/garden.webp'));expect(p.locator('.photo-label')).to_contain_text('已附上照片');p.locator('.submit').click();p.wait_for_url('**/m08-p20.html*');expect(p.locator('.book-supplement-images img')).to_have_count(1)
    assert len(value(p)[0]['pages'][0]['supplements'])==3
    p.screenshot(path=str(OUT/'supplements.png'),full_page=True)

def image_fragments(p):
    b=fixture();b['pages'][0].update(template='照片故事',source={'kind':'photo','id':'photo-v2'},body='照片旁边的文字也要完整读完。'*40,photos=[{'source':{'kind':'photo','id':'photo-v2'},'crop':{'x':40,'y':60,'zoom':1.5}} for _ in range(3)])
    rs=[dict(id='photo-v2',type='photo',title='一起看晚霞',body='',date='2026-10-04',visibility='shared',status='published',image='../assets/book-v2/garden.webp')]
    seed(p,books=[b],records=rs);go(p,16,'?id=book-state&page=page-state');ready(p)
    images=0;content='';parts=0
    while True:
        images+=p.locator('.v2-reader-sheets .v2-reader-photo img').count()
        for text in p.locator('.v2-reader-sheets .copy').all_inner_texts():content+=text
        assert p.locator('.v2-reader-sheets .v2-paper-content').first.evaluate('(e)=>e.scrollHeight<=e.clientHeight+2')
        parts+=1
        if p.locator('.next-page').is_disabled():break
        p.locator('.next-page').click();p.wait_for_timeout(40)
        assert parts<30
    assert images==3 and content==b['pages'][0]['body'],(images,len(content))

def animation(p):
    p.emulate_media(reduced_motion='no-preference');seed(p,books=books());go(p,16,'?id=volume-0&page=v0-p0');ready(p);p.wait_for_timeout(160)
    r=p.locator('.v2-book-stage').bounding_box();x=r['x']+r['width']*.8;y=r['y']+r['height']*.65
    p.mouse.move(x,y);p.mouse.down();p.mouse.move(x-135,y,steps=8)
    expect(p.locator('.v2-turn-slice')).to_have_count(12)
    metrics=p.locator('.v2-turn-slice').evaluate_all('''es=>es.map(e=>{const m=new DOMMatrix(getComputedStyle(e).transform);return {x:m.m41,z:m.m43,dx:m.m11*e.clientWidth,dz:m.m13*e.clientWidth}})''')
    assert any(abs(m['z'])>10 for m in metrics)
    assert all(abs(a['x']+a['dx']-b['x'])<2 and abs(a['z']+a['dz']-b['z'])<2 for a,b in zip(metrics,metrics[1:])),metrics
    p.screenshot(path=str(OUT/'actual-page-turn.png'),full_page=True)
    assert value(p)[0]['lastPage']=='v0-p0'
    p.mouse.up();expect(p.locator('.page-count')).to_contain_text('2 / 4');assert value(p)[0]['lastPage']=='v0-p1'

def landscape(p):
    b=books()[0]
    for page in b['pages']:page['body']='我们一起走过的普通日子。'
    seed(p,books=[b]);p.set_viewport_size({'width':844,'height':450});go(p,16,'?id=volume-0&page=v0-p0');ready(p)
    expect(p.locator('.v2-reader-sheets .v2-paper')).to_have_count(2);expect(p.locator('.page-count')).to_contain_text('1–2 / 4')
    p.locator('.next-page').click();expect(p.locator('.page-count')).to_contain_text('3–4 / 4');expect(p.locator('.next-page')).to_be_disabled()
    p.screenshot(path=str(OUT/'actual-landscape.png'),full_page=True)
    p.set_viewport_size({'width':390,'height':844});expect(p.locator('.v2-reader-sheets .v2-paper')).to_have_count(1);expect(p.locator('.page-count')).to_contain_text('3 / 4')

def touch_shelf(p):
    seed(p,books=books());go(p,1);ready(p)
    rail=p.locator('.v2-shelf-rail');r=rail.bounding_box();session=p.context.new_cdp_session(p);x=r['x']+r['width']*.8;y=r['y']+r['height']*.5
    session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
    for step in range(1,11):
        session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x-step*24,'y':y}]});p.wait_for_timeout(20)
    session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});expect(p.locator('.continue-book')).not_to_have_text('我们的夏天')
    assert rail.evaluate('e=>e.scrollLeft')>0
    p.screenshot(path=str(OUT/'actual-shelf.png'),full_page=True)

def touch_reader(p):
    p.add_init_script("window.touchTrace=[];for(const type of ['pointerdown','pointermove','pointerup','pointercancel','lostpointercapture'])document.addEventListener(type,e=>touchTrace.push({type,x:e.clientX,y:e.clientY,button:e.button,target:e.target.className,selection:String(getSelection()),turn:!!document.querySelector('.v2-turn-overlay')}),true)")
    seed(p,books=books());go(p,16,'?id=volume-0&page=v0-p0');ready(p)
    r=p.locator('.v2-book-stage').bounding_box();session=p.context.new_cdp_session(p);x=r['x']+r['width']*.8;y=r['y']+r['height']*.6
    session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
    for step in range(1,10):
        session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x-step*19,'y':y}]});p.wait_for_timeout(25)
    session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    (OUT/'touch-reader-trace.json').write_text(json.dumps(p.evaluate('touchTrace'),ensure_ascii=False,indent=2),encoding='utf-8')
    expect(p.locator('.page-count')).to_contain_text('2 / 4');assert value(p)[0]['lastPage']=='v0-p1'

def open_close(p):
    p.emulate_media(reduced_motion='no-preference');seed(p,books=books());go(p,16,'?id=volume-0&page=v0-p0&open=cover')
    expect(p.locator('.v2-cover-opening')).to_have_count(1);expect(p.locator('.v2-cover-opening')).to_have_count(0)
    p.locator('.back').click();expect(p.locator('.v2-cover-closing')).to_have_count(1);p.wait_for_url('**/m08-p01.html*');ready(p);expect(p.locator('.v2-shelf')).to_be_visible()

rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'three-supplements-retry-real-photo':supplements,'all-photos-and-long-body-through-continuations':image_fragments,'normal-curved-turn-geometry-and-commit':animation,'landscape-spread-end-and-portrait-anchor':landscape,'real-touch-carousel':touch_shelf,'real-touch-reader':touch_reader,'cover-open-close-animation':open_close}.items():
  c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',has_touch=True);p=c.new_page();p.set_default_timeout(7000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-2200:]};p.screenshot(path=str(OUT/('failure-'+name+'.png')),full_page=True)
  row['errors']=errors;rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
(OUT/'integration-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
