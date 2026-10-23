"""Run the affected workshop contracts and existing flows sequentially, binding source and exits."""
import hashlib,json,subprocess,sys
from pathlib import Path
from verify_pet_controls import ROOT,DEMO,source

def main():
 files=source();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')};out=ROOT/'evidence/current/work-album-decode';rows=[]
 for script,report,count in [('verify_workshop_controls.py','workshop-controls-results.json',92),('verify_workshop_flow.py','workshop-flow-results.json',3),('verify_workshop_states.py','workshop-state-results.json',8)]:
  before=h(ROOT/script);print('RUN '+script,flush=True);run=subprocess.run([sys.executable,str(ROOT/script)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8');path=ROOT/'evidence/current'/report
  v=json.loads(path.read_text(encoding='utf-8'));results=v['results'] if isinstance(v,dict) else v
  assert source()==files and h(ROOT/script)==before
  if isinstance(v,dict):assert v['files']==files
  row=dict(script=script,script_sha256=before,report=path.relative_to(ROOT).as_posix(),report_sha256=h(path),exit_code=run.returncode,cases=len(results),passed=sum(r['passed'] for r in results),errors=sum(len(r['errors']) for r in results));rows.append(row)
  (out/'regressions.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=h(Path(__file__)),results=rows,accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print(json.dumps(row),flush=True)
  if run.returncode or len(results)!=count or row['passed']!=count or row['errors']:print(run.stdout[-5000:],flush=True);raise SystemExit(1)
 print('103 workshop regression cases passed',flush=True)

if __name__=='__main__':main()
