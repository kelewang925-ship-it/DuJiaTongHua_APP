"""Compare actual visible computed styles before/after exact-value token adoption."""
import json,sys,traceback
from playwright.sync_api import sync_playwright
from audit_hidden_overlays import declarations,seed_onboarding
from verify_pet_controls import ROOT,BASE,source

CASES=[('m01-p02','onboarding'),('m03-p08','record'),('m03-p12','record'),('m04-p04','moment'),('m04-p09','time'),('m04-p13','time'),('m05-p03','workshop'),('m06-p05','settings'),('m07-p03','pet'),('m07-p18','pet'),('m08-p10','book'),('components','preview')]
PROPS=['color','backgroundColor','fontSize','fontFamily','lineHeight','paddingTop','paddingRight','paddingBottom','paddingLeft','marginTop','marginRight','marginBottom','marginLeft','borderTopColor','borderTopWidth','borderRadius','boxShadow','minHeight','minWidth','gap','transitionDuration','animationDuration']
def main():
    before='--before'in sys.argv;files=source();rows=[];fixtures={k:declarations('verify_'+k+'_controls.py')for k in ['record','moment','time','workshop','settings','pet','book']}
    prior=None
    if not before:prior=json.loads((ROOT/'evidence/baseline/shared-style-computed-before.json').read_text(encoding='utf-8'));assert len(prior['results'])==60 and all(r['passed']for r in prior['results'])
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in [320,360,390,414,430]:
            for identifier,group in CASES:
                context=browser.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=context.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(page=identifier,width=width)
                try:
                    if group=='onboarding':seed_onboarding(p,identifier)
                    elif group=='preview':p.goto(BASE+'prototype/components.html');p.evaluate('document.fonts.ready')
                    else:fixtures[group]['seed'](p,identifier)
                    if identifier in ['m03-p08','m03-p12']:
                        p.locator('#reply').fill('Token一致性回应');p.locator('#message [type=submit]').click();p.wait_for_function('document.querySelector("#reply").value===""')
                    p.wait_for_timeout(500)
                    observed=p.evaluate('''props=>[...document.body.querySelectorAll('*')].filter(e=>e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden').map(e=>{const s=getComputedStyle(e);return {tag:e.tagName,classes:e.className instanceof SVGAnimatedString?e.className.baseVal:e.className,styles:Object.fromEntries(props.map(k=>[k,s[k]]))}})''',PROPS)
                    if not before:
                        old=next(r['observed']for r in prior['results']if r['page']==identifier and r['width']==width);assert observed==old,[(i,a,b)for i,(a,b)in enumerate(zip(old,observed))if a!=b][:2]
                    assert not errors,errors;row.update(passed=True,observed=observed)
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-2400:])
                row['errors']=errors;rows.append(row);context.close();assert source()==files
            print(str(width)+'px '+str(sum(r['passed']for r in rows if r['width']==width))+'/12',flush=True)
        browser.close()
    path=ROOT/('evidence/baseline/shared-style-computed-before.json'if before else'evidence/current/shared-style-computed-results.json');path.write_text(json.dumps(dict(files=files,results=rows,accepted_pages=0,scope='Actual visible computed properties across12 representative render contexts at five widths, including new comment Avatar and tag management; not global workflows/visual acceptance.'),ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(rows),passed=sum(r['passed']for r in rows))));raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
