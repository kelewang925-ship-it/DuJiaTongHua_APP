"""Replay existing V2 contracts separately; preserve its prior evidence and sources."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,importlib.util

ROOT=Path(__file__).resolve().parent
DEMO=ROOT.parent
OUT=ROOT/'evidence/current/book-v2-reconciliation'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dependencies():
    files=set()
    for n in range(1,22):
        for folder in ['custom','pages']:
            p=DEMO/f'{folder}/m08-p{n:02d}.html';files.add(p)
            for relative in re.findall(r'(?:src|href)="([^"]+)"',p.read_text(encoding='utf-8')):
                if relative.startswith('../assets/'):files.add((p.parent/relative).resolve())
    files.update((DEMO/'assets/book-v2').glob('*'))
    # Include font/texture dependencies referenced by CSS rather than HTML.
    for p in list(files):
        if p.suffix=='.css':
            for relative in re.findall(r'url\([\'"]?([^\)\'" ]+)',p.read_text(encoding='utf-8')):
                if not relative.startswith(('data:','http')):files.add((p.parent/relative).resolve())
    return {p.relative_to(DEMO).as_posix():sha(p) for p in sorted(files) if p.is_file()}

def main():
    OUT.mkdir(parents=True,exist_ok=True);before=dependencies()
    prior_path=ROOT/'evidence/current/book-v2/verification-summary.json'
    prior=json.loads(prior_path.read_text(encoding='utf-8'))
    prior_changes=[p for p,h in prior['hashes'].items() if not (DEMO/p).is_file() or sha(DEMO/p)!=h]
    spec=importlib.util.spec_from_file_location('book_v2_existing_contracts',ROOT/'verify_book_v2.py')
    suite=importlib.util.module_from_spec(spec);spec.loader.exec_module(suite)
    suite.OUT=OUT
    result=suite.main()
    rows=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
    assert len(rows)==11 and dependencies()==before
    (OUT/'provenance.json').write_text(json.dumps(dict(verified_at=datetime.now(timezone.utc).isoformat(),passed=result==0,scope='Fresh replay of 11 existing V2 browser contracts only; does not certify full 114-page goal or human visual acceptance.',dependency_files=before,prior_summary_sha256=sha(prior_path),prior_summary_changed_sources=prior_changes,producer_sha256=sha(Path(__file__)),suite_sha256=sha(ROOT/'verify_book_v2.py'),helpers_sha256=sha(ROOT/'book_test_helpers.py'),cases=len(rows),human_accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Fresh book V2 contracts:',sum(r['passed'] for r in rows),'/',len(rows),'prior source mismatches:',len(prior_changes))
    return result

if __name__=='__main__':raise SystemExit(main())
