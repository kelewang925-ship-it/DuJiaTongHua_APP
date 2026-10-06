"""Explicit initial controls on twelve personal/settings fixtures."""
from pathlib import Path
import json,hashlib,traceback,sys
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from audit_runtime import INIT,OBSERVE
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;BASE='http://127.0.0.1:8765/';OUT=ROOT/'evidence/current'
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
def seed(p,page):
    d=data(True);d['dujia-prototype-session']=dict(loggedIn=True,phone='13812345678');d['dujia-prototype-records'][0].update(status='draft',author='小满',title='日记草稿');d['dujia-prototype-works'][0].update(status='draft',name='工坊草稿');d['dujia-prototype-capsules']=[dict(id='settings-capsule',name='胶囊草稿',message='尚未封存',status='draft',opening='2026-12-24',reminder=True)];d['dujia-prototype-books'][0].update(status='draft',name='回忆册草稿');d['dujia-prototype-anniversaries']=[]
    d['dujia-prototype-tags']=[dict(id='settings-tag',name='个人标签',scope='personal'),dict(id='settings-joint-tag',name='共同标签',scope='shared')]
    d['dujia-prototype-preferences']=dict(autoBackup=False,reduceMotion=False,twoFactor=False,language='zh-CN');d['dujia-prototype-pet']=None
    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d);p.goto(BASE+'pages/'+page+'.html')
    if page=='m06-p04':expect(p.locator('.prototype-settings-drafts button')).to_have_count(4)
    p.evaluate('document.fonts.ready')
def store(p):return p.evaluate('JSON.stringify({...localStorage})')
def contract(page,v):
    label=v['label'];s=v['selector']
    if s.startswith('body>nav'):return 'route:'+{'首页':'m03-p02','重要时刻':'m04-p01','工坊':'m05-p01','宠物':'m07-p04','我的':'self'}[label]
    if label=='返回设置':return 'route:m06-p07'
    if label=='返回我的与设置':return 'route:m06-p01'
    if page=='m06-p01':
        return 'route:'+('m06-p02'if label.startswith('小满')else'm06-p03'if label.startswith('我们的小世界')else{'草稿箱':'m06-p04','标签管理':'m06-p05','童话会员':'m06-p06','设置':'m06-p07','帮助与关于':'m06-p12'}[label])
    if page=='m06-p02':
        if s=='#birthday':return 'sheet:你的生日'
        if label=='更换头像':return 'native-file'if s=='#avatar'else'file'
        if s=='#save':return 'profile-save'
    if page=='m06-p03':
        if label.startswith('共同昵称'):return 'sheet:共同昵称'
        if label=='共同头像':return 'world-file'
        if label.startswith('共同空间设置'):return 'route:m06-p09'
        if label=='关联状态':return 'modal:关联状态'
        if label=='解除关联':return 'modal:请求解除关联？'
    if page=='m06-p04':
        if label.startswith('日记草稿'):return 'draft:m03-p05:audit-diary'
        if label.startswith('工坊草稿'):return 'draft:m05-p03:audit-work'
        if label.startswith('胶囊草稿'):return 'draft:m04-p13:settings-capsule'
        if label.startswith('回忆册草稿'):return 'draft:m08-p04:book-state'
        if label=='刷新草稿箱':return 'refresh'
    if page=='m06-p05':return 'sheet:新建标签'if label=='新建标签'else'sheet:'+label
    if label=='开通童话会员':return 'modal:开通演示会员？'
    if label=='查看会员说明 ›':return 'modal:童话会员说明'
    if page=='m06-p07':
        if label in ['账号与安全','隐私与共同可见','通知设置','数据与存储']:return 'route:'+{'账号与安全':'m06-p08','隐私与共同可见':'m06-p09','通知设置':'m06-p10','数据与存储':'m06-p11'}[label]
        if label in ['显示与外观','语言']:return 'sheet:'+label
    if label=='退出登录':return 'modal:退出当前登录？'
    if page=='m06-p08':
        if label=='修改密码':return 'route:m01-p04'
        if label=='绑定手机':return 'sheet:绑定手机（本地演示）'
        if label.startswith('登录设备'):return 'modal:登录设备'
        if label.startswith('两步验证'):return 'sheet:开启两步验证演示'
        if label=='注销账号':return 'modal:注销本地演示账号？'
    if s=='#scope':return 'sheet:新记录默认可见范围'
    if s=='#auto':return 'auto'
    if v['role']=='switch':return 'switch'
    if page=='m06-p11':
        if s=='#export':return 'export'
        if s=='#backup':return 'backup'
        if s=='#auto':return 'auto'
        if label=='存储空间管理':return 'modal:本地存储空间'
        if s=='#cache':return 'modal:清理浏览记录缓存？'
    if page=='m06-p12':return ('sheet:'if label=='意见反馈'else'modal:')+('版本信息'if label=='检查更新'else label)
    if v['native_input']:return 'input'
    raise AssertionError((page,label,'missing contract'))
def control(p,page,v,kind):
    seed(p,page);button=p.locator(v['selector']);expect(button).to_be_visible();expect(button).to_be_enabled();before=store(p)
    if kind=='input':
        if button.get_attribute('type')=='color':button.fill('#cc8844');expect(button).to_have_value('#cc8844')
        else:limit=int(button.get_attribute('maxlength'));button.fill('心'*(limit+8));assert len(button.input_value())==limit;expect(button).to_be_focused()
        assert store(p)==before;return
    if kind in ['file','native-file','world-file']:
        from PIL import Image
        from io import BytesIO
        stream=BytesIO();Image.new('RGB',(30,20),'blue').save(stream,format='PNG');item=dict(name='avatar.png',mimeType='image/png',buffer=stream.getvalue())
        if kind=='native-file':button.set_input_files(item)
        else:
            with p.expect_file_chooser()as info:button.click()
            info.value.set_files(item)
        if kind=='world-file':expect(p.locator('.portrait')).to_contain_text('已设置');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-relationship")).profile.avatar').startswith('data:image/');return
        expect(p.locator('#avatar-preview')).to_be_visible();assert store(p)==before;return
    if kind=='export':
        with p.expect_download()as info:button.click()
        download=info.value;assert download.suggested_filename=='dujia-records.json';value=json.loads(Path(download.path()).read_text(encoding='utf-8'));assert value['format']=='dujia-prototype-backup-v1'and value['scope']=='accessible';assert store(p)==before;return
    key=button.get_attribute('data-key');old=button.get_attribute('aria-checked')
    button.click()
    if kind.startswith('route:'):
        dest=kind.split(':')[1]
        if dest=='self':assert page+'.html'in p.url
        else:p.wait_for_url('**/'+dest+'.html*')
    elif kind.startswith('draft:'):_,dest,id=kind.split(':');p.wait_for_url('**/'+dest+'.html?id='+id)
    elif kind.startswith(('sheet:','modal:')):expect(p.locator('dialog h2')).to_have_text(kind.split(':')[1]);p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);expect(button).to_be_focused()
    elif kind=='profile-save':p.wait_for_url('**/m06-p01.html');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-profile")).nickname')=='小满';return
    elif kind=='switch':
        expect(button).to_have_attribute('aria-checked','false'if old=='true'else'true');assert p.evaluate('([k,f])=>JSON.parse(localStorage.getItem(k))[f]',['dujia-privacy'if page=='m06-p09'else'dujia-notifications',key])==(old!='true');return
    elif kind=='refresh':expect(p.locator('.prototype-settings-drafts')).to_have_attribute('aria-busy','true');expect(p.locator('.prototype-settings-drafts button')).to_have_count(4)
    elif kind=='backup':expect(p.locator('.prototype-toast')).to_contain_text('备份已创建');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-backup")).scope')=='shared';return
    elif kind=='auto':expect(button).to_have_attribute('aria-checked','true');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-preferences")).autoBackup');return
    else:raise AssertionError(kind)
    assert store(p)==before
def main():
    files=source();inventory=[];rows=[]
    with sync_playwright()as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for i in range(1,13):
            page=f'm06-p{i:02}';c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');c.add_init_script(INIT);p=c.new_page();p.set_default_timeout(4500);seed(p,page);controls=[v for v in p.evaluate(OBSERVE)['controls']if v['visible']and not v['disabled']];inventory.append(dict(page=page,effective=p.url,controls=controls));print(page,len(controls),flush=True);c.close()
        if '--inventory'not in sys.argv:
            for entry in inventory:
                for v in entry['controls']:
                    c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));kind=contract(entry['page'],v)
                    try:control(p,entry['page'],v,kind);assert not errors;row=dict(passed=True)
                    except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
                    row.update(page=entry['page'],selector=v['selector'],label=v['label'],contract=kind,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+entry['page']+' '+v['label'].replace('\n',' '),flush=True);c.close()
        b.close()
    assert files==source();(OUT/('settings-control-inventory.json'if '--inventory'in sys.argv else'settings-controls-results.json')).write_text(json.dumps(dict(files=files,inventory=inventory,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if all(r['passed']for r in rows)else 1)
if __name__=='__main__':main()
