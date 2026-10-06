"""Time detail damage must not claim content was deleted; actual shared state CTA."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from verify_time_collection_recovery import seed,raw,prompt,KINDS,key
from verify_pet_controls import ROOT,source
OUT=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');files=source();rows=[]
pages={'moments':'m04-p03.html?id=missing','anniversaries':'m04-p10.html?id=missing','capsules':'m04-p15.html?id=missing'}
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,360,390,414,430]:
  for kind,page in pages.items():
   for damaged in [True,False]:
    c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(2000 if '--baseline'in sys.argv else 4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
    try:
     value='{broken'if damaged else'[]';seed(p,kind,value,page)
     if damaged:prompt(p,kind);p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
     state=p.locator('.prototype-component-state');expect(state).to_have_count(1);expect(state).to_have_attribute('data-kind','error'if damaged else'empty');expect(state).to_have_attribute('role','alert'if damaged else'region');expect(state.locator('h2')).to_have_text(KINDS[kind][0]+'数据需要恢复'if damaged else'这个'+KINDS[kind][0]+'已经不在了');button=state.locator('button');button.scroll_into_view_if_needed();m=button.evaluate('b=>{const r=b.getBoundingClientRect();return {x:r.x,right:r.right,h:r.height,hit:document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===b}}');assert m['h']>=44 and m['x']>=0 and m['right']<=width+1 and m['hit'],m;assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');button.focus()
     if width==320:p.screenshot(path=str(OUT/f'time-missing-{kind}-{damaged}-320.png'),full_page=True)
     p.keyboard.press('Enter')
     if damaged:prompt(p,kind);p.get_by_role('button',name='稍后处理',exact=True).click();assert raw(p,kind)==value
     else:p.wait_for_url('**/'+('m04-p02.html'if kind=='moments'else'm04-p08.html'if kind=='anniversaries'else'm04-p12.html'))
     assert not errors;row=dict(passed=True)
    except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
    row.update(width=width,kind=kind,damaged=damaged,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+kind+' '+str(width)+' '+str(damaged),flush=True);c.close()
 b.close()
assert files==source();(OUT/'time-missing-state-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
