"""Join the full static and runtime scan; distinguish observed and planned behavior."""
from pathlib import Path
import json
import re

OUT=Path(__file__).resolve().parent
def clean(value):return str(value).replace('|','／').replace('\n',' ').strip()

def main():
 inventory=json.loads((OUT/'baseline-inventory.json').read_text(encoding='utf-8'))
 runtime=json.loads((OUT/'baseline-runtime.json').read_text(encoding='utf-8'))
 by_id={r['id']:r for r in runtime}
 rows=[];queue=[]
 lines=['# 全量控件行为审计基线','', '基于全部页面源代码和隔离浏览器注册事件观察生成。每项列出已观察的绑定及处理代码；存在绑定不等于业务流程已闭环。所有项仍需要真实点击/输入流程验收。','', '| 页面 | 序号 | 名称 | 当前行为类型 | 已绑定处理 | 待验证 |','| --- | ---: | --- | --- | --- | --- |']
 states=['# 114 页状态补齐矩阵','', '下表是实施前的适用状态设计。既有状态稿已计入页面清单；“需要”不代表已经实现或通过测试。','', '| 页面 | 名称 | 类型 | 需要的状态/交互 | 执行状态 |','| --- | --- | --- | --- | --- |']
 list_ids={'m03-p01','m03-p02','m03-p04','m03-p06','m03-p09','m03-p10','m04-p01','m04-p02','m04-p05','m04-p06','m04-p07','m04-p08','m04-p12','m04-p16','m04-p17','m05-p01','m05-p02','m05-p09','m06-p04','m06-p05','m07-p11','m07-p12','m07-p15','m07-p18','m07-p21','m07-p22','m08-p01','m08-p02','m08-p03','m08-p06','m08-p13','m08-p15'}
 for page in inventory['pages']:
  observed=by_id[page['id']]
  assert len(page['controls'])==len(observed['controls']),(page['id'],len(page['controls']),len(observed['controls']))
  for index,(static,c) in enumerate(zip(page['controls'],observed['controls']),1):
   assert static['tag'].upper()==c['tag'],(page['id'],index)
   code=c['inline']+'; '+ '; '.join(e['handler'] for e in c['own_events'])
   if c['type']=='submit':code+='; '+ '; '.join(e['handler'] for e in c['form_events'] if e['type']=='submit')
   if not code.strip('; '): code='; '.join(e['handler'] for a in c['ancestor_events'] for e in a['events'])
   routes=sorted(set(re.findall(r'm\d{2}-p\d{2}(?=\.html)',code+' '+(c['href'] or ''))))
   kinds=[]
   if c['native_input']:
    kinds.append('文件选择' if c['type']=='file' else '勾选/切换' if c['type'] in {'checkbox','radio'} else '原生选择器' if c['tag']=='SELECT' else '输入/键盘')
   if routes or c['href'] and c['href']!='#':kinds.append('页面跳转')
   if re.search(r'(setAttribute|classList|hidden|\.style\.|\.value|textContent)',code):kinds.append('状态/内容变化')
   if re.search(r'(save|persist|setItem|submit|FormData)',code,re.I):kinds.append('提交/本地保存候选')
   if re.search(r'(show\(|tell\(|notify\(|toast)',code):kinds.append('提示反馈')
   if re.search(r'(confirm\(|prompt\(|dialog|Modal)',code):kinds.append('弹窗/确认')
   if re.search(r'(navigator.share|clipboard|download)',code):kinds.append('分享/复制/导出')
   if not kinds:kinds.append('函数调用/需核对上下文')
   row={'page':page['id'],'index':index,'selector':c['selector'],'name':c['label'],'types':kinds,'observed_handler':code,'routes':routes,'visible':c['visible'],'disabled':c['disabled'],'status':'observed-not-flow-tested'}
   rows.append(row)
   lines.append('| '+' | '.join(clean(x) for x in [page['id'],index,c['label'],'、'.join(kinds),code[:600] or '原生输入；关联行为见源页面', '跨页数据/返回/异常/触发条件'])+' |')
  form_controls=any(c['native_input'] and c['type'] not in {'checkbox','radio','hidden'} for c in observed['controls'])
  needed=['返回/fallback','pressed/focus/reduced-motion']
  if page['id'] in list_ids:needed+=['loading skeleton','empty + CTA','load error + retry','条件筛选/状态变化']
  if form_controls:needed+=['focus/typing/filled','blur校验/error/disabled','提交loading/success/failure','dirty返回保护']
  if page['id']=='m05-p06':needed+=['生成progress','取消保留参数','成功/失败/超时分支']
  if any(re.search(r'删除|解除|退出',c['label']) for c in observed['controls']):needed+=['危险确认/取消安全','成功反馈及数据更新']
  if re.search(r'详情|翻阅|阅读|倒计时',page['design_title']):needed+=['ID上下文','缺失/权限失效恢复','编辑后重读数据']
  queue.append({'id':page['id'],'title':page['design_title'],'baseline_sha256':page['sha256'],'controls':len(page['controls']),'source_scanned':True,'runtime_observed':True,'needed_states':needed,'status':'audited-awaiting-implementation','flow_verified':False})
  states.append('| '+' | '.join(clean(x) for x in [page['id'],page['design_title'],page['type'],'；'.join(needed),'待实施/流程验证'])+' |')
 assert len(rows)==653 and len(queue)==114
 (OUT/'CONTROL_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 (OUT/'STATE_MATRIX.md').write_text('\n'.join(states)+'\n',encoding='utf-8')
 (OUT/'control-audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 (OUT/'queue.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2),encoding='utf-8')
 print(f'Joined {len(queue)} pages / {len(rows)} controls; all marked pending flow verification.')

if __name__=='__main__':main()
