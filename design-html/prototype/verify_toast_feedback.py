"""Real Toast visibility/layout/lifetime and dialog handoff; isolated local fixtures."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import traceback

from playwright.sync_api import sync_playwright, expect
from audit_hidden_overlays import declarations
from verify_pet_controls import ROOT, DEMO, BASE, source

LONG = '共同数据已更新，当前输入保留；保存时将核对最新记录'


def stored(page):
    return page.evaluate('JSON.stringify({...localStorage})')


def layout(page, controls):
    metrics = page.locator('.prototype-toast').evaluate('''(node,selector)=>{
      const r=node.getBoundingClientRect(),style=getComputedStyle(node);
      return {rect:r.toJSON(),width:innerWidth,height:innerHeight,parent:node.parentElement.tagName,
       role:node.getAttribute('role'),kind:node.dataset.kind,pointerEvents:style.pointerEvents,
       buttons:[...document.querySelectorAll(selector)].filter(e=>e.getClientRects().length).map(e=>{const b=e.getBoundingClientRect();return {text:e.textContent,rect:b.toJSON(),overlap:b.width>0&&b.height>0&&b.bottom>0&&b.top<innerHeight&&r.left<b.right&&r.right>b.left&&r.top<b.bottom&&r.bottom>b.top}})}}''', controls)
    assert metrics['rect']['left'] >= 15 and metrics['rect']['right'] <= metrics['width']-15, metrics
    assert metrics['rect']['top'] >= 0 and metrics['rect']['bottom'] <= metrics['height'], metrics
    assert metrics['pointerEvents'] == 'none'
    assert not any(button['overlap'] for button in metrics['buttons']), metrics
    return metrics


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');args=parser.parse_args()
    out=ROOT/('evidence/baseline/toast-feedback' if args.baseline else 'evidence/current/toast-feedback');out.mkdir(parents=True,exist_ok=True)
    files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')}
    if args.baseline:
        for name in ['prototype-ui.js','prototype-ui.css']:
            target=out/name;assert not target.exists();target.write_bytes((DEMO/'assets'/name).read_bytes())
    fixtures={name:declarations('verify_'+name+'_controls.py') for name in ['record','book']}
    cases=[('body',width,height,kind,'reduce') for width in [320,390] for height in [420,844] for kind in ['success','error','info']]
    cases += [('peer',width,420,'info',mode) for width in [320,390] for mode in ['reduce','no-preference']]
    cases += [('save',width,420,'success','reduce') for width in [320,390]]
    cases += [('lifetime',390,844,kind,'no-preference') for kind in ['success','error','info']]
    cases += [('replace',320,420,'info','reduce')]
    assert len(cases)==22
    rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index,(scenario,width,height,kind,motion) in enumerate(cases):
            context=browser.new_context(viewport=dict(width=width,height=height),reduced_motion=motion)
            page=context.new_page();page.set_default_timeout(5500);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            row=dict(case=scenario,width=width,height=height,kind=kind,motion=motion)
            try:
                fixtures['book' if scenario in ['peer','save'] else 'record']['seed'](page,'m08-p21' if scenario in ['peer','save'] else 'm03-p05')
                page.evaluate('document.documentElement.style.setProperty("--ui-safe-top","44px");document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
                if scenario=='body':
                    page.locator('#diary .submit').scroll_into_view_if_needed();before=stored(page)
                    page.evaluate('([message,kind])=>PrototypeUI.toast(message,kind)',[LONG,kind])
                    row['layout']=layout(page,'#diary .submit');assert stored(page)==before
                elif scenario=='peer':
                    page.locator('.rename').click();expect(page.locator('dialog[open]')).to_have_count(1);page.wait_for_timeout(320)
                    field=page.get_by_role('textbox',name='回忆册名称',exact=True);value=field.input_value()
                    peer=context.new_page();peer.goto(BASE+'prototype/review.html');peer.evaluate('()=>{const key="dujia-prototype-books",v=JSON.parse(localStorage.getItem(key));v[0].name="另一处更新的书名";localStorage.setItem(key,JSON.stringify(v))}')
                    expect(page.locator('.prototype-toast')).to_contain_text('共同数据已更新')
                    assert page.locator('.prototype-toast').evaluate('node=>!!node.closest("dialog[open]")'), 'Toast outside native dialog top layer'
                    row['layout']=layout(page,'dialog[open] button');expect(field).to_have_value(value)
                    page.screenshot(path=str(out/f'{index:02}-peer.png'))
                    before=stored(page);page.get_by_role('button',name='取消',exact=True).click();expect(page.locator('dialog')).to_have_count(0)
                    expect(page.locator('.prototype-toast')).to_have_attribute('data-visible','true')
                    assert page.locator('.prototype-toast').evaluate('node=>node.parentElement===document.body&&node.isConnected')
                    assert stored(page)==before;peer.close();row['closed_dialog_kept_feedback']=True
                elif scenario=='save':
                    page.locator('.rename').click();page.get_by_role('textbox',name='回忆册名称',exact=True).fill('反馈保存交接')
                    page.get_by_role('button',name='保存书名',exact=True).click();expect(page.locator('dialog')).to_have_count(0)
                    expect(page.locator('.prototype-toast')).to_have_attribute('data-visible','true')
                    assert page.locator('.prototype-toast').evaluate('node=>node.parentElement===document.body&&node.isConnected')
                    assert page.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-books"))[0].name')=='反馈保存交接'
                    row['saved_value_and_feedback_survived']=True
                elif scenario=='lifetime':
                    before=stored(page);start=time.perf_counter();page.evaluate('kind=>PrototypeUI.toast("反馈计时验证",kind)',kind)
                    expect(page.locator('.prototype-toast')).to_have_attribute('data-visible','true')
                    expect(page.locator('.prototype-toast')).to_have_attribute('role','alert' if kind=='error' else 'status')
                    page.wait_for_function('document.querySelector(".prototype-toast").dataset.visible==="false"',timeout=4200)
                    row['elapsed_seconds']=time.perf_counter()-start;assert 2.45<=row['elapsed_seconds']<4.2
                    page.wait_for_timeout(200);assert float(page.locator('.prototype-toast').evaluate('e=>getComputedStyle(e).opacity'))<0.05
                    assert stored(page)==before
                else:
                    page.evaluate('PrototypeUI.toast("第一条")');page.wait_for_timeout(1300);page.evaluate('PrototypeUI.toast("后来的提示")');page.wait_for_timeout(1400)
                    expect(page.locator('.prototype-toast')).to_have_attribute('data-visible','true');expect(page.locator('.prototype-toast')).to_have_text('后来的提示')
                    page.wait_for_function('document.querySelector(".prototype-toast").dataset.visible==="false"',timeout=2100)
                    assert page.locator('.prototype-toast').count()==1;row['older_timer_did_not_hide_new_message']=True
                assert not errors,errors;row['passed']=True
            except Exception:
                row.update(passed=False,failure=traceback.format_exc()[-2400:]);page.screenshot(path=str(out/f'{index:02}-failure.png'))
            row['errors']=errors;rows.append(row);context.close();assert source()==files
            report=dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,accepted_pages=0,
                        scope='22 shared feedback contracts over actual editor/dialog fixtures, including real peer storage event and real save. Timers use real wall time. Not human visual or all114-state acceptance.')
            (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+scenario+' '+str(width)+'x'+str(height)+' '+kind+' '+motion,flush=True)
        browser.close()
    print(json.dumps(dict(cases=22,passed=sum(row['passed'] for row in rows))),flush=True)
    raise SystemExit(0 if all(row['passed'] for row in rows) else 1)


if __name__=='__main__':main()
