"""Common-profile compatibility: peer decisions, retry and existing direct demo access."""
import hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_world_write_context import choose_avatar,pair,watch
from verify_image_read_order import A,uri

def main():
 files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')};fixture=declarations('verify_settings_controls.py');rows=[];out=ROOT/'evidence/current/world-existing-flow';out.mkdir(parents=True,exist_ok=True)
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for name in ['peer-accept','peer-reject-retry','logged-out-demo','nickname-quota-retry']:
   c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(case=name)
   try:
    fixture['seed'](p,'m06-p03')
    if name.startswith('peer-'):
     p.locator('.unlink').click();p.get_by_role('button',name='请求解除关联',exact=True).click();expect(p.locator('.status')).to_contain_text('等待');expect(p.locator('.unlink')).to_be_disabled();assert pair(p)['bound']
     p.goto(BASE+'prototype/review.html');p.get_by_role('button',name='另一半同意解除' if name=='peer-accept' else '另一半拒绝解除',exact=True).click();p.wait_for_url('**/m06-p03.html');assert not pair(p).get('unlinkPending')
     if name=='peer-accept':
      assert not pair(p)['bound'];expect(p.locator('.unlink')).to_be_disabled();p.locator('.portrait').click();expect(p.locator('dialog h2')).to_have_text('还没有关联另一半');p.get_by_role('button',name='取消',exact=True).click()
     else:
      assert pair(p)['bound'];expect(p.locator('.unlink')).to_be_enabled();p.evaluate("sessionStorage.setItem('dujia-prototype-fail-next','settings-unlink')");p.locator('.unlink').click();p.get_by_role('button',name='请求解除关联',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert not pair(p).get('unlinkPending');expect(p.locator('.unlink')).to_be_enabled();p.locator('.unlink').click();p.get_by_role('button',name='请求解除关联',exact=True).click();expect(p.locator('.status')).to_contain_text('等待');assert pair(p)['unlinkPending']
    else:
     if name=='logged-out-demo':
      p.evaluate("localStorage.removeItem('dujia-prototype-session')");p.reload();choose_avatar(p,A);p.wait_for_function("image=>JSON.parse(localStorage.getItem('dujia-prototype-relationship')).profile.avatar===image",arg=uri(A))
     else:watch(p,True)
     p.locator('.nick').click();field=p.get_by_label('共同昵称',exact=True);field.fill('保留演示小屋');p.get_by_role('button',name='保存',exact=True).click()
     if name=='nickname-quota-retry':
      expect(p.locator('.prototype-toast')).to_contain_text('空间不足');expect(field).to_have_value('保留演示小屋');p.get_by_role('button',name='保存',exact=True).click()
     expect(p.locator('dialog[open]')).to_have_count(0);assert pair(p)['profile']['nickname']=='保留演示小屋'
     if name=='logged-out-demo':assert pair(p)['profile']['avatar']==uri(A)
    saved=pair(p);p.reload();assert pair(p)==saved;assert not errors,errors;row.update(passed=True,reload_consistent=True)
   except Exception:row.update(passed=False,failure=traceback.format_exc()[-2400:])
   row['errors']=errors;rows.append(row);c.close();assert source()==files;print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True)
   (out/'results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  b.close()
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
