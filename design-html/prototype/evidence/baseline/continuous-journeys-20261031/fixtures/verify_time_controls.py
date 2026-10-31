"""Explicit reminder/anniversary/capsule fixtures; source-bound browser evidence."""
from pathlib import Path
import json,hashlib,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from audit_runtime import INIT,OBSERVE
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;BASE='http://127.0.0.1:8765/'
OUT=ROOT/'evidence'/('baseline' if '--baseline' in sys.argv else 'current')
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
def seed(p,page):
    d=data(True)
    for kind in ['anniversaries','capsules','moments','works','records']:d['dujia-prototype-'+kind]=[]
    d['dujia-prototype-pet']=None;d['dujia-prototype-reminder-reads']=[]
    d['dujia-prototype-moments']=[dict(id='time-moment',name='关联时刻',story='已有的故事',date='2026-10-04',comments=[],related=[])]
    if page not in ['m04-p06','m04-p08']:
        d['dujia-prototype-anniversaries']=[dict(id='time-future',name='未来约定',date='2026-12-24',repeat=True,enabled=True,reminderDays=3,momentId='time-moment'),dict(id='time-today',name='今天约定',date='2026-10-05',repeat=True,enabled=True,reminderDays=0,momentId='time-moment')]
    d['dujia-prototype-capsules']=[dict(id='time-sealed',name='封存的信',message='封存内容不能提前展示',opening='2026-10-06',status='sealed',reminder=True),dict(id='time-opened',name='开启的信',message='给未来的祝福',opening='2026-10-04',status='opened',reminder=True),dict(id='time-draft',name='草稿的信',message='草稿内容',opening='2026-10-06',status='draft',reminder=True)] if page not in ['m04-p06','m04-p08'] else []
    q={'m04-p10':'?id=time-future','m04-p11':'?id=time-today','m04-p14':'?id=time-opened','m04-p15':'?id=time-sealed'}.get(page,'')
    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-05");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d);p.goto(BASE+'pages/'+page+'.html'+q)
    if page=='m04-p07':expect(p.locator('.prototype-anniversary-card')).to_have_count(2)
    if page=='m04-p12':expect(p.locator('.prototype-capsule-card')).to_have_count(1)
    p.evaluate('document.fonts.ready')
def store(p):return p.evaluate('JSON.stringify({...localStorage})')
def contract(page,v):
    label=v['label']
    if label in ['返回重要时刻','去看看重要时刻']:return 'route:m04-p01'
    if label in ['返回纪念日列表','返回纪念日']:return 'route:m04-p07'
    if label=='返回胶囊列表':return 'route:m04-p12'
    if label in ['添加纪念日','添加第一个纪念日','编辑纪念日']:return 'route:m04-p09'
    if label in ['新建时光胶囊','＋ 新建时光胶囊']:return 'route:m04-p13'
    if label.startswith('今天约定就在今天'):return 'notice:time-today'
    if label.startswith('今天约定\n')or label=='2026-10-05':return 'route:m04-p11'
    if label.startswith('未来约定\n'):return 'route:m04-p10'
    if label in ['今天约定提醒','未来约定提醒']:return 'toggle-anniversary:'+('time-today'if label.startswith('今天')else'time-future')
    if label in ['关联时刻','查看这个时刻']:return 'route:m04-p03'
    if label in ['写下新的共同记录','一起留下今天的记录']:return 'route:m03-p05'
    if label in ['更多操作','更多胶囊操作']:return 'sheet:'+('纪念日操作'if label=='更多操作'else'胶囊操作')
    if label=='纪念日日期':return 'sheet:纪念日日期'
    if label=='opening':return 'sheet:开启日期'
    if label.startswith('刷新'):return 'refresh:'+('anniversary'if label=='刷新纪念日'else'capsule')
    if label in ['等待开启','已经开启','草稿']:return 'tab:'+label
    if label.startswith('封存的信'):return 'route:m04-p15'
    if label=='添加照片':return 'file'
    if label=='保存纪念日':return 'save-anniversary'
    if label=='暂存草稿':return 'save-draft'
    if label=='封存这份心意':return 'save-sealed'
    if label=='把这一刻收录进重要时刻':return 'collect'
    if v['native_input']:return 'native'
    raise AssertionError((page,label,'missing contract'))
def control(p,page,v,kind):
    seed(p,page);button=p.locator(v['selector']);before=store(p);expect(button).to_be_visible();expect(button).to_be_enabled()
    if kind=='native':
        typ=button.get_attribute('type')
        if typ=='checkbox':old=button.is_checked();button.click();expect(button).to_be_checked(checked=not old)
        elif v['tag']=='SELECT':button.select_option(index=1);expect(button).to_have_value('提前 1 天'if page=='m04-p09'and '提前'in v['label']else'time-moment')
        else:limit=int(button.get_attribute('maxlength')or'2000');button.fill('信'*(limit+5));assert len(button.input_value())==limit;expect(button).to_be_focused()
        if page=='m04-p15':assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-capsules")).find(v=>v.id==="time-sealed").reminder')is False
        else:assert store(p)==before
        return
    if kind=='file':
        from PIL import Image
        from io import BytesIO
        stream=BytesIO();Image.new('RGB',(30,20),'blue').save(stream,format='PNG')
        with p.expect_file_chooser()as info:button.click()
        info.value.set_files(dict(name='memory.png',mimeType='image/png',buffer=stream.getvalue()));expect(p.locator('.prototype-capsule-preview')).to_be_visible();assert store(p)==before;return
    if kind.startswith('save-'):
        p.locator('[name=name]').fill('控件实际保存')
        if page=='m04-p13':p.locator('[name=message]').fill('给未来的一封信')
    button.click()
    if kind.startswith('route:'):
        dest=kind.split(':')[1];p.wait_for_url('**/'+dest+'.html*')
        from urllib.parse import urlparse,parse_qs
        q=parse_qs(urlparse(p.url).query)
        if dest=='m04-p03':assert q['id']==['time-moment']
        if dest=='m04-p10':assert q['id']==['time-future']
        if dest=='m04-p11':assert q['id']==['time-today']
        if dest=='m04-p15':assert q['id']==['time-sealed']
        if dest in ['m03-p05','m04-p09']and page in ['m04-p10','m04-p11']:assert q['anniversary'if dest=='m03-p05'else'id']==['time-future'if page=='m04-p10'else'time-today']
    elif kind.startswith('sheet:'):expect(p.locator('dialog h2')).to_have_text(kind.split(':')[1]);p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);expect(button).to_be_focused()
    elif kind.startswith('refresh:'):
        box=p.locator('.entries'if kind.endswith('anniversary')else'.cards');expect(box).to_have_attribute('aria-busy','true');expect(box.locator('button')).to_have_count(4 if kind.endswith('anniversary')else 1)
    elif kind.startswith('tab:'):
        expect(button).to_have_attribute('aria-selected','true');expect(p.locator('.cards')).to_contain_text({'等待开启':'封存的信','已经开启':'开启的信','草稿':'草稿的信'}[kind.split(':')[1]])
    elif kind.startswith('toggle-anniversary:'):
        expect(button).to_have_attribute('aria-checked','false');assert p.evaluate('id=>JSON.parse(localStorage.getItem("dujia-prototype-anniversaries")).find(v=>v.id===id).enabled',kind.split(':')[1])is False;return
    elif kind.startswith('notice:'):
        p.wait_for_url('**/m04-p11.html?id=time-today');saved=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-reminder-reads"))');assert len(saved)==1 and saved[0]['read']and saved[0]['targetId']=='time-today';return
    elif kind.startswith('save-'):
        p.wait_for_url('**/'+('m04-p07'if kind=='save-anniversary'else'm04-p12'if kind=='save-draft'else'm04-p15')+'.html*');values=p.evaluate('key=>JSON.parse(localStorage.getItem(key))','dujia-prototype-anniversaries'if kind=='save-anniversary'else'dujia-prototype-capsules');assert len(values)==(3 if kind=='save-anniversary'else 4);assert sum(v['name']=='控件实际保存'for v in values)==1;return
    elif kind=='collect':p.wait_for_url('**/m04-p03.html?id=capsule-moment-time-opened');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-moments")).length')==2;return
    else:raise AssertionError(kind)
    assert store(p)==before
def collect_quota(p,key):
    seed(p,'m04-p14');before=store(p)
    p.evaluate('key=>{const old=Storage.prototype.setItem;window.restoreTimeWrite=old;Storage.prototype.setItem=function(k,v){if(k===key)throw new DOMException("full","QuotaExceededError");return old.call(this,k,v)}}',key)
    p.locator('#collect').click();expect(p.locator('.prototype-toast')).to_contain_text('不足');assert store(p)==before,'Second write failed but first collection write persisted'
    p.evaluate('()=>{Storage.prototype.setItem=window.restoreTimeWrite}');p.locator('#collect').click();p.wait_for_url('**/m04-p03.html?id=capsule-moment-time-opened');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-moments")).length')==2
    seed_id=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-capsules")).find(v=>v.id==="time-opened").momentId');assert seed_id=='capsule-moment-time-opened'
    p.goto(BASE+'pages/m04-p14.html?id=time-opened');p.locator('#collect').click();p.wait_for_url('**/m04-p03.html?id=capsule-moment-time-opened');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-moments")).length')==2
def dirty(p,page,mode):
    seed(p,page);before=store(p);p.locator('[name=name]').fill('返回应保留的编辑')
    def back():p.go_back()if mode=='browser'else p.locator('.back').click()
    back();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('[name=name]')).to_have_value('返回应保留的编辑');assert store(p)==before
    back();p.get_by_role('button',name='放弃修改',exact=True).click();p.wait_for_url('**/'+('m04-p07'if page=='m04-p09'else'm04-p12')+'.html');assert store(p)==before
def notice_quota(p):
    seed(p,'m04-p05');before=store(p)
    p.evaluate('()=>{const old=Storage.prototype.setItem;window.restoreTimeWrite=old;Storage.prototype.setItem=function(k,v){if(k==="dujia-prototype-reminder-reads")throw new DOMException("full","QuotaExceededError");return old.call(this,k,v)}}')
    p.locator('.prototype-reminder-card').click();expect(p.locator('.prototype-toast')).to_contain_text('不足');assert p.url.endswith('m04-p05.html')and store(p)==before
    p.evaluate('()=>{Storage.prototype.setItem=window.restoreTimeWrite}');p.locator('.prototype-reminder-card').click();p.wait_for_url('**/m04-p11.html?id=time-today');p.goto(BASE+'pages/m04-p05.html');expect(p.locator('.prototype-reminder-card')).to_contain_text('已读');assert len(p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-reminder-reads"))'))==1
files=source();rows=[];inventory=[]
with sync_playwright()as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    if '--inventory' in sys.argv or '--controls' in sys.argv:
        for i in range(5,16):
            page=f'm04-p{i:02}';c=b.new_context(viewport={'width':390,'height':844});c.add_init_script(INIT);p=c.new_page();p.set_default_timeout(4500);seed(p,page);controls=[v for v in p.evaluate(OBSERVE)['controls']if v['visible']and not v['disabled']];inventory.append(dict(page=page,effective=p.url,controls=controls));print(page,len(controls),flush=True);c.close()
        if '--controls'in sys.argv:
            for entry in inventory:
                for v in entry['controls']:
                    c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));kind=contract(entry['page'],v)
                    try:control(p,entry['page'],v,kind);assert not errors;row=dict(passed=True)
                    except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
                    row.update(page=entry['page'],selector=v['selector'],label=v['label'],contract=kind,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+entry['page']+' '+v['label'].replace('\n',' '),flush=True);c.close()
    else:
        cases=[('collect-quota-rollback-retry-idempotence:'+key,lambda p,key=key:collect_quota(p,key))for key in ['dujia-prototype-capsules','dujia-prototype-moments']]+[(page+'-dirty-'+mode,lambda p,page=page,mode=mode:dirty(p,page,mode))for page in ['m04-p09','m04-p13']for mode in ['button','browser']]+[('reminder-read-quota-retry',notice_quota)]
        for name,run in cases:
            c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:run(p);assert not errors;row=dict(passed=True)
            except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
            row.update(case=name,errors=errors,effective=p.url);rows.append(row);print(row,flush=True);c.close()
    b.close()
assert files==source();OUT.mkdir(parents=True,exist_ok=True)
(OUT/('time-control-inventory.json'if '--inventory'in sys.argv else'time-controls-results.json'if '--controls'in sys.argv else'time-collection-results.json')).write_text(json.dumps(dict(files=files,fixture_date='2026-10-05',inventory=inventory,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed']for r in rows)else 1)
