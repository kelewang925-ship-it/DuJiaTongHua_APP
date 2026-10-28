"""Publish a scoped checkpoint only when all required current browser suites pass."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import hashlib,json,re,subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'prototype/evidence/current/book-v2'
SUITES={'results.json':11,'integration-results.json':7,'layout-results.json':106,
        'regressions/book-flow-results.json':4,'regressions/book-state-results.json':6,
        'regressions/book-structure-results.json':5,'regressions/book-editor-draft-results.json':7,
        'regressions/book-extended-results.json':7,'regressions/book-global-results.json':6}
summary=[]
for name,total in SUITES.items():
    rows=json.loads((OUT/name).read_text(encoding='utf-8'))
    assert len(rows)==total,(name,len(rows),total)
    assert all(row.get('passed') for row in rows),(name,[r for r in rows if not r.get('passed')])
    summary.append({'suite':name,'passed':len(rows),'total':total})
files=set()
for n in range(1,22):
    source=ROOT/'custom'/f'm08-p{n:02}.html';page=ROOT/'pages'/source.name
    assert source.read_bytes()==page.read_bytes(),source
    files.update([source,page])
    for relative in re.findall(r'(?:src|href)="([^"]+)"',source.read_text(encoding='utf-8')):
        if relative.startswith('../assets/'):
            dependency=(source.parent/relative).resolve();assert dependency.is_file(),dependency;files.add(dependency)
files.update((ROOT/'assets/book-v2').glob('*.webp'))
node=r'C:\Users\kele\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
js=['prototype-book','prototype-book-store','prototype-book-structure','prototype-book-v2','prototype-book-reader']
for name in js:subprocess.run([node,'--check',str(ROOT/'assets'/(name+'.js'))],check=True)
paths=[str(p.relative_to(ROOT.parent)) for p in files if p.suffix in ['.html','.js','.css']]
subprocess.run(['git','diff','--check','--',*paths],cwd=ROOT.parent,check=True)
current_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
existing_summary=OUT/'verification-summary.json'
if existing_summary.exists():
    existing=json.loads(existing_summary.read_text(encoding='utf-8'))
    assert existing['hashes']==current_hashes, ('The saved159-case summary belongs to different source bytes. Preserve it; use verify_book_v2_delta_checkpoint.py for current scoped evidence. Do not bind old suite results to new sources.')
report={'passed':True,'verified_at':datetime.now(timezone(timedelta(hours=8))).isoformat(),
        'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT.parent,text=True).strip(),
        'browser_cases':sum(r['total'] for r in summary),'suites':summary,'route_pairs':21,'javascript_syntax_files':len(js),
        'scope':'HTML memory-book V2; Chrome mobile simulation and CDP touch; no real-device performance claim',
        'hashes':current_hashes}
(OUT/'verification-summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"PASS {report['browser_cases']} browser cases; 21 route pairs; five JS syntax checks; scoped diff and asset checks")
