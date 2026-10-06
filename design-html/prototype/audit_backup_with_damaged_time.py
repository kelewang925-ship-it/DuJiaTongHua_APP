"""Diagnostic only: does a damaged source replace the last complete shared backup?"""
import json,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
files=source();rows=[];KEY='dujia-prototype-moments';BACKUP='dujia-prototype-backup'
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for mode in ['manual','automatic']:
  c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:
   d=data(True);d['dujia-prototype-session']=dict(loggedIn=True,phone='13812345678');d['dujia-prototype-preferences']=dict(autoBackup=mode=='automatic',reduceMotion=True)
   p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));}',d);p.goto(BASE+'pages/m06-p11.html');p.evaluate('()=>{localStorage.setItem("dujia-prototype-backup",JSON.stringify(PrototypePreferences.snapshot(true)));}');before=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-backup"))');p.evaluate('()=>localStorage.setItem("dujia-prototype-moments","{broken")')
   p.goto(BASE+'pages/'+('m06-p11.html'if mode=='manual'else'm03-p05.html'));expect(p.get_by_role('dialog',name='时刻需要恢复',exact=True)).to_be_visible();p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
   if mode=='manual':p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('备份已创建')
   else:p.locator('[name=title]').fill('受损集合旁的新日记');p.locator('[name=body]').fill('这个内容保存本身应当成功');p.locator('.submit').click();p.wait_for_url('**/m03-p06.html')
   after=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-backup"))');row=dict(before_moments=len(before['moments']),after_moments=len(after['moments']),complete_backup_replaced=bool(before['moments'])and not after['moments'],damaged_original_preserved=p.evaluate('localStorage.getItem("dujia-prototype-moments")')=='{broken',effective=p.url)
  except Exception:row=dict(failure=traceback.format_exc()[-2000:])
  row.update(mode=mode,errors=errors);rows.append(row);print('OBS '+mode+' '+json.dumps(row,ensure_ascii=False),flush=True);c.close()
 b.close()
assert files==source();(ROOT/'evidence/current/backup-damaged-time-observations.json').write_text(json.dumps(dict(files=files,scope='Diagnostic observations only; expected bad-backup outcomes are not passing acceptance checks',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
