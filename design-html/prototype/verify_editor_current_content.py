"""Rendered edit/read-marker competition paths; isolated local browser context."""
import argparse,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source

parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');args=parser.parse_args()
OUT=ROOT/'evidence'/('baseline'if args.baseline else'current');OUT.mkdir(parents=True,exist_ok=True);files=source();rows=[]
REC='dujia-prototype-records';MOM='dujia-prototype-moments'
CONFIG={'diary':(REC,'audit-diary','m03-p05','body','m03-p08'),'photo':(REC,'audit-photo','m03-p11','caption','m03-p12'),'moment':(MOM,'audit-moment','m04-p04','story','m04-p03')}

def seed(p,kind,read=False):
 key,id,page,field,detail=CONFIG[kind];d=data(True);d['dujia-prototype-session']={'loggedIn':True};d['dujia-prototype-preferences']={'autoBackup':False,'reduceMotion':True};d['dujia-prototype-books']=[];d['dujia-prototype-pet']=None
 for r in d[key]:
  if r['id']==id:r['comments']=[dict(id='first',author='阿舟',text='原来的留言',createdAt=1,read=False)]
 p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d)
 p.goto(BASE+'pages/'+('m04-p16.html'if read else page+'.html?id='+id));return key,id,field,detail

def change(p,key,id,mode):
 # Same-origin producer without a storage event in this tab, as during a pending callback.
 return p.evaluate('([key,id,mode])=>{let a=JSON.parse(localStorage.getItem(key));let v=a.find(v=>v.id===id);if(mode==="delete")a=a.filter(v=>v.id!==id);else if(mode==="private"){v.visibility="private";v.author="阿舟";}else if(mode==="comment"){v.comments.push({id:"new",author:"阿舟",text:"另一处新增的留言",createdAt:2,read:false});v.updatedAt=Date.now();}else {v.body="另一处的新正文";v.caption="另一处的新正文";v.story="另一处的新正文";v.title="另一处的新标题";v.name="另一处的新名称";v.comments.push({id:"new",author:"阿舟",text:"另一处新增的留言",createdAt:2,read:false});}localStorage.setItem(key,JSON.stringify(a));return localStorage.getItem(key)}',[key,id,mode])

def editor(p,kind,mode):
 key,id,field,detail=seed(p,kind);input=p.locator('[name='+field+']');input.fill('当前未保存的输入');p.locator('.submit').click();raw=change(p,key,id,mode)
 if mode=='comment':
  p.wait_for_url('**/'+detail+'.html?id='+id);entry=p.evaluate('([key,id])=>JSON.parse(localStorage.getItem(key)).find(v=>v.id===id)',[key,id]);assert len(entry['comments'])==2 and entry['comments'][1]['text']=='另一处新增的留言';assert entry[field]=='当前未保存的输入'
 else:
  expect(p.locator('.prototype-toast')).to_contain_text('已删除'if mode=='delete'else'已在另一处更新');assert p.evaluate('(key)=>localStorage.getItem(key)',key)==raw;expect(input).to_have_value('当前未保存的输入');expect(p.locator('.submit')).to_be_enabled();p.locator('.back').click();expect(p.get_by_role('dialog')).to_contain_text('是否放弃当前修改');p.get_by_role('button',name='继续编辑',exact=True).click();expect(input).to_have_value('当前未保存的输入')

def read_marker(p,kind,mode):
 key,id,field,detail=seed(p,kind,True);button=p.locator('.prototype-reply-cards article').filter(has_text='原来的留言').get_by_role('button');raw=change(p,key,id,mode);button.click()
 if mode in ['delete','private']:
  expect(p.locator('.prototype-toast')).to_contain_text('不再共同可见');assert p.evaluate('(key)=>localStorage.getItem(key)',key)==raw;assert 'm04-p16.html'in p.url
 else:
  p.wait_for_url('**/'+detail+'.html?id='+id);entry=p.evaluate('([key,id])=>JSON.parse(localStorage.getItem(key)).find(v=>v.id===id)',[key,id]);assert entry[field]=='另一处的新正文';assert len(entry['comments'])==2;assert entry['comments'][0]['read']is True and entry['comments'][1]['read']is False

def unrelated(p,kind):
 key,id,field,detail=seed(p,kind);p.locator('[name='+field+']').fill('无关更新后的输入');p.locator('.submit').click();p.evaluate('([key,id])=>{const a=JSON.parse(localStorage.getItem(key));a.push({...a.find(v=>v.id===id),id:"unrelated",title:"独立内容",name:"独立内容",comments:[]});localStorage.setItem(key,JSON.stringify(a))}',[key,id]);p.wait_for_url('**/'+detail+'.html?id='+id);values=p.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',key);assert any(v['id']=='unrelated'for v in values);assert next(v for v in values if v['id']==id)[field]=='无关更新后的输入'

def retry(p,kind):
 key,id,field,detail=seed(p,kind);p.locator('[name='+field+']').fill('失败后保留输入');p.evaluate('(kind)=>sessionStorage.setItem("dujia-prototype-fail-next",kind+"-save")',kind);before=p.evaluate('(key)=>localStorage.getItem(key)',key);p.locator('.submit').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.evaluate('(key)=>localStorage.getItem(key)',key)==before;expect(p.locator('[name='+field+']')).to_have_value('失败后保留输入');expect(p.locator('.submit')).to_be_enabled();change(p,key,id,'comment');p.locator('.submit').click();p.wait_for_url('**/'+detail+'.html?id='+id);entry=p.evaluate('([key,id])=>JSON.parse(localStorage.getItem(key)).find(v=>v.id===id)',[key,id]);assert entry[field]=='失败后保留输入'and len(entry['comments'])==2

def missing_reply(p,kind):
 key,id,field,detail=seed(p,kind,True);button=p.locator('.prototype-reply-cards article').filter(has_text='原来的留言').get_by_role('button');raw=p.evaluate('([key,id])=>{const a=JSON.parse(localStorage.getItem(key));a.find(v=>v.id===id).comments=[];localStorage.setItem(key,JSON.stringify(a));return localStorage.getItem(key)}',[key,id]);button.click();expect(p.locator('.prototype-toast')).to_contain_text('这条留言已不存在');assert p.evaluate('(key)=>localStorage.getItem(key)',key)==raw

jobs={**{f'{kind}-editor-{mode}':lambda p,k=kind,m=mode:editor(p,k,m)for kind in CONFIG for mode in ['content','delete','comment']},**{f'{kind}-read-current-{mode}':lambda p,k=kind,m=mode:read_marker(p,k,m)for kind in ['diary','moment']for mode in ['content','delete','private']}}
if not args.baseline:jobs.update({**{kind+'-unrelated-change':lambda p,k=kind:unrelated(p,k)for kind in CONFIG},**{kind+'-failure-comment-retry':lambda p,k=kind:retry(p,k)for kind in CONFIG},**{kind+'-read-missing-reply':lambda p,k=kind:missing_reply(p,k)for kind in ['diary','moment']}})
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in jobs.items():
  c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);p.set_default_navigation_timeout(15000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-2000:])
  row.update(case=name,errors=errors);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert source()==files;(OUT/'editor-current-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
