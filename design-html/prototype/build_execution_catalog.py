"""Join current observations with actual executions without promoting candidates to acceptance."""
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;OUT=ROOT/'evidence/current'
def clean(value):return str(value).replace('|','／').replace('\r',' ').replace('\n',' ').strip()
def table(values):return '| '+' | '.join(clean(v) for v in values)+' |'

def main():
    report=json.loads((OUT/'current-runtime-summary.json').read_text(encoding='utf-8'))
    observed=json.loads((OUT/'current-runtime-inventory.json').read_text(encoding='utf-8'))
    executed=json.loads((OUT/'onboarding-control-results.json').read_text(encoding='utf-8'))
    overlays=json.loads((OUT/'onboarding-overlay-results.json').read_text(encoding='utf-8'))
    assert len(observed)==228 and not report['errors']
    for path,digest in report['files'].items():assert hashlib.sha256((DEMO/path).read_bytes()).hexdigest()==digest, 'Stale runtime inventory: '+path
    fingerprint=hashlib.sha256(json.dumps(report['files'],sort_keys=True).encode()).hexdigest()
    assert all(r.get('source_fingerprint')==fingerprint for r in executed+overlays), 'Execution results are stale or lack source fingerprints; rerun the control and overlay scripts'
    eligible={(r['id'],c['selector']) for r in observed if r['scenario']=='empty' and r['id'].startswith(('m01-','m02-')) for c in r['observed']['controls'] if c['visible'] and not c['disabled']}
    assert eligible=={(r['id'],r['selector']) for r in executed}, 'Control execution coverage differs from current initial account/relationship inventory'
    labels={(r['id'],c['selector']):c['label'] for r in observed if r['scenario']=='empty' for c in r['observed']['controls']}
    assert all(labels[(r['id'],r['selector'])]==r['label'] for r in executed), 'Executed control names differ from current inventory'
    by_key={(r['id'],r['selector']):r for r in executed}
    lines=['# 控件行为与执行清单（持续实施）','',f'当前运行源码指纹：`{fingerprint}`。114页空／有数据共228次观察、{report["controls_observed"]}条控件记录；一条记录对应请求页+场景+实际节点，重定向及重复控件不应当作独立产品控件数量。','',f'账号／关系17页的{len(executed)}个初始可用控件有明确契约并实际执行；{sum(r["passed"] for r in executed)}项通过。另有{len(overlays)}条弹层/重发检查，{sum(r["passed"] for r in overlays)}项通过。仅证明声明fixture和代表性操作；同一个控件的其他数据、错误、返回、长输入与动态分支仍需验收。114页最终验收0页。','','## 前置条件与证据','','- 每次操作独立浏览器上下文，使用空集合、未绑定关系与本地演示资料；登录/注册/重置按钮先填入有效值，验证码为284631。重置使用已验证recovery challenge，避免把无资格重置认定为成功。','- 分享等待固定为manual响应；剪贴板检查使用已授予本地剪贴板权限的Chrome，读取真实值；下载检查真实SVG内容。没有真实短信、微信发送或后端。','- 原生输入检查焦点、输入/勾选、值和未提交数据不变；分组验证码/邀请码验证当前清洗规则。不是全部输入错误、长度和键盘行为验收。','- 全量观察：current-runtime-inventory.json；逐控件契约和结果：onboarding-control-results.json；弹层实际出现的控件与操作结果：onboarding-overlay-results.json。文件均位于evidence/current。','','## 全部观察节点','','| 请求页／场景 | 实际页 | 控件 | 可用性 | 明确契约／观察处理 | 执行证据 |','| --- | --- | --- | --- | --- | --- |']
    for row in observed:
        actual=Path(row['effective'].split('?')[0]).stem
        for c in row['observed']['controls']:
            result=by_key.get((row['id'],c['selector'])) if row['scenario']=='empty' else None
            handler=c['inline'] or c['href'] or '; '.join(e['handler'] for e in c['own_events']) or ('原生输入/选择器' if c['native_input'] else '事件委托候选，待复核')
            contract=result['contract'] if result else '观察候选：'+handler[:450]
            proof=('初始代表性执行通过' if result['passed'] else '执行失败：'+result['failure'][-180:]) if result else '此状态未逐项执行'
            lines.append(table([row['id']+'／'+row['scenario'],actual,c['label'],'可用' if c['visible'] and not c['disabled'] else '隐藏/禁用',contract,proof]))
    lines+=['','## 实际出现的隐藏弹层','','这里只登记本批测试真正打开的弹层。相同标题出现于不同来源时分别保留；未执行的控件仍待逐项补充，不能从弹层打开成功推断全部按钮正常。','','| 来源页／案例 | 弹层 | 类型 | 出现的控件 | 案例结果 |','| --- | --- | --- | --- | --- |']
    for row in overlays:
        for overlay in row.get('overlays',[]):
            controls=', '.join(c['label'] or c['type'] for c in overlay['controls'])
            lines.append(table([row['page']+'／'+row['action'],overlay['title'],overlay['type'],controls,'通过' if row['passed'] else '失败']))
    (ROOT/'CONTROL_BEHAVIORS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    nav=['# 导航关系与执行证据（持续实施）','',f'源码指纹：`{fingerprint}`。完整页面类型见PAGE_CATALOG.md；{len(json.loads((OUT/"current-navigation-candidates.json").read_text(encoding="utf-8")))}条回调引用候选和{len(report["redirects"])}次条件重定向见CURRENT_NAVIGATION.md。动态ID、数字拼接和条件结果仍需补全；本文件不宣称完整导航终验。','','## 本批实际执行的初始入口','','有效提交前置条件见CONTROL_BEHAVIORS.md。返回按钮在直接进入页面的上下文验证fallback，不能由此证明从所有来源进入后的历史返回。','','| 来源页 | 控件 | 触发契约 | 实际落点 | 结果 |','| --- | --- | --- | --- | --- |']
    for row in executed:
        if row['contract'].split(':')[0] in ['route','login','register','recovery','reset','retry','verify','invite','bind','cancel','profile','renew']:
            nav.append(table([row['id'],row['label'],row['contract'],Path(row['effective'].split('?')[0]).stem,'通过' if row['passed'] else '失败']))
    nav+=['','## 弹层后的实际导航','','| 来源页 | 操作 | 实际落点 | 结果 |','| --- | --- | --- | --- |']
    for row in overlays:
        if Path(row['effective'].split('?')[0]).stem!=row['page']:
            nav.append(table([row['page'],row['action'],Path(row['effective'].split('?')[0]).stem,'通过' if row['passed'] else '失败']))
    nav+=['','## 五Tab与返回规则','','首页→m03-p02、重要时刻→m04-p01、工坊→m05-p01、宠物→m07-p03、我的→m06-p01；空数据或等待领养由控制器决定实际页。Tab使用replace，详情和完整编辑任务使用页面导航，局部选择使用Sheet，危险决策使用Modal。实际行为及未保存规则见INTERACTION_RULES.md；已有五Tab运行证据见PRIMARY_NAVIGATION_IMPLEMENTATION.md，不自动计入本批控件数量。','','## 未闭环','','其余模块动态列表条目、全部隐藏弹层、私密与已删除引用、任务提交后历史/BFCache、错误重试后的落点与全部一级入口返回仍需实际执行。旧候选图的无入边不是死路证明。完整产品首次使用串行终验和原生端返回都未完成。']
    (ROOT/'NAVIGATION.md').write_text('\n'.join(nav)+'\n',encoding='utf-8',newline='\n')
    flow=['# 流程测试报告（阶段证据，未最终验收）','',f'当前源码指纹：`{fingerprint}`。114页最终验收仍为0页；本报告分开记录全页观察与本批实际操作，不将事件绑定、候选出口或历史阶段结果计为已完成完整产品流程。','','## 当前证据','','| 检查 | 数量 | 结果与边界 |','| --- | ---: | --- |',table(['全页空／有数据观察',len(observed),f'114个请求页各两次；脚本/观察错误{len(report["errors"])}，无绑定/委托候选{len(report["unbound_or_delegated_candidates"])}。不执行所有事件']),table(['初始账号／关系控件',len(executed),f'{sum(r["passed"] for r in executed)}通过；17页当前空态所有可用初始控件，一个声明前置条件/代表性操作']),table(['隐藏弹层与重发',len(overlays),f'{sum(r["passed"] for r in overlays)}通过；协议确认、验证方式、剪贴板、实际下载、分享等待、日期回填/取消/未保存保护及重发恢复']),table(['导航回调引用候选',len(json.loads((OUT/'current-navigation-candidates.json').read_text(encoding='utf-8'))),'618为本次生成值，未来以当前文件为准；包含fallback和条件分支，不是618条已走通路径']),table(['条件重定向',len(report['redirects']),'保留请求与实际落点；未进入的原状态仍需特定条件触发']),'','本批有名实际操作检查为81+14=95，重复运行不重复累计。最初分享下载探测使用了全页同名按钮选择器，发生观察器strict-mode错误，修正为当前dialog范围后通过；原错误保留在baseline/onboarding-overlay-observer-error.json，不算产品缺陷。','','## 各模块覆盖边界','','| 模块 | 页面数 | 当前空／有数据观察节点记录 | 本批初始控件实际执行 | 全部页面验收 |','| --- | ---: | ---: | ---: | --- |']
    for module in range(1,9):
        prefix='m'+str(module).zfill(2)+'-';module_rows=[r for r in observed if r['id'].startswith(prefix)]
        flow.append(table([prefix[:-1],len(module_rows)//2,sum(len(r['observed']['controls']) for r in module_rows),sum(r['id'].startswith(prefix) for r in executed),'未完成']))
    flow+=['','其余模块已有模块实施记录与历史流程证据，本批列为0仅表示本批尚未逐控件执行，不表示没有实现。源文件哈希不同的历史报告不直接升级为当前全产品验收。','','## 未完成的最终门槛','','- 114页每个控件全部适用状态、动态列表条目、Modal/Sheet及真实导航完整契约与执行。','- 首次完全无预置数据→登录→绑定→首页→内容创建/编辑/阅读/删除的连续用户流程，以及宠物/工坊/回忆册跨模块闭环。','- 破损数据、图片/加载/保存/生成失败的可恢复性，保留有效数据和未提交输入。','- 全部任务来源、提交后历史、快速返回、缓存恢复与弹层优先级；浏览器证据不等于Android原生验证。','- 当前版本全部状态的五宽度、长输入、热区、滚动、键盘、安全区、视觉与访问性验证。','','复查脚本：audit_current_runtime.py、build_current_catalog.py、verify_onboarding_controls.py、verify_onboarding_overlays.py、build_execution_catalog.py。脚本依赖当前本地8765预览、独立Chrome与已配置Python/Playwright环境。最后两类结果必须与当前运行源码哈希匹配，不跳过失败行；详细原始结果保留于evidence/current。']
    (ROOT/'FLOW_TEST_REPORT.md').write_text('\n'.join(flow)+'\n',encoding='utf-8',newline='\n')
    for name in ['CURRENT_PAGES.md','CURRENT_CONTROL_AUDIT.md']:
        p=ROOT/name;body='\n'.join(line for line in p.read_text(encoding='utf-8').split('\n') if not line.startswith('运行源码指纹：'));heading='运行源码指纹：`'+fingerprint+'`；日期固定为2026-10-05的观察fixture，不是当前设备日期。绑定观察不等于实际执行。'
        p.write_text(body.split('\n',1)[0]+'\n\n'+heading+'\n\n'+body.split('\n',1)[1].lstrip('\n'),encoding='utf-8',newline='\n')
    summary={'source_fingerprint':fingerprint,'requested_pages':114,'observations':228,'observed_control_records':report['controls_observed'],'initial_account_relationship_controls':len(executed),'control_checks_passed':sum(r['passed'] for r in executed),'overlay_and_resend_checks':len(overlays),'overlay_checks_passed':sum(r['passed'] for r in overlays),'final_accepted':0}
    (OUT/'control-execution-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(summary,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
