"""Execute every available initial control in six moment/reply page fixtures plus hidden branches."""
from pathlib import Path
import json,hashlib,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from audit_runtime import INIT,OBSERVE
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;BASE='http://127.0.0.1:8765/';OUT=ROOT/'evidence'/('baseline' if '--baseline' in sys.argv else 'current')
PAGES={'m04-p01':True,'m04-p02':False,'m04-p03':True,'m04-p04':False,'m04-p16':True,'m04-p17':False}
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
def seed(p,page):
    p.goto(BASE+'prototype/review.html');d=data(PAGES[page])
    if PAGES[page]:
        d['dujia-prototype-moments'][0]['related']=['audit-diary'];d['dujia-prototype-moments'][0]['comments']=[{'id':'reply-a','text':'一起收藏这个时刻','author':'阿舟','createdAt':1791158400000,'read':False}]
    p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d)
    p.goto(BASE+'pages/'+page+'.html'+('?id=audit-moment' if page=='m04-p03' else ''))
    if page=='m04-p01':expect(p.locator('.cards button')).to_have_count(1)
    p.evaluate('document.fonts.ready')
def store(p):return p.evaluate('JSON.stringify({...localStorage})')
def go(p,name):p.wait_for_url('**/'+name+'.html*')
def reply(p):p.locator('.message').click();p.get_by_label('回应这个时刻').fill('尚未发送的心意')
def dirty(p,exit):
    seed(p,'m04-p03');before=store(p);reply(p)
    def close():
        if exit=='cancel':p.get_by_role('button',name='取消',exact=True).click()
        elif exit=='escape':p.keyboard.press('Escape')
        elif exit=='back':p.go_back()
        else:
            handle=p.locator('.prototype-sheet-handle');box=handle.bounding_box();p.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);p.mouse.down();p.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2+110,steps=8);p.mouse.up()
    close();expect(p.get_by_text('是否放弃当前修改？',exact=True)).to_be_visible();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.get_by_label('回应这个时刻')).to_have_value('尚未发送的心意');assert store(p)==before
    close();p.get_by_role('button',name='放弃修改',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert store(p)==before;expect(p.locator('.message')).to_be_focused()

def contract(page,c):
    label=c['label']
    nav={'首页':'m03-p02' if PAGES[page] else 'm03-p01','重要时刻':'self','工坊':'m05-p01','宠物':'pet','我的':'m06-p01'}
    rules={'共同提醒':'route:m04-p05','返回重要时刻':'route:m04-p01' if PAGES[page] else 'route:m04-p02','查看纪念日':'route:m04-p07','珍藏一个新时刻':'route:m04-p04','查看全部 ›':'expand','共同重要时刻\n2026-10-04':'route:m04-p03','纪念日':'route:'+('m04-p07' if PAGES[page] else 'm04-p08'),'时光胶囊':'route:m04-p12','悄悄留言':'route:'+('m04-p16' if PAGES[page] else 'm04-p17'),'新建重要时刻':'route:m04-p04','刷新时刻册':'refresh','从共同记录中收录':'collect-empty','共同日记':'route:m03-p08','悄悄留言 1 条':'sheet:时刻回应','编辑时刻':'route:m04-p04','更多操作':'sheet:时刻操作','添加封面':'file','发生日期':'sheet:发生日期','关联共同记录，已选 0 条':'modal:选择共同记录','保存到时刻册':'save','查看原记录':'read-reply','去看看共同记录':'route:m03-p06'}
    if c['selector'].startswith('body>nav'):return 'nav:'+nav[label]
    if label in rules:return rules[label]
    if c['native_input']:return 'input'
    raise AssertionError((page,label,'missing explicit behavior'))
def control(p,page,c,kind):
    seed(p,page);button=p.locator(c['selector']);expect(button).to_be_visible();expect(button).to_be_enabled();before=store(p)
    if kind=='file':
        with p.expect_file_chooser() as info:button.click()
        info.value.set_files({'name':'cover.png','mimeType':'image/png','buffer':bytes.fromhex('89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000b49444154789c636000020000050001a5f645400000000049454e44ae426082')});expect(p.locator('#cover-preview')).to_be_visible();assert store(p)==before;return
    if kind=='input':
        if button.get_attribute('type')=='radio':button.locator('..').click();expect(button).to_be_checked();button.focus();p.keyboard.press('Space');expect(button).to_be_checked()
        else:button.fill('一'*250);limit=button.get_attribute('maxlength');assert len(button.input_value())==int(limit);expect(button).to_be_focused()
        assert store(p)==before;return
    if kind=='save':p.locator('[name=name]').fill('实际保存的时刻')
    button.click()
    if kind.startswith('route:'):go(p,kind.split(':')[1])
    elif kind.startswith('nav:'):
        dest=kind.split(':')[1]
        if dest=='self':assert '/'+page+'.html' in p.url
        elif dest=='pet':p.wait_for_url('**/m07-p0*.html')
        else:go(p,dest)
    elif kind.startswith(('sheet:','modal:')):
        expect(p.locator('dialog h2')).to_have_text(kind.split(':')[1]);p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);expect(button).to_be_focused()
    elif kind=='expand':expect(button).to_have_text('收起章节');button.click();expect(button).to_have_text('查看全部 ›')
    elif kind=='refresh':expect(p.locator('.cards')).to_have_attribute('aria-busy','true');expect(button).to_be_disabled();expect(p.locator('.cards button')).to_have_count(1)
    elif kind=='collect-empty':go(p,'m04-p04');expect(p.locator('dialog h2')).to_have_text('选择共同记录');p.get_by_role('button',name='继续创建时刻',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
    elif kind=='save':go(p,'m04-p01');expect(p.locator('.cards button')).to_contain_text('实际保存的时刻');assert len(p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-moments"))'))==1;return
    elif kind=='read-reply':go(p,'m04-p03');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-moments"))[0].comments[0].read') is True;return
    else:raise AssertionError(kind)
    assert store(p)==before

def hidden(p,kind):
    seed(p,'m04-p03');before=store(p)
    if kind=='delete':
        p.locator('#more').click();p.get_by_role('button',name='删除重要时刻',exact=True).click();p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert store(p)==before
        p.locator('#more').click();p.get_by_role('button',name='删除重要时刻',exact=True).click();p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","moment-delete")');p.get_by_role('button',name='确认删除',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert store(p)==before
        p.locator('#more').click();p.get_by_role('button',name='删除重要时刻',exact=True).click();p.get_by_role('button',name='确认删除',exact=True).click();go(p,'m04-p02');assert len(p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records"))'))==3
    elif kind=='reply':
        reply(p);p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","moment-comment")');p.get_by_role('button',name='发送回应',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert store(p)==before;expect(p.get_by_label('回应这个时刻')).to_have_value('尚未发送的心意');p.get_by_role('button',name='发送回应',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert len(p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-moments"))[0].comments'))==2
    elif kind=='privacy':
        p.evaluate('localStorage.setItem("dujia-privacy",JSON.stringify({replies:false}))');p.locator('.message').click();expect(p.get_by_label('回应这个时刻')).to_be_disabled();expect(p.get_by_role('button',name='发送回应',exact=True)).to_be_disabled()
    elif kind=='date':
        seed(p,'m04-p04');p.locator('[name=date]').click();p.get_by_label('选择发生日期').fill('2026-09-10');p.get_by_role('button',name='使用这个日期',exact=True).click();expect(p.locator('[name=date]')).to_have_value('2026-09-10');p.locator('.back').click();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('[name=date]')).to_have_value('2026-09-10')
    elif kind=='load':
        seed(p,'m04-p01');before=store(p);p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","moment-load")');p.get_by_role('button',name='刷新时刻册',exact=True).click();p.get_by_role('button',name='重试加载时刻册',exact=True).click();expect(p.locator('.cards button')).to_have_count(1);assert store(p)==before

def layout(p,width):
    p.set_viewport_size({'width':width,'height':844});seed(p,'m04-p03');p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")');reply(p);p.get_by_role('button',name='取消',exact=True).click();expect(p.get_by_text('是否放弃当前修改？',exact=True)).to_be_visible()
    dialog=p.locator('dialog');box=dialog.bounding_box();assert box['x']>=0 and box['x']+box['width']<=width
    for name in ['继续编辑','放弃修改']:
        button=p.get_by_role('button',name=name,exact=True);button.scroll_into_view_if_needed();r=button.bounding_box();assert r['height']>=44 and r['x']>=0 and r['x']+r['width']<=width and r['y']+r['height']<=844-34
    expect(p.get_by_role('button',name='继续编辑',exact=True)).to_be_focused();p.screenshot(path=str(OUT/f'moment-reply-discard-{width}.png'),full_page=True);p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.get_by_label('回应这个时刻')).to_have_value('尚未发送的心意');p.get_by_label('回应这个时刻').fill('心意'*500);assert len(p.get_by_label('回应这个时刻').input_value())==300
rows=[];hashes=source();inventory=[];case_meta={}
with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    cases=[]
    if '--baseline' not in sys.argv and '--layout' not in sys.argv:
        for page in PAGES:
            c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');c.add_init_script(INIT);p=c.new_page();seed(p,page);controls=[v for v in p.evaluate(OBSERVE)['controls'] if v['visible'] and not v['disabled']];inventory.append({'id':page,'populated':PAGES[page],'controls':controls})
            for v in controls:
                name=page+' '+v['selector'];behavior=contract(page,v);case_meta[name]={'page':page,'label':v['label'],'selector':v['selector'],'contract':behavior,'scenario':'populated' if PAGES[page] else 'empty'};cases.append((name,lambda p,page=page,v=v:control(p,page,v,contract(page,v))))
            c.close()
        for name in ['delete','reply','privacy','date','load']:cases.append(('hidden-'+name,lambda p,name=name:hidden(p,name)))
    if '--layout' in sys.argv:
        cases=[('reply-discard-layout-'+str(w),lambda p,w=w:layout(p,w))for w in [320,360,390,414,430]]
    else:
        for exit in ['cancel','escape','back','drag']:cases.append(('reply-dirty-'+exit,lambda p,exit=exit:dirty(p,exit)))
    for name,run in cases:
        c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);p.set_default_navigation_timeout(15000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p);assert not errors,errors;row={'case':name,'passed':True}
        except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-1900:]}
        row.update(case_meta.get(name,{}));row.update(errors=errors,effective=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
    b.close()
assert hashes==source()
(OUT/('moment-reply-layout-results.json' if '--layout' in sys.argv else 'moment-controls-results.json')).write_text(json.dumps({'files':hashes,'inventory':inventory,'results':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(row['passed'] for row in rows) else 1)
