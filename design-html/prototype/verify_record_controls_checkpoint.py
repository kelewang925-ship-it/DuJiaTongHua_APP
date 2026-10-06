"""Verify current home/diary/photo control contracts and named regressions."""
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlparse,parse_qs
from concurrent.futures import ThreadPoolExecutor
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'prototype/evidence/current'
report=json.loads((OUT/'record-controls-results.json').read_text(encoding='utf-8'));files=report['files']
for path,digest in files.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
initial=[r for r in report['results']if 'contract'in r];assert len(initial)==92 and len(report['inventory'])==12
assert {(r['page'],r['selector'])for r in initial}=={(r['page'],c['selector'])for r in report['inventory']for c in r['controls']}
for row in initial:
    expected_id={'route:m03-p07':'audit-private','route:m03-p08':'audit-diary','route:m03-p12':'audit-photo','route:m08-p15':'book-state','route:m04-p10':'audit-anniversary'}.get(row['contract'])
    if row['contract']=='route:m03-p05'and row['page']in ['m03-p07','m03-p08']:expected_id='audit-private'if row['page']=='m03-p07'else'audit-diary'
    if row['contract']=='route:m03-p11'and row['page']=='m03-p12':expected_id='audit-photo'
    if expected_id:assert parse_qs(urlparse(row['effective']).query).get('id')==[expected_id],row['case']
expected={'record-controls-results.json':109,'record-reply-layout-results.json':10,'diary-flow-results.json':4,'photo-flow-results.json':3,'new-user-journey-results.json':2,'record-back-reentry-results.json':6,'moment-controls-results.json':53,'onboarding-flow-results.json':8};tests={}
for name,count in expected.items():
    p=OUT/name;value=json.loads(p.read_text(encoding='utf-8'));rows=value['results']if isinstance(value,dict)else value
    assert len(rows)==count and all(r['passed']and not r.get('errors')for r in rows),name
    actual=value['files']if isinstance(value,dict)else json.loads((OUT/name.replace('-results.json','-source.json')).read_text(encoding='utf-8'))['files'];assert actual==files,name
    tests[name]={'checks':count,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
paths=[f'pages/{p.name}'for p in sorted((ROOT/'custom').glob('*.html'))]+[p for p in files if p.startswith('assets/')]
def served(path):
    with urlopen('http://127.0.0.1:8765/'+path,timeout=15)as r:assert r.status==200 and r.read()==(ROOT/path).read_bytes(),path
    if path.startswith('pages/'):assert (ROOT/path).read_bytes()==(ROOT/'custom'/Path(path).name).read_bytes(),path
with ThreadPoolExecutor(max_workers=4)as pool:list(pool.map(served,paths))
queue=json.loads((ROOT/'prototype/queue.json').read_text(encoding='utf-8'));assert len(queue)==114 and not any(r['flow_verified']for r in queue)
fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
checkpoint={'scope':'92 initial controls across 12 declared home/diary/photo fixtures; nine hidden operation groups; four reply exit paths, two privacy states, valid date fallback and real caption search; 10 width checks and nine normal regressions. Whole-product conditions and final acceptance incomplete.','source_fingerprint':fingerprint,'files':files,'tests':tests,'named_checks':sum(t['checks']for t in tests.values()),'http_pages':114,'http_shared_assets':37,'accepted_pages':0}
(OUT/'record-controls-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lines=['# 首页、日记与照片控件执行记录','',f'源码指纹：`{fingerprint}`。12页各一个声明fixture的全部92个初始可用控件；不代表全部数据前置条件或114页最终验收。原始节点、label、selector、契约及结果见evidence/current/record-controls-results.json。','', '| 页面/场景 | 控件 | 实际契约 | 结果 |','| --- | --- | --- | --- |']
for r in initial:lines.append('| '+ ' | '.join(str(r[k]if k!='page'else r['page']+'/'+r['scenario']).replace('\n',' / ').replace('|','／')for k in ['page','label','contract'])+' | 通过 |')
lines+=['','契约说明：route/navigation实际进入目标或条件redirect；当前主Tab滚回顶部；input/query/mood校验输入长度、选择和focus；file触发系统文件选择并实际预览；diary-draft/save及photo-save持久化后回列表；reply实际追加回应、清空并可离开；emoji追加表情且聚焦；sheet验证标题、关闭及焦点回到入口；tab筛选/草稿有可用空态；refresh显示区域busy并恢复列表；search-chip实际搜索并保存历史；clear-query清空且回到可继续输入的搜索入口。','','## 修复与隐藏分支','', '日记和照片未发送回应离开时使用现有guard确认继续/放弃；成功发送后清空并commit，失败保留输入和存储，照片成功增加共享Toast。回应隐私关闭时禁用表情。日记列表/详情对缺少createdAt但有date的有效记录用date回退，解析失败显示日期未记录。照片心情caption参与搜索与结果摘要；结果清除搜索后入口聚焦。日记编辑器返回aria-label改为实际日记列表。共享浏览器返回在确认前恢复guard节点，防止选择继续后快速再次返回的空窗；6项重复返回专项每项连续继续3次，最后确认放弃。', '', '隐藏检查：两类删除取消/失败/重试及保存其他记录；两类回应失败保留/重试并干净返回；两类筛选应用/清除；照片日期与标签回填/取消和dirty；搜索失败重试；日记照片添加后移除。四种未发送回应返回检查、两种关闭回应权限、有效日期回退、实际输入caption搜索另列。320/360/390/414/430px每类回应确认各一次，共10项，检查44px热区、安全区、继续后300字仍保留。', '', '## 证据与边界', '', 'baseline/record-controls-results.json保留原源码8项失败（四种丢失输入、两个权限表情仍可用、日期显示Invalid Date、caption遗漏搜索）。baseline/record-search-focus-results.json记录随后逐控件执行的焦点缺口；probe手动观察焦点在body，修复后全组重跑。随后record-overlay-and-back-race-results.json包含两个同名selector观察器错误和两个实际快速返回竞态，分别修正选择器与共享guard；原始诊断保留。record-reentry-dialog-expectation与record-reentry-close-expectation记录修复后仅留在当前页/再次显示确认的合法时序被观察器误判；最终快速返回专项验证输入和页面不丢、允许新确认、稳定后仍能确认离开。共享返回变更后重新执行时刻6页53项控件/隐藏操作和8条账号/关系流程；原完整时刻67项及旧账号82+14汇总仍保持阶段来源。此前全114页扫描属于aed142d。', '', '本批195项通过并检查114页/37共享资产HTTP与工作区一致。其余79页初始控件契约、已覆盖页全部动态分支/记录结构与引用、所有设计组件/布局条件、跨模块连续流程仍开放；114页最终验收0。Android式返回为浏览器历史模拟，不是原生Android设备验收。']
(ROOT/'prototype/RECORD_CONTROL_EXECUTION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:checkpoint[k]for k in ['named_checks','http_pages','http_shared_assets','accepted_pages']}),flush=True)
