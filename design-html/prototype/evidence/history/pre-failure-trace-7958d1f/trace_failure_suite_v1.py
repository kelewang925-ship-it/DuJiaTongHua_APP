"""Run an existing browser suite and record actual consumed failure hooks per case."""
import argparse
import hashlib
import json
import runpy
import shutil
from playwright.sync_api import Browser
from verify_pet_controls import ROOT, source

TRACE = """(() => {
 let ui;
 Object.defineProperty(window, 'PrototypeUI', {configurable:true,
  get(){return ui}, set(value){
   ui=value;
   if(typeof value?.failNext==='function'){
    const original=value.failNext;
    value.failNext=function(operation){
     const result=original.apply(this,arguments);
     if(result===true) window.__recordConsumedFailure({operation,url:location.href});
     return result;
    };
   }
  }
 });
})()"""


def main():
    p=argparse.ArgumentParser()
    p.add_argument('script');p.add_argument('report')
    args=p.parse_args()
    assert '/' not in args.script and args.script.startswith('verify_')
    out=ROOT/'evidence/current';files=source()
    history=ROOT/'evidence/history/pre-failure-trace-7958d1f'
    history.mkdir(parents=True,exist_ok=True)
    if (out/args.report).exists():
        shutil.copy2(out/args.report,history/args.report)
    events=[];contexts=[]
    original=Browser.new_context
    def new_context(browser,*a,**kw):
        context=original(browser,*a,**kw);index=len(contexts);contexts.append(context)
        context.expose_binding('__recordConsumedFailure',lambda origin,event:events.append(dict(event,context_index=index)))
        context.add_init_script(TRACE)
        return context
    Browser.new_context=new_context
    exit_code=0
    try:
        runpy.run_path(str(ROOT/args.script),run_name='__main__')
    except SystemExit as e:
        exit_code=e.code or 0
    finally:
        Browser.new_context=original
    assert source()==files
    raw=(out/args.report).read_bytes();payload=json.loads(raw)
    rows=payload['results']if isinstance(payload,dict)else payload
    assert len(contexts)==len(rows), (len(contexts),len(rows))
    for event in events:
        event['case']=rows[event['context_index']]['case']
        event['case_passed']=bool(rows[event['context_index']]['passed'])
    artifact=dict(files=files,script=args.script,script_sha256=hashlib.sha256((ROOT/args.script).read_bytes()).hexdigest(),
                  trace_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  report=args.report,report_sha256=hashlib.sha256(raw).hexdigest(),exit_code=exit_code,
                  cases=len(rows),passed=sum(r['passed']for r in rows),events=events,
                  consumed_operations=sorted({e['operation']for e in events if e['case_passed']}),
                  scope='Actual UI.failNext true returns in isolated existing case contexts. Only passing cases count. Does not prove every branch of each operation or native image decoder failures.')
    (out/(args.report.replace('-results.json','-failure-trace.json'))).write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(script=args.script,exit_code=exit_code,cases=len(rows),passed=artifact['passed'],consumed=artifact['consumed_operations']),ensure_ascii=False),flush=True)
    raise SystemExit(exit_code)


from pathlib import Path
if __name__=='__main__':main()
