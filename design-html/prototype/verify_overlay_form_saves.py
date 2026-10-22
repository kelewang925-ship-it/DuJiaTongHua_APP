"""Execute declared overlay form values, validation and real storage-failure recovery."""
import argparse,hashlib,json,traceback
from urllib.request import urlopen
from playwright.sync_api import sync_playwright,expect
from audit_runtime import INIT
from audit_hidden_overlays import MODULES,declarations
from verify_pet_controls import ROOT,BASE,source

OUT=ROOT/'evidence/current'
TEXT='弹层保存测试'
# Index: exact editable values, destination key, explicit result predicate.
SPECS={
17:({'回应这个时刻':TEXT},'dujia-prototype-moments','d.some(v=>v.id==="audit-moment"&&v.comments.filter(c=>c.text===text).length===1)'),
42:({'共同昵称':TEXT},'dujia-prototype-relationship','d.profile.nickname===text'),
45:({'标签名称':'保存标签45','标签范围':'personal'},'dujia-prototype-tags','d.filter(v=>v.name==="保存标签45"&&v.scope==="personal").length===1'),
46:({'标签名称':'保存标签46','标签范围':'personal'},'dujia-prototype-tags','d.filter(v=>v.name==="保存标签46"&&v.scope==="personal").length===1'),
52:({'动效':'reduce'},'dujia-prototype-preferences','d.reduceMotion===true'),
55:({'手机号':'13987654321','演示验证码 284631':'284631'},'dujia-prototype-session','d.phone==="13987654321"&&d.loggedIn===true'),
57:({'演示验证码 284631':'284631'},'dujia-prototype-preferences','d.twoFactor===true'),
64:({'意见反馈':TEXT},'dujia-feedback-draft','d===text'),
72:({'今天的小心情':TEXT},'dujia-prototype-pet','d.logs.filter(v=>v.type==="note"&&v.text===text).length===1'),
82:({'成长故事内容':TEXT},'dujia-prototype-pet','d.logs.filter(v=>v.type==="note"&&v.text===text).length===1'),
84:({'成长故事内容':TEXT},'dujia-prototype-pet','d.logs.filter(v=>v.type==="note"&&v.text===text).length===1'),
85:({'回应内容':TEXT},'dujia-prototype-pet','(d.logs.find(v=>v.id==="pet-story").comments||[]).filter(v=>v.text===text).length===1'),
97:({'每天提醒时间':'21:45'},'dujia-prototype-pet','d.settings.time==="21:45"'),
118:({'书页寄语':TEXT},'dujia-prototype-books','d.find(v=>v.id==="book-state").pages.find(v=>v.id==="page-state").message===text'),
122:({'章节名':TEXT},'dujia-prototype-books','d.find(v=>v.id==="book-state").chapters.filter(v=>v.name===text).length===1'),
129:({'回忆册名称':TEXT},'dujia-prototype-books','d.find(v=>v.id==="book-state").name===text')}
CANDIDATES={118:('.done','#quote'),122:('.save','.book-structure')}

def storage(page):return page.evaluate('JSON.stringify({...localStorage})')
def snapshot(form):return form.evaluate('f=>JSON.stringify([...f.querySelectorAll("input,textarea,select")].map(e=>[e.value,e.checked]))')
def fill(form,values):
    for label,value in values.items():
        field=form.get_by_label(label,exact=True)
        if field.evaluate('e=>e.tagName')=='SELECT':field.select_option(value)
        else:field.fill(value)
def quota(page,key):
    page.evaluate('key=>{const original=Storage.prototype.setItem;window.__overlayQuota=0;Storage.prototype.setItem=function(k,v){if(this===localStorage&&k===key&&window.__overlayQuota===0){window.__overlayQuota++;throw new DOMException("Injected quota failure","QuotaExceededError")}return original.call(this,k,v)}}',key)
def activate(button):
    button.evaluate('b=>{b.click();b.click()}')
    expect(button).to_be_disabled();expect(button).to_have_attribute('aria-busy','true')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--locator-candidates',action='store_true',help='Use historical observation selectors only; re-execute actual titles, forms and storage predicates on current source');args=parser.parse_args()
    files=source();raw=(OUT/'hidden-overlay-observations.json').read_bytes();observed=json.loads(raw)
    if not args.locator_candidates:assert observed['files']==files
    for path,digest in files.items():
        with urlopen(BASE+(path.replace('custom/','pages/',1)if path.startswith('custom/')else path),timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==digest
    fixtures={group:declarations(name)for group,name in MODULES.items()};results=[]
    cases=[(index,mode)for index in SPECS for mode in ['save','quota-retry','invalid']if mode!='invalid'or index!=52]
    assert len(cases)==47
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index,mode in cases:
            original=observed['results'][index];values,key,predicate=SPECS[index]
            context=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');context.add_init_script(INIT)
            page=context.new_page();page.set_default_timeout(4500);page.set_default_navigation_timeout(15000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            row=dict(observation_index=index,page=original['page'],title=original['overlays'][0]['title'],mode=mode,key=key,candidate_parent_save=index in CANDIDATES)
            try:
                fixtures[original['group']]['seed'](page,original['page']);page.locator(original['selector']).click()
                dialog=page.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text(row['title']);form=dialog.locator('form');submit=form.locator('[type=submit]');before=storage(page)
                fill(form,values)
                if mode=='invalid':
                    for label in values:
                        field=form.get_by_label(label,exact=True)
                        if field.evaluate('e=>e.tagName')!='SELECT':field.fill('')
                    submit.click();expect(form.locator('[aria-invalid=true]').first).to_be_visible();expect(submit).to_be_enabled()
                    assert storage(page)==before;expect(dialog).to_have_count(1)
                else:
                    candidate_snapshot=snapshot(form)
                    if index in CANDIDATES:
                        activate(submit);expect(dialog).to_have_count(0);assert storage(page)==before,'Candidate wrote before parent save'
                        parent,preview=CANDIDATES[index];expect(page.locator(preview)).to_contain_text(TEXT);submit=page.locator(parent)
                    if mode=='quota-retry':
                        quota(page,key);activate(submit);expect(page.locator('.prototype-toast')).to_contain_text('空间不足');expect(submit).to_be_enabled()
                        assert storage(page)==before;assert page.evaluate('window.__overlayQuota')==1
                        if index in CANDIDATES:expect(page.locator(CANDIDATES[index][1])).to_contain_text(TEXT)
                        else:expect(dialog).to_have_count(1);assert snapshot(form)==candidate_snapshot
                    activate(submit)
                    page.wait_for_function('arg=>{const d=JSON.parse(localStorage.getItem(arg.key)),text=arg.text;return '+predicate+'}',arg=dict(key=key,text=TEXT))
                    expect(page.locator('dialog[open]')).to_have_count(0)
                    if index in [84,118,122]:page.wait_for_url('**/m07-p18.html*'if index==84 else'**/m08-p13.html*'if index==118 else'**/m08-p14.html*')
                    row['stored_predicate']=predicate;row['duplicate_activation_checked']=True
                assert not errors,errors;row['passed']=True
            except Exception:row.update(passed=False,failure=traceback.format_exc()[-2600:])
            row.update(errors=errors,effective=page.url);results.append(row);context.close();assert source()==files
            report=dict(files=files,observations_sha256=hashlib.sha256(raw).hexdigest(),locator_candidates_only=args.locator_candidates,script_sha256=hashlib.sha256(__import__('pathlib').Path(__file__).read_bytes()).hexdigest(),expected_cases=47,results=results,accepted_pages=0)
            temp=OUT/'overlay-form-save-results.json.tmp';temp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temp.replace(OUT/'overlay-form-save-results.json')
            print(('PASS 'if row['passed']else'FAIL ')+str(len(results))+'/47 '+row['page']+' '+row['title']+' '+mode,flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(results),passed=sum(row['passed']for row in results))))
    raise SystemExit(0 if all(row['passed']for row in results)else 1)

if __name__=='__main__':main()
