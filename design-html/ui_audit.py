"""Capture per-page UI review evidence without changing application state."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--module', type=int, required=True)
parser.add_argument('--phase', choices=['before', 'after'], required=True)
args = parser.parse_args()
items = [x for x in json.loads((ROOT/'manifest.json').read_text(encoding='utf-8')) if x['module_number'] == args.module]
out = ROOT/'ui-audit'/'evidence'/args.phase
out.mkdir(parents=True, exist_ok=True)
records = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for item in items:
        record = {'id': item['id'], 'widths': {}}
        for width in [320,375,390,414,430]:
            page = browser.new_page(viewport={'width':width,'height':932})
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto((ROOT/'pages'/f"{item['id']}.html").as_uri())
            page.evaluate('document.fonts.ready')
            metrics=page.evaluate('''() => {
              const visible = el => el.getClientRects().length && getComputedStyle(el).visibility !== 'hidden';
              const controls=[...document.querySelectorAll('button,a,input,textarea,select')].filter(visible);
              const target = el => {
                const r=el.getBoundingClientRect();
                const label=el.closest('label');
                if(label && label.getBoundingClientRect().height>=40 && el.tagName==='INPUT') return label.getBoundingClientRect();
                if(el.classList.contains('ui-hit-text')) return {width:r.width+12,height:44};
                return r;
              };
              return {documentWidth:document.documentElement.scrollWidth, fontLoaded:document.fonts.check('12px Fairy'),
                smallTargets:controls.filter(el=>{const r=target(el);return r.width<40||r.height<40}).map(el=>({text:(el.innerText||el.getAttribute('aria-label')||el.placeholder||el.name).slice(0,55),width:Math.round(target(el).width),height:Math.round(target(el).height)})),
                textOverflow:[...document.querySelectorAll('button,p,h1,h2,label')].filter(el=>visible(el)&&!el.classList.contains('ui-hit-text')&&el.clientWidth>0&&el.scrollWidth>el.clientWidth+2).map(el=>el.innerText.slice(0,70)),
                brokenImages:[...document.images].filter(el=>visible(el)&&(!el.complete||!el.naturalWidth)).map(el=>el.src)};
            }''')
            metrics['pageErrors']=errors
            record['widths'][str(width)]=metrics
            if width == 390:
                shot=page.locator('.screen').screenshot()
                import io
                Image.open(io.BytesIO(shot)).convert('RGB').save(out/f"{item['id']}.webp",quality=90)
            page.close()
        records.append(record)
        print(item['id'],flush=True)
    browser.close()
(out/f'm{args.module:02d}-metrics.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
for start in range(0,len(items),4):
    group=items[start:start+4]
    sheet=Image.new('RGB',(780,len(group)*840),'#e8dfd5')
    draw=ImageDraw.Draw(sheet)
    for row,item in enumerate(group):
        for col,path in enumerate([ROOT/'assets'/f"{item['id']}-source.webp",out/f"{item['id']}.webp"]):
            im=Image.open(path).convert('RGB'); im.thumbnail((390,815))
            sheet.paste(im,(col*390,row*840+24));draw.text((col*390+8,row*840+5),item['id']+(' source' if col==0 else ' '+args.phase),fill='#51321e')
    sheet.save(out/f'm{args.module:02d}-compare-{start//4+1}.webp',quality=87)
print('Evidence saved',out)
