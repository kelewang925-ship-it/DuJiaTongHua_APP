"""Template sketches remain distinguishable, reachable and preserve existing routes."""
import argparse,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_book_v2_reconciliation import ROOT,dependencies,sha

LABELS=['日记摘录','照片故事','重要时刻','工坊作品','宠物成长','章节扉页']
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args()
    out=ROOT/f'evidence/{args.stage}/book-template-previews';out.mkdir(parents=True,exist_ok=True);files=dependencies();fixture=declarations('verify_book_controls.py');rows=[]
    cases=[('layout',w) for w in [320,375,390,414,430]]
    if args.stage=='current':cases += [('route',i) for i in range(6)]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,v in cases:
            c=b.new_context(viewport=dict(width=v if kind=='layout' else 390,height=844),reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(kind=kind,value=v,passed=False)
            try:
                fixture['seed'](p,'m08-p08');p.evaluate('document.fonts.ready');before=p.evaluate('({...localStorage})')
                if kind=='layout':
                    if v==390:p.screenshot(path=str(out/'390.png'),full_page=True)
                    previews=p.locator('.v2-template-preview');expect(previews).to_have_count(6)
                    assert len(set(previews.evaluate_all('(es)=>es.map(e=>e.dataset.preview)')))==6
                    expect(p.get_by_text('版式示意，内容由你选择的共同回忆填入。',exact=True)).to_be_visible()
                    for i,label in enumerate(LABELS):
                        choice=p.get_by_role('button',name=label,exact=True);preview=previews.nth(i);expect(preview).to_have_attribute('aria-hidden','true')
                        choice.scroll_into_view_if_needed();box=preview.bounding_box();assert box['width']>=70 and box['height']>=56,box
                        assert choice.evaluate('e=>{const r=e.getBoundingClientRect();const h=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return e===h||e.contains(h)}')
                        choice.click();expect(choice).to_have_attribute('aria-pressed','true')
                        expect(p.locator('.templates button[aria-pressed="true"]')).to_have_count(1)
                    assert p.evaluate('document.documentElement.scrollWidth')==v
                    assert p.evaluate('({...localStorage})')==before
                    row['sketch_shapes']=previews.evaluate_all('(es)=>es.map(e=>({type:e.dataset.preview,height:e.clientHeight,width:e.clientWidth}))')
                else:
                    p.get_by_role('button',name=LABELS[v],exact=True).click();p.locator('.use').click()
                    if v==5:
                        expect(p.get_by_role('dialog')).to_be_visible();expect(p.get_by_role('textbox',name='章节名',exact=True)).to_be_visible()
                        p.get_by_role('button',name='取消',exact=True).click();expect(p.get_by_role('dialog')).to_have_count(0);assert p.evaluate('({...localStorage})')==before
                    else:
                        target=[9,10,11,12,12][v];p.wait_for_url('**/m08-p'+str(target).zfill(2)+'.html*');expect(p.locator('.screen')).to_have_attribute('aria-busy','false')
                    row['outcome']=p.url
                assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            row['errors']=errors;rows.append(row);c.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(v),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps(dict(dependency_files=files,producer_sha256=sha(Path(__file__)),fixture_sha256=sha(ROOT/'verify_book_controls.py'),browser=version,viewport_height=844,locale='zh-CN',timezone='Asia/Shanghai',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if all(x['passed'] for x in rows) else 1)

if __name__=='__main__':raise SystemExit(main())
