"""Repeat immediate Back after Keep Editing against the restored guard sentinel."""
from pathlib import Path
import json,hashlib,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;BASE='http://127.0.0.1:8765/'
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
files=source();rows=[]
with sync_playwright()as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for page,key in [('m03-p08','audit-diary'),('m03-p12','audit-photo')]:
        for turn in range(3):
            c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:
                p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',data(True));p.goto(BASE+'pages/'+page+'.html?id='+key);before=p.evaluate('JSON.stringify({...localStorage})');p.locator('#reply').fill('快速返回也要保留')
                for repeat in range(3):
                    p.go_back();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();p.go_back();expect(p.locator('#reply')).to_have_value('快速返回也要保留')
                    p.wait_for_function('()=>{const d=document.querySelector("dialog");return d?!d.classList.contains("prototype-closing"):history.state?.prototypeGuard===true&&!history.state?.prototypeOverlay}')
                    if p.locator('dialog').count():
                        expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click()
                    expect(p.locator('dialog')).to_have_count(0);p.wait_for_function('history.state?.prototypeGuard===true&&!history.state?.prototypeOverlay');expect(p.locator('#reply')).to_have_value('快速返回也要保留')
                p.go_back();p.get_by_role('button',name='放弃修改',exact=True).click();p.wait_for_url('**/'+('m03-p06'if page=='m03-p08'else'm03-p10')+'.html');assert p.evaluate('JSON.stringify({...localStorage})')==before;assert not errors;row={'case':page+'-reentry-'+str(turn),'passed':True}
            except Exception:row={'case':page+'-reentry-'+str(turn),'passed':False,'failure':traceback.format_exc()[-1800:]}
            row.update(errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+row['case'],flush=True);c.close()
    b.close()
assert files==source()
(ROOT/'evidence/current/record-back-reentry-results.json').write_text(json.dumps({'files':files,'results':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(r['passed']for r in rows)else 1)
