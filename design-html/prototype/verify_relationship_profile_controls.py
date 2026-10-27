"""Replay the five existing profile controls, leaving the original82 report untouched."""
import hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
from audit_hidden_overlays import declarations
from audit_runtime import INIT
from verify_pet_controls import ROOT,source

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    out=ROOT/'evidence/current/relationship-day-counter';catalog_path=ROOT/'evidence/current/page-contracts.json';catalog=json.loads(catalog_path.read_text(encoding='utf-8'));cases=next(p for p in catalog['pages'] if p['id']=='m02-p06')['control_evidence'];assert len(cases)==5
    fixture=declarations('verify_onboarding_controls.py');files=source();rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for case in cases:
            context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');context.add_init_script(INIT);page=context.new_page();page.set_default_timeout(6500);page.set_default_navigation_timeout(20000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));row=dict(label=case['label'],selector=case['selector'],contract=case['contract'],passed=False,errors=errors)
            try:row['result']=fixture['run'](page,context,{**case,'id':'m02-p06'});assert not errors;row['passed']=True
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);context.close();assert source()==files;print(('PASS ' if row['passed'] else 'FAIL ')+case['label'],flush=True)
        browser.close()
    (out/'controls.json').write_text(json.dumps(dict(files=files,script_sha256=sha(Path(__file__)),fixture_script_sha256=sha(ROOT/'verify_onboarding_controls.py'),catalog_sha256=sha(catalog_path),scope='Historical selectors only; five current actual controls. Original82 report preserved.',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
