from pathlib import Path
import json, sys, traceback
from playwright.sync_api import sync_playwright, expect

BASE = 'http://127.0.0.1:8765/'
OUT = Path(__file__).resolve().parent / ('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current')

def style(p, selector):
    return p.locator(selector).evaluate('e=>{const s=getComputedStyle(e);return {animation:s.animationName,duration:s.animationDuration,transition:s.transitionDuration,transform:s.transform}}')

def entrance(p):
    p.goto(BASE+'pages/m03-p05.html')
    s = style(p, '.screen')
    assert s['animation'] == 'prototype-page-in' and s['duration'] == '0.22s', s
    p.wait_for_timeout(260)
    assert style(p, '.screen')['transform'] == 'none'
    assert p.evaluate('document.documentElement.scrollWidth') == 390
    expect(p.locator('[name=title]')).to_be_visible()

def overlays(p):
    p.goto(BASE+'prototype/components.html')
    for label, name, duration, close_duration in [('确认弹窗','prototype-modal-in','0.22s','0.16s'),('底部选择器','prototype-sheet-in','0.28s','0.22s')]:
        trigger = p.get_by_role('button',name=label,exact=True)
        trigger.click()
        s = style(p,'dialog[open]')
        assert s['animation'] == name and s['duration'] == duration, s
        backdrop = p.locator('dialog[open]').evaluate("e=>{const s=getComputedStyle(e,'::backdrop');return [s.animationName,s.animationDuration]}")
        assert backdrop == ['prototype-backdrop-in','0.22s'], backdrop
        p.keyboard.press('Escape')
        s = style(p,'dialog.prototype-closing')
        assert close_duration in s['transition'], s
        expect(p.locator('dialog')).to_have_count(0)
        expect(trigger).to_be_focused()
        assert p.url.endswith('components.html')

def reduced(p):
    p.goto(BASE+'pages/m03-p05.html')
    assert style(p,'.screen')['animation'] == 'none'
    p.goto(BASE+'prototype/components.html')
    assert style(p,'.prototype-component-spinner')['animation'] == 'none'
    trigger = p.get_by_role('button',name='底部选择器',exact=True)
    assert style(p,'#buttons>button:first-child')['transition'] == '0s'
    trigger.click()
    assert style(p,'dialog')['animation'] == 'none'
    assert p.locator('dialog').evaluate("e=>getComputedStyle(e,'::backdrop').animationName") == 'none'
    p.keyboard.press('Escape')
    expect(p.locator('dialog')).to_have_count(0)
    expect(trigger).to_be_focused()

def preference(p):
    p.goto(BASE+'prototype/components.html')
    p.evaluate("localStorage.setItem('dujia-prototype-preferences',JSON.stringify({reduceMotion:true}))")
    reduced(p)
    assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-preferences')).reduceMotion") is True

def drag(p):
    p.goto(BASE+'prototype/components.html')
    trigger=p.get_by_role('button',name='底部选择器',exact=True)
    trigger.click()
    p.wait_for_timeout(310)
    box=p.locator('.prototype-sheet-handle').bounding_box()
    x,y=box['x']+box['width']/2,box['y']+box['height']/2
    p.mouse.move(x,y);p.mouse.down();p.mouse.move(x,y+95,steps=5);p.mouse.up()
    expect(p.locator('dialog')).to_have_count(0)
    expect(trigger).to_be_focused()
    assert p.url.endswith('components.html')

cases=[('page-enter-and-settle','no-preference',entrance),('modal-sheet-backdrop-close','no-preference',overlays),('system-reduced-motion','reduce',reduced),('saved-reduced-motion','no-preference',preference),('sheet-real-pointer-dismiss','no-preference',drag),('sheet-pointer-reduced-motion','reduce',drag)]
rows=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,motion,run in cases:
        context=browser.new_context(viewport={'width':390,'height':844},reduced_motion=motion)
        page=context.new_page();page.set_default_timeout(4500);errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        try:
            run(page);assert not errors,errors;row={'case':name,'passed':True}
        except Exception:
            row={'case':name,'passed':False,'failure':traceback.format_exc()[-2000:]}
        row.update(errors=errors,url=page.url);rows.append(row)
        print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True)
        context.close()
    browser.close()
(OUT/'motion-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(row['passed'] for row in rows) else 1)
