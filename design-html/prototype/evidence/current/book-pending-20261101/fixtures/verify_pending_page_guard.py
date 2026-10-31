"""Actual top-level editor exits while the existing busy delay is pending."""
import argparse,hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import MODULES,declarations
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_pending_form_cancel import HOLD
from verify_overlay_form_saves import storage

TEXT='取消等待中的页面编辑'
CASES={
 'diary-publish':dict(group='record',page='m03-p05',submit='#diary .submit',key='dujia-prototype-records',predicate='d.filter(v=>v.title===text&&v.status==="published").length===1'),
 'diary-draft':dict(group='record',page='m03-p05',submit='#top-save',key='dujia-prototype-records',predicate='d.filter(v=>v.title===text&&v.status==="draft").length===1'),
 'book-theme':dict(group='book',page='m08-p05',submit='.next',key='dujia-prototype-books',predicate='d.find(v=>v.id==="book-state").theme===expected')}


CASES.update({
 'diary-reply':dict(group='record',page='m03-p08',submit='#message [type=submit]',fields={'#reply':TEXT},key='dujia-prototype-records',predicate='d.find(v=>v.id==="audit-diary").comments.filter(v=>v.text===text).length===1',stays=True),
 'photo-reply':dict(group='record',page='m03-p12',submit='#message [type=submit]',fields={'#reply':TEXT},key='dujia-prototype-records',predicate='d.find(v=>v.id==="audit-photo").comments.filter(v=>v.text===text).length===1',stays=True),
 'photo-edit':dict(group='record',page='m03-p11',seed_page='m03-p12',editor='m03-p11.html?id=audit-photo',submit='#photo-form .submit',fields={'[name=caption]':TEXT},key='dujia-prototype-records',predicate='d.find(v=>v.id==="audit-photo").caption===text'),
 'photo-top':dict(group='record',page='m03-p11',seed_page='m03-p12',editor='m03-p11.html?id=audit-photo',submit='#done',fields={'[name=caption]':TEXT},key='dujia-prototype-records',predicate='d.find(v=>v.id==="audit-photo").caption===text'),
 'moment':dict(group='moment',page='m04-p04',submit='#moment-form .submit',fields={'[name=name]':TEXT,'[name=story]':'保留时刻输入'},key='dujia-prototype-moments',predicate='d.filter(v=>v.name===text).length===1'),
 'anniversary':dict(group='time',page='m04-p09',submit='#anniversary-form .submit',fields={'[name=name]':TEXT},key='dujia-prototype-anniversaries',predicate='d.filter(v=>v.name===text).length===1'),
 'capsule-draft':dict(group='time',page='m04-p13',submit='#draft',fields={'[name=name]':TEXT,'[name=message]':'尚未封存的信件'},key='dujia-prototype-capsules',predicate='d.filter(v=>v.name===text&&v.status==="draft").length===1'),
 'work-draft':dict(group='workshop',page='m05-p03',submit='.prototype-work-draft',fields={'#story':TEXT},key='dujia-prototype-works',predicate='d.find(v=>v.id==="work-free").story===text'),
 'profile':dict(group='settings',page='m06-p02',submit='#save',fields={'#nickname':TEXT},key='dujia-profile',predicate='d.nickname===text'),
 'pet-adopt':dict(group='pet',page='m07-p02',submit='#invite',exit_selector='.pet-back',fields={'#pet-name':TEXT},key='dujia-prototype-pet',predicate='d&&d.name===text&&d.status==="pending"')})

def prepare(p,name):
 if name in ['diary-publish','diary-draft']:
  p.locator('[name=title]').fill(TEXT);p.locator('[name=body]').fill('输入必须原样保留，放弃不能保存。');return None
 if name=='book-theme':
  button=p.locator('.themes button[aria-pressed=false]').first;expected=button.get_attribute('data-theme');button.click();return expected
 if 'fields' in CASES[name]:
  for selector,value in CASES[name]['fields'].items():p.locator(selector).fill(value)
  return None
 raise AssertionError(name)

def capture(p):return p.locator('.screen').evaluate('e=>JSON.stringify([...e.querySelectorAll("input,textarea,select,[aria-pressed]")].map(v=>[v.id,v.name,v.value,v.checked,v.getAttribute("aria-pressed")]))')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');parser.add_argument('--cases');parser.add_argument('--modes',default='keep,discard');parser.add_argument('--exits',default='button,back');args=parser.parse_args();names=args.cases.split(',') if args.cases else list(CASES)
 out=ROOT/('evidence/baseline/pending-page-guard' if args.baseline else 'evidence/current/pending-page-guard');out.mkdir(parents=True,exist_ok=True);files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')};fixtures={k:declarations(v) for k,v in MODULES.items()};rows=[]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for name in names:
   for method in args.exits.split(','):
    for mode in args.modes.split(','):
     c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));case=CASES[name];row=dict(case=name,page=case['page'],exit=method,mode=mode)
     try:
      fixtures[case['group']]['seed'](p,case.get('seed_page',case['page']))
      if 'editor' in case:p.goto(BASE+'pages/'+case['editor'])
      expected=prepare(p,name);candidate=capture(p);before=storage(p);url=p.url;p.evaluate(HOLD);submit=p.locator(case['submit']);submit.click();expect(submit).to_have_attribute('aria-busy','true');assert p.evaluate('!!window.__pendingRelease')
      if method=='back':p.go_back()
      else:p.locator(case.get('exit_selector','.back')).first.click()
      dialog=p.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text('是否放弃当前修改？');p.evaluate('window.__pendingRelease()');p.wait_for_function('()=>new Promise(resolve=>setTimeout(resolve,70))')
      row['storage_unchanged_before_decision']=storage(p)==before;row['after_release_url']=p.url;assert row['storage_unchanged_before_decision'],'Pending operation wrote before keep/discard decision'
      expect(submit).to_be_enabled();expect(submit).not_to_have_attribute('aria-busy','true');expect(dialog).to_have_count(1)
      dialog.get_by_role('button',name='继续编辑' if mode=='keep' else '放弃修改',exact=True).click();expect(dialog).to_have_count(0)
      if mode=='discard':
       p.wait_for_function('url=>location.href!==url',arg=url);assert storage(p)==before;p.reload();assert storage(p)==before;row['discard_reload_consistent']=True
      else:
       assert p.url==url and capture(p)==candidate and storage(p)==before;p.wait_for_function('history.state?.prototypeGuard===true');submit.click()
       p.wait_for_function('arg=>{const d=JSON.parse(localStorage.getItem(arg.key)),text=arg.text,expected=arg.expected;return '+case['predicate']+'}',arg=dict(key=case['key'],text=TEXT,expected=expected))
       # Resolve any successful navigation before closing this private context.
       if not case.get('stays'):
        p.wait_for_function('url=>location.href!==url',arg=url);p.wait_for_load_state('domcontentloaded')
       else:expect(p.locator('#reply')).to_have_value('')
       saved=storage(p);p.reload();assert storage(p)==saved;row['retry_saved_once_and_reload_consistent']=True
      assert not errors,errors;row['passed']=True
     except Exception:row.update(passed=False,failure=traceback.format_exc()[-2100:])
     row['errors']=errors;rows.append(row);c.close();assert source()==files
     report=dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,timer_instrumentation='Only the existing 550ms UI.busy delay is held; actual operations, navigation and storage are unchanged',accepted_pages=0)
     (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+name+' '+method+' '+mode,flush=True)
  b.close()
 print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
