"""Execute explicit initial controls on ten workshop page fixtures."""
from pathlib import Path
import json,hashlib,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from audit_runtime import INIT,OBSERVE
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;BASE='http://127.0.0.1:8765/';OUT=ROOT/'evidence/current'
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
def seed(p,page):
    d=data(True)
    for key in ['anniversaries','capsules','works','moments','records']:d['dujia-prototype-'+key]=[]
    d['dujia-prototype-pet']=None
    d['dujia-prototype-records']=[dict(id='work-diary',type='diary',title='共同素材日记',body='一起散步。一起许愿。',visibility='shared',status='published',comments=[]),dict(id='work-photo',type='photo',title='共同素材照片',body='旅行合照',image='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><rect width="40" height="40" fill="pink"/></svg>',visibility='shared',status='published',comments=[])]
    d['dujia-prototype-moments']=[dict(id='work-moment',name='共同素材时刻',story='星空下的祝福',date='2026-10-05',comments=[])]
    items=[]
    for id,typ,kind,status in [('work-free','comic','free','draft'),('work-photos','comic','photo','draft'),('work-film','film','diary','draft'),('work-running','comic','free','generating'),('work-failed','comic','free','failed'),('work-ready','film','diary','ready')]:
        items.append(dict(id=id,name=id,story='一起散步。一起许愿。',type=typ,sourceKind=kind,sourceIds=['work-photo']if kind=='photo'else['work-diary']if kind=='diary'else[],style='水彩'if kind=='photo'else'暖暖水彩',mode='温柔叙事',mood='温柔手帐',status=status,startedAt=0,dueAt=9999999999999 if status=='generating'else 0,comments=[]))
    d['dujia-prototype-works']=items
    q={'m05-p03':'?id=work-free','m05-p04':'?id=work-photos','m05-p05':'?id=work-film','m05-p06':'?id=work-running','m05-p07':'?id=work-failed','m05-p08':'?id=work-ready','m05-p10':'?work=work-free'}.get(page,'')
    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d);p.goto(BASE+'pages/'+page+'.html'+q)
    if page=='m05-p09':expect(p.locator('.prototype-work-card')).to_have_count(6)
    p.evaluate('document.fonts.ready')
def store(p):return p.evaluate('JSON.stringify({...localStorage})')
def contract(page,v):
    s=v['selector'];label=v['label']
    if s.startswith('body>nav'):return 'nav:'+{'首页':'m03-p02','重要时刻':'m04-p01','工坊':'self','宠物':'m07-p04','我的':'m06-p01'}[label]
    if label.startswith('work-'):return 'work:'+label.split('\n')[0]
    if label.startswith('做成童话漫画')or label in ['开始一次创作','开始创作']:return 'route:m05-p02'
    if label.startswith('制作回忆影片'):return 'new-film'
    if label=='查看全部 ›':return 'route:m05-p09'
    if label in ['返回童话工坊','返回工坊','返回当前创作']or label.startswith('先回到童话工坊'):return 'route:'+('m05-p03'if page=='m05-p10'else'm05-p01')
    if label=='返回素材选择':return 'route:m05-p02'
    if label=='返回我的创作':return 'route:m05-p09'
    if page=='m05-p02'and label in ['共同日记','相册照片','重要时刻','自由写一段回忆']:return 'choice'
    if s=='#go':return 'sheet:选择共同素材'
    if label in ['创作草稿操作','更多作品操作']:return 'sheet:创作操作'
    if label=='给另一半看看':return 'sheet:给另一半看看'
    if label=='选择照片':return 'sheet:选择共同素材'
    if label=='选择共同片段':return 'sheet:片段类型'
    if label=='取消生成':return 'modal:取消这次生成？'
    if label.startswith('移除片段'):return 'remove-clip'
    if label=='共同素材照片':return 'toggle-photo'
    if label=='编辑':return 'focus-story'
    if label.startswith(('默默 & 小满','他 ','她 ')):return 'characters'
    if s=='#generate'or label=='重新生成'and page=='m05-p07':return 'generate'
    if label=='重新生成'or label=='调整内容':return 'route:m05-p05'if page=='m05-p08'else'route:m05-p03'
    if label=='暂存创作草稿':return 'draft'
    if label=='试听演示音轨':return 'audio'
    if label=='播放片段演示':return 'play'
    if label.startswith('第')and label.endswith('页'):return 'frame:'+label[1:-1]
    if label=='保存到共同相册':return 'album'
    if label=='更新我们的主角':return 'save-characters'
    if label=='收藏夹':return 'favorites'
    if label=='刷新我的创作':return 'refresh'
    if page=='m05-p09'and label in ['全部','漫画','影片','草稿']:return 'tab:'+label
    if v['native_input']:return 'input'
    if page in ['m05-p03','m05-p04','m05-p05']and v.get('aria_pressed')is not None:return 'setting'
    raise AssertionError((page,label,'missing explicit contract'))
def control(p,page,v,kind):
    seed(p,page);button=p.locator(v['selector']);expect(button).to_be_visible();expect(button).to_be_enabled();before=store(p)
    if kind=='input':limit=int(button.get_attribute('maxlength'));button.fill('长'*(limit+8));assert len(button.input_value())==limit;expect(button).to_be_focused();assert store(p)==before;return
    if kind=='audio':button.click();expect(p.locator('#play')).to_have_attribute('aria-label','停止试听');p.locator('#play').click();expect(p.locator('#play')).to_have_attribute('aria-label','试听演示音轨');assert store(p)==before;return
    button.click()
    if kind.startswith(('route:','nav:','work:')):
        dest=kind.split(':')[1]
        if kind.startswith('work:'):dest={'work-free':'m05-p03','work-photos':'m05-p04','work-film':'m05-p05','work-running':'m05-p06','work-failed':'m05-p07','work-ready':'m05-p08'}[dest]
        if dest=='self':assert page+'.html'in p.url
        else:p.wait_for_url('**/'+dest+'.html*')
        if kind.startswith('work:'):assert p.url.endswith('?id='+kind.split(':')[1])
        if page=='m05-p10':assert p.url.endswith('?id=work-free')
        if page=='m05-p08'and kind=='route:m05-p05':assert p.url.endswith('?id=work-ready')
    elif kind=='new-film':p.wait_for_url('**/m05-p05.html?id=*');assert len(p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-works"))'))==7;return
    elif kind in ['choice','setting']:expect(button).to_have_attribute('aria-pressed','true')
    elif kind=='focus-story':expect(p.locator('#story')).to_be_focused()
    elif kind.startswith(('sheet:','modal:')):
        expect(p.locator('dialog h2')).to_have_text(kind.split(':')[1]);p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);expect(button).to_be_focused()
    elif kind=='toggle-photo':expect(p.locator('.photos button')).to_have_attribute('aria-pressed','false');expect(p.locator('#photo-count')).to_have_text('0')
    elif kind=='remove-clip':expect(p.locator('.clips button')).to_have_count(1)
    elif kind=='characters':p.wait_for_url('**/m05-p10.html?work=*');assert p.url.endswith('work='+{'m05-p03':'work-free','m05-p04':'work-photos','m05-p05':'work-film'}[page]);assert len(p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-works"))'))==6;return
    elif kind=='draft':p.wait_for_url('**/m05-p09.html');assert len(p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-works"))'))==6;return
    elif kind=='generate':p.wait_for_url('**/m05-p06.html?id=*');assert p.evaluate('id=>JSON.parse(localStorage.getItem("dujia-prototype-works")).find(v=>v.id===id).status',p.url.split('id=')[1])=='generating';return
    elif kind.startswith('frame:'):expect(p.locator('#page-count')).to_have_text(kind.split(':')[1]+' / 8');expect(button).to_have_attribute('aria-pressed','true')
    elif kind=='album':expect(p.locator('.prototype-toast')).to_contain_text('已保存到共同相册');values=p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-records"))');assert len(values)==3 and sum(v.get('workId')=='work-ready'for v in values)==1;return
    elif kind=='save-characters':p.wait_for_url('**/m05-p03.html?id=work-free');assert len(p.evaluate('JSON.parse(localStorage.getItem("dujia-characters"))'))==4;return
    elif kind=='favorites':expect(button).to_have_attribute('aria-pressed','true');expect(p.get_by_role('button',name='查看全部作品',exact=True)).to_be_visible()
    elif kind.startswith('tab:'):expect(button).to_have_attribute('aria-selected','true');expect(p.locator('.prototype-work-card')).to_have_count({'全部':6,'漫画':4,'影片':2,'草稿':3}[kind.split(':')[1]])
    elif kind=='refresh':expect(p.locator('.prototype-work-list')).to_have_attribute('aria-busy','true');expect(p.locator('.prototype-work-card')).to_have_count(6)
    elif kind=='play':expect(p.get_by_role('button',name='暂停播放',exact=True)).to_be_visible();expect(p.locator('#page-count')).not_to_have_text('1 / 8');p.get_by_role('button',name='暂停播放',exact=True).click();expect(p.get_by_role('button',name='播放片段演示',exact=True)).to_be_visible()
    else:raise AssertionError(kind)
    assert store(p)==before
def main():
    files=source();inventory=[];rows=[]
    with sync_playwright()as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for i in range(1,11):
            page=f'm05-p{i:02}';c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');c.add_init_script(INIT);p=c.new_page();p.set_default_timeout(4500);seed(p,page);controls=[v for v in p.evaluate(OBSERVE)['controls']if v['visible']and not v['disabled']];inventory.append(dict(page=page,effective=p.url,controls=controls));print(page,len(controls),flush=True);c.close()
        if '--inventory'not in sys.argv:
            for entry in inventory:
                for v in entry['controls']:
                    c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));kind=contract(entry['page'],v)
                    try:control(p,entry['page'],v,kind);assert not errors;row=dict(passed=True)
                    except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
                    row.update(page=entry['page'],selector=v['selector'],label=v['label'],contract=kind,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+entry['page']+' '+v['label'].replace('\n',' '),flush=True);c.close()
        b.close()
    assert files==source();(OUT/('workshop-control-inventory.json'if '--inventory'in sys.argv else'workshop-controls-results.json')).write_text(json.dumps(dict(files=files,inventory=inventory,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=="__main__":main()
