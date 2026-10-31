"""Book editor hidden choices: exact references, crop/stickers and explicit parent save."""
import hashlib,json,time,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from audit_runtime import INIT
from verify_pet_controls import ROOT,source

OUT=ROOT/'evidence/current/hidden-book-editor-outcomes'
SOURCES={101:('photo','共同照片','coverPhoto'),108:('diary','共同日记','source'),109:('photo','共同照片','photoSource'),112:('photo','共同照片','photos'),113:('photo','共同照片','photos'),114:('photo','共同照片','photos'),116:('photo','共同照片','photoSource'),117:('moment','共同重要时刻','source'),119:('work','实际工坊作品','source'),120:('pet','实际成长故事','source'),121:('photo','共同照片','photoSource')}
CASES=[(i,label) for i,(_,label,_) in SOURCES.items()]+[(111,s) for s in ['替换这张照片','裁剪这张照片','移除这张照片']]+[(115,s) for s in ['💗','⭐','🌸','😊']]
REFS={k:{'kind':k,'id':v} for k,v in [('photo','audit-photo'),('diary','audit-diary'),('moment','audit-moment'),('work','audit-work'),('pet','audit-pet:audit-story')]}

PREPARE="""({index,action})=>{
 const key='dujia-prototype-books',books=PrototypeBooks.all(),b=books.find(v=>v.id==='book-state'),p=b.pages.find(v=>v.id==='page-state');
 const records=JSON.parse(localStorage.getItem('dujia-prototype-records'));
 for(const kind of ['diary','photo']){const original=records.find(v=>v.id==='audit-'+kind);records.push({...structuredClone(original),id:'alternate-'+kind,title:'备用'+kind});}
 localStorage.setItem('dujia-prototype-records',JSON.stringify(records));
 const moments=JSON.parse(localStorage.getItem('dujia-prototype-moments'));moments.push({...structuredClone(moments.find(v=>v.id==='audit-moment')),id:'alternate-moment',name:'备用时刻'});localStorage.setItem('dujia-prototype-moments',JSON.stringify(moments));
 const pet=JSON.parse(localStorage.getItem('dujia-prototype-pet'));pet.logs.push({...structuredClone(pet.logs.find(v=>v.id==='audit-story')),id:'alternate-story',text:'备用成长'});localStorage.setItem('dujia-prototype-pet',JSON.stringify(pet));
 if(index===108)p.source={kind:'diary',id:'alternate-diary'};
 if(index===117)p.source={kind:'moment',id:'alternate-moment'};
 if(index===120)p.source={kind:'pet',id:'audit-pet:alternate-story'};
 if([109,116,121].includes(index))p.photoSource={kind:'photo',id:'alternate-photo'};
 if([112,113,114].includes(index)||(index===111&&action==='替换这张照片')){p.source={kind:'photo',id:'alternate-photo'};p.photos=[{source:p.source,crop:{x:50,y:50,zoom:1}}];}
 localStorage.setItem(key,JSON.stringify(books));
}"""

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def store(p):return p.evaluate('({...localStorage})')
def books(p):return p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-books"))')
def unchanged_except_books(before,after):
    a=dict(before);b=dict(after);a.pop('dujia-prototype-books');b.pop('dujia-prototype-books');assert a==b
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
            page=context.new_page();page.set_default_timeout(6500);page.set_default_navigation_timeout(20000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            row=dict(observation_index=index,control_label=label,passed=False,errors=errors)
            try:
                original=observed['results'][index];seed(page,original['page']);page.evaluate(PREPARE,dict(index=index,action=label));page.reload()
                expect(page.locator('.screen')).to_have_attribute('aria-busy','false');expect(page.locator('.book-load')).to_have_count(0)
                before=store(page);oldbooks=books(page);old=next(b for b in oldbooks if b['id']=='book-state');oldpage=next(p for p in old['pages'] if p['id']=='page-state')
                page.locator(original['selector']).click();dialog=page.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text(original['overlays'][0]['title'])
                dialog.get_by_role('button',name=label,exact=True).click()
                if index==111 and label=='替换这张照片':
                    expect(dialog.locator('h2')).to_have_text('选择共同素材');dialog.get_by_role('button',name='共同照片',exact=True).click()
                elif index==111 and label=='裁剪这张照片':
                    expect(dialog.locator('h2')).to_have_text('裁剪照片')
                    for field,value in [('水平位置',30),('垂直位置',70),('缩放',1.5)]:
                        slider=dialog.get_by_label(field,exact=True);slider.evaluate('(e,value)=>{e.value=String(value);e.dispatchEvent(new Event("input",{bubbles:true}))}',value)
                    dialog.get_by_role('button',name='应用裁剪',exact=True).click()
                expect(dialog).to_have_count(0);assert store(page)==before,'Editor choice persisted before explicit parent save'
                if index==111 and label=='移除这张照片':
                    expect(page.locator('.book-photo-preview')).to_contain_text('从共同照片中挑选一张')
                    page.locator('.done').click();expect(page.locator('.prototype-toast')).to_contain_text('请至少选择一张共同照片')
                    expect(page.locator('.done')).to_be_enabled();assert store(page)==before
                    page.locator('[data-tool="添加照片"]').click();page.locator('dialog[open]').get_by_role('button',name='备用photo',exact=True).click()
                    expect(page.locator('dialog[open]')).to_have_count(0);assert store(page)==before
                if index==101:
                    expect(page.locator('.toggle')).to_have_attribute('aria-checked','true');page.locator('.next').click();destination='m08-p13' if old.get('start')=='blank' else 'm08-p06';page.wait_for_url('**/'+destination+'.html*')
                else:
                    page.locator('.done').click();destination='m08-p13';page.wait_for_url('**/m08-p13.html*')
                result=next(b for b in books(page) if b['id']=='book-state');saved=next(p for p in result['pages'] if p['id']=='page-state')
                if index in SOURCES:
                    kind,_,field=SOURCES[index];wanted=REFS[kind]
                    if field=='coverPhoto':assert result[field]==wanted
                    elif field=='photos':
                        assert len(saved['photos'])==2 and saved['photos'][-1]['source']==wanted
                        assert saved['photos'][0]['source']=={'kind':'photo','id':'alternate-photo'}
                    else:assert saved[field]==wanted
                    if index in [108,109,116,117,120,121]:assert oldpage.get(field)!=wanted
                    row['result']='selected exact '+kind+' reference; chooser preserves storage; only explicit parent save persists '+field
                    row['expected_reference']=wanted
                elif index==111:
                    if label=='替换这张照片':assert saved['photos'][0]['source']==REFS['photo'] and len(saved['photos'])==1
                    elif label=='裁剪这张照片':assert saved['photos'][0]['crop']==dict(x=30,y=70,zoom=1.5)
                    else:assert len(saved['photos'])==1 and saved['photos'][0]['source']=={'kind':'photo','id':'alternate-photo'}
                    row['result']='photo operation is local candidate; parent save persists exact replacement/crop/removal; original image records unchanged'
                    if label=='移除这张照片':row['result']+='; removing last photo blocks save without writes; reselecting another photo recovers and original photo remains removed'
                else:
                    assert saved['stickers']==[label];row['result']='selected exact sticker appended to candidate; parent save persists it once'
                assert [p for p in old['pages'] if p['id']!='page-state']==[p for p in result['pages'] if p['id']!='page-state']
                assert [b for b in oldbooks if b['id']!='book-state']==[b for b in books(page) if b['id']!='book-state']
                unchanged_except_books(before,store(page));row['destination']=destination;assert not errors;row['passed']=True
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);context.close();assert source()==files
            save_report(dict(files=files,script_sha256=sha(Path(__file__)),observations_sha256=sha(obspath),fixture_script_sha256=sha(ROOT/'verify_book_controls.py'),expected_cases=len(CASES),results=rows,accepted_pages=0,scope='18 observed book editor choices; alternate source fixtures make replacements observable; no product mutation'))
            print(('PASS ' if row['passed'] else 'FAIL ')+str(index)+' '+label,flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
