"""Corrupt records must remain recoverable; no successful result is inferred from a toast."""
from pathlib import Path
import hashlib,json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data

ROOT=Path(__file__).resolve().parent;BASE='http://127.0.0.1:8765/';KEY='dujia-prototype-records'
OUT=ROOT/'evidence'/('baseline' if '--baseline' in sys.argv else 'current')
DEMO=ROOT.parent
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
def seed(p,raw):
    fixture=data(True);fixture.pop(KEY);p.goto(BASE+'prototype/review.html')
    p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));}',fixture)
    p.evaluate('(v)=>localStorage.setItem("dujia-prototype-records",v)',raw);p.goto(BASE+'pages/m03-p06.html')
def original(p):return p.evaluate('localStorage.getItem("dujia-prototype-records")')
def archives(p):return p.evaluate("Object.keys(localStorage).filter(k=>k.startsWith('dujia-prototype-record-recovery-')).map(k=>JSON.parse(localStorage.getItem(k)))")
def prompt(p):expect(p.get_by_role('dialog',name='记录需要恢复',exact=True)).to_be_visible()
def repair(p):
    prompt(p);p.get_by_role('dialog').get_by_role('button',name='恢复可读记录',exact=True).click();expect(p.locator('dialog h2')).to_have_text('保留原始副本并恢复？');p.get_by_role('dialog').get_by_role('button',name='确认恢复',exact=True).click()
def valid():return data(True)[KEY][:1]
def mixed(p):
    good=valid();raw=json.dumps(good+[None],ensure_ascii=False);seed(p,raw);prompt(p);assert original(p)==raw
    with p.expect_download() as info:p.get_by_role('dialog').get_by_role('button',name='导出原始记录',exact=True).click()
    assert Path(info.value.path()).read_text(encoding='utf-8')==raw
    prompt(p);p.get_by_role('dialog').get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
    assert p.evaluate("PrototypeUI.write('dujia-prototype-records',[])") is False
    assert original(p)==raw
    p.evaluate("localStorage.setItem('dujia-prototype-tags','[]')")
    assert p.evaluate("PrototypePreferences.transaction([['dujia-prototype-tags',[{id:'new',name:'不能写入'}]],['dujia-prototype-records',[]]])") is False
    assert p.evaluate("localStorage.getItem('dujia-prototype-tags')")=='[]';assert original(p)==raw
    p.get_by_role('button',name='恢复记录',exact=True).click();repair(p)
    p.wait_for_function("JSON.parse(localStorage.getItem('dujia-prototype-records')).length===1")
    assert json.loads(original(p))==good and archives(p)==[raw]
    p.reload();expect(p.get_by_role('button',name='共同日记',exact=False)).to_be_visible();expect(p.locator('dialog')).to_have_count(0)

def reset_bad(p,raw):
    seed(p,raw);repair(p);p.wait_for_function("localStorage.getItem('dujia-prototype-records')==='[]'");assert archives(p)==[raw]
    p.reload();p.get_by_role('button',name='写第一篇日记',exact=True).click();p.wait_for_url('**/m03-p05.html');p.locator('[name=title]').fill('恢复后新故事');p.locator('[name=body]').fill('原始副本仍完整保留。');p.locator('#diary .submit').click();p.wait_for_url('**/m03-p06.html');assert len(json.loads(original(p)))==1 and archives(p)==[raw]

def duplicate(p):
    good=valid();raw=json.dumps(good+[{**good[0],'title':'重复的ID'}],ensure_ascii=False);seed(p,raw);repair(p);p.wait_for_function("JSON.parse(localStorage.getItem('dujia-prototype-records')).length===1");assert json.loads(original(p))==good and archives(p)==[raw]

def nested(p):
    record={**valid()[0],'tags':['旅行',None,5],'comments':[None,{'id':'reply-ok','author':'阿舟','text':'可读回应'}, {'id':'bad','text':{}}]};raw=json.dumps([record],ensure_ascii=False);seed(p,raw);repair(p)
    p.wait_for_function("JSON.parse(localStorage.getItem('dujia-prototype-records'))[0].tags.length===1")
    actual=json.loads(original(p))[0];assert actual['body']==record['body'] and actual['tags']==['旅行'] and actual['comments']==[record['comments'][1]] and archives(p)==[raw]

def archive_failure(p):
    raw=json.dumps(valid()+[None],ensure_ascii=False);seed(p,raw);prompt(p)
    p.evaluate("const old=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(String(k).startsWith('dujia-prototype-record-recovery-'))throw new DOMException('full','QuotaExceededError');return old.call(this,k,v)};true")
    repair(p);expect(p.locator('.prototype-toast')).to_contain_text('未能保存');assert original(p)==raw and not archives(p)

def race(p):
    raw=json.dumps(valid()+[None],ensure_ascii=False);seed(p,raw);prompt(p);p.get_by_role('dialog').get_by_role('button',name='恢复可读记录',exact=True).click();expect(p.locator('dialog h2')).to_have_text('保留原始副本并恢复？')
    fresh=[{**valid()[0],'title':'另一页面刚保存的内容'}];p.evaluate('(v)=>localStorage.setItem("dujia-prototype-records",JSON.stringify(v))',fresh)
    p.get_by_role('dialog').get_by_role('button',name='确认恢复',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('其他页面');assert json.loads(original(p))==fresh and not archives(p)

def healthy(p):
    raw=json.dumps(valid(),ensure_ascii=False);seed(p,raw);expect(p.get_by_role('button',name='共同日记',exact=False)).to_be_visible();expect(p.locator('dialog')).to_have_count(0);expect(p.get_by_role('button',name='恢复记录',exact=True)).to_have_count(0);assert original(p)==raw and not archives(p)

def backup_race(p):
    raw=json.dumps(valid()+[None],ensure_ascii=False);seed(p,raw);prompt(p);fresh=[{**valid()[0],'title':'备份期间的新内容'}]
    p.evaluate("fresh=>{const old=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){old.call(this,k,v);if(String(k).startsWith('dujia-prototype-record-recovery-'))old.call(this,'dujia-prototype-records',JSON.stringify(fresh));};return true;}",fresh)
    repair(p);expect(p.locator('.prototype-toast')).to_contain_text('其他页面');assert json.loads(original(p))==fresh and archives(p)==[raw]

def replacement_failure(p):
    raw=json.dumps(valid()+[None],ensure_ascii=False);seed(p,raw);prompt(p)
    p.evaluate("const old=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==='dujia-prototype-records')throw new DOMException('full','QuotaExceededError');return old.call(this,k,v)};true")
    repair(p);expect(p.locator('.prototype-toast')).to_contain_text('未能保存');assert original(p)==raw and archives(p)==[raw]

def dirty_editor(p):
    seed(p,json.dumps(valid(),ensure_ascii=False));p.goto(BASE+'pages/m03-p05.html');p.locator('[name=title]').fill('恢复时不丢输入');p.locator('[name=body]').fill('还没保存的正文仍在。');raw=json.dumps(valid()+[None],ensure_ascii=False)
    p.evaluate('(v)=>localStorage.setItem("dujia-prototype-records",v)',raw);p.locator('#diary .submit').click();repair(p)
    expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('dialog').get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
    expect(p.locator('[name=title]')).to_have_value('恢复时不丢输入');expect(p.locator('[name=body]')).to_have_value('还没保存的正文仍在。');assert archives(p)==[raw]
    p.locator('#diary .submit').click();p.wait_for_url('**/m03-p06.html');items=json.loads(original(p));assert len(items)==2 and any(v['title']=='恢复时不丢输入' for v in items)

def retry_external(p):
    raw=json.dumps(valid()+[None],ensure_ascii=False);seed(p,raw);prompt(p)
    fresh=[{**valid()[0],'title':'外部修好的最新日记'}];p.evaluate('(v)=>localStorage.setItem("dujia-prototype-records",JSON.stringify(v))',fresh)
    p.get_by_role('dialog').get_by_role('button',name='重新检查',exact=True).click()
    expect(p.get_by_role('button',name='外部修好的最新日记',exact=False)).to_be_visible();expect(p.locator('dialog')).to_have_count(0);assert json.loads(original(p))==fresh and not archives(p)

def reader(p,page):
    raw=json.dumps(valid()+[None],ensure_ascii=False);seed(p,raw);prompt(p);p.get_by_role('dialog').get_by_role('button',name='稍后处理',exact=True).click()
    expect(p.locator('dialog')).to_have_count(0)
    p.goto(BASE+'pages/'+page+'.html');prompt(p);assert original(p)==raw
    p.get_by_role('dialog').get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
    expect(p.get_by_role('button',name='恢复记录',exact=True)).to_be_visible();assert original(p)==raw

def layout(p,width):
    p.set_viewport_size({'width':width,'height':844});seed(p,json.dumps(valid()+[None],ensure_ascii=False));prompt(p)
    p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
    for button in p.get_by_role('dialog').get_by_role('button').all():
        button.scroll_into_view_if_needed();box=button.bounding_box();assert box['height']>=44 and box['width']>=44
        assert button.evaluate('(e)=>{const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return e===hit||e.contains(hit)}')
    assert p.evaluate('document.documentElement.scrollWidth')<=width
    p.get_by_role('dialog').get_by_role('button',name='稍后处理',exact=True).click()
    b=p.get_by_role('button',name='恢复记录',exact=True);box=b.bounding_box();assert box['height']>=44 and box['y']+box['height']<=844-34
    assert b.evaluate('(e)=>{const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return e===hit||e.contains(hit)}')
    b.click();prompt(p);p.screenshot(path=str(OUT/f'record-recovery-{width}.png'),full_page=True)

cases={'mixed-readonly-export-repair':mixed,'broken-json-preserved-before-restart':lambda p:reset_bad(p,'{broken'),'wrong-root-preserved-before-restart':lambda p:reset_bad(p,'{"records":[]}'),'duplicate-id-preserves-first-and-raw':duplicate,'nested-tags-comments-salvage':nested,'archive-quota-leaves-original-untouched':archive_failure,'concurrent-change-does-not-overwrite':race,'healthy-data-no-recovery-or-write':healthy,'concurrent-change-during-backup':backup_race,'replacement-quota-retains-original-and-copy':replacement_failure,'dirty-editor-keeps-input-after-repair':dirty_editor}
cases['recheck-refreshes-externally-repaired-list']=retry_external
for page in ['m03-p02','m03-p10','m04-p05','m06-p04']:cases['reader-'+page]=lambda p,page=page:reader(p,page)
for width in [320,360,390,414,430]:cases['recovery-layout-'+str(width)]=lambda p,width=width:layout(p,width)
if '--backup-race-only' in sys.argv:cases={'concurrent-change-during-backup':backup_race}
if '--dirty-only' in sys.argv:cases={'dirty-editor-keeps-input-after-repair':dirty_editor}
rows=[];hashes=source()
with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,run in cases.items():
        c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p);assert not errors,errors;row={'case':name,'passed':True}
        except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-2400:]}
        row.update(errors=errors,effective=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
    b.close()
name='record-recovery-backup-race-results.json' if '--backup-race-only' in sys.argv else 'record-recovery-dirty-results.json' if '--dirty-only' in sys.argv else 'record-recovery-results.json'
(OUT/name).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
assert hashes==source(),'Source changed during recovery verification'
if '--baseline' not in sys.argv:(OUT/'record-recovery-source.json').write_text(json.dumps({'files':hashes,'checks':len(rows),'passed':sum(r['passed'] for r in rows),'accepted_pages':0},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
