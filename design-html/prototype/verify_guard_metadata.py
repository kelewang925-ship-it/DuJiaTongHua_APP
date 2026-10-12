"""Guard input state must ignore presentation IDs while preserving real dirty edits."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import seed_onboarding
from verify_pet_controls import ROOT,BASE,source

def main():
    before='--before'in sys.argv;files=source();rows=[]
    with sync_playwright()as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for mode in ['clean-back','clean-link','dirty-back','dirty-browser']:
            c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));r=dict(case=mode)
            try:
                seed_onboarding(p,'m02-p03');old=p.evaluate('JSON.stringify({...localStorage})')
                if mode.startswith('dirty'):
                    p.locator('.code input').first.fill('Z9')
                    def leave():p.go_back()if mode=='dirty-browser'else p.locator('.back').click()
                    leave();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('.code input').first).to_have_value('Z9');assert p.evaluate('JSON.stringify({...localStorage})')==old;leave();p.get_by_role('button',name='放弃修改',exact=True).click();p.wait_for_url('**/m02-p01.html*')
                else:
                    p.locator('.back'if mode=='clean-back'else'.later a').click();p.wait_for_url('**/m02-p01.html*');expect(p.locator('dialog[open]')).to_have_count(0)
                assert p.evaluate('JSON.stringify({...localStorage})')==old;assert not errors;r['passed']=True
            except Exception:r.update(passed=False,failure=traceback.format_exc()[-1600:])
            r['errors']=errors;rows.append(r);c.close();assert source()==files
        c=b.new_context();p=c.new_page();p.goto(BASE+'prototype/components.html');r=dict(case='stable-id-and-real-field-changes')
        try:
            observed=p.evaluate('''()=>{const f=document.createElement('form'),t=document.createElement('input'),cb=document.createElement('input'),s=document.createElement('select'),a=document.createElement('textarea');t.value='原值';cb.type='checkbox';s.innerHTML='<option value="own">自己</option><option value="shared">共同</option>';a.value='原文';f.append(t,cb,s,a);document.body.append(f);window.__metadataForm=f;window.__metadataGuard=PrototypeUI.guard(f,{fallback:'review.html'});t.id='presentation-id';const metadataClean=!__metadataGuard.dirty();t.value='实际编辑';const textDirty=__metadataGuard.dirty();__metadataGuard.commit();t.name='different-business-field';const nameDirty=__metadataGuard.dirty();__metadataGuard.commit();cb.checked=true;const checkboxDirty=__metadataGuard.dirty();__metadataGuard.commit();s.value='shared';const selectDirty=__metadataGuard.dirty();__metadataGuard.commit();a.value='新正文';const textareaDirty=__metadataGuard.dirty();__metadataGuard.commit();a.remove();const removedDirty=__metadataGuard.dirty();return {metadataClean,textDirty,nameDirty,checkboxDirty,selectDirty,textareaDirty,removedDirty}}''');r['observed']=observed;assert all(observed.values()),observed;r['passed']=True
        except Exception:r.update(passed=False,failure=traceback.format_exc()[-1400:])
        rows.append(r);c.close()
        c=b.new_context();p=c.new_page();p.goto(BASE+'prototype/components.html');r=dict(case='sheet-adoption-clean-and-dirty')
        try:
            p.evaluate('''()=>{const f=document.createElement('form'),i=document.createElement('input');i.value='原值';i.setAttribute('aria-label','原生字段');f.append(i);const guard=PrototypeUI.protectSheet(f);PrototypeUI.sheet({title:'原生保护',content:f,actions:[],beforeClose:guard.beforeClose})}''');expect(p.get_by_label('原生字段',exact=True)).to_be_visible();p.keyboard.press('Escape');expect(p.locator('dialog[open]')).to_have_count(0)
            p.evaluate('''()=>{const f=document.createElement('form'),i=document.createElement('input');i.value='原值';i.setAttribute('aria-label','原生字段');f.append(i);const guard=PrototypeUI.protectSheet(f);PrototypeUI.sheet({title:'原生保护',content:f,actions:[],beforeClose:guard.beforeClose})}''');p.get_by_label('原生字段',exact=True).fill('真正修改');p.keyboard.press('Escape');expect(p.locator('.prototype-sheet-discard')).to_be_visible();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.get_by_label('原生字段',exact=True)).to_have_value('真正修改');p.keyboard.press('Escape');p.get_by_role('button',name='放弃修改',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);r['passed']=True
        except Exception:r.update(passed=False,failure=traceback.format_exc()[-1400:])
        rows.append(r);c.close();b.close()
    path=ROOT/('evidence/baseline/guard-metadata-before.json'if before else'evidence/current/guard-metadata-results.json');path.write_text(json.dumps(dict(files=files,results=rows,accepted_pages=0,scope='Two untouched invite exits, actual dirty button/browser back keep/discard, stable presentation ID vs real value/name/checked/select/textarea/removal changes and native modal field protection.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(rows),passed=sum(r['passed']for r in rows))));raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
