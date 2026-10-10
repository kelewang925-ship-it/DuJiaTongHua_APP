"""Chapter/page deletion is a candidate until guarded arrangement save."""
import hashlib,json,traceback
from urllib.request import urlopen
from playwright.sync_api import sync_playwright,expect
from audit_runtime import INIT
from audit_hidden_overlays import declarations
from verify_nested_confirmations import CASES
from verify_overlay_form_saves import quota,activate
from verify_pet_controls import ROOT,BASE,source

OUT=ROOT/'evidence/current';KEY='dujia-prototype-books'
SPECS={123:('chapter','chapter-state'),126:('chapter','chapter-two'),
       124:('page','page-state'),125:('page','page-second'),127:('page','page-third')}
MODES=['save','discard','semantic-retry','quota-retry','external-update']

def storage(page):return page.evaluate('({...localStorage})')

def prepare(page,seed):
    seed(page,'m08-p13')
    page.evaluate('''() => {
      const k='dujia-prototype-books',books=JSON.parse(localStorage.getItem(k)),book=books[0];
      book.bookmarks=book.pages.map(p=>p.id);book.lastPage='page-second';
      book.selected=book.pages.map(p=>p.source);
      book.pages.forEach(p=>p.supplements=[{id:'supp-'+p.id,kind:'写几句话',text:'保留原始补页',author:'小满',date:'2026-10-06'}]);
      books.push({...structuredClone(book),id:'untouched-book',name:'保留的另一册'});
      localStorage.setItem(k,JSON.stringify(books));
    }''')
    page.reload();expect(page.locator('.screen')).to_have_attribute('aria-busy','false');expect(page.locator('.book-load')).to_have_count(0)

def remove_candidate(page,original,index):
    page.locator(original['selector']).click();dialog=page.locator('dialog[open]')
    expect(dialog.locator('h2')).to_have_text(original['overlays'][0]['title'])
    dialog.get_by_role('button',name=CASES[index][0],exact=True).click()
    expect(dialog.locator('h2')).to_have_text(CASES[index][1])
    dialog.get_by_role('button',name='确认删除章节'if SPECS[index][0]=='chapter'else'确认删除书页',exact=True).click()
    expect(page.locator('dialog[open]')).to_have_count(0)

def candidate(page,ids):
    assert page.locator('.book-page-row').evaluate_all('els=>els.map(e=>e.dataset.pageId)')==ids
    return page.locator('.book-structure').inner_text()

def discard(page,before,ids):
    page.get_by_role('button',name='返回编排',exact=True).click()
    expect(page.locator('dialog[open] h2')).to_have_text('是否放弃当前修改？')
    page.get_by_role('button',name='继续编辑',exact=True).click()
    candidate(page,ids);assert storage(page)==before
    page.get_by_role('button',name='返回编排',exact=True).click()
    page.get_by_role('button',name='放弃修改',exact=True).click()
    page.wait_for_url('**/m08-p06.html*');assert storage(page)==before

def expected_book(old,kind,target):
    chapters=[v for v in old['chapters']if kind!='chapter'or v['id']!=target]
    pages=[v for v in old['pages']if v['chapterId']!=target]if kind=='chapter'else[v for v in old['pages']if v['id']!=target]
    remaining={v['id']for v in pages};removed=[v for v in old['pages']if v['id']not in remaining]
    selected=[ref for ref in old['selected']if not any(v.get('source')==ref for v in removed)or any(v.get('source')==ref for v in pages)]
    return dict(chapters=chapters,pages=pages,selected=selected,bookmarks=[v for v in old['bookmarks']if v in remaining],
                lastPage=old['lastPage']if old['lastPage']in remaining else pages[0]['id']if pages else None,status='published')

def main():
    files=source();raw=(OUT/'hidden-overlay-observations.json').read_bytes();observed=json.loads(raw);assert observed['files']==files
    for path,digest in files.items():
        with urlopen(BASE+(path.replace('custom/','pages/',1)if path.startswith('custom/')else path),timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==digest
    seed=declarations('verify_book_controls.py')['seed'];results=[]
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index,(kind,target)in SPECS.items():
            original=observed['results'][index]
            for mode in MODES:
                context=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');context.add_init_script(INIT)
                page=context.new_page();page.set_default_timeout(4500);page.set_default_navigation_timeout(15000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                row=dict(observation_index=index,page='m08-p13',kind=kind,target=target,mode=mode)
                try:
                    prepare(page,seed);before=storage(page);books=json.loads(before[KEY]);old=books[0];wanted=expected_book(old,kind,target);ids=[p['id']for p in wanted['pages']]
                    remove_candidate(page,original,index);preview=candidate(page,ids)
                    assert storage(page)==before,'Candidate deletion wrote before arrangement save'
                    if mode=='discard':
                        discard(page,before,ids);page.goto(BASE+'pages/m08-p13.html?id=book-state');expect(page.locator('.screen')).to_have_attribute('aria-busy','false')
                        candidate(page,[p['id']for p in old['pages']]);assert storage(page)==before
                    elif mode=='external-update':
                        page.evaluate('''() => {const k='dujia-prototype-books',books=JSON.parse(localStorage.getItem(k));books[0].name='另一处更新的册名';books[0].updatedAt=(books[0].updatedAt||0)+1;localStorage.setItem(k,JSON.stringify(books))}''')
                        changed=storage(page);activate(page.locator('.save'));expect(page.locator('.prototype-toast')).to_contain_text('另一处更新');expect(page.locator('.save')).to_be_enabled()
                        assert storage(page)==changed;assert candidate(page,ids)==preview
                        discard(page,changed,ids);row['external_update_preserved']=True
                    else:
                        if mode=='semantic-retry':page.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","book-publish")')
                        if mode=='quota-retry':quota(page,KEY)
                        if mode!='save':
                            activate(page.locator('.save'));expect(page.locator('.prototype-toast')).to_contain_text('空间不足'if mode=='quota-retry'else'保存未完成');expect(page.locator('.save')).to_be_enabled()
                            assert storage(page)==before;assert candidate(page,ids)==preview
                            if mode=='quota-retry':assert page.evaluate('window.__overlayQuota')==1
                            else:assert page.evaluate('sessionStorage.getItem("dujia-prototype-fail-next")')is None
                            row['failure_preserved_all_storage']=True
                        activate(page.locator('.save'));page.wait_for_url('**/m08-p14.html*');after=storage(page);saved_books=json.loads(after[KEY]);saved=next(b for b in saved_books if b['id']=='book-state')
                        for key,value in wanted.items():assert saved[key]==value,(key,saved[key],value)
                        allowed=set(wanted)|{'updatedAt'}
                        assert {k:v for k,v in saved.items()if k not in allowed}=={k:v for k,v in old.items()if k not in allowed}
                        assert [b for b in saved_books if b['id']!='book-state']==books[1:],'Changed another book'
                        assert {k:v for k,v in after.items()if k not in[KEY,'dujia-prototype-backup']}=={k:v for k,v in before.items()if k not in[KEY,'dujia-prototype-backup']},'Changed original source or unrelated storage'
                        row['persistent_contract']=wanted;row['sources_and_other_book_preserved']=True
                    assert not errors,errors;row.update(passed=True,candidate_deferred=True)
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-2800:])
                row.update(errors=errors,effective=page.url);results.append(row);context.close();assert source()==files
                value=dict(files=files,observations_sha256=hashlib.sha256(raw).hexdigest(),expected_cases=25,results=results,accepted_pages=0)
                temporary=OUT/'book-candidate-deletion-results.json.tmp';temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temporary.replace(OUT/'book-candidate-deletion-results.json')
                print(('PASS 'if row['passed']else'FAIL ')+str(len(results))+'/25 '+kind+' '+target+' '+mode,flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(results),passed=sum(r['passed']for r in results))))
    raise SystemExit(0 if all(r['passed']for r in results)else 1)

if __name__=='__main__':main()
