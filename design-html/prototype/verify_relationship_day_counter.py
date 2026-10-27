"""Relationship profile ordinal-day display, live preview and actual save recovery."""
import argparse,hashlib,json,time,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from audit_runtime import INIT
from verify_pet_controls import ROOT,BASE,source

BASIC=[('2026年1月1日','2026-10-06','279'),('2026年10月6日','2026-10-06','1'),('2024年2月28日','2024-03-01','3'),('2023年2月28日','2023-03-01','2'),('2025年12月31日','2026-01-01','2')]
CASES=[('calendar',i) for i in range(len(BASIC))]+[('invalid',v) for v in ['', '2026年2月30日','2026年10月7日']]+[('width',w) for w in [320,360,390,414,430]]+[('save',True),('save',False)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def store(p):return p.evaluate('({...localStorage})')
def seed(p,met='2026年1月1日',today='2026-10-06',bound=True):
    p.goto(BASE+'prototype/review.html');d=data(True);d['dujia-prototype-relationship']['bound']=bound;d['dujia-prototype-relationship'].setdefault('profile',{}).update(nickname='共同小屋',met=met,anniversary='每月 1 日')
    p.evaluate('([d,today])=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));sessionStorage.setItem("dujia-prototype-today",today)}',[d,today]);p.goto(BASE+'pages/m02-p06.html');p.evaluate('document.fonts.ready')
def choose(p,value,apply=True):
    p.locator('#met').click();dialog=p.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text('选择相遇日期');dialog.get_by_label('选择相遇日期',exact=True).fill(value);dialog.get_by_role('button',name='使用这个日期' if apply else '取消',exact=True).click();expect(dialog).to_have_count(0)
def report(path,value):
    tmp=path.with_suffix('.tmp');payload=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    for attempt in range(30):
        try:tmp.write_text(payload,encoding='utf-8');tmp.replace(path);return
        except PermissionError:
            if attempt==29:raise
            time.sleep(.1)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args();out=ROOT/f'evidence/{args.stage}/relationship-day-counter';out.mkdir(exist_ok=True);files=source();rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for kind,value in CASES:
            context=browser.new_context(viewport={'width':value if kind=='width' else 390,'height':844},reduced_motion='reduce');context.add_init_script(INIT);page=context.new_page();page.set_default_timeout(6500);page.set_default_navigation_timeout(20000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));row=dict(kind=kind,value=value,passed=False,errors=errors)
            try:
                if kind=='calendar':
                    met,today,wanted=BASIC[value];seed(page,met,today);before=store(page);expect(page.locator('.days b')).to_have_text(wanted);assert store(page)==before;row.update(met=met,today=today,expected_ordinal=wanted)
                elif kind=='invalid':
                    seed(page);before=store(page);page.locator('#met').evaluate('(e,value)=>{e.value=value;e.dispatchEvent(new Event("input",{bubbles:true}))}',value)
                    expect(page.locator('.days')).to_have_text('相遇日期待补充');assert store(page)==before
                elif kind=='width':
                    seed(page);before=store(page);expect(page.locator('.days b')).to_have_text('279');choose(page,'2026-10-01');expect(page.locator('.days b')).to_have_text('6');expect(page.locator('#met')).to_have_value('2026年10月1日');assert store(page)==before
                    choose(page,'2026-09-01',False);expect(page.locator('.days b')).to_have_text('6');expect(page.locator('#met')).to_have_value('2026年10月1日');assert store(page)==before
                    box=page.locator('.days').bounding_box();screen=page.locator('.screen').bounding_box();assert box['x']>=screen['x'] and box['x']+box['width']<=screen['x']+screen['width']
                    page.screenshot(path=str(out/f'{value}-preview.png'),full_page=True);row['expected_ordinal']='6'
                else:
                    seed(page,bound=value);before=store(page);choose(page,'2026-10-01');expect(page.locator('.days b')).to_have_text('6');assert store(page)==before
                    page.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","profile")');button=page.get_by_role('button',name='保存小资料',exact=True);button.click();expect(page.locator('.prototype-toast')).to_contain_text('资料没有保存成功');expect(button).to_be_enabled();assert store(page)==before;expect(page.locator('#met')).to_have_value('2026年10月1日');expect(page.locator('.days b')).to_have_text('6')
                    button.click();destination='m02-p05' if value else 'm02-p01';page.wait_for_url('**/'+destination+'.html*')
                    after=store(page);old=dict(before);new=dict(after);pair=json.loads(new.pop('dujia-prototype-relationship'));saved_profile=pair['profile'];oldpair=json.loads(old.pop('dujia-prototype-relationship'));assert pair['profile']['met']=='2026年10月1日' and pair['bound']==oldpair['bound'];oldpair.pop('profile');pair.pop('profile');assert pair==oldpair
                    for name in ['nickname','met','anniversary']:
                        key='dujia-profile-'+name;assert new.pop(key)==saved_profile[name];old.pop(key,None)
                    assert new==old
                    page.goto(BASE+'pages/m02-p06.html');expect(page.locator('.days b')).to_have_text('6')
                    if value:
                        page.goto(BASE+'pages/m03-p02.html');expect(page.locator('.hero-copy strong')).to_have_text('5')
                    row.update(destination=destination,result='failed save preserves data/input/preview; retry persists date; reload reflects it; ordinal includes first day and home elapsed count stays unchanged')
                assert not errors;row['passed']=True
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);context.close();assert source()==files;report(out/'results.json',dict(files=files,script_sha256=sha(Path(__file__)),expected_cases=len(CASES),results=rows,accepted_pages=0));print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
