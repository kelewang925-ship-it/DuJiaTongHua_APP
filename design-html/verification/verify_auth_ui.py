import json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
results=[]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    page=b.new_page(viewport={'width':320,'height':640})
    def load(n): page.goto((root/'pages'/f'm01-p{n:02d}.html').as_uri())
    load(3)
    page.locator('[name=nickname]').fill('小满的很长很长的童话昵称'*8)
    page.locator('[name=phone]').fill('13812345678')
    page.locator('[name=code]').fill('123456')
    page.locator('#password').fill('demo123456')
    page.locator('#eye').click()
    assert page.locator('#password').get_attribute('type')=='text'
    assert page.locator('#eye').get_attribute('aria-label')=='隐藏密码'
    page.locator('.submit').click()
    assert page.locator('.toast').is_visible()
    assert page.evaluate('document.documentElement.scrollWidth')==320
    results.append('m01-p03 long nickname, password visibility and valid form passed at 320px')
    load(5)
    page.locator('#password').fill('abc12345');page.locator('#confirm').fill('abc12345')
    page.locator('.eye').first.click()
    assert page.locator('#password').get_attribute('type')=='text'
    assert page.locator('.eye').first.bounding_box()['x']>200
    page.locator('.submit').click();assert page.locator('.toast').is_visible()
    results.append('m01-p05 eye position, visibility and reset demo passed')
    load(6)
    for _ in range(4):
        page.locator('#password').fill('abc12345');page.locator('.retry').click()
    assert page.locator('.retry').is_disabled()
    assert float(page.locator('.retry').evaluate('el=>getComputedStyle(el).opacity'))<1
    results.append('m01-p06 retry count and visible disabled state passed')
    load(7)
    page.locator('.code input').first.fill('5')
    assert page.locator('.code input').nth(1).evaluate('el=>el===document.activeElement')
    for i in range(6):page.locator('.code input').nth(i).fill(str(i))
    page.locator('.verify').click();assert page.locator('.toast').is_visible()
    results.append('m01-p07 OTP auto-focus and complete-code feedback passed')
    page.set_viewport_size({'width':320,'height':740})
    for n in range(1,9):
        load(n)
        page.evaluate('document.fonts.ready')
        page.locator('.screen').screenshot(path=str(root/'ui-audit/evidence/after'/f'm01-p{n:02}-320.png'))
    page.set_viewport_size({'width':390,'height':826})
    for n in range(1,9):
        load(n)
        page.add_style_tag(content=':root{--ui-safe-top:44px;--ui-safe-bottom:34px}')
        bounds=page.locator('.screen').bounding_box()
        assert bounds['y']>=44
        assert page.evaluate('document.documentElement.scrollHeight')>=bounds['height']+78-2
        assert page.evaluate('document.documentElement.scrollWidth')==390
    results.append('all 8 pages simulated 44px top and 34px bottom safe areas passed')
    b.close()
(root/'ui-audit'/'auth-interaction-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('\n'.join(results))
