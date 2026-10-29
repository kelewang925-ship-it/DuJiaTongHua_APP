"""Verify exact local calendar patch and preserve actual red/green provenance."""
import json,subprocess
from pathlib import Path
from verify_anniversary_calendar import ROOT,DEMO,dependencies
from verify_anniversary_calendar_updates import dependencies as update_dependencies
from verify_book_v2_reconciliation import sha

def load(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    baseline=ROOT/'evidence/baseline/anniversary-calendar';current=ROOT/'evidence/current/anniversary-calendar';patch=load(baseline/'patch.json')
    for folder in ['custom','pages']:
        raw=(DEMO/f'{folder}/m04-p07.html').read_bytes()
        for key in ['css','markup','script']:
            part=patch[key].encode();assert raw.count(part)==1;raw=raw.replace(part,b'',1)
        assert raw==(baseline/f'source-{folder}.html').read_bytes()
    assert (DEMO/'custom/m04-p07.html').read_bytes()==(DEMO/'pages/m04-p07.html').read_bytes()
    red=load(baseline/'results.json');green=load(current/'results.json');files=dependencies()
    assert len(red['results'])==20 and not any(r['passed'] for r in red['results'])
    assert red['producer_sha256']==sha(baseline/'verifier.py')
    assert len(green['results'])==39 and all(r['passed'] for r in green['results']) and green['dependency_files']==files
    assert green['producer_sha256']==sha(ROOT/'verify_anniversary_calendar.py') and green['fixture_sha256']==sha(ROOT/'verify_time_controls.py')
    assert set(files)-set(red['dependency_files'])=={'assets/prototype-anniversary-calendar.js'}
    assert all(files[p]==h for p,h in red['dependency_files'].items() if p not in ['custom/m04-p07.html','pages/m04-p07.html'])
    consumers=[p.stem for p in (DEMO/'custom').glob('*.html') if 'prototype-anniversary-calendar.js' in p.read_text(encoding='utf-8')];assert consumers==['m04-p07'],consumers
    update_base=ROOT/'evidence/baseline/anniversary-calendar-updates';old=load(update_base/'results.json');updates=load(ROOT/'evidence/current/anniversary-calendar-updates/results.json')
    assert len(old['results'])==5 and sum(r['passed'] for r in old['results'])==4
    assert old['producer_sha256']==sha(update_base/'verifier.py')
    assert old['dependency_files']['assets/prototype-anniversary-calendar.js']==sha(update_base/'prototype-anniversary-calendar.js')
    assert len(updates['results'])==6 and all(r['passed'] for r in updates['results']) and updates['dependency_files']==update_dependencies()
    assert updates['producer_sha256']==sha(ROOT/'verify_anniversary_calendar_updates.py') and updates['fixture_sha256']==sha(ROOT/'verify_time_controls.py')
    invalid_base=ROOT/'evidence/baseline/anniversary-calendar-invalid';invalid=load(invalid_base/'results.json')
    assert len(invalid['results'])==6 and sum(r['passed'] for r in invalid['results'])==5
    assert invalid['producer_sha256']==sha(invalid_base/'verify_anniversary_calendar_updates.py')
    assert invalid['dependency_files']['assets/prototype-anniversary-calendar.js']==sha(invalid_base/'prototype-anniversary-calendar.js')
    for folder,count,script in [('first-calendar-version',34,'verify_anniversary_calendar.py'),('lifecycle-fixed',39,'verify_anniversary_calendar.py')]:
        archive=current/folder;r=load(archive/'results.json');assert len(r['results'])==count and all(x['passed'] for x in r['results'])
        assert r['producer_sha256']==sha(archive/script) and r['dependency_files']['assets/prototype-anniversary-calendar.js']==sha(archive/'prototype-anniversary-calendar.js')
    subprocess.run([r'C:\Users\kele\.nvmd\bin\node.exe','--check',str(DEMO/'assets/prototype-anniversary-calendar.js')],check=True)
    report=dict(passed=True,scope='m04-p07 display-only calendar,39 date/geometry/original-control checks plus6 named update/recovery flows. Simulated cached lifecycle is not real-device certification.',dependency_files=files,update_dependency_files=update_dependencies(),exact_html_css_reversal=True,original_artwork_and_business_sources_preserved=True,script_consumers=consumers,browser_cases=45,human_accepted_pages=0,producer_sha256=sha(Path(__file__)))
    (current/'checkpoint.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS45 calendar cases; exact HTML/CSS reversal; original artwork/controller/date helper preserved; single-page consumer; actual archived red/green scripts verified')

if __name__=='__main__':main()
