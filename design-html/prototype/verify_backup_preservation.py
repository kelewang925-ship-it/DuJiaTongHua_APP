"""Actual manual backup and diary-save auto backup with damaged shared sources."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
files=source();rows=[];out=ROOT/'evidence'/('baseline'if '--baseline'in sys.argv else'current')
damage={'moments':'{broken','anniversaries':'{broken','capsules':'{broken','works':'{broken','records':'{broken','tags':'{broken','pet':'{broken','books':'{broken'}
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for kind,raw in damage.items():
  for mode in ['manual','automatic']:
   if mode=='automatic'and kind=='records':continue
   c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));key='dujia-prototype-'+kind
   try:
    d=data(True);d['dujia-prototype-session']=dict(loggedIn=True,phone='13812345678');d['dujia-prototype-preferences']=dict(autoBackup=mode=='automatic',reduceMotion=True)
    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));}',d);p.goto(BASE+'pages/m06-p11.html');p.evaluate('localStorage.setItem("dujia-prototype-backup",JSON.stringify(PrototypePreferences.snapshot(true)))');before=p.evaluate('localStorage.getItem("dujia-prototype-backup")');p.evaluate('([k,v])=>localStorage.setItem(k,v)',[key,raw]);p.goto(BASE+'pages/'+('m06-p11.html'if mode=='manual'else'm03-p05.html'))
    if p.locator('dialog[open]').count():p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
    if mode=='manual':p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('备份未更新');expect(p.locator('[data-backup-status]')).to_contain_text('恢复')
    else:
     p.locator('[name=title]').fill('备份受保护的新日记');p.locator('[name=body]').fill('其他损坏集合不妨碍这篇日记保存');p.locator('.submit').click();p.wait_for_url('**/m03-p06.html');assert any(v['title']=='备份受保护的新日记'for v in p.evaluate('PrototypeRecords.all()'))
    assert p.evaluate('localStorage.getItem("dujia-prototype-backup")')==before,'last complete backup changed'
    assert p.evaluate('(k)=>localStorage.getItem(k)',key)==raw,'damaged source changed'
    row=dict(passed=True,backup_preserved=True,original_preserved=True)
   except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
   row.update(case=kind+'-'+mode,errors=errors);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+row['case'],flush=True);c.close()
 b.close()
assert files==source();out.mkdir(parents=True,exist_ok=True);(out/'backup-preservation-results.json').write_text(json.dumps(dict(files=files,scope='15 actual damaged-source manual or auto backup paths; full acceptance pending',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['passed']and not v['errors']for v in rows)else 1)
