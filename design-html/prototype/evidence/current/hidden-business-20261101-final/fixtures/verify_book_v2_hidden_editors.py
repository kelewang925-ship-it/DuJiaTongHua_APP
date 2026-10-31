"""Reuse exact editor business contracts, bound to the current V2 overlay inventory."""
import json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_book_v2_reconciliation import ROOT,dependencies,sha

old=declarations('verify_hidden_book_editor_outcomes.py')
legacy=declarations('verify_book_controls.py')
BINDINGS={101:(5,'使用封面照片'),108:(9,'更换摘录'),109:(9,'选择照片'),111:(10,'照片 1 · 裁剪或替换'),112:(10,'照片 2 · 裁剪或替换'),113:(10,'照片 3 · 裁剪或替换'),114:(10,'添加照片'),115:(10,'添加贴纸'),116:(11,'更换照片'),117:(11,'选择重要时刻'),119:(12,'工坊作品'),120:(12,'换内容'),121:(12,'换照片')}

def main():
    out=ROOT/'evidence/current/book-v2-hidden-editors';out.mkdir(parents=True,exist_ok=True);files=dependencies();inventory_path=ROOT/'evidence/current/book-v2-hidden/inventory.json';inventory=json.loads(inventory_path.read_text(encoding='utf-8'));assert inventory['dependency_files']==files;rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=browser.version
        for index,label in old['CASES']:
            n,trigger=BINDINGS[index];page_id=f'm08-p{n:02d}';observations=[r for r in inventory['results'] if r['page']==page_id and r['trigger']==trigger];assert len(observations)==1,(page_id,trigger)
            observation=observations[0];context=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');page=context.new_page();page.set_default_timeout(6500);page.set_default_navigation_timeout(15000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));row=dict(original_suite_case_id=index,page=page_id,trigger=trigger,control_label=label,passed=False)
            try:
                legacy['seed'](page,page_id);page.evaluate(old['PREPARE'],dict(index=index,action=label));page.reload();expect(page.locator('.screen')).to_have_attribute('aria-busy','false');expect(page.locator('.book-load')).to_have_count(0)
                before=old['store'](page);oldbooks=old['books'](page);beforebook=next(b for b in oldbooks if b['id']=='book-state');beforepage=next(p for p in beforebook['pages'] if p['id']=='page-state')
                page.locator(observation['selector']).click();dialog=page.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text(observation['expected_title']);dialog.get_by_role('button',name=label,exact=True).click()
                if index==111 and label=='替换这张照片':
                    expect(dialog.locator('h2')).to_have_text('选择共同素材');dialog.get_by_role('button',name='共同照片',exact=True).click()
                elif index==111 and label=='裁剪这张照片':
                    expect(dialog.locator('h2')).to_have_text('裁剪照片')
                    for field,number in [('水平位置',30),('垂直位置',70),('缩放',1.5)]:
                        slider=dialog.get_by_label(field,exact=True);slider.evaluate('(e,v)=>{e.value=String(v);e.dispatchEvent(new Event("input",{bubbles:true}))}',number)
                    dialog.get_by_role('button',name='应用裁剪',exact=True).click()
                expect(dialog).to_have_count(0);assert old['store'](page)==before,'Chooser persisted before explicit parent save'
                if index==111 and label=='移除这张照片':
                    expect(page.locator('.book-photo-preview')).to_contain_text('从共同照片中挑选一张');page.locator('.done').click();expect(page.locator('.prototype-toast')).to_contain_text('请至少选择一张共同照片');expect(page.locator('.done')).to_be_enabled();assert old['store'](page)==before
                    page.locator('[data-tool="添加照片"]').click();page.locator('dialog[open]').get_by_role('button',name='备用photo',exact=True).click();expect(page.locator('dialog[open]')).to_have_count(0);assert old['store'](page)==before
                if index==101:
                    expect(page.locator('.toggle')).to_have_attribute('aria-checked','true');page.locator('.next').click();destination='m08-p13' if beforebook.get('start')=='blank' else 'm08-p06';page.wait_for_url('**/'+destination+'.html*')
                else:page.locator('.done').click();destination='m08-p13';page.wait_for_url('**/m08-p13.html*')
                result=next(b for b in old['books'](page) if b['id']=='book-state');saved=next(p for p in result['pages'] if p['id']=='page-state')
                if index in old['SOURCES']:
                    kind,_,field=old['SOURCES'][index];wanted=old['REFS'][kind]
                    if field=='coverPhoto':assert result[field]==wanted
                    elif field=='photos':
                        assert len(saved['photos'])==2 and saved['photos'][-1]['source']==wanted and saved['photos'][0]['source']==dict(kind='photo',id='alternate-photo')
                    else:assert saved[field]==wanted
                    if index in [108,109,116,117,120,121]:assert beforepage.get(field)!=wanted
                    row['result']='exact '+kind+' reference saved in '+field+' only after parent save';row['expected_reference']=wanted
                elif index==111:
                    if label=='替换这张照片':assert saved['photos'][0]['source']==old['REFS']['photo'] and len(saved['photos'])==1
                    elif label=='裁剪这张照片':assert saved['photos'][0]['crop']==dict(x=30,y=70,zoom=1.5)
                    else:assert len(saved['photos'])==1 and saved['photos'][0]['source']==dict(kind='photo',id='alternate-photo')
                    row['result']='photo operation remains candidate until parent save; exact replacement/crop/removal and last-photo recovery verified'
                else:assert saved['stickers']==[label];row['result']='exact sticker saved once after parent save'
                assert [p for p in beforebook['pages'] if p['id']!='page-state']==[p for p in result['pages'] if p['id']!='page-state']
                assert [b for b in oldbooks if b['id']!='book-state']==[b for b in old['books'](page) if b['id']!='book-state']
                old['unchanged_except_books'](before,old['store'](page));row['destination']=destination;assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc();page.screenshot(path=str(out/(str(index)+'-'+str(len(rows))+'.png')),full_page=True)
            row.update(errors=errors,effective=page.url);rows.append(row);context.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+str(index)+' '+label,flush=True)
        browser.close()
    report=dict(dependency_files=files,producer_sha256=sha(Path(__file__)),current_inventory_sha256=sha(inventory_path),original_contract_suite_sha256=sha(ROOT/'verify_hidden_book_editor_outcomes.py'),fixture_sha256=sha(ROOT/'verify_book_controls.py'),browser=version,viewport=[390,844],locale='zh-CN',timezone='Asia/Shanghai',scope='18 exact current editor chooser/crop/sticker outcomes; original contracts are reused, current trigger bindings are explicit; not an exhaustive hidden-state claim.',results=rows)
    (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Hidden editor outcomes:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
