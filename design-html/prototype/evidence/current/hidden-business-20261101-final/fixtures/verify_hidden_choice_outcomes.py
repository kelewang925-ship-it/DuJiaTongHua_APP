"""Business outcomes for selected hidden actions; does not infer success from closure."""
import hashlib,json,traceback
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright,expect
from audit_runtime import INIT
from audit_current_runtime import data
from audit_hidden_overlays import declarations
from verify_pet_controls import ROOT,DEMO,BASE,source

OUT=ROOT/'evidence/current/hidden-choice-outcomes'
record_seed=declarations('verify_record_controls.py')['seed']
CASES=[('auth',v) for v in ['phone-recovery','phone-register','code','cancel']]+[('share',v) for v in ['copy','save','wait','cancel','copy-denied']]+[(kind,v) for kind in ['diary','photo'] for v in ['shared','private','clear','cancel']]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def store(page):return page.evaluate('JSON.stringify({...localStorage})')
def seed(page,identifier):
    page.goto(BASE+'prototype/review.html')
    page.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));sessionStorage.setItem("dujia-prototype-peer-response","manual")}',data(False))
    page.goto(BASE+'pages/'+identifier+'.html');page.evaluate('document.fonts.ready')

def main():
    OUT.mkdir(exist_ok=True);files=source();rows=[]
    observed=ROOT/'evidence/current/hidden-overlay-observations.json'
    for path,sha in files.items():
        served=path.replace('custom/','pages/',1) if path.startswith('custom/') else path
        with urlopen(BASE+served,timeout=15) as response:assert hashlib.sha256(response.read()).hexdigest()==sha,path
    styles={p.relative_to(DEMO).as_posix():digest(p) for p in (DEMO/'assets').glob('*.css')}
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for kind,mode in CASES:
            context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',accept_downloads=True,permissions=['clipboard-read','clipboard-write'])
            context.add_init_script(INIT);page=context.new_page();page.set_default_timeout(6000);page.set_default_navigation_timeout(20000)
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            row=dict(kind=kind,mode=mode,passed=False,errors=errors)
            try:
                if kind=='auth':
                    seed(page,'m01-p07')
                    if mode=='phone-register':
                        page.evaluate('()=>{const k="dujia-prototype-challenge",v=JSON.parse(sessionStorage.getItem(k));v.purpose="register";sessionStorage.setItem(k,JSON.stringify(v))}')
                        page.reload()
                    before=store(page);url=page.url
                    page.locator('#switch').click();dialog=page.locator('dialog[open]')
                    label='重新填写手机号' if mode.startswith('phone') else '查看演示验证码' if mode=='code' else '取消'
                    row.update(observation_index=4,control_label=label)
                    dialog.get_by_role('button',name=label,exact=True).click()
                    if mode.startswith('phone'):
                        expected='m01-p03' if mode.endswith('register') else 'm01-p04'
                        page.wait_for_url('**/'+expected+'.html*');row['destination']=expected
                    elif mode=='code':
                        expect(page.locator('dialog[open] h2')).to_have_text('演示验证码')
                        expect(page.locator('dialog[open]')).to_contain_text('284631')
                        page.locator('dialog[open]').get_by_role('button',name='知道了',exact=True).click()
                        expect(page.locator('dialog[open]')).to_have_count(0);assert page.url==url
                        row['result']='second modal contains actual demo code'
                    else:
                        expect(dialog).to_have_count(0);assert page.url==url
                    assert store(page)==before
                elif kind=='share':
                    seed(page,'m02-p02');before=store(page);url=page.url
                    if mode=='copy-denied':page.evaluate('()=>{navigator.clipboard.writeText=async()=>{throw new DOMException("Denied for QA","NotAllowedError")}}')
                    page.locator('#share').click();dialog=page.locator('dialog[open]')
                    label={'copy':'复制邀请链接','copy-denied':'复制邀请链接','save':'保存邀请卡','wait':'查看邀请进度','cancel':'取消'}[mode]
                    row.update(observation_index=5,control_label=label)
                    button=dialog.get_by_role('button',name=label,exact=True)
                    if mode=='save':
                        with page.expect_download() as download:button.click()
                        value=download.value;raw=Path(value.path()).read_text(encoding='utf-8')
                        assert value.suggested_filename=='独家童话邀请卡.svg'
                        assert '<svg' in raw and 'XH7K-9M2Q' in raw
                        row.update(download_name=value.suggested_filename,download_sha256=hashlib.sha256(raw.encode()).hexdigest())
                    else:button.click()
                    if mode=='copy':
                        expect(page.locator('.prototype-toast')).to_contain_text('已复制')
                        value=page.evaluate('navigator.clipboard.readText()');assert value==BASE+'pages/m02-p03.html?code=XH7K9M2Q';row['clipboard']=value
                    elif mode=='copy-denied':
                        expect(page.locator('dialog[open] h2')).to_have_text('可以手动复制')
                        expect(page.locator('dialog[open]')).to_contain_text(BASE+'pages/m02-p03.html?code=XH7K9M2Q')
                        page.locator('dialog[open]').get_by_role('button',name='知道了',exact=True).click()
                        row['result']='clipboard rejection exposes exact link for manual copy'
                    elif mode=='wait':
                        page.wait_for_url('**/m02-p07.html*')
                        invite=page.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-invite"))')
                        assert invite['status']=='pending' and invite['autoAt']>0
                        old=json.loads(before);new=json.loads(store(page));old.pop('dujia-prototype-invite');new.pop('dujia-prototype-invite');assert old==new
                        row['result']='pending invite and progress page; unrelated local data unchanged'
                    expect(page.locator('dialog[open]')).to_have_count(0)
                    if mode!='wait':assert store(page)==before and page.url==url
                else:
                    is_diary=kind=='diary';identifier='m03-p06' if is_diary else 'm03-p10'
                    record_seed(page,identifier);before=store(page)
                    state_key='dujia-diary-list-state' if is_diary else 'dujia-photo-album-state'
                    cards=page.locator('.prototype-diary-card' if is_diary else '.prototype-photo-card')
                    original=cards.all_text_contents()
                    page.locator('#filter').click();dialog=page.locator('dialog[open]');select=dialog.locator('select')
                    select.select_option('shared' if mode=='clear' else 'private' if mode=='cancel' else mode)
                    label='取消' if mode=='cancel' else '应用筛选'
                    row.update(observation_index=8 if is_diary else 12,control_label='清除筛选' if mode=='clear' else label,native_field='可见范围' if is_diary else '照片可见范围')
                    dialog.get_by_role('button',name=label,exact=True).click();expect(dialog).to_have_count(0)
                    if mode=='clear':
                        page.locator('#filter').click();page.locator('dialog[open]').get_by_role('button',name='清除筛选',exact=True).click()
                        expect(page.locator('dialog[open]')).to_have_count(0)
                    if mode=='cancel':
                        assert cards.all_text_contents()==original
                        assert page.evaluate('k=>sessionStorage.getItem(k)',state_key) is None
                    else:
                        state=page.evaluate('k=>JSON.parse(sessionStorage.getItem(k))',state_key)
                        expected='all' if mode=='clear' else mode;assert state['visibility']==expected
                        if mode=='private':
                            expect(cards).to_have_count(1 if is_diary else 0)
                            if is_diary:expect(cards).to_contain_text('自己的日记')
                            else:expect(page.locator('.prototype-photo-empty')).to_contain_text('没有符合条件的照片')
                        elif mode=='shared':
                            expect(cards).to_have_count(1);expect(cards).to_contain_text('共同日记' if is_diary else '共同照片')
                        else:assert cards.all_text_contents()==original
                        row['persisted_state']=state
                    assert store(page)==before
                    row['visible_cards']=cards.all_text_contents()
                assert not errors;row['passed']=True
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);context.close();assert source()==files
            report=dict(files=files,styles=styles,script_sha256=digest(Path(__file__)),observations_sha256=digest(observed),results=rows,expected_cases=len(CASES),accepted_pages=0,scope='Four observed overlay triggers: explicit declared choices and representative business outcomes; not all hidden controls or final visual acceptance')
            temporary=OUT/'results.json.tmp';temporary.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temporary.replace(OUT/'results.json')
            print(('PASS' if row['passed'] else 'FAIL')+' '+kind+'/'+mode,flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
