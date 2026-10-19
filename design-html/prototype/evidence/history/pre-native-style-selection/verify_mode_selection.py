"""Selection painting, keyboard use, save failure/retry and generation agree."""
import argparse
import hashlib
import json
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_initial_quality import canonical
from verify_pet_controls import ROOT,DEMO,BASE,source

def assert_selection(p,index):
    buttons=p.locator('.modes button');assert buttons.count()==2
    for i in range(2):
        button=buttons.nth(i);expect(button).to_have_attribute('aria-pressed',str(i==index).lower())
        marker=button.locator('.mode-check');assert marker.count()==1,'Each editable mode needs its own native selection marker'
        expect(marker).to_have_attribute('aria-hidden','true')
        if i==index:expect(marker).to_be_visible()
        else:expect(marker).not_to_be_visible()
        assert button.locator('.mode-art[aria-hidden=true]').count()==1
    assert p.locator('.modes').evaluate("e=>getComputedStyle(e).backgroundColor")not in ['transparent','rgba(0, 0, 0, 0)'],'Old raster selection must be covered'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');args=parser.parse_args()
    out=ROOT/('evidence/baseline/mode-selection'if args.baseline else'evidence/current/mode-selection');out.mkdir(parents=True,exist_ok=True)
    files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in (DEMO/'assets').glob('*.css')};rows=[]
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in [320,375,390,414,430]:
            context=browser.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=context.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:
                canonical(p,'m05-p03');assert_selection(p,0);work_id=p.evaluate("new URLSearchParams(location.search).get('id')");story=p.locator('#story').input_value();before=p.locator('.modes').bounding_box()
                p.locator('.modes button').last.click();assert_selection(p,1);assert p.locator('.modes').bounding_box()==before
                p.screenshot(path=str(out/f'movie-selected-{width}.png'),full_page=True)
                p.get_by_role('button',name='暂存创作草稿',exact=True).click();p.wait_for_url('**/m05-p09.html')
                saved=p.evaluate("id=>JSON.parse(localStorage.getItem('dujia-prototype-works')).find(r=>r.id===id)",work_id);assert saved['mode']=='电影感'and saved['story']==story
                p.goto(BASE+'pages/m05-p03.html?id='+work_id);assert_selection(p,1)
                first=p.locator('.modes button').first;first.focus();p.keyboard.press('Space');assert_selection(p,0)
                focus=first.evaluate("e=>({visible:e.matches(':focus-visible'),width:getComputedStyle(e).outlineWidth})");assert focus['visible']and float(focus['width'].removesuffix('px'))>=2
                p.evaluate("sessionStorage.setItem('dujia-prototype-fail-next','work-save')");p.get_by_role('button',name='暂存创作草稿',exact=True).click();p.wait_for_function("sessionStorage.getItem('dujia-prototype-fail-next')!=='work-save'");expect(p.locator('.prototype-toast')).to_contain_text('重试');assert_selection(p,0)
                assert p.evaluate("id=>JSON.parse(localStorage.getItem('dujia-prototype-works')).find(r=>r.id===id).mode",work_id)=='电影感'
                p.get_by_role('button',name='暂存创作草稿',exact=True).click();p.wait_for_url('**/m05-p09.html');p.goto(BASE+'pages/m05-p03.html?id='+work_id);assert_selection(p,0)
                p.screenshot(path=str(out/f'warm-selected-{width}.png'),full_page=True)
                p.locator('.modes button').last.click();p.evaluate("sessionStorage.setItem('dujia-prototype-fail-next','work-generate')");p.locator('#generate').click();p.wait_for_url('**/m05-p07.html*',timeout=15000)
                failed=p.evaluate("id=>JSON.parse(localStorage.getItem('dujia-prototype-works')).find(r=>r.id===id)",work_id);assert failed['mode']=='电影感'and failed['story']==story and failed['status']=='failed'
                p.get_by_role('button',name='重新生成',exact=True).click();p.wait_for_url('**/m05-p08.html*',timeout=15000)
                final=p.evaluate("id=>JSON.parse(localStorage.getItem('dujia-prototype-works')).find(r=>r.id===id)",work_id);assert final['mode']=='电影感'and final['story']==story and final['status']=='ready';assert not errors,errors
                row=dict(width=width,passed=True,work_id=work_id,saved_mode=saved['mode'],failed_mode=failed['mode'],failed_status=failed['status'],final_mode=final['mode'],status=final['status'],focus=focus)
            except Exception:row=dict(width=width,passed=False,failure=traceback.format_exc()[-2600:],errors=errors)
            rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+'mode-selection '+str(width),flush=True);context.close()
        browser.close()
    assert files==source();(out/'results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if all(row['passed']for row in rows)else 1)

if __name__=='__main__':main()
