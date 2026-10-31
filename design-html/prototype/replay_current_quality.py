"""Current114 initial geometry/keyboard audit with native-modal accessibility."""
import json, traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
import audit_initial_quality as Q
from replay_current_initial_controls import ROOT, DEMO, deps, fixture_files, sha, dump

OUT=ROOT/'evidence/current/quality-20261031'
WIDTHS=[320,375,390,414,430]

def main():
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'results.json').exists()
    files=deps();scripts=fixture_files();scripts.update({n:sha(ROOT/n) for n in ['audit_initial_quality.py',Path(__file__).name]})
    old={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'evidence/current/initial-quality').glob('*') if p.is_file()}
    for sub,mapping,origin in [('source',files,DEMO),('fixtures',scripts,ROOT)]:
        for n in mapping:
            target=OUT/sub/n;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((origin/n).read_bytes())
    manifest=json.loads((DEMO/'manifest.json').read_text(encoding='utf-8'));ids=[v['id'] for v in manifest];assert len(set(ids))==114
    observe=Q.OBSERVE.replace("const visible=e=>{", "const modal=document.querySelector('dialog[open]');const visible=e=>{if(e.closest('[inert]')||(modal&&!modal.contains(e)))return false;")
    assert observe!=Q.OBSERVE
    rows=[];executions=[]
    with sync_playwright() as pw:
        for module in [f'm{i:02}' for i in range(1,9)]:
            browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
            version=browser.version
            for width in WIDTHS:
                for page in [v for v in ids if v.startswith(module)]:
                    context=browser.new_context(viewport={'width':width,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai')
                    p=context.new_page();p.set_default_timeout(6000);p.set_default_navigation_timeout(15000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
                    try:
                        Q.canonical(p,page)
                        p.evaluate("document.documentElement.style.setProperty('--ui-safe-top','44px');document.documentElement.style.setProperty('--ui-safe-bottom','34px')")
                        modal=p.locator('dialog[open]').count()
                        session=context.new_cdp_session(p)
                        tree=session.send('Accessibility.getFullAXTree')['nodes']
                        missing=[{'role':n.get('role',{}).get('value'),'backend':n.get('backendDOMNodeId')} for n in tree if not n.get('ignored') and n.get('role',{}).get('value') in ['button','link','textbox','searchbox','combobox','checkbox','radio','switch','tab'] and not n.get('name',{}).get('value')]
                        if width==390:p.screenshot(path=str(OUT/(page+'.png')),full_page=True)
                        metrics=p.evaluate(observe);Q.effective_targets(p,session,metrics)
                        keys=Q.keyboard(p,metrics['controls']) if width==390 else None
                        failures={'overflow':metrics['documentWidth']>width,'blocked':[c for c in metrics['controls'] if not c['disabled'] and not c['hit']],'small':[c for c in metrics['controls'] if not c['disabled'] and min(c['rect']['width'],c['rect']['height'])<39.5],'unsafe':[c for c in metrics['controls'] if not c['safeTop'] or not c['safeBottom']],'unlabelled':[c for c in metrics['controls'] if not c['labelled']],'missingNames':missing,'imagesWithoutAlt':metrics['imagesWithoutAlt'],'keyboardUnreached':keys['unreached'] if keys else [],'keyboardFocus':keys['noVisibleFocus'] if keys else [],'errors':errors}
                        row={'page':page,'width':width,'passed':not any(failures.values()),'effective':p.url,'native_modal':bool(modal),'metrics':metrics,'keyboard':keys,'failures':failures}
                    except Exception:row={'page':page,'width':width,'passed':False,'failure':traceback.format_exc(),'errors':errors}
                    if not row['passed']:p.screenshot(path=str(OUT/(page+'-'+str(width)+'-finding.png')),full_page=True)
                    rows.append(row);context.close()
                assert deps()==files and all(sha(ROOT/n)==h for n,h in scripts.items())
                assert all(sha(ROOT/n)==h for n,h in old.items())
                dump(OUT/'results.json',{'dependencies':files,'fixture_sha256':scripts,'preserved_reports':old,'browser':version,'widths':WIDTHS,'height':844,'safe_insets':[44,34],'motion':'reduce','results':rows,'complete':len(rows)==570,'all_passed':len(rows)==570 and all(r['passed'] for r in rows),'human_accepted_pages':0,'scope':'114 canonical initial fixtures at five widths, actual Tab traversal at390; native open modal defines accessible surface. Not all hidden conditions, visual fidelity, native IME, screen readers or full41 acceptance.'})
                print(module,width,'PASS',sum(r['passed'] for r in rows if r['page'].startswith(module) and r['width']==width),'/',len([r for r in rows if r['page'].startswith(module) and r['width']==width]),flush=True)
            browser.close();executions.append(module)
    return 0 if all(r['passed'] for r in rows) else 1

if __name__=='__main__':raise SystemExit(main())
