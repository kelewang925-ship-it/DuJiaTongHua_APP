from pathlib import Path
import json,traceback,sys
from playwright.sync_api import sync_playwright,expect
BASE='http://127.0.0.1:8765/'
OUT=Path(__file__).resolve().parent/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current')
def form(p):
 p.goto(BASE+'prototype/components.html');p.get_by_label('昵称',exact=True).fill('');p.get_by_role('button',name='演示保存',exact=True).click();expect(p.get_by_text('请填写昵称',exact=True)).to_be_visible();p.get_by_label('昵称',exact=True).fill('星星');p.get_by_role('button',name='演示保存',exact=True).click();expect(p.get_by_role('button',name='保存中…',exact=True)).to_be_disabled();expect(p.locator('#saved')).to_have_text('已保存：星星');p.get_by_role('button',name='旅行标签',exact=True).click();expect(p.get_by_role('button',name='旅行标签',exact=True)).to_have_attribute('aria-pressed','true')
def overlays(p):
 p.goto(BASE+'prototype/components.html');trigger=p.get_by_role('button',name='确认弹窗',exact=True);trigger.click();expect(p.locator('dialog[open]')).to_be_visible();p.keyboard.press('Escape');expect(p.locator('dialog[open]')).to_have_count(0);expect(trigger).to_be_focused();p.get_by_role('button',name='底部选择器',exact=True).click();p.go_back();expect(p.locator('dialog[open]')).to_have_count(0);assert p.url.endswith('components.html')
def layout(p,width):
 p.goto(BASE+'prototype/components.html');p.evaluate('document.fonts.ready');p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")');metrics=p.evaluate('''()=>({width:document.documentElement.scrollWidth,buttons:[...document.querySelectorAll('button')].filter(e=>!e.disabled&&e.getClientRects().length).map(e=>{e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {label:e.textContent,width:r.width,height:r.height,hit:hit===e||e.contains(hit)}})})''');assert metrics['width']==width and all(v['width']>=44 and v['height']>=44 and v['hit'] for v in metrics['buttons']),metrics;assert p.get_by_role('progressbar',name='生成进度').get_attribute('value')=='60';p.screenshot(path=str(OUT/f'components-{width}.png'),full_page=True)
def recovery(p):
 p.goto(BASE+'prototype/components.html');p.get_by_role('button',name='重新加载',exact=True).click();expect(p.get_by_text('重新加载中…',exact=True)).to_be_visible();expect(p.get_by_text('重新加载成功',exact=True)).to_be_visible();p.get_by_role('button',name='写第一篇日记',exact=True).click();p.wait_for_url('**/m03-p05.html');expect(p.locator('[name=title]')).to_have_value('')
def missing(p,width):
 p.goto(BASE+'prototype/review.html');p.evaluate("localStorage.setItem('dujia-prototype-moments','[]');localStorage.setItem('dujia-prototype-records','[]')");p.goto(BASE+'pages/m04-p03.html?id=gone');button=p.get_by_role('button',name='返回时刻册',exact=True);expect(p.locator('.prototype-component-state[role=alert]')).to_be_visible();button.scroll_into_view_if_needed();box=button.bounding_box();assert box['height']>=44 and box['width']>=44;assert p.evaluate('document.documentElement.scrollWidth')==width;p.screenshot(path=str(OUT/f'component-missing-moment-{width}.png'),full_page=True);button.click();p.wait_for_url('**/m04-p02.html')
cases=[('form-validation-save-and-tag',390,form),('native-modal-sheet-back-focus',390,overlays)]+[('layout-'+str(w),w,lambda p,w=w:layout(p,w)) for w in [320,375,390,414,430]]
if '--baseline' not in sys.argv:cases += [('error-retry-and-empty-create',390,recovery)]+[('missing-moment-'+str(w),w,lambda p,w=w:missing(p,w)) for w in [320,375,390,414,430]]
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,width,run in cases:
  c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row=dict(case=name,passed=True)
  except Exception:row=dict(case=name,passed=False,failure=traceback.format_exc()[-1800:])
  row.update(errors=errors,url=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
(OUT/'component-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
