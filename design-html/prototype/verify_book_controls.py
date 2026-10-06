"""Declared book fixtures and actual initial controls, isolated from user browser."""
from pathlib import Path
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from audit_runtime import INIT,OBSERVE
from verify_pet_controls import ROOT,DEMO,BASE,OUT,source,store

def seed(p,page):
 n=int(page[-2:]);d=data(True);d['dujia-prototype-session']=dict(loggedIn=True);book=d['dujia-prototype-books'][0]
 book['pages'] += [dict(id='page-second',source=dict(kind='photo',id='audit-photo'),chapterId='chapter-state',template='照片故事'),dict(id='page-third',source=dict(kind='moment',id='audit-moment'),chapterId='chapter-two',template='重要时刻')]
 book['chapters'].append(dict(id='chapter-two',name='第二章'));book['lastPage']='page-second' if n in [16,17,18,19,20] else None
 if n==2:d['dujia-prototype-books']=[]
 if n==6:book['selected']=[dict(kind='pet',id='audit-pet:audit-story')]
 if n==7:book['pages']=[]
 if n in [10,11,12]:
  kind={10:'photo',11:'moment',12:'pet'}[n];ref=dict(kind=kind,id={'photo':'audit-photo','moment':'audit-moment','pet':'audit-pet:audit-story'}[kind]);book['pages'][0].update(source=ref,template={10:'照片故事',11:'重要时刻',12:'宠物成长'}[n]);book['selected']=[ref]
 query='?id=book-state' if n>=5 else ''
 if n in [9,10,11,12]:query+='&page=page-state'
 if n in [16,17,18,19,20]:query+='&page=page-second'
 p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d)
 p.goto(BASE+'pages/'+page+'.html'+query);expect(p.locator('.screen')).to_have_attribute('aria-busy','false');expect(p.locator('.book-load')).to_have_count(0);assert page+'.html' in p.url,(page,p.url);p.evaluate('document.fonts.ready')

ROUTES={1:{'继续阅读 ›':15,'新建回忆册':4,'本月推荐':3,'返回首页':'m03-p02'},2:{'返回':'m03-p02','新建第一本回忆册':4},3:{'返回回忆册':1,'查看并确认素材':4,'返回书架':1,'共同日记 · 2026-10-04':'m03-p08?id=audit-diary','共同照片 · 2026-10-04':'m03-p12?id=audit-photo','共同重要时刻 · 2026-10-04':'m04-p03?id=audit-moment','实际工坊作品 · 2026-10-05':'m05-p08?id=audit-work','实际成长故事 · 2026-10-04':'m07-p19?id=audit-story'},4:{'返回':1},5:{'返回上一步':4},6:{'返回上一步':5},7:{'返回素材选择':6,'放入回忆册':8,'重新选择素材':6},8:{'返回素材预览':7,'使用这个模板':9},9:{'返回版式选择':8},10:{'返回':8},11:{'返回版式选择':8},12:{'返回版式选择':8},13:{'返回编排':6,'添加书页':8,'共同日记':'m08-p09?id=book-state&page=page-state','共同照片':'m08-p10?id=book-state&page=page-second','共同重要时刻':'m08-p11?id=book-state&page=page-third'},14:{'开始翻阅':15,'继续整理':13,'返回书架':1},15:{'返回书架':1,'从第 1 页开始 →':'m08-p16?id=book-state&page=page-state','管理这本回忆册':21,'共同日记':'m08-p16?id=book-state&page=page-state','共同照片':'m08-p16?id=book-state&page=page-second','共同重要时刻':'m08-p16?id=book-state&page=page-third'},16:{'返回':15,'目录':15,'下一页':'m08-p16?id=book-state&page=page-third','查看原始共同记录':'m03-p12?id=audit-photo','上一页':'m08-p16?id=book-state&page=page-state','阅读工具':17},17:{'返回阅读':16,'目录\n查看全书目录和章节':15,'添加补页\n在书中添加新的补充页':18,'整理这本书\n调整页序、重命名、导出等':13,'管理这本书 · 书名、归档、导出与删除':21},18:{'返回阅读':16,'回到目录':15,'选择回应方式':'m08-p19?id=book-state&page=page-second&kind=写几句话'},19:{'返回补页选择':18},20:{'返回阅读工具':17,'目录':15,'查看原始共同记录':'m03-p12?id=audit-photo','上一页':'m08-p16?id=book-state&page=page-state','阅读工具':17},21:{'返回阅读':15,'整理页序':13,'修改主题与封面':'m08-p05?id=book-state&origin=manage'}}

def contract(page,v):
 n=int(page[-2:]);label=v['label'];sel=v['selector']
 if v['native_input']:return 'file' if v['type']=='file' else 'input'
 if label in ROUTES[n]:
  dest=ROUTES[n][label];return 'route:'+('m08-p'+str(dest).zfill(2) if isinstance(dest,int) else dest)
 if n==1:return 'route:m08-p15' if '共同测试册' in label else 'sheet:归档与草稿'
 if n==4:return 'create' if label.startswith('下一步') else 'pressed'
 if n==5:return 'theme-save' if label=='下一步：选择素材' else 'sheet:选择共同素材' if label=='使用封面照片' else 'pressed'
 if n==6:
  if label=='开始编排':return 'select-save'
  return 'source-toggle' if ' · ' in label else 'tab'
 if n==7:return 'skip'
 if n==8:return 'pressed'
 if n==9:
  return {'#changeExcerpt':'sheet:选择共同素材','#changePhoto':'sheet:选择共同素材','#changeTemplate':'stash'}.get(sel,'page-save')
 if n==10:
  if label=='裁剪/替换':return 'sheet:照片1' if 'button:nth-of-type(3)' in sel else 'sheet:选择共同素材'
  return {'预览':'modal:共同照片','添加照片':'sheet:选择共同素材','添加文字':'focus:这一页的想法','添加贴纸':'sheet:选择贴纸','保留草稿换模板':'stash','完成这一页':'page-save'}[label]
 if n==11:return {'更换照片':'sheet:选择共同素材','选择时刻 ›':'sheet:选择共同素材','添加一句话':'sheet:一句话','完成这一页 ♡':'page-save','保留草稿换模板':'stash'}[label]
 if n==12:return {'工坊作品':'sheet:选择共同素材','宠物成长':'tab','换内容':'sheet:选择共同素材','换照片':'sheet:选择共同素材','添加说明':'focus:成长说明','完成这一页':'page-save','保留草稿换模板':'stash'}[label]
 if n==13:
  if label=='保存排列':return 'structure-save'
  if label=='新增章节':return 'sheet:章节'
  return 'sheet:'+label.split('「')[1].rstrip('」')+(' · 章节操作' if label.startswith('章节') else ' · 页面操作')
 if n in [16,20]:return 'bookmark'
 if n==17:return 'sheet:我的书签'
 if n==18:return 'pressed'
 if n==19:return 'supplement' if label=='放进回忆书' else 'pressed'
 if n==21:return {'修改书名':'sheet:书名','归档回忆册':'archive','删除这本回忆册':'modal:确定删除《共同测试册》？','导出这本回忆册':'export'}[label]
 raise AssertionError((page,label,'missing contract'))

def books(p):return p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-books"))')
def clean_read(s):
 value=json.loads(s)
 if 'dujia-prototype-books' in value:
  rows=json.loads(value['dujia-prototype-books'])
  for b in rows:b.pop('updatedAt',None);b.pop('lastPage',None)
  value['dujia-prototype-books']=rows
 return value

def control(p,page,v,kind):
 from urllib.parse import urlparse,parse_qs
 seed(p,page);b=p.locator(v['selector']);expect(b).to_be_visible();expect(b).to_be_enabled();before=store(p);old=books(p);n=int(page[-2:])
 if kind=='input':
  initial=b.input_value();limit=b.get_attribute('maxlength');text='新文字' if not limit else '长'*int(limit)
  b.fill(text);expect(b).to_have_value(text);expect(b).to_be_focused();assert store(p)==before;return
 if kind=='file':
  from io import BytesIO
  from PIL import Image
  out=BytesIO();Image.new('RGB',(30,40),'pink').save(out,format='PNG');b.set_input_files(dict(name='book-control.png',mimeType='image/png',buffer=out.getvalue()));expect(p.locator('.photo-label')).to_have_text('♥ 已附上照片 ♥');expect(p.locator('.book-supplement-preview')).to_be_visible();assert store(p)==before;return
 if kind=='export':
  with p.expect_download() as info:b.click()
  d=info.value;assert d.suggested_filename=='共同测试册.json';val=json.loads(Path(d.path()).read_text(encoding='utf-8'));assert val['format']=='dujia-book-v1' and val['book']['id']=='book-state';assert store(p)==before;return
 if kind=='create':p.locator('.book-name').fill('初始控件测试册')
 if kind=='supplement':p.locator('.message').fill('初始控件真实补页')
 b.click()
 if kind.startswith('route:'):
  wanted=kind.split(':',1)[1];dest=wanted.split('?')[0];p.wait_for_url('**/'+dest+'.html*');expected=parse_qs(wanted.partition('?')[2]);actual=parse_qs(urlparse(p.url).query)
  for key,val in expected.items():assert actual.get(key)==val,(wanted,p.url)
  assert clean_read(store(p))==clean_read(before);return
 if kind.startswith(('sheet:','modal:')):
  expect(p.locator('dialog h2')).to_have_text(kind.split(':',1)[1]);p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);expect(b).to_be_focused()
 elif kind=='pressed':expect(b).to_have_attribute('aria-pressed','true')
 elif kind=='tab':expect(b).to_have_attribute('aria-selected','true')
 elif kind=='source-toggle':expect(p.get_by_role('button',name=v['label'],exact=True)).to_have_attribute('aria-pressed','false' if v['aria_pressed']=='true' else 'true')
 elif kind.startswith('focus:'):expect(p.get_by_role('textbox',name=kind.split(':',1)[1],exact=True)).to_be_focused()
 elif kind=='stash':
  p.wait_for_url('**/m08-p08.html*');row=p.evaluate('Object.values(JSON.parse(sessionStorage.getItem("dujia-prototype-book-editor")))[0]');assert row['bookId']=='book-state' and row['data']['id']=='page-state'
 elif kind=='create':
  p.wait_for_url('**/m08-p05.html*');new=books(p);assert len(new)==len(old)+1 and new[0]['name']=='初始控件测试册' and new[0]['status']=='draft';return
 elif kind=='theme-save':p.wait_for_url('**/m08-p06.html*');assert books(p)[0]['theme']==old[0]['theme'];return
 elif kind=='select-save':p.wait_for_url('**/m08-p07.html*');assert books(p)[0]['selected']==[dict(kind='pet',id='audit-pet:audit-story')];return
 elif kind=='skip':p.wait_for_url('**/m08-p13.html*');assert books(p)[0]['skipped']==[dict(kind='diary',id='audit-diary')];return
 elif kind=='page-save':p.wait_for_url('**/m08-p13.html*');new=books(p);assert len(new[0]['pages'])==3 and new[0]['pages'][0]['id']=='page-state' and new[0]['pages'][0]['source']==old[0]['pages'][0]['source'];return
 elif kind=='structure-save':p.wait_for_url('**/m08-p14.html*');new=books(p);assert new[0]['pages']==old[0]['pages'] and new[0]['chapters']==old[0]['chapters'];return
 elif kind=='bookmark':expect(p.locator('.prototype-toast')).to_contain_text('书签已更新');assert books(p)[0]['bookmarks']==['page-second'];expect(b).to_have_attribute('aria-pressed','true');return
 elif kind=='supplement':p.wait_for_url('**/m08-p20.html*');row=books(p)[0]['pages'][1]['supplements'];assert len(row)==1 and row[0]['text']=='初始控件真实补页' and row[0]['author']=='小满';return
 elif kind=='archive':expect(p.locator('.prototype-toast')).to_contain_text('已归档');assert books(p)[0]['archived'];expect(b).to_have_text('取消归档回忆册');return
 else:raise AssertionError(kind)
 assert store(p)==before

def main():
 files=source();inventory=[];rows=[]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for i in range(1,22):
   page=f'm08-p{i:02}';c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');c.add_init_script(INIT);p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   seed(p,page);assert not errors,errors;controls=[v for v in p.evaluate(OBSERVE)['controls'] if v['visible'] and not v['disabled']];inventory.append(dict(page=page,effective=p.url,controls=controls));print(page,len(controls),flush=True);c.close()
  if '--inventory' not in sys.argv:
   for entry in inventory:
    for v in entry['controls']:
     c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));kind=contract(entry['page'],v)
     try:control(p,entry['page'],v,kind);assert not errors;row=dict(passed=True)
     except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1600:])
     row.update(page=entry['page'],selector=v['selector'],label=v['label'],contract=kind,errors=errors,effective=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+entry['page']+' '+v['label'].replace('\n',' '),flush=True);c.close()
  b.close()
 assert files==source();(OUT/('book-control-inventory.json' if '--inventory' in sys.argv else 'book-controls-results.json')).write_text(json.dumps(dict(files=files,inventory=inventory,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
