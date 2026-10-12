"""Compare archived/current CSS for focused/error/disabled and full/reduced motion."""
import json,hashlib
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import ROOT,BASE,source

PROPS=['color','backgroundColor','fontFamily','fontSize','lineHeight','padding','margin','borderRadius','borderTopColor','boxShadow','outlineColor','outlineWidth','transitionDuration','animationDuration','animationName','animationTimingFunction','opacity']
def main():
    files=source();history=ROOT/'evidence/history/pre-shared-style-tokens-74b3eca';rows=[]
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for mode in ['no-preference','reduce']:
            observed={}
            for variant in ['archived','current']:
                context=browser.new_context(viewport=dict(width=390,height=844),reduced_motion=mode);p=context.new_page()
                if variant=='archived':
                    def restore(route):
                        name=route.request.url.rsplit('/',1)[-1];path=history/name
                        if path.exists():route.fulfill(status=200,content_type='text/css',body=path.read_bytes())
                        else:route.continue_()
                    p.route('**/assets/prototype-*.css',restore)
                p.goto(BASE+'prototype/components.html');p.evaluate('document.fonts.ready')
                p.evaluate('''()=>{const U=PrototypeUI,box=document.createElement('div'),field=U.components.field({label:'字段状态',value:'原值'});field.input.dataset.contract='field';field.setError('请核对输入');const disabled=U.components.button('禁用按钮',null,{disabled:true});disabled.dataset.contract='disabled';const spinner=U.components.loading({mode:'spinner'});spinner.dataset.contract='spinner';box.append(field.root,disabled,spinner);U.modal({title:'样式状态',content:box,confirm:'关闭'})}''')
                expect(p.locator('dialog[open]')).to_have_count(1);p.locator('[data-contract=field]').focus();p.wait_for_timeout(300)
                observed[variant]=p.evaluate('''props=>{const selectors=['dialog[open]','dialog[open] h2','[data-contract=field]','.prototype-component-error:not([hidden])','[data-contract=disabled]','[data-contract=spinner] .prototype-component-spinner'];return Object.fromEntries(selectors.map(selector=>{const e=document.querySelector(selector),s=getComputedStyle(e);return [selector,Object.fromEntries(props.map(k=>[k,s[k]]))]}).concat([['backdrop',{backgroundColor:getComputedStyle(document.querySelector('dialog'),'::backdrop').backgroundColor}]]))}''',PROPS)
                context.close();assert source()==files
            assert observed['archived']==observed['current'],(mode,observed)
            rows.append(dict(mode=mode,passed=True,observed=observed['current']))
        browser.close()
    (ROOT/'evidence/current/shared-token-motion-results.json').write_text(json.dumps(dict(files=files,archived_css_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in history.glob('prototype-*.css')},results=rows,scope='Archived vs current exact CSS over focused field, inline error, disabled button, spinner, modal and backdrop at390px in full/reduced motion. Supplemental appearance contracts, not complete product flows.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(motion_modes=2,passed=2)))

if __name__=='__main__':main()
