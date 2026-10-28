"""Replay current V2 initial controls with explicit contracts, retaining legacy tests."""
import json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_book_v2_reconciliation import ROOT,dependencies,sha

BACK={1:'m03-p02',2:'m03-p02',3:1,4:1,5:4,6:5,7:6,8:7,9:8,10:8,11:8,12:8,13:6,14:1,15:1,16:1,17:16,18:16,19:18,21:15}
def route(target):return 'route:'+('m08-p'+str(target).zfill(2) if isinstance(target,int) else target)
def contract(page,v,old):
    n=int(page[-2:]);label=v['label'];selector=v['selector']
    if v['native_input']:return 'file' if v['type']=='file' else 'input'
    if n==20:return 'close-supplements'
    if label in ['返回','返回首页','‹ 书架']:return route(BACK[n])
    if n==1:
        if label in ['···','全部回忆册 ›','归档与草稿']:return 'sheet:全部回忆册'
        if label.startswith('从封面打开'):return route('m08-p16?id=book-state&page=page-state')
        return {'封面':route(15),'整理':route(13),'开始翻阅 →':route('m08-p16?id=book-state&page=page-state'),'＋ 新建回忆册':route(4),'本月推荐':route(3)}[label]
    if n==3 and label=='开始制作':return route(4)
    if n==5 and label=='保存封面 · 继续':return 'theme-save'
    if n==6 and label=='下一步 · 编排回忆':return 'select-save'
    if n==8 and label=='使用这个版式':return route(9)
    if n in [9,10,11,12] and label=='保存这一页':return 'page-save'
    if n==10:
        if label.startswith('照片 '):return 'sheet:照片1' if label.startswith('照片 1 ') else 'sheet:选择共同素材'
        if label=='预览这一页':return 'modal:共同照片'
    if n==11 and label=='选择重要时刻':return 'sheet:选择共同素材'
    if n==13 and label=='＋ 添加回忆':return route(8)
    if n==15 and label=='从第一页翻阅':return route('m08-p16?id=book-state&page=page-state')
    if n==16:
        if label in ['上一页','下一页']:return 'reader-prev' if label=='上一页' else 'reader-next'
        if label=='阅读设置与工具':return 'sheet:阅读设置与工具'
        if label=='放大照片':return 'modal:查看照片'
        if label.startswith('当前第') or label=='☷ 目录':return 'sheet:回忆册目录'
        if label=='♧ 书签':return 'bookmark'
        if label=='＋ 留一张补页':return route('m08-p18?id=book-state&page=page-second')
    if n==17:
        return {'全书目录':route(15),'我的书签':'sheet:我的书签','添加补页':route(18),'整理书页':route(13),'管理这本书 · 书名、归档、导出与删除':route(21)}[label]
    if n==18:
        if label=='查看目录':return route(15)
        if label=='下一步 · 写补页':return route('m08-p19?id=book-state&page=page-second&kind=写几句话')
    return old['contract'](page,v)

def custom_control(p,page,v,kind,fixture):
    fixture['seed'](p,page);button=p.locator(v['selector']);before=fixture['store'](p)
    if kind=='close-supplements':
        expect(p.locator('dialog[open]')).to_have_count(1);button.click();expect(p.locator('dialog')).to_have_count(0);assert fixture['store'](p)==before;return
    p.evaluate('window.__bookControlDocument=1729');button.click();wanted='page-state' if kind=='reader-prev' else 'page-third'
    p.wait_for_function('id=>JSON.parse(localStorage.getItem("dujia-prototype-books"))[0].lastPage===id',arg=wanted)
    assert p.evaluate('window.__bookControlDocument')==1729
    expect(p.locator('.page-count')).to_contain_text('1 / 3' if kind=='reader-prev' else '3 / 3')
    assert fixture['clean_read'](fixture['store'](p))==fixture['clean_read'](before)

def main():
    out=ROOT/'evidence/current/book-v2-controls';inventory=json.loads((out/'inventory.json').read_text(encoding='utf-8'));files=dependencies();assert inventory['dependency_files']==files
    fixture=declarations('verify_book_controls.py');cases=[]
    for page in inventory['results']:
        for control in page['controls']:
            if control['visible'] and not control['disabled'] and not control['blocked_by_modal']:
                cases.append((page['page'],control,contract(page['page'],control,fixture)))
    rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for page,v,kind in cases:
            c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai',accept_downloads=True);p=c.new_page();p.set_default_timeout(5000);p.set_default_navigation_timeout(15000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(page=page,selector=v['selector'],label=v['label'],contract=kind,passed=False)
            try:
                if kind in ['close-supplements','reader-prev','reader-next']:custom_control(p,page,v,kind,fixture)
                else:fixture['control'](p,page,v,kind)
                assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            row.update(errors=errors,effective=p.url);rows.append(row);c.close();assert dependencies()==files
            print(('PASS ' if row['passed'] else 'FAIL ')+page+' '+v['label'].replace('\n',' '),flush=True)
        b.close()
    report=dict(dependency_files=files,producer_sha256=sha(Path(__file__)),fixture_sha256=sha(ROOT/'verify_book_controls.py'),inventory_sha256=sha(out/'inventory.json'),browser=version,viewport=[390,844],locale='zh-CN',timezone='Asia/Shanghai',scope='Each enabled current initial control in the declared21 fixtures; no claim of hidden or arbitrary states.',results=rows)
    (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Current initial controls:',sum(r['passed'] for r in rows),'/',len(rows))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
