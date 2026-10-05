from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright,expect

OUT=Path(__file__).resolve().parent/'evidence/current';BASE='http://127.0.0.1:8765/'
rows=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for width in [320,375,390,414,430]:
        c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:
            p.goto(BASE+'pages/m02-p05.html');p.evaluate('document.fonts.ready');p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
            button=p.get_by_role('button',name='先逛逛我们的首页',exact=True);expect(button).to_be_visible();button.scroll_into_view_if_needed()
            metrics=p.evaluate('''()=>{const s=document.querySelector('.screen').getBoundingClientRect(),f=document.querySelector('.prototype-relationship-home').getBoundingClientRect(),b=document.querySelector('.prototype-relationship-home button'),r=b.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {width:document.documentElement.scrollWidth,artWidth:s.width,artHeight:s.height,footerStart:f.top,artEnd:s.bottom,buttonWidth:r.width,buttonHeight:r.height,hit:hit===b||b.contains(hit)}}''')
            assert metrics['width']==width and metrics['buttonWidth']>=44 and metrics['buttonHeight']>=44 and metrics['hit'],metrics
            assert abs(metrics['artHeight']/metrics['artWidth']-1825/862)<.002 and metrics['footerStart']>=metrics['artEnd']-.5,metrics
            p.screenshot(path=str(OUT/f'binding-home-{width}.png'),full_page=True)
            button.click();p.wait_for_url('**/m03-p01.html');assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-records')||'[]')")==[];assert not errors,errors
            row={'width':width,'passed':True,'metrics':metrics}
        except Exception:row={'width':width,'passed':False,'failure':traceback.format_exc()[-1800:]}
        row.update(errors=errors,effective=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+str(width),flush=True);c.close()
    b.close()
(OUT/'binding-home-layout-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
