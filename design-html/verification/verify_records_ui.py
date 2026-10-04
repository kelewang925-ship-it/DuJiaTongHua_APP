from pathlib import Path
import json
from playwright.sync_api import sync_playwright
r=Path('design-html').resolve(); results=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');page=b.new_page(viewport={'width':320,'height':740})
 def go(id):page.goto((r/'pages'/f'{id}.html').as_uri());page.evaluate('document.fonts.ready')
 go('m03-p03');page.locator('#query').fill('很长的搜索关键词'*30);assert page.evaluate('document.documentElement.scrollWidth')==320;page.locator('#clear').click();assert page.locator('#query').input_value()=='';page.locator('[data-query="晚霞"]').click();page.wait_for_url('**/m03-p04.html?q=*');assert page.locator('#query').input_value()=='晚霞';results.append('320px long search input, clear, recent query and result routing passed')
 go('m03-p05');page.locator('.title').fill('日记标题'*40);page.locator('.body-text').fill('长正文'*200);page.locator('input[value="private"]').check();page.locator('#remove').click();assert not page.locator('#preview').is_visible();page.locator('#file').set_input_files(str(r/'assets/m03-p05-source.webp'));assert page.locator('#preview').is_visible();page.locator('.submit').click();data=page.evaluate("JSON.parse(localStorage.getItem('dujia-diary-draft'))");assert data['visibility']=='private' and len(data['body'])==600;assert page.evaluate('document.documentElement.scrollWidth')==320;results.append('Long diary title/body, private state, photo remove/upload and draft save passed')
 go('m03-p06');page.locator('[data-tab="draft"]').click();assert page.locator('[data-tab="draft"]').get_attribute('aria-selected')=='true';page.locator('#filter').click();assert page.locator('#toast').is_visible();results.append('Diary tab state and existing demo filter feedback passed')
 go('m03-p10');page.get_by_role('tab',name='旅行',exact=True).click();assert page.get_by_role('tab',name='旅行',exact=True).get_attribute('aria-selected')=='true';results.append('Album tab selection passed')
 go('m03-p11');page.locator('#file').set_input_files(str(r/'assets/m03-p11-source.webp'));assert page.locator('#selected').is_visible();page.locator('.caption').fill('照片说明'*100);page.locator('input[name="tag"]').fill('旅行标签'*30);page.locator('#add-tag').click();assert page.locator('input[name="tag"]').input_value().endswith('、');page.locator('input[value="private"]').check();page.locator('.submit').click();data=page.evaluate("JSON.parse(localStorage.getItem('dujia-photo-draft'))");assert data['visibility']=='private' and len(data['caption'])==400;assert page.evaluate('document.documentElement.scrollWidth')==320;results.append('Photo upload, long caption/tag, private radio and metadata save passed')
 for id in ['m03-p08','m03-p12']:
  go(id);page.locator('#reply').fill('留言'*200);page.locator('#emoji').click();assert '❤️' in page.locator('#reply').input_value();page.locator('.composer button[type="submit"]').click();assert page.locator('#toast').is_visible() and page.locator('#reply').input_value()==''
 results.append('Both detail composers retain emoji-content and demo-send behavior with long messages')
 for i in range(1,13):
  id=f'm03-p{i:02}';go(id);page.locator('.screen').screenshot(path=str(r/'ui-audit/evidence/after'/f'{id}-320.png'))
  page.evaluate("document.documentElement.style.setProperty('--ui-safe-top','44px');document.documentElement.style.setProperty('--ui-safe-bottom','34px')")
  m=page.evaluate("()=>{const r=document.querySelector('.screen').getBoundingClientRect();return {y:r.y,h:r.height,doc:document.documentElement.scrollHeight,w:document.documentElement.scrollWidth}}")
  assert m['y']>=44 and m['doc']>=m['h']+77 and m['w']==320,(id,m)
 results.append('All 12 screens at 320px with simulated 44/34px safe area passed')
 page.evaluate('localStorage.clear()');b.close()
(r/'ui-audit/records-interaction-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');print('\n'.join(results))
