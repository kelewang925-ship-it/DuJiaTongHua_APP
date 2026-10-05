"""Two tabs: preserve drafts and validate current pet/source before writing."""
from pathlib import Path
import json, traceback
from playwright.sync_api import sync_playwright, expect
from pet_test_helpers import seed, go, value

OUT = Path(__file__).resolve().parent / 'evidence/current'

def peer_tab(p):
    other = p.context.new_page()
    other.goto('http://127.0.0.1:8765/prototype/review.html')
    return other

def story_draft(p):
    seed(p); go(p,18)
    p.get_by_role('button',name='写一页成长故事',exact=True).click()
    field=p.get_by_label('成长故事内容',exact=True); field.fill('保留我的未保存故事')
    other=peer_tab(p)
    other.evaluate('''()=>{const v=JSON.parse(localStorage.getItem('dujia-prototype-pet'));v.logs.unshift({id:'peer-live',type:'water',date:'2026-10-05',actor:'阿舟',text:'另一半添水',story:true});localStorage.setItem('dujia-prototype-pet',JSON.stringify(v));}''')
    expect(p.locator('.prototype-toast')).to_contain_text('当前输入保留')
    expect(field).to_have_value('保留我的未保存故事')
    p.get_by_role('button',name='保存成长故事',exact=True).click()
    expect(p.locator('dialog[open]')).to_have_count(0)
    logs=value(p)['logs']; assert any(v['id']=='peer-live' for v in logs)
    assert sum(v['text']=='保留我的未保存故事' for v in logs)==1

def source_reply(p):
    seed(p,logs=[dict(id='source-live',type='source',sourceId='shared-live',sourceKind='record',date='2026-10-05',actor='阿舟',text='关联了共同记录',story=True)])
    p.evaluate('''localStorage.setItem('dujia-prototype-records',JSON.stringify([{id:'shared-live',type:'diary',visibility:'shared',status:'published',title:'共同记录',body:'LIVE-PRIVATE-BODY',author:'阿舟'}]))''')
    go(p,19,'?id=source-live');expect(p.locator('.note')).to_contain_text('LIVE-PRIVATE-BODY')
    p.get_by_role('button',name='回应这一页',exact=True).click()
    field=p.get_by_label('回应内容',exact=True);field.fill('仍然未保存的回应')
    other=peer_tab(p)
    other.evaluate('''()=>{const v=JSON.parse(localStorage.getItem('dujia-prototype-records'));v[0].visibility='private';localStorage.setItem('dujia-prototype-records',JSON.stringify(v));}''')
    expect(p.locator('.note')).to_contain_text('已不可见')
    expect(p.locator('.note')).not_to_contain_text('LIVE-PRIVATE-BODY')
    expect(field).to_have_value('仍然未保存的回应')
    p.get_by_role('button',name='保存回应',exact=True).click()
    expect(p.locator('.prototype-toast')).to_contain_text('已不可见')
    assert not value(p)['logs'][0].get('comments')
    p.keyboard.press('Escape');p.get_by_role('button',name='继续编辑',exact=True).click()
    expect(field).to_have_value('仍然未保存的回应')

def replaced_pet(p):
    seed(p);go(p,12)
    p.get_by_role('button',name='小花围巾 已拥有',exact=True).click()
    other=peer_tab(p)
    other.evaluate('''()=>{const v=JSON.parse(localStorage.getItem('dujia-prototype-pet'));v.id='replacement-pet';v.name='新伙伴';localStorage.setItem('dujia-prototype-pet',JSON.stringify(v));}''')
    expect(p.locator('.prototype-toast')).to_contain_text('当前输入保留')
    before=value(p);p.locator('#save').click()
    expect(p.locator('.prototype-toast')).to_contain_text('宠物已经发生变化')
    assert value(p)==before

rows=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,run in {'story-draft-preserved-peer-log-retained':story_draft,'private-source-masked-reply-draft-preserved':source_reply,'replaced-pet-rejects-old-outfit-draft':replaced_pet}.items():
        context=browser.new_context(viewport={'width':390,'height':844});p=context.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p);assert not errors;row={'case':name,'passed':True}
        except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-2200:]}
        row.update(errors=errors,final_url=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);context.close()
    browser.close()
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'pet-live-edit-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
