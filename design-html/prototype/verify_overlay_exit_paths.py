"""Exercise real closure paths for observed overlays and dirty save forms."""
import hashlib
import json
import traceback
from urllib.request import urlopen
from playwright.sync_api import sync_playwright, expect
from audit_runtime import INIT
from audit_hidden_overlays import MODULES, declarations, seed_onboarding
from verify_pet_controls import ROOT, BASE, source

OUT=ROOT/'evidence/current'
SAFE_CLOSE=['取消','关闭','知道了','先看看','继续编辑','继续生成','继续照顾','继续使用','继续创建时刻']

def close(page,method):
    dialog=page.locator('dialog[open]')
    if method=='button':
        cancel=dialog.locator('[data-cancel=true]')
        if cancel.count():cancel.click();return
        for name in SAFE_CLOSE:
            button=dialog.get_by_role('button',name=name,exact=True)
            if button.count()and button.first.is_visible()and button.first.is_enabled():button.first.click();return
        raise AssertionError('No declared safe close action')
    elif method=='back':page.go_back()
    elif method=='backdrop':page.mouse.click(1,1)
    elif method=='drag':
        box=dialog.locator('.prototype-sheet-handle').bounding_box();assert box
        x=box['x']+box['width']/2;y=box['y']+box['height']/2
        page.mouse.move(x,y);page.mouse.down();page.mouse.move(x,y+110,steps=8);page.mouse.up()
    else:raise AssertionError(method)

def change_field(form):
    fields=form.locator('input:not([type=file]):not([type=hidden]),textarea,select')
    for index in range(fields.count()):
        field=fields.nth(index)
        if not field.is_visible()or not field.is_enabled()or field.get_attribute('readonly')is not None:continue
        tag=field.evaluate('e=>e.tagName');kind=field.get_attribute('type')or'text'
        if tag=='SELECT':
            old=field.input_value();options=field.locator('option').evaluate_all('items=>items.filter(e=>!e.disabled).map(e=>e.value)');other=next((v for v in options if v!=old),None)
            if other is None:continue
            field.select_option(other)
        elif kind in ['checkbox','radio']:
            if kind=='radio'and field.is_checked():continue
            field.set_checked(not field.is_checked())
        else:
            old=field.input_value()
            value='21:45'if kind=='time'else'#cc8844'if kind=='color'else'2026-11-01'if kind=='date'else'未保存的修改'
            if value==old:value='22:30'if kind=='time'else'另一份修改'
            field.fill(value)
        return form.evaluate('f=>JSON.stringify([...f.querySelectorAll("input,textarea,select")].map(e=>[e.value,e.checked]))')
    raise AssertionError('No editable field with a distinct candidate')

def main():
    files=source();raw=(OUT/'hidden-overlay-observations.json').read_bytes();observations=json.loads(raw)
    assert observations['files']==files and observations['completed']==observations['candidates']
    for path,digest in files.items():
        served=path.replace('custom/','pages/',1)if path.startswith('custom/')else path
        with urlopen(BASE+served,timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==digest
    fixtures={group:declarations(name)for group,name in MODULES.items()};cases=[];results=[]
    for index,row in enumerate(observations['results']):
        if not row['overlays']:continue
        assert row['passed']and len(row['overlays'])==1
        overlay=row['overlays'][0];methods=['button','back','backdrop']
        if 'prototype-sheet' in overlay['html'].split('>')[0]:methods.append('drag')
        for method in methods:cases.append((index,method,False))
        if any(c['type']=='submit'and c['visible']for c in overlay['controls']):
            for method in methods:cases.append((index,method,True))
    def save():
        assert source()==files
        value=dict(files=files,observations_sha256=hashlib.sha256(raw).hexdigest(),cases=len(cases),completed=len(results),results=results,
            scope='Observed representative overlays, clean close and dirty save forms; nested actions and submission cancellation remain pending',accepted_pages=0)
        temporary=OUT/'overlay-exit-path-results.json.tmp';temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temporary.replace(OUT/'overlay-exit-path-results.json')
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for number,(index,method,dirty)in enumerate(cases):
            original=observations['results'][index];context=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',accept_downloads=True)
            context.add_init_script(INIT);page=context.new_page();page.set_default_timeout(4500);page.set_default_navigation_timeout(15000)
            errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
            row=dict(observation_index=index,page=original['page'],trigger=original['selector'],title=original['overlays'][0]['title'],method=method,dirty=dirty)
            try:
                if original['group']=='onboarding':seed_onboarding(page,original['page'])
                else:fixtures[original['group']]['seed'](page,original['page'])
                trigger=page.locator(original['selector']);trigger.click();dialog=page.locator('dialog[open]');expect(dialog).to_have_count(1)
                expect(dialog.locator('h2')).to_have_text(row['title'])
                before_url=page.url;before_store=page.evaluate('JSON.stringify({...localStorage})')
                if dirty:
                    form=dialog.locator('form');expect(form).to_have_count(1);snapshot=change_field(form)
                    close(page,method);warning=dialog.locator('.prototype-sheet-discard');expect(warning).to_be_visible();expect(dialog).to_have_count(1)
                    warning.get_by_role('button',name='继续编辑',exact=True).click();expect(warning).to_have_count(0);expect(form).to_be_visible()
                    assert snapshot==form.evaluate('f=>JSON.stringify([...f.querySelectorAll("input,textarea,select")].map(e=>[e.value,e.checked]))'),'Continue lost candidate fields'
                    assert page.url==before_url and before_store==page.evaluate('JSON.stringify({...localStorage})')
                    close(page,method);expect(warning).to_be_visible();warning.get_by_role('button',name='放弃修改',exact=True).click()
                else:close(page,method)
                expect(page.locator('dialog[open]')).to_have_count(0)
                assert page.url==before_url,'Closing left the underlying page'
                assert before_store==page.evaluate('JSON.stringify({...localStorage})'),'Closing changed stored data'
                expect(trigger).to_be_focused();assert not errors,errors
                row.update(passed=True,storage_preserved=True,underlying_page_preserved=True,focus_returned=True)
            except Exception:row.update(passed=False,failure=traceback.format_exc()[-2500:])
            row['errors']=errors;results.append(row);context.close();save()
            print(('PASS 'if row['passed']else'FAIL ')+str(number+1)+'/'+str(len(cases))+' '+row['page']+' '+method+(' dirty'if dirty else' clean'),flush=True)
        browser.close()
    save();print(json.dumps(dict(cases=len(cases),passed=sum(r['passed']for r in results),dirty=sum(r['dirty']for r in results))))
    raise SystemExit(0 if all(r['passed']for r in results)else 1)

if __name__=='__main__':main()
