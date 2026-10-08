"""Rendered scope, known owner identity and current comment submission gates."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
OUT=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');OUT.mkdir(parents=True,exist_ok=True);files=source();rows=[]
CAP='dujia-prototype-capsules';REC='dujia-prototype-records';MOM='dujia-prototype-moments'
SECRET='PRIVATE-SOURCE-DISPLAY'
def seed(p,page,shared=False,peer=False):
 d=data(True);d['dujia-prototype-session']={'loggedIn':True};d['dujia-prototype-preferences']={'autoBackup':False,'reduceMotion':True};d['dujia-prototype-books']=[]
 cap=dict(id='ancestor',name='来源信',message=SECRET,opening='2026-10-04',status='opened',visibility='shared'if shared else'private')
 moment=dict(id='derived',name='衍生时刻',story=SECRET,date='2026-10-04',visibility='shared',author='阿舟'if peer else'小满',capsuleId=cap['id'],comments=[dict(id='private-reply',text=SECRET,author='阿舟',createdAt=2)])
 work={**d['dujia-prototype-works'][0],'id':'derived-work','sourceKind':'moment','sourceIds':['derived']}
 photo={**d[REC][-1],'id':'derived-photo','title':'衍生照片','caption':SECRET,'body':SECRET,'author':'阿舟'if peer else'小满','workId':work['id'],'comments':[]}
 own={**d[REC][1],'id':'own-private','title':'自己的私密日记'};peer_record={**own,'id':'peer-private','title':'另一方的私密日记','author':'阿舟','body':'PEER-PRIVATE-BODY'}
 normal={**d[REC][0],'id':'normal','title':'普通共同日记','comments':[dict(id='normal-reply',text='PUBLIC-REPLY',author='阿舟',createdAt=1)]}
 normal_photo={**d[REC][-1],'id':'normal-photo','title':'普通共同照片'}
 d[CAP]=[cap];d[MOM]=[moment];d['dujia-prototype-works']=[work];d[REC]=[photo,own,peer_record,normal,normal_photo];d['dujia-prototype-pet']=None
 p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-05");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d);p.goto(BASE+'pages/'+page)

def gallery(p):
 seed(p,'m03-p10.html');p.get_by_role('tab').nth(1).click();expect(p.locator('.prototype-photo-grid')).not_to_contain_text('衍生照片');expect(p.locator('.prototype-photo-grid')).to_contain_text('普通共同照片')
def personal_filter(p):
 seed(p,'m03-p10.html');p.locator('#filter').click();p.get_by_label('照片可见范围',exact=True).select_option('private');p.get_by_role('button',name='应用筛选',exact=True).click();expect(p.locator('.prototype-photo-grid')).to_contain_text('衍生照片')
def home(p):
 seed(p,'m03-p02.html');expect(p.locator('.recent')).not_to_contain_text('另一方的私密日记');entry=p.get_by_role('button',name='衍生照片',exact=False);expect(entry).to_contain_text('仅自己可见')
def search(p):
 seed(p,'m03-p04.html?q='+SECRET);expect(p.locator('.prototype-search-results')).to_contain_text('仅自己可见')
def diary_list(p):
 seed(p,'m03-p06.html');expect(p.locator('.screen')).to_contain_text('自己的私密日记');expect(p.locator('.screen')).not_to_contain_text('另一方的私密日记')
def peer_diary(p,edit=False):
 seed(p,('m03-p05.html'if edit else'm03-p07.html')+'?id=peer-private');expect(p.get_by_text('这篇日记暂不可见',exact=True)).to_be_visible();assert 'PEER-PRIVATE-BODY'not in p.locator('.screen').inner_text()
def peer_photo(p,edit=False):
 seed(p,('m03-p11.html'if edit else'm03-p12.html')+'?id=derived-photo',peer=True);expect(p.get_by_text('这张照片暂不可见',exact=True)).to_be_visible();assert SECRET not in p.locator('.screen').inner_text()
def own_photo(p):
 seed(p,'m03-p12.html?id=derived-photo');expect(p.locator('.meta')).to_contain_text('仅自己可见');expect(p.locator('#message')).to_be_hidden();expect(p.locator('.caption')).to_contain_text(SECRET)
def own_moment(p):
 seed(p,'m04-p03.html?id=derived');expect(p.locator('.people')).to_contain_text('仅自己可见');expect(p.locator('.message')).to_be_disabled();expect(p.locator('.description')).to_contain_text(SECRET)
def replies(p):
 seed(p,'m04-p16.html');expect(p.locator('.prototype-reply-cards')).to_contain_text('PUBLIC-REPLY');expect(p.locator('.prototype-reply-cards')).not_to_contain_text(SECRET)
def flip(p,other=False,shared=False):
 target=p
 if other:target=p.context.new_page();target.goto(BASE+'prototype/review.html')
 target.evaluate('([k,visibility])=>{const v=JSON.parse(localStorage.getItem(k));v[0].visibility=visibility;localStorage.setItem(k,JSON.stringify(v));}',[CAP,'shared'if shared else'private'])
 if other:target.close()
def photo_pending(p):
 seed(p,'m03-p12.html?id=derived-photo',True);p.locator('#reply').fill('未发送文字');before=p.evaluate('localStorage.getItem("dujia-prototype-records")');p.locator('#message [type=submit]').click();flip(p);expect(p.locator('.prototype-toast')).to_contain_text('不再共同可见');assert p.evaluate('localStorage.getItem("dujia-prototype-records")')==before;expect(p.locator('#reply')).to_have_value('未发送文字')
def moment_pending(p):
 seed(p,'m04-p03.html?id=derived',True);p.locator('.message').click();field=p.get_by_label('回应这个时刻',exact=True);field.fill('时刻未发送');before=p.evaluate('localStorage.getItem("dujia-prototype-moments")');p.get_by_role('button',name='发送回应',exact=True).click();flip(p);expect(p.locator('.prototype-toast')).to_contain_text('不再共同可见');assert p.evaluate('localStorage.getItem("dujia-prototype-moments")')==before;expect(field).to_have_value('时刻未发送')
def external_gallery(p):
 seed(p,'m03-p10.html',True);p.get_by_role('tab').nth(1).click();expect(p.locator('.prototype-photo-grid')).to_contain_text('衍生照片');flip(p,True);expect(p.locator('.prototype-photo-grid')).not_to_contain_text('衍生照片')
def external_photo_draft(p):
 seed(p,'m03-p12.html?id=derived-photo',True);p.locator('#reply').fill('外部变化草稿');flip(p,True);expect(p.locator('.meta')).to_contain_text('仅自己可见');expect(p.locator('#reply')).to_have_value('外部变化草稿');expect(p.locator('#message [type=submit]')).to_be_disabled()
def peer_moment(p,edit=False):
 seed(p,('m04-p04.html'if edit else'm04-p03.html')+'?id=derived',peer=True);expect(p.get_by_text('这个时刻暂不可见',exact=True)).to_be_visible();assert SECRET not in p.locator('.screen').inner_text();p.get_by_role('button',name='返回时刻册',exact=True).click();p.wait_for_url('**/m04-p02.html')
def photo_restore(p):
 seed(p,'m03-p12.html?id=derived-photo',True);p.locator('#reply').fill('恢复后发送');flip(p,True);expect(p.locator('#message [type=submit]')).to_be_disabled();flip(p,True,True);expect(p.locator('.meta')).to_contain_text('共同可见');expect(p.locator('#message [type=submit]')).to_be_enabled();expect(p.locator('.comments-title')).not_to_contain_text('仅自己可见');p.locator('#message [type=submit]').click();expect(p.locator('.prototype-toast')).to_contain_text('留言已保存');assert p.evaluate('PrototypeRecords.find("derived-photo").comments.at(-1).text')=='恢复后发送'
def moment_restore(p):
 seed(p,'m04-p03.html?id=derived',True);p.locator('.message').click();field=p.get_by_label('回应这个时刻',exact=True);field.fill('恢复后回应');flip(p,True);expect(p.get_by_role('button',name='发送回应',exact=True)).to_be_disabled();flip(p,True,True);expect(p.get_by_role('button',name='发送回应',exact=True)).to_be_enabled();expect(field).to_have_value('恢复后回应');p.get_by_role('button',name='发送回应',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-moments"))[0].comments.at(-1).text')=='恢复后回应'
def layout(p,width):
 for page in ['m03-p12.html?id=derived-photo','m04-p03.html?id=derived']:
  seed(p,page);p.evaluate('()=>{document.documentElement.style.setProperty("--ui-safe-top","44px");document.documentElement.style.setProperty("--ui-safe-bottom","34px");}')
  expect(p.locator('.meta'if page.startswith('m03')else'.people')).to_contain_text('仅自己可见');assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
  for button in p.locator('button:visible:enabled').all():
   button.scroll_into_view_if_needed();rect=button.evaluate('b=>{const r=b.getBoundingClientRect();return {width:r.width,height:r.height,left:r.left,right:r.right,hit:document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===b||b.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))}}');assert rect['width']>=44 and rect['height']>=44 and rect['left']>=0 and rect['right']<=width+1 and rect['hit'],rect
  if width in [320,430]:p.screenshot(path=str(OUT/('shared-display-'+page[:7]+'-'+str(width)+'.png')),full_page=True)
jobs={'gallery-shared-tab':gallery,'gallery-personal-filter':personal_filter,'home-access-and-scope':home,'search-effective-scope':search,'diary-list-known-owner':diary_list,'peer-private-diary-read':peer_diary,'peer-private-diary-edit':lambda p:peer_diary(p,True),'peer-derived-photo-read':peer_photo,'peer-derived-photo-edit':lambda p:peer_photo(p,True),'own-derived-photo-personal':own_photo,'own-derived-moment-personal':own_moment,'shared-replies-source-gate':replies,'photo-pending-comment-gate':photo_pending,'moment-pending-comment-gate':moment_pending,'external-gallery-refresh':external_gallery,'external-photo-draft-retained':external_photo_draft,'peer-private-moment-read-return':peer_moment,'peer-private-moment-edit-return':lambda p:peer_moment(p,True),'photo-source-restored-draft-submit':photo_restore,'moment-source-restored-draft-submit':moment_restore,**{'private-layout-'+str(w):lambda p,w=w:layout(p,w)for w in [320,360,390,414,430]}}
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in jobs.items():
  width=int(name.rsplit('-',1)[1])if name.startswith('private-layout-')else 390;c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);p.set_default_navigation_timeout(15000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-2000:])
  row.update(case=name,errors=errors);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert source()==files;(OUT/'shared-display-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
