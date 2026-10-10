"""Actual direct deletion results, semantic failure and storage rollback/retry."""
import hashlib,json,traceback
from urllib.request import urlopen
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright,expect
from audit_runtime import INIT
from audit_hidden_overlays import MODULES,declarations
from verify_nested_confirmations import CASES
from verify_overlay_form_saves import quota
from verify_pet_controls import ROOT,BASE,source

OUT=ROOT/'evidence/current'
# Observation index: persistent key, existing failure operation, destination (None stays).
SPECS={9:('records','diary-delete','m03-p06'),11:('records','diary-delete','m03-p06'),
16:('records','photo-delete','m03-p09'),18:('moments','moment-delete','m04-p02'),
22:('anniversaries','anniversary-delete','m04-p07'),23:('anniversaries','anniversary-delete','m04-p07'),
25:('capsules','capsule-delete','m04-p12'),26:('capsules','capsule-delete','m04-p12'),
30:('works','work-delete','m05-p09'),33:('works','work-delete','m05-p09'),
36:('works','work-delete','m05-p09'),39:('works','work-delete','m05-p09'),
47:('tags','settings-tag',None),48:('tags','settings-tag',None),49:('tags','settings-tag',None)}

def storage(page):return page.evaluate('({...localStorage})')

def confirm(page,original,index):
    page.locator(original['selector']).click()
    dialog=page.locator('dialog[open]')
    expect(dialog.locator('h2')).to_have_text(original['overlays'][0]['title'])
    dialog.get_by_role('button',name=CASES[index][0],exact=True).click()
    expect(dialog.locator('h2')).to_have_text(CASES[index][1])
    dialog.get_by_role('button',name='确认删除',exact=True).click()
    expect(page.locator('dialog[open]')).to_have_count(0)

def main():
    files=source();raw=(OUT/'hidden-overlay-observations.json').read_bytes();observed=json.loads(raw)
    assert observed['files']==files
    for path,digest in files.items():
        with urlopen(BASE+(path.replace('custom/','pages/',1)if path.startswith('custom/')else path),timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==digest
    fixtures={group:declarations(name)for group,name in MODULES.items()};results=[]
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index,(kind,operation,destination)in SPECS.items():
            original=observed['results'][index];key='dujia-prototype-'+kind
            for mode in ['success','semantic-retry','quota-retry']:
                context=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');context.add_init_script(INIT)
                page=context.new_page();page.set_default_timeout(4500);page.set_default_navigation_timeout(15000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                row=dict(observation_index=index,page=original['page'],mode=mode,key=key,operation=operation,destination=destination)
                try:
                    fixtures[original['group']]['seed'](page,original['page'])
                    before=storage(page);items=json.loads(before[key]);url=page.url
                    if kind=='tags':
                        items=page.evaluate('PrototypePreferences.tags()')
                        label=page.locator(original['selector']).inner_text();target=next(v for v in items if v['name']==label)
                        retained=next(v['name']for v in items if v['id']!=target['id'])
                        page.evaluate('names=>{const key="dujia-prototype-records",records=JSON.parse(localStorage.getItem(key));records[0].tags=names;localStorage.setItem(key,JSON.stringify(records))}',[target['name'],retained])
                        before=storage(page)
                    else:
                        identifier=parse_qs(urlparse(url).query)['id'][0];target=next(v for v in items if v['id']==identifier)
                    row['target_id']=target['id'];row['target_name']=target.get('name',target.get('title'))
                    if mode=='semantic-retry':page.evaluate('operation=>sessionStorage.setItem("dujia-prototype-fail-next",operation)',operation)
                    if mode=='quota-retry':quota(page,'dujia-prototype-records'if kind=='tags'else key)
                    if mode!='success':
                        confirm(page,original,index)
                        expect(page.locator('.prototype-toast')).to_contain_text('空间不足'if mode=='quota-retry'else'删除')
                        expect(page.locator(original['selector'])).to_be_enabled()
                        assert storage(page)==before,'Failure changed persistent data'
                        assert page.url==url,'Failure left original page'
                        if mode=='quota-retry':assert page.evaluate('window.__overlayQuota')==1
                        else:assert page.evaluate('sessionStorage.getItem("dujia-prototype-fail-next")')is None
                        row['failure_preserved_all_storage']=True
                    confirm(page,original,index)
                    page.wait_for_function('arg=>!JSON.parse(localStorage.getItem(arg.key)).some(v=>v.id===arg.id)',arg=dict(key=key,id=target['id']))
                    if destination:page.wait_for_url('**/'+destination+'.html*')
                    after=storage(page);remaining=json.loads(after[key])
                    assert remaining==[v for v in items if v['id']!=target['id']],'Deletion changed sibling records'
                    allowed={key,'dujia-prototype-backup'}
                    if kind=='tags':
                        allowed.add('dujia-prototype-records');old_records=json.loads(before['dujia-prototype-records']);new_records=json.loads(after['dujia-prototype-records'])
                        assert len(old_records)==len(new_records)
                        for old,new in zip(old_records,new_records):
                            assert {k:v for k,v in old.items()if k!='tags'}=={k:v for k,v in new.items()if k!='tags'}
                            assert not any(name==target['name']for name in new.get('tags',[]))
                        assert new_records[0]['tags']==[retained],'Tag deletion changed retained label'
                    assert {k:v for k,v in before.items()if k not in allowed}=={k:v for k,v in after.items()if k not in allowed},'Deletion changed related/unrelated storage'
                    assert not errors,errors;row.update(passed=True,siblings_preserved=True,related_storage_preserved=True)
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-2700:])
                row.update(errors=errors,effective=page.url);results.append(row);context.close();assert source()==files
                report=dict(files=files,observations_sha256=hashlib.sha256(raw).hexdigest(),expected_cases=45,results=results,accepted_pages=0)
                temporary=OUT/'confirmed-deletion-results.json.tmp';temporary.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temporary.replace(OUT/'confirmed-deletion-results.json')
                print(('PASS 'if row['passed']else'FAIL ')+str(len(results))+'/45 '+row['page']+' '+mode,flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(results),passed=sum(r['passed']for r in results))))
    raise SystemExit(0 if all(r['passed']for r in results)else 1)

if __name__=='__main__':main()
