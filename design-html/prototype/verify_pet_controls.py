"""Explicit pet page conditions; observe then execute every enabled initial control."""
from pathlib import Path
import json,hashlib,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from audit_runtime import INIT,OBSERVE
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;BASE='http://127.0.0.1:8765/';OUT=ROOT/'evidence/current'
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
def seed(p,page):
    n=int(page[-2:]);d=data(True);pet=d['dujia-prototype-pet'];d['dujia-prototype-anniversaries']=[];d['dujia-prototype-capsules']=[];d['dujia-prototype-works']=[];d['dujia-prototype-books']=[]
    d['dujia-prototype-session']=dict(loggedIn=True);pet['logs']=[dict(id='pet-story',type='note',text='共同成长故事',actor='小满',date='2026-10-05',at=1791158400000,story=True)];pet['ownedRoom']=[]
    if n==1:pet.update(status='pending',requestedBy='小满',requestedAt=1791158400000)
    if n in [2,4]:d['dujia-prototype-pet']=None
    if n==5:pet['logs']=[dict(id='pet-play',type='play',text='摸摸头',actor='小满',date='2026-10-06',delta=dict(energy=-5,mood=2,affinity=3),story=True)];pet['lastInteraction']='pet-play'
    if n==7:pet['energy']=0
    if n==9:pet['food']=[0,0,0]
    if n==10:pet['logs']=[dict(id='pet-reward',type='reward',text='金币 ×20',actor='小满',date='2026-10-06',story=False)];pet['lastReward']='pet-reward'
    if n==13:pet['stars']=0
    if n==14:pet['logs']=[dict(id='pet-room',type='room',text='整理了小屋',actor='小满',date='2026-10-06',after={},story=True)];pet['lastRoom']='pet-room'
    if n==16:pet['coins']=0;pet['stars']=0
    if n==17:pet['logs']=[dict(id='pet-blocked',type='source',text='原有故事',sourceId='gone',sourceKind='record',actor='小满',date='2026-10-05',story=True)]
    query={5:'?id=pet-play',7:'?cost=5',10:'?id=pet-reward',13:'?item=crown',14:'?id=pet-room',16:'?item=lamp',17:'?id=pet-blocked',19:'?id=pet-story',20:'?achievement=days30',23:'?item=scarf'}.get(n,'')
    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d);p.goto(BASE+'pages/'+page+'.html'+query);expect(p.locator('.screen')).to_have_attribute('aria-busy','false');expect(p.locator('.pet-load')).to_have_count(0);assert page+'.html'in p.url,(page,p.url);p.evaluate('document.fonts.ready')
def store(p):return p.evaluate('JSON.stringify({...localStorage})')
ITEMS={'小花围巾':'scarf','格纹蝴蝶结':'bow','星星领结':'star-bow','蜜桃帽子':'peach-hat','星光皇冠':'crown','雨天小斗篷':'cape','暖暖小马甲':'vest','晚安铃铛':'bell','花朵地毯':'flower-rug','格纹地毯':'plaid-rug','月亮地毯':'moon-rug','野餐垫':'picnic-rug'}
ACHIEVEMENTS={'第一次见面':'meet','玩到天黑':'play10','默契喂食':'feed20','小屋变新了':'room','照顾7天':'care7','亲密搭档':'affinity','陪伴30天':'days30'}
def contract(page,v):
    n=int(page[-2:]);s=v['selector'];label=v['label']
    if s.startswith('body>nav'):return 'route:'+{'首页':'m03-p02','重要时刻':'m04-p01','工坊':'m05-p01','宠物':'self','我的':'m06-p01'}[label]
    if label in ['返回','宠物空间','返回宠物小屋','返回宠物空间','返回成长时间线']:return 'route:'+('m03-p02'if n==1 else'm07-p04'if n==2 else'm03-p02'if n in [3,4]else'm07-p18'if n in [17,19]else'm07-p25'if n==24 else'm07-p22'if n==23 else'm07-p03')
    if label in ['暂时返回']:return 'route:m03-p02'
    if s=='#remind':return 'remind'
    if n==2:
        if s=='#pet-name':return 'input'
        if s=='#invite':return 'adopt'
        return 'pressed'
    if label in ['照顾指南','先看看照顾指南']:return 'modal:一起照顾小伙伴'
    if label=='宠物日记':return 'modal:从第一天开始记录'
    if label=='一起领养':return 'route:m07-p02'
    if label in ['互动','陪宠物互动','再玩一次']:return 'route:m07-p06'
    if label in ['喂食','给宠物喂食','去喂食补充精力 ›']:return 'route:m07-p08'
    if label in ['任务','去任务 ›','去做任务','去获得更多食物 ›','返回任务','去完成今天的照顾']:return 'route:m07-p11'
    if label in ['装扮']and n==3:return 'route:m07-p12'
    if label in ['布置小屋','整理宠物小屋','继续布置']:return 'route:m07-p15'
    if label in ['成长故事','成长日记']:return 'route:m07-p18'
    if label=='成就图鉴':return 'route:m07-p21'
    if label=='宠物设置':return 'route:m07-p25'
    if label in ['回到小屋','返回小屋']:return 'route:m07-p03'
    if n==6:return 'play'if s=='#play'else'pressed'
    if n==8:return 'feed'if s=='#feed'else'pressed'
    if n==11:
        if label in ['每日任务','本周约定']:return 'tab'
        if label=='给宠物添水':return 'water'
        if label=='记录今天的小心情':return 'sheet:宠物小心情'
    if n==12:
        if label in ['衣服','配饰','小物']:return 'tab'
        if label=='不佩戴':return 'none'
        if s=='#save':return 'outfit-save'
    if n==15:
        if label in ['地毯','小床','墙饰','摆件']:return 'tab'
        if label=='保存小屋布置':return 'room-save'
    if n==18:
        if label=='写一页成长故事':return 'sheet:成长故事'
        if label=='关联共同记录':return 'sheet:关联共同记录'
        if label.startswith('2026-10-05'):return 'route:m07-p19:id=pet-story'
    if n==19:return 'sheet:成长故事'if label=='写下今天的下一页'else'sheet:回应'
    if n==20 and label=='领取奖励':return 'achievement'
    if n==21:
        if label=='收藏图鉴':return 'route:m07-p22'
        for name,id in ACHIEVEMENTS.items():
            if label.startswith(name):return 'route:m07-p20:achievement='+id
    if n==22:
        if label in ['装扮','小屋','纪念物']:return 'tab'
        if label=='认识小伙伴':return 'sheet:四位小伙伴'
    if n==23:
        if label=='返回图鉴':return 'route:m07-p22'
        if s=='#wear':return 'equip'
    if n==24:
        if s=='#export':return 'export'
        if s=='#unlink':return 'modal:暂停共同照顾？'
        if label=='我再想想，返回':return 'route:m07-p25'
    if n==25:
        if s=='#time':return 'sheet:提醒时间'
        if s=='#export':return 'export'
        if s=='#explain':return 'modal:仅我们可见'
        if label=='暂时解除共同照顾':return 'route:m07-p24'
        if label=='更多':return 'sheet:宠物资料与数据'
        return 'setting'
    for name,id in ITEMS.items():
        if label.startswith(name):return 'catalog:'+id
    raise AssertionError((page,label,'missing contract'))
def control(p,page,v,kind):
    seed(p,page);button=p.locator(v['selector']);expect(button).to_be_visible();expect(button).to_be_enabled();before=store(p);n=int(page[-2:])
    if kind=='input':button.fill('长'*20);expect(button).to_have_value('长'*12);expect(button).to_be_focused();assert store(p)==before;return
    if kind=='export':
        with p.expect_download()as info:button.click()
        d=info.value;assert d.suggested_filename=='团团成长记录.json';value=json.loads(Path(d.path()).read_text(encoding='utf-8'));assert value;assert store(p)==before;return
    if kind=='adopt':p.locator('#pet-name').fill('新伙伴')
    button.click()
    if kind.startswith('route:'):
        bits=kind.split(':');dest=bits[1]
        if dest=='self':assert page+'.html'in p.url
        else:p.wait_for_url('**/'+dest+'.html'+('?' +bits[2]if len(bits)>2 else'*'))
    elif kind.startswith(('sheet:','modal:')):expect(p.locator('dialog h2')).to_have_text(kind.split(':')[1]);p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);expect(button).to_be_focused()
    elif kind=='pressed':expect(button).to_have_attribute('aria-pressed','true')
    elif kind=='tab':expect(button).to_have_attribute('aria-selected','true')
    elif kind=='none':expect(p.get_by_role('button',name='不佩戴',exact=True)).to_have_attribute('aria-pressed','true')
    elif kind=='remind':expect(p.locator('.prototype-toast')).to_contain_text('本地提醒');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet")).lastReminder')>0;return
    elif kind=='adopt':p.wait_for_url('**/m07-p01.html');pet=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet"))');assert pet['name']=='新伙伴'and pet['status']=='pending';return
    elif kind=='play':p.wait_for_url('**/m07-p05.html?id=*');pet=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet"))');assert pet['energy']==77 and pet['affinity']==163 and pet['logs'][0]['type']=='play';return
    elif kind=='feed':expect(p.locator('#stock0')).to_have_text('11');pet=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet"))');assert pet['energy']==97 and pet['satiety']==88 and pet['logs'][0]['type']=='feed';return
    elif kind=='water':expect(p.get_by_role('button',name='领取添水奖励',exact=True)).to_be_visible();assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet")).logs[0].type')=='water';return
    elif kind=='outfit-save':expect(p.locator('.prototype-toast')).to_contain_text('穿戴已保存')
    elif kind=='room-save':p.wait_for_url('**/m07-p14.html?id=*');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet")).logs[0].type')=='room';return
    elif kind=='achievement':expect(p.locator('.prototype-toast')).to_contain_text('成就奖励已到账');expect(p.locator('.claim')).to_be_disabled();pet=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet"))');assert pet['stars']==60 and 'achievement:days30'in pet['claims'];return
    elif kind=='equip':p.wait_for_url('**/m07-p12.html');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet")).outfit')=='小花围巾';return
    elif kind=='setting':
        key='stories'if v['label']=='成长故事自动收录'else'notice'if v['label']=='照顾通知'else'reminder';p.wait_for_function('key=>JSON.parse(localStorage.getItem("dujia-prototype-pet")).settings[key]===false',arg=key);return
    elif kind.startswith('catalog:'):
        id=kind.split(':')[1]
        if n==22:p.wait_for_url('**/m07-p23.html?item='+id)
        elif id in ['scarf','flower-rug']:expect(p.locator('[data-item="'+id+'"]').first).to_have_attribute('aria-pressed','true')
        elif id=='picnic-rug':p.wait_for_url('**/m07-p16.html?item=picnic-rug')
        else:expect(p.locator('dialog h2')).to_have_text('解锁'+next(name for name,key in ITEMS.items()if key==id));p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0)
    else:raise AssertionError(kind)
    assert store(p)==before
def main():
    files=source();inventory=[];rows=[]
    with sync_playwright()as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for i in range(1,26):
            page=f'm07-p{i:02}';c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');c.add_init_script(INIT);p=c.new_page();p.set_default_timeout(4500);seed(p,page);controls=[v for v in p.evaluate(OBSERVE)['controls']if v['visible']and not v['disabled']];inventory.append(dict(page=page,effective=p.url,controls=controls));print(page,len(controls),flush=True);c.close()
        if '--inventory'not in sys.argv:
            for entry in inventory:
                for v in entry['controls']:
                    c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));kind=contract(entry['page'],v)
                    try:control(p,entry['page'],v,kind);assert not errors;row=dict(passed=True)
                    except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
                    row.update(page=entry['page'],selector=v['selector'],label=v['label'],contract=kind,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+entry['page']+' '+v['label'].replace('\n',' '),flush=True);c.close()
        b.close()
    assert files==source();(OUT/('pet-control-inventory.json'if '--inventory'in sys.argv else'pet-controls-results.json')).write_text(json.dumps(dict(files=files,inventory=inventory,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if all(r['passed']for r in rows)else 1)
if __name__=='__main__':main()
