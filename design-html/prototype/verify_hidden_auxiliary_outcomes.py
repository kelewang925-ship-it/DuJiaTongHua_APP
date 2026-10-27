"""Explicit settings, informational and empty-state hidden business contracts."""
import hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import MODULES,declarations
from audit_runtime import INIT
from verify_pet_controls import ROOT,source

OUT=ROOT/'evidence/current/hidden-auxiliary-outcomes'
CASES=[(53,'简体中文'),(53,'English · 尚无译稿'),(60,'仅自己可见'),(60,'共同可见'),(69,'知道了'),(71,'知道了'),(98,'知道了'),(70,'去领养'),(20,'去写日记')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def store(p):return p.evaluate('({...localStorage})')

def main():
    OUT.mkdir(exist_ok=True);files=source();observed_path=ROOT/'evidence/current/hidden-overlay-observations.json';observed=json.loads(observed_path.read_text(encoding='utf-8'))
    fixtures={k:declarations(v) for k,v in MODULES.items()};rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index,label in CASES:
            context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');context.add_init_script(INIT)
            page=context.new_page();page.set_default_timeout(6000);page.set_default_navigation_timeout(20000)
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)));row=dict(observation_index=index,control_label=label,passed=False,errors=errors)
            try:
                original=observed['results'][index];fixtures[original['group']]['seed'](page,original['page'])
                if index==53 and label=='简体中文':
                    page.evaluate('()=>{const k="dujia-prototype-preferences",v=JSON.parse(localStorage.getItem(k));v.language="unselected";localStorage.setItem(k,JSON.stringify(v))}');page.reload()
                if index==60:
                    page.evaluate('()=>{const k="dujia-privacy",v=PrototypePreferences.privacy();v.scope="仅自己可见";v.shared=true;localStorage.setItem(k,JSON.stringify(v))}');page.reload()
                before=store(page);url=page.url
                page.locator(original['selector']).click();dialog=page.locator('dialog[open]')
                expect(dialog.locator('h2')).to_have_text(original['overlays'][0]['title'])
                button=dialog.get_by_role('button',name=label,exact=True)
                if index==53 and label.startswith('English'):
                    expect(button).to_be_disabled();button.evaluate('b=>b.click()')
                    expect(dialog).to_have_count(1);assert store(page)==before and page.url==url
                    expect(dialog.get_by_role('button',name='简体中文',exact=True)).to_be_focused()
                    page.keyboard.press('Tab');expect(dialog.get_by_role('button',name='取消',exact=True)).to_be_focused()
                    page.keyboard.press('Tab');expect(dialog.get_by_role('button',name='简体中文',exact=True)).to_be_focused()
                    row['result']='English remains disabled; DOM click cannot activate it; keyboard skips it; no data or route change'
                else:
                    button.click();expect(page.locator('dialog[open]')).to_have_count(0)
                    if index in [53,60]:
                        key='dujia-prototype-preferences' if index==53 else 'dujia-privacy';field='language' if index==53 else 'scope';wanted='zh-CN' if index==53 else label
                        after=store(page);old=json.loads(before[key]);new=json.loads(after[key]);assert new[field]==wanted
                        old.pop(field,None);new.pop(field,None);assert old==new
                        before.pop(key);after.pop(key);assert before==after
                        page.reload()
                        if index==53:assert page.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-preferences")).language')=='zh-CN'
                        else:expect(page.locator('#scope span')).to_have_text(label)
                        row.update(result=f'only {key}.{field} changes to {wanted}; reload preserves result',persisted_key=key,persisted_field=field)
                    elif index in [70,20]:
                        destination='m07-p02' if index==70 else 'm03-p05';page.wait_for_url('**/'+destination+'.html*')
                        assert store(page)==before;row.update(destination=destination,result='empty-state CTA navigates to '+destination+' without writing data')
                    else:
                        assert store(page)==before and page.url==url
                        row['result']='informational confirm closes; same page and all local data preserved'
                assert not errors;row['passed']=True
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);context.close();assert source()==files
            report=dict(files=files,script_sha256=sha(Path(__file__)),observations_sha256=sha(observed_path),fixture_scripts={v:sha(ROOT/v) for v in MODULES.values()},expected_cases=len(CASES),results=rows,accepted_pages=0)
            temporary=OUT/'results.json.tmp';temporary.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temporary.replace(OUT/'results.json')
            print(('PASS ' if row['passed'] else 'FAIL ')+str(index)+' '+label,flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
