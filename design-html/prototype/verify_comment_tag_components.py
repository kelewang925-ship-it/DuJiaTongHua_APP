"""Real comment avatars and tag management: layout and preserved business behavior."""
import json,sys,traceback,hashlib
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_pet_controls import ROOT,source

def main():
    files=source();baseline='--baseline'in sys.argv;repair='--replay-tags'in sys.argv;rows=[];retained=[];replayed=[];prior_sha=None;record=declarations('verify_record_controls.py');settings=declarations('verify_settings_controls.py')
    if repair:
        raw=(ROOT/'evidence/baseline/comment-tag-components-first-pass.json').read_bytes();prior=json.loads(raw);assert prior['files']==files and len(prior['results'])==17
        assert [(r['page'],r['width'])for r in prior['results']if not r['passed']]==[('m06-p05',w)for w in [320,360,390,414,430]]
        rows=prior['results'];retained=[i for i,r in enumerate(rows)if r['passed']];assert len(retained)==12;prior_sha=hashlib.sha256(raw).hexdigest()
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in ([390]if baseline else[320,360,390,414,430]):
            for identifier,kind,target in ([]if repair else[('m03-p08','diary','audit-diary'),('m03-p12','photo','audit-photo')]):
                context=browser.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=context.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(page=identifier,width=width)
                try:
                    record['seed'](p,identifier);input=p.locator('#reply');submit=p.locator('#message [type=submit]');input.fill('组件回归回应');submit.evaluate('b=>{b.click();b.click()}');expect(input).to_have_value('');comments=p.locator('[aria-label=留言]');expect(comments.locator('article')).to_have_count(1);avatar=comments.locator('.prototype-component-avatar');expect(avatar).to_have_count(1);expect(avatar).to_have_attribute('aria-label','小满');expect(avatar).to_have_attribute('aria-hidden','true');expect(comments.locator('article b')).to_have_text('小满');expect(comments.locator('article p')).to_have_text('组件回归回应');avatar.evaluate('e=>e.scrollIntoView({block:"center"})');rect=avatar.bounding_box();assert rect['width']>=44 and rect['height']>=44 and rect['x']>=0 and rect['x']+rect['width']<=width,rect
                    old=p.evaluate('JSON.stringify({...localStorage})');input.fill('失败后重试回应');p.evaluate('op=>sessionStorage.setItem("dujia-prototype-fail-next",op)',kind+'-comment');submit.click();expect(p.locator('.prototype-toast')).to_contain_text('未发送成功'if kind=='photo'else'没有发送成功');expect(input).to_have_value('失败后重试回应');assert p.evaluate('JSON.stringify({...localStorage})')==old;expect(comments.locator('.prototype-component-avatar')).to_have_count(1);submit.click();expect(input).to_have_value('');expect(comments.locator('.prototype-component-avatar')).to_have_count(2);stored=p.evaluate('id=>JSON.parse(localStorage.getItem("dujia-prototype-records")).find(v=>v.id===id).comments',target);assert [v['text']for v in stored]==['组件回归回应','失败后重试回应'];assert not errors,errors;row.update(passed=True,failure_retry=True,actual_comments=len(stored))
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-1800:])
                row['errors']=errors;rows.append(row);context.close();assert source()==files
            context=browser.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=context.new_page();p.set_default_timeout(6000);row=dict(page='m06-p05',width=width);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:
                settings['seed'](p,'m06-p05');list=p.locator('.prototype-settings-tags');expect(list.locator('.prototype-component-tag')).to_have_count(3);assert set(list.locator('.prototype-component-tag').all_text_contents())=={'个人标签','共同标签','旅行'};expect(list.locator('.prototype-component-divider')).to_have_count(1)
                before=p.evaluate('JSON.stringify({...localStorage})')
                for name in ['个人标签','共同标签']:
                    tag=list.get_by_role('button',name=name,exact=True);assert tag.get_attribute('aria-pressed')is None;tag.evaluate('e=>e.scrollIntoView({block:"center"})');rect=tag.bounding_box();assert rect['height']>=44 and rect['width']>=44 and rect['x']>=0 and rect['x']+rect['width']<=width,rect;tag.click();expect(p.locator('dialog h2')).to_have_text(name);p.keyboard.press('Escape');expect(p.locator('dialog[open]')).to_have_count(0);expect(tag).to_be_focused();assert p.evaluate('JSON.stringify({...localStorage})')==before
                tag=list.get_by_role('button',name='个人标签',exact=True);tag.click();p.get_by_role('button',name='编辑标签',exact=True).click();dialog=p.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text('编辑标签');dialog.get_by_label('标签名称',exact=True).fill('组件重命名');dialog.locator('[type=submit]').click();expect(p.locator('dialog[open]')).to_have_count(0);expect(list.get_by_role('button',name='组件重命名',exact=True)).to_be_visible();assert p.evaluate('PrototypePreferences.tags().find(v=>v.id==="settings-tag").name')=='组件重命名';assert p.evaluate('PrototypePreferences.tags().find(v=>v.id==="settings-joint-tag").name')=='共同标签';expect(list.locator('.prototype-component-divider')).to_have_count(1);assert not errors,errors;row.update(passed=True,action_cancel_preserved=True,rename_verified=True)
            except Exception:row.update(passed=False,failure=traceback.format_exc()[-1800:])
            row['errors']=errors
            if repair:
                index=next(i for i,r in enumerate(rows)if r.get('page')=='m06-p05'and r.get('width')==width);rows[index]=row;replayed.append(index)
            else:rows.append(row)
            context.close();assert source()==files;print(str(width)+'px '+str(sum(r['passed']for r in rows if r.get('width')==width))+'/3',flush=True)
        context=browser.new_context();p=context.new_page();settings['seed'](p,'m06-p05')
        for mode in ([]if repair else['toggle','action']):
            row=dict(contract=mode)
            try:
                observed=p.evaluate('''mode=>{let changes=[],activations=0;const b=PrototypeUI.components.tag({label:'组件契约',selected:mode==='action'?null:false,onChange:v=>changes.push(v),onActivate:()=>activations++});document.body.append(b);b.click();b.click();const result={pressed:b.getAttribute('aria-pressed'),changes,activations};b.remove();return result}''',mode);row['observed']=observed;assert observed==({'pressed':'false','changes':[True,False],'activations':0}if mode=='toggle'else{'pressed':None,'changes':[],'activations':2}),observed;row['passed']=True
            except Exception:row.update(passed=False,failure=traceback.format_exc()[-1200:])
            rows.append(row)
        context.close();browser.close()
    path=ROOT/('evidence/baseline/comment-tag-components-before.json'if baseline else'evidence/current/comment-tag-components-results.json');path.write_text(json.dumps(dict(files=files,results=rows,retained_baseline_sha256=prior_sha,retained_indices=retained,replayed_indices=replayed,accepted_pages=0,scope='Diary/photo actual replies, duplicate activation and demonstration failure/retry; tag action menus/cancel/rename and divider at five widths, plus default/action Tag contracts. Not whole114-page/global/visual acceptance.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(rows),passed=sum(r['passed']for r in rows))));raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
