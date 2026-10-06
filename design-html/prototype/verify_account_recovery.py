"""Typed local identity data must not crash pages or be silently replaced."""
from pathlib import Path
import hashlib,json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;BASE='http://127.0.0.1:8765/';PROFILE='dujia-profile';PAIR='dujia-prototype-relationship';PREFIX='dujia-prototype-account-recovery-'
OUT=ROOT/'evidence'/('baseline' if '--baseline' in sys.argv or '--layout-baseline' in sys.argv else 'current')
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
def seed(p,key,raw,page):
    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',data(True));p.evaluate('([k,v])=>localStorage.setItem(k,v)',[key,raw]);p.goto(BASE+'pages/'+page+'.html')
def stored(p,key):return p.evaluate('k=>localStorage.getItem(k)',key)
def copies(p):return p.evaluate('Object.keys(localStorage).filter(k=>k.startsWith("dujia-prototype-account-recovery-")).map(k=>JSON.parse(localStorage.getItem(k)))')
def prompt(p):expect(p.get_by_role('dialog',name='资料需要恢复',exact=True)).to_be_visible()
def repair(p):
    prompt(p);p.get_by_role('dialog').get_by_role('button',name='恢复可读资料',exact=True).click();expect(p.locator('dialog h2')).to_have_text('保留原始副本并恢复资料？');p.get_by_role('dialog').get_by_role('button',name='确认恢复',exact=True).click()
def damaged(p,key,raw,page):
    seed(p,key,raw,page);prompt(p);assert stored(p,key)==raw
    with p.expect_download() as info:p.get_by_role('dialog').get_by_role('button',name='导出原始资料',exact=True).click()
    assert Path(info.value.path()).read_text(encoding='utf-8')==raw;prompt(p);p.get_by_role('dialog').get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
    before=stored(p,'dujia-prototype-records');assert p.evaluate('PrototypeUI.write("dujia-prototype-records",[])') is False;assert stored(p,'dujia-prototype-records')==before and stored(p,key)==raw
    p.get_by_role('button',name='恢复资料',exact=True).click();repair(p);p.wait_for_function('([k,raw])=>localStorage.getItem(k)!==raw',arg=[key,raw]);assert copies(p)==[raw];assert isinstance(json.loads(stored(p,key)),dict);p.reload();expect(p.locator('dialog')).to_have_count(0)
def healthy(p):
    raw=json.dumps(data(True)[PROFILE],ensure_ascii=False);seed(p,PROFILE,raw,'m02-p05');expect(p.locator('.names .pink')).to_have_text(data(True)[PROFILE]['nickname']);expect(p.locator('dialog')).to_have_count(0);assert stored(p,PROFILE)==raw and not copies(p)
def nested(p):
    raw=json.dumps({'id':'stable-pair','bound':True,'partner':'阿舟','profile':{'nickname':'保留共同昵称','met':42,'anniversary':'每月 5 日'},'acceptedAt':1791100000000},ensure_ascii=False);seed(p,PAIR,raw,'m06-p03');repair(p);p.wait_for_function('JSON.parse(localStorage.getItem("dujia-prototype-relationship")).profile.met===undefined');value=json.loads(stored(p,PAIR));assert value['id']=='stable-pair' and value['bound'] is True and value['profile']['nickname']=='保留共同昵称' and copies(p)==[raw]
def quota(p,main=False):
    raw='null';seed(p,PROFILE,raw,'m02-p05');prompt(p)
    p.evaluate('main=>{const old=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(main?k==="dujia-profile":String(k).startsWith("dujia-prototype-account-recovery-"))throw new DOMException("full","QuotaExceededError");return old.call(this,k,v)};return true}',main)
    repair(p);expect(p.locator('.prototype-toast')).to_contain_text('未能保存');assert stored(p,PROFILE)==raw and copies(p)==([raw] if main else [])
def race(p):
    raw='null';seed(p,PROFILE,raw,'m02-p05');prompt(p);p.get_by_role('button',name='恢复可读资料',exact=True).click();fresh={'nickname':'另一页面新昵称'};p.evaluate('v=>localStorage.setItem("dujia-profile",JSON.stringify(v))',fresh);p.get_by_role('button',name='确认恢复',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('其他页面');assert json.loads(stored(p,PROFILE))==fresh and not copies(p)
def dirty(p):
    seed(p,PROFILE,json.dumps(data(True)[PROFILE],ensure_ascii=False),'m06-p02');p.locator('#nickname').fill('保留未保存昵称');raw=json.dumps({**data(True)[PROFILE],'aliases':{}},ensure_ascii=False);p.evaluate('v=>localStorage.setItem("dujia-profile",v)',raw);p.locator('#save').click();repair(p);expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('#nickname')).to_have_value('保留未保存昵称');assert copies(p)==[raw];p.locator('#save').click();p.wait_for_url('**/m06-p01.html');assert json.loads(stored(p,PROFILE))['nickname']=='保留未保存昵称'
def backup_race(p):
    seed(p,PROFILE,'null','m02-p05');prompt(p);fresh={'nickname':'备份期间保存的新昵称'}
    p.evaluate('fresh=>{const old=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){old.call(this,k,v);if(String(k).startsWith("dujia-prototype-account-recovery-"))old.call(this,"dujia-profile",JSON.stringify(fresh));};return true}',fresh)
    repair(p);expect(p.locator('.prototype-toast')).to_contain_text('其他页面');assert json.loads(stored(p,PROFILE))==fresh and copies(p)==['null']
def transaction(p):
    seed(p,PROFILE,'null','m02-p05');prompt(p);p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0);before=p.evaluate('JSON.stringify({...localStorage})')
    assert p.evaluate('PrototypePreferences.transaction([["dujia-prototype-tags",[]],["dujia-profile",{nickname:"不能覆盖"}]])') is False;assert p.evaluate('JSON.stringify({...localStorage})')==before
def invalid_write(p):
    raw=json.dumps(data(True)[PROFILE],ensure_ascii=False);seed(p,PROFILE,raw,'m06-p01');assert p.evaluate('PrototypeUI.write("dujia-profile",{nickname:{}})') is False;assert stored(p,PROFILE)==raw;expect(p.locator('dialog')).to_have_count(0)
def combined(p):
    seed(p,PROFILE,'null','m03-p06');prompt(p);p.evaluate('localStorage.setItem("dujia-prototype-records","{bad records");localStorage.setItem("dujia-prototype-relationship","null")')
    with p.expect_event('load'):repair(p)
    p.wait_for_function('localStorage.getItem("dujia-profile")==="{}"');prompt(p);expect(p.get_by_role('dialog')).to_contain_text('关系资料')
    with p.expect_event('load'):repair(p)
    assert stored(p,PAIR)=='{}' and copies(p)==['null','null'];assert stored(p,'dujia-prototype-records')=='{bad records'
    expect(p.locator('dialog h2')).to_have_text('记录需要恢复');p.get_by_role('button',name='恢复可读记录',exact=True).click()
    with p.expect_event('load'):p.get_by_role('button',name='确认恢复',exact=True).click()
    assert stored(p,'dujia-prototype-records')=='[]'
def archive_history(p):
    raw='{资料副本中的私人原文';seed(p,PROFILE,raw,'m02-p05');repair(p);p.wait_for_function('localStorage.getItem("dujia-profile")==="{}"');p.goto(BASE+'pages/m06-p11.html')
    with p.expect_download() as info:p.locator('#export').click()
    assert raw not in Path(info.value.path()).read_text(encoding='utf-8')
    p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('共同记录备份已创建');assert raw not in stored(p,'dujia-prototype-backup')
    p.locator('.manage').click();p.get_by_role('button',name='查看恢复原始副本',exact=True).click();p.get_by_role('button',name='原始副本 1',exact=True).click();expect(p.get_by_role('dialog')).to_contain_text('个人或关系资料原始内容')
    with p.expect_download() as info:p.get_by_role('button',name='下载原始副本',exact=True).click()
    assert Path(info.value.path()).read_text(encoding='utf-8')==raw and copies(p)==[raw]
def layout(p,width):
    p.set_viewport_size({'width':width,'height':844});seed(p,PROFILE,'null','m02-p05');prompt(p);p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
    for b in p.get_by_role('dialog').get_by_role('button').all():
        b.scroll_into_view_if_needed();box=b.bounding_box();assert box['width']>=44 and box['height']>=44
        assert b.evaluate('(e)=>{const r=e.getBoundingClientRect(),h=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return h===e||e.contains(h)}')
    assert p.evaluate('document.documentElement.scrollWidth')<=width;p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
    for b in p.locator('.primary,.secondary,.prototype-relationship-home button,.prototype-account-recovery').all():
        b.scroll_into_view_if_needed();assert b.evaluate('(e)=>{const r=e.getBoundingClientRect(),h=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return h===e||e.contains(h)}'),b.inner_text()
    b=p.get_by_role('button',name='恢复资料',exact=True);b.scroll_into_view_if_needed();box=b.bounding_box();assert box['height']>=44 and box['y']+box['height']<=844-34;p.screenshot(path=str(OUT/f'account-recovery-{width}.png'),full_page=True)
cases={}
for name,key,raw,page in [('profile-null',PROFILE,'null','m02-p05'),('pair-null',PAIR,'null','m06-p01'),('profile-broken-json',PROFILE,'{broken','m06-p02'),('pair-wrong-root',PAIR,'[]','m06-p03')]:cases[name]=lambda p,key=key,raw=raw,page=page:damaged(p,key,raw,page)
cases.update({'healthy-profile-unchanged':healthy,'nested-pair-keeps-readable-fields':nested,'archive-quota':lambda p:quota(p),'replacement-quota':lambda p:quota(p,True),'concurrent-change':race,'dirty-profile-form':dirty})
cases.update({'backup-race':backup_race,'transaction-blocks-all-writes':transaction,'invalid-proposed-profile-rejected':invalid_write,'multiple-corrupt-data-recovery-order':combined,'account-copy-download-from-history':archive_history})
for width in [320,360,390,414,430]:cases['account-recovery-layout-'+str(width)]=lambda p,width=width:layout(p,width)
if '--baseline' in sys.argv:cases={key:value for key,value in cases.items() if key in ['profile-null','pair-null','profile-broken-json','pair-wrong-root','healthy-profile-unchanged']}
if '--layout-baseline' in sys.argv:cases={key:value for key,value in cases.items() if key.startswith('account-recovery-layout-')}
rows=[];hashes=source()
with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,run in cases.items():
        c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p);assert not errors,errors;row={'case':name,'passed':True}
        except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-2200:]}
        row.update(errors=errors,effective=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
    b.close()
assert hashes==source()
(OUT/('account-recovery-layout-baseline.json' if '--layout-baseline' in sys.argv else 'account-recovery-results.json')).write_text(json.dumps({'files':hashes,'results':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(row['passed'] for row in rows) else 1)
