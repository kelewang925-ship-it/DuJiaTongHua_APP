"""Exact scoped controls, regression provenance and served-file gate."""
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
import json,hashlib
from verify_workshop_controls import ROOT,DEMO,source
OUT=ROOT/'evidence/current';files=source();report=json.loads((OUT/'workshop-controls-results.json').read_text(encoding='utf-8'));assert report['files']==files
assert len(report['inventory'])==10 and len(report['results'])==92
assert {(r['page'],r['selector'])for r in report['results']}=={(entry['page'],v['selector'])for entry in report['inventory']for v in entry['controls']}
tests={};total=0
for name,count in [('workshop-controls-results.json',92),('workshop-hidden-results.json',12),('workshop-control-layout-results.json',10)]:
    p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));assert v['files']==files and len(v['results'])==count and all(r['passed']and not r['errors']for r in v['results']),name;total+=count;tests[name]=dict(cases=count,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
meta=json.loads((OUT/'workshop-regression-source.json').read_text(encoding='utf-8'));assert meta['files']==files
for name,count in [('workshop-flow-results.json',3),('workshop-state-results.json',8)]:
    p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));r=meta['reports'][name];assert len(v)==count and all(row['passed']and not row['errors']for row in v)and r['exit_code']==0 and r['sha256']==hashlib.sha256(p.read_bytes()).hexdigest(),name;tests[name]=r;total+=count
assert total==125
v=json.loads((OUT/'workshop-control-layout-results.json').read_text(encoding='utf-8'));assert {(r['scenario'],r['width'])for r in v['results']}=={(s,w)for s in ['source-sheet','dirty-modal']for w in [320,360,390,414,430]}
for p in (DEMO/'custom').glob('*.html'):assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
served=[DEMO/'pages'/p.name for p in (DEMO/'custom').glob('*.html')]+list((DEMO/'assets').glob('prototype-*.*'))
def verify(p):
    with urlopen('http://127.0.0.1:8765/'+p.relative_to(DEMO).as_posix(),timeout=15)as r:assert r.status==200 and r.read()==p.read_bytes(),p.name
with ThreadPoolExecutor(max_workers=6)as pool:list(pool.map(verify,served))
queue=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'));entries=queue if isinstance(queue,list)else queue['pages'];assert len(entries)==114 and not any(v.get('flow_verified')for v in entries)
fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest();checkpoint=dict(scope='Ten workshop fixtures and named hidden branches; full-product acceptance pending',files=files,fingerprint=fingerprint,tests=tests,named_checks=total,initial_controls=92,http_pages=114,http_shared_assets=len(served)-114,accepted_pages=0)
(OUT/'workshop-controls-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 童话工坊控件执行','','## 当前结果','','m05-p01至p10十页声明fixture的92个初始可用控件全部按明确行为实际执行；12项隐藏检查、10项五宽度弹层检查、11项已有正常/异常流程回归，共125项通过。六个稳定作品ID覆盖漫画自由/照片/影片草稿、生成中、失败、影片完成；生成中初始控件fixture采用远期dueAt保证逐项检查不会自动离页，真实3秒生成及离开后完成由既有连续流程另行验证。所有测试在隔离浏览器context内运行。','','## 实际修复','','1. W.sources(moment)曾把私密/未发布时刻显示在共同素材Sheet中。添加与共同创作一致的visibility/private与status/draft过滤；已发布且没有可见性字段的历史正常时刻继续可用。baseline/workshop-hidden-results.json记录修复前私密时刻出现；修复后检查私密和草稿均不出现，共同时刻仍可选并能创建稳定作品。更广集合类型、语义与引用完整性仍开放。','2. 主角设定页已有work参数时实际回原创作，但返回按钮仍叫“返回童话工坊”。现在根据work是否存在显示“返回当前创作”或原工坊文字，导航逻辑与稳定ID保持一致。','','## 隐藏分支与异常','','12项检查包括：时刻素材权限1项，日记/照片/时刻/自由回忆四类实际选择并创建作品4项，漫画/照片/影片/主角四个编辑页浏览器返回继续/放弃4项，相册重复保存不重复1项，删除取消与实际删除仅移除目标1项，主角返回文字与原作品ID1项。既有11项重跑覆盖生成失败重试、保存失败/空间不足、主角保存、真实生成/离页完成/播放、素材图片/保存相册失败重试、deadline后取消确认、历史加载/删除失败、收藏及复制权限失败的手动复制入口。','','320/360/390/414/430px，34px安全区下分别检查素材Sheet与300字未保存确认：弹层在屏内，按钮至少44px高，取消/继续不写入数据且保留正文。人工查看320px两张截图。实际软键盘、所有页面/状态视觉及全产品动效并未由这些检查覆盖。','','## 观察器诊断','','baseline/workshop-controls-observer-pet-route.json记录初轮92项中宠物目的地错误期望；bound关系且pet为空时正确入口为m07-p04（领养），已按当前业务规则修正契约。baseline/workshop-hidden-results.json另包含默认日记选项accessible name带CSS选中✓造成exact匹配失败的观察器问题，使用明确.option文本定位实际按钮；同文件两项产品缺口照常保留。baseline/workshop-layout-selector-diagnostic.json记录背景按钮和Sheet checkbox同名的strict匹配失败，修正为dialog内选择。旧工坊状态脚本恢复Storage方法时改为不返回函数，避免Illegal invocation观察器错误。','','## 控件契约','','| 页面 | 控件 | 实际契约 |','| --- | --- | --- |']
for row in report['results']:lines.append('| '+row['page']+' | '+row['label'].replace('\n',' / ').replace('|','／')+' | '+row['contract']+' |')
lines.extend(['','## 来源与验收边界','','源码指纹 `'+fingerprint+'`；125项报告严格绑定当前源码。114页与37共享资产HTTP字节一致，custom/pages一致。旧工坊报告与修复前本轮回归保存在evidence/history/pre-workshop-controls-56ce968；该文件夹命名为保留时HEAD，不等于旧测试来源。上一阶段纪念日/胶囊99项与更早记录195项保持原源码指纹，本轮没有累计为当前全产品通过。','','已建初始控件契约累计56页，余下58页继续逐项执行。所有页面动态条件/其他集合恢复/引用完整性、完整跨模块连续使用、全部组件/视觉/动效与键盘状态仍需推进；114页最终验收0，目标继续。Android式返回是浏览器历史模拟。'])
(ROOT/'WORKSHOP_CONTROL_EXECUTION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({k:checkpoint[k]for k in ['named_checks','initial_controls','http_pages','http_shared_assets','accepted_pages']}),flush=True)
