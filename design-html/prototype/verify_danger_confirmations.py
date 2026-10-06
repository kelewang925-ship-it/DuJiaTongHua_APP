"""Actual destructive dialogs/forms: shared DangerButton, safe focus and cancellation."""
import json,sys,traceback,re
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source,store
OUT=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');files=source();rows=[]
CASES=['diary','photo','moment','anniversary','capsule','work','book','chapter','page','tag','unlink','cache','record-repair','account-repair','form-discard','sheet-discard','account-delete','pet-delete']
def seed(p,case):
 d=data(True);d['dujia-prototype-session']=dict(loggedIn=True,phone='13812345678');d['dujia-prototype-tags']=[dict(id='danger-tag',name='旅行',scope='personal')];d['dujia-prototype-records'][0]['tags']=['旅行'];d['dujia-prototype-preferences']=dict(autoBackup=False,reduceMotion=True);d['dujia-prototype-anniversaries']=[dict(id='danger-ann',name='危险操作纪念日',date='2026-12-24',repeat=True,enabled=True,reminderDays=3)];d['dujia-prototype-pet']['status']='active'
 p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));}',d)
 if case=='record-repair':p.evaluate('()=>{const r=JSON.parse(localStorage.getItem("dujia-prototype-records"));r.push(null);localStorage.setItem("dujia-prototype-records",JSON.stringify(r));}')
 if case=='account-repair':p.evaluate('localStorage.setItem("dujia-profile","null")')
 route={'diary':'m03-p08.html?id=audit-diary','photo':'m03-p12.html?id=audit-photo','moment':'m04-p03.html?id=audit-moment','anniversary':'m04-p10.html?id=danger-ann','capsule':'m04-p14.html?id=audit-opened','work':'m05-p08.html?id=audit-work','book':'m08-p21.html?id=book-state','chapter':'m08-p13.html?id=book-state','page':'m08-p13.html?id=book-state','tag':'m06-p05.html','unlink':'m06-p03.html','cache':'m06-p11.html','record-repair':'m03-p06.html','account-repair':'m06-p02.html','form-discard':'m03-p05.html','sheet-discard':'m06-p12.html','account-delete':'m06-p08.html','pet-delete':'m07-p25.html'}[case];p.goto(BASE+'pages/'+route)
 return store(p)
def opened(p,case):
 if case in ['diary','photo','moment','anniversary','capsule','work']:
  selectors={'diary':'#more','photo':'#more','moment':'#more','anniversary':'#more','capsule':'#more','work':'#more'};p.locator(selectors[case]).click();p.get_by_role('button',name={'diary':'删除日记','photo':'删除照片','moment':'删除重要时刻','anniversary':'删除纪念日','capsule':'删除胶囊','work':'删除作品'}[case],exact=True).click()
 elif case=='book':p.locator('.show-delete').click()
 elif case=='chapter':p.get_by_role('button',name='章节操作「第一章」',exact=True).click();p.get_by_role('button',name='删除章节',exact=True).click()
 elif case=='page':p.get_by_role('button',name=re.compile('^页面操作')).first.click();p.get_by_role('button',name='删除书页',exact=True).click()
 elif case=='tag':p.get_by_role('button',name='旅行',exact=True).click();p.get_by_role('button',name='删除标签',exact=True).click()
 elif case=='unlink':p.locator('.unlink').click()
 elif case=='cache':p.locator('#cache').click()
 elif case=='record-repair':p.get_by_role('button',name='恢复可读记录',exact=True).click()
 elif case=='account-repair':p.get_by_role('button',name='恢复可读资料',exact=True).click()
 elif case=='form-discard':p.locator('[name=title]').fill('未保存的日记');p.locator('.back').click()
 elif case=='sheet-discard':p.locator('.feedback').click();p.get_by_role('textbox',name='意见反馈',exact=True).fill('未保存的反馈');p.keyboard.press('Escape')
 elif case=='account-delete':p.locator('.delete').click();p.get_by_role('button',name='继续身份确认',exact=True).click()
 elif case=='pet-delete':p.get_by_role('button',name='更多',exact=True).click();p.get_by_role('button',name='永久删除宠物数据',exact=True).click()
 confirm={'chapter':'确认删除章节','page':'确认删除书页','unlink':'请求解除关联','cache':'确认清理','record-repair':'确认恢复','account-repair':'确认恢复','form-discard':'放弃修改','sheet-discard':'放弃修改','account-delete':'注销演示账号','pet-delete':'永久删除'}.get(case,'确认删除');keep='继续编辑'if case in ['form-discard','sheet-discard']else'取消';dialog=p.locator('dialog');expect(dialog).to_be_visible();danger=dialog.get_by_role('button',name=confirm,exact=True);cancel=dialog.get_by_role('button',name=keep,exact=True)
 if case=='sheet-discard':cancel=p.locator('.prototype-sheet-discard').get_by_role('button',name=keep,exact=True)
 return dialog,danger,cancel
def inspect(p,button):
 return button.evaluate('(b)=>{const s=getComputedStyle(b),r=b.getBoundingClientRect();return{variant:b.dataset.variant,danger:b.dataset.danger,shared:b.classList.contains("prototype-component-button"),primary:b.dataset.primary,color:s.color,background:s.backgroundColor,paper:getComputedStyle(document.documentElement).getPropertyValue("--prototype-paper").trim(),dangerToken:getComputedStyle(document.documentElement).getPropertyValue("--prototype-danger").trim(),height:r.height,width:r.width}}')
def main():
 with sync_playwright()as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for case in CASES:
   c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   try:
    before=seed(p,case);dialog,danger,cancel=opened(p,case);metrics=inspect(p,danger);assert metrics['variant']=='danger'and metrics['danger']=='true'and metrics['shared']and metrics['primary']!='true'and metrics['height']>=44 and metrics['color']=='rgb(152, 91, 80)' and metrics['background']=='rgb(253, 251, 247)',metrics;expect(cancel).to_be_focused();assert store(p)==before
    cancel.click()
    if case=='sheet-discard':expect(p.get_by_role('textbox',name='意见反馈',exact=True)).to_have_value('未保存的反馈')
    elif case in ['record-repair','account-repair']:
     expect(p.get_by_role('button',name='恢复可读记录'if case=='record-repair'else'恢复可读资料',exact=True)).to_be_visible();p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
    else:expect(p.locator('dialog')).to_have_count(0)
    assert store(p)==before;assert not errors;row=dict(passed=True,metrics=metrics)
   except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1600:])
   row.update(case=case,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+case,flush=True);c.close()
  b.close()
 assert files==source();(OUT/'danger-confirmation-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=="__main__":main()
