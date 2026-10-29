"""Current quote/rename form persistence and whole-book delete boundaries."""
import json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_book_v2_reconciliation import ROOT,dependencies,sha

fixture=declarations('verify_book_controls.py')
def store(p):return p.evaluate('({...localStorage})')
def books(p):return json.loads(store(p)['dujia-prototype-books'])
def run(p,name):
    identity='m08-p11' if name.startswith('quote-') else 'm08-p21';fixture['seed'](p,identity);before=store(p);original=books(p)
    if name.startswith('quote-'):
        p.locator('.quote-action').click();field=p.get_by_role('textbox',name='书页寄语',exact=True)
        if name=='quote-validation-parent-save':
            p.get_by_role('button',name='保存一句话',exact=True).click();expect(field).to_have_attribute('aria-invalid','true');assert store(p)==before
            field.fill('这句寄语只在书中保存');p.get_by_role('button',name='保存一句话',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('#quote')).to_have_text('这句寄语只在书中保存');assert store(p)==before
            p.locator('.done').click();p.wait_for_url('**/m08-p13.html*');saved=books(p);assert saved[0]['pages'][0]['message']=='这句寄语只在书中保存';assert saved[0]['pages'][0]['source']==original[0]['pages'][0]['source'];assert saved[0]['pages'][1:]==original[0]['pages'][1:]
            a=dict(before);b=store(p);a.pop('dujia-prototype-books');b.pop('dujia-prototype-books');assert a==b;return
        field.fill('取消的寄语');p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('#quote')).not_to_have_text('取消的寄语');assert store(p)==before;return
    if name.startswith('rename-'):
        p.locator('.rename').click();field=p.get_by_role('textbox',name='回忆册名称',exact=True)
        if name=='rename-validation-save':
            field.fill('');p.get_by_role('button',name='保存书名',exact=True).click();expect(field).to_have_attribute('aria-invalid','true');assert store(p)==before
            field.fill('已经改名的回忆册');p.get_by_role('button',name='保存书名',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.book-name')).to_have_text('已经改名的回忆册');saved=books(p);assert saved[0]['name']=='已经改名的回忆册'
            left=original[0].copy();right=saved[0].copy()
            for key in ['name','updatedAt']:left.pop(key,None);right.pop(key,None)
            assert left==right
            a=dict(before);b=store(p);a.pop('dujia-prototype-books');b.pop('dujia-prototype-books');assert a==b;return
        field.fill('取消的书名');p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert store(p)==before;return
    if name=='delete-confirm-only-target-book':
        p.evaluate('()=>{const b=JSON.parse(localStorage.getItem("dujia-prototype-books"));b.push({...structuredClone(b[0]),id:"keep-book",name:"必须保留的另一本"});localStorage.setItem("dujia-prototype-books",JSON.stringify(b))}')
        before=store(p);other=books(p)[1];p.locator('.show-delete').click();p.get_by_role('button',name='确认删除',exact=True).click();p.wait_for_url('**/m08-p01.html*');expect(p.locator('.screen')).to_have_attribute('aria-busy','false');assert books(p)==[other]
        a=dict(before);b=store(p);a.pop('dujia-prototype-books');b.pop('dujia-prototype-books');assert a==b;return
    raise AssertionError(name)

CASES=['quote-validation-parent-save','quote-cancel','rename-validation-save','rename-cancel','delete-confirm-only-target-book']
def main():
    out=ROOT/'evidence/current/book-v2-hidden-forms';out.mkdir(parents=True,exist_ok=True);files=dependencies();rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for name in CASES:
            c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(case=name,passed=False)
            try:run(p,name);assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc();p.screenshot(path=str(out/(name+'.png')),full_page=True)
            row['errors']=errors;rows.append(row);c.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps(dict(dependency_files=files,producer_sha256=sha(Path(__file__)),fixture_sha256=sha(ROOT/'verify_book_controls.py'),browser=version,scope='Five named current hidden-form/save/delete outcomes; no product-source changes.',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Hidden form outcomes:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
