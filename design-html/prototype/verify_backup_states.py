"""Backup retries, honest save result, concurrency and visible status."""
import json,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
files=source();rows=[];KEY='dujia-prototype-backup'
def seed(p,empty=False,auto=False):
 d=data(not empty);d['dujia-prototype-session']=dict(loggedIn=True,phone='13812345678');d['dujia-prototype-preferences']=dict(autoBackup=auto,reduceMotion=True)
 p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));}',d);p.goto(BASE+'pages/m06-p11.html');p.evaluate('localStorage.setItem("dujia-prototype-backup",JSON.stringify(PrototypePreferences.snapshot(true)))');return p.evaluate('localStorage.getItem("dujia-prototype-backup")')
def stored(p):return p.evaluate('localStorage.getItem("dujia-prototype-backup")')
def healthy(p):
 seed(p);p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('备份已创建');v=json.loads(stored(p));assert len(v['moments'])==1 and v['books'] and v['pet'];assert v['scope']=='shared'
def empty(p,absent=False):
 seed(p,True)
 if absent:p.evaluate('()=>{for(const k of ["records","moments","anniversaries","capsules","works","books","pet","tags"])localStorage.removeItem("dujia-prototype-"+k)}')
 p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('备份已创建');v=json.loads(stored(p));assert not v['records']and not v['books']and v['pet']is None
def quota(p,auto=False):
 before=seed(p,auto=auto);p.evaluate('()=>{const real=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==="dujia-prototype-backup")throw new DOMException("full","QuotaExceededError");return real.call(this,k,v)}}')
 if auto:assert p.evaluate('PrototypeUI.write("dujia-prototype-records",[...PrototypeRecords.all(),{id:"backup-save",type:"diary",title:"已保存正文",body:"可重试备份",visibility:"shared",status:"published",tags:[],comments:[]}])')is True;assert any(v['id']=='backup-save'for v in p.evaluate('PrototypeRecords.all()'))
 else:p.locator('#backup').click()
 expect(p.locator('.prototype-toast')).to_contain_text('备份未更新');assert stored(p)==before
def race(p,backup=False):
 before=seed(p);key='dujia-prototype-backup'if backup else'dujia-prototype-moments';new='external-new-backup'if backup else'[]'
 p.evaluate('([key,value])=>{const real=JSON.stringify;JSON.stringify=function(v,...args){if(v?.format==="dujia-prototype-backup-v1"){JSON.stringify=real;localStorage.setItem(key,value)}return real.call(this,v,...args)}}',[key,new]);p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('数据已在其他页面变化');assert stored(p)==(new if backup else before);assert p.evaluate('(k)=>localStorage.getItem(k)',key)==new
def unavailable(p):
 before=seed(p);p.evaluate('()=>{const real=Storage.prototype.getItem;window.restoreGet=()=>{Storage.prototype.getItem=real};Storage.prototype.getItem=function(k){if(k==="dujia-prototype-moments")throw new DOMException("blocked","SecurityError");return real.call(this,k)}}');assert p.evaluate('PrototypePreferences.backup()')is False;expect(p.locator('.prototype-toast')).to_contain_text('备份未更新');p.evaluate('()=>{restoreGet()}');assert stored(p)==before
def nested(p,key,patch):
 before=seed(p);p.evaluate('([key,patch])=>{let v=JSON.parse(localStorage.getItem(key));if(Array.isArray(v))v[0]={...v[0],...patch};else v={...v,...patch};localStorage.setItem(key,JSON.stringify(v))}',[key,patch]);raw=p.evaluate('(k)=>localStorage.getItem(k)',key);p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('备份未更新');assert stored(p)==before and p.evaluate('(k)=>localStorage.getItem(k)',key)==raw
def retry(p):
 before=seed(p);p.evaluate('localStorage.setItem("dujia-prototype-moments","{broken")');p.goto(BASE+'pages/m06-p11.html');p.get_by_role('button',name='稍后处理',exact=True).click();p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('备份未更新');assert stored(p)==before;p.get_by_role('button',name='恢复时刻',exact=True).click();p.get_by_role('button',name='恢复可读时刻',exact=True).click();p.get_by_role('button',name='确认恢复',exact=True).click();expect(p.locator('dialog')).to_have_count(0);p.wait_for_function('localStorage.getItem("dujia-prototype-moments")==="[]"');p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('备份已创建');assert not json.loads(stored(p))['moments'];assert p.evaluate('Object.keys(localStorage).some(k=>k.startsWith("dujia-prototype-moments-recovery-"))')
def layout(p,width):
 seed(p);p.evaluate('localStorage.setItem("dujia-prototype-moments","{broken")');p.goto(BASE+'pages/m06-p11.html');p.get_by_role('button',name='稍后处理',exact=True).click();p.locator('[data-backup-status]').scroll_into_view_if_needed();expect(p.locator('[data-backup-status]')).to_contain_text('恢复时刻');assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');p.locator('#backup').focus();p.keyboard.press('Enter');expect(p.locator('.prototype-toast')).to_contain_text('备份未更新');p.screenshot(path=str(ROOT/'evidence/current'/f'backup-paused-{width}.png'),full_page=True)
cases={'healthy-manual':healthy,'legitimate-empty':lambda p:empty(p),'absent-sources':lambda p:empty(p,True),'manual-quota':quota,'automatic-quota-save-still-success':lambda p:quota(p,True),'source-race':race,'backup-race':lambda p:race(p,True),'unavailable-storage':unavailable,'explicit-recovery-then-backup':retry,
 'pet-null-log':lambda p:nested(p,'dujia-prototype-pet',{'logs':[None]}),'pet-invalid-id':lambda p:nested(p,'dujia-prototype-pet',{'id':''}),'pet-unknown-status':lambda p:nested(p,'dujia-prototype-pet',{'status':'unknown'}),'book-null-page':lambda p:nested(p,'dujia-prototype-books',{'pages':[None]}),'book-unknown-status':lambda p:nested(p,'dujia-prototype-books',{'status':'unknown'}),'book-invalid-photos':lambda p:nested(p,'dujia-prototype-books',{'pages':[dict(id='p',photos={})]})}
cases.update({f'layout-{w}':lambda p,w=w:layout(p,w)for w in [320,360,390,414,430]})
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in cases.items():
  w=int(name.split('-')[-1])if name.startswith('layout-')else 390
  c=b.new_context(viewport=dict(width=w,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
  row.update(case=name,errors=errors);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert files==source();(ROOT/'evidence/current/backup-state-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed']and not r['errors']for r in rows)else 1)
