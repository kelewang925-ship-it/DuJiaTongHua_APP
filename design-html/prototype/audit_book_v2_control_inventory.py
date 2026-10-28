"""Observe current book initial controls; legacy selectors are not relabelled."""
import json,traceback
from pathlib import Path
from datetime import datetime,timezone
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from audit_runtime import INIT,OBSERVE
from verify_book_v2_reconciliation import ROOT,dependencies,sha

def main():
    out=ROOT/'evidence/current/book-v2-controls';out.mkdir(parents=True,exist_ok=True)
    files=dependencies();fixture=declarations('verify_book_controls.py');rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for n in range(1,22):
            identity=f'm08-p{n:02d}';c=b.new_context(viewport=dict(width=390,height=844),locale='zh-CN',timezone_id='Asia/Shanghai',reduced_motion='reduce');c.add_init_script(INIT)
            p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(page=identity,passed=False)
            try:
                fixture['seed'](p,identity);p.evaluate('document.fonts.ready');p.wait_for_timeout(350)
                observed=p.evaluate(OBSERVE)
                for control in observed['controls']:
                    control['blocked_by_modal']=p.evaluate('s=>{const e=document.querySelector(s),d=document.querySelector("dialog[open]");return !!e&&(!!e.closest("[inert]")||!!d&&!d.contains(e))}',control['selector'])
                row.update(effective=p.url,controls=observed['controls'],headings=p.locator('h1,h2').all_text_contents(),dialogs=p.locator('dialog[open]').count(),errors=errors)
                assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            rows.append(row);c.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+identity+' '+str(len(row.get('controls',[]))),flush=True)
        b.close()
    report=dict(observed_at=datetime.now(timezone.utc).isoformat(),scope='21 current book initial states only; inventory does not prove controls work or exhaust conditional/hidden states.',dependency_files=files,producer_sha256=sha(Path(__file__)),fixture_sha256=sha(ROOT/'verify_book_controls.py'),observer_sha256=sha(ROOT/'audit_runtime.py'),browser=version,viewport=[390,844],locale='zh-CN',timezone='Asia/Shanghai',results=rows)
    (out/'inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
