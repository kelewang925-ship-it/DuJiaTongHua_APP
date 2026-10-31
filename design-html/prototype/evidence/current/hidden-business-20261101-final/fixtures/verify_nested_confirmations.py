"""Explicit second-layer destructive/identity paths; cancellation must not write."""
import hashlib
import json
import traceback
from playwright.sync_api import sync_playwright, expect
from audit_runtime import INIT
from audit_hidden_overlays import MODULES, declarations
from verify_overlay_exit_paths import close
from verify_pet_controls import ROOT,source

# Indexes refer to the source-bound observations, with expected titles from controller branches.
CASES={9:('删除日记','删除这篇日记？'),11:('删除日记','删除这篇日记？'),16:('删除照片','删除这张照片？'),
18:('删除重要时刻','删除这个时刻？'),22:('删除纪念日','删除这个纪念日？'),23:('删除纪念日','删除这个纪念日？'),
25:('删除胶囊','删除这个胶囊？'),26:('删除胶囊','删除这个胶囊？'),
30:('删除作品','删除这件作品？'),33:('删除作品','删除这件作品？'),36:('删除作品','删除这件作品？'),39:('删除作品','删除这件作品？'),
47:('删除标签','删除这个标签？'),48:('删除标签','删除这个标签？'),49:('删除标签','删除这个标签？'),
59:('继续身份确认','确认注销演示账号'),99:('永久删除宠物数据','删除确认'),
123:('删除章节','删除「第一章」？'),126:('删除章节','删除「第二章」？'),
124:('删除书页','删除「共同日记」？'),125:('删除书页','删除「共同照片」？'),127:('删除书页','删除「共同重要时刻」？')}

def main():
    out=ROOT/'evidence/current';files=source();raw=(out/'hidden-overlay-observations.json').read_bytes();observations=json.loads(raw)
    assert observations['files']==files
    fixtures={group:declarations(name)for group,name in MODULES.items()};results=[]
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index,(action,title)in CASES.items():
            original=observations['results'][index]
            for method in ['button','back','backdrop']:
                context=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',accept_downloads=True);context.add_init_script(INIT)
                page=context.new_page();page.set_default_timeout(4500);page.set_default_navigation_timeout(15000);errors=[]
                page.on('pageerror',lambda error:errors.append(str(error)))
                row=dict(observation_index=index,page=original['page'],action=action,title=title,method=method)
                try:
                    fixtures[original['group']]['seed'](page,original['page'])
                    trigger=page.locator(original['selector']);trigger.click();dialog=page.locator('dialog[open]')
                    expect(dialog.locator('h2')).to_have_text(original['overlays'][0]['title'])
                    before=page.evaluate('JSON.stringify({...localStorage})');url=page.url;screen=page.locator('.screen').inner_text()
                    dialog.get_by_role('button',name=action,exact=True).click()
                    expect(dialog).to_have_count(1);expect(dialog.locator('h2')).to_have_text(title)
                    expect(dialog.get_by_role('button',name='取消',exact=True)).to_be_focused()
                    assert before==page.evaluate('JSON.stringify({...localStorage})'),'Opening final confirmation wrote data'
                    close(page,method);expect(page.locator('dialog[open]')).to_have_count(0)
                    assert before==page.evaluate('JSON.stringify({...localStorage})'),'Final cancellation wrote data'
                    assert page.url==url and page.locator('.screen').inner_text()==screen,'Final cancellation changed underlying page'
                    expect(trigger).to_be_focused();assert not errors,errors
                    row.update(passed=True,safe_cancel_focus=True,storage_preserved=True,underlying_page_preserved=True)
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-2500:])
                row['errors']=errors;results.append(row);context.close()
                assert source()==files
                value=dict(files=files,observations_sha256=hashlib.sha256(raw).hexdigest(),expected_cases=len(CASES)*3,results=results,accepted_pages=0)
                temporary=out/'nested-confirmation-results.json.tmp';temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temporary.replace(out/'nested-confirmation-results.json')
                print(('PASS 'if row['passed']else'FAIL ')+str(len(results))+'/'+str(len(CASES)*3)+' '+row['page']+' '+action+' '+method,flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(results),passed=sum(row['passed']for row in results))))
    raise SystemExit(0 if all(row['passed']for row in results)else 1)

if __name__=='__main__':main()
