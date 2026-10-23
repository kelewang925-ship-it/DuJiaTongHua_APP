"""Real common-profile controls with a second private tab changing local state during asynchronous work."""
import argparse,copy,hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_image_read_order import GATE,A,B,uri,finish
from verify_submission_changes import HOLD
from verify_overlay_form_saves import storage

KEY='dujia-prototype-relationship';NAME='本次共同昵称'
AVATAR=['unchanged','profile-merge','pending-merge','unbound','deleted','pair-replaced','avatar-conflict','avatar-cleared','privacy-closed','logout','session-switch','corrupt','pair-before-selection','session-before-selection','unbound-before-open','privacy-before-open','quota-retry']
NICK=['unchanged','avatar-merge','nickname-conflict','unbound','privacy-closed','session-switch']
UNLINK=['unchanged','profile-merge','pair-replaced','unbound','pending-existing','privacy-closed','session-switch']
ALLOW_AVATAR={'unchanged','profile-merge','pending-merge','quota-retry'};ALLOW_NICK={'unchanged','avatar-merge'};ALLOW_UNLINK={'unchanged','profile-merge','privacy-closed'}
MUTATE="""arg=>{const key='dujia-prototype-relationship',mode=arg.mode;let p=JSON.parse(localStorage.getItem(key)||'null');const save=()=>localStorage.setItem(key,JSON.stringify(p));if(mode==='unchanged'||mode==='quota-retry')return;if(mode==='deleted'){localStorage.removeItem(key);return}if(mode==='corrupt'){localStorage.setItem(key,'{"broken":');return}if(['privacy-closed','privacy-before-open'].includes(mode)){localStorage.setItem('dujia-privacy',JSON.stringify({...JSON.parse(localStorage.getItem('dujia-privacy')||'{}'),space:false}));return}if(mode==='logout'||['session-switch','session-before-selection'].includes(mode)){const s=JSON.parse(localStorage.getItem('dujia-prototype-session')||'{}');localStorage.setItem('dujia-prototype-session',JSON.stringify({...s,...(mode==='logout'?{loggedIn:false}:{loggedIn:true,phone:'13987654321'})}));return}if(['unbound','unbound-before-open'].includes(mode)){p.bound=false;p.unlinkedAt=1792771200000}else if(['pair-replaced','pair-before-selection'].includes(mode)){p={id:'pair-new',bound:true,partner:'新伙伴',acceptedAt:1792771200000,profile:{nickname:'新世界',avatar:null}}}else if(mode==='profile-merge'){p.profile={...p.profile,nickname:'外部共同昵称',met:'2026-02-02',saying:'保留外部资料'};p.externalNote='keep'}else if(['pending-merge','pending-existing'].includes(mode)){p.unlinkPending={id:'external-request',createdAt:1792771200000};p.externalNote='keep'}else if(['avatar-conflict','avatar-merge'].includes(mode)){p.profile={...p.profile,avatar:arg.image}}else if(mode==='avatar-cleared'){p.profile={...p.profile,avatar:null}}else if(mode==='nickname-conflict'){p.profile={...p.profile,nickname:'外部共同昵称'}}else throw Error(mode);save()}"""

def pair(p):return p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-relationship"))')
def watch(p,quota=False):p.evaluate("quota=>{const set=Storage.prototype.setItem;window.__worldWrites=0;window.__worldAttempts=0;Storage.prototype.setItem=function(k,v){if(this===localStorage&&k==='dujia-prototype-relationship'){window.__worldAttempts++;if(quota&&window.__worldAttempts===1)throw new DOMException('Injected quota failure','QuotaExceededError');window.__worldWrites++}return set.call(this,k,v)}}",quota)
def mutate(other,mode):other.evaluate(MUTATE,dict(mode=mode,image=uri(B)))
def choose_avatar(p,data=A):
 with p.expect_file_chooser() as info:p.locator('.portrait').click()
 info.value.set_files(dict(name='world.svg',mimeType='image/svg+xml',buffer=data))

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');parser.add_argument('--only');args=parser.parse_args();cases=[('avatar',n) for n in AVATAR]+[('nickname',n) for n in NICK]+[('unlink',n) for n in UNLINK]+[('status','unbound')]
 if args.only:cases=[v for v in cases if '/'.join(v) in args.only.split(',')]
 out=ROOT/('evidence/baseline/world-write-context' if args.baseline else 'evidence/current/world-write-context');out.mkdir(parents=True,exist_ok=True);files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')};fixture=declarations('verify_settings_controls.py');rows=[]
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for kind,mode in cases:
   c=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(kind=kind,mode=mode)
   try:
    fixture['seed'](p,'m06-p03');other=c.new_page();other.goto(BASE+'prototype/review.html')
    if mode=='avatar-cleared':other.evaluate("image=>{const k='dujia-prototype-relationship',v=JSON.parse(localStorage.getItem(k));v.profile.avatar=image;localStorage.setItem(k,JSON.stringify(v))}",uri(B));p.reload()
    watch(p,mode=='quota-retry');p.evaluate(GATE);p.evaluate(HOLD);before=storage(p)
    if kind=='avatar' and mode.endswith('before-open'):
     mutate(other,mode);changed=storage(p);opened=[];p.on('filechooser',lambda e:opened.append(e));p.locator('.portrait').click();dialog=p.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text('还没有关联另一半' if mode=='unbound-before-open' else '共同空间已关闭');assert not opened;dialog.get_by_role('button',name='取消',exact=True).click();assert storage(p)==changed;row['entry_rechecked']=True
    elif kind=='avatar':
     with p.expect_file_chooser() as info:p.locator('.portrait').click()
     if mode.endswith('before-selection'):mutate(other,mode)
     info.value.set_files(dict(name='world.svg',mimeType='image/svg+xml',buffer=A));assert p.evaluate('window.__imageJobs.length')==1
     if not mode.endswith('before-selection'):mutate(other,mode)
     changed=storage(p);latest=pair(p) if mode!='corrupt' else None;finish(p,0,A)
     if mode=='quota-retry':
      assert storage(p)==changed;expect(p.locator('.prototype-toast')).to_contain_text('空间不足');choose_avatar(p,B);finish(p,1,B)
     if mode in ALLOW_AVATAR:
      expected=copy.deepcopy(latest);expected['profile']={**expected.get('profile',{}),'avatar':uri(B) if mode=='quota-retry' else uri(A)};assert pair(p)==expected,'Avatar overwrote a concurrent field';assert p.evaluate('window.__worldWrites')==1;row['merged_current_data']=True
      expect(p.locator('.portrait')).to_contain_text('已设置')
     else:
      row['unchanged_after_rejected_avatar']=storage(p)==changed;assert row['unchanged_after_rejected_avatar'],'Stale avatar callback changed external state';assert p.evaluate('window.__worldWrites')==0;expect(p.locator('.prototype-toast[role=alert]')).to_be_visible()
      if mode=='avatar-cleared':expect(p.locator('.portrait')).not_to_contain_text('已设置')
     saved=storage(p);p.reload();assert storage(p)==saved
    elif kind=='nickname':
     p.locator('.nick').click();dialog=p.locator('dialog[open]');field=dialog.get_by_label('共同昵称',exact=True);field.fill(NAME);mutate(other,mode);changed=storage(p);latest=pair(p);submit=dialog.locator('[type=submit]');submit.click();p.evaluate('window.__releaseSubmissionTimers()');p.wait_for_function('!document.querySelector("dialog [aria-busy=true]")')
     if mode in ALLOW_NICK:
      expect(dialog).to_have_count(0);expected=copy.deepcopy(latest);expected['profile']={**expected.get('profile',{}),'nickname':NAME};assert pair(p)==expected,'Nickname overwrote a concurrent field';assert p.evaluate('window.__worldWrites')==1;row['merged_current_data']=True
     else:
      assert storage(p)==changed,'Stale nickname save changed external state';expect(field).to_have_value(NAME);expect(submit).to_be_enabled();dialog.get_by_role('button',name='取消',exact=True).click();expect(dialog.locator('.prototype-sheet-discard')).to_be_visible();dialog.get_by_role('button',name='继续编辑',exact=True).click();expect(field).to_have_value(NAME);dialog.get_by_role('button',name='取消',exact=True).click();dialog.get_by_role('button',name='放弃修改',exact=True).click();expect(dialog).to_have_count(0);assert storage(p)==changed;assert p.evaluate('window.__worldWrites')==0;row['input_and_external_state_preserved']=True
     saved=storage(p);p.reload();assert storage(p)==saved
    elif kind=='unlink':
     p.locator('.unlink').click();dialog=p.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text('请求解除关联？');mutate(other,mode);changed=storage(p);latest=pair(p);dialog.get_by_role('button',name='请求解除关联',exact=True).click();expect(dialog).to_have_count(0);p.evaluate('window.__releaseSubmissionTimers()');p.wait_for_function('!document.querySelector(".unlink[aria-busy=true]")')
     if mode in ALLOW_UNLINK:
      actual=pair(p);request=actual.pop('unlinkPending',None);expected=copy.deepcopy(latest);expected.pop('unlinkPending',None);assert actual==expected and request and request['id'];assert p.evaluate('window.__worldWrites')==1;row['merged_current_data']=True
     else:
      assert storage(p)==changed,'Stale unlink changed external state';assert p.evaluate('window.__worldWrites')==0;row['unlink_rejected_without_write']=True
     saved=storage(p);p.reload();assert storage(p)==saved
    else:
     mutate(other,mode);changed=storage(p);p.locator('.connection').click();dialog=p.locator('dialog[open]');expect(dialog).to_contain_text('当前未关联另一半');dialog.get_by_role('button',name='知道了',exact=True).click();assert storage(p)==changed;row['read_current_status']=True
    assert not errors,errors;row['passed']=True
   except Exception:row.update(passed=False,failure=traceback.format_exc()[-2400:])
   row['errors']=errors;rows.append(row);c.close();assert source()==files
   (out/'results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,scope='Actual common-avatar/nickname/unlink/status controls; native image I/O held, another private same-origin tab mutates mock WebStorage; real commit and reload verified',accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+mode,flush=True)
  browser.close()
 print(json.dumps(dict(cases=len(rows),passed=sum(v['passed'] for v in rows))))
 raise SystemExit(0 if all(v['passed'] for v in rows) else 1)

if __name__=='__main__':main()
