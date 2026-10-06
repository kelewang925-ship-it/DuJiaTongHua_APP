"""Book editor and rename dirty confirmations at five phone widths."""
import json,traceback
from playwright.sync_api import sync_playwright,expect
from verify_book_controls import ROOT,seed,store,source,OUT
files=source();rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,360,390,414,430]:
  for kind in ['supplement','editor','rename']:
   c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   try:
    seed(p,'m08-p19' if kind=='supplement' else 'm08-p09' if kind=='editor' else 'm08-p21');before=store(p);p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
    if kind=='rename':p.locator('.rename').click();target=p.get_by_role('textbox',name='回忆册名称',exact=True);target.fill('长'*20);p.keyboard.press('Escape')
    else:target=p.locator('.message' if kind=='supplement' else '#excerpt');target.fill('长'*500);p.locator('.back').click()
    expect(p.get_by_text('是否放弃当前修改？',exact=True)).to_be_visible();metrics=p.locator('dialog').evaluate('d=>{const rect=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height}};return {dialog:rect(d),buttons:[...d.querySelectorAll("button")].filter(b=>b.getClientRects().length).map(rect)}}');r=metrics['dialog'];assert r['x']>=0 and r['right']<=width+1 and r['y']>=0 and r['bottom']<=845 and all(v['height']>=44 and v['width']>=44 and v['x']>=0 and v['right']<=width+1 and v['y']>=0 and v['bottom']<=845 for v in metrics['buttons']),metrics
    if width==320:p.screenshot(path=str(OUT/f'book-control-layout-{kind}-320.png'),full_page=True)
    p.get_by_role('button',name='继续编辑',exact=True).click();expect(target).to_have_value('长'*(20 if kind=='rename' else 500));assert store(p)==before;assert not errors;row=dict(passed=True,metrics=metrics)
   except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1600:])
   row.update(width=width,kind=kind,errors=errors,effective=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(width),flush=True);c.close()
 b.close()
assert files==source();(OUT/'book-control-layout-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed']for r in rows)else 1)
