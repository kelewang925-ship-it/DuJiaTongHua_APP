"""Five widths for source Sheet and unsaved editor confirmation."""
import json,traceback
from playwright.sync_api import sync_playwright,expect
from verify_workshop_controls import seed,store,source,ROOT
OUT=ROOT/'evidence/current';files=source();rows=[]
with sync_playwright()as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for width in [320,360,390,414,430]:
        for scenario in ['source-sheet','dirty-modal']:
            c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:
                seed(p,'m05-p04'if scenario=='source-sheet'else'm05-p03');before=store(p);p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
                if scenario=='source-sheet':p.get_by_role('button',name='选择照片',exact=True).click();expect(p.locator('dialog').get_by_label('共同素材照片',exact=True)).to_be_visible()
                else:p.locator('#story').fill('长'*300);p.locator('.back').click();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？')
                metrics=p.locator('dialog').evaluate('d=>{const r=d.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,buttons:[...d.querySelectorAll("button")].map(b=>b.getBoundingClientRect().height)}}');assert metrics['x']>=0 and metrics['right']<=width+1 and metrics['y']>=0 and metrics['bottom']<=845 and all(h>=44 for h in metrics['buttons']),metrics
                if width==320:p.screenshot(path=str(OUT/f'workshop-control-layout-{scenario}-320.png'),full_page=True)
                if scenario=='source-sheet':p.keyboard.press('Escape')
                else:p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('#story')).to_have_value('长'*300)
                expect(p.locator('dialog')).to_have_count(0);assert store(p)==before;assert not errors;row=dict(passed=True,metrics=metrics)
            except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
            row.update(width=width,scenario=scenario,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+scenario+' '+str(width),flush=True);c.close()
    b.close()
assert files==source();(OUT/'workshop-control-layout-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed']for r in rows)else 1)
