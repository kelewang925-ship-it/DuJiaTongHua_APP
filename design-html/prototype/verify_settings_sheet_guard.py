"""Settings shared editable Sheets: real unsaved closes and clean commits."""
import sys,json,traceback
from playwright.sync_api import sync_playwright,expect
from verify_settings_controls import seed,store,source,ROOT
OUT=ROOT/'evidence'/('baseline'if '--baseline'in sys.argv else'current')
def dirty(p,exit):
    seed(p,'m06-p12');before=store(p);p.locator('.feedback').click();p.get_by_role('textbox',name='意见反馈',exact=True).fill('尚未保存的反馈内容')
    def close():
        if exit=='cancel':p.get_by_role('button',name='取消',exact=True).click()
        elif exit=='escape':p.keyboard.press('Escape')
        elif exit=='back':p.go_back()
        else:
            r=p.locator('.prototype-sheet-handle').bounding_box();p.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2);p.mouse.down();p.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2+110,steps=8);p.mouse.up()
    close();expect(p.get_by_text('是否放弃当前修改？',exact=True)).to_be_visible();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.get_by_role('textbox',name='意见反馈',exact=True)).to_have_value('尚未保存的反馈内容');assert store(p)==before;close();p.get_by_role('button',name='放弃修改',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert store(p)==before;expect(p.locator('.feedback')).to_be_focused()
def save(p):
    seed(p,'m06-p12');p.locator('.feedback').click();p.get_by_role('textbox',name='意见反馈',exact=True).fill('失败重试仍保留');p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","settings-feedback")');p.get_by_role('button',name='保存反馈',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');expect(p.get_by_role('textbox',name='意见反馈',exact=True)).to_have_value('失败重试仍保留');p.get_by_role('button',name='保存反馈',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert p.evaluate('JSON.parse(localStorage.getItem("dujia-feedback-draft"))')=='失败重试仍保留';p.locator('.back').click();p.wait_for_url('**/m06-p01.html');expect(p.locator('dialog')).to_have_count(0)
def field(p,kind):
    page,button,label,value={'tag':('m06-p05','.plus','标签名称','未保存标签'),'world':('m06-p03','.nick','共同昵称','未保存共同昵称'),'phone':('m06-p08','.phone','手机号','13912345678'),'code':('m06-p08','.two-factor','演示验证码 284631','123456')}[kind]
    seed(p,page);before=store(p);p.locator(button).click();p.get_by_role('textbox',name=label,exact=True).fill(value);p.keyboard.press('Escape');expect(p.get_by_text('是否放弃当前修改？',exact=True)).to_be_visible();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.get_by_role('textbox',name=label,exact=True)).to_have_value(value);p.keyboard.press('Escape');p.get_by_role('button',name='放弃修改',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert store(p)==before
def appearance(p):
    seed(p,'m06-p07');before=store(p);p.locator('.display').click();p.get_by_label('动效',exact=True).select_option('reduce');p.keyboard.press('Escape');expect(p.get_by_text('是否放弃当前修改？',exact=True)).to_be_visible();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.get_by_label('动效',exact=True)).to_have_value('reduce');assert store(p)==before;p.get_by_role('button',name='保存',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-preferences")).reduceMotion')
def update(p):
    seed(p,'m06-p12');before=store(p);p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","settings-update")');p.locator('.updates').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.updates')).to_be_enabled();expect(p.locator('.updates')).to_be_focused();assert store(p)==before;p.locator('.updates').click();expect(p.locator('dialog h2')).to_have_text('版本信息');p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.updates')).to_be_focused();assert store(p)==before
files=source();rows=[];cases=[('feedback-dirty-'+k,lambda p,k=k:dirty(p,k))for k in ['cancel','escape','back','drag']]
if '--baseline'not in sys.argv:cases+=[('feedback-failure-retry-clean-commit',save)]+[(k+'-sheet-dirty',lambda p,k=k:field(p,k))for k in ['tag','world','phone','code']]+[('appearance-select-dirty-save',appearance),('update-failure-retry-trigger-focus',update)]
with sync_playwright()as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,run in cases:
        c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p);assert not errors;row=dict(passed=True)
        except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
        row.update(case=name,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
    b.close()
assert files==source();OUT.mkdir(parents=True,exist_ok=True);(OUT/'settings-sheet-guard-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed']for r in rows)else 1)
