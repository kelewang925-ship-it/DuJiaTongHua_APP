"""Diagnostic next-action evidence: real creation against damaged roots."""
import json,traceback
from playwright.sync_api import sync_playwright
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
files=source();rows=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for kind in ['pet','books']:
  for variant in ['broken-json','wrong-root']:
   c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));key='dujia-prototype-'+kind;raw='{broken'if variant=='broken-json'else'[]'if kind=='pet'else'{}'
   try:
    d=data(True);d['dujia-prototype-session']=dict(loggedIn=True,phone='13812345678');d['dujia-prototype-preferences']=dict(autoBackup=False,reduceMotion=True)
    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d);p.evaluate('([k,v])=>localStorage.setItem(k,v)',[key,raw]);p.goto(BASE+'pages/'+('m07-p02.html'if kind=='pet'else'm08-p04.html'))
    if kind=='pet':p.locator('#pet-name').fill('新领养观察');p.locator('#invite').click();p.wait_for_url('**/m07-p01.html*')
    else:p.get_by_label('书名',exact=True).fill('新回忆册观察');p.get_by_label('开始月份',exact=True).fill('2026.10');p.get_by_label('结束月份',exact=True).fill('2026.10');p.get_by_role('button',name='空白回忆册',exact=True).click();p.locator('.next').click();p.wait_for_url('**/m08-p05.html*')
    row=dict(raw_preserved=p.evaluate('(k)=>localStorage.getItem(k)',key)==raw,effective=p.url)
   except Exception:row=dict(failure=traceback.format_exc()[-1800:])
   row.update(kind=kind,variant=variant,errors=errors);rows.append(row);print(row,flush=True);c.close()
 b.close()
assert source()==files;(ROOT/'evidence/current/pet-book-root-write-observations.json').write_text(json.dumps(dict(files=files,scope='Four seeded root conditions with actual create actions; diagnostic only, not acceptance',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
