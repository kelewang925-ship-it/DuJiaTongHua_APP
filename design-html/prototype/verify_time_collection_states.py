"""Actual time recovery failures, races, dirty editors, originals and five widths."""
import json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from verify_time_collection_recovery import seed,raw,archives,prompt,repair,key,prefix,KINDS
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source,store
OUT=ROOT/'evidence/current';files=source();rows=[]
def mixed(kind):return json.dumps([data(True)[key(kind)][0],None],ensure_ascii=False)
def recover(p,kind):
 with p.expect_event('load'):repair(p,kind)
 expect(p.locator('dialog')).to_have_count(0)
def quota(p,kind,replace):
 value=mixed(kind);seed(p,kind,value,KINDS[kind][1][0]);prompt(p,kind);p.evaluate('([key,pre,replace])=>{window.oldTimeSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(replace?k===key:k.startsWith(pre))throw new DOMException("full","QuotaExceededError");return oldTimeSet.call(this,k,v);};}',[key(kind),prefix(kind),replace]);repair(p,kind);expect(p.locator('.prototype-toast')).to_contain_text('未能保存');assert raw(p,kind)==value and archives(p,kind)==([value]if replace else[])
 p.evaluate('()=>{Storage.prototype.setItem=oldTimeSet;}');p.get_by_role('button',name='恢复'+KINDS[kind][0],exact=True).click();recover(p,kind);assert len(json.loads(raw(p,kind)))==1;assert all(v==value for v in archives(p,kind))
def race(p,kind,backup):
 value=mixed(kind);seed(p,kind,value,KINDS[kind][1][0]);prompt(p,kind);fresh=json.dumps([{**data(True)[key(kind)][0],'name':'别处更新'}],ensure_ascii=False)
 if backup:p.evaluate('([key,pre,fresh])=>{window.oldTimeSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){const r=oldTimeSet.call(this,k,v);if(k.startsWith(pre))oldTimeSet.call(this,key,fresh);return r;};}',[key(kind),prefix(kind),fresh]);repair(p,kind)
 else:p.get_by_role('button',name='恢复可读'+KINDS[kind][0],exact=True).click();p.evaluate('([k,v])=>localStorage.setItem(k,v)',[key(kind),fresh]);p.get_by_role('button',name='确认恢复',exact=True).click()
 expect(p.locator('.prototype-toast')).to_contain_text('更新');assert raw(p,kind)==fresh and archives(p,kind)==([value]if backup else[])
def guarded(p,kind):
 value=mixed(kind);seed(p,kind,value,KINDS[kind][1][0]);prompt(p,kind);p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0);before=store(p)
 assert p.evaluate('k=>[PrototypeUI.write(k,[]),PrototypePreferences.transaction([[k,[]],["dujia-prototype-records",[]]])]',key(kind))==[False,False];assert store(p)==before
def healthy(p,kind):
 seed(p,kind,'[]',KINDS[kind][1][0]);expect(p.locator('dialog')).to_have_count(0);assert raw(p,kind)=='[]'and not archives(p,kind)
 assert not p.evaluate('k=>PrototypeUI.write(k,[null])',key(kind));assert raw(p,kind)=='[]'
def dirty(p,kind):
 item=data(True)[key(kind)][0];item={**item,**({'status':'draft'}if kind=='capsules'else{})};pages={'moments':'m04-p04','anniversaries':'m04-p09','capsules':'m04-p13'};seed(p,kind,json.dumps([item],ensure_ascii=False),pages[kind]+'.html?id='+item['id']);field=p.locator('[name=name]');field.fill('未保存的名称');value=json.dumps([item,None],ensure_ascii=False);p.evaluate('([k,v])=>localStorage.setItem(k,v)',[key(kind),value]);p.evaluate('k=>{PrototypeUI.recoverCollection(k);}',key(kind));prompt(p,kind);repair(p,kind);expect(p.get_by_text('是否放弃当前修改？',exact=True)).to_be_visible();p.get_by_role('button',name='继续编辑',exact=True).click();expect(field).to_have_value('未保存的名称');assert archives(p,kind)==[value]
def history(p,kind):
 value='{'+KINDS[kind][0]+'私人原文';seed(p,kind,value,KINDS[kind][1][0]);prompt(p,kind);recover(p,kind);p.goto(BASE+'pages/m06-p11.html');p.locator('.manage').click();p.get_by_role('button',name='查看恢复原始副本',exact=True).click();p.get_by_role('button',name='原始副本 1',exact=True).click();expect(p.locator('dialog')).to_contain_text(KINDS[kind][0]+'完整原始内容')
 with p.expect_download()as download:p.get_by_role('button',name='下载原始副本',exact=True).click()
 assert Path(download.value.path()).read_text(encoding='utf-8')==value
def recheck(p,kind):
 seed(p,kind,'{broken',KINDS[kind][1][0]);prompt(p,kind);p.evaluate('([k,v])=>localStorage.setItem(k,v)',[key(kind),json.dumps(data(True)[key(kind)],ensure_ascii=False)])
 with p.expect_event('load'):p.get_by_role('button',name='重新检查',exact=True).click()
 expect(p.locator('dialog')).to_have_count(0);assert not archives(p,kind)
def unavailable(p,kind):
 seed(p,kind,'[]',KINDS[kind][1][0]);p.evaluate('key=>{window.oldTimeGet=Storage.prototype.getItem;Storage.prototype.getItem=function(k){if(k===key)throw new Error("blocked");return oldTimeGet.call(this,k);};PrototypeUI.recoverCollection(key);}',key(kind));prompt(p,kind);expect(p.get_by_role('button',name='恢复可读'+KINDS[kind][0],exact=True)).to_be_disabled();expect(p.get_by_role('button',name='导出原始'+KINDS[kind][0],exact=True)).to_be_disabled();p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0);p.evaluate('()=>{Storage.prototype.getItem=oldTimeGet;}');assert raw(p,kind)=='[]'
def layout(p,kind,width):
 value=mixed(kind);seed(p,kind,value,KINDS[kind][1][0]);prompt(p,kind);p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
 for state in ['choice','confirm']:
  if state=='confirm':p.get_by_role('button',name='恢复可读'+KINDS[kind][0],exact=True).click();expect(p.get_by_role('button',name='取消',exact=True)).to_be_focused();assert p.get_by_role('button',name='确认恢复',exact=True).evaluate('b=>b.dataset.danger==="true"')
  for b in p.locator('dialog button').all():
   m=b.evaluate('b=>{const r=b.getBoundingClientRect();return {x:r.x,right:r.right,y:r.y,bottom:r.bottom,w:r.width,h:r.height,hit:document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===b}}');assert m['x']>=0 and m['right']<=width+1 and m['y']>=0 and m['bottom']<=845 and m['w']>=44 and m['h']>=44 and m['hit'],m
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
  if width==320:p.screenshot(path=str(OUT/f'time-recovery-{kind}-{state}-320.png'),full_page=True)
 p.get_by_role('button',name='取消',exact=True).click();prompt(p,kind);p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0);button=p.get_by_role('button',name='恢复'+KINDS[kind][0],exact=True);button.scroll_into_view_if_needed();button.focus();p.keyboard.press('Enter');prompt(p,kind);p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);expect(button).to_be_focused();assert raw(p,kind)==value
def ordered(p):
 seed(p,'moments','[]','m06-p11.html');p.evaluate('()=>{for(const k of ["moments","anniversaries","capsules"])localStorage.setItem("dujia-prototype-"+k,"{broken");}');p.reload()
 for kind in KINDS:
  prompt(p,kind)
  with p.expect_event("load"):repair(p,kind)
  assert raw(p,kind)=="[]"
 expect(p.locator("dialog")).to_have_count(0)
 assert all(raw(p,k)=='[]'and archives(p,k)==['{broken']for k in KINDS)
jobs=[]
for kind in KINDS:
 for name,run in [('archive-quota',lambda p,k=kind:quota(p,k,False)),('replace-quota',lambda p,k=kind:quota(p,k,True)),('before-race',lambda p,k=kind:race(p,k,False)),('during-race',lambda p,k=kind:race(p,k,True)),('guarded-writes',lambda p,k=kind:guarded(p,k)),('healthy-empty',lambda p,k=kind:healthy(p,k)),('dirty-input',lambda p,k=kind:dirty(p,k)),('archive-download',lambda p,k=kind:history(p,k)),('external-recheck',lambda p,k=kind:recheck(p,k)),('unavailable',lambda p,k=kind:unavailable(p,k))]:jobs.append((kind+'-'+name,390,run))
 for width in [320,360,390,414,430]:jobs.append((kind+'-layout-'+str(width),width,lambda p,k=kind,w=width:layout(p,k,w)))
jobs.append(('three-collection-order',390,ordered))
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,width,run in jobs:
  c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);p.set_default_navigation_timeout(15000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-2000:])
  row.update(case=name,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert files==source();(OUT/'time-collection-state-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
