"""Fixed expected chapter/page layouts and whole-book deletion boundaries."""
import hashlib,json,time,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from audit_runtime import INIT
from verify_pet_controls import ROOT,source

OUT=ROOT/'evidence/current/hidden-book-structure-outcomes'
CASES=[(i,s) for i in [123,126] for s in ['修改章节名','上移章节','下移章节']]+[(i,s) for i in [124,125,127] for s in ['上移一页','下移一页','移动到另一章']]+[(132,'确认删除')]
BOUNDARY={(123,'上移章节'),(126,'下移章节'),(124,'上移一页'),(125,'下移一页'),(127,'上移一页'),(127,'下移一页')}
S='page-state';T='page-second';U='page-third';C='chapter-state';D='chapter-two'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def store(p):return p.evaluate('({...localStorage})')
def books(p):return p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-books"))')
def save_report(value):
    tmp=OUT/'results.json.tmp';payload=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    for attempt in range(30):
        try:tmp.write_text(payload,encoding='utf-8');tmp.replace(OUT/'results.json');return
        except PermissionError:
            if attempt==29:raise
            time.sleep(.1)

def main():
    OUT.mkdir(exist_ok=True);files=source();obspath=ROOT/'evidence/current/hidden-overlay-observations.json';observed=json.loads(obspath.read_text(encoding='utf-8'));seed=declarations('verify_book_controls.py')['seed'];rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index,label in CASES:
            context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');context.add_init_script(INIT)
            page=context.new_page();page.set_default_timeout(6500);page.set_default_navigation_timeout(20000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));row=dict(observation_index=index,control_label=label,passed=False,errors=errors)
            try:
                original=observed['results'][index];seed(page,original['page'])
                page.evaluate('()=>{const b=PrototypeBooks.all();b.push({...structuredClone(b[0]),id:"untouched-book",name:"保留的另一册"});localStorage.setItem("dujia-prototype-books",JSON.stringify(b))}');page.reload()
                expect(page.locator('.screen')).to_have_attribute('aria-busy','false');expect(page.locator('.book-load')).to_have_count(0)
                before=store(page);oldbooks=books(page);old=next(b for b in oldbooks if b['id']=='book-state')
                page.locator(original['selector']).click();dialog=page.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text(original['overlays'][0]['title']);dialog.get_by_role('button',name=label,exact=True).click()
                if index==132:
                    page.wait_for_url('**/m08-p01.html*');assert books(page)==[b for b in oldbooks if b['id']!='book-state']
                    row.update(destination='m08-p01',result='only selected book deleted; second book and all original source records retained')
                else:
                    chapter_order=[C,D];page_order=[S,T,U];override={};names={C:'第一章',D:'第二章'}
                    if label=='修改章节名':
                        title='新的第一章' if index==123 else '新的第二章';expect(dialog.locator('h2')).to_have_text('章节名');form=dialog.locator('form')
                        expect(form.get_by_label('章节名',exact=True)).to_have_value('第一章' if index==123 else '第二章');form.get_by_label('章节名',exact=True).fill(title);form.get_by_role('button',name='保存章节名',exact=True).click();names[C if index==123 else D]=title
                    elif label=='移动到另一章':
                        expect(dialog.locator('h2')).to_have_text('选择目标章节');dialog.get_by_role('button',name='第一章' if index==127 else '第二章',exact=True).click()
                        target={124:S,125:T,127:U}[index];override[target]=C if index==127 else D
                        page_order={124:[T,U,S],125:[S,U,T],127:[S,T,U]}[index]
                    elif (index,label) in [(123,'下移章节'),(126,'上移章节')]:chapter_order=[D,C];page_order=[U,S,T]
                    elif (index,label) in [(124,'下移一页'),(125,'上移一页')]:page_order=[T,S,U]
                    expect(dialog).to_have_count(0)
                    if (index,label) in BOUNDARY:expect(page.locator('.prototype-toast')).to_contain_text('边界')
                    assert store(page)==before,'Candidate layout wrote before parent save'
                    assert page.locator('.book-structure h2').all_text_contents()==[names[c] for c in chapter_order]
                    assert page.locator('.book-page-row').evaluate_all('els=>els.map(e=>e.dataset.pageId)')==page_order
                    page.locator('.save').click();page.wait_for_url('**/m08-p14.html*')
                    value=next(b for b in books(page) if b['id']=='book-state');original_chapters={v['id']:v for v in old['chapters']};original_pages={v['id']:v for v in old['pages']}
                    expected_chapters=[{**original_chapters[c],'name':names[c]} for c in chapter_order]
                    expected_pages=[{**original_pages[p],'chapterId':override.get(p,original_pages[p]['chapterId'])} for p in page_order]
                    assert value['chapters']==expected_chapters and value['pages']==expected_pages
                    assert [b for b in books(page) if b['id']!='book-state']==[b for b in oldbooks if b['id']!='book-state']
                    other_old={k:v for k,v in old.items() if k not in ['pages','chapters','updatedAt','status']};other_new={k:v for k,v in value.items() if k not in ['pages','chapters','updatedAt','status']};assert other_old==other_new
                    row.update(destination='m08-p14',expected_chapter_order=chapter_order,expected_page_order=page_order,result='exact chapter/page candidate and stored layout; boundary action gives feedback without rearranging; parent save required; sources/other book retained')
                oldlocal=dict(before);newlocal=store(page);oldlocal.pop('dujia-prototype-books');newlocal.pop('dujia-prototype-books');assert oldlocal==newlocal
                assert not errors;row['passed']=True
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);context.close();assert source()==files
            save_report(dict(files=files,script_sha256=sha(Path(__file__)),observations_sha256=sha(obspath),fixture_script_sha256=sha(ROOT/'verify_book_controls.py'),expected_cases=len(CASES),results=rows,accepted_pages=0))
            print(('PASS ' if row['passed'] else 'FAIL ')+str(index)+' '+label,flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
