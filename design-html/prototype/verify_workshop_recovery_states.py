"""Work recovery: writes, quota/races, dirty inputs, archive UI and every state page."""
import json,traceback,time
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from verify_workshop_recovery import seed,raw,archives,prompt,repair,KEY
from verify_pet_controls import ROOT,BASE,source,store
from audit_current_runtime import data
OUT=ROOT/'evidence/current';files=source();rows=[];W=data(True)[KEY][0];MIX=json.dumps([W,None],ensure_ascii=False)
def recover(p):
 with p.expect_event('load'):repair(p)
 expect(p.locator('dialog')).to_have_count(0)
def quota(p,replace=False):
 seed(p,MIX);prompt(p);p.evaluate('([key,replace])=>{window.oldSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(replace?k===key:k.startsWith("dujia-prototype-work-recovery-"))throw new DOMException("full","QuotaExceededError");return oldSet.call(this,k,v);}}',[KEY,replace]);repair(p);expect(p.locator('.prototype-toast')).to_contain_text('未能保存');assert raw(p)==MIX and archives(p)==([MIX]if replace else[]);p.evaluate('()=>{Storage.prototype.setItem=oldSet;}');p.get_by_role('button',name='恢复作品',exact=True).click();recover(p);assert json.loads(raw(p))==[W];assert all(v==MIX for v in archives(p))
def race(p,backup=False):
 seed(p,MIX);prompt(p);fresh=json.dumps([{**W,'name':'另一处已更新'}],ensure_ascii=False)
 if backup:p.evaluate('([key,fresh])=>{window.oldSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){const result=oldSet.call(this,k,v);if(k.startsWith("dujia-prototype-work-recovery-"))oldSet.call(this,key,fresh);return result;}}',[KEY,fresh])
 else:
  p.get_by_role('button',name='恢复可读作品',exact=True).click();p.evaluate('([k,v])=>localStorage.setItem(k,v)',[KEY,fresh]);p.get_by_role('button',name='确认恢复',exact=True).click()
 if backup:repair(p)
 expect(p.locator('.prototype-toast')).to_contain_text('更新');assert raw(p)==fresh and archives(p)==([MIX]if backup else[])
def dirty(p):
 seed(p,json.dumps([{**W,'status':'draft'}],ensure_ascii=False),'m05-p03.html?id=audit-work');p.locator('#story').fill('当前尚未保存的长故事');p.evaluate('([k,v])=>localStorage.setItem(k,v)',[KEY,MIX]);p.get_by_role('button',name='暂存创作草稿',exact=True).click();prompt(p);assert raw(p)==MIX;repair(p);expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('#story')).to_have_value('当前尚未保存的长故事');p.get_by_role('button',name='暂存创作草稿',exact=True).click();p.wait_for_url('**/m05-p09.html');assert json.loads(raw(p))[0]['story']=='当前尚未保存的长故事'
def retry(p):
 seed(p,'{broken');prompt(p);p.evaluate('([k,v])=>localStorage.setItem(k,v)',[KEY,json.dumps([W],ensure_ascii=False)])
 with p.expect_event('load'):p.get_by_role('button',name='重新检查',exact=True).click()
 assert not archives(p);expect(p.locator('.prototype-work-list')).to_contain_text(W['name'])
def invalid(p,change):
 value={**W,**change};seed(p,json.dumps([value],ensure_ascii=False));prompt(p);recover(p);value=json.loads(raw(p))[0];assert value['id']==W['id']and value['name']==W['name']and value['story']==W['story'];assert value['status']=='draft'if change.get('status')=='generating'else value['characters']=={'appearance':'保留外貌'}
def history(p):
 seed(p,'{工坊私人原文');prompt(p);recover(p);p.goto(BASE+'pages/m06-p11.html');p.locator('.manage').click();p.get_by_role('button',name='查看恢复原始副本',exact=True).click();p.get_by_role('button',name='原始副本 1',exact=True).click();expect(p.locator('dialog')).to_contain_text('工坊作品完整原始内容')
 with p.expect_download()as download:p.get_by_role('button',name='下载原始副本',exact=True).click()
 assert Path(download.value.path()).read_text(encoding='utf-8')=='{工坊私人原文';assert raw(p)=='[]'
def unavailable(p):
 seed(p,'[]');p.evaluate('()=>{window.oldGet=Storage.prototype.getItem;Storage.prototype.getItem=function(k){if(k==="dujia-prototype-works")throw new Error("blocked");return oldGet.call(this,k);};PrototypeUI.recoverWorks();}');prompt(p);expect(p.get_by_role('button',name='恢复可读作品',exact=True)).to_be_disabled();expect(p.get_by_role('button',name='导出原始作品',exact=True)).to_be_disabled();p.get_by_role('button',name='稍后处理',exact=True).click();p.evaluate('()=>{Storage.prototype.getItem=oldGet;}');assert raw(p)=='[]'
def healthy(p):
 original=json.dumps([W],ensure_ascii=False);seed(p,original);expect(p.locator('dialog')).to_have_count(0);assert raw(p)==original;assert not archives(p);assert p.evaluate('PrototypeUI.workHealth().issues.length')==0

def state_page(p,n):
 work={**W};query='?id=audit-work'
 if n in [3,4,5]:work['status']='draft'
 if n==4:work.update(sourceKind='photo')
 if n==5:work.update(type='film')
 if n==6:work.update(status='generating',startedAt=int(time.time()*1000),dueAt=int(time.time()*1000)+30000)
 if n==7:work.update(status='failed')
 if n==10:query='?work=audit-work'
 if n==2:query=''
 original=json.dumps([work,None],ensure_ascii=False);seed(p,original,f'm05-p{n:02}.html'+query);prompt(p);assert f'm05-p{n:02}.html'in p.url;recover(p);assert json.loads(raw(p))==[work]
def combined(p):
 seed(p,MIX);prompt(p);p.get_by_role('button',name='稍后处理',exact=True).click();p.evaluate('()=>{localStorage.setItem("dujia-profile","null");localStorage.setItem("dujia-prototype-records","{broken");}');p.reload();expect(p.get_by_role('dialog',name='资料需要恢复',exact=True)).to_be_visible();p.get_by_role('button',name='恢复可读资料',exact=True).click()
 with p.expect_event('load'):p.get_by_role('button',name='确认恢复',exact=True).click()
 expect(p.get_by_role('dialog',name='记录需要恢复',exact=True)).to_be_visible();assert raw(p)==MIX;p.get_by_role('button',name='恢复可读记录',exact=True).click()
 with p.expect_event('load'):p.get_by_role('button',name='确认恢复',exact=True).click()
 prompt(p);recover(p);assert json.loads(raw(p))==[W];assert p.evaluate('localStorage.getItem("dujia-prototype-records")')=='[]'
def layout(p,width):
 seed(p,MIX);prompt(p);p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0);p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")');button=p.get_by_role('button',name='恢复作品',exact=True);button.scroll_into_view_if_needed();r=button.bounding_box();assert r['x']>=0 and r['x']+r['width']<=width+.5 and r['height']>=44;assert button.evaluate('b=>{const r=b.getBoundingClientRect(),e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return e===b||b.contains(e);}');button.focus();p.keyboard.press('Enter');prompt(p);cancel=p.get_by_role('button',name='稍后处理',exact=True);expect(cancel).to_be_focused();p.wait_for_function('!document.querySelector("[aria-busy=true]")');p.evaluate('document.fonts.ready');p.screenshot(path=str(OUT/f'workshop-recovery-{width}.png'));p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);assert raw(p)==MIX and not archives(p)
jobs=[('combined-recovery-order',combined),('archive-quota',lambda p:quota(p)),('replacement-quota',lambda p:quota(p,True)),('before-archive-race',lambda p:race(p)),('during-archive-race',lambda p:race(p,True)),('dirty-editor',dirty),('external-repair-recheck',retry),('archive-history-download',history),('storage-unavailable',unavailable),('healthy-unchanged',healthy),('nested-characters',lambda p:invalid(p,dict(characters={'appearance':'保留外貌','outfit':{}}))),('invalid-generation-time',lambda p:invalid(p,dict(status='generating',startedAt=3,dueAt='broken'))),('inverted-generation-time',lambda p:invalid(p,dict(status='generating',startedAt=3,dueAt=2))),('invalid-generation-result-flag',lambda p:invalid(p,dict(status='generating',startedAt=3,dueAt=4,willFail={})))]+[(f'state-page-{n}',lambda p,n=n:state_page(p,n))for n in [2,3,4,5,6,7,10]]+[(f'layout-{w}',lambda p,w=w:layout(p,w))for w in [320,360,390,414,430]]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in jobs:
  width=int(name[7:])if name.startswith('layout-')else 390;c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-2200:])
  row.update(case=name,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert files==source();(OUT/'workshop-recovery-state-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
