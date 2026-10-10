"""Identity-confirmed account and pet deletion boundaries and recovery."""
import hashlib,json,traceback
from urllib.request import urlopen
from playwright.sync_api import sync_playwright,expect
from audit_runtime import INIT
from audit_hidden_overlays import declarations
from verify_nested_confirmations import CASES
from verify_overlay_form_saves import quota,activate,snapshot
from verify_pet_controls import ROOT,BASE,source

OUT=ROOT/'evidence/current'
SPECS={59:('verify_settings_controls.py','演示验证码 284631','注销演示账号','settings-account-delete','dujia-prototype-records','m01-p01'),
99:('verify_pet_controls.py','输入宠物名字确认删除','永久删除','pet-delete','dujia-prototype-pet','m07-p04')}
MODES=['success','blank','wrong','dirty-cancel','semantic-retry','quota-retry']
CONTENT=['records','moments','anniversaries','capsules','works','pet','books']
def stores(page):return page.evaluate('({local:{...localStorage},session:{...sessionStorage}})')

def main():
    files=source();raw=(OUT/'hidden-overlay-observations.json').read_bytes();observed=json.loads(raw)
    changed=[k for k in set(files)|set(observed['files'])if files.get(k)!=observed['files'].get(k)]
    assert changed in [[],['assets/prototype-preferences.js']],changed
    for path,digest in files.items():
        with urlopen(BASE+(path.replace('custom/','pages/',1)if path.startswith('custom/')else path),timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==digest
    results=[]
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index,(fixture,label,submit_label,operation,key,dest)in SPECS.items():
            original=observed['results'][index]
            for mode in MODES+(['quota-late-retry']if index==59 else[]):
                context=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');context.add_init_script(INIT)
                page=context.new_page();page.set_default_timeout(4500);page.set_default_navigation_timeout(15000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                row=dict(observation_index=index,page=original['page'],mode=mode,operation=operation)
                try:
                    declarations(fixture)['seed'](page,original['page'])
                    page.evaluate('localStorage.setItem("unrelated-test-key","keep");sessionStorage.setItem("unrelated-session-key","keep");sessionStorage.setItem("dujia-test-account-state","remove-on-account-only")')
                    value='284631'if index==59 else page.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet")).name')
                    before=stores(page);url=page.url;page.locator(original['selector']).click();dialog=page.locator('dialog[open]')
                    expect(dialog.locator('h2')).to_have_text(original['overlays'][0]['title'])
                    dialog.get_by_role('button',name=CASES[index][0],exact=True).click();expect(dialog.locator('h2')).to_have_text(CASES[index][1])
                    form=dialog.locator('form');field=form.get_by_label(label,exact=True);button=form.locator('[type=submit]');expect(button).to_have_text(submit_label)
                    assert stores(page)==before
                    if mode in['blank','wrong']:
                        field.fill(''if mode=='blank'else'000000'if index==59 else'错误名字')
                        button.click();expect(button).to_be_enabled();expect(page.locator('.prototype-toast')).to_contain_text('验证码不正确'if index==59 else'请填写'if mode=='blank'else'名字不一致')
                        assert stores(page)==before;expect(dialog).to_have_count(1)
                    elif mode=='dirty-cancel':
                        field.fill(value);page.keyboard.press('Escape');expect(dialog).to_contain_text('是否放弃当前修改')
                        dialog.get_by_role('button',name='继续编辑',exact=True).click();expect(field).to_have_value(value)
                        page.keyboard.press('Escape');dialog.get_by_role('button',name='放弃修改',exact=True).click();expect(page.locator('dialog[open]')).to_have_count(0);assert stores(page)==before
                    else:
                        field.fill(value);inputs=snapshot(form)
                        if mode=='semantic-retry':page.evaluate('op=>sessionStorage.setItem("dujia-prototype-fail-next",op)',operation)
                        if mode.startswith('quota'):quota(page,'dujia-prototype-moments'if mode=='quota-late-retry'else key)
                        if mode!='success':
                            activate(button);expect(page.locator('.prototype-toast')).to_contain_text('空间不足'if mode.startswith('quota')else'未完成')
                            expect(button).to_be_enabled();assert stores(page)==before,'Identity deletion failure changed storage'
                            assert snapshot(form)==inputs and page.url==url
                            if mode.startswith('quota'):assert page.evaluate('window.__overlayQuota')==1
                            row['failure_preserved_storage_and_input']=True
                        activate(button);page.wait_for_url('**/'+dest+'.html*');after=stores(page)
                        assert after['local']['unrelated-test-key']=='keep'and after['session']['unrelated-session-key']=='keep'
                        if index==59:
                            for kind in CONTENT:assert after['local']['dujia-prototype-'+kind]==('null'if kind=='pet'else'[]')
                            assert not any(k.startswith(('dujia-','fairy-'))and k not in['dujia-prototype-'+v for v in CONTENT]for k in after['local'])
                            assert not any(k.startswith(('dujia-','fairy-'))for k in after['session'])
                        else:
                            assert after['local']['dujia-prototype-pet']=='null'
                            assert {k:v for k,v in after['local'].items()if k not in['dujia-prototype-pet','dujia-prototype-backup']}=={k:v for k,v in before['local'].items()if k not in['dujia-prototype-pet','dujia-prototype-backup']}
                            assert after['session']==before['session']
                        row['deletion_boundary_verified']=True
                    assert not errors,errors;row['passed']=True
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-3000:],storage_at_failure=stores(page))
                row.update(errors=errors,effective=page.url);results.append(row);context.close();assert source()==files
                report=dict(files=files,observations_sha256=hashlib.sha256(raw).hexdigest(),historical_observation_changed_files=changed,expected_cases=13,results=results,accepted_pages=0)
                temp=OUT/'identity-deletion-results.json.tmp';temp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temp.replace(OUT/'identity-deletion-results.json')
                print(('PASS 'if row['passed']else'FAIL ')+str(len(results))+'/13 '+original['page']+' '+mode,flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(results),passed=sum(r['passed']for r in results))))
    raise SystemExit(0 if all(r['passed']for r in results)else 1)

if __name__=='__main__':main()
