"""Five-width date/operation sheet and confirmation reachability."""
from pathlib import Path
import json,hashlib,traceback
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;OUT=ROOT/'evidence/current';BASE='http://127.0.0.1:8765/pages/'
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
files=source();rows=[]
with sync_playwright()as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for width in [320,360,390,414,430]:
        for page in ['m04-p09','m04-p13','m04-p10','m04-p14']:
            c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:
                p.goto(BASE+'m04-p12.html');p.evaluate('()=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-05");localStorage.setItem("dujia-prototype-anniversaries",JSON.stringify([{id:"layout",name:"纪念日",date:"2026-12-24",repeat:true,enabled:true,reminderDays:3}]));localStorage.setItem("dujia-prototype-capsules",JSON.stringify([{id:"layout",name:"信件",message:"祝福",opening:"2026-10-04",status:"opened",reminder:true}]))}')
                p.goto(BASE+page+'.html'+('?id=layout'if page in ['m04-p10','m04-p14']else''));p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")');before=p.evaluate('JSON.stringify({...localStorage})')
                if page in ['m04-p09','m04-p13']:
                    p.locator('[name=date]'if page=='m04-p09'else'[name=opening]').click();expect(p.locator('dialog input[type=date]')).to_be_visible();p.locator('dialog input').fill('2026-12-25')
                else:p.locator('#more').click();p.get_by_role('button',name='删除纪念日'if page=='m04-p10'else'删除胶囊',exact=True).click();expect(p.locator('dialog h2')).to_contain_text('删除')
                metrics=p.locator('dialog').evaluate('(d)=>{const r=d.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,buttons:[...d.querySelectorAll("button")].map(b=>{const r=b.getBoundingClientRect();return {name:b.textContent,width:r.width,height:r.height}})}}')
                assert metrics['x']>=0 and metrics['right']<=width+1 and metrics['y']>=0 and metrics['bottom']<=844+1,metrics
                assert all(v['height']>=44 for v in metrics['buttons']),metrics
                if width==320:p.screenshot(path=str(OUT/f'time-layout-{page}-{width}.png'),full_page=True)
                p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);assert p.evaluate('JSON.stringify({...localStorage})')==before;assert not errors;row=dict(passed=True,metrics=metrics)
            except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
            row.update(page=page,width=width,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+page+' '+str(width),flush=True);c.close()
    b.close()
assert files==source();(OUT/'time-layout-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed']for r in rows)else 1)
