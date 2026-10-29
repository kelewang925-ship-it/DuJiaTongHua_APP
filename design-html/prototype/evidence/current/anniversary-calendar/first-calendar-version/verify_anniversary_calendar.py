"""The decorative calendar must reflect the actual selected occurrence date."""
import argparse,calendar,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_pet_controls import ROOT,DEMO
from verify_book_v2_reconciliation import sha

DATES=[('2026-10-05','2026-10-05',False,'2026-10-05'),('2026-01-01','2026-08-31',False,'2026-08-31'),('2028-01-01','2028-02-29',False,'2028-02-29'),('2025-02-01','2024-02-29',True,'2025-02-28'),('2026-01-01','9999-12-31',False,'9999-12-31')]
def dependencies():
    html=(DEMO/'custom/m04-p07.html').read_text(encoding='utf-8');files={'custom/m04-p07.html','pages/m04-p07.html','assets/m04-p07-art.webp','assets/ui-foundation.css','assets/font.ttf'}
    files|={'assets/'+p for p in re.findall(r'(?:src|href)="\.\./assets/(prototype-[^"]+)"',html)}
    return {p:sha(DEMO/p) for p in sorted(files)}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args();out=ROOT/f'evidence/{args.stage}/anniversary-calendar';out.mkdir(parents=True,exist_ok=True)
    fixture=declarations('verify_time_controls.py');files=dependencies();cases=[('date',(w,d)) for w in [320,360,390,414,430] for d in DATES]
    if args.stage=='current':
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));controls=next(r for r in catalog['pages'] if r['id']=='m04-p07')['control_evidence'];cases += [('control',v) for v in controls]
    rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,v in cases:
            c=b.new_context(viewport=dict(width=v[0] if kind=='date' else 390,height=844),device_scale_factor=1,reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(kind=kind,value=v,passed=False)
            try:
                if kind=='date':
                    width,(today,date,repeat,wanted)=v;fixture['seed'](p,'m04-p07');p.evaluate('d=>{sessionStorage.setItem("dujia-prototype-today",d.today);const a=JSON.parse(localStorage.getItem("dujia-prototype-anniversaries"))[0];a.date=d.date;a.repeat=d.repeat;a.name="真实纪念日";localStorage.setItem("dujia-prototype-anniversaries",JSON.stringify([a]))}',dict(today=today,date=date,repeat=repeat));p.reload();expect(p.locator('.prototype-anniversary-card')).to_have_count(1);expect(p.locator('.date-pill')).to_have_text(wanted);p.evaluate('document.fonts.ready');before=p.evaluate('({...localStorage})')
                    if width==390:p.screenshot(path=str(out/(wanted+'.png')),full_page=True)
                    root=p.locator('.anniversary-calendar');assert root.count()==1,'Actual date is rendered, but the art still contains the unrelated static calendar';expect(root).to_be_visible();expect(root).to_have_attribute('data-date',wanted)
                    year,month,day=map(int,wanted.split('-'));first,days=calendar.monthrange(year,month);expect(root.locator('.calendar-month')).to_have_text(f'{year}.{month:02d}');assert root.locator('[data-day]').all_text_contents()==[str(d) for d in range(1,days+1)]
                    expect(root.locator('[data-selected="true"]')).to_have_count(1);expect(root.locator('[data-selected="true"]')).to_have_text(str(day));expect(root).to_have_attribute('aria-label',f'{year}年{month}月{day}日纪念日')
                    cells=root.locator('.calendar-grid>span');assert cells.count()==((first+days+6)//7)*7;assert cells.nth(first).inner_text()=='1'
                    assert root.locator('.calendar-grid').evaluate('e=>e.scrollHeight<=e.clientHeight+1 && e.scrollWidth<=e.clientWidth+1')
                    boxes={s:p.locator(s).bounding_box() for s in ['.hero-title','.countdown','.date-pill','.anniversary-calendar']};row['boxes']=boxes
                    assert boxes['.countdown']['y']+boxes['.countdown']['height']+2<=boxes['.date-pill']['y']
                    assert boxes['.hero-title']['x']+boxes['.hero-title']['width']+2<=boxes['.anniversary-calendar']['x']
                    assert p.evaluate('({...localStorage})')==before
                else:fixture['control'](p,'m04-p07',v,v['contract'])
                assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            row['errors']=errors;rows.append(row);c.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(v),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps(dict(dependency_files=files,producer_sha256=sha(Path(__file__)),fixture_sha256=sha(ROOT/'verify_time_controls.py'),browser=version,viewport_height=844,dpr=1,locale='zh-CN',timezone='Asia/Shanghai',scope='Calendar occurrence/month geometry and original list controls only; no full114 replay or human acceptance claim.',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Calendar cases:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
