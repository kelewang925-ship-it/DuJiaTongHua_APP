"""Explicit initial controls for 12 home/diary/photo fixtures and related hidden branches."""
from pathlib import Path
import json,hashlib,traceback,sys,base64
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from audit_runtime import INIT,OBSERVE
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;BASE='http://127.0.0.1:8765/';OUT=ROOT/'evidence'/('baseline' if '--baseline' in sys.argv else 'current')
PAGES={f'm03-p{i:02}':i not in [1,3,5,9,11]for i in range(1,13)}
QUERY={'m03-p04':'?q=共同','m03-p07':'?id=audit-private','m03-p08':'?id=audit-diary','m03-p12':'?id=audit-photo'}
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jB2kAAAAASUVORK5CYII=')
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
def seed(p,page):
    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',data(PAGES[page]));p.goto(BASE+'pages/'+page+'.html'+QUERY.get(page,''))
    if page=='m03-p04':expect(p.locator('.prototype-search-results h2')).to_be_visible()
    if page=='m03-p06':expect(p.locator('.prototype-diary-card')).to_have_count(2)
    if page=='m03-p10':expect(p.locator('.prototype-photo-card')).to_have_count(1)
    p.evaluate('document.fonts.ready')
def store(p):return p.evaluate('JSON.stringify({...localStorage})')
def go(p,page):p.wait_for_url('**/'+page+'.html*')
def image(p):p.locator('#file').set_input_files({'name':'memory.png','mimeType':'image/png','buffer':PNG})
def rows(p):return p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records"))')
def dirty(p,page,exit):
    seed(p,page);before=store(p);p.locator('#reply').fill('未发送的温柔回应')
    def close():p.go_back()if exit=='back'else p.locator('.back').click()
    close();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('#reply')).to_have_value('未发送的温柔回应');assert store(p)==before;expect(p.locator('dialog')).to_have_count(0);p.wait_for_function('history.state?.prototypeGuard===true')
    close();p.get_by_role('button',name='放弃修改',exact=True).click();go(p,'m03-p06'if page=='m03-p08'else'm03-p10');assert store(p)==before

def legacy_date(p):
    seed(p,'m03-p06');expect(p.locator('.prototype-diary-list')).not_to_contain_text('Invalid Date');expect(p.locator('.prototype-diary-list')).to_contain_text('2026')
def caption_search(p):
    seed(p,'m03-p04');p.goto(BASE+'pages/m03-p03.html');p.locator('#query').fill('共同照片说明');p.locator('#query').press('Enter');go(p,'m03-p04');expect(p.locator('.prototype-search-results button')).to_contain_text('共同照片')
def privacy(p,page):
    seed(p,page);p.evaluate('localStorage.setItem("dujia-privacy",JSON.stringify({replies:false}))');p.reload();expect(p.locator('#reply')).to_be_disabled();expect(p.locator('#emoji')).to_be_disabled();expect(p.locator('#message [type=submit]')).to_be_disabled()

def contract(page,c):
    label=c['label'];selector=c['selector'];pop=PAGES[page]
    if selector.startswith('body>nav'):return 'nav:'+{'首页':'self','重要时刻':'m04-p01'if pop else'm04-p02','工坊':'m05-p01','宠物':'pet','我的':'m06-p01'}[label]
    if page in ['m03-p01','m03-p02']:
        if label=='搜索共同记录':return'route:m03-p03'
        if label.startswith('写日记'):return'route:m03-p05'
        if label.startswith('添加照片'):return'route:m03-p11'
        if label.startswith('去童话工坊'):return'route:m05-p01'
        if label=='查看全部 ›':return'route:m03-p06'
        if label.startswith('共同日记'):return'route:m03-p08'
        if label.startswith('自己的日记'):return'route:m03-p07'
        if label.startswith('共同照片'):return'route:m03-p12'
        if selector.endswith('button:nth-of-type(2)'):return'route:m08-p15'
        if selector.endswith('button:nth-of-type(3)'):return'route:m04-p10'
    if page in ['m03-p03','m03-p04']:
        if label=='搜索关键词':return'query'
        if label in ['返回首页','返回搜索']:return'route:'+('m03-p01'if page=='m03-p03'else'm03-p03')
        if label in ['清除搜索','清除']:return'clear-query'
        if label.startswith('共同日记'):return'route:m03-p08'
        if label.startswith('共同照片'):return'route:m03-p12'
        return'search-chip:'+label
    if label.startswith('返回'):
        return'route:'+{'m03-p05':'m03-p06','m03-p06':'m03-p02','m03-p07':'m03-p06','m03-p08':'m03-p06','m03-p09':'m03-p01','m03-p10':'m03-p02','m03-p11':'m03-p09','m03-p12':'m03-p10'}[page]
    if label=='存草稿':return'diary-draft'
    if label=='保存日记':return'diary-save'
    if label=='今天的心情':return'mood'
    if label=='编辑日记':return'route:m03-p05'
    if label=='编辑照片':return'route:m03-p11'
    if label=='更多操作':return'sheet:'+('日记操作'if page in ['m03-p07','m03-p08']else'照片操作')
    if label=='筛选日记':return'sheet:筛选日记'
    if label=='筛选照片':return'sheet:筛选照片'
    if label=='刷新日记':return'refresh:diary'
    if label=='刷新相册':return'refresh:photo'
    if label=='全部':return'tab:all'
    if label=='草稿 0':return'tab:draft'
    if label=='共同可见':return'tab:shared'
    if label=='旅行':return'tab:travel'
    if label.startswith('共同日记'):return'route:m03-p08'
    if label.startswith('自己的日记'):return'route:m03-p07'
    if label=='共同照片':return'route:m03-p12'
    if label in ['写日记']:return'route:m03-p05'
    if label in ['＋ 添加照片','添加第一张照片','从系统相册选择']:return'route:m03-p11'
    if label in ['添加照片','选择照片']:return'file'
    if label in ['完成','保存照片']:return'photo-save'
    if label=='照片日期':return'sheet:选择照片日期'
    if label=='添加标签':return'sheet:照片标签'
    if label=='添加表情':return'emoji'
    if label=='发送留言':return'reply'
    if c['native_input']:return'input'
    raise AssertionError((page,label,'missing explicit contract'))

def control(p,page,c,kind):
    seed(p,page);button=p.locator(c['selector']);expect(button).to_be_visible();expect(button).to_be_enabled();before=store(p)
    if kind in ['input','query','mood']:
        typ=button.get_attribute('type')
        if kind=='mood':button.select_option(index=1);assert button.input_value()!=''
        elif typ=='radio':button.locator('..').click();expect(button).to_be_checked();button.focus();p.keyboard.press('Space');expect(button).to_be_checked()
        else:
            limit=int(button.get_attribute('maxlength')or'100');button.fill('心'* (limit+10));assert len(button.input_value())==limit;expect(button).to_be_focused()
        assert store(p)==before;return
    if kind=='file':
        with p.expect_file_chooser()as info:button.click()
        info.value.set_files({'name':'memory.png','mimeType':'image/png','buffer':PNG});expect(p.locator('#preview'if page=='m03-p05'else'#selected')).to_be_visible();assert store(p)==before;return
    if kind.startswith('diary-'):
        p.locator('[name=title]').fill('实际控件保存');p.locator('[name=body]').fill('可回到列表继续编辑的故事')
    if kind=='photo-save':image(p);expect(p.locator('#selected')).to_be_visible();p.locator('[name=caption]').fill('实际控件照片')
    if kind=='reply':p.locator('#reply').fill('实际发送的回应')
    if kind=='clear-query'and page=='m03-p03':p.locator('#query').fill('待清除')
    button.click()
    if kind.startswith(('route:','nav:')):
        dest=kind.split(':')[1]
        if dest=='self':assert '/'+page+'.html'in p.url
        elif dest=='pet':p.wait_for_url('**/m07-p0*.html')
        else:go(p,dest)
    elif kind.startswith('sheet:'):
        expect(p.locator('dialog h2')).to_have_text(kind.split(':')[1]);p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);expect(button).to_be_focused()
    elif kind.startswith('search-chip:'):
        go(p,'m03-p04');assert p.locator('#query').input_value()==kind.split(':')[1];assert p.locator('#query').input_value()in p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-search-history"))');return
    elif kind=='clear-query':
        if page=='m03-p04':go(p,'m03-p03')
        expect(p.locator('#query')).to_have_value('');expect(p.locator('#query')).to_be_focused()
    elif kind.startswith('tab:'):
        expect(button).to_have_attribute('aria-selected','true')
        if kind=='tab:draft':expect(p.get_by_role('button',name='写第一篇日记',exact=True)).to_be_visible()
        if kind=='tab:travel':expect(p.get_by_role('button',name='清除筛选',exact=True)).to_be_visible()
    elif kind.startswith('refresh:'):
        box=p.locator('.prototype-diary-list'if kind.endswith('diary')else'.grid');expect(box).to_have_attribute('aria-busy','true');expect(button).to_be_disabled();expect(box.locator('button')).to_have_count(2 if kind.endswith('diary')else 1)
    elif kind.startswith('diary-'):
        go(p,'m03-p06');r=rows(p);assert len(r)==1 and r[0]['status']==('draft'if kind=='diary-draft'else'published');return
    elif kind=='photo-save':go(p,'m03-p10');assert len(rows(p))==1 and rows(p)[0]['type']=='photo';return
    elif kind=='emoji':assert '❤️'in p.locator('#reply').input_value();expect(p.locator('#reply')).to_be_focused()
    elif kind=='reply':expect(p.locator('#reply')).to_have_value('');assert sum(len(r.get('comments',[]))for r in rows(p))==1;return
    else:raise AssertionError(kind)
    assert store(p)==before

def hidden(p,kind):
    page='m03-p08'if kind.startswith('diary')else'm03-p12';seed(p,page);before=store(p)
    if kind.endswith('reply'):
        p.locator('#reply').fill('失败后保留的回应');p.evaluate('k=>sessionStorage.setItem("dujia-prototype-fail-next",k)',kind.replace('reply','comment'));p.locator('#message [type=submit]').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');expect(p.locator('#reply')).to_have_value('失败后保留的回应');assert store(p)==before;p.locator('#message [type=submit]').click();expect(p.locator('#reply')).to_have_value('');p.locator('.back').click();go(p,'m03-p06'if page=='m03-p08'else'm03-p10');expect(p.locator('dialog')).to_have_count(0)
    elif kind.endswith('delete'):
        label='日记'if page=='m03-p08'else'照片'
        def choose():p.locator('#more').click();p.get_by_role('button',name='删除'+label,exact=True).click()
        choose();p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert store(p)==before;choose();p.evaluate('k=>sessionStorage.setItem("dujia-prototype-fail-next",k)',kind);p.get_by_role('button',name='确认删除',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert store(p)==before;choose();p.get_by_role('button',name='确认删除',exact=True).click();go(p,'m03-p06'if page=='m03-p08'else'm03-p09');assert len(rows(p))==2

def extra(p,kind):
    if kind in ['diary-filter','photo-filter']:
        diary=kind.startswith('diary');seed(p,'m03-p06'if diary else'm03-p10');before=store(p);p.locator('#filter').click();p.get_by_label('可见范围'if diary else'照片可见范围',exact=True).select_option('private');p.get_by_role('button',name='应用筛选',exact=True).click()
        if diary:expect(p.locator('.prototype-diary-card')).to_have_count(1);expect(p.locator('.prototype-diary-card')).to_contain_text('自己的日记')
        else:expect(p.get_by_role('button',name='清除筛选',exact=True)).to_be_visible()
        p.locator('#filter').click();p.get_by_role('dialog').get_by_role('button',name='清除筛选',exact=True).click();expect(p.locator('.prototype-diary-card'if diary else'.prototype-photo-card')).to_have_count(2 if diary else 1);assert store(p)==before
    elif kind=='photo-date-tags':
        seed(p,'m03-p11');before=store(p);p.locator('[name=date]').click();p.locator('dialog input[type=date]').fill('2026-09-05');p.get_by_role('button',name='使用这个日期',exact=True).click();expect(p.locator('[name=date]')).to_have_value('2026-09-05');p.locator('#add-tag').click();p.get_by_label('编辑照片标签',exact=True).fill('旅行、晚霞');p.get_by_role('button',name='使用这些标签',exact=True).click();expect(p.locator('[name=tag]')).to_have_value('旅行、晚霞');p.locator('#add-tag').click();p.get_by_label('编辑照片标签',exact=True).fill('取消的标签');p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('[name=tag]')).to_have_value('旅行、晚霞');p.locator('.back').click();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();assert store(p)==before
    elif kind=='search-retry':
        seed(p,'m03-p04');before=store(p);p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","record-search")');p.reload();p.get_by_role('button',name='重试搜索',exact=True).click();expect(p.locator('.prototype-search-results button')).to_have_count(2);assert store(p)==before
    elif kind=='diary-image-remove':
        seed(p,'m03-p05');before=store(p);image(p);expect(p.locator('#preview')).to_be_visible();p.locator('#remove').click();expect(p.locator('#preview')).to_be_hidden();p.locator('.back').click();go(p,'m03-p06');expect(p.locator('dialog')).to_have_count(0);assert store(p)==before
def layout(p,page,width):
    p.set_viewport_size({'width':width,'height':844});seed(p,page);before=store(p);p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")');p.locator('#reply').fill('温柔回应'*100);assert len(p.locator('#reply').input_value())==300;p.locator('.back').click();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？')
    for name in ['继续编辑','放弃修改']:
        button=p.get_by_role('button',name=name,exact=True);button.scroll_into_view_if_needed();r=button.bounding_box();assert r['height']>=44 and r['x']>=0 and r['x']+r['width']<=width and r['y']+r['height']<=844-34
    p.screenshot(path=str(OUT/f'record-reply-{page}-{width}.png'),full_page=True);p.get_by_role('button',name='继续编辑',exact=True).click();assert len(p.locator('#reply').input_value())==300 and store(p)==before
rows_out=[];hashes=source();inventory=[];cases=[];metadata={}
with sync_playwright()as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    if '--baseline'not in sys.argv and '--layout'not in sys.argv:
        for page in PAGES:
            c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');c.add_init_script(INIT);p=c.new_page();seed(p,page);controls=[v for v in p.evaluate(OBSERVE)['controls']if v['visible']and not v['disabled']];inventory.append({'page':page,'populated':PAGES[page],'controls':controls})
            for v in controls:
                name=page+' '+v['selector'];behavior=contract(page,v);metadata[name]={'page':page,'label':v['label'],'selector':v['selector'],'contract':behavior,'scenario':'populated'if PAGES[page]else'empty'};cases.append((name,lambda p,page=page,v=v,behavior=behavior:control(p,page,v,behavior)))
            c.close()
        for kind in ['diary-reply','photo-reply','diary-delete','photo-delete']:cases.append(('hidden-'+kind,lambda p,kind=kind:hidden(p,kind)))
        for kind in ['diary-filter','photo-filter','photo-date-tags','search-retry','diary-image-remove']:cases.append(('hidden-'+kind,lambda p,kind=kind:extra(p,kind)))
    for page in ['m03-p08','m03-p12']:
        for exit in ['button','back']:cases.append(('dirty-'+page+'-'+exit,lambda p,page=page,exit=exit:dirty(p,page,exit)))
        cases.append(('privacy-'+page,lambda p,page=page:privacy(p,page)))
    cases += [('legacy-date',legacy_date),('photo-caption-search',caption_search)]
    if '--layout'in sys.argv:cases=[('layout-'+page+'-'+str(width),lambda p,page=page,width=width:layout(p,page,width))for page in ['m03-p08','m03-p12']for width in [320,360,390,414,430]]
    for name,run in cases:
        c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p);assert not errors,errors;row={'case':name,'passed':True}
        except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-1600:]}
        row.update(metadata.get(name,{}));row.update(errors=errors,effective=p.url);rows_out.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
    b.close()
assert hashes==source()
(OUT/('record-reply-layout-results.json'if '--layout'in sys.argv else'record-controls-results.json')).write_text(json.dumps({'files':hashes,'inventory':inventory,'results':rows_out},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(r['passed']for r in rows_out)else 1)
