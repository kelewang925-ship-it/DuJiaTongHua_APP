"""User-facing original recovery copies remain downloadable without rewriting records."""
from pathlib import Path
import hashlib,json,sys,traceback
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;BASE='http://127.0.0.1:8765/';PREFIX='dujia-prototype-record-recovery-'
OUT=ROOT/'evidence'/('baseline' if '--baseline' in sys.argv else 'current')
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
def seed(p,copies):
    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();localStorage.setItem("dujia-prototype-records","[]");for(const[k,v]of Object.entries(d))localStorage.setItem(k,v)}',copies);p.goto(BASE+'pages/m06-p11.html')
def storage(p):return p.evaluate('JSON.stringify({...localStorage})')
def open_history(p):
    p.locator('.manage').click();p.get_by_role('dialog').get_by_role('button',name='查看恢复原始副本',exact=True).click();expect(p.locator('dialog h2')).to_have_text('恢复原始副本')
def download(p,name):
    with p.expect_download() as info:p.get_by_role('dialog').get_by_role('button',name='下载原始副本',exact=True).click()
    return Path(info.value.path()).read_text(encoding='utf-8')
def empty(p):
    seed(p,{});before=storage(p);open_history(p);expect(p.get_by_role('dialog')).to_contain_text('还没有恢复副本');p.get_by_role('dialog').get_by_role('button',name='关闭',exact=True).click();assert storage(p)==before
def multiple(p):
    values={'a':'{坏JSON','b':'[{"private":"私密原始内容"}]'};seed(p,{PREFIX+k:json.dumps(v,ensure_ascii=False) for k,v in values.items()});before=storage(p)
    for i,key in enumerate(['a','b'],1):
        open_history(p);p.get_by_role('button',name='原始副本 '+str(i),exact=True).click();assert download(p,key)==values[key];expect(p.locator('dialog')).to_have_count(0)
    assert storage(p)==before
def wrapper(p):
    raw='broken archive wrapper';seed(p,{PREFIX+'a':raw});before=storage(p);open_history(p);p.get_by_role('button',name='原始副本 1',exact=True).click();expect(p.get_by_role('dialog')).to_contain_text('副本格式无法解析');assert download(p,'a')==raw;assert storage(p)==before
def stale(p):
    seed(p,{PREFIX+'a':json.dumps('{old')});open_history(p);p.evaluate('localStorage.removeItem("dujia-prototype-record-recovery-a")');p.get_by_role('button',name='原始副本 1',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('副本已不存在');expect(p.locator('dialog h2')).to_have_text('恢复原始副本');expect(p.get_by_role('dialog')).to_contain_text('还没有恢复副本')
def changed(p):
    seed(p,{PREFIX+'a':json.dumps('{old')});open_history(p);p.evaluate('localStorage.setItem("dujia-prototype-record-recovery-a",JSON.stringify("{最新原始内容"))');p.get_by_role('button',name='原始副本 1',exact=True).click();assert download(p,'a')=='{最新原始内容'
def cancel(p):
    seed(p,{PREFIX+'a':json.dumps('{raw')});before=storage(p);open_history(p);p.get_by_role('button',name='原始副本 1',exact=True).click();p.get_by_role('dialog').get_by_role('button',name='关闭',exact=True).click();expect(p.locator('dialog')).to_have_count(0);open_history(p);p.go_back();expect(p.locator('dialog')).to_have_count(0);assert p.url.endswith('m06-p11.html') and storage(p)==before
def cache(p):
    seed(p,{PREFIX+'a':json.dumps('{raw')});before=storage(p);p.locator('#cache').click();p.get_by_role('button',name='确认清理',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('已清理');assert storage(p)==before;open_history(p);p.get_by_role('button',name='原始副本 1',exact=True).click();assert download(p,'a')=='{raw'
def actual_repair(p):
    seed(p,{});raw='{修复前无法解析的原文';p.evaluate('(v)=>localStorage.setItem("dujia-prototype-records",v)',raw);p.goto(BASE+'pages/m03-p06.html')
    p.get_by_role('dialog').get_by_role('button',name='恢复可读记录',exact=True).click();p.get_by_role('dialog').get_by_role('button',name='确认恢复',exact=True).click();p.wait_for_function('localStorage.getItem("dujia-prototype-records")==="[]"');p.goto(BASE+'pages/m06-p11.html');before=storage(p);open_history(p);p.get_by_role('button',name='原始副本 1',exact=True).click();assert download(p,'a')==raw and storage(p)==before
def account_delete(p):
    seed(p,{PREFIX+'a':json.dumps('{私人原文')});p.goto(BASE+'pages/m06-p08.html');p.locator('.delete').click();p.get_by_role('button',name='继续身份确认',exact=True).click();p.get_by_role('textbox',name='演示验证码 284631',exact=True).fill('284631');p.get_by_role('button',name='注销演示账号',exact=True).click();p.wait_for_url('**/m01-p01.html');assert p.evaluate('Object.keys(localStorage).filter(k=>k.startsWith("dujia-prototype-record-recovery-")).length')==0
def private_export(p):
    raw='{仅供本地恢复的私人原文';seed(p,{PREFIX+'a':json.dumps(raw,ensure_ascii=False)})
    with p.expect_download() as info:p.locator('#export').click()
    exported=Path(info.value.path()).read_text(encoding='utf-8');assert raw not in exported and 'record-recovery-' not in exported
    p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('共同记录备份已创建')
    assert raw not in p.evaluate('localStorage.getItem("dujia-prototype-backup")') and p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-record-recovery-a"))')==raw
def layout(p,width):
    p.set_viewport_size({'width':width,'height':844});seed(p,{PREFIX+str(i):json.dumps('{raw') for i in range(18)});open_history(p)
    p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
    for b in p.get_by_role('dialog').get_by_role('button').all():
        b.scroll_into_view_if_needed();box=b.bounding_box();assert box['width']>=44 and box['height']>=44
        assert b.evaluate('(e)=>{const r=e.getBoundingClientRect(),h=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return e===h||e.contains(h)}')
    assert p.evaluate('document.documentElement.scrollWidth')<=width
    p.get_by_role('button',name='原始副本 18',exact=True).click();expect(p.get_by_role('button',name='下载原始副本',exact=True)).to_be_visible();p.screenshot(path=str(OUT/f'recovery-archive-{width}.png'),full_page=True)
cases={'empty-history':empty,'multiple-original-downloads':multiple,'damaged-archive-wrapper':wrapper,'removed-after-list':stale,'changed-after-list':changed,'cancel-and-native-back':cancel,'cache-keeps-original-copies':cache,'actual-repair-then-download':actual_repair,'account-delete-removes-private-copies':account_delete}
cases['normal-export-and-shared-backup-exclude-original-copies']=private_export
for width in [320,360,390,414,430]:cases['archive-layout-'+str(width)]=lambda p,width=width:layout(p,width)
rows=[];hashes=source()
with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,run in cases.items():
        c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p);assert not errors,errors;row={'case':name,'passed':True}
        except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-2000:]}
        row.update(errors=errors,effective=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
    b.close()
assert hashes==source()
(OUT/'recovery-archive-results.json').write_text(json.dumps({'files':hashes,'results':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(row['passed'] for row in rows) else 1)
