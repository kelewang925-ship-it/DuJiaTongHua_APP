"""Actual refresh/retry/date-sheet/save/back behavior and explicit cached lifecycle."""
import argparse,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_anniversary_calendar import ROOT,DEMO,dependencies as calendar_dependencies
from verify_book_v2_reconciliation import sha

fixture=declarations('verify_time_controls.py')
def dependencies():
    files=calendar_dependencies()
    for n in [9,11]:
        for folder in ['custom','pages']:
            path=f'{folder}/m04-p{n:02d}.html';files[path]=sha(DEMO/path)
        html=(DEMO/f'custom/m04-p{n:02d}.html').read_text(encoding='utf-8')
        for p in re.findall(r'\.\./assets/([a-zA-Z0-9._/-]+)',html):files['assets/'+p]=sha(DEMO/'assets'/p)
    return dict(sorted(files.items()))
def store(p):return p.evaluate('({...localStorage})')
def expect_calendar(p,day):
    expect(p.locator('.date-pill')).to_have_text(day);expect(p.locator('.anniversary-calendar')).to_have_attribute('data-date',day)
def change(p):p.evaluate('()=>{const a=JSON.parse(localStorage.getItem("dujia-prototype-anniversaries"));localStorage.setItem("dujia-prototype-anniversaries",JSON.stringify(a.filter(a=>a.id==="time-future")))}')
def run(p,name):
    fixture['seed'](p,'m04-p07');expect_calendar(p,'2026-10-05')
    if name=='invalid-date-recovery':
        p.evaluate('()=>{const a=JSON.parse(localStorage.getItem("dujia-prototype-anniversaries")).find(a=>a.id==="time-today");a.date="invalid-date";localStorage.setItem("dujia-prototype-anniversaries",JSON.stringify([a]))}')
        p.get_by_role('button',name='刷新纪念日',exact=True).click();expect(p.locator('.date-pill')).to_have_text('编辑日期');expect(p.locator('.anniversary-calendar')).to_be_visible();expect(p.locator('.anniversary-calendar')).to_have_attribute('aria-label','纪念日日期待确认');expect(p.locator('.anniversary-calendar [data-day]')).to_have_count(0)
        p.evaluate('()=>{const a=JSON.parse(localStorage.getItem("dujia-prototype-anniversaries"));a[0].date="2026-10-05";localStorage.setItem("dujia-prototype-anniversaries",JSON.stringify(a))}');before=store(p)
        p.get_by_role('button',name='刷新纪念日',exact=True).click();expect_calendar(p,'2026-10-05');expect(p.locator('.anniversary-calendar')).to_be_visible();assert store(p)==before;return
    if name=='picker-save':
        p.evaluate('localStorage.setItem("dujia-prototype-anniversaries","[]")');p.locator('.plus').click();p.wait_for_url('**/m04-p09.html*');p.locator('[name=name]').fill('日期选择器的新约定');p.get_by_role('textbox',name='纪念日日期',exact=True).click();field=p.get_by_label('选择纪念日日期',exact=True);field.fill('2026-10-09');p.get_by_role('button',name='使用这个日期',exact=True).click();expect(p.locator('dialog')).to_have_count(0);p.locator('.submit').click();p.wait_for_url('**/m04-p07.html*');expect_calendar(p,'2026-10-09');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-anniversaries"))[0].date')=='2026-10-09';return
    if name=='back-refresh':
        p.locator('.date-pill').click();p.wait_for_url('**/m04-p11.html*');p.go_back();expect_calendar(p,'2026-10-05')
    if name=='cached-lifecycle-refresh':
        p.evaluate('()=>{window.dispatchEvent(new PageTransitionEvent("pagehide",{persisted:true}));window.dispatchEvent(new PageTransitionEvent("pageshow",{persisted:true}));}')
    change(p);before=store(p)
    if name=='load-failure-retry':
        p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","anniversary-load")');p.get_by_role('button',name='刷新纪念日',exact=True).click();expect(p.get_by_role('button',name='重试加载纪念日',exact=True)).to_be_visible();expect_calendar(p,'2026-10-05');p.get_by_role('button',name='重试加载纪念日',exact=True).click()
    else:p.get_by_role('button',name='刷新纪念日',exact=True).click()
    expect_calendar(p,'2026-12-24');assert store(p)==before

CASES=['refresh','load-failure-retry','picker-save','back-refresh','cached-lifecycle-refresh','invalid-date-recovery']
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args();out=ROOT/f'evidence/{args.stage}/anniversary-calendar-updates';out.mkdir(parents=True,exist_ok=True);files=dependencies();rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for name in CASES:
            c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(case=name,passed=False)
            try:run(p,name);assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc();p.screenshot(path=str(out/(name+'.png')),full_page=True)
            row.update(errors=errors,effective=p.url);rows.append(row);c.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps(dict(dependency_files=files,producer_sha256=sha(Path(__file__)),fixture_sha256=sha(ROOT/'verify_time_controls.py'),browser=version,viewport=[390,844],locale='zh-CN',timezone='Asia/Shanghai',scope='Six explicit updates/navigation/recovery flows; cached-lifecycle case dispatches PageTransitionEvents and is not a real-device cache/IME certification.',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
