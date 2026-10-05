from pathlib import Path
import json
from playwright.sync_api import sync_playwright,expect
OUT=Path(__file__).resolve().parent/'evidence/current';OUT.mkdir(parents=True,exist_ok=True);URL='http://127.0.0.1:8765/pages/'
def go(p,n,query=''):p.goto(URL+f'm07-p{n:02}.html'+query)
def seed(p,**changes):
 go(p,4);pet=dict(id='pet-test',name='团团',kind='小狗',status='active',adoptedDate='2026-10-05',energy=82,satiety=76,mood=70,affinity=0,food=[12,5,1],gifts=1,coins=0,stars=0,owned=[],outfit=None,room={},claims=[],logs=[],care=True,settings={});pet.update(changes)
 p.evaluate('(pet)=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-05");localStorage.setItem("dujia-prototype-relationship",JSON.stringify({bound:true,partner:"阿舟"}));localStorage.setItem("dujia-profile",JSON.stringify({nickname:"小满"}));localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet));}',pet)
def value(p):return p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet"))')
def fail(p,op):p.evaluate('(op)=>sessionStorage.setItem("dujia-prototype-fail-next",op)',op)
def invite_failure(p):
 seed(p);p.evaluate('localStorage.removeItem("dujia-prototype-pet")');go(p,2);p.locator('#pet-name').fill('');p.locator('#invite').click();expect(p.locator('#pet-name')).to_have_attribute('aria-invalid','true');p.locator('#pet-name').fill('花花');fail(p,'pet-adopt');p.locator('#invite').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');assert value(p) is None;p.locator('.pet-back').click();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);expect(p.locator('#pet-name')).to_have_value('花花');p.locator('#invite').click();p.wait_for_url('**/m07-p01.html');fail(p,'pet-remind');p.locator('#remind').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');assert not value(p).get('lastReminder');p.locator('#remind').click();expect(p.locator('.prototype-toast')).to_contain_text('不会发送真实消息')
def peer_rejection(p):
 seed(p,status='pending',requestedBy='小满');p.goto('http://127.0.0.1:8765/prototype/review.html');p.get_by_role('button',name='另一半拒绝领养',exact=True).click();p.wait_for_url('**/m07-p04.html');expect(p.locator('.adopt')).to_have_text('一起领养');assert value(p)['status']=='rejected';p.locator('.adopt').click();p.get_by_role('button',name='重新选择',exact=True).click();p.wait_for_url('**/m07-p02.html');assert value(p) is None
def energy_recovery(p):
 seed(p,energy=4);go(p,6);p.locator('#play').click();p.wait_for_url('**/m07-p07.html*');expect(p.locator('.energy span')).to_have_text('4/100');p.locator('.feed').click();p.wait_for_url('**/m07-p08.html');p.locator('#feed').click();expect(p.locator('#stock0')).to_have_text('11');assert value(p)['energy']==19;go(p,6);p.locator('#play').click();p.wait_for_url('**/m07-p05.html*');assert value(p)['energy']==14
def limits_gift_and_date(p):
 seed(p,gifts=0);go(p,6);p.locator('.option').nth(3).click();p.locator('#play').click();expect(p.locator('.prototype-toast')).to_contain_text('礼物已经用完');assert value(p)['affinity']==0
 for _ in range(2):
  go(p,6);p.locator('#play').click();p.wait_for_url('**/m07-p05.html*')
 go(p,6);expect(p.locator('#play')).to_be_disabled();p.evaluate('sessionStorage.setItem("dujia-prototype-today","2026-10-06")');p.reload();expect(p.locator('#play')).to_be_enabled();p.locator('#play').click();p.wait_for_url('**/m07-p05.html*');assert len([v for v in value(p)['logs'] if v['type']=='play'])==3
def atomic_failure(p):
 seed(p);go(p,9,'?food=0');p.wait_for_url('**/m07-p08.html');before=value(p);fail(p,'pet-feed');p.locator('#feed').click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');assert value(p)==before
 p.evaluate('(()=>{const old=Storage.prototype.setItem;Storage.prototype.setItem=function(key,value){if(key==="dujia-prototype-pet")throw new DOMException("full","QuotaExceededError");return old.call(this,key,value);};window.restorePetStorage=()=>{Storage.prototype.setItem=old;};})()');p.locator('#feed').click();expect(p.locator('.prototype-toast')).to_contain_text('本地空间不足');assert value(p)==before;p.evaluate('restorePetStorage()');p.locator('#feed').click();expect(p.locator('#stock0')).to_have_text('11');assert value(p)['energy']==97
def reward_failure_note(p):
 seed(p);go(p,11);p.get_by_role('button',name='给宠物添水',exact=True).click();expect(p.get_by_role('button',name='领取添水奖励',exact=True)).to_be_visible();before=value(p);fail(p,'pet-claim');p.get_by_role('button',name='领取添水奖励',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');assert value(p)==before;p.get_by_role('button',name='领取添水奖励',exact=True).click();p.wait_for_url('**/m07-p10.html*');go(p,11);expect(p.get_by_role('button',name='奖励已领取',exact=True)).to_be_disabled();p.get_by_role('button',name='记录今天的小心情',exact=True).click();p.get_by_label('今天的小心情',exact=True).fill('今天抱了抱团团');fail(p,'pet-note');p.get_by_role('button',name='保存小心情',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('未完成');expect(p.get_by_label('今天的小心情',exact=True)).to_have_value('今天抱了抱团团');p.get_by_role('button',name='保存小心情',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);expect(p.get_by_role('button',name='领取心情奖励',exact=True)).to_be_visible();assert any(v['text']=='今天抱了抱团团' for v in value(p)['logs'])
def load_retry_pause_export(p):
 seed(p);fail(p,'pet-load');go(p,3);p.get_by_role('button',name='重新加载',exact=True).click();expect(p.locator('.pet-load')).to_have_count(0);expect(p.locator('.title')).to_have_text('团团的小屋');p.evaluate('localStorage.setItem("dujia-prototype-preferences",JSON.stringify({autoBackup:true}));');go(p,11);p.get_by_role('button',name='给宠物添水',exact=True).click();expect(p.get_by_role('button',name='领取添水奖励',exact=True)).to_be_visible();assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-backup")).pet.logs[0].type')=='water';p.evaluate('(()=>{let v=JSON.parse(localStorage.getItem("dujia-prototype-pet"));v.care=false;localStorage.setItem("dujia-prototype-pet",JSON.stringify(v));})()');go(p,6);p.locator('#play').click();expect(p.locator('.prototype-toast')).to_contain_text('共同照顾已暂停');assert value(p)['affinity']==0
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'invite-validation-dirty-failure-reminder':invite_failure,'peer-reject-restart':peer_rejection,'low-energy-feed-recovery':energy_recovery,'gift-day-limit-rollover':limits_gift_and_date,'feed-failure-quota-atomic':atomic_failure,'reward-idempotency-note-failure':reward_failure_note,'load-retry-backup-paused-care':load_retry_pause_export}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as e:row={'case':name,'passed':False,'failure':repr(e)[:1800]}
  row.update(errors=errors,final_url=p.url);rows.append(row);(OUT/'pet-state-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
