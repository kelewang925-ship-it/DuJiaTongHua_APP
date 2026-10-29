"""Exercise literal close/cancel buttons for every observed current V2 overlay."""
import json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_book_v2_reconciliation import ROOT,dependencies,sha

def main():
    out=ROOT/'evidence/current/book-v2-overlay-cancel';out.mkdir(parents=True,exist_ok=True);files=dependencies();inventory_path=ROOT/'evidence/current/book-v2-hidden/inventory.json';inventory=json.loads(inventory_path.read_text(encoding='utf-8'));assert inventory['dependency_files']==files;fixture=declarations('verify_book_controls.py');rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for observation in inventory['results']:
            candidates=[c for c in observation['overlays'][0]['controls'] if c['visible'] and not c['disabled'] and c['tag']=='BUTTON' and c['label'] in ['取消','继续编辑','返回阅读']];assert len(candidates)==1,observation['trigger'];label=candidates[0]['label']
            c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(page=observation['page'],trigger=observation['trigger'],control_label=label,passed=False)
            try:
                fixture['seed'](p,observation['page']);before=fixture['store'](p);trigger=p.locator(observation['selector']);trigger.click();expect(p.locator('dialog h2')).to_have_text(observation['expected_title']);p.locator('dialog[open]').get_by_role('button',name=label,exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(trigger).to_be_focused();assert fixture['store'](p)==before;assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            row['errors']=errors;rows.append(row);c.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+row['page']+' '+row['trigger'],flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps(dict(dependency_files=files,producer_sha256=sha(Path(__file__)),fixture_sha256=sha(ROOT/'verify_book_controls.py'),inventory_sha256=sha(inventory_path),browser=version,scope='31 literal cancel/return buttons in untouched declared overlay states; does not replace dirty-form confirmation or nested-dialog checks.',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Literal overlay cancel:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
