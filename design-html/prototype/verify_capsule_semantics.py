"""Actual sealed-date recovery and capsule-to-moment identity boundaries."""
import json,sys,traceback,copy
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import ROOT,BASE,source
from audit_current_runtime import data
files=source();out=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');out.mkdir(parents=True,exist_ok=True);rows=[]
CAP='dujia-prototype-capsules';MOM='dujia-prototype-moments'
def seed(p,opening='2026-02-30',status='sealed',moments=None,**extra):
 d=data(True);d['dujia-prototype-session']={'loggedIn':True};d['dujia-prototype-preferences']={'autoBackup':False,'reduceMotion':True}
 for k in ['moments','anniversaries','capsules','works','books']:d['dujia-prototype-'+k]=[]
 item=dict(id='semantic-cap',name='日期异常信',message='CAPSULE-SECRET-BODY',opening=opening,status=status,reminder=True,photo='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="3" height="3"><rect width="3" height="3" fill="purple"/></svg>',**extra)
 d[CAP]=[item];d[MOM]=moments or[];p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d);p.goto(BASE+'pages/'+('m04-p14'if status=='opened'else'm04-p15')+'.html?id=semantic-cap');return item

def values(p,k=CAP):return p.evaluate('k=>JSON.parse(localStorage.getItem(k))',k)
def unread(p):assert 'CAPSULE-SECRET-BODY'not in p.locator('body').inner_text();assert not p.locator('img[src*="purple"]').count();expect(p.get_by_role('button',name='打开这份心意',exact=True)).to_have_count(0)
def edit(p):p.get_by_role('button',name='修正开启日期',exact=True).click();return p.get_by_label('新的开启日期',exact=True)
def save(p):p.get_by_role('button',name='保存开启日期',exact=True).click()
def saved(p,original):
 expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.countdown')).to_contain_text('2');expect(p.locator('.screen.prototype-capsule-missing')).to_have_count(0);actual=values(p)[0];assert actual['status']=='sealed'and actual['opening']=='2026-10-08';assert {k:v for k,v in actual.items()if k not in ['opening','updatedAt']}=={k:v for k,v in original.items()if k not in ['opening','updatedAt']};unread(p)
def date_roundtrip(p,opening):
 original=seed(p,opening);unread(p);field=edit(p);expect(field).to_have_value('');save(p);expect(field).to_have_attribute('aria-invalid','true');assert values(p)[0]==original;field.fill('2026-10-05');save(p);expect(field).to_have_attribute('aria-invalid','true');field.fill('2026-10-08');save(p);saved(p,original);p.reload();unread(p);expect(p.locator('.countdown')).to_contain_text('2')
def cancel(p):
 original=seed(p);field=edit(p);field.fill('2026-10-08');p.keyboard.press('Escape');expect(p.locator('dialog')).to_contain_text('放弃');p.get_by_role('button',name='继续编辑',exact=True).click();expect(field).to_have_value('2026-10-08');p.keyboard.press('Escape');p.get_by_role('button',name='放弃修改',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert values(p)[0]==original;expect(p.get_by_role('button',name='修正开启日期',exact=True)).to_be_focused();unread(p)
def failure(p,quota=False):
 original=seed(p);field=edit(p);field.fill('2026-10-08')
 if quota:p.evaluate('()=>{window.originalDateWrite=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==="dujia-prototype-capsules")throw new DOMException("full","QuotaExceededError");return window.originalDateWrite.call(this,k,v)}}')
 else:p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","capsule-date")')
 save(p);expect(p.locator('.prototype-toast')).to_contain_text('不足'if quota else'重试');expect(field).to_have_value('2026-10-08');assert values(p)[0]==original
 if quota:p.evaluate('()=>{Storage.prototype.setItem=window.originalDateWrite}')
 save(p);saved(p,original)
def race(p,damage=False):
 original=seed(p);field=edit(p);field.fill('2026-10-08');raw='{broken'if damage else json.dumps([{**original,'message':'PEER-SECRET'}],ensure_ascii=False);p.evaluate('v=>localStorage.setItem("dujia-prototype-capsules",v)',raw);save(p);expect(p.locator('.prototype-toast')).to_contain_text('更新'if not damage else'恢复');expect(field).to_have_value('2026-10-08');assert p.evaluate('localStorage.getItem("dujia-prototype-capsules")')==raw;assert 'PEER-SECRET'not in p.locator('body').inner_text()
def collect(p,mode):
 foreign=dict(id='foreign',name='无关时刻',date='2026-10-06',story='FOREIGN-STORY',capsuleId='another',related=[],comments=[])
 kw={};existing=[]
 if mode=='foreign':kw['momentId']='foreign';existing=[foreign]
 if mode=='collision':foreign['id']='capsule-moment-semantic-cap';existing=[foreign]
 if mode=='private':kw['visibility']='private'
 item=seed(p,'2026-10-06','opened',moments=existing,**kw);p.locator('#collect').click();p.wait_for_url('**/m04-p03.html?id=*');expect(p.get_by_role('heading',name=item['name'],exact=True)).to_be_visible();moment=next(v for v in values(p,MOM)if v.get('capsuleId')==item['id']);assert moment['story']==item['message'][:200];assert values(p)[0]['momentId']==moment['id']
 if existing:assert next(v for v in values(p,MOM)if v['id']==foreign['id'])==foreign
 if mode=='private':assert moment['visibility']=='private'and not p.evaluate('PrototypePreferences.snapshot(true).moments.some(v=>v.capsuleId==="semantic-cap")')
 before=values(p,MOM);p.goto(BASE+'pages/m04-p14.html?id=semantic-cap');p.locator('#collect').click();p.wait_for_url('**/m04-p03.html?id=*');assert values(p,MOM)==before

def stale(p):
 seed(p,'2026-10-06','opened');p.evaluate('()=>{const v=JSON.parse(localStorage.getItem("dujia-prototype-capsules"));v[0].status="sealed";localStorage.setItem("dujia-prototype-capsules",JSON.stringify(v))}');before=values(p);p.locator('#collect').click();expect(p.locator('.prototype-toast')).to_contain_text('开启');assert values(p)==before and values(p,MOM)==[]
def layout(p,w):
 seed(p);p.evaluate('()=>{document.documentElement.style.setProperty("--ui-safe-top","44px");document.documentElement.style.setProperty("--ui-safe-bottom","34px")}');unread(p);field=edit(p);field.fill('2026-10-08');button=p.get_by_role('button',name='保存开启日期',exact=True);button.scroll_into_view_if_needed();b=button.bounding_box();assert b['height']>=44 and b['width']>=44;assert button.evaluate('e=>{const r=e.getBoundingClientRect();return e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))}');assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');box=p.locator('dialog').bounding_box();assert box['y']>=0 and box['y']+box['height']<=845;p.screenshot(path=str(out/f'capsule-date-sheet-{w}.png'),full_page=True);button.focus();p.keyboard.press('Enter');expect(p.locator('dialog')).to_have_count(0);unread(p)
cases={'invalid-calendar':lambda p:date_roundtrip(p,'2026-02-30'),'missing-date':lambda p:date_roundtrip(p,''),'dirty-cancel':cancel,'save-failure-retry':failure,'quota-retry':lambda p:failure(p,True),'date-race-preserves-peer':race,'damaged-source-refuses-date-write':lambda p:race(p,True),'collect-foreign-reference':lambda p:collect(p,'foreign'),'collect-id-collision':lambda p:collect(p,'collision'),'private-collect':lambda p:collect(p,'private'),'normal-idempotent-collect':lambda p:collect(p,'normal'),'stale-opened-now-sealed':stale}
for w in [320,360,390,414,430]:cases['layout-'+str(w)]=lambda p,w=w:layout(p,w)
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in cases.items():
  w=int(name.split('-')[-1])if name.startswith('layout-')else 390;c=b.new_context(viewport=dict(width=w,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1900:])
  row.update(case=name,errors=errors,width=w,safe_area_simulated=name.startswith('layout-'));rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert source()==files;(out/'capsule-semantic-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']and not r['errors']for r in rows)else 1)
