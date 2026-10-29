"""Observe current V2 overlays and safe Escape; business outcomes remain separate."""
import json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations,SNAPSHOT
from audit_runtime import INIT
from verify_book_v2_reconciliation import ROOT,dependencies,sha

def main():
    out=ROOT/'evidence/current/book-v2-hidden';out.mkdir(parents=True,exist_ok=True);files=dependencies()
    initial=ROOT/'evidence/current/book-v2-controls/results.json';report=json.loads(initial.read_text(encoding='utf-8'));assert report['dependency_files']==files
    cases=[r for r in report['results'] if r['contract'].startswith(('sheet:','modal:'))];fixture=declarations('verify_book_controls.py');rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for case in cases:
            c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');c.add_init_script(INIT);p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(page=case['page'],trigger=case['label'],selector=case['selector'],expected_title=case['contract'].split(':',1)[1],passed=False)
            try:
                fixture['seed'](p,case['page']);before=fixture['store'](p);trigger=p.locator(case['selector']);trigger.click();expect(p.locator('dialog[open] h2')).to_have_text(row['expected_title'])
                row['overlays']=p.evaluate(SNAPSHOT);assert len(row['overlays'])==1
                p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);expect(trigger).to_be_focused();assert fixture['store'](p)==before;assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            row['errors']=errors;rows.append(row);c.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+case['page']+' '+case['label'].replace('\n',' '),flush=True)
        b.close()
    data=dict(dependency_files=files,producer_sha256=sha(Path(__file__)),fixture_sha256=sha(ROOT/'verify_book_controls.py'),snapshot_producer_sha256=sha(ROOT/'audit_hidden_overlays.py'),initial_report_sha256=sha(initial),browser=version,viewport=[390,844],locale='zh-CN',timezone='Asia/Shanghai',scope='Overlays reached from declared initial fixtures and safe Escape only. Does not prove hidden business controls, nested overlays, every close method or all conditional states.',results=rows)
    (out/'inventory.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Hidden overlay observations:',sum(r['passed'] for r in rows),'/',len(rows))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
