from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,go,fixture,records

OUT=Path(__file__).resolve().parent/'evidence/current'
rows=[]
def metrics(p,width):
    result=p.evaluate('''()=>({width:document.documentElement.scrollWidth,controls:[...document.querySelectorAll(document.querySelector('dialog[open]')?'dialog[open] button':'.screen button')].filter(e=>!e.disabled&&e.getClientRects().length&&!e.closest('[inert]')).map(e=>{e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {text:e.textContent,hit:hit===e||e.contains(hit),height:r.height,width:r.width}})})''')
    assert result['width']==width,result
    assert all(v['hit'] and v['height']>=44 for v in result['controls']),result
    return result
with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for width in [320,375,390,414,430]:
        for number in [7,13]:
            c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:
                book=fixture();book['chapters'].append(dict(id='second-chapter',name='另一个拥有二十字以内长名称的章节'))
                book['selected'].append(dict(kind='diary',id='pending-source'))
                source=dict(id='pending-source',type='diary',title='等待逐页编排的一份新素材',body='长正文'*120,date='2026-10-04',visibility='shared',status='published')
                seed(p,books=[book],records=records()+[source]);go(p,number,'?id=book-state');p.wait_for_function('document.querySelector(".screen").getAttribute("aria-busy")==="false"')
                p.evaluate('document.documentElement.style.setProperty("--ui-safe-top","44px");document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
                initial=metrics(p,width)
                if number==13:
                    p.get_by_role('button',name='继续编排 1 份素材',exact=True).scroll_into_view_if_needed()
                    p.screenshot(path=str(OUT/f'book-structure-pending-{width}.png'),full_page=True)
                    p.get_by_role('button',name='章节操作「另一个拥有二十字以内长名称的章节」',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(1);sheet=metrics(p,width)
                    p.get_by_role('button',name='删除章节',exact=True).click();expect(p.get_by_role('button',name='确认删除章节',exact=True)).to_be_visible();modal=metrics(p,width);p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0)
                else:
                    expect(p.locator('.diary-title')).to_have_text(source['title']);p.screenshot(path=str(OUT/f'book-material-pending-{width}.png'),full_page=True);sheet=None;modal=None
                assert not errors,errors
                row=dict(page=f'm08-p{number:02}',width=width,passed=True,metrics=initial,sheet=sheet,modal=modal)
            except Exception:row=dict(page=f'm08-p{number:02}',width=width,passed=False,failure=traceback.format_exc()[-2500:],errors=errors)
            rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+f'p{number} {width}',flush=True);c.close()
    b.close()
OUT.mkdir(parents=True,exist_ok=True);(OUT/'book-structure-layout-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['passed'] for v in rows) else 1)

