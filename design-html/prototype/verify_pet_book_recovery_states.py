import json,traceback,copy
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
files=source();rows=[];base=data(True);base['dujia-prototype-session']=dict(loggedIn=True,phone='13812345678');base['dujia-prototype-preferences']=dict(reduceMotion=True,autoBackup=False)
def seed(p):
 p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',base)
def damage(p,kind):
 key='dujia-prototype-'+kind;p.evaluate('(k)=>localStorage.setItem(k,"{broken")',key);p.goto(BASE+'pages/m06-p11.html');expect(p.get_by_role('dialog',name=('宠物'if kind=='pet'else'回忆册')+'需要恢复',exact=True)).to_be_visible();return key
def original(p,key):return p.evaluate('(k)=>localStorage.getItem(k)',key)
def repair(p,kind):
 p.get_by_role('button',name='恢复可读'+('宠物'if kind=='pet'else'回忆册'),exact=True).click();p.get_by_role('button',name='确认恢复',exact=True).click()
def quota(p,kind,replacement=False):
 seed(p);key=damage(p,kind);p.evaluate('([key,replacement])=>{const raw=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(replacement?k===key:k.startsWith(key+"-recovery-"))throw new DOMException("full","QuotaExceededError");return raw.call(this,k,v)}}',[key,replacement]);repair(p,kind);expect(p.locator('dialog')).to_have_count(0);assert original(p,key)=='{broken';copies=p.evaluate('(k)=>Object.keys(localStorage).filter(v=>v.startsWith(k+"-recovery-"))',key);assert bool(copies)==replacement
def race(p,kind,after=False):
 seed(p);key=damage(p,kind);p.get_by_role('button',name='恢复可读'+('宠物'if kind=='pet'else'回忆册'),exact=True).click();value=json.dumps(None if kind=='pet'else[])
 if after:p.evaluate('([key,value])=>{const raw=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){raw.call(this,k,v);if(k.startsWith(key+"-recovery-")){raw.call(this,key,value)}}}',[key,value])
 else:p.evaluate('([key,value])=>localStorage.setItem(key,value)',[key,value])
 p.get_by_role('button',name='确认恢复',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert original(p,key)==value
def legacy(p,value):
 seed(p);p.evaluate('(v)=>localStorage.setItem("dujia-prototype-pet",v)',value);p.goto(BASE+'pages/m07-p04.html');expect(p.get_by_role('button',name='一起领养',exact=True)).to_be_visible();assert not p.locator('dialog').count();assert p.evaluate('PrototypeUI.collectionHealth("dujia-prototype-pet").issues')==[];p.goto(BASE+'pages/m06-p11.html');p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('备份已创建');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-backup")).pet')is None
def deleted(p):
 seed(p);p.goto(BASE+'pages/m06-p11.html');p.evaluate('()=>{PrototypePreferences.deleteAccount()}');p.wait_for_url('**/m01-p01.html');assert original(p,'dujia-prototype-pet')=='null';p.evaluate('localStorage.setItem("dujia-prototype-session",JSON.stringify({loggedIn:true,phone:"13812345678"}))');p.goto(BASE+'pages/m06-p11.html');p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('备份已创建')
def dirty(p,kind):
 seed(p)
 if kind=='pet':p.evaluate('localStorage.setItem("dujia-prototype-pet","null")');p.goto(BASE+'pages/m07-p02.html');field=p.locator('#pet-name');field.fill('保留的领养输入')
 else:p.goto(BASE+'pages/m08-p04.html');field=p.get_by_label('书名',exact=True);field.fill('保留的新册输入')
 key='dujia-prototype-'+kind;p.evaluate('(k)=>localStorage.setItem(k,"{broken")',key);p.evaluate('(k)=>PrototypeUI.read(k)',key);expect(p.get_by_role('dialog',name=('宠物'if kind=='pet'else'回忆册')+'需要恢复',exact=True)).to_be_visible();repair(p,kind);expect(p.get_by_role('dialog',name='是否放弃当前修改？',exact=True)).to_be_visible();p.get_by_role('button',name='继续编辑',exact=True).click();expect(field).to_have_value('保留的领养输入'if kind=='pet'else'保留的新册输入');assert original(p,key)!='{broken'
def archive(p,kind):
 seed(p);key=damage(p,kind)
 with p.expect_request_finished(lambda r:r.resource_type=='document'and r.url==BASE+'pages/m06-p11.html'):repair(p,kind)
 p.wait_for_load_state('load');expect(p.locator('dialog')).to_have_count(0);p.locator('.manage').click();p.get_by_role('button',name='查看恢复原始副本',exact=True).click();p.get_by_role('button',name='原始副本 1',exact=True).click();expect(p.locator('dialog')).to_contain_text(('宠物'if kind=='pet'else'回忆册')+'完整原始内容')
 with p.expect_download()as dl:p.get_by_role('button',name='下载原始副本',exact=True).click()
 assert Path(dl.value.path()).read_text(encoding='utf-8')=='{broken'
def layout(p,kind,w):
 seed(p);p.evaluate('(k)=>localStorage.setItem(k,"{broken")','dujia-prototype-'+kind);p.goto(BASE+'pages/'+('m07-p25.html'if kind=='pet'else'm08-p16.html?id=book-state&page=page-state'));expect(p.locator('dialog')).to_be_visible();p.get_by_role('button',name='稍后处理',exact=True).click();state=p.locator('.screen .prototype-component-state');expect(state).to_contain_text('数据需要恢复');b=state.get_by_role('button',name='恢复'+('宠物'if kind=='pet'else'回忆册'),exact=True);b.scroll_into_view_if_needed();box=b.bounding_box();assert box['width']>=44 and box['height']>=44;assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');b.focus();p.keyboard.press('Enter');expect(p.locator('dialog')).to_be_visible();p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);expect(b).to_be_focused();p.screenshot(path=str(ROOT/'evidence/current'/f'{kind}-damaged-{w}.png'),full_page=True)
def unknown_pet(p):
 seed(p);v=copy.deepcopy(base['dujia-prototype-pet']);v['status']='unknown';p.evaluate('(v)=>{localStorage.setItem("dujia-prototype-pet",JSON.stringify(v));sessionStorage.setItem("dujia-prototype-peer-pet","accepted")}',v);p.goto(BASE+'pages/m06-p11.html')
 with p.expect_request_finished(lambda r:r.resource_type=='document'and r.url==BASE+'pages/m06-p11.html'):repair(p,'pet')
 p.wait_for_function('document.readyState==="complete"&&JSON.parse(localStorage.getItem("dujia-prototype-pet")).status==="pending"&&sessionStorage.getItem("dujia-prototype-peer-pet")===null');expect(p.locator('dialog')).to_have_count(0)
cases={'legacy-null':lambda p:legacy(p,'null'),'legacy-empty-array':lambda p:legacy(p,'[]'),'delete-account-then-first-backup':deleted,'unknown-status-does-not-auto-adopt':unknown_pet}
for kind in ['pet','books']:
 cases.update({kind+'-archive-quota':lambda p,k=kind:quota(p,k),kind+'-replace-quota':lambda p,k=kind:quota(p,k,True),kind+'-before-race':lambda p,k=kind:race(p,k),kind+'-after-race':lambda p,k=kind:race(p,k,True),kind+'-dirty':lambda p,k=kind:dirty(p,k),kind+'-archive-download':lambda p,k=kind:archive(p,k)})
 for w in [320,360,390,414,430]:cases[f'{kind}-layout-{w}']=lambda p,k=kind,w=w:layout(p,k,w)
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in cases.items():
  w=int(name.split('-')[-1])if '-layout-'in name else 390;c=b.new_context(viewport=dict(width=w,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
  row.update(case=name,errors=errors);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert source()==files;(ROOT/'evidence/current/pet-book-recovery-state-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed']and not r['errors']for r in rows)else 1)
