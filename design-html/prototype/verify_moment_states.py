from pathlib import Path
import argparse,base64,json
from playwright.sync_api import sync_playwright,expect
parser=argparse.ArgumentParser();parser.add_argument('--case');args=parser.parse_args();OUT=Path(__file__).resolve().parent/'evidence/current';URL='http://127.0.0.1:8765/pages/'
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jB2kAAAAASUVORK5CYII=')
def go(p,id):p.goto(URL+id+'.html')
def seed(p):
 go(p,'m04-p01');p.evaluate('localStorage.setItem("dujia-prototype-moments",JSON.stringify([{id:"moment-proof",name:"星空时刻",date:"2026-01-03",type:"旅行",story:"今天的星星",related:[],cover:null,comments:[]}]))');p.goto(URL+'m04-p04.html?id=moment-proof')
def fail(p,key):p.evaluate('(k)=>sessionStorage.setItem("dujia-prototype-fail-next",k)',key)
def cover_quota_delete(p):
 seed(p);p.locator('#cover-file').set_input_files({'name':'bad.png','mimeType':'image/png','buffer':b'bad'});expect(p.locator('.prototype-toast')).to_contain_text('无法打开');assert p.locator('#cover-preview').is_hidden();p.locator('#cover-file').set_input_files({'name':'cover.png','mimeType':'image/png','buffer':PNG});expect(p.locator('#cover-preview')).to_be_visible();p.locator('[name=name]').fill('保留封面的时刻')
 p.evaluate('()=>{window.saveSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==="dujia-prototype-moments")throw new DOMException("full","QuotaExceededError");return window.saveSet.call(this,k,v)}}');p.locator('.submit').click();expect(p.locator('.prototype-toast')).to_contain_text('空间不足');assert p.locator('[name=name]').input_value()=='保留封面的时刻';p.evaluate('()=>{Storage.prototype.setItem=window.saveSet}');p.locator('.submit').click();p.wait_for_url('**/m04-p03.html?id=*');p.reload();assert p.locator('.prototype-moment-cover img').evaluate('e=>e.complete&&e.naturalWidth>0');assert p.locator('.prototype-moment-cover img').evaluate('e=>e.getBoundingClientRect().bottom<=e.parentElement.getBoundingClientRect().bottom+1'),'Cover must stay inside its frame';fail(p,'moment-delete');p.locator('#more').click();p.get_by_role('button',name='删除重要时刻',exact=True).click();p.get_by_role('button',name='确认删除',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-moments")).length')==1
def date_input(p):
 seed(p);original=p.locator('[name=date]').input_value();p.locator('[name=date]').click();p.locator('dialog input[type=date]').fill('2026-02-04');p.keyboard.press('Escape');expect(p.locator('dialog[open]')).to_have_count(0);assert p.locator('[name=date]').input_value()==original;p.locator('[name=date]').click();p.locator('dialog input[type=date]').fill('2026-02-04');p.get_by_role('button',name='使用这个日期',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);expect(p.locator('[name=date]')).to_have_value('2026-02-04');p.locator('[name=story]').fill('很长的故事'*100);assert len(p.locator('[name=story]').input_value())==200;p.locator('.types label').filter(has_text='节日').click();p.locator('.submit').click();p.wait_for_url('**/m04-p03.html?id=*');expect(p.locator('.date')).to_have_text('2026-02-04');p.get_by_role('button',name='编辑时刻',exact=True).click();p.wait_for_url('**/m04-p04.html?id=*');assert p.locator('input[value=节日]').is_checked()
def aggregation(p):
 go(p,'m04-p16');p.evaluate('localStorage.setItem("dujia-prototype-moments","[]");localStorage.setItem("dujia-prototype-records",JSON.stringify([{id:"shared",type:"diary",visibility:"shared",status:"published",title:"共同日记",body:"正文",comments:[{id:"reply1",author:"阿舟",text:"共同的回应",createdAt:1}],createdAt:1},{id:"private",type:"diary",visibility:"private",status:"published",title:"私密",comments:[{id:"reply2",author:"小满",text:"不该聚合的回应",createdAt:2}]}]))');go(p,'m04-p16');expect(p.locator('[aria-label=留言]')).to_contain_text('共同的回应');expect(p.get_by_text('不该聚合的回应',exact=False)).to_have_count(0);p.get_by_role('button',name='查看原记录',exact=False).click();p.wait_for_url('**/m03-p08.html?id=shared');go(p,'m04-p16');expect(p.get_by_role('button',name='查看原记录 · 已读',exact=True)).to_be_visible()
def missing(p):
 go(p,'m04-p03');p.goto(URL+'m04-p03.html?id=gone');expect(p.get_by_text('这个时刻已经不在了',exact=True)).to_be_visible();p.locator('.prototype-moment-state button').click();p.wait_for_url('**/m04-p02.html');expect(p.get_by_role('button',name='新建重要时刻',exact=True)).to_be_visible()
def empty_choose(p):
 go(p,'m04-p02');p.evaluate('localStorage.setItem("dujia-prototype-moments","[]");localStorage.setItem("dujia-prototype-records","[]")');p.reload();p.locator('#from-records').click();p.wait_for_url('**/m04-p04.html?choose=1');p.get_by_role('button',name='去写日记',exact=True).click();p.wait_for_url('**/m03-p05.html')
def list_failure(p):
 seed(p);fail(p,'moment-load');go(p,'m04-p01');expect(p.get_by_text('时刻册暂时打不开',exact=True)).to_be_visible();p.get_by_role('button',name='重试加载时刻册',exact=True).click();expect(p.locator('.cards')).to_contain_text('星空时刻');p.get_by_role('button',name='刷新时刻册',exact=True).click();expect(p.locator('.cards')).to_contain_text('星空时刻')
import hashlib
DEMO=Path(__file__).resolve().parents[1]
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
source_files=source()
results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'cover-quota-delete-recovery':cover_quota_delete,'date-long-story-type':date_input,'reply-aggregation-privacy-read':aggregation,'missing-moment':missing,'empty-related-create-entry':empty_choose,'list-load-refresh-retry':list_failure}.items():
  if args.case and name!=args.case:continue
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':repr(e)[:1500]}
  row.update(errors=errors,final_url=p.url);results.append(row);p.screenshot(path=str(OUT/f'moment-state-{name}.png'),full_page=True);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
assert source_files==source(), 'Source changed during moment regression'
(OUT/'moment-state-source.json').write_text(json.dumps({'files':source_files},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/('moment-state-results.json' if not args.case else 'moment-state-'+args.case+'.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');raise SystemExit(0 if all(r['passed'] for r in results) else 1)
