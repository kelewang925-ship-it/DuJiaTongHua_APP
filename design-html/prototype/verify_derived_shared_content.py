"""Current ancestry must gate shared selectors, backups and new publication."""
import json,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from book_test_helpers import fixture
from verify_pet_controls import ROOT,BASE,source
OUT=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');OUT.mkdir(parents=True,exist_ok=True);files=source();rows=[]
CAP='dujia-prototype-capsules';MOM='dujia-prototype-moments';WORK='dujia-prototype-works';REC='dujia-prototype-records'
SECRET='DERIVED-CAPSULE-SECRET'

def seed(p,mode='private',page='m06-p11.html'):
 d=data(True);d['dujia-prototype-session']={'loggedIn':True};d['dujia-prototype-preferences']={'autoBackup':False,'reduceMotion':True}
 cap=dict(id='ancestor',name='来源胶囊',message=SECRET,opening='2026-10-04',status='opened',visibility='private'if mode=='private'else'shared')
 if mode in ['sealed','draft']:cap['status']=mode
 moment=dict(id='derived',name='收录来源',story=SECRET,date='2026-10-04',status='published',visibility='private'if mode=='private-child'else'shared',capsuleId=cap['id'],comments=[])
 work={**d[WORK][0], 'id':'derived-work','name':'来源作品','sourceKind':'moment','sourceIds':[moment['id']],'story':SECRET}
 photo={**d[REC][-1],'id':'derived-photo','title':'衍生照片','workId':work['id'],'caption':SECRET,'body':SECRET}
 d[CAP]=[]if mode=='deleted'else[cap];d[MOM]=[moment,dict(id='independent',name='独立共同时刻',story='INDEPENDENT',date='2026-10-04',comments=[])];d[WORK]=[work];d[REC]=[photo]
 pet=d['dujia-prototype-pet'];pet['logs']=[dict(id='derived-log',type='source',sourceKind='moment',sourceId=moment['id'],text=SECRET,actor='小满',date='2026-10-04',at=1791158400000)]
 book=fixture();book['pages']=[dict(id='page-state',chapterId='chapter-state',template='重要时刻',source=dict(kind='moment',id='derived'))];d['dujia-prototype-books']=[book]
 p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-05");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d)
 if mode=='damaged':p.evaluate('k=>localStorage.setItem(k,"{broken")',CAP)
 if mode=='cycle':p.evaluate('k=>{const w=JSON.parse(localStorage.getItem(k));w[0].sourceKind="photo";w[0].sourceIds=["derived-photo"];localStorage.setItem(k,JSON.stringify(w));}',WORK)
 p.goto(BASE+'pages/'+page)

def catalog(p,mode,allow=False):
 seed(p,mode);before=p.evaluate('()=>Object.fromEntries(Object.entries(localStorage))');v=p.evaluate('PrototypePreferences.bookSources()');assert any(x['id']=='independent'for x in v);assert any(x['id']=='derived'for x in v)==(allow or mode=='cycle');assert any(x['id']=='derived-work'for x in v)==allow;assert any(x['id']=='derived-photo'for x in v)==allow;assert p.evaluate('()=>Object.fromEntries(Object.entries(localStorage))')==before

def backup(p):
 seed(p);p.locator('#backup').click();expect(p.locator('.prototype-toast')).to_contain_text('备份已创建');v=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-backup"))');assert SECRET not in json.dumps(v), 'Private ancestor content leaked into shared backup';assert any(x['id']=='independent'for x in v['moments']);assert SECRET in json.dumps(p.evaluate('PrototypePreferences.snapshot(false)')['moments'])

def reading(p):
 seed(p,page='m08-p16.html?id=book-state&page=page-state');expect(p.get_by_text('关联内容不可见',exact=False).first).to_be_visible();assert SECRET not in p.locator('.screen').inner_text()

def download(p):
 seed(p,page='m08-p21.html?id=book-state')
 with p.expect_download()as result:p.get_by_role('button',name='导出这本回忆册',exact=True).click()
 assert SECRET not in Path(result.value.path()).read_text(encoding='utf-8')

def workshop(p):
 seed(p,page='m05-p02.html');p.get_by_role('button',name='重要时刻',exact=False).click();p.locator('#go').click();expect(p.locator('dialog')).to_be_visible();assert '收录来源'not in p.locator('dialog').inner_text();expect(p.get_by_text('独立共同时刻',exact=True)).to_be_visible()

def pet(p):
 seed(p,page='m07-p19.html?id=derived-log');p.wait_for_url('**/m07-p17.html*');assert SECRET not in p.locator('.screen').inner_text()

def generate(p):
 seed(p,'shared','m05-p03.html?id=derived-work');p.evaluate('k=>{const v=JSON.parse(localStorage.getItem(k));v[0].visibility="private";localStorage.setItem(k,JSON.stringify(v));}',CAP);before=p.evaluate('localStorage.getItem("dujia-prototype-works")');p.locator('#generate').click();expect(p.locator('.prototype-toast')).to_contain_text('不可见');assert p.evaluate('localStorage.getItem("dujia-prototype-works")')==before;assert p.locator('#story').input_value()==SECRET

def album(p):
 seed(p,page='m05-p08.html?id=derived-work');before=p.evaluate('localStorage.getItem("dujia-prototype-records")');result=p.evaluate('async()=>{try{await PrototypeWorkshop.album(PrototypeWorkshop.find("derived-work"));return null}catch(e){return e.message}}');assert result and '不可见'in result;assert p.evaluate('localStorage.getItem("dujia-prototype-records")')==before

def external(p,pet=False):
 seed(p,'shared',('m07-p19.html?id=derived-log'if pet else'm08-p16.html?id=book-state&page=page-state'));expect(p.get_by_text(SECRET,exact=False).first).to_be_visible();other=p.context.new_page();other.goto(BASE+'prototype/review.html');other.evaluate('k=>{const v=JSON.parse(localStorage.getItem(k));v[0].visibility="private";localStorage.setItem(k,JSON.stringify(v));}',CAP)
 if pet:p.wait_for_url('**/m07-p17.html*')
 else:expect(p.get_by_text('关联内容不可见',exact=False).first).to_be_visible()
 assert SECRET not in p.locator('.screen').inner_text();other.close()

def pending_album(p,work_race=False):
 seed(p,'shared','m05-p08.html?id=derived-work');p.evaluate('()=>{localStorage.setItem("dujia-prototype-records","[]");const decode=HTMLImageElement.prototype.decode;HTMLImageElement.prototype.decode=function(){return decode.call(this).then(()=>new Promise(resolve=>{window.releaseAlbumImage=resolve;}));};}');before=p.evaluate('localStorage.getItem("dujia-prototype-records")');p.locator('#save').click();p.wait_for_function('typeof releaseAlbumImage==="function"')
 if work_race:p.evaluate('k=>{const v=JSON.parse(localStorage.getItem(k));v[0].name="别处更新的作品";localStorage.setItem(k,JSON.stringify(v));releaseAlbumImage();}',WORK)
 else:p.evaluate('k=>{const v=JSON.parse(localStorage.getItem(k));v[0].visibility="private";localStorage.setItem(k,JSON.stringify(v));releaseAlbumImage();}',CAP)
 expect(p.locator('.prototype-toast')).to_contain_text('更新'if work_race else'不可见');assert p.evaluate('localStorage.getItem("dujia-prototype-records")')==before
 if work_race:assert p.evaluate('PrototypeWorkshop.find("derived-work").name')=='别处更新的作品'

jobs={**{mode+'-catalog':lambda p,m=mode:catalog(p,m)for mode in ['private','sealed','draft','private-child','damaged','cycle']},'shared-chain-retained':lambda p:catalog(p,'shared',True),'deleted-ancestor-independent-copy-retained':lambda p:catalog(p,'deleted',True),'actual-shared-backup':backup,'actual-book-reading':reading,'actual-book-download':download,'actual-workshop-selector':workshop,'actual-pet-story':pet,'current-generation-refuses-private':generate,'current-album-refuses-private':album,'external-book-privacy-refresh':external,'external-pet-privacy-refresh':lambda p:external(p,True),'pending-album-privacy-no-publication':pending_album,'pending-album-work-race-no-publication':lambda p:pending_album(p,True)}
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in jobs.items():
  c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);p.set_default_navigation_timeout(15000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-2000:])
  row.update(case=name,errors=errors);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert source()==files;(OUT/'derived-shared-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
