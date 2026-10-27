"""Observe real date-derived countdown geometry before choosing its repair."""
import hashlib,json
from datetime import date,timedelta
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from audit_runtime import INIT
from verify_pet_controls import ROOT,BASE,source

def main():
    out=ROOT/'evidence/current/countdown-diagnostic';out.mkdir(exist_ok=True);files=source();rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in [320,360,390,414,430]:
            for days in [1,80,365,3650]:
                context=browser.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');context.add_init_script(INIT)
                page=context.new_page();page.set_default_navigation_timeout(15000);page.goto(BASE+'prototype/review.html');values=data(True)
                item=dict(id='countdown-probe',name='真实日期倒计时',date=(date(2026,10,5)+timedelta(days=days)).isoformat(),repeat=False,enabled=True,reminderDays=3)
                values['dujia-prototype-anniversaries']=[item]
                page.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-05");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',values)
                page.goto(BASE+'pages/m04-p10.html?id=countdown-probe');page.evaluate('document.fonts.ready');expect(page.locator('.number')).to_have_text(str(days))
                boxes=page.evaluate('''()=>Object.fromEntries(['.screen','.number','.days','.date','.still'].map(s=>{const r=document.querySelector(s).getBoundingClientRect();return [s,{left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}];}))''')
                n,u,s=boxes['.number'],boxes['.days'],boxes['.screen']
                overlap=min(n['right'],u['right'])>max(n['left'],u['left']) and min(n['bottom'],u['bottom'])>max(n['top'],u['top'])
                assert page.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-anniversaries"))')==[item]
                rows.append(dict(width=width,days=days,bounds=boxes,number_unit_rect_overlap=overlap,number_exceeds_viewport=n['right']>s['right'],storage_preserved=True))
                if width==390 and days in [80,3650]:page.screenshot(path=str(out/f'390-{days}.png'),full_page=True)
                context.close()
        browser.close()
    assert source()==files
    value=dict(scope='Current original countdown layout diagnosis, not repair or acceptance; actual stored dates and real date arithmetic, no DOM day replacement.',files=files,script_sha256=hashlib.sha256(__import__('pathlib').Path(__file__).read_bytes()).hexdigest(),cases=rows,accepted_pages=0)
    (out/'results.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(rows),unit_overlap=sum(r['number_unit_rect_overlap'] for r in rows),viewport_overflow=sum(r['number_exceeds_viewport'] for r in rows),storage_preserved=True)))

if __name__=='__main__':main()
