"""Error CTA rechecks a work repaired in another tab, then shows its actual state."""
import json,sys,time,traceback
from playwright.sync_api import sync_playwright,expect
from verify_workshop_recovery import seed,prompt,raw,KEY
from verify_pet_controls import ROOT,source
from audit_current_runtime import data
OUT=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');files=source();rows=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for n,status in [(3,'draft'),(6,'generating'),(8,'ready')]:
  c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:
   page=f'm05-p{n:02}.html?id=missing-work';seed(p,'{broken',page);prompt(p);p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0);p.wait_for_function('!history.state?.prototypeOverlay');work={**data(True)[KEY][0],'id':'missing-work','name':'另一处恢复的作品','story':'修复后的共同故事','status':status,'startedAt':int(time.time()*1000),'dueAt':int(time.time()*1000)+30000};value=json.dumps([work],ensure_ascii=False);p.evaluate('([k,v])=>localStorage.setItem(k,v)',[KEY,value]);p.locator('.prototype-work-state').get_by_role('button',name='恢复作品',exact=True).click();expect(p.locator('.prototype-work-state')).to_have_count(0)
   if n==3:expect(p.locator('#story')).to_have_value('修复后的共同故事')
   elif n==8:expect(p.locator('.title')).to_have_text(work['name'])
   else:expect(p.locator('.steps')).to_be_visible()
   assert p.url.endswith(page)and raw(p)==value and not errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1600:])
  row.update(page=n,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+str(n),flush=True);c.close()
 b.close()
assert files==source();(OUT/'work-error-refresh-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
