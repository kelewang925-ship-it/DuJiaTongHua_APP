"""Verify scoped reports, exact control coverage, and actual served bytes."""
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'prototype/evidence/current'
report=json.loads((OUT/'time-controls-results.json').read_text(encoding='utf-8'));files=report['files']
for path,digest in files.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
assert len(report['inventory'])==11 and len(report['results'])==54
assert {(r['page'],r['selector'])for r in report['results']}=={(entry['page'],v['selector'])for entry in report['inventory']for v in entry['controls']}
tests={};total=0
for name,count in [('time-controls-results.json',54),('time-collection-results.json',7),('time-layout-results.json',20)]:
    value=json.loads((OUT/name).read_text(encoding='utf-8'));assert value['files']==files,name;assert len(value['results'])==count and all(r['passed']and not r['errors']for r in value['results']),name;total+=count;tests[name]=dict(cases=count,sha256=hashlib.sha256((OUT/name).read_bytes()).hexdigest())
regression=json.loads((OUT/'time-regression-source.json').read_text(encoding='utf-8'));assert regression['files']==files
for name,count in [('anniversary-flow-results.json',3),('anniversary-state-results.json',7),('capsule-flow-results.json',3),('capsule-state-results.json',5)]:
    value=json.loads((OUT/name).read_text(encoding='utf-8'));meta=regression['reports'][name];assert len(value)==count and all(r['passed']and not r['errors']for r in value),name;assert meta['sha256']==hashlib.sha256((OUT/name).read_bytes()).hexdigest()and meta['exit_code']==0,name;total+=count;tests[name]=meta
assert total==99
layout=json.loads((OUT/'time-layout-results.json').read_text(encoding='utf-8'));assert {(r['page'],r['width'])for r in layout['results']}=={(page,w)for page in ['m04-p09','m04-p13','m04-p10','m04-p14']for w in [320,360,390,414,430]}
for p in (ROOT/'custom').glob('*.html'):assert p.read_bytes()==(ROOT/'pages'/p.name).read_bytes(),p.name
served=[ROOT/'pages'/p.name for p in (ROOT/'custom').glob('*.html')]+list((ROOT/'assets').glob('prototype-*.*'))
def verify(p):
    with urlopen('http://127.0.0.1:8765/'+p.relative_to(ROOT).as_posix(),timeout=15)as response:assert response.status==200 and response.read()==p.read_bytes(),p.name
with ThreadPoolExecutor(max_workers=6)as pool:list(pool.map(verify,served))
queue=json.loads((ROOT/'prototype/queue.json').read_text(encoding='utf-8'));entries=queue if isinstance(queue,list)else queue['pages'];assert len(entries)==114 and not any(r.get('flow_verified')for r in entries)
fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
checkpoint=dict(scope='11 reminder/anniversary/capsule page fixtures; full-product acceptance pending',files=files,fingerprint=fingerprint,tests=tests,named_checks=total,initial_controls=54,http_pages=114,http_shared_assets=len(served)-114,accepted_pages=0)
(OUT/'time-controls-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 提醒、纪念日与胶囊控件执行','','## 范围与结果','','m04-p05 至 m04-p15 的11页声明fixture，54个初始可用控件全部按明确契约实际执行；由报告计算：54个控件、7项额外操作、20项五宽度弹层检查、18项已有流程/异常回归，共99项通过。','', '测试日期2026-10-05是显式fixture，真实执行日期为2026-10-06；两者不同。纪念日repeat为boolean、enabled为boolean、reminderDays为number；当天和未来使用独立稳定ID。胶囊包含草稿/封存/开启三种数据，封存内容在未到期时不显示。所有测试只改隔离浏览器context的数据。','','## 已修复问题','','胶囊收录原先先写重要时刻、再更新胶囊；第二次写入空间不足时留下半完成的时刻。baseline/time-controls-results.json保留修复前失败。现在复用PrototypePreferences.transaction，先更新胶囊关系、再写新增时刻，并在写入失败时回滚。两种集合分别模拟QuotaExceededError，失败保持原内容与当前页，重试进入正确稳定ID；再收录不会重复生成。既有transaction的回滚依赖浏览器仍允许恢复旧值；本轮不声称支持同时拒绝所有写入的故障。baseline/time-observer-restore-results.json是恢复Storage方法时观察器返回函数导致的Illegal invocation诊断，已经改为不返回函数。','','## 指定隐藏状态与回归','','新增7项：两种集合写入失败/回滚/重试/重复收录，纪念日及胶囊编辑器各自按钮和浏览器返回继续/放弃4项，提醒已读写入失败保持未读/不跳转、重试后单条已读1项。既有18项重新运行，覆盖纪念日新建/关联/修改/删除、保存失败及dirty、今天关联日记、闰年/过期、开关/加载/删除失败、日期取消/长输入/空间不足、提醒已读/空态/失效、刷新后删除；胶囊草稿/封存/开启/收录、图片/长输入/过期/缺失/失败重试。','','五宽度320/360/390/414/430px，在34px安全区下检查纪念日/胶囊日期Sheet和两类删除Modal的可达性及44px按钮高度；Escape关闭不写数据。人工查看320px纪念日日期Sheet和胶囊删除确认截图。其余页面状态/动效/实际软键盘并未由这20项覆盖。','','## 控件契约','','| 页面 | 控件 | 实际契约 |','| --- | --- | --- |']
for row in report['results']:lines.append('| '+row['page']+' | '+row['label'].replace('\n',' / ').replace('|','／')+' | '+row['contract']+' |')
lines.extend(['','## 证据边界','','全部99项绑定源码指纹 `'+fingerprint+'`，114页与'+str(len(served)-114)+'共享资产HTTP字节一致，custom/pages一致。以前record-controls的195项属于4f89521来源，本轮没有重新累计为当前全产品通过。旧纪念日/胶囊报告在evidence/history/pre-time-controls-4f89521保留；历史文件夹命名是保留时HEAD，不等同于旧测试来源。','','已建初始控件契约的页面累计46页，余下68页仍需逐项建立与执行。已覆盖页仍有未覆盖动态条件、集合类型/引用恢复、跨模块连续流程、全部设计组件/布局/动效条件；114页最终验收仍为0，目标继续。Android式返回为浏览器历史模拟。'])
(ROOT/'prototype/TIME_CONTROL_EXECUTION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({k:checkpoint[k]for k in ['named_checks','initial_controls','http_pages','http_shared_assets','accepted_pages']}),flush=True)
