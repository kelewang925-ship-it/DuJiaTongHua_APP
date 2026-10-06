"""Diagnostic: declared private/draft sources in actual shared backups."""
import json
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
files=source();rows=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for mode in ['manual','automatic']:
  c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  d=data(True);d['dujia-prototype-session']=dict(loggedIn=True,phone='13812345678');d['dujia-prototype-preferences']=dict(autoBackup=mode=='automatic',reduceMotion=True);d['dujia-prototype-moments'] += [dict(id='private-scope',name='仅自己可见的时刻',story='PRIVATE-MOMENT-MARKER',visibility='private'),dict(id='draft-scope',name='尚未发布的时刻',story='DRAFT-MOMENT-MARKER',status='draft')];d['dujia-prototype-anniversaries'].append(dict(id='private-anniversary',name='PRIVATE-ANNIVERSARY-MARKER',date='2026-12-24',visibility='private'));d['dujia-prototype-capsules'].append(dict(id='private-capsule',name='PRIVATE-CAPSULE-MARKER',message='自己的文字',opening='2026-01-01',visibility='private',status='opened'))
  p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d);p.goto(BASE+'pages/'+('m06-p11.html'if mode=='manual'else'm03-p05.html'))
  if mode=='manual':p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('备份已创建')
  else:p.locator('[name=title]').fill('自动备份范围观察');p.locator('[name=body]').fill('实际保存触发自动备份');p.locator('.submit').click();p.wait_for_url('**/m03-p06.html')
  value=p.evaluate('localStorage.getItem("dujia-prototype-backup")');accessible=p.evaluate('JSON.stringify(PrototypePreferences.snapshot())');rows.append(dict(mode=mode,private_moment_in_shared_backup='PRIVATE-MOMENT-MARKER'in value,draft_moment_in_shared_backup='DRAFT-MOMENT-MARKER'in value,private_anniversary_in_shared_backup='PRIVATE-ANNIVERSARY-MARKER'in value,private_capsule_in_shared_backup='PRIVATE-CAPSULE-MARKER'in value,accessible_content_retained=all(marker in accessible for marker in ['PRIVATE-MOMENT-MARKER','DRAFT-MOMENT-MARKER','PRIVATE-ANNIVERSARY-MARKER','PRIVATE-CAPSULE-MARKER']),scope=json.loads(value)['scope'],errors=errors));c.close()
 b.close()
assert files==source();(ROOT/'evidence/current/backup-scope-observations.json').write_text(json.dumps(dict(files=files,scope='Seeded privacy/draft conditions with actual manual/auto operation; diagnostic only',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(rows,ensure_ascii=False))
