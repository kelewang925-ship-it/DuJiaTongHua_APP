"""Execute current overlay field adoption and save/invalid/quota recovery at five widths."""
import hashlib,json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import MODULES,declarations
from verify_overlay_form_saves import SPECS,TEXT,fill,quota,activate,storage,snapshot
from verify_pet_controls import ROOT,BASE,source

INDICES=[17,42,45,46,52,55,57,64,72,82,84,85,97,129]

def main():
    files=source();baseline='--baseline'in sys.argv;rows=[];raw=(ROOT/'evidence/current/hidden-overlay-observations.json').read_bytes();candidates=json.loads(raw)['results']
    fixtures={group:declarations(name)for group,name in MODULES.items()}
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in ([390]if baseline else[320,360,390,414,430]):
            for index in INDICES:
                original=candidates[index];values,key,predicate=SPECS[index];context=browser.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=context.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row={'index':index,'page':original['page'],'width':width,'fields':list(values)}
                try:
                    fixtures[original['group']]['seed'](p,original['page']);p.locator(original['selector']).click();dialog=p.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text(original['overlays'][0]['title']);form=dialog.locator('form');submit=form.locator('[type=submit]');before=storage(p)
                    for label in values:
                        field=form.get_by_label(label,exact=True);assert field.evaluate('e=>!!e.closest(".prototype-component-field")'),'Field still uses local implementation'
                        assert field.get_attribute('aria-labelledby')and field.get_attribute('aria-describedby')
                        field.evaluate('e=>e.scrollIntoView({block:"center"})');g=field.evaluate('e=>{const r=e.getBoundingClientRect();return {width:r.width,height:r.height,left:r.left,right:r.right}}');assert g['width']>=44 and g['height']>=44 and g['left']>=-1 and g['right']<=width+1,g
                    if index!=52:
                        for label in values:
                            field=form.get_by_label(label,exact=True)
                            if field.evaluate('e=>e.tagName')!='SELECT':field.fill('')
                        submit.click();invalid=form.locator('[aria-invalid=true]').first;expect(invalid).to_be_visible();linked=p.locator('#'+invalid.get_attribute('aria-describedby'));expect(linked).to_be_visible();expect(linked).to_have_attribute('role','alert');assert storage(p)==before;row['inline_error_verified']=True
                    fill(form,values)
                    expect(form.locator('[aria-invalid=true]')).to_have_count(0)
                    candidate=snapshot(form);quota(p,key);activate(submit);expect(p.locator('.prototype-toast')).to_contain_text('空间不足');expect(submit).to_be_enabled();assert storage(p)==before;assert snapshot(form)==candidate;assert p.evaluate('window.__overlayQuota')==1
                    activate(submit);p.wait_for_function('arg=>{const d=JSON.parse(localStorage.getItem(arg.key)),text=arg.text;return '+predicate+'}',arg={'key':key,'text':TEXT});expect(p.locator('dialog[open]')).to_have_count(0)
                    if index==84:p.wait_for_url('**/m07-p18.html*')
                    assert not errors,errors;row.update(passed=True,quota_retry_preserved=True,stored_predicate=predicate)
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-2200:])
                row['errors']=errors;rows.append(row);context.close();assert source()==files
            print(str(width)+'px '+str(sum(r['passed']for r in rows if r['width']==width))+'/14',flush=True)
        context=browser.new_context();p=context.new_page();row={'case':'select-and-error-association-contract'}
        try:
            p.goto(BASE+'prototype/components.html');value=p.evaluate('''()=>{const f=PrototypeUI.components.field({label:'范围',options:[['own','仅自己'],['shared','共同']],value:'shared',disabled:true});document.body.append(f.root);PrototypeUI.fieldError(f.input,'请选择范围');const disabledBefore=f.input.disabled,errorVisible=!f.error.hidden&&f.error.textContent==='请选择范围';f.input.disabled=false;f.input.dispatchEvent(new Event('input'));const result={tag:f.input.tagName,value:f.input.value,options:f.input.options?.length,disabledBefore,errorVisible,cleared:f.error.hidden&&f.input.getAttribute('aria-invalid')==='false',described:f.input.getAttribute('aria-describedby')===f.error.id};f.root.remove();return result}''');row['observed']=value;assert value=={'tag':'SELECT','value':'shared','options':2,'disabledBefore':True,'errorVisible':True,'cleared':True,'described':True},value;row['passed']=True
        except Exception:row.update(passed=False,failure=traceback.format_exc()[-1600:])
        rows.append(row);context.close();browser.close()
    path=ROOT/('evidence/baseline/shared-overlay-fields-before.json'if baseline else'evidence/current/shared-overlay-fields-results.json');path.write_text(json.dumps({'files':files,'locator_candidates_sha256':hashlib.sha256(raw).hexdigest(),'results':rows,'scope':'14 actual overlay entries, shared field semantics/inline validation/five-width dimensions and real duplicate-save/quota retry. Old overlay inventory provides locator candidates only.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'cases':len(rows),'passed':sum(r['passed']for r in rows)}));raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
