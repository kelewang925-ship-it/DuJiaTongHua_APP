"""Five-width behavior checks for search-chip targets and selected-mode keyboard focus."""
import json
import hashlib
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_initial_quality import canonical,effective_targets,OBSERVE
from verify_pet_controls import ROOT,DEMO,source

files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in (DEMO/'assets').glob('*.css')};rows=[]
with sync_playwright()as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for width in [320,375,390,414,430]:
        c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:
            canonical(p,'m03-p03');texts=['第'+str(i)+'段'+('很长的共同回忆'*12)for i in range(6)]
            p.evaluate("rows=>localStorage.setItem('dujia-prototype-search-history',JSON.stringify(rows))",texts);p.reload();p.evaluate('document.fonts.ready')
            chips=p.locator('.chips');metrics=chips.evaluate("e=>({width:e.clientWidth,scrollWidth:e.scrollWidth,height:e.clientHeight,wrap:getComputedStyle(e).flexWrap})")
            assert metrics['scrollWidth']>metrics['width']and metrics['wrap']=='nowrap'and metrics['height']>=44,metrics
            assert p.evaluate('document.documentElement.scrollWidth')==width
            last=p.locator('.chips button').last;last.scroll_into_view_if_needed();box=last.bounding_box();assert box['height']>=44
            assert last.evaluate('(e)=>{const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return hit===e||e.contains(hit)}')
            last.click();p.wait_for_url('**/m03-p04.html*');assert p.evaluate("new URLSearchParams(location.search).get('q')")==texts[-1]
            canonical(p,'m05-p03');button=p.locator('.modes button').last;button.click();expect(button).to_have_attribute('aria-pressed','true');before=button.bounding_box()
            p.keyboard.press('Shift+Tab');p.keyboard.press('Tab');expect(button).to_be_focused()
            focus=button.evaluate("e=>({visible:e.matches(':focus-visible'),style:getComputedStyle(e).outlineStyle,width:getComputedStyle(e).outlineWidth,selected:e.getAttribute('aria-pressed')})")
            assert focus['visible']and focus['style']!='none'and float(focus['width'].removesuffix('px'))>=2 and focus['selected']=='true',focus
            assert button.bounding_box()==before;assert not errors,errors
            row=dict(width=width,passed=True,history=metrics,focus=focus)
        except Exception:row=dict(width=width,passed=False,failure=traceback.format_exc()[-2400:],errors=errors)
        rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+'quality-repairs '+str(width),flush=True);c.close()
    b.close()
assert files==source()and styles=={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in (DEMO/'assets').glob('*.css')}
(ROOT/'evidence/current/initial-quality/repair-behavior-results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(row['passed']for row in rows)else 1)
