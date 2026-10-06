"""Tag recovery quota, concurrent writes, editor protection and accessible controls."""
import json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from verify_tag_recovery import seed,raw,archives,prompt,repair,KEY,PREFIX,TAG
from verify_pet_controls import ROOT,BASE,source,store
OUT=ROOT/'evidence/current';files=source();rows=[];MIX=json.dumps([TAG,None],ensure_ascii=False)
def recover(p):
 with p.expect_event('load'):repair(p)
 expect(p.locator('dialog')).to_have_count(0)
def dismiss(p):
 p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0);p.wait_for_function('!history.state?.prototypeOverlay')
def quota(p,replace):
 seed(p,MIX);prompt(p);p.evaluate('([key,replace,prefix])=>{window.oldTagSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(replace?k===key:k.startsWith(prefix))throw new DOMException("full","QuotaExceededError");return oldTagSet.call(this,k,v);};}',[KEY,replace,PREFIX]);repair(p)
 expect(p.locator('.prototype-toast')).to_contain_text('未能保存');assert raw(p)==MIX and archives(p)==([MIX]if replace else[])
 p.evaluate('()=>{Storage.prototype.setItem=oldTagSet;}');p.get_by_role('button',name='恢复标签',exact=True).click();recover(p);assert json.loads(raw(p))==[TAG];assert all(v==MIX for v in archives(p))
def race(p,backup):
 seed(p,MIX);prompt(p);fresh=json.dumps([{**TAG,'name':'其他页面的更新'}],ensure_ascii=False)
 if backup:
  p.evaluate('([key,fresh,prefix])=>{window.oldTagSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){const r=oldTagSet.call(this,k,v);if(k.startsWith(prefix))oldTagSet.call(this,key,fresh);return r;};}',[KEY,fresh,PREFIX]);repair(p)
 else:
  p.get_by_role('button',name='恢复可读标签',exact=True).click();p.evaluate('([k,v])=>localStorage.setItem(k,v)',[KEY,fresh]);p.get_by_role('button',name='确认恢复',exact=True).click()
 expect(p.locator('.prototype-toast')).to_contain_text('更新');assert raw(p)==fresh and archives(p)==([MIX]if backup else[])
def blocked(p):
 seed(p,MIX);prompt(p);dismiss(p);before=store(p)
 outcomes=p.evaluate('()=>[PrototypeUI.write("dujia-prototype-tags",[]),PrototypePreferences.transaction([["dujia-prototype-tags",[]],["dujia-prototype-records",[]]]),PrototypePreferences.tagUpdate({id:"kept-tag",name:"替换",scope:"shared"}),PrototypePreferences.tagUpdate({id:"kept-tag",name:"保留标签",scope:"shared"},true)]')
 assert outcomes==[False]*4 and raw(p)==MIX;assert store(p)==before
def dirty(p):
 seed(p,json.dumps([TAG],ensure_ascii=False),'m06-p02.html');p.locator('#nickname').fill('尚未保存的名字');p.evaluate('([k,v])=>localStorage.setItem(k,v)',[KEY,MIX]);p.evaluate('()=>{PrototypePreferences.recoverTags();}');prompt(p);repair(p)
 expect(p.get_by_text('是否放弃当前修改？',exact=True)).to_be_visible();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('#nickname')).to_have_value('尚未保存的名字');assert json.loads(raw(p))==[TAG]and archives(p)==[MIX]
 p.locator('#save').click();p.wait_for_url('**/m06-p01.html');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-profile")).nickname')=='尚未保存的名字'
def recheck(p):
 seed(p,'{broken');prompt(p);p.evaluate('([k,v])=>localStorage.setItem(k,v)',[KEY,json.dumps([TAG],ensure_ascii=False)])
 with p.expect_event('load'):p.get_by_role('button',name='重新检查',exact=True).click()
 expect(p.get_by_role('button',name=TAG['name'],exact=True)).to_be_visible();assert not archives(p)
def history(p):
 seed(p,'{标签私人原文');prompt(p);recover(p);p.goto(BASE+'pages/m06-p11.html');p.locator('.manage').click();p.get_by_role('button',name='查看恢复原始副本',exact=True).click();p.get_by_role('button',name='原始副本 1',exact=True).click();expect(p.locator('dialog')).to_contain_text('标签完整原始内容')
 with p.expect_download()as download:p.get_by_role('button',name='下载原始副本',exact=True).click()
 assert Path(download.value.path()).read_text(encoding='utf-8')=='{标签私人原文';assert raw(p)=='[]'
def unavailable(p):
 seed(p,'[]');p.evaluate('()=>{window.oldTagGet=Storage.prototype.getItem;Storage.prototype.getItem=function(k){if(k==="dujia-prototype-tags")throw new Error("blocked");return oldTagGet.call(this,k);};PrototypePreferences.recoverTags();}');prompt(p);expect(p.get_by_role('button',name='恢复可读标签',exact=True)).to_be_disabled();expect(p.get_by_role('button',name='导出原始标签',exact=True)).to_be_disabled();dismiss(p)
 assert not p.evaluate('PrototypePreferences.initializeTags()');p.evaluate('()=>{Storage.prototype.getItem=oldTagGet;}');assert raw(p)=='[]'and not archives(p)
def healthy(p,missing):
 seed(p,None if missing else'[]');expect(p.locator('dialog')).to_have_count(0);assert not archives(p)
 if missing:assert any(v['name']=='日常'for v in json.loads(raw(p)))
 else:assert raw(p)=='[]'
def invalid(p):
 seed(p,json.dumps([TAG],ensure_ascii=False));before=store(p)
 assert p.evaluate('()=>[PrototypeUI.write("dujia-prototype-tags",{}),PrototypeUI.write("dujia-prototype-tags",[null]),PrototypeUI.write("dujia-prototype-tags",[{id:"x",name:"名字",scope:"invalid"}])]')==[False]*3
 assert store(p)==before
def records_kept(p):
 seed(p,MIX);prompt(p);before=p.evaluate('localStorage.getItem("dujia-prototype-records")');recover(p);assert p.evaluate('localStorage.getItem("dujia-prototype-records")')==before
 expect(p.get_by_role('button',name=TAG['name'],exact=True)).to_be_visible()
 backup=p.evaluate('PrototypePreferences.snapshot(true)');assert all(v['scope']=='shared'for v in backup['tags']);assert '标签私人原文'not in json.dumps(backup,ensure_ascii=False)
def ordered(p):
 seed(p,json.dumps([TAG],ensure_ascii=False),'m06-p11.html');p.evaluate('([key,mix])=>{localStorage.setItem("dujia-profile","{profile");localStorage.setItem("dujia-prototype-records","{records");localStorage.setItem("dujia-prototype-works","{works");localStorage.setItem(key,mix);}',[KEY,MIX]);p.reload()
 for title,action,confirm_title in [('资料需要恢复','恢复可读资料','保留原始副本并恢复资料？'),('记录需要恢复','恢复可读记录','保留原始副本并恢复？'),('作品需要恢复','恢复可读作品','保留原始副本并恢复作品？'),('标签需要恢复','恢复可读标签','保留原始副本并恢复标签？')]:
  expect(p.get_by_role('dialog',name=title,exact=True)).to_be_visible();p.get_by_role('button',name=action,exact=True).click();expect(p.get_by_role('dialog',name=confirm_title,exact=True)).to_be_visible()
  with p.expect_event('load'):p.get_by_role('button',name='确认恢复',exact=True).click()
 assert archives(p)==[MIX]and json.loads(raw(p))==[TAG]
def dirty_tag(p):
 seed(p,json.dumps([TAG],ensure_ascii=False));p.get_by_role('button',name=TAG['name'],exact=True).click();p.get_by_role('button',name='编辑标签',exact=True).click();field=p.get_by_role('textbox',name='标签名称',exact=True);field.fill('还没保存的标签');p.evaluate('([k,v])=>localStorage.setItem(k,v)',[KEY,MIX]);p.get_by_role('button',name='保存标签',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('请先恢复标签');expect(field).to_have_value('还没保存的标签');assert raw(p)==MIX
 p.keyboard.press('Escape');p.get_by_role('button',name='继续编辑',exact=True).click();expect(field).to_have_value('还没保存的标签');p.keyboard.press('Escape');p.get_by_role('button',name='放弃修改',exact=True).click();expect(p.locator('dialog')).to_have_count(0);p.get_by_role('button',name='恢复标签',exact=True).click();prompt(p);recover(p)
 p.get_by_role('button',name=TAG['name'],exact=True).click();p.get_by_role('button',name='编辑标签',exact=True).click();p.get_by_role('textbox',name='标签名称',exact=True).fill('恢复后保存');p.get_by_role('button',name='保存标签',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.get_by_role('button',name='恢复后保存',exact=True)).to_be_visible()
def cache_account(p):
 seed(p,'{标签私人原文');prompt(p);recover(p);assert archives(p)==['{标签私人原文'];p.goto(BASE+'pages/m06-p11.html');p.locator('#cache').click();p.get_by_role('button',name='确认清理',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('缓存');assert archives(p)==['{标签私人原文']
 p.goto(BASE+'pages/m06-p08.html');p.locator('.delete').click();p.get_by_role('button',name='继续身份确认',exact=True).click();p.get_by_role('textbox',name='演示验证码 284631',exact=True).fill('284631');p.get_by_role('button',name='注销演示账号',exact=True).click();p.wait_for_url('**/m01-p01.html');assert not archives(p)and raw(p)is None
def layout(p,width):
 seed(p,MIX);prompt(p);p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
 for state in ['choice','confirm']:
  if state=='confirm':p.get_by_role('button',name='恢复可读标签',exact=True).click();expect(p.get_by_role('dialog',name='保留原始副本并恢复标签？',exact=True)).to_be_visible()
  buttons=p.locator('dialog button');assert buttons.count()>=2
  for b in buttons.all():
   metric=b.evaluate('b=>{const r=b.getBoundingClientRect();return {x:r.x,right:r.right,y:r.y,bottom:r.bottom,w:r.width,h:r.height,hit:document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===b}}');assert metric['x']>=0 and metric['right']<=width+1 and metric['y']>=0 and metric['bottom']<=845 and metric['w']>=44 and metric['h']>=44 and metric['hit'],metric
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
  if width==320:p.screenshot(path=str(OUT/f'tag-recovery-{state}-320.png'),full_page=True)
 p.get_by_role('button',name='取消',exact=True).click();prompt(p);dismiss(p);button=p.get_by_role('button',name='恢复标签',exact=True);button.scroll_into_view_if_needed();button.focus();p.keyboard.press('Enter');prompt(p);p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);expect(button).to_be_focused();assert raw(p)==MIX
jobs=[('archive-quota',lambda p:quota(p,False)),('replace-quota',lambda p:quota(p,True)),('before-repair-race',lambda p:race(p,False)),('during-archive-race',lambda p:race(p,True)),('blocked-write-and-transaction',blocked),('dirty-profile-keeps-input',dirty),('external-repair-recheck',recheck),('archive-history-download',history),('storage-unavailable',unavailable),('missing-default-initialization',lambda p:healthy(p,True)),('valid-empty-stays-empty',lambda p:healthy(p,False)),('invalid-proposed-values',invalid),('records-retained-backup-scope',records_kept),('account-record-work-tag-order',ordered),('dirty-tag-recovery-save',dirty_tag),('cache-preserves-account-removes-tag-copy',cache_account)]+[(f'layout-{width}',lambda p,w=width:layout(p,w))for width in [320,360,390,414,430]]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in jobs:
  width=int(name[7:])if name.startswith('layout-')else 390;c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-2400:])
  row.update(case=name,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert files==source();(OUT/'tag-recovery-state-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
