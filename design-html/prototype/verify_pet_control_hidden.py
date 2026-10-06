"""Pet dirty exits, resource write failures and blocked-story return contracts."""
import json,traceback,sys
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import seed,store,source,ROOT,BASE
OUT=ROOT/'evidence'/('baseline'if '--baseline'in sys.argv else'current')
def blocked(p):
    seed(p,'m07-p17');expect(p.locator('.back')).to_have_attribute('aria-label','返回成长时间线');expect(p.locator('.return')).to_have_text('返回成长时间线');p.locator('.return').click();p.wait_for_url('**/m07-p18.html')
def dirty(p,kind):
    page={'adopt':'m07-p02','outfit':'m07-p12','room':'m07-p15'}[kind];seed(p,page)
    if kind=='room':p.evaluate('()=>{const k="dujia-prototype-pet",v=JSON.parse(localStorage.getItem(k));v.ownedRoom=["格纹地毯"];localStorage.setItem(k,JSON.stringify(v))}');p.reload();expect(p.locator('.pet-load')).to_have_count(0);expect(p.locator('.screen')).to_have_attribute('aria-busy','false')
    before=store(p)
    if kind=='adopt':p.locator('#pet-name').fill('未保存名字')
    else:p.locator('[data-item="'+('scarf'if kind=='outfit'else'plaid-rug')+'"]').click()
    p.go_back();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
    if kind=='adopt':expect(p.locator('#pet-name')).to_have_value('未保存名字')
    else:expect(p.locator('[data-item="'+('scarf'if kind=='outfit'else'plaid-rug')+'"]').first).to_have_attribute('aria-pressed','true')
    assert store(p)==before;p.go_back();p.get_by_role('button',name='放弃修改',exact=True).click();p.wait_for_url('**/'+('m07-p04'if kind=='adopt'else'm07-p03')+'.html');assert store(p)==before
def reply(p,exit):
    seed(p,'m07-p19');before=store(p);p.get_by_role('button',name='回应这一页',exact=True).click();p.get_by_role('textbox',name='回应内容',exact=True).fill('还未发送的回应')
    def close():
        if exit=='cancel':p.get_by_role('button',name='取消',exact=True).click()
        elif exit=='escape':p.keyboard.press('Escape')
        elif exit=='back':p.go_back()
        else:
            r=p.locator('.prototype-sheet-handle').bounding_box();p.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2);p.mouse.down();p.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2+110,steps=8);p.mouse.up()
    close();expect(p.get_by_text('是否放弃当前修改？',exact=True)).to_be_visible();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.get_by_role('textbox',name='回应内容',exact=True)).to_have_value('还未发送的回应');assert store(p)==before;close();p.get_by_role('button',name='放弃修改',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert store(p)==before
def quota(p,kind):
    seed(p,'m07-p06'if kind=='play'else'm07-p08');before=store(p);p.evaluate('()=>{const old=Storage.prototype.setItem;window.petWrite=old;Storage.prototype.setItem=function(k,v){if(k==="dujia-prototype-pet")throw new DOMException("full","QuotaExceededError");return old.call(this,k,v)}}');p.locator('#play'if kind=='play'else'#feed').click();expect(p.locator('.prototype-toast')).to_contain_text('不足');assert store(p)==before;p.evaluate('()=>{Storage.prototype.setItem=window.petWrite}');p.locator('#play'if kind=='play'else'#feed').click()
    if kind=='play':p.wait_for_url('**/m07-p05.html?id=*');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet")).energy')==77
    else:expect(p.locator('#stock0')).to_have_text('11')
    assert len(p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet")).logs'))==2
files=source();rows=[];cases=[('blocked-story-return-labels',blocked)]
if '--baseline'not in sys.argv:cases+=[(k+'-dirty-browser',lambda p,k=k:dirty(p,k))for k in ['adopt','outfit','room']]+[('reply-dirty-'+k,lambda p,k=k:reply(p,k))for k in ['cancel','escape','back','drag']]+[(k+'-quota-atomic-retry',lambda p,k=k:quota(p,k))for k in ['play','feed']]
with sync_playwright()as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,run in cases:
        c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p);assert not errors;row=dict(passed=True)
        except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
        row.update(case=name,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
    b.close()
assert files==source();OUT.mkdir(parents=True,exist_ok=True);(OUT/'pet-control-hidden-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed']for r in rows)else 1)
