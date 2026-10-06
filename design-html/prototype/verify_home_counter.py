"""Home day count uses calendar data rather than design placeholders."""
import json,traceback,sys
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import ROOT,BASE,source,store
OUT=ROOT/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current');files=source();rows=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for case in ['fresh-bound','explicit-met','unbound','bound-undated','invalid-met-fallback','future-met-clamped']:
  c=b.new_context(viewport=dict(width=390,height=844),timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(3500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:
   p.goto(BASE+'prototype/review.html');pair=dict(bound=case!='unbound',partner='阿舟',profile={})
   if case in ['fresh-bound','invalid-met-fallback']:pair['acceptedAt']=1791217800000
   if case=='explicit-met':pair['profile']['met']='2026-10-05';pair['acceptedAt']=1791217800000
   if case=='invalid-met-fallback':pair['profile']['met']='2026-02-30'
   if case=='future-met-clamped':pair['profile']['met']='2026-10-07'
   records=[dict(id='counter-diary',type='diary',title='现有日记',body='保持现有内容',visibility='shared',status='published',createdAt=1791217800000)]
   p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");localStorage.setItem("dujia-prototype-relationship",JSON.stringify(d.pair));localStorage.setItem("dujia-prototype-records",JSON.stringify(d.records));}',dict(pair=pair,records=records));before=store(p);p.goto(BASE+'pages/m03-p01.html');p.wait_for_url('**/m03-p02.html')
   expected='1' if case=='explicit-met' else '—' if case in ['unbound','bound-undated'] else '0';label='我们已经一起走过' if case in ['explicit-met','future-met-clamped'] else '我们已关联' if case in ['fresh-bound','invalid-met-fallback'] else '等待一起记录' if case=='unbound' else '相识日期待补充';expect(p.locator('.hero-copy strong')).to_have_text(expected);expect(p.locator('.hero-copy p').nth(0)).to_have_text(label);assert store(p)==before;assert not errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1400:])
  row.update(case=case,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+case,flush=True);c.close()
 b.close()
assert files==source();(OUT/'home-counter-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(v['passed']for v in rows)else 1)
