"""Actual form entries under short-viewport pressure; no real IME claim."""
import argparse
import hashlib
import json
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from audit_hidden_overlays import MODULES, declarations
from verify_overlay_form_saves import SPECS, CANDIDATES, TEXT, fill
from verify_pet_controls import ROOT, DEMO, BASE, source


def bounds(dialog, target):
    value = target.evaluate('e=>{const r=e.getBoundingClientRect(),d=e.closest("dialog").getBoundingClientRect();return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,dialogTop:d.top,dialogBottom:d.bottom,height:innerHeight,width:innerWidth}}')
    assert value['top'] >= max(0,value['dialogTop'])-1 and value['bottom'] <= min(value['height'],value['dialogBottom'])+1, value
    assert value['left'] >= -1 and value['right'] <= value['width']+1, value
    return value


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--baseline',action='store_true'); parser.add_argument('--indices'); args=parser.parse_args()
    indices = [int(v) for v in args.indices.split(',')] if args.indices else list(SPECS)
    out=ROOT/('evidence/baseline/overlay-entry-focus' if args.baseline else 'evidence/current/overlay-entry-focus'); out.mkdir(parents=True,exist_ok=True)
    raw=(ROOT/'evidence/current/hidden-overlay-observations.json').read_bytes(); candidates=json.loads(raw)['results']; fixtures={k:declarations(v) for k,v in MODULES.items()}
    files=source(); styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')}; rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
        for width in [320,375,390,414,430]:
            for index in indices:
                item=candidates[index]; values,key,predicate=SPECS[index]; c=browser.new_context(viewport=dict(width=width,height=420),reduced_motion='reduce'); p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
                row=dict(index=index,page=item['page'],width=width)
                try:
                    fixtures[item['group']]['seed'](p,item['page']); trigger=p.locator(item['selector']);trigger.click()
                    dialog=p.locator('dialog[open]');heading=dialog.locator('h2');expect(heading).to_have_text(item['overlays'][0]['title'])
                    if index==72:p.screenshot(path=str(out/f'entry-72-{width}.png'),full_page=True)
                    row['entry']=heading.evaluate('e=>{const r=e.getBoundingClientRect(),d=e.closest("dialog").getBoundingClientRect();return {headingTop:r.top,headingBottom:r.bottom,dialogTop:d.top,dialogBottom:d.bottom,focused:e===document.activeElement,scrollTop:e.closest("dialog").scrollTop}}')
                    bounds(dialog,heading)
                    expect(heading).to_be_focused();expect(heading).to_have_attribute('tabindex','-1')
                    form=dialog.locator('form');fields=form.locator('input:not([type=hidden]):visible,textarea:visible,select:visible');p.keyboard.press('Tab');expect(fields.first).to_be_focused()
                    p.set_viewport_size(dict(width=width,height=844))
                    for field in fields.all():
                        if field.evaluate('e=>e.tagName')=='TEXTAREA':
                            field.fill('我们一起记下很长的回忆，'*100)
                            maximum=field.evaluate('e=>e.maxLength');assert maximum<0 or len(field.input_value())<=maximum
                    fill(form,values)
                    before=form.evaluate('e=>JSON.stringify([...e.querySelectorAll("input,textarea,select")].map(v=>v.value))')
                    p.set_viewport_size(dict(width=width,height=420))
                    for field in fields.all():
                        field.focus();field.evaluate('e=>e.scrollIntoView({block:"nearest"})');bounds(dialog,field)
                    assert form.evaluate('e=>JSON.stringify([...e.querySelectorAll("input,textarea,select")].map(v=>v.value))')==before
                    submit=form.locator('[type=submit]');submit.scroll_into_view_if_needed();bounds(dialog,submit);submit.click()
                    expect(p.locator('dialog[open]')).to_have_count(0)
                    if index in CANDIDATES:
                        parent,preview=CANDIDATES[index];expect(p.locator(preview)).to_contain_text(TEXT);p.set_viewport_size(dict(width=width,height=844));p.locator(parent).click()
                    p.wait_for_function('arg=>{const d=JSON.parse(localStorage.getItem(arg.key)),text=arg.text;return '+predicate+'}',arg=dict(key=key,text=TEXT))
                    if index in [84,118,122]:p.wait_for_url('**/m07-p18.html*' if index==84 else '**/m08-p13.html*' if index==118 else '**/m08-p14.html*')
                    assert not errors,errors;row.update(passed=True,persisted=True)
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-2400:],errors=errors)
                rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+str(index)+' '+str(width),flush=True);c.close()
        if not args.baseline:
            c=browser.new_context(viewport=dict(width=320,height=420),reduced_motion='reduce');p=c.new_page();p.goto(BASE+'prototype/components.html')
            for variant in ['ordinary-form','danger-form','confirmation','plain-sheet']:
                row=dict(case=variant)
                try:
                    p.evaluate('''variant=>{const UI=PrototypeUI,trigger=UI.components.button('入口',()=>{let content=null;if(variant.endsWith('form')){content=document.createElement('form');content.append(UI.components.field({label:'内容'}).root,UI.components.button('提交',null,{variant:variant==='danger-form'?'danger':'primary'}));}window.__result=UI.modal({title:'焦点测试',content,actions:content?[]:null,sheet:variant.endsWith('form')||variant==='plain-sheet',cancel:'取消',confirm:'确认'});});trigger.id='entry-trigger';document.body.append(trigger);trigger.focus();}''',variant)
                    p.locator('#entry-trigger').click();dialog=p.locator('dialog[open]')
                    if variant=='ordinary-form':expect(dialog.locator('h2')).to_be_focused()
                    else:expect(dialog.get_by_role('button',name='确认' if variant=='plain-sheet' else '取消',exact=True)).to_be_focused()
                    p.keyboard.press('Escape');expect(p.locator('dialog[open]')).to_have_count(0);expect(p.locator('#entry-trigger')).to_be_focused();p.locator('#entry-trigger').evaluate('e=>e.remove()');row['passed']=True
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-1800:])
                rows.append(row)
            c.close()
        browser.close()
    assert source()==files
    report=dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),locator_candidates_sha256=hashlib.sha256(raw).hexdigest(),results=rows,scope='Five widths,420px layout viewport reduced from844; actual entry and save. Native focus/scroll reachability and long-text entry. No real Android/iOS IME or screen-reader acceptance.')
    (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)


if __name__=='__main__':main()
