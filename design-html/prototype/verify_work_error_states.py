"""Editable work error states distinguish inaccessible data from an absent work."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from verify_workshop_recovery import seed,raw,prompt
from verify_pet_controls import ROOT,source,store
OUT=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');files=source();rows=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,360,390,414,430]:
  for page in ['m05-p03.html?id=missing-work','m05-p06.html?id=missing-work','m05-p08.html?id=missing-work']:
   for broken in [True,False]:
    c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
    try:
     original='{broken'if broken else'[]';seed(p,original,page)
     if broken:prompt(p);p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0);p.wait_for_function('!history.state?.prototypeOverlay')
     before=store(p);box=p.locator('.prototype-work-state');expect(box).to_be_visible();assert box.evaluate('e=>e.classList.contains("prototype-component-state")');expect(box.locator('h2')).to_have_text('作品数据需要恢复'if broken else'这件创作已经不在了');expect(box).to_have_attribute('data-kind','error'if broken else'empty');button=box.get_by_role('button',name='恢复作品'if broken else'返回我的创作',exact=True);r=button.bounding_box();assert r['width']>=44 and r['height']>=44 and r['x']>=0 and r['x']+r['width']<=width+.5;assert button.evaluate('b=>{const r=b.getBoundingClientRect(),e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return e===b||b.contains(e);}');assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');button.focus()
     if width==320:p.evaluate('document.fonts.ready');p.screenshot(path=str(OUT/f'work-error-{page[:7]}-{broken}-320.png'))
     p.keyboard.press('Enter')
     if broken:prompt(p);assert p.url.endswith(page);p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert store(p)==before
     else:p.wait_for_url('**/m05-p09.html');assert raw(p)=='[]'
     assert not errors;row=dict(passed=True)
    except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
    row.update(actual_title=p.locator('.prototype-work-state h2').first.text_content()if p.locator('.prototype-work-state h2').count()else None,page=page,width=width,broken=broken,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+page+' '+str(width)+' '+str(broken),flush=True);c.close()
 b.close()
assert files==source();(OUT/'work-error-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
