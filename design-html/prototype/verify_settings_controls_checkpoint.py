"""Settings exact control coverage, provenance, and served bytes."""
import json,hashlib
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from verify_settings_controls import ROOT,DEMO,source
OUT=ROOT/'evidence/current';files=source();report=json.loads((OUT/'settings-controls-results.json').read_text(encoding='utf-8'));assert report['files']==files
assert len(report['inventory'])==12 and len(report['results'])==81
assert {(r['page'],r['selector'])for r in report['results']}=={(e['page'],v['selector'])for e in report['inventory']for v in e['controls']}
tests={};total=0
for name,count in [('settings-controls-results.json',81),('settings-sheet-guard-results.json',11),('settings-guard-layout-results.json',10)]:
    p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));assert v['files']==files and len(v['results'])==count and all(r['passed']and not r['errors']for r in v['results']),name;total+=count;tests[name]=dict(cases=count,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
v=json.loads((OUT/'settings-guard-layout-results.json').read_text(encoding='utf-8'));assert {(r['kind'],r['width'])for r in v['results']}=={(k,w)for k in ['feedback','phone']for w in [320,360,390,414,430]}
meta=json.loads((OUT/'settings-control-regression-source.json').read_text(encoding='utf-8'));assert meta['files']==files
for name,count in [('settings-flow-results.json',5),('settings-state-results.json',9)]:
    p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));r=meta['reports'][name];assert len(v)==count and all(row['passed']and not row['errors']for row in v)and r['exit_code']==0 and r['sha256']==hashlib.sha256(p.read_bytes()).hexdigest(),name;tests[name]=r;total+=count
assert total==116
for p in (DEMO/'custom').glob('*.html'):assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
served=[DEMO/'pages'/p.name for p in (DEMO/'custom').glob('*.html')]+list((DEMO/'assets').glob('prototype-*.*'))
def verify(p):
    with urlopen('http://127.0.0.1:8765/'+p.relative_to(DEMO).as_posix(),timeout=15)as r:assert r.status==200 and r.read()==p.read_bytes(),p.name
with ThreadPoolExecutor(max_workers=6)as pool:list(pool.map(verify,served))
queue=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'));entries=queue if isinstance(queue,list)else queue['pages'];assert len(entries)==114 and not any(v.get('flow_verified')for v in entries)
fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest();checkpoint=dict(scope='Twelve personal/settings fixtures and editable Sheet protection; full-product acceptance pending',files=files,fingerprint=fingerprint,tests=tests,named_checks=total,initial_controls=81,http_pages=114,http_shared_assets=len(served)-114,accepted_pages=0)
(OUT/'settings-controls-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 个人中心与设置控件执行','','## 当前结果','','m06-p01至p12十二页声明fixture的81个初始可用控件实际执行；11项编辑弹层/版本检查、10项五宽度检查、14项既有正常/异常流程回归，共116项通过。fixture包含四类草稿（本人日记/工坊/胶囊/回忆册），草稿入口检查对应原ID；资料与会话有效、已关联，通知/隐私默认开启，会员未开通。只操作隔离浏览器context数据。','','## 已修复问题','','设置模块edit()共用弹层此前关闭时不保护输入。baseline/settings-sheet-guard-results.json保留四种实际失败：取消/Escape/浏览器历史返回/下滑关闭反馈Sheet，未保存内容丢失。修复复用现有PrototypeUI.protectSheet(form)，关闭钩子要求继续或放弃，继续保留输入；成功保存后commit再关闭，失败保留内容和保护。此帮助函数用于共同昵称、标签、显示与外观、手机号、两步验证、注销身份确认、反馈。没有为每个页面新增独立弹层。检查更新的版本Modal曾在busy按钮禁用时打开，关闭后丢失触发焦点；现在等待检查结束、恢复并聚焦按钮后打开Modal，关闭返回原触发按钮。','','## 隐藏与回归范围','','11项新检查：反馈四种关闭方式继续/放弃4项；失败保留/重试后干净关闭与返回1项；新标签、共同昵称、手机号、验证码的Escape保护4项；动效Select改值后关闭保护与保存1项；检查更新失败不打开Modal、恢复按钮及焦点，重试成功后关闭返回触发按钮1项。注销验证码的未保存关闭并未单独作为这些专项验收，仍需结合其完整动态分支审计。14项重新运行覆盖资料/头像失败/生日取消、草稿路由及加载重试、标签创建修改删除/重复/两集合写入回滚、默认可见范围/通知关闭/回应、实际下载JSON/共同备份/缓存清理、自动备份写入失败、会员/反馈重试、手机号/验证码/注销失败重试、两步验证真实登录流程、关系解除请求/接受拒绝。','','五宽度320/360/390/414/430px共10项，对1000字反馈和手机号编辑设置34px安全区，关闭确认弹层及其可见按钮全部在屏内、按钮宽高至少44px；继续后原输入保留，再确认放弃不写入。人工查看320px两类确认截图。实际软键盘及所有页面视觉/动效不由该项覆盖。','','## 诊断与证据来源','','第一次反馈定位使用get_by_label同时匹配dialog及textarea，产生观察器strict错误，保存在baseline/settings-sheet-label-selector-diagnostic.json。随后采用textbox角色定位，四种丢失输入产品失败另存正确基线。baseline/settings-controls-initial-diagnostic.json保留初轮81控件的两项失败：自动备份被观察器误分类为通知开关，改为明确preferences.autoBackup契约；检查更新关闭后真实焦点丢失，修复后全组重跑。修复更新焦点前的本轮各报告保留在before-update-focus-fix子目录。旧设置流程、状态、布局及检查点保存在evidence/history/pre-settings-controls-e411ac1；文件夹为保留时HEAD，不代表旧测试来源。','','## 初始控件契约','','| 页面 | 控件 | 实际契约 |','| --- | --- | --- |']
for row in report['results']:lines.append('| '+row['page']+' | '+row['label'].replace('\n',' / ').replace('|','／')+' | '+row['contract']+' |')
lines.extend(['','## 验收边界','','源码指纹 `'+fingerprint+'`。116项报告绑定当前源码，114页与37共享资产HTTP字节一致，custom/pages一致。上一阶段工坊125项和其他历史范围保留原来源，没有累计为当前全产品通过。','','累计68页已建立初始控件契约，余下46页继续。已覆盖页完整动态条件、其他集合恢复与引用完整性、全部组件状态/视觉/软键盘/动效、跨模块连续使用仍需推进；114页最终验收0，目标保持执行。Android式返回为浏览器历史模拟。'])
(ROOT/'SETTINGS_CONTROL_EXECUTION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({k:checkpoint[k]for k in ['named_checks','initial_controls','http_pages','http_shared_assets','accepted_pages']}),flush=True)
