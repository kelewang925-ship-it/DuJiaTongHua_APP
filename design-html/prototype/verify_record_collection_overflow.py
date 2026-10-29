"""Real multi-record scrolling after removing the album's inherited fixed grid rows."""
import json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_record_presentation import ROOT,dependencies,sha

def main():
    out=ROOT/'evidence/current/record-collection-overflow';out.mkdir(parents=True,exist_ok=True)
    assert not (out/'results.json').exists(),'Preserve prior evidence before re-running'
    fixture=declarations('verify_record_controls.py');files=dependencies();rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for page in ['m03-p06','m03-p10']:
            for width in [320,360,390,414,430]:
                c=b.new_context(viewport={'width':width,'height':844},locale='zh-CN',timezone_id='Asia/Shanghai',reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000)
                errors=[];p.on('pageerror',lambda error:errors.append(str(error)));r={'page':page,'width':width,'passed':False}
                try:
                    fixture['seed'](p,page)
                    p.evaluate('album=>{const source=PrototypeRecords.all().find(r=>r.type===(album?"photo":"diary")),rows=[];for(let i=0;i<10;i++){const canvas=document.createElement("canvas");canvas.width=i%2?90:320;canvas.height=i%2?320:90;const ctx=canvas.getContext("2d");ctx.fillStyle=i%2?"#9aaeb4":"#b5bd99";ctx.fillRect(0,0,canvas.width,canvas.height);rows.push({...source,id:"overflow-"+i,title:"第"+(i+1)+"条"+"可编辑的真实记录".repeat(6),body:"长正文".repeat(300),image:canvas.toDataURL(),updatedAt:Date.now()-i});}localStorage.setItem("dujia-prototype-records",JSON.stringify(rows));}',page=='m03-p10')
                    p.reload();selector='.prototype-photo-card' if page=='m03-p10' else '.prototype-diary-card';container=p.locator('.prototype-photo-grid' if page=='m03-p10' else '.prototype-diary-list')
                    expect(p.locator(selector)).to_have_count(10);p.wait_for_function('s=>[...document.querySelectorAll(s+" img")].every(i=>i.complete&&i.naturalWidth>0)',arg=selector);p.evaluate('document.fonts.ready');before=fixture['store'](p)
                    assert container.evaluate('e=>e.scrollHeight>e.clientHeight+100 && e.scrollWidth<=e.clientWidth+1')
                    assert p.locator(selector).evaluate_all('cards=>cards.every(e=>{const i=e.querySelector("img"),r=i.getBoundingClientRect(),b=e.getBoundingClientRect();return r.bottom<=b.bottom+1&&r.right<=b.right+1})')
                    last=p.locator('[data-record-id="overflow-9"]');last.focus();last.scroll_into_view_if_needed();assert container.evaluate('e=>e.scrollTop>0');expect(last).to_be_focused()
                    if width==390:p.screenshot(path=str(out/f'{page}-last.png'),full_page=True)
                    p.keyboard.press('Enter');fixture['go'](p,'m03-p12' if page=='m03-p10' else 'm03-p08');assert 'id=overflow-9' in p.url;assert fixture['store'](p)==before
                    assert not errors;r['passed']=True
                except Exception:r['failure']=traceback.format_exc();p.screenshot(path=str(out/f'failure-{page}-{width}.png'),full_page=True)
                r['page_errors']=errors;rows.append(r);c.close();assert dependencies()==files;print(('PASS ' if r['passed'] else 'FAIL ')+page+' '+str(width),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps({'dependency_files':files,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_record_controls.py'),'browser':version,'results':rows,'scope':'10 actual records, alternating portrait/landscape canvas fixture images, scroll/frame bounds and last-record keyboard route in diary and album at five widths. No human acceptance.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
