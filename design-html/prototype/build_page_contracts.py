"""Explicit design-page taxonomy and source-bound evidence/navigation index."""
import json,re,hashlib,shutil
from pathlib import Path
from html.parser import HTMLParser
from verify_pet_controls import ROOT,DEMO,source

# Original design roles, checked against markup, controller families and runtime fixtures.
TYPES={
 'm01':['引导入口','登录表单','注册表单','找回密码账号验证表单','新密码表单','登录表单／校验失败','验证码表单／等待验证','密码重置成功状态'],
 'm02':['关系建立入口','邀请分享工具','邀请码表单','关系确认决策','绑定成功状态','情侣资料表单','邀请等待状态','邀请码失效状态','已有关系冲突状态'],
 'm03':['首页／空记录','首页／有记录','搜索表单／初始','搜索表单与结果列表','日记编辑表单','日记列表','日记详情／私密','日记详情与回应表单／共同','相册／空列表','相册／照片网格','照片编辑表单','照片详情与回应表单'],
 'm04':['时刻册列表','时刻册／空列表','时刻详情','时刻编辑表单','共同提醒列表／未读','共同提醒／空列表','纪念日列表','纪念日／空列表','纪念日编辑表单','纪念日详情／倒计时','纪念日详情／当天','胶囊列表','胶囊编辑表单','胶囊详情／已开启','胶囊详情／封存','共同留言聚合列表','共同留言／空列表'],
 'm05':['工坊入口与最近作品','创作素材选择','回忆漫画编辑任务','照片漫画编辑任务','回忆影片编辑任务','生成进度任务状态','生成失败状态','作品详情','作品列表','主角资料编辑任务'],
 'm06':['个人中心入口','个人资料设置与编辑弹层','共同空间设置','多类型草稿列表','标签管理列表','会员权益说明与方案选择','设置入口','账号安全设置','共同可见设置','通知设置','数据存储管理','帮助与关于工具'],
 'm07':['领养等待确认状态','宠物品种与名字选择任务','宠物空间入口','宠物空间／未领养','宠物互动成功状态','宠物互动操作','宠物互动／精力不足','宠物喂食操作','宠物喂食／资源不足','任务奖励成功状态','宠物任务列表','装扮选择与保存任务','装扮／资源不足','房间布置保存成功状态','房间布置选择与保存任务','房间布置／资源不足','成长故事／来源权限失效','成长故事列表','成长章节详情','成就奖励成功状态','成就列表','宠物收藏图鉴列表','图鉴条目详情','宠物数据导出与解除照顾确认','宠物设置'],
 'm08':['回忆册书架列表','回忆册／空书架','本月共同素材推荐','回忆册基础信息编辑任务','主题封面选择任务','共同素材选择任务','素材预览与确认','回忆页模板选择','日记摘录书页编辑任务','照片故事书页编辑任务','重要时刻书页编辑任务','作品宠物书页编辑任务','章节与页序编辑任务','建册完成状态','回忆册目录','沉浸阅读','阅读工具菜单页','双人补页模板选择','双人补页编辑任务','阅读／含补页','回忆册管理与删除确认'],
}
REPORTS=['onboarding-control-results.json','record-controls-results.json','moment-controls-results.json','time-controls-results.json','workshop-controls-results.json','settings-controls-results.json','pet-controls-results.json','book-controls-results.json']
class Markup(HTMLParser):
 def __init__(self):super().__init__();self.scripts=[];self.styles=[];self.forms=[];self.inputs=[];self.icons=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='script'and a.get('src'):self.scripts.append(a['src'])
  if tag=='link'and a.get('rel')=='stylesheet'and a.get('href'):self.styles.append(a['href'])
  if tag=='form':self.forms.append(a.get('id')or a.get('class')or 'form')
  if tag in ['input','textarea','select']:self.inputs.append(dict(tag=tag,name=a.get('name'),id=a.get('id'),type=a.get('type')))
  if tag=='svg':self.icons+=1
def target(url):
 m=re.search(r'm\d{2}-p\d{2}',str(url));return m[0]if m else None
def clean(value):return str(value).replace('|','／').replace('\n',' ').replace('\r',' ')
def dump(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
 files=source();manifest=json.loads((DEMO/'manifest.json').read_text(encoding='utf-8'));ids=[p['id']for p in manifest];assert len(ids)==114 and len(set(ids))==114
 taxonomy={f'{module}-p{n:02}':kind for module,rows in TYPES.items()for n,kind in enumerate(rows,1)};assert set(taxonomy)==set(ids)
 out=ROOT/'evidence/current';runtime=json.loads((out/'current-runtime-summary.json').read_text(encoding='utf-8'));assert runtime['files']==files and not runtime['errors']
 observations=json.loads((out/'current-runtime-inventory.json').read_text(encoding='utf-8'));assert len(observations)==228
 history=ROOT/'evidence/history/pre-page-contracts-594e6eb';history.mkdir(parents=True,exist_ok=True)
 for name in ['PAGE_CATALOG.md','CURRENT_NAVIGATION.md','STATE_MATRIX.md']:
  if not(history/name).exists():shutil.copy2(ROOT/name,history/name)
 controls=[];reports={};edges=[];fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
 for name in REPORTS:
  p=out/name;assert p.exists(),name;v=json.loads(p.read_text(encoding='utf-8'));rows=v.get('results',[])if isinstance(v,dict)else v;current=(isinstance(v,dict)and v.get('files')==files)or(isinstance(v,list)and bool(rows)and all(r.get('source_fingerprint')==fingerprint for r in rows))
  reports[name]=dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source_current=current,cases=len(rows),passed=sum(bool(r.get('passed'))for r in rows))
  for index,r in enumerate(rows):
   page=r.get('page')or r.get('id')or target(r.get('case'))
   if page not in ids or not r.get('selector'):continue
   status='当前源码通过'if current and r.get('passed')and not r.get('errors')else'历史通过／待当前复验'if r.get('passed')and not r.get('errors')else'失败／待解决'
   row=dict(page=page,selector=r['selector'],label=r.get('label',''),contract=r.get('contract',''),report='evidence/current/'+name,result_index=index,status=status,effective=r.get('effective')or r.get('details',{}).get('effective'));controls.append(row)
   dest=target(row['effective'])
   if dest in ids and dest!=page and row['contract']and not row['contract'].startswith(('input','radio')):
    edges.append(dict(source=page,target=dest,kind='executed-current'if status=='当前源码通过'else'executed-historical',label=row['label'],evidence=row['report'],result_index=index,contract=row['contract']))
 for r in observations:
  effective=target(r['effective']);assert effective in ids
  if effective!=r['id']:edges.append(dict(source=r['id'],target=effective,kind='observed-redirect',label=r['scenario'],evidence='evidence/current/current-runtime-inventory.json'))
  for c in r['observed']['controls']:
   handlers=' '.join([c.get('inline')or'',c.get('href')or'',*[e['handler']for e in c.get('own_events',[])]])
   for dest in sorted(set(re.findall(r'm\d{2}-p\d{2}',handlers))):
    assert dest in ids,dest;edges.append(dict(source=effective,target=dest,kind='code-candidate',label=c['label'],selector=c['selector'],scenario=r['scenario'],enabled=c['visible']and not c['disabled']))
 pages=[]
 for r in manifest:
  id=r['id'];p=DEMO/'custom'/f'{id}.html';s=p.read_text(encoding='utf-8');m=Markup();m.feed(s);pair=[o for o in observations if o['id']==id];assert {o['scenario']for o in pair}=={'empty','populated'}
  dependencies=[(p.parent/v).resolve()for v in m.scripts if 'prototype-'in v];assert all(v.exists()for v in dependencies)
  executed=[c for c in controls if c['page']==id];assert executed,id
  styles=[(p.parent/v).resolve()for v in m.styles];assert all(v.exists()for v in styles)
  required=['来源返回／直接入口fallback','pressed／focus／disabled／reduced-motion']
  if m.inputs or any(c['native_input']for o in pair for c in o['observed']['controls']):required+=['输入或选择的focus／filled／error／disabled','可输入字段的typing／长度限制及及时校验']
  if any(k in taxonomy[id]for k in ['编辑','表单','选择','布置']):required+=['未保存返回／取消选择保护','有写入时提交loading／success／failure及保留输入']
  if any(k in taxonomy[id]for k in ['列表','网格','书架','推荐','空记录']):required+=['Empty图形／说明／真实CTA','有异步读取时Loading／Error／重试','刷新／分页／长按／滑动适用决定']
  if any(k in taxonomy[id]for k in ['详情','阅读','状态','成功','失败','确认']):required+=['状态／内容ID／来源失效检查','下一步或恢复出口及不重复写入']
  if any(c['contract'].startswith(('sheet:','modal:','picker:'))for c in executed):required+=['动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复']
  pages.append(dict(id=id,title=r['title'],type=taxonomy[id],required_states=required,html='custom/'+p.name,html_sha256=files['custom/'+p.name],static_forms=m.forms,static_fields=m.inputs,inline_svg_count=m.icons,controllers=[v.relative_to(DEMO).as_posix()for v in dependencies],stylesheets=[v.relative_to(DEMO).as_posix()for v in styles],runtime=[dict(scenario=o['scenario'],effective=o['effective'],inventory_index=observations.index(o),controls=len(o['observed']['controls']),visible_enabled=sum(c['visible']and not c['disabled']for c in o['observed']['controls']),forms=o['observed']['forms'],observed_controls=o['observed']['controls'])for o in pair],incoming=[e for e in edges if e['target']==id],outgoing=[e for e in edges if e['source']==id],control_evidence=executed,acceptance='not-finally-accepted'))
 assert all(p['type']and '逐页确认'not in p['type']for p in pages);assert source()==files
 assets=[dict(path=p.relative_to(DEMO).as_posix(),bytes=p.stat().st_size,extension=p.suffix.lower(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in sorted((DEMO/'assets').rglob('*'))if p.is_file()]
 result=dict(scope='114 original design-page roles and current runtime/control evidence; candidate navigation is not acceptance',files=files,assets=assets,reports=reports,pages=pages,edges=edges)
 dump(out/'page-contracts.json',result)
 lines=['# 114页明确类型与入口出口证据','','本表使用人工指定的设计页职责，核对当前HTML字段、控制器和实际空／有数据观察。设计状态名不保证直接入口停留在该状态：控制器可按条件重定向。动态表单由控制器创建，不能用HTML中的form数量判断页面类型。','', '完整逐控件selector／行为契约、入口出口及运行落点见[机器可读目录](evidence/current/page-contracts.json)；关系图见[完整导航候选图](PAGE_RELATIONSHIPS.mmd)。当前执行、历史执行、候选和重定向分别记录；114页均未最终验收。','', '| 页面 | 原稿名称 | 明确类型 | 空／有数据实际页 | 当前／历史初始控件证据 | 入口／出口记录 |','| --- | --- | --- | --- | --- | --- |']
 for p in pages:
  counts=[sum(c['status']==state for c in p['control_evidence'])for state in ['当前源码通过','历史通过／待当前复验']]
  effective='／'.join(target(r['effective'])for r in p['runtime']);lines.append('| '+' | '.join(map(clean,[p['id'],p['title'],p['type'],effective,f'{counts[0]}／{counts[1]}',f"{len(p['incoming'])}／{len(p['outgoing'])}"]))+' |')
 (ROOT/'PAGE_CATALOG.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 nav=['# 当前114页导航与来源','','当前源码绑定于page-contracts.json的151文件字节指纹。实线为当前源码实际控件执行；历史点击使用粗线，仅证明当时路径；虚线为当前代码候选或观察到的条件重定向。每条边保留类型和报告位置，数字go、动态ID、弹层取消／确认及来源历史仍需条件验证。','', '| 来源 | 目标 | 类型 | 控件／条件 | 证据 |','| --- | --- | --- | --- | --- |']
 graph=['flowchart LR']
 for p in pages:graph.append(f'  {p["id"].replace("-","_")}["{p["id"]} {p["type"]}"]')
 seen=set()
 for e in edges:
  key=(e['source'],e['target'],e['kind'],e['label'])
  if key in seen:continue
  seen.add(key);nav.append('| '+' | '.join(map(clean,[e['source'],e['target'],e['kind'],e['label'],e.get('evidence','当前运行回调；未执行')]))+' |');symbol='-->'if e['kind']=='executed-current'else'==>'if e['kind']=='executed-historical'else'-.->'
  label=(e['kind']+' · '+clean(e['label'])).replace('"','＂').replace('<','＜').replace('>','＞')[:90]
  graph.append(f'  {e["source"].replace("-","_")} {symbol}|"{label}"| {e["target"].replace("-","_")}')
 (ROOT/'CURRENT_NAVIGATION.md').write_text('\n'.join(nav)+'\n',encoding='utf-8');(ROOT/'PAGE_RELATIONSHIPS.mmd').write_text('\n'.join(graph)+'\n',encoding='utf-8')
 # Replace ambiguous types while retaining the preimplementation requirements and explicit pending state.
 p=ROOT/'STATE_MATRIX.md';text=p.read_text(encoding='utf-8');updated=[];matrix_lines=[]
 text=text.replace('下表是实施前的适用状态设计。既有状态稿已计入页面清单；“需要”不代表已经实现或通过测试。','下表按明确页面职责、实际字段和控件契约更新适用需求；条件性要求仍需逐页决定。执行列记录初始控件证据，不能替代动态状态和最终验收。')
 for line in text.splitlines():
  parts=line.split('|')
  if len(parts)>5 and parts[1].strip()in taxonomy:
   page=next(p for p in pages if p['id']==parts[1].strip());parts[3]=' '+page['type']+' ';parts[4]=' '+'；'.join(page['required_states'])+' ';parts[5]=' 初始控件当前'+str(sum(c['status']=='当前源码通过'for c in page['control_evidence']))+'／历史'+str(sum(c['status']=='历史通过／待当前复验'for c in page['control_evidence']))+'；观察2次；状态终验未完成 ';line='|'.join(parts);updated.append(parts[1].strip())
  matrix_lines.append(line)
 assert set(updated)==set(ids);p.write_text('\n'.join(matrix_lines)+'\n',encoding='utf-8')
 queue=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'));assert len(queue)==114 and not any(p.get('flow_verified')for p in queue)
 for q in queue:
  page=next(p for p in pages if p['id']==q['id']);q['page_type']=page['type'];q['needed_states']=page['required_states'];q['page_contract']='evidence/current/page-contracts.json';q['current_initial_control_checks']=sum(c['status']=='当前源码通过'for c in page['control_evidence'])
 dump(ROOT/'queue.json',queue)
 dump(out/'page-contract-audit-checkpoint.json',dict(files=files,pages=114,assets=len(assets),observations=228,observed_controls=sum(r['controls']for p in pages for r in p['runtime']),initial_control_evidence=len(controls),current_controls=sum(c['status']=='当前源码通过'for c in controls),historical_controls=sum(c['status']=='历史通过／待当前复验'for c in controls),navigation_records=len(edges),distinct_navigation_records=len(seen),accepted_pages=0))
 print(json.dumps({k:v for k,v in json.loads((out/'page-contract-audit-checkpoint.json').read_text(encoding='utf-8')).items()if k!='files'},ensure_ascii=False))
if __name__=='__main__':main()
