"""Derive a current catalog without treating callback routes as executed flows."""
from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
TYPES={
1:'引导|登录表单|注册表单|验证表单|重置表单|登录错误状态|验证码表单|重置成功状态',
2:'关系入口|邀请分享|邀请码表单|关系确认|绑定成功|共同资料表单|等待确认|邀请错误状态|已有关系状态',
3:'一级空状态|一级首页|搜索初始|搜索结果|日记表单|日记列表|私密日记详情|共同日记详情|相册空状态|相册列表|照片表单|照片详情',
4:'一级时刻列表|一级空状态|时刻详情|时刻表单|提醒列表|提醒空状态|纪念日列表|纪念日空状态|纪念日表单|倒计时详情|当日详情|胶囊列表|胶囊表单|已开启胶囊详情|封存胶囊详情|留言列表|留言空状态',
5:'一级工坊|素材选择|漫画表单|照片漫画表单|影片表单|生成进度|生成错误状态|作品详情|作品列表|主角表单',
6:'一级个人中心|个人资料表单|共同资料表单|草稿列表|标签管理|会员说明|设置入口|账号设置|隐私设置|通知设置|数据设置|帮助说明',
7:'一级领养等待|领养表单|一级宠物首页|一级首次空状态|互动成功|互动任务|精力不足状态|喂食任务|食物不足状态|任务奖励状态|任务列表|装扮选择|装扮不足状态|房间保存成功|房间编辑|房间不足状态|故事权限状态|成长列表|成长详情|成就奖励状态|成就列表|图鉴列表|图鉴详情|危险设置操作|宠物设置',
8:'书架列表|书架空状态|素材推荐|基础信息表单|主题封面选择|素材选择|素材确认队列|模板选择|日记编排表单|照片编排表单|时刻编排表单|作品成长编排表单|章节页序管理|建册成功|回忆目录|阅读|阅读工具|补页种类选择|补页表单|补页阅读|回忆册管理'
}
TABS={'首页':'m03-p02','重要时刻':'m04-p01','工坊':'m05-p01','宠物':'m07-p03','我的':'m06-p01'}
def clean(value):return str(value).replace('|','／').replace('\r',' ').replace('\n',' ').strip()
def main():
 manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));rows=json.loads((ROOT/'prototype/evidence/current/current-runtime-inventory.json').read_text(encoding='utf-8'));edges=[]
 report=json.loads((ROOT/'prototype/evidence/current/current-runtime-summary.json').read_text(encoding='utf-8'))
 assert len(rows)==228 and not report['errors'], 'Runtime observation is incomplete or contains errors'
 for path,digest in report['files'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest, 'Stale observation: '+path
 fingerprint=hashlib.sha256(json.dumps(report['files'],sort_keys=True).encode()).hexdigest()
 for row in rows:
  source=Path(row['effective'].split('?')[0]).stem
  for control in row.get('observed',{}).get('controls',[]):
   handler=(control.get('inline') or '')+' '+(control.get('href') or '')+' '+' '.join(e['handler'] for e in control['own_events'])
   targets=set(re.findall(r'm\d{2}-p\d{2}(?=\.html)',handler))
   if 'tab.key===active.key' in handler and control['label'] in TABS:targets.add(TABS[control['label']])
   for target in sorted(targets):edges.append(dict(source=source,target=target,requested=row['id'],scenario=row['scenario'],control=control['label'],selector=control['selector'],available=control['visible'] and not control['disabled'],kind='返回候选' if 'UI.back(' in handler or 'PrototypeUI.back(' in handler else '导航/条件动作候选'))
 (ROOT/'prototype/evidence/current/current-navigation-candidates.json').write_text(json.dumps(edges,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 lines=['# 当前114页类型与入口出口候选','','页面类型对应原稿职责；实际状态随控制器数据发生变化。入口/出口来自当前运行处理函数的literal引用和明确的Tab目标，包含返回fallback及条件弹层动作，**尚未全部执行，不是最终导航验收**。动态ID、闭包变量及数字拼接无法由literal完整解析；没有候选不能据此判为死路。弹层仍需另行逐项登记。','', '| 页面 | 名称 | 原稿页面类型 | 入口候选页 | 出口候选页 | 空／有数据实际页 |','| --- | --- | --- | --- | --- | --- |']
 lines[2:2]=['运行源码指纹：`'+fingerprint+'`；文件哈希见evidence/current/current-runtime-summary.json。日期固定为2026-10-05的本地fixture；此日期是可重复观察条件，不是设备今日日期。','']
 for entry in manifest:
  id=entry['id'];kind=TYPES[int(id[1:3])].split('|')[int(id[-2:])-1];pair=[next(r for r in rows if r['id']==id and r['scenario']==scenario) for scenario in ['empty','populated']]
  inbound=sorted({e['source'] for e in edges if e['target']==id});outbound=sorted({e['target'] for e in edges if e['source']==id})
  lines.append('| '+' | '.join(map(clean,[id,entry['title'],kind,', '.join(inbound) or '动态/条件入口待核对',', '.join(outbound) or '动态/本页动作待核对','／'.join(Path(r['effective'].split('?')[0]).stem for r in pair)]))+' |')
 (ROOT/'prototype/PAGE_CATALOG.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 nav=['# 当前控件与导航候选','','当前回调引用关联控件、场景和目标；同一控件多个目标可能属于取消、确认、失败或fallback，不能直接当成必然跳转。完整动态条件与实际点击证据继续补齐。已执行的五Tab切换见 PRIMARY_NAVIGATION_IMPLEMENTATION.md。','', '| 实际页 | 请求页／场景 | 控件 | 目标 | 类别 | 可用 |','| --- | --- | --- | --- | --- | --- |']
 nav[2:2]=['运行源码指纹：`'+fingerprint+'`；114页空／有数据共228次观察，候选不等于执行验收。','']
 for e in edges:nav.append('| '+' | '.join(map(clean,[e['source'],e['requested']+'／'+e['scenario'],e['control'],e['target'],e['kind'],'是' if e['available'] else '隐藏/禁用']))+' |')
 nav+=['','## 条件重定向观察','','| 请求页 | 场景 | 实际页 |','| --- | --- | --- |']
 for r in rows:
  effective=Path(r['effective'].split('?')[0]).stem
  if effective!=r['id']:nav.append('| '+r['id']+' | '+r['scenario']+' | '+effective+' |')
 (ROOT/'prototype/CURRENT_NAVIGATION.md').write_text('\n'.join(nav)+'\n',encoding='utf-8');print(f'Catalog: {len(manifest)} pages; {len(edges)} callback route candidates')
if __name__=='__main__':main()
