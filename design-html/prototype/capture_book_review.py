"""Capture V2 routes separately and prepare original/legacy/current review boards."""
from pathlib import Path
from datetime import datetime,timezone
import json,traceback
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from audit_runtime import INIT
from verify_book_v2_reconciliation import ROOT,DEMO,dependencies,sha

OUT=ROOT/'evidence/current/book-visual-review'
ORIGINAL=Path(r'D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\新模块分布')

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    boards=DEMO.parent/'.design-html-tools/book-review-boards';boards.mkdir(parents=True,exist_ok=True)
    queue=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'))
    legacy=json.loads((ROOT/'evidence/current/design-state-capture/results.json').read_text(encoding='utf-8'))
    fixture=declarations('verify_book_controls.py');before=dependencies();rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for item in [q for q in queue if q['id'].startswith('m08-')]:
            identity=item['id'];row=dict(page=identity,passed=False)
            c=b.new_context(viewport=dict(width=390,height=844),device_scale_factor=1,reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');c.add_init_script(INIT)
            p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:
                fixture['seed'](p,identity);expect(p.locator('.screen')).to_have_attribute('aria-busy','false');p.evaluate('document.fonts.ready');p.wait_for_timeout(350)
                screenshot=OUT/(identity+'.png');p.screenshot(path=str(screenshot),full_page=True)
                old=next(r for r in legacy['results'] if r['page']==identity)
                original=ORIGINAL/item['original_design_reference']['path']
                assert sha(original)==item['original_design_reference']['sha256']
                assert sha(ROOT/old['screenshot'])==old['screenshot_sha256']
                row.update(original_design_reference=item['original_design_reference'],original_export=item['design_path'],original_export_sha256=sha(DEMO.parent/item['design_path']),legacy_screenshot=old['screenshot'],legacy_screenshot_sha256=old['screenshot_sha256'],current_screenshot=screenshot.relative_to(ROOT).as_posix(),current_screenshot_sha256=sha(screenshot),current_url=p.url,headings=p.locator('h1,h2').all_text_contents(),errors=errors)
                assert not errors
                imgs=[Image.open(original),Image.open(ROOT/old['screenshot']),Image.open(screenshot)]
                resized=[im.convert('RGB').resize((390,round(im.height*390/im.width))) for im in imgs]
                board=Image.new('RGB',(1170,max(im.height for im in resized)+30),'#eeeeee');draw=ImageDraw.Draw(board)
                for i,(im,label) in enumerate(zip(resized,['ORIGINAL PNG','LEGACY CAPTURE (OLD SOURCE)','CURRENT V2 (NEW CAPTURE)'])):
                    board.paste(im,(i*390,30));draw.text((i*390+8,8),identity+' '+label,fill='black')
                board.save(boards/(identity+'.jpg'),quality=92)
                row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            rows.append(row);c.close();assert dependencies()==before
            print(('PASS ' if row['passed'] else 'FAIL ')+identity,flush=True)
        b.close()
    report=dict(captured_at=datetime.now(timezone.utc).isoformat(),browser=version,viewport=[390,844],dpr=1,locale='zh-CN',timezone='Asia/Shanghai',baseline='temporary comparison conditions; not human acceptance',dependency_files=before,producer_sha256=sha(Path(__file__)),fixture_sha256=sha(ROOT/'verify_book_controls.py'),results=rows)
    (OUT/'captures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
