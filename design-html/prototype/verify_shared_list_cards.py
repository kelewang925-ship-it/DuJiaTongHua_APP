"""Actual dynamic card content, hit targets and route contracts in five widths."""
import hashlib,json,re,sys,traceback
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import ROOT,BASE,source
from audit_current_runtime import data

CASES=[
 ('home','m03-p02','','.prototype-home-record','共同日记','m03-p08','audit-diary'),
 ('search','m03-p04','?q=共同','.prototype-diary-card','共同日记','m03-p08','audit-diary'),
 ('diary','m03-p06','','.prototype-diary-card','共同日记','m03-p08','audit-diary'),
 ('photo','m03-p10','','.prototype-photo-card','共同照片','m03-p12','audit-photo'),
 ('moment','m04-p01','','.prototype-moment-cards>button','共同重要时刻','m04-p03','audit-moment'),
 ('anniversary','m04-p07','','.prototype-anniversary-row','未来的纪念日','m04-p10','audit-anniversary'),
 ('reminder','m04-p05','','.prototype-reminder-card','今天的纪念日','m04-p11','audit-today'),
 ('capsule','m04-p12','','.prototype-capsule-card','未来的信','m04-p15','audit-sealed'),
 ('work-recent','m05-p01','','.prototype-work-recent>button','实际工坊作品','m05-p08','audit-work'),
 ('work-list','m05-p09','','.prototype-work-card','实际工坊作品','m05-p08','audit-work'),
 ('drafts','m06-p04','','.prototype-settings-drafts>button','共同日记','m03-p05','audit-diary'),
 ('pet-stories','m07-p18','','.pet-life-story-list>button','实际成长故事','m07-p19','audit-story'),
 ('reply','m04-p16','','.prototype-reply-cards>article','共同日记','m03-p08','audit-diary'),
]

def seed(name):
    d=data(True);d['dujia-prototype-session']={'loggedIn':True}
    if name=='drafts':d['dujia-prototype-records'][0]['status']='draft'
    if name=='reminder':d['dujia-prototype-anniversaries'][1].update(date='2026-10-06',enabled=True,reminderDays=3)
    if name=='reply':d['dujia-prototype-records'][0]['comments']=[{'id':'audit-reply','author':'阿舟','text':'一起珍藏这一天','createdAt':1791158400000,'read':False}]
    return d

def main():
    files=source();baseline='--baseline'in sys.argv;rows=[];final_repair='--replay-reminders'in sys.argv;repair='--replay-failed'in sys.argv or final_repair;retained=[];replayed=[];baseline_sha=None
    if repair:
        raw=(ROOT/('evidence/baseline/shared-list-cards-before-reminder-days-fix.json'if final_repair else'evidence/baseline/shared-list-cards-before-probe-fix.json')).read_bytes();prior=json.loads(raw);assert prior['files']==files and len(prior['results'])==66
        failed={(r['case'],r['width'])for r in prior['results']if not r['passed']};assert failed=={('reminder',w)for w in [320,360,390,414,430]}| (set()if final_repair else{('work-recent',430)})
        rows=prior['results'];retained=[i for i,r in enumerate(rows)if r['passed']];assert len(retained)==(61 if final_repair else 60);baseline_sha=hashlib.sha256(raw).hexdigest()
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in ([390]if baseline else[320,360,390,414,430]):
            for name,page_id,query,selector,title,dest,identifier in CASES:
                if repair and (name,width)not in failed:continue
                context=browser.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=context.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row={'case':name,'page':page_id,'width':width}
                try:
                    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',seed(name));p.goto(BASE+'pages/'+page_id+'.html'+query);p.wait_for_timeout(650)
                    card=p.locator(selector).filter(has_text=title).first;expect(card).to_be_visible();assert 'prototype-component-card'in card.get_attribute('class').split(),'Dynamic card is still local'
                    assert card.evaluate('(e)=>e.tagName')==('ARTICLE'if name in ['reply','anniversary']else'BUTTON')
                    if name=='photo':expect(card.locator('img')).to_have_count(1);assert card.locator('img').evaluate('(e)=>e.complete&&e.naturalWidth>0')
                    if name=='diary':expect(card).to_contain_text('真正可编辑的共同正文');expect(card).to_contain_text('共同可见')
                    if name=='capsule':expect(card).to_contain_text('2026-12-24')
                    if name=='reply':expect(card).to_contain_text('一起珍藏这一天')
                    action=card.get_by_role('button',name='查看原记录',exact=True)if name=='reply'else card.locator('.prototype-anniversary-card')if name=='anniversary'else card
                    action.evaluate('e=>e.scrollIntoView({block:"center"})');g=action.evaluate('''e=>{const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {width:r.width,height:r.height,left:r.left,right:r.right,hit:hit===e||e.contains(hit)}}''');row['geometry']=g
                    assert g['width']>=44 and g['height']>=44 and g['left']>=-1 and g['right']<=width+1 and g['hit'],g
                    if width==390:action.focus();action.press('Enter')
                    else:action.click()
                    expect(p).to_have_url(re.compile(dest+r'\.html\?[^#]*\bid='+re.escape(identifier)+r'(?:&|$)'))
                    if name=='reply':assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records")).find(v=>v.id==="audit-diary").comments[0].read')is True
                    if name=='reminder':assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-reminder-reads")).some(v=>v.targetId==="audit-today"&&v.read)')is True
                    assert not errors,errors;row.update(passed=True,effective=p.url)
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-2200:])
                row['errors']=errors
                if repair:
                    index=next(i for i,r in enumerate(rows)if r['case']==name and r['width']==width);rows[index]=row;replayed.append(index)
                else:rows.append(row)
                context.close();assert source()==files
            print(str(width)+'px '+str(sum(r['passed']for r in rows if r['width']==width and r['case']!='factory-content-and-default-contract'))+'/13',flush=True)
        if repair:browser.close()
        else:
          context=browser.new_context();p=context.new_page();row={'case':'factory-content-and-default-contract','width':390}
          try:
            p.goto(BASE+'prototype/components.html');value=p.evaluate('''()=>{const C=PrototypeUI.components,leaf=document.createElement('strong');leaf.textContent='原有正文';const custom=C.card({content:[leaf],onClick:()=>{},selected:false}),old=C.card({title:'旧标题',message:'旧摘要'});return {same:custom.firstChild===leaf,children:custom.children.length,tag:custom.tagName,type:custom.type,selected:custom.getAttribute('aria-pressed'),defaultTitle:old.querySelector('h2').textContent,defaultBody:old.querySelector('p').textContent,defaultTag:old.tagName}}''');row['observed']=value
            assert value=={'same':True,'children':1,'tag':'BUTTON','type':'button','selected':'false','defaultTitle':'旧标题','defaultBody':'旧摘要','defaultTag':'ARTICLE'},value;row['passed']=True
          except Exception:row.update(passed=False,failure=traceback.format_exc()[-1600:])
          rows.append(row);context.close();browser.close()
    path=ROOT/('evidence/baseline/shared-list-cards-before.json'if baseline else'evidence/current/shared-list-cards-results.json');path.write_text(json.dumps({'files':files,'results':rows,'scope':'13 dynamic card contexts, actual content, five-width center hit/44px bounds and routes; Enter at 390px; factory backward compatibility','retained_baseline_sha256':baseline_sha,'retained_indices':retained,'replayed_indices':replayed},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'cases':len(rows),'passed':sum(r['passed']for r in rows)}));raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
