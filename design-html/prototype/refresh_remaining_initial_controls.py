"""Sequential six-module replay after account deletion repair, with actual exits."""
import hashlib,json,shutil,subprocess,sys
from verify_pet_controls import ROOT,source

OUT=ROOT/'evidence/current'
GROUPS=[('record','verify_record_controls.py',[],109,92),('moment','verify_moment_controls.py',[],55,46),
        ('time','verify_time_controls.py',['--controls'],54,54),('workshop','verify_workshop_controls.py',[],92,92),
        ('pet','verify_pet_controls.py',[],151,151),('book','verify_book_controls.py',[],154,154)]

def main():
    files=source();history=ROOT/'evidence/history/pre-remaining-refresh-97edd42';history.mkdir(parents=True,exist_ok=True)
    for name in ['page-contracts.json','identity-deletion-checkpoint.json','current-evidence-state.json']:
        if not(history/name).exists():shutil.copy2(OUT/name,history/name)
    for name in ['PAGE_CATALOG.md','CURRENT_NAVIGATION.md','STATE_MATRIX.md','queue.json']:
        if not(history/name).exists():shutil.copy2(ROOT/name,history/name)
    meta=dict(files=files,reports={},scripts={},expected_initial=589,expected_checks=615,accepted_pages=0)
    def save():
        assert source()==files
        (OUT/'remaining-initial-refresh-source.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for group,script,args,count,initial in GROUPS:
        assert source()==files;name=group+'-controls-results.json';path=OUT/name
        if not(history/name).exists():shutil.copy2(path,history/name)
        meta['scripts'][script]=hashlib.sha256((ROOT/script).read_bytes()).hexdigest()
        print('START '+group,flush=True)
        run=subprocess.run([sys.executable,str(ROOT/script),*args]);assert source()==files
        raw=path.read_bytes();report=json.loads(raw);rows=report['results']
        value=dict(exit_code=run.returncode,sha256=hashlib.sha256(raw).hexdigest(),source_current=report['files']==files,
            expected_checks=count,expected_initial=initial,cases=len(rows),initial_cases=sum(bool(r.get('selector'))for r in rows),passed=sum(bool(r.get('passed'))for r in rows),errors=sum(len(r.get('errors',[]))for r in rows))
        meta['reports'][name]=value;save();print('FINISH '+group+' '+json.dumps(value),flush=True)
    assert source()==files
    ok=all(r['exit_code']==0 and r['source_current']and r['cases']==r['passed']==r['expected_checks']and r['initial_cases']==r['expected_initial']and not r['errors']for r in meta['reports'].values())
    print(json.dumps(dict(checks=sum(r['cases']for r in meta['reports'].values()),passed=sum(r['passed']for r in meta['reports'].values()),initial=sum(r['initial_cases']for r in meta['reports'].values()),all_passed=ok)),flush=True)
    raise SystemExit(0 if ok else 1)

if __name__=='__main__':main()
