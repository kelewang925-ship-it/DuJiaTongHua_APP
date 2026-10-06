"""Five widths for pet reply Sheet and wardrobe unsaved confirmation."""
import json,traceback
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import ROOT,seed,store,source
OUT=ROOT/'evidence/current';files=source();rows=[]
with sync_playwright()as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for width in [320,360,390,414,430]:
        for kind in ['reply','outfit','blocked']:
            c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:
                seed(p,'m07-p19'if kind=='reply'else'm07-p17'if kind=='blocked'else'm07-p12');before=store(p);p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
                if kind=='blocked':
                    metrics=[]
                    for selector in ['.back','.return']:
                        button=p.locator(selector);button.scroll_into_view_if_needed();r=button.bounding_box();assert r['width']>=44 and r['height']>=40 and r['x']>=0 and r['x']+r['width']<=width+1 and r['y']>=0 and r['y']+r['height']<=845,r;metrics.append(r)
                    expect(p.locator('.return')).to_have_text('返回成长时间线')
                    if width==320:p.screenshot(path=str(OUT/'pet-control-layout-blocked-320.png'),full_page=True)
                    p.locator('.return').click();p.wait_for_url('**/m07-p18.html');assert store(p)==before;assert not errors;row=dict(passed=True,metrics=metrics)
                    row.update(width=width,kind=kind,errors=errors,effective=p.url);rows.append(row);print('PASS blocked '+str(width),flush=True);c.close();continue
                if kind=='reply':p.get_by_role('button',name='回应这一页',exact=True).click();p.get_by_role('textbox',name='回应内容',exact=True).fill('长'*300);p.keyboard.press('Escape')
                else:p.locator('[data-item=scarf]').click();p.locator('.back').click()
                expect(p.get_by_text('是否放弃当前修改？',exact=True)).to_be_visible();metrics=p.locator('dialog').evaluate('d=>{const rect=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height}};return {dialog:rect(d),buttons:[...d.querySelectorAll("button")].filter(b=>b.getClientRects().length).map(rect)}}');r=metrics['dialog'];assert r['x']>=0 and r['right']<=width+1 and r['y']>=0 and r['bottom']<=845 and all(v['height']>=44 and v['width']>=44 and v['x']>=0 and v['right']<=width+1 and v['y']>=0 and v['bottom']<=845 for v in metrics['buttons']),metrics
                if width==320:p.screenshot(path=str(OUT/f'pet-control-layout-{kind}-320.png'),full_page=True)
                p.get_by_role('button',name='继续编辑',exact=True).click()
                if kind=='reply':expect(p.get_by_role('textbox',name='回应内容',exact=True)).to_have_value('长'*300)
                else:expect(p.locator('[data-item=scarf]')).to_have_attribute('aria-pressed','true')
                assert store(p)==before;assert not errors;row=dict(passed=True,metrics=metrics)
            except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
            row.update(width=width,kind=kind,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+kind+' '+str(width),flush=True);c.close()
    b.close()
assert files==source();(OUT/'pet-control-layout-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed']for r in rows)else 1)
