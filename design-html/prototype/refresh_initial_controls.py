"""Sequential source-bound initial-control replays, with actual execution provenance."""
import sys,json,hashlib,shutil,subprocess
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';FILES=source();META=OUT/'initial-controls-refresh-source.json'
groups=[('time','verify_time_controls.py',['--controls'],'time-controls-results.json',54),('workshop','verify_workshop_controls.py',[],'workshop-controls-results.json',92),('settings','verify_settings_controls.py',[],'settings-controls-results.json',81),('pet','verify_pet_controls.py',[],'pet-controls-results.json',151),('book','verify_book_controls.py',[],'book-controls-results.json',154)]
history=ROOT/'evidence/history/pre-initial-refresh-5b71c64';history.mkdir(parents=True,exist_ok=True)
previous=json.loads(META.read_text(encoding='utf-8'))if '--resume'in sys.argv and META.exists()else{};reports={}
def save():META.write_text(json.dumps(dict(files=FILES,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for group,script,args,name,count in groups:
 assert source()==FILES;path=OUT/name
 if path.exists()and not(history/name).exists():shutil.copy2(path,history/name)
 old=previous.get('reports',{}).get(name,{})
 if path.exists()and previous.get('files')==FILES and old.get('exit_code')==0 and old.get('passed')==old.get('cases')==count and not old.get('errors')and old.get('sha256')==hashlib.sha256(path.read_bytes()).hexdigest():
  value=json.loads(path.read_text(encoding='utf-8'));assert value['files']==FILES and all(r['passed']and not r['errors']for r in value['results']);reports[name]={**old,'retained_execution':True};save();print('RETAINED '+group,flush=True);continue
 print('START '+group,flush=True);run=subprocess.run([sys.executable,str(ROOT/script),*args]);assert source()==FILES
 report=dict(exit_code=run.returncode,expected_cases=count,source_current=False)
 if path.exists():
  value=json.loads(path.read_text(encoding='utf-8'));rows=value.get('results',[])if isinstance(value,dict)else value;report.update(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source_current=isinstance(value,dict)and value.get('files')==FILES,cases=len(rows),passed=sum(bool(r.get('passed'))for r in rows),errors=sum(len(r.get('errors',[]))for r in rows))
 reports[name]=report;save();print('REPORT '+group+' '+str(report.get('passed',0))+'/'+str(report.get('cases',0))+' exit='+str(run.returncode),flush=True)
assert source()==FILES
raise SystemExit(0 if all(r['exit_code']==0 and r['source_current']and r.get('cases')==r.get('passed')==r['expected_cases']and not r['errors']for r in reports.values())else 1)
