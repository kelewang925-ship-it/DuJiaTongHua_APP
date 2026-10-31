"""Asset review board generated from the real native SVG renderer, separate from page QA."""
import hashlib,json
from pathlib import Path
from playwright.sync_api import sync_playwright
from audit_hidden_overlays import declarations
from verify_pet_item_previews import ROOT,DEMO,prepare

def main():
    out=ROOT/'evidence/current/pet-item-previews';out.mkdir(parents=True,exist_ok=True);assert not (out/'vector-gallery.json').exists()
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();dependency=sha(DEMO/'assets/prototype-pet-item-preview.js')
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');p=b.new_page(viewport={'width':1200,'height':820});prepare(p,declarations('verify_pet_controls.py'),'crown','owned');before=p.evaluate('JSON.stringify({...localStorage})')
        vectors=p.evaluate('''()=>{const rows=[],screen=document.querySelector('.screen'),pet=PrototypePet.read();for(const item of PrototypePetLife.catalog){document.querySelector('.crown').textContent=item.name;PrototypePetItemPreview.paint(screen,item,pet);const svg=[...screen.querySelectorAll('.pet-item-preview svg')].at(-1);rows.push({id:item.id,name:item.name,svg:svg.outerHTML});}return rows}''');assert p.evaluate('JSON.stringify({...localStorage})')==before
        assert len(vectors)==18
        html='<!doctype html><meta charset="utf-8"><style>@font-face{font-family:Fairy;src:url(http://127.0.0.1:8765/assets/font.ttf)}*{box-sizing:border-box}body{margin:0;padding:16px;background:#fff8ed;color:#684320;font-family:Fairy,serif}main{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}article{height:245px;padding:16px;text-align:center;border:1px solid #d9c3a5;border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px}svg{width:140px;height:140px;fill:#efd4ad;stroke:#ac7b47;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}h2{margin:0;font-size:18px;font-weight:400}small{font:12px Arial,sans-serif}</style><main>'+''.join('<article>'+r['svg']+'<h2>'+r['name']+'</h2><small>'+r['id']+'</small></article>' for r in vectors)+'</main>'
        (out/'vector-gallery.html').write_text(html,encoding='utf-8');p.set_content(html);p.evaluate('document.fonts.ready');p.screenshot(path=str(out/'vector-gallery.png'),full_page=True);b.close()
    assert dependency==sha(DEMO/'assets/prototype-pet-item-preview.js')
    (out/'vector-gallery.json').write_text(json.dumps({'kind':'native-vector-asset-review-board-not-app-page','items':[{'id':r['id'],'name':r['name'],'svg_sha256':hashlib.sha256(r['svg'].encode()).hexdigest()} for r in vectors],'renderer_sha256':dependency,'producer_sha256':sha(Path(__file__)),'html_sha256':sha(out/'vector-gallery.html'),'screenshot_sha256':sha(out/'vector-gallery.png')},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Captured18 real native vector assets;display did not change storage')

if __name__=='__main__':main()
