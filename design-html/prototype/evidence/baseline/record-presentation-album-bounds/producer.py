"""Source-bound visual contracts and unchanged controls for four record collections."""
import argparse, hashlib, json, re, traceback
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from audit_hidden_overlays import declarations

ROOT=Path(__file__).resolve().parent
DEMO=ROOT.parent
PAGES={'m03-p02':'home','m03-p04':'search','m03-p06':'diary','m03-p10':'album'}
SELECTORS={'home':'.prototype-home-record','search':'.prototype-search-results .prototype-diary-card','diary':'.prototype-diary-list .prototype-diary-card','album':'.prototype-photo-card'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def dependencies():
    files={'assets/prototype-components.css','assets/font.ttf','assets/book-v2/paper.webp'}
    for page in PAGES:
        for folder in ['custom','pages']:files.add(f'{folder}/{page}.html')
        files.add(f'assets/{page}-art.webp')
        text=(DEMO/f'custom/{page}.html').read_text(encoding='utf-8')
        files.update('assets/'+s for s in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',text))
    return {s:sha(DEMO/s) for s in sorted(files) if (DEMO/s).is_file()}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);parser.add_argument('--album-only',action='store_true');args=parser.parse_args()
    out=ROOT/f'evidence/{args.stage}'/('record-presentation-album-bounds' if args.album_only else 'record-presentation');out.mkdir(parents=True,exist_ok=True)
    assert not (out/'results.json').exists(),'Preserve previous evidence before re-running'
    fixture=declarations('verify_record_controls.py');files=dependencies();rows=[]
    cases=[('visual',(page,width)) for page in PAGES for width in [320,360,390,414,430]]
    if args.album_only:cases=[case for case in cases if case[1][0]=='m03-p10']
    if args.stage=='current' and not args.album_only:
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'))
        for entry in catalog['pages']:
            if entry['id'] in PAGES:
                cases += [('control',(entry['id'],c)) for c in entry['control_evidence']]
        cases += [('extra',kind) for kind in ['diary-filter','photo-filter']]
        cases += [('hidden',kind) for kind in ['diary-delete','photo-delete']]
        cases += [('load-error',page) for page in ['m03-p04','m03-p06','m03-p10']]
        cases += [('image-error',page) for page in PAGES]
        cases += [('privacy',page) for page in PAGES]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=browser.version
        for kind,value in cases:
            width=value[1] if kind=='visual' else 390
            context=browser.new_context(viewport={'width':width,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai')
            p=context.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            row={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':fixture['control'](p,value[0],value[1],fixture['contract'](value[0],value[1]))
                elif kind in ['extra','hidden']:fixture[kind](p,value)
                else:
                    page=value[0] if kind=='visual' else value;variant=PAGES[page];selector=SELECTORS[variant]
                    fixture['seed'](p,page)
                    if kind in ['visual','image-error']:
                        # A real record image, not a copy of the design's sample photo grid.
                        p.evaluate('options=>{const rows=PrototypeRecords.all();if(options.variant!=="search"||options.bad)rows.find(r=>r.id==="audit-diary").image=options.bad?"/missing-record-image.png":rows.find(r=>r.type==="photo").image;if(options.bad)rows.find(r=>r.type==="photo").image="/missing-record-image.png";localStorage.setItem("dujia-prototype-records",JSON.stringify(rows));}',{'bad':kind=='image-error','variant':variant})
                        p.reload();expect(p.locator(selector)).to_have_count(3 if variant=='home' else 2 if variant in ['search','diary'] else 1);p.evaluate('document.fonts.ready')
                    before=fixture['store'](p)
                    if kind=='visual':
                        if width==390:p.screenshot(path=str(out/f'{page}.png'),full_page=True)
                        cards=p.locator(selector);expect(cards.first).to_have_attribute('data-record-presentation',variant)
                        images=cards.locator('img');assert images.count()>0,'Actual record images were discarded by the list renderer'
                        p.wait_for_function('s=>[...document.querySelectorAll(s+" img")].every(i=>i.complete&&i.naturalWidth>0)',arg=selector)
                        if variant in ['home','search']:expect(cards.locator('.record-preview[data-kind="note"]')).to_have_count(1)
                        assert cards.evaluate_all('nodes=>nodes.every(e=>e.scrollWidth<=e.clientWidth+1)'), 'Card content escapes its bounds'
                        for card in cards.all():
                            assert card.get_attribute('aria-label'),'Native card name must survive decorative previews'
                            box=card.bounding_box();assert box['width']>=44 and box['height']>=44
                        if variant!='home':
                            assert p.locator('.screen').evaluate('e=>getComputedStyle(e,"::after").backgroundImage.includes("paper.webp")'),'Original fake cards/photos remain visible around the collection'
                        if variant=='album':
                            assert images.evaluate_all('nodes=>nodes.every(i=>{const r=i.getBoundingClientRect(),b=i.closest("button").getBoundingClientRect();return r.top>=b.top-1&&r.bottom<=b.bottom+1&&r.left>=b.left-1&&r.right<=b.right+1})'),'Real album image protrudes beyond its paper frame'
                            assert p.locator('.screen').evaluate('e=>{const s=getComputedStyle(e,"::after");return s.maskImage==="none"&&parseFloat(s.top)<=e.clientHeight*.20+1}'),'Static sample photo/tape edges remain above the native grid'
                        # Long native text must remain clipped/wrapped within the original hit target.
                        cards.first.locator('strong,span:not(.record-preview):not(.record-card-copy)').first.evaluate('e=>e.textContent="很长的真实记录标题".repeat(20)')
                        assert cards.first.evaluate('e=>e.scrollWidth<=e.clientWidth+1')
                    elif kind=='load-error':
                        key={'m03-p04':'record-search','m03-p06':'diary-load','m03-p10':'photo-load'}[page]
                        p.evaluate('k=>sessionStorage.setItem("dujia-prototype-fail-next",k)',key);p.reload()
                        label={'m03-p04':'重试搜索','m03-p06':'重新加载日记','m03-p10':'重试加载'}[page]
                        p.get_by_role('button',name=label,exact=True).click();expect(p.locator(selector)).to_have_count(2 if page!='m03-p10' else 1)
                    elif kind=='image-error':
                        image=p.locator(selector).locator('img').first;expect(image).to_be_hidden()
                        card=image.locator('xpath=ancestor::button[1]');expect(card).to_contain_text('共同')
                        # Even a failed preview must retain the exact original detail route.
                        card.click();fixture['go'](p,'m03-p12' if variant=='album' else 'm03-p08')
                    elif kind=='privacy':
                        p.evaluate('()=>{const rows=PrototypeRecords.all();rows.push({...rows[0],id:"blocked-peer-record",title:"不能泄露的照片",author:"别人",visibility:"private",image:"/never-request-private.png"});localStorage.setItem("dujia-prototype-records",JSON.stringify(rows));}')
                        before=fixture['store'](p);requests=[];p.on('request',lambda r:requests.append(r.url));p.reload();expect(p.locator(selector)).to_have_count(3 if variant=='home' else 2 if variant in ['search','diary'] else 1)
                        assert all('不能泄露' not in text for text in p.locator(selector).all_text_contents());assert not any('never-request-private' in u for u in requests)
                    assert fixture['store'](p)==before,'Presentation/reading must not write records'
                assert not errors;row['passed']=True
            except Exception:
                row['failure']=traceback.format_exc()
                if kind!='visual':p.screenshot(path=str(out/f'failure-{len(rows):03d}.png'),full_page=True)
            row['page_errors']=errors;rows.append(row);context.close();assert dependencies()==files
            print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        browser.close()
    report={'dependency_files':files,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_record_controls.py'),'browser':version,'results':rows,'scope':'Four record list presentation variants, five widths, original initial controls and selected failure/privacy/delete/filter outcomes. Not a full114 replay or human acceptance.'}
    (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':(out/'producer.py').write_bytes(Path(__file__).read_bytes())
    print('Record presentation:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
