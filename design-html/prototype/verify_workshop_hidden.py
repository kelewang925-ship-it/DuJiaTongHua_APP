"""Source permissions, applied choices and dirty editor exits through actual UI."""
from pathlib import Path
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from verify_workshop_controls import seed,store,source,ROOT,BASE
OUT=ROOT/'evidence'/('baseline'if '--baseline'in sys.argv else'current')
def permissions(p):
    seed(p,'m05-p02');p.evaluate('()=>{const key="dujia-prototype-moments",values=JSON.parse(localStorage.getItem(key));values.push({id:"private",name:"私密时刻",story:"不应进入共同创作",visibility:"private",status:"published",comments:[]},{id:"draft",name:"未发布时刻",story:"还没发布",status:"draft",comments:[]});localStorage.setItem(key,JSON.stringify(values))}');p.get_by_role('button',name='重要时刻',exact=True).click();p.locator('#go').click();expect(p.locator('dialog')).not_to_contain_text('私密时刻');expect(p.locator('dialog')).not_to_contain_text('未发布时刻');expect(p.get_by_label('共同素材时刻',exact=True)).to_be_visible()
def choices(p,kind):
    seed(p,'m05-p02');p.locator('.option').filter(has_text={'diary':'共同日记','photo':'相册照片','moment':'重要时刻','free':'自由写一段回忆'}[kind]).click();p.locator('#go').click()
    if kind!='free':
        p.get_by_label({'diary':'共同素材日记','photo':'共同素材照片','moment':'共同素材时刻'}[kind],exact=True).check();p.get_by_role('button',name='使用这些素材'if kind=='photo'else'使用这段回忆',exact=True).click()
    p.wait_for_url('**/'+('m05-p04'if kind=='photo'else'm05-p03')+'.html?id=*');values=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-works"))');assert len(values)==7;item=next(v for v in values if v['id']==p.url.split('id=')[1]);assert item['sourceKind']==kind and item['sourceIds']==([]if kind=='free'else['work-'+kind])
def dirty(p,page):
    seed(p,page);before=store(p);field=p.locator('#appearance'if page=='m05-p10'else'#narration'if page=='m05-p05'else'#story');field.fill('返回仍保留的故事');p.go_back();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(field).to_have_value('返回仍保留的故事');assert store(p)==before;p.go_back();p.get_by_role('button',name='放弃修改',exact=True).click();p.wait_for_url('**/'+('m05-p03'if page=='m05-p10'else'm05-p09')+'.html*');assert store(p)==before
def album(p):
    seed(p,'m05-p08');p.locator('#save').click();expect(p.locator('.prototype-toast')).to_contain_text('相册');p.locator('#save').click();expect(p.locator('.prototype-toast')).to_contain_text('相册');assert len(p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records"))'))==3
def delete(p):
    seed(p,'m05-p08');before=store(p);p.locator('#more').click();p.get_by_role('button',name='删除作品',exact=True).click();p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert store(p)==before;p.locator('#more').click();p.get_by_role('button',name='删除作品',exact=True).click();p.get_by_role('button',name='确认删除',exact=True).click();p.wait_for_url('**/m05-p09.html');values=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-works"))');assert len(values)==5 and not any(v['id']=='work-ready'for v in values)
def label(p):seed(p,'m05-p10');expect(p.locator('.back')).to_have_attribute('aria-label','返回当前创作');p.locator('.back').click();p.wait_for_url('**/m05-p03.html?id=work-free')
files=source();rows=[]
cases=[('shared-moment-source-permissions',permissions)]+[('apply-source-'+k,lambda p,k=k:choices(p,k))for k in ['diary','photo','moment','free']]+[(page+'-dirty-browser',lambda p,page=page:dirty(p,page))for page in ['m05-p03','m05-p04','m05-p05','m05-p10']]+[('album-repeat-idempotence',album),('delete-cancel-preserve-other-works',delete),('characters-return-label-and-id',label)]
with sync_playwright()as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,run in cases:
        c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p);assert not errors;row=dict(passed=True)
        except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
        row.update(case=name,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
    b.close()
assert files==source();OUT.mkdir(parents=True,exist_ok=True);(OUT/'workshop-hidden-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed']for r in rows)else 1)
