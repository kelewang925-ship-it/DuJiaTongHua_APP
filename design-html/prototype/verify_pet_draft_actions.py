"""Original controls, unlock selection, and two-tab draft protection on the current renderer."""
import json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from verify_pet_draft_previews import ROOT,DEMO,sha,dependencies,prepare,select,check,BASE
from audit_hidden_overlays import declarations

def peer(p,f,n):
    prepare(p,f,n);item=select(p,'bow' if n==12 else 'cream-bed');room=p.evaluate('PrototypePetLife.room(PrototypePet.read())')
    if n==15:room['小床']=item['name']
    other=p.context.new_page();other.goto('http://127.0.0.1:8765/prototype/review.html')
    other.evaluate('''n=>{const pet=JSON.parse(localStorage.getItem('dujia-prototype-pet'));if(n===12)pet.logs.push({id:'peer-preview',type:'water',date:'2026-10-06',actor:'阿舟',text:'另一半添水',story:true});else pet.id='replacement-preview-pet';localStorage.setItem('dujia-prototype-pet',JSON.stringify(pet));}''',n)
    expect(p.locator('.prototype-toast')).to_contain_text('当前输入保留');check(p,n,item['name'],room);before=f['store'](p);p.locator('#save' if n==12 else '.save').click()
    if n==12:
        expect(p.locator('.prototype-toast')).to_contain_text('穿戴已保存');assert p.evaluate('PrototypePet.read().logs.some(v=>v.id==="peer-preview")');assert p.evaluate('PrototypePet.read().outfit')==item['name']
    else:
        expect(p.locator('.prototype-toast')).to_contain_text('宠物已经发生变化');assert f['store'](p)==before;check(p,n,item['name'],room)
    other.close()

def unlock(p,f,n):
    f['seed'](p,f'm07-p{n}');id='bow' if n==12 else 'lamp';item=select(p,id);before=f['store'](p)
    p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","pet-unlock")');p.get_by_role('button',name='解锁并选择',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert f['store'](p)==before
    p.locator('[data-item="'+id+'"]').click();p.get_by_role('button',name='解锁并选择',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('已解锁');pet=p.evaluate('PrototypePet.read()');room=p.evaluate('PrototypePetLife.room(PrototypePet.read())')
    if n==15:room['摆件']=item['name']
    check(p,n,item['name'],room);assert pet.get('outfit') is None if n==12 else pet.get('room',{})=={}

def main():
    out=ROOT/'evidence/current/pet-draft-previews';assert not (out/'actions.json').exists();deps=dependencies();f=declarations('verify_pet_controls.py');catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'))
    cases=[('control',(r['id'],v)) for r in catalog['pages'] if r['id'] in ['m07-p12','m07-p15'] for v in r['control_evidence']]+[('peer',n) for n in [12,15]]+[('unlock',n) for n in [12,15]];rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':page,v=value;f['control'](p,page,v,v['contract'])
                else:(peer if kind=='peer' else unlock)(p,f,value)
                assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            row['page_errors']=errors;rows.append(row);c.close();assert dependencies()==deps;print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        b.close()
    (out/'actions.json').write_text(json.dumps({'dependencies':deps,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_pet_controls.py'),'catalog_sha256':sha(ROOT/'evidence/current/page-contracts.json'),'browser':version,'results':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
