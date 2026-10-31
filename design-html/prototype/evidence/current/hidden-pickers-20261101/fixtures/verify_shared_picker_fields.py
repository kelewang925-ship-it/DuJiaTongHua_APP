"""Actual dynamic picker/filter/tag/two-factor controls; isolated browser data."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import MODULES,declarations,seed_onboarding
from verify_pet_controls import ROOT,source

SPECS=[('m02-p06','onboarding','[name=met]','选择相遇日期',{'选择相遇日期':'2026-01-01'},'[name=met]','2026年1月1日'),
('m02-p06','onboarding','[name=anniversary]','选择共同纪念日',{'纪念日重复周期':'yearly','纪念日期':'2026-01-01'},'[name=anniversary]','每年 1 月 1 日'),
('m03-p06','record','#filter','筛选日记',{'可见范围':'shared'},None,None),
('m03-p11','record','[name=date]','选择照片日期',{'选择照片日期':'2026-01-01'},'[name=date]','2026-01-01'),
('m03-p11','record','#add-tag','照片标签',{'编辑照片标签':'一起、旅行'},'[name=tag]','一起、旅行'),
('m04-p04','moment','[name=date]','发生日期',{'选择发生日期':'2026-01-01'},'[name=date]','2026-01-01'),
('m04-p09','time','[name=date]','纪念日日期',{'选择纪念日日期':'2026-12-24'},'[name=date]','2026-12-24'),
('m04-p13','time','[name=opening]','开启日期',{'胶囊开启日期':'2026-12-24'},'[name=opening]','2026-12-24'),
('m06-p02','settings','#birthday','你的生日',{'选择生日':'1998-06-21'},'#birthday','1998-06-21')]
def store(p):return p.evaluate('JSON.stringify({...localStorage})')
def main():
    files=source();baseline='--baseline'in sys.argv;rows=[];fixtures={k:declarations(v)for k,v in MODULES.items()if k!='onboarding'}
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in ([390]if baseline else[320,360,390,414,430]):
            for identifier,group,trigger,title,values,target,expected in SPECS:
                context=browser.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=context.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(page=identifier,trigger=trigger,width=width,title=title)
                try:
                    if group=='onboarding':seed_onboarding(p,identifier)
                    else:fixtures[group]['seed'](p,identifier)
                    before=store(p);parent=p.locator(target).input_value()if target else None
                    p.locator(trigger).click();dialog=p.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text(title)
                    properties={}
                    for label in values:
                        field=dialog.get_by_label(label,exact=True);assert field.evaluate('e=>!!e.closest(".prototype-component-field")'),'Raw modal field still local'
                        properties[label]=field.evaluate('e=>({tag:e.tagName,type:e.type,min:e.min,max:e.max,maxLength:e.maxLength,value:e.value})')
                        field.evaluate('e=>e.scrollIntoView({block:"center"})');rect=field.bounding_box();assert rect['width']>=44 and rect['height']>=44 and rect['x']>=-1 and rect['x']+rect['width']<=width+1,rect
                        p.evaluate('e=>PrototypeUI.fieldError(e,"请核对选择")',field.element_handle());expect(field).to_have_attribute('aria-invalid','true');error=dialog.locator('#'+field.get_attribute('aria-describedby'));expect(error).to_be_visible();expect(error).to_have_attribute('role','alert')
                        if properties[label]['tag']=='SELECT':field.select_option(values[label])
                        else:field.fill(values[label])
                        expect(field).to_have_attribute('aria-invalid','false')
                    assert store(p)==before
                    p.keyboard.press('Escape');expect(p.locator('dialog[open]')).to_have_count(0);assert store(p)==before
                    if target:expect(p.locator(target)).to_have_value(parent)
                    p.locator(trigger).click();dialog=p.locator('dialog[open]')
                    for label,value in values.items():
                        field=dialog.get_by_label(label,exact=True)
                        if field.evaluate('e=>e.tagName')=='SELECT':field.select_option(value)
                        else:field.fill(value)
                    dialog.locator('.prototype-modal-actions button').first.click();expect(p.locator('dialog[open]')).to_have_count(0)
                    if target:expect(p.locator(target)).to_have_value(expected);assert store(p)==before
                    else:
                        expect(p.locator('.prototype-diary-list')).not_to_contain_text('自己的日记');assert p.evaluate('JSON.parse(sessionStorage.getItem("dujia-diary-list-state")||"{}").visibility')=='shared'
                    assert not errors,errors;row.update(passed=True,properties=properties,cancel_preserved=True,apply_verified=True)
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-2000:])
                row['errors']=errors;rows.append(row);context.close();assert source()==files
            context=browser.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=context.new_page();row=dict(page='m06-p07',title='两步验证',width=width);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:
                fixtures['settings']['seed'](p,'m06-p07');p.evaluate('''()=>{const preferences=PrototypePreferences.preferences();localStorage.setItem('dujia-prototype-preferences',JSON.stringify({...preferences,twoFactor:true}));localStorage.setItem('dujia-prototype-session',JSON.stringify({loggedIn:false}));window.__twoFactorDone=null;PrototypePreferences.login('13812345678').then(v=>window.__twoFactorDone=v)}''');before=store(p);dialog=p.locator('dialog[open]');field=dialog.get_by_label('两步验证码',exact=True);assert field.evaluate('e=>!!e.closest(".prototype-component-field")');expect(field).to_have_attribute('maxlength','6');field.fill('000000');dialog.locator('[type=submit]').click();expect(field).to_have_attribute('aria-invalid','true');expect(dialog.locator('#'+field.get_attribute('aria-describedby'))).to_be_visible();assert store(p)==before
                field.fill('284631');expect(field).to_have_attribute('aria-invalid','false');p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","two-factor-verify")');dialog.locator('[type=submit]').click();expect(p.locator('.prototype-toast')).to_contain_text('验证未完成');expect(field).to_have_value('284631');assert store(p)==before;dialog.locator('[type=submit]').click();p.wait_for_function('window.__twoFactorDone===true');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-session")).phone')=='13812345678';assert not errors,errors;row.update(passed=True,invalid_preserved=True,failure_retry=True)
            except Exception:row.update(passed=False,failure=traceback.format_exc()[-2000:])
            row['errors']=errors;rows.append(row);context.close();assert source()==files;print(str(width)+'px '+str(sum(r['passed']for r in rows if r['width']==width))+'/10',flush=True)
        browser.close()
    path=ROOT/('evidence/baseline/shared-picker-fields-before.json'if baseline else'evidence/current/shared-picker-fields-results.json');path.write_text(json.dumps(dict(files=files,results=rows,accepted_pages=0,scope='Nine actual picker/filter/tag entrances plus local two-factor login function, five widths. Existing callbacks apply/cancel, storage/candidate/error clearing and two-factor demonstration failure/retry; not full auth/global/final visual acceptance.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(rows),passed=sum(r['passed']for r in rows))));raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
