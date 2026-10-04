from pathlib import Path
import json
from playwright.sync_api import sync_playwright
r=Path('design-html').resolve();results=[];out=r/'ui-audit/evidence/after'
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');page=b.new_page(viewport={'width':320,'height':740},accept_downloads=True)
 def go(id):
  page.goto((r/'pages'/f'{id}.html').as_uri());page.evaluate('document.fonts.ready')
 def once(answer=None):page.once('dialog',lambda d:d.accept(answer) if answer is not None else d.dismiss())
 go('m06-p02');page.evaluate('localStorage.clear()');page.reload();long='很长的资料文字'*40
 for sel in ['nickname','birthday','saying']:page.locator('#'+sel).fill(long)
 page.locator('#color').fill('#889d78');assert page.locator('#color').evaluate('e=>getComputedStyle(e).opacity')=='1'
 page.locator('#avatar').set_input_files(str(r/'assets/m06-p01-source.webp'));page.wait_for_function("document.querySelector('#avatar-preview').naturalWidth>0");page.locator('#save').click();assert page.locator('#toast').is_visible();page.reload();assert page.locator('#nickname').input_value()==long and page.locator('#color').input_value()=='#889d78';assert page.locator('#avatar-preview').is_visible();assert page.evaluate('document.documentElement.scrollWidth')==320
 go('m06-p01');assert page.locator('.name').inner_text()==long+' ♡';assert page.locator('.name').evaluate('e=>getComputedStyle(e).textOverflow')=='ellipsis';assert page.locator('.name').bounding_box()['x']+page.locator('.name').bounding_box()['width']<320;results.append('Profile long inputs/color/avatar save and reload; home nickname bounded at 320px')
 go('m06-p03');once(long);page.locator('.nick').click();assert page.evaluate("localStorage.getItem('dujia-joint-name')")==long;page.reload();assert page.locator('#joint-name').inner_text()==long;assert page.locator('#joint-name').evaluate('e=>getComputedStyle(e).overflow')=='hidden';page.locator('.unlink').click();assert page.locator('#toast').inner_text()=='解除关联需要双方确认';results.append('Joint nickname prompt/save/reload with bounded text; existing unlink feedback preserved')
 go('m06-p05');once(long);page.locator('.daily').click();assert json.loads(page.evaluate("localStorage.getItem('dujia-tags')"))['daily']==long;page.reload();assert page.locator('.daily').inner_text()==long;assert page.evaluate('document.documentElement.scrollWidth')==320;once('新增标签');page.locator('.plus').click();assert json.loads(page.evaluate("localStorage.getItem('dujia-extra-tags')"))==['新增标签'];assert page.locator('#toast').is_visible();results.append('Long tag edit persistence and new-tag prompt/toast passed')
 go('m06-p06');page.locator('.open').click();assert '当前未接入支付' in page.locator('#toast').inner_text();page.locator('.details').click();assert '会员说明' in page.locator('#toast').inner_text();results.append('Membership demo and details feedback preserved')
 go('m06-p07');page.locator('.language').click();assert '简体中文' in page.locator('#toast').inner_text();once();page.locator('.logout').click();assert page.url.endswith('m06-p07.html');page.locator('.security').click();page.wait_for_url('**/m06-p08.html');once();page.locator('.password').click();once('');page.locator('.devices').click();page.locator('.back').click();page.wait_for_url('**/m06-p07.html');results.append('Settings/security navigation and existing dialogs/logout cancellation passed')
 go('m06-p09');page.locator('#scope').click();assert page.locator('#scope span').inner_text()=='共同可见'
 for sw in page.locator('.switch').all():sw.click();assert sw.get_attribute('aria-checked')=='false';assert sw.evaluate("e=>getComputedStyle(e,'::before').backgroundColor")=='rgb(213, 203, 192)'
 page.reload();assert all(sw.get_attribute('aria-checked')=='false' for sw in page.locator('.switch').all());page.locator('.screen').screenshot(path=str(out/'m06-p09-off.png'));results.append('Privacy scope and all four switches show/persist disabled state')
 go('m06-p10')
 for sw in page.locator('.switch').all():sw.click()
 page.reload();assert all(sw.get_attribute('aria-checked')=='false' for sw in page.locator('.switch').all());bounds=page.locator('.s5').bounding_box();assert bounds['y']+bounds['height']<=page.locator('.screen').bounding_box()['height'];page.locator('.screen').screenshot(path=str(out/'m06-p10-off.png'));results.append('Five notification switches persist state; final 44px switch stays within 320px canvas')
 go('m06-p11');page.locator('#auto').click();page.reload();assert page.locator('#auto').get_attribute('aria-checked')=='false';page.locator('#backup').click();assert page.evaluate("localStorage.getItem('dujia-last-backup')")
 with page.expect_download() as download:page.locator('#export').click()
 d=download.value;assert d.suggested_filename=='dujia-records.json';data=json.loads(Path(d.path()).read_text(encoding='utf-8'));assert json.loads(data['profile'])['nickname']==long;page.locator('#cache').click();assert page.locator('#cache span').inner_text()=='0 MB';assert page.evaluate("localStorage.getItem('dujia-profile')") is not None;page.locator('.screen').screenshot(path=str(out/'m06-p11-off.png'));results.append('Auto-backup persistence, backup timestamp, JSON export and cache feedback passed; profile retained')
 go('m06-p12');once(long);page.locator('.feedback').click();assert page.evaluate("localStorage.getItem('dujia-feedback-draft')")==long;assert page.locator('#toast').is_visible();page.locator('.updates').click();assert page.locator('#toast').inner_text()=='当前已是最新版本';results.append('Feedback draft prompt/save and update demo passed')
 page.evaluate('localStorage.clear()')
 for i in range(1,13):
  id=f'm06-p{i:02}';go(id);page.locator('.screen').screenshot(path=str(out/f'{id}-320.png'));page.evaluate("document.documentElement.style.setProperty('--ui-safe-top','44px');document.documentElement.style.setProperty('--ui-safe-bottom','34px')");m=page.evaluate("()=>{const r=document.querySelector('.screen').getBoundingClientRect();return {y:r.y,h:r.height,doc:document.documentElement.scrollHeight,w:document.documentElement.scrollWidth}}");assert m['y']>=44 and m['doc']>=m['h']+77 and m['w']==320,(id,m)
 results.append('All 12 pages at 320px with 44/34px simulated safe area passed');b.close()
(r/'ui-audit/settings-interaction-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');print('\n'.join(results))
