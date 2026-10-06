from pathlib import Path
from io import BytesIO
import json,sys,traceback
from PIL import Image
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,go,value,fail,fixture,records

OUT=Path(__file__).resolve().parent/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current')
def image_file():
 out=BytesIO();Image.new('RGB',(120,80),(210,145,80)).save(out,format='PNG');return {'name':'book-photo.png','mimeType':'image/png','buffer':out.getvalue()}
def extended_seed(p):
 seed(p,books=[fixture()],records=records())
 image=p.evaluate("()=>{const c=document.createElement('canvas');c.width=80;c.height=100;const x=c.getContext('2d');x.fillStyle='#a04e70';x.fillRect(0,0,80,100);return c.toDataURL();}")
 p.evaluate('''image=>{const rows=JSON.parse(localStorage.getItem('dujia-prototype-records'));rows.push({id:'photo-state',type:'photo',title:'共同照片',body:'一起看晚霞',date:'2026-10-04',visibility:'shared',status:'published',image});localStorage.setItem('dujia-prototype-records',JSON.stringify(rows));localStorage.setItem('dujia-prototype-moments',JSON.stringify([{id:'moment-state',name:'第一次旅行',story:'海边的风',date:'2026-10-04',visibility:'shared',cover:image}]));localStorage.setItem('dujia-prototype-works',JSON.stringify([{id:'work-state',name:'我们的手作',story:'实际作品故事',sourceKind:'free',type:'comic',sourceIds:[],status:'ready',createdAt:1791072000000}]));localStorage.setItem('dujia-prototype-pet',JSON.stringify({id:'pet-state',name:'云朵',kind:'小猫',status:'active',logs:[{id:'pet-story',type:'note',text:'小猫的实际成长',date:'2026-10-04',story:true,actor:'小满'}]}));}''',image)

def photo_edit_crop(p):
 extended_seed(p);go(p,10,'?id=book-state&source=photo-state&kind=photo&template=照片故事')
 expect(p.get_by_label('书页标题',exact=True)).to_have_value('共同照片')
 p.locator('.crop').first.click();p.get_by_role('button',name='裁剪这张照片',exact=True).click();p.get_by_label('缩放',exact=True).fill('1.5');p.get_by_role('button',name='应用裁剪',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0)
 p.locator('[data-tool=添加贴纸]').click();p.get_by_role('button',name='🌸',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);p.get_by_label('这一页的想法',exact=True).fill('照片旁的实际说明');p.locator('.done').click();p.wait_for_url('**/m08-p13.html*')
 page=value(p)[0]['pages'][-1];assert page['photos'][0]['crop']['zoom']==1.5 and page['stickers']==['🌸'] and page['body']=='照片旁的实际说明'
 go(p,16,'?id=book-state&page='+page['id']);expect(p.locator('.book-reading-images img')).to_have_count(1);expect(p.locator('.copy')).to_contain_text('照片旁的实际说明')

def moment_work_pet(p):
 extended_seed(p)
 for kind,source,template,n,expected in [('moment','moment-state','重要时刻',11,'第一次旅行'),('work','work-state','工坊作品',12,'我们的手作'),('pet','pet-state:pet-story','宠物成长',12,'小猫的实际成长')]:
  go(p,8,'?id=book-state&source='+source+'&kind='+kind);p.locator('[data-template="'+template+'"]').click();p.locator('.use').click();p.wait_for_url('**/m08-p'+str(n)+'.html*');expect(p.locator('.screen')).to_contain_text(expected);p.locator('.done').click();p.wait_for_url('**/m08-p13.html*');page=value(p)[0]['pages'][-1];assert page['template']==template and page['source']['kind']==kind
 assert len(value(p)[0]['pages'])==4

def supplements_tools(p):
 extended_seed(p);go(p,16,'?id=book-state&page=page-state');p.get_by_role('button',name='阅读工具',exact=True).click();p.wait_for_url('**/m08-p17.html*');p.get_by_role('button',name='添加补页',exact=False).click();p.wait_for_url('**/m08-p18.html*');p.locator('.next').click();p.wait_for_url('**/m08-p19.html*');p.get_by_label('补页文字',exact=True).fill('这是我的真实补页');fail(p,'book-supplement');p.locator('.submit').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');expect(p.get_by_label('补页文字',exact=True)).to_have_value('这是我的真实补页');p.locator('.submit').click();p.wait_for_url('**/m08-p20.html*');expect(p.locator('.right-copy')).to_contain_text('这是我的真实补页')
 go(p,18,'?id=book-state&page=page-state');p.locator('[data-kind=送一个表情]').click();p.locator('.next').click();p.wait_for_url('**/m08-p19.html*');p.get_by_role('button',name='星星',exact=True).click();p.locator('.submit').click();p.wait_for_url('**/m08-p20.html*');expect(p.locator('.right-copy')).to_contain_text('⭐')
 go(p,18,'?id=book-state&page=page-state');p.locator('[data-kind=附上一张照片]').click();p.locator('.next').click();p.wait_for_url('**/m08-p19.html*');expect(p.locator('input[type=file]')).to_be_enabled();p.locator('input[type=file]').set_input_files(image_file());expect(p.locator('.photo-label')).to_contain_text('已附上照片');p.locator('.submit').click();p.wait_for_url('**/m08-p20.html*');expect(p.locator('.book-supplement-images img')).to_have_count(1);assert len(value(p)[0]['pages'][0]['supplements'])==3

def upload_dirty_failure(p):
 extended_seed(p);go(p,19,'?id=book-state&page=page-state&kind=附上一张照片');file=p.locator('input[type=file]');expect(file).to_be_enabled();fail(p,'book-image');file.set_input_files(image_file());expect(p.locator('.prototype-toast')).to_contain_text('图片读取失败');assert not value(p)[0]['pages'][0].get('supplements');file.set_input_files(image_file());expect(p.locator('.photo-label')).to_contain_text('已附上照片');p.locator('.back').click();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('.book-supplement-preview img')).to_have_count(1);fail(p,'book-supplement');p.locator('.submit').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');assert not value(p)[0]['pages'][0].get('supplements');p.locator('.submit').click();p.wait_for_url('**/m08-p20.html*');assert value(p)[0]['pages'][0]['supplements'][0]['image'].startswith('data:image/png')

def missing_specialist_source(p):
 seed(p,books=[fixture()],records=records());go(p,12,'?id=book-state&template=工坊作品');p.locator('.done').click();expect(p.locator('.prototype-toast')).to_contain_text('请先选择');assert len(value(p)[0]['pages'])==1;p.locator('[data-action=换内容]').click();expect(p.get_by_role('button',name='去童话工坊',exact=True)).to_be_visible();p.keyboard.press('Escape');expect(p.locator('dialog[open]')).to_have_count(0);extended_seed(p);p.evaluate("()=>{const b=JSON.parse(localStorage.getItem('dujia-prototype-books'));b[0].pages.push({id:'switch-work',chapterId:'chapter-state',template:'工坊作品',source:{kind:'work',id:'work-state'}});localStorage.setItem('dujia-prototype-books',JSON.stringify(b));}");go(p,12,'?id=book-state&page=switch-work&template=宠物成长');p.locator('.done').click();expect(p.locator('.prototype-toast')).to_contain_text('请先选择');assert value(p)[0]['pages'][-1]['template']=='工坊作品' 

def photo_private_export(p):
 extended_seed(p);p.evaluate('''()=>{const books=JSON.parse(localStorage.getItem('dujia-prototype-books'));books[0].pages.push({id:'photo-private',chapterId:'chapter-state',template:'照片故事',source:{kind:'photo',id:'photo-state'},photos:[{source:{kind:'photo',id:'photo-state'},crop:{x:50,y:50,zoom:1}}]});const records=JSON.parse(localStorage.getItem('dujia-prototype-records'));records.find(v=>v.id==='photo-state').visibility='private';localStorage.setItem('dujia-prototype-books',JSON.stringify(books));localStorage.setItem('dujia-prototype-records',JSON.stringify(records));}''');go(p,16,'?id=book-state&page=photo-private');expect(p.locator('.copy')).to_contain_text('关联内容已不可见');expect(p.locator('.book-reading-images img')).to_have_count(0);dump=p.evaluate("JSON.stringify(PrototypeBooks.exported('book-state'))");assert 'data:image/' not in dump and '一起看晚霞' not in dump

def no_edit_back_and_reply_gate(p):
 extended_seed(p);go(p,10,'?id=book-state&source=photo-state&kind=photo&template=照片故事');p.locator('.back').click();p.wait_for_url('**/m08-p08.html*');expect(p.locator('dialog[open]')).to_have_count(0);p.evaluate("localStorage.setItem('dujia-privacy',JSON.stringify({replies:false}))");go(p,18,'?id=book-state&page=page-state');expect(p.locator('.next')).to_be_disabled();go(p,19,'?id=book-state&page=page-state');expect(p.locator('.submit')).to_be_disabled();result=p.evaluate("()=>{try{PrototypeBooks.supplement('book-state','page-state',{kind:'写几句话',text:'禁止写入'});return 'saved';}catch(e){return e.message;}}");assert '回应已关闭' in result and not value(p)[0]['pages'][0].get('supplements')

rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'photo-actual-select-crop-sticker-save-read':photo_edit_crop,'three-specialist-templates-save-typed-source':moment_work_pet,'reading-tools-three-supplements-failure-retry':supplements_tools,'upload-decode-failure-dirty-save-retry':upload_dirty_failure,'missing-specialist-source-no-fake-page':missing_specialist_source,'photo-private-read-export-redacted':photo_private_export,'no-edit-back-reply-privacy-gate':no_edit_back_and_reply_gate}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(5000);p.set_default_navigation_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-2300:]}
  row.update(errors=errors,final_url=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
OUT.mkdir(parents=True,exist_ok=True);(OUT/'book-extended-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['passed'] for v in rows) else 1)
