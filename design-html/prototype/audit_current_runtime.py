"""Current runtime inventory. Baseline files and user browser data are never changed."""
from pathlib import Path
import json,re,hashlib,traceback
from playwright.sync_api import sync_playwright
from audit_runtime import INIT,OBSERVE
from book_test_helpers import fixture

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'prototype/evidence/current'
IMAGE='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="80" height="100"><rect width="80" height="100" fill="pink"/></svg>'
def data(populated):
 result={'dujia-profile':dict(nickname='小满'),'dujia-prototype-session':dict(loggedIn=False),'dujia-prototype-relationship':dict(bound=populated,partner='阿舟',profile=dict(nickname='共同小屋',met='2026-01-01'))}
 for kind in ['records','moments','anniversaries','capsules','works','books']:result['dujia-prototype-'+kind]=[]
 if not populated:return result
 result['dujia-prototype-records']=[dict(id='audit-diary',type='diary',title='共同日记',body='真正可编辑的共同正文',date='2026-10-04',status='published',visibility='shared',author='小满',tags=['旅行'],comments=[]),dict(id='audit-private',type='diary',title='自己的日记',body='独立私密正文',date='2026-10-04',status='published',visibility='private',author='小满',tags=[],comments=[]),dict(id='audit-photo',type='photo',title='共同照片',caption='共同照片说明',date='2026-10-04',status='published',visibility='shared',author='小满',image=IMAGE,tags=[],comments=[])]
 result['dujia-prototype-moments']=[dict(id='audit-moment',name='共同重要时刻',story='真实时刻正文',date='2026-10-04',type='旅行',sourceIds=['audit-diary'],comments=[],visibility='shared')]
 result['dujia-prototype-anniversaries']=[dict(id='audit-anniversary',name='未来的纪念日',date='2026-12-24',repeat='每年',type='恋爱',reminder=True,momentId='audit-moment'),dict(id='audit-today',name='今天的纪念日',date='2026-10-05',repeat='每年',type='恋爱',reminder=True)]
 result['dujia-prototype-capsules']=[dict(id='audit-opened',name='已经打开的信',message='实际打开的内容',opening='2026-10-05',status='opened',reminder=True),dict(id='audit-sealed',name='未来的信',message='仍然封存的内容',opening='2026-12-24',status='sealed',reminder=True)]
 result['dujia-prototype-works']=[dict(id='audit-work',name='实际工坊作品',story='一起看星星。一起许愿。',type='comic',sourceKind='free',sourceIds=[],style='暖暖水彩',mode='温柔叙事',mood='温柔手帐',status='ready',createdAt=1791158400000,completedAt=1791158400000)]
 result['dujia-prototype-pet']=dict(id='audit-pet',name='团团',kind='小狗',status='active',adoptedDate='2026-09-01',energy=82,satiety=76,mood=70,affinity=160,food=[12,5,1],gifts=1,coins=50,stars=30,owned=['小花围巾'],outfit=None,room={},claims=[],logs=[dict(id='audit-story',type='note',text='实际成长故事',actor='小满',date='2026-10-04',at=1791158400000)],care=True,settings=dict(reminder=True,time='20:30',notice=True,stories=True))
 book=fixture();book['pages'][0]['source']['id']='audit-diary';book['selected'][0]['id']='audit-diary';result['dujia-prototype-books']=[book]
 return result
def query(id,populated):
 if not populated:return ''
 routes={'m03-p05':'audit-diary','m03-p07':'audit-private','m03-p08':'audit-diary','m03-p11':'audit-photo','m03-p12':'audit-photo','m04-p03':'audit-moment','m04-p04':'audit-moment','m04-p09':'audit-anniversary','m04-p10':'audit-anniversary','m04-p11':'audit-today','m04-p14':'audit-opened','m04-p15':'audit-sealed'}
 if id in routes:return '?id='+routes[id]
 if id.startswith('m05-') and id not in ['m05-p01','m05-p02','m05-p09']:return '?id=audit-work'
 if id=='m07-p19':return '?id=audit-story'
 if id.startswith('m08-') and int(id[-2:])>=5:return '?id=book-state'+('&page=page-state' if int(id[-2:]) in [9,10,11,12,16,17,18,19,20] else '')
 return ''
def clean(value):return str(value or '').replace('|','／').replace('\r',' ').replace('\n',' ').strip()
def main():
 manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));rows=[];assert len(manifest)==114
 source_files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in list((ROOT/'custom').glob('*.html'))+list((ROOT/'assets').glob('prototype-*.*'))}
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for populated in [False,True]:
   scenario='populated' if populated else 'empty';context=browser.new_context(viewport={'width':390,'height':844});context.add_init_script(INIT)
   for number,entry in enumerate(manifest):
    p=context.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));requested='http://127.0.0.1:8765/pages/'+entry['id']+'.html'+query(entry['id'],populated)
    try:
     p.goto('http://127.0.0.1:8765/prototype/review.html');p.evaluate("data=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem('dujia-prototype-today','2026-10-06');for(const[key,value] of Object.entries(data))localStorage.setItem(key,JSON.stringify(value));}",data(populated));p.goto(requested)
     for attempt in range(6):
      try:
       p.wait_for_load_state('domcontentloaded');p.evaluate('document.fonts.ready');before=p.url;p.wait_for_timeout(650)
       if p.url!=before:continue
       observed=p.evaluate("() => {const value=("+OBSERVE+")();value.form_handlers=Object.fromEntries([...document.forms].map(f=>[f.id||'',f.onsubmit?String(f.onsubmit):'']));return value;}")
       form_handlers=observed.pop('form_handlers');break
      except Exception as error:
       if attempt==5 or not any(text in str(error) for text in ['Execution context was destroyed','Cannot find context']):raise
     else:raise RuntimeError('Navigation did not settle for observation')
     for c in observed['controls']:
      c['direct_candidate']=bool(c['native_input'] or c['inline'] or c['href'] and c['href']!='#' or any(e['type'] in ['click','keydown','pointerdown'] for e in c['own_events']) or c['type']=='submit' and (any(e['type']=='submit' for e in c['form_events']) or any(form_handlers.values())))
      c['observed_literal_routes']=sorted(set(re.findall(r'm\d{2}-p\d{2}(?=\.html)',(c['inline'] or '')+' '+(c['href'] or ''))))
     row=dict(id=entry['id'],scenario=scenario,requested=requested,effective=p.url,page_errors=errors,observed=observed)
    except Exception:row=dict(id=entry['id'],scenario=scenario,requested=requested,effective=p.url,page_errors=errors,failure=traceback.format_exc()[-2200:])
    rows.append(row);p.close()
    if (number+1)%19==0:print(f'Observed {scenario}: {number+1}/114',flush=True)
   context.close()
  browser.close()
 assert source_files=={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in list((ROOT/'custom').glob('*.html'))+list((ROOT/'assets').glob('prototype-*.*'))}, 'Product source changed during observation'
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'current-runtime-inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 candidates=[dict(id=r['id'],scenario=r['scenario'],effective=r['effective'],label=c['label'],selector=c['selector'],global_delegate_candidate=c['has_candidate_behavior']) for r in rows for c in r.get('observed',{}).get('controls',[]) if c['visible'] and not c['disabled'] and not c['direct_candidate']]
 report=dict(requested_pages=114,observations=len(rows),controls_observed=sum(len(r.get('observed',{}).get('controls',[])) for r in rows),unbound_or_delegated_candidates=candidates,errors=[r for r in rows if r.get('failure') or r['page_errors']],redirects=[dict(id=r['id'],scenario=r['scenario'],effective=r['effective']) for r in rows if r['effective'].split('?')[0]!=r['requested'].split('?')[0]],acceptance='Observation only; callbacks and candidate routes do not prove executed behavior or acceptance.',files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in list((ROOT/'custom').glob('*.html'))+list((ROOT/'assets').glob('prototype-*.*'))})
 (OUT/'current-runtime-summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 lines=['# 当前114页运行观察','','空数据与有数据各观察一次。重定向是实际控制器条件的结果；未进入的原状态页仍需单独条件验证。绑定函数和静态出口不代表已点击或流程验收通过。','', '| 页面 | 原稿名称 | 空数据实际页 | 有数据实际页 | 可见可用控件（空／有） |','| --- | --- | --- | --- | ---: |']
 controls=['# 当前控件行为观察','','以下保留实际处理代码、原生操作和literal出口，尚待逐项执行、返回与异常验证。全局委托只作为候选，不能自动判为有效。','', '| 请求页 | 场景 | 实际页 | 控件 | 可用 | 当前处理／出口 |','| --- | --- | --- | --- | --- | --- |']
 for entry in manifest:
  pair=[next(r for r in rows if r['id']==entry['id'] and r['scenario']==s) for s in ['empty','populated']]
  counts=[sum(c['visible'] and not c['disabled'] for c in r.get('observed',{}).get('controls',[])) for r in pair]
  lines.append('| '+' | '.join(map(clean,[entry['id'],entry['title'],Path(pair[0]['effective'].split('?')[0]).stem,Path(pair[1]['effective'].split('?')[0]).stem,str(counts[0])+'／'+str(counts[1])]))+' |')
  for row in pair:
   for c in row.get('observed',{}).get('controls',[]):
    handler=c['inline'] or c['href'] or ('原生输入/选择器' if c['native_input'] else '; '.join(e['handler'] for e in c['own_events'])) or '委托候选/待复核'
    controls.append('| '+' | '.join(map(clean,[entry['id'],row['scenario'],Path(row['effective'].split('?')[0]).stem,c['label'],'可用' if c['visible'] and not c['disabled'] else '隐藏/禁用',handler[:600]]))+' |')
 (ROOT/'prototype/CURRENT_PAGES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');(ROOT/'prototype/CURRENT_CONTROL_AUDIT.md').write_text('\n'.join(controls)+'\n',encoding='utf-8')
 print(json.dumps({k:report[k] if k not in ['errors','unbound_or_delegated_candidates','redirects'] else len(report[k]) for k in ['requested_pages','observations','controls_observed','errors','unbound_or_delegated_candidates','redirects']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
