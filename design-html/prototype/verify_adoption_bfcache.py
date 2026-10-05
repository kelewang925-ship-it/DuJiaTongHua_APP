from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright
from verify_adoption_history import begin,unchanged
OUT=Path(__file__).resolve().parent/'evidence/current'
def run():
 row={}
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',ignore_default_args=['--disable-back-forward-cache'])
  c=b.new_context(viewport={'width':390,'height':844});c.add_init_script("addEventListener('pageshow',event=>{const key='test-adoption-pageshow';const events=JSON.parse(sessionStorage.getItem(key)||'[]');events.push({url:location.href,persisted:event.persisted,state:history.state,type:performance.getEntriesByType('navigation')[0]?.type});sessionStorage.setItem(key,JSON.stringify(events));});addEventListener('storage',event=>{const key='test-adoption-pageshow';const events=JSON.parse(sessionStorage.getItem(key)||'[]');events.push({url:location.href,kind:'storage',key:event.key});sessionStorage.setItem(key,JSON.stringify(events));})")
  p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:
   before=begin(p)
   for _ in range(3):p.go_back();p.wait_for_url('**/m03-p01.html');p.wait_for_timeout(500);unchanged(p,before)
   events=p.evaluate("JSON.parse(sessionStorage.getItem('test-adoption-pageshow')||'[]')");restores=[e for e in events if e.get('persisted')];assert not errors,errors
   row=dict(case='native-cache-restored-completed-adoption-history',passed=True,bfcache_observed=bool(restores),restores=restores,events=events,coverage='Native persisted pageshow observed' if restores else 'History flow passed; native BFCache restoration was not observed and remains unverified')
  except Exception:row=dict(case='native-cache-restored-completed-adoption-history',passed=False,failure=traceback.format_exc()[-1800:])
  row.update(errors=errors,url=p.url,observed_events=p.evaluate("JSON.parse(sessionStorage.getItem('test-adoption-pageshow')||'[]')"));c.close();b.close()
 return row
rows=[]
for trial in range(5):
 row=run();row['trial']=trial+1;rows.append(row);print('Trial '+str(trial+1)+': '+str(row['passed']),flush=True)
(OUT/'adoption-bfcache-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps([{'passed':r['passed'],'bfcache_observed':r.get('bfcache_observed'),'failure':r.get('failure')} for r in rows],ensure_ascii=False),flush=True)
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
