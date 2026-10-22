"""Actual editable tasks: pending input, picker intent, and competing save/generate actions."""
import argparse,hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import MODULES,declarations
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_pending_page_guard import CASES,prepare,TEXT,capture
from verify_overlay_form_saves import storage

NEW='继续输入的新内容'
HOLD="""()=>{const timer=window.setTimeout;window.__submissionTimers=[];window.__releaseSubmissionTimers=()=>{const tasks=window.__submissionTimers.splice(0);for(const task of tasks)timer(task,0)};window.setTimeout=function(fn,delay,...args){if(delay===550){window.__submissionTimers.push(()=>fn(...args));return -550;}return timer(fn,delay,...args)}}"""
EDIT={
 'diary-publish':('[name=body]','d.filter(v=>v.title===original&&v.status==="published"&&v.body===text).length===1'),
 'diary-draft':('[name=body]','d.filter(v=>v.title===original&&v.status==="draft"&&v.body===text).length===1'),
 'diary-reply':('#reply',None),'photo-reply':('#reply',None),'photo-edit':('[name=caption]',None),'photo-top':('[name=caption]',None),
 'moment':('[name=story]','d.filter(v=>v.name===original&&v.story===text).length===1'),
 'anniversary':('[name=name]',None),'capsule-draft':('[name=message]','d.filter(v=>v.name===original&&v.message===text&&v.status==="draft").length===1'),
 'work-draft':('#story',None),'profile':('#nickname',None),'pet-adopt':('#pet-name',None),'book-theme':(None,None)}

def seed(p,fixtures,name):
 case=CASES[name];fixtures[case['group']]['seed'](p,case.get('seed_page',case['page']))
 if 'editor' in case:p.goto(BASE+'pages/'+case['editor'])
 return prepare(p,name)

def settled(p,url):p.wait_for_function('url=>location.href!==url||!document.querySelector("[aria-busy=true]")',arg=url)

def retry(p,name,expected,predicate,text=NEW):
 case=CASES[name];url=p.url;p.locator(case['submit']).click();p.evaluate('window.__releaseSubmissionTimers()')
 p.wait_for_function('arg=>{const d=JSON.parse(localStorage.getItem(arg.key)),text=arg.text,original=arg.original,expected=arg.expected;return '+predicate+'}',arg=dict(key=case['key'],text=text,original=TEXT,expected=expected))
 if not case.get('stays'):p.wait_for_function('url=>location.href!==url',arg=url);p.wait_for_load_state('domcontentloaded')
 else:expect(p.locator('#reply')).to_have_value('')
 saved=storage(p);p.reload();assert storage(p)==saved

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');parser.add_argument('--only');args=parser.parse_args();selected=args.only.split(',') if args.only else None
 out=ROOT/('evidence/baseline/submission-changes' if args.baseline else 'evidence/current/submission-changes');out.mkdir(parents=True,exist_ok=True);files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')};fixtures={k:declarations(v) for k,v in MODULES.items()};rows=[]
 cases=[('edit',name,None) for name in EDIT]+[('picker',m,None) for m in ['apply','cancel']]+[('concurrent',first,mode) for first in ['draft','generate'] for mode in ['finish','cancel']]
 if selected:cases=[v for v in cases if '/'.join(str(x) for x in v if x is not None) in selected]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for kind,name,mode in cases:
   c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(kind=kind,case=name,mode=mode)
   try:
    task=name if kind=='edit' else 'photo-top' if kind=='picker' else 'work-draft';expected=seed(p,fixtures,task);case=CASES[task];before=storage(p);url=p.url;p.evaluate(HOLD)
    if kind=='edit':
     submit=p.locator(case['submit']);submit.click();expect(submit).to_have_attribute('aria-busy','true');selector,predicate=EDIT[name]
     if selector:p.locator(selector).fill(NEW)
     else:
      button=p.locator('.themes button[aria-pressed=false]').first;expected=button.get_attribute('data-theme');button.click()
     candidate=capture(p);p.evaluate('window.__releaseSubmissionTimers()');settled(p,url);row['unchanged_before_retry']=storage(p)==before;assert row['unchanged_before_retry'],'Pending submission wrote after input changed';assert p.url==url and capture(p)==candidate;expect(submit).to_be_enabled();expect(p.locator('.prototype-toast')).to_have_text('内容已更新，请重新提交')
     retry(p,name,expected,predicate or case['predicate']);row['latest_input_saved_once']=True
    elif kind=='picker':
     submit=p.locator(case['submit']);submit.click();p.locator('[name=date]').click();dialog=p.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text('选择照片日期');dialog.locator('input[type=date]').fill('2026-10-03');p.evaluate('window.__releaseSubmissionTimers()');settled(p,url);row['unchanged_with_picker_open']=storage(p)==before;assert row['unchanged_with_picker_open'],'Pending save wrote while picker still open';assert p.url==url;expect(dialog).to_have_count(1)
     dialog.get_by_role('button',name='使用这个日期' if name=='apply' else '取消',exact=True).click();expect(dialog).to_have_count(0);expect(p.locator('[name=caption]')).to_have_value(TEXT)
     if name=='apply':expect(p.locator('[name=date]')).to_have_value('2026-10-03')
     predicate='d.find(v=>v.id==="audit-photo").caption===text'+('&&d.find(v=>v.id==="audit-photo").date==="2026-10-03"' if name=='apply' else '')
     retry(p,task,None,predicate,text=TEXT);row['picker_result_and_retry_saved']=True
    else:
     p.evaluate("()=>{window.__writes=0;const set=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(this===localStorage&&k==='dujia-prototype-works')window.__writes++;return set.call(this,k,v)}}")
     buttons={'draft':'.prototype-work-draft','generate':'#generate'};p.locator(buttons[name]).click();expect(p.locator(buttons[name])).to_have_attribute('aria-busy','true');p.locator(buttons['generate' if name=='draft' else 'draft']).click()
     if mode=='cancel':
      p.locator('.back').click();dialog=p.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text('是否放弃当前修改？');p.evaluate('window.__releaseSubmissionTimers()');settled(p,url);row['unchanged_before_decision']=storage(p)==before;assert row['unchanged_before_decision'],'Competing pending task escaped cancellation';dialog.get_by_role('button',name='放弃修改',exact=True).click();p.wait_for_function('url=>location.href!==url',arg=url);assert storage(p)==before;p.reload();assert storage(p)==before
     else:
      expect(p.locator('.prototype-toast')).to_have_text('当前操作还在处理中，请稍候');p.evaluate('window.__releaseSubmissionTimers()');p.wait_for_url('**/m05-p09.html*' if name=='draft' else '**/m05-p06.html*');p.wait_for_load_state('domcontentloaded')
      value=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-works")).find(v=>v.id==="work-free")');assert value['status']==('draft' if name=='draft' else 'generating'),value;row['first_intent_only']=True
    assert not errors,errors;row['passed']=True
   except Exception:row.update(passed=False,failure=traceback.format_exc()[-2300:])
   row['errors']=errors;rows.append(row);c.close();assert source()==files
   report=dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,scope='13 real pending input changes, two real photo pickers, four real competing draft/generate tasks; hold only 550ms timers, execute real business/storage/navigation',accepted_pages=0)
   (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+name+' '+str(mode),flush=True)
  b.close()
 print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
