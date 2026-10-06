"""Prove six-page control/overlay evidence without relabeling historical whole-product runs."""
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'prototype/evidence/current'
report=json.loads((OUT/'moment-controls-results.json').read_text(encoding='utf-8'));files=report['files']
for path,digest in files.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
assert len(report['inventory'])==6 and sum(len(r['controls'])for r in report['inventory'])==44
initial=[r for r in report['results'] if 'contract' in r];assert len(initial)==44
assert {(r['page'],r['selector'])for r in initial}=={(r['id'],c['selector'])for r in report['inventory']for c in r['controls']}
expected={'moment-controls-results.json':53,'moment-reply-layout-results.json':5,'moment-flow-results.json':3,'moment-state-results.json':6};tests={}
for name,count in expected.items():
    path=OUT/name;result=json.loads(path.read_text(encoding='utf-8'));rows=result['results'] if isinstance(result,dict)else result
    assert len(rows)==count and all(r['passed'] and not r.get('errors')for r in rows),name
    if isinstance(result,dict):assert result['files']==files,name
    else:assert json.loads((OUT/name.replace('-results.json','-source.json')).read_text(encoding='utf-8'))['files']==files,name
    tests[name]={'checks':count,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
paths=[f'pages/{p.name}'for p in sorted((ROOT/'custom').glob('*.html'))]+[p for p in files if p.startswith('assets/')]
def served(path):
    with urlopen('http://127.0.0.1:8765/'+path,timeout=15)as r:assert r.status==200 and r.read()==(ROOT/path).read_bytes(),path
    if path.startswith('pages/'):assert (ROOT/path).read_bytes()==(ROOT/'custom'/Path(path).name).read_bytes(),path
with ThreadPoolExecutor(max_workers=4)as pool:list(pool.map(served,paths))
queue=json.loads((ROOT/'prototype/queue.json').read_text(encoding='utf-8'));assert len(queue)==114 and not any(r['flow_verified']for r in queue)
fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
checkpoint={'scope':'44 initial controls in six moment/reply fixtures, five hidden operation groups, four dirty-sheet exit paths, five widths and nine specified moment regressions. Whole-product initial controls/conditions remain incomplete.','source_fingerprint':fingerprint,'files':files,'tests':tests,'named_checks':sum(t['checks']for t in tests.values()),'http_pages':114,'http_shared_assets':37,'accepted_pages':0}
(OUT/'moment-controls-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lines=['# 时刻册与留言控件执行记录','',f'源码指纹：`{fingerprint}`。6页各一个声明fixture的全部44个初始可用控件；不代表全部数据条件或全产品验收。原始节点与执行结果见evidence/current/moment-controls-results.json。','', '| 页面/场景 | 控件 | 实际契约 | 结果 |','| --- | --- | --- | --- |']
for r in initial:lines.append('| '+ ' | '.join(str(r[k] if k!='page' else r['page']+'/'+r['scenario']).replace('\n',' / ').replace('|','／')for k in ['page','label','contract'])+' | 通过 |')
lines+=['','契约说明：route按业务进入目标页面；nav包含主导航replace、当前Tab滚回顶部和宠物前置状态redirect；input包含文字长度上限和类型标签/键盘选择；file实际触发文件选择并预览；save写入后返回列表；read-reply保存已读后进入原时刻；modal/sheet确认标题、关闭、焦点回到入口；expand展开/收起；refresh加载禁用后恢复列表；collect-empty进入编辑器再打开无共同记录出口。','','## 隐藏分支','', '删除取消/失败/重试且不删关联记录；回应失败保留/重试成功；关闭回应隐私；日期回填及编辑器dirty；列表加载失败/重试。回应输入后取消、Escape、浏览器返回、拖动均确认继续/放弃并还原焦点；五宽度检查安全区、按钮44px与300字限制。','','## 复现及诊断','', 'baseline/moment-controls-results.json保留原源码的4种回应关闭失败，输入直接丢失。修复复用protectSheet，不新增状态架构；发送失败不提交，成功后commit再关闭。baseline/moment-radio-observer-error.json的3项失败是测试直接点击pointer-events:none的原生radio，修正为实际label点击并检验键盘Space；baseline/moment-state-fixture-errors.json的两项失败是旧fixture私密回应缺少author触发正确资料恢复、空列表出口错误期待正常列表。诊断不计作产品缺陷。五宽度截图见evidence/current/moment-reply-discard-*.png。', '', '## 边界','', '全114页动态分支仍待执行；其余91页初始控件契约待完善，历史账号17页和本批6页的代表性控件不等于23页最终验收。时刻集合损坏与引用异常、更多数据条件、照片/日记回应dirty、重要删除DangerButton、跨模块连续流程仍开放。此前完整全页扫描属于aed142d；上阶段50项登录/邀请检查属于94a7065，未重跑为本批结果。']
(ROOT/'prototype/MOMENT_CONTROL_EXECUTION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:checkpoint[k]for k in ['named_checks','http_pages','http_shared_assets','accepted_pages']}),flush=True)
