"""Read-time creation-date fallback; explicit dates and privacy remain authoritative."""
import json,traceback
from playwright.sync_api import sync_playwright
from verify_pet_controls import source,ROOT,BASE,store
files=source();rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for case in ['created-only-local-date','explicit-date-priority','undated-not-in-month','private-draft-excluded','book-view-export-resolve-created-only']:
  c=b.new_context(timezone_id='Asia/Shanghai');p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:
   p.goto(BASE+'pages/m08-p02.html');p.wait_for_function('document.querySelector(".screen").getAttribute("aria-busy")==="false"')
   record=dict(id='actual-date',type='diary',title='创建时间日记',body='真实创建时间正文',status='published',visibility='shared',createdAt=1791217800000,author='小满')
   if case=='explicit-date-priority':record['date']='2026-09-15'
   if case=='undated-not-in-month':record.pop('createdAt')
   records=[record]
   if case=='private-draft-excluded':records=[dict(record,visibility='private'),dict(record,id='draft-date',status='draft')]
   book=dict(id='date-book',name='日期测试',dates=['2026.10','2026.10'],status='published',pages=[dict(id='date-page',source=dict(kind='diary',id='actual-date'))],chapters=[],bookmarks=[])
   p.evaluate('d=>{localStorage.setItem("dujia-prototype-records",JSON.stringify(d.records));localStorage.setItem("dujia-prototype-books",JSON.stringify([d.book]));}',dict(records=records,book=book));before=store(p)
   result=p.evaluate('b=>PrototypePreferences.bookSources(b)',book)
   if case=='created-only-local-date':assert len(result)==1 and result[0]['date']=='2026-10-06'
   if case=='explicit-date-priority':assert result==[];book['dates']=['2026.09','2026.09'];result=p.evaluate('b=>PrototypePreferences.bookSources(b)',book);assert len(result)==1 and result[0]['date']=='2026-09-15'
   if case in ['undated-not-in-month','private-draft-excluded']:assert result==[]
   if case=='book-view-export-resolve-created-only':
    view=p.evaluate('b=>PrototypePreferences.bookPageView(b.pages[0],b)',book);assert not view['blocked'] and view['body']=='真实创建时间正文' and view['date']=='2026-10-06';value=p.evaluate('b=>PrototypePreferences.bookExport(b)',book);assert value['pages'][0]['body']=='真实创建时间正文'
   assert store(p)==before;assert not errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1400:])
  row.update(case=case,errors=errors);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+case,flush=True);c.close()
 b.close()
assert files==source();(ROOT/'evidence/current/book-created-date-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
