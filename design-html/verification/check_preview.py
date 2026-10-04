"""Verify the running local preview serves this checkout and its gallery works."""
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:8765/'
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
for path in ['index.html','assets/font.ttf']+[f"pages/{x['id']}.html" for x in manifest]:
    with urlopen(BASE+path,timeout=10) as response:
        assert response.status==200
        assert hashlib.sha256(response.read()).digest()==hashlib.sha256((ROOT/path).read_bytes()).digest(),path
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    page=browser.new_page(viewport={'width':1280,'height':900})
    page.goto(BASE+'index.html');assert page.locator('.card').count()==114
    page.screenshot(path=str(ROOT/'ui-audit/evidence/after/full-suite/browser-index.png'))
    page.locator('#search').fill('共同回忆册');assert page.locator('.card:visible').count()==21
    page.locator('#search').fill('童话首页');assert page.locator('.card:visible').count()==12
    page.set_viewport_size({'width':390,'height':826})
    page.locator('a[href="pages/m03-p02.html"]').click();page.wait_for_url('**/pages/m03-p02.html')
    page.evaluate('document.fonts.ready');assert page.evaluate('document.documentElement.scrollWidth')==390
    page.locator('.screen').screenshot(path=str(ROOT/'ui-audit/evidence/after/full-suite/http-home-390.png'))
    browser.close()
(ROOT/'ui-audit/preview-results.json').write_text(json.dumps({'pages_served':114,'matches_current_checkout':True,'gallery_cards':114,'memory_filter':21,'home_filter':12,'home_navigation':True},ensure_ascii=False,indent=2),encoding='utf-8')
print('HTTP preview passed: all 114 pages and font match this checkout; gallery filtering and home navigation passed')
