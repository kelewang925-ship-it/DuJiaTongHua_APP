"""Default template must be visibly selected before using its existing route."""
import argparse,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_book_v2_reconciliation import ROOT,dependencies,sha

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args()
    out=ROOT/f'evidence/{args.stage}/book-template-default';out.mkdir(parents=True,exist_ok=True)
    fixture=declarations('verify_book_controls.py');files=dependencies();rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for width in [320,375,390,414,430]:
            c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            row=dict(width=width,passed=False)
            try:
                fixture['seed'](p,'m08-p08');before=p.evaluate('({...localStorage})')
                row['initial_choices']=p.locator('.templates button').evaluate_all('(es)=>es.map(e=>({name:e.dataset.template,pressed:e.getAttribute("aria-pressed")}))')
                if width==390:p.screenshot(path=str(out/'initial-390.png'),full_page=True)
                selected=p.locator('.templates button[aria-pressed="true"]');expect(selected).to_have_count(1);expect(selected).to_have_attribute('data-template','日记摘录')
                assert p.evaluate('({...localStorage})')==before
                # Re-select each existing template: one choice remains selected and
                # the selected computed background differs from the other choices.
                for i in range(6):
                    choice=p.locator('.templates button').nth(i);choice.click();expect(selected).to_have_count(1);expect(choice).to_have_attribute('aria-pressed','true')
                    assert choice.evaluate('e=>getComputedStyle(e).backgroundColor')!=p.locator('.templates button').nth((i+1)%6).evaluate('e=>getComputedStyle(e).backgroundColor')
                assert p.evaluate('({...localStorage})')==before
                p.locator('.templates button').first.click();p.locator('.use').click();p.wait_for_url('**/m08-p09.html*');expect(p.locator('.screen')).to_have_attribute('aria-busy','false')
                assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            row['errors']=errors;rows.append(row);c.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+str(width),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps(dict(dependency_files=files,producer_sha256=sha(Path(__file__)),fixture_sha256=sha(ROOT/'verify_book_controls.py'),browser=version,viewport_height=844,locale='zh-CN',timezone='Asia/Shanghai',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if all(x['passed'] for x in rows) else 1)

if __name__=='__main__':main()
