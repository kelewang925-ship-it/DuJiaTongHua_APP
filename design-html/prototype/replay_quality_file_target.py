"""Recheck only the five affected page layouts and real photo supplement flow."""
import ast,json,traceback
from pathlib import Path
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright,expect
from replay_current_initial_controls import ROOT,DEMO,deps,sha,dump
from audit_hidden_overlays import declarations

OUT=ROOT/'evidence/current/quality-file-target-20261031'
BASELINE=ROOT/'evidence/current/quality-20261031'
CSS='assets/prototype-book-v2.css'

def main():
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'results.json').exists()
    baseline=json.loads((BASELINE/'results.json').read_text(encoding='utf-8'))
    files=deps();assert [n for n,h in files.items() if baseline['dependencies'].get(n)!=h]==[CSS]
    before=(BASELINE/'source'/CSS).read_bytes();after=(DEMO/CSS).read_bytes();assert after.startswith(before)
    patch=after[len(before):].decode('utf-8');assert len(patch.splitlines())==2
    assert all(line.startswith('.book-v2[data-book-page="19"] .v2-upload input[type="file"]') for line in patch.splitlines())
    path=ROOT/'replay_current_quality.py';tree=ast.parse(path.read_text(encoding='utf-8'))
    replacements=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.For) and isinstance(node.target,ast.Name) and node.target.id in ['module','page']:
            node.iter=ast.List(elts=[ast.Constant('m08' if node.target.id=='module' else 'm08-p19')],ctx=ast.Load());replacements.append(node.target.id)
    assert sorted(replacements)==['module','page']
    ast.fix_missing_locations(tree)
    namespace={'__file__':str(path),'__name__':'quality_target_fixture'}
    exec(compile(tree,str(path),'exec'),namespace);namespace['OUT']=OUT
    assert namespace['main']()==0
    fresh=json.loads((OUT/'results.json').read_text(encoding='utf-8'));assert len(fresh['results'])==5 and all(r['passed'] for r in fresh['results'])
    (OUT/'five-layout-results.json').write_bytes((OUT/'results.json').read_bytes())
    sample=BytesIO();Image.new('RGB',(30,40),'pink').save(sample,format='PNG')
    book=declarations('verify_book_controls.py');flows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in [320,375,390,414,430]:
            context=browser.new_context(viewport={'width':width,'height':420},reduced_motion='reduce');p=context.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:
                book['seed'](p,'m08-p19');original=book['store'](p)
                field=p.locator('input[type=file]');field.scroll_into_view_if_needed()
                rect=field.bounding_box();assert rect['height']>=44
                button_height=field.evaluate('e=>parseFloat(getComputedStyle(e,"::file-selector-button").minHeight)');assert button_height>=44
                with p.expect_file_chooser() as chosen:field.click()
                chosen.value.set_files({'name':'photo.png','mimeType':'image/png','buffer':sample.getvalue()})
                expect(p.locator('.photo-label')).to_have_text('♥ 已附上照片 ♥');expect(p.locator('.book-supplement-preview img')).to_be_visible()
                assert book['store'](p)==original
                field.set_input_files({'name':'bad.txt','mimeType':'text/plain','buffer':b'bad'})
                expect(p.locator('.prototype-toast')).to_contain_text('原照片仍保留')
                p.locator('.message').fill('触控照片补页')
                p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","book-supplement")')
                p.locator('.submit').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成')
                assert book['store'](p)==original
                expect(p.locator('.message')).to_have_value('触控照片补页')
                p.locator('.submit').click();p.wait_for_url('**/m08-p20.html*')
                p.wait_for_function('JSON.parse(localStorage.getItem("dujia-prototype-books")).find(b=>b.id==="book-state").pages.find(p=>p.id==="page-second").supplements.some(s=>s.text==="触控照片补页")')
                saved=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-books")).find(b=>b.id==="book-state").pages.find(p=>p.id==="page-second").supplements.filter(s=>s.text==="触控照片补页")')
                assert len(saved)==1 and saved[0]['image'].startswith('data:image/png') and not errors
                row={'width':width,'passed':True,'file_height':rect['height'],'native_button_min_height':button_height,'scope':'420px viewport; real chooser activation, PNG read, invalid replacement retained, failed save input/storage kept, successful retry exactly once.'}
            except Exception:row={'width':width,'passed':False,'failure':traceback.format_exc(),'errors':errors}
            flows.append(row);context.close();print('PHOTO_FLOW',width,row['passed'],flush=True)
        browser.close()
    assert deps()==files
    retained=[{**r,'execution':'retained-unaffected','provenance':{'report':'evidence/current/quality-20261031/results.json','sha256':sha(BASELINE/'results.json'),'page':r['page'],'width':r['width']}} for r in baseline['results'] if r['page']!='m08-p19']
    assert len(retained)==565 and all(r['passed'] for r in retained)
    results=retained+[{**r,'execution':'fresh'} for r in fresh['results']]
    final={**fresh,'results':results,'complete':True,'all_passed':all(r['passed'] for r in results),'reconciliation':{'producer':'replay_quality_file_target.py','sha256':sha(ROOT/'replay_quality_file_target.py'),'baseline_report_sha256':sha(BASELINE/'results.json'),'five_layout_report_sha256':sha(OUT/'five-layout-results.json'),'patch':patch,'changed_dependency':CSS,'retained_cases':565,'fresh_cases':5,'boundary':'Only data-book-page=19 file input and native selector button receive appended rules. Every page19 width re-executed; other565 page-width cases retain original provenance.'},'photo_flows':flows,'scope':'570 initial geometry cases:565 retained outside scoped page19 CSS plus5 fresh page19 layouts. Five additional fresh photo flows at420px height. Not full visual/native acceptance.'}
    dump(OUT/'results.json',final)
    for n in ['replay_quality_file_target.py','verify_book_controls.py']:
        target=OUT/'fixtures'/n;target.write_bytes((ROOT/n).read_bytes())
    return 0 if all(r['passed'] for r in flows) else 1

if __name__=='__main__':raise SystemExit(main())
