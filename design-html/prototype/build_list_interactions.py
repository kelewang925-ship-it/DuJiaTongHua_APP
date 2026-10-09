"""Explicit list/selection interaction decisions, bound to current page contracts."""
import hashlib
import json
from verify_pet_controls import ROOT, DEMO, source

# Reviewed page roles. These decisions are not inferred from Chinese title keywords.
SURFACES = {}
def group(ids, role, click, refresh, reason):
    for page in ids.split():
        assert page not in SURFACES
        SURFACES[page] = dict(role=role, click=click, refresh=refresh, reason=reason)

group('m03-p01 m03-p02', '首页摘要', '卡片进入对应记录；全部入口进入集合', '跨标签相关storage事件重新读取；进入页重读', '最近记录最多3条；摘要不分页，全部内容在对应集合')
group('m03-p03', '搜索历史与快捷词', '词条提交搜索；保留可编辑关键词', '提交生成结果；当前关键词不因storage变化丢失', '搜索历史最多6条，快捷词是固定选项')
group('m03-p04', '搜索结果', '稳定记录ID进入实际详情', '重新提交关键词；storage重新查询；失败有重试', '本地匹配集全部渲染，无远端下一页')
group('m03-p06', '日记集合', '进入日记详情；Tab筛选正文和草稿', '显式刷新日记；加载禁用，失败重试', '按本地集合和Tab筛选全量显示；编辑删除在详情完成')
group('m03-p09 m03-p10', '相册集合／空态', '照片进入详情；空态添加照片', '有数据页刷新相册；空页重新进入按真实集合判定', '照片网格显示当前筛选集，不用滑动删除照片')
group('m04-p01 m04-p02', '时刻集合／空态', '稳定ID进入详情；空态添加时刻', '有数据页刷新时刻册；空页重入判定', '当前可访问本地集合；全部入口不是远端分页')
group('m04-p05 m04-p06', '共同提醒／空态', '提醒进入对应纪念日／胶囊／作品／回应／宠物来源；空态返回时刻册', '页面重入重读；没有显式刷新和本模块storage重绘', '提醒是有限本地派生集合，点击写入已读后进入来源；来源失效条件继续核查')
group('m04-p07 m04-p08', '纪念日集合／空态', '进入倒计时或当天详情；空态新建', '有数据页刷新纪念日；空页重入判定', '完整本地纪念日集合，无网络分页')
group('m04-p12', '胶囊集合', 'Tab筛选封存／开启／草稿，条目进入实际状态', '显式刷新胶囊；失败重试', '状态过滤全量集合，封存内容不提供快捷滑动开启或删除')
group('m04-p16 m04-p17', '共同留言聚合／空态', '查看当前原记录并更新当前留言已读；空态返回', '相关storage重载；失效提示后重入重读', '从可共同访问记录派生留言；没有独立删除留言的批量手势')
group('m05-p01', '最近作品摘要', '作品进入草稿／生成／失败／结果；全部进入作品页', '进入时W.refresh推进当前状态', '最近最多2条；完整列表由我的创作承接')
group('m05-p02', '创作来源选择', '选择素材种类或自由创作；动态选择器确认后回填', '打开选择器读取来源；不重置当前选择', '有限种类菜单和本地素材；选择确认与取消优先')
group('m05-p09', '作品集合', 'Tab／收藏夹筛选；稳定ID进入真实状态', '显式刷新我的创作，读取并推进生成状态', '本地筛选集全部显示；作品操作位于详情更多菜单')
group('m06-p04', '多类型草稿集合', '对应类型进入继续编辑', '显式刷新草稿箱；失败重试', '四类本地草稿全量列出，不按四类分页')
group('m06-p05', '标签管理集合', '标签打开编辑／删除菜单；新增打开输入Sheet', '本页保存／删除后paint；重入读取，跨标签即时更新未证明', '标签是小型本地配置；菜单提供明确危险确认，保持记录本体')
group('m06-p06', '会员方案说明', '说明／本地开通确认；已有演示会员禁用开通', '重新进入读取演示会员；不请求真实订阅', '静态权益与本地演示方案，不是可分页商品列表')
group('m07-p02', '品种选择', '选品种并输入名字；邀请前校验', '相关storage提示变化；保留当前输入', '固定4种品种，不需要网络刷新与分页')
group('m07-p06 m07-p08', '互动／食物选择', '单选后明确提交互动或喂食；不足进入恢复页', '相关storage更新资源显示，操作核对当前库存', '固定4种互动或3种食物，选择本身不消费资源')
group('m07-p11', '任务集合', '每日／每周Tab；任务执行或领取一次奖励', '操作后读取当前宠物；相关storage刷新', '有限任务配置与本地进度，无下一页')
group('m07-p12 m07-p15', '装扮／房间选择任务', '分类与条目选择；显式保存；不足进入说明页', '跨标签变化提示并保留候选；保存核对当前库存', '固定目录；刷新不能静默覆盖未保存搭配或布置')
group('m07-p18', '成长故事集合', '故事稳定ID进入章节；写故事打开编辑Sheet', '无弹层时相关storage重载；有弹层时保留输入', '全量可访问成长日志；不在列表直接删除共同记录')
group('m07-p21', '成就集合', '成就查看要求或领取；未达标显示进度', '进入页和操作后读当前宠物；相关storage更新', '有限成就配置；奖励具有一次领取约束')
group('m07-p22', '收藏图鉴集合', '分类Tab；条目选择／详情／解锁说明', '进入页读取当前目录和库存；相关storage更新', '有限物品目录；无远端目录分页')
group('m08-p01 m08-p02', '回忆册书架／空态', '稳定册ID进入目录；新建；草稿归档Sheet选择', '非编辑且无弹层时相关storage重载；重入读取', '当前出版册全部列出；草稿归档是有限本地Sheet集合')
group('m08-p03', '本月素材推荐', '素材进入原记录；确认进入建册；空态写共同日记', '相关storage重载；按当前月份重读来源', '按月本地派生集合，不调用远端推荐服务')
group('m08-p05', '主题封面选择', '主题选择／照片回填；确认下一步', '保留编辑会话；变化提示，保存核对', '固定主题，换照片属于明确选择器')
group('m08-p06', '共同素材选择', '分类筛选／多选素材；开始编排', '相关storage仅提示，保留候选；确认核对来源', '本地可共同访问素材全集；不能以刷新丢弃未确认选择')
group('m08-p08', '书页模板选择', '单选模板后使用；返回原素材预览', '进入读取固定模板；相关storage按非编辑页逻辑重读', '固定6类模板，与任务候选相匹配')
group('m08-p13', '章节与页序管理', '章节／页面打开操作菜单；保存排列', '保留当前编辑；保存核对当前册与来源', '当前册页全量显示；页序用明确操作，不增加拖拽架构')
group('m08-p15', '回忆册目录', '目录页条目进入对应阅读页；管理进入册管理', '无弹层时相关storage重载；重入重读', '当前册全目录；阅读上一页／下一页属于内容导航，不是列表分页')
group('m08-p18', '补页类型选择', '文字／表情／照片进入补页编辑', '进入读取固定模板；相关storage按非编辑页逻辑重读', '固定3种补页方式')
group('m03-p08 m03-p12 m04-p03 m07-p19', '详情中的回应', '输入／表情／发送；现有留言文本不是删除入口', '详情按模块storage逻辑重读或保留输入；发送核对当前来源', '回应附属于原记录；独立分页、滑删、长按删除不是当前产品契约')

def main():
    files = source()
    catalog_path = ROOT / 'evidence/current/page-contracts.json'
    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
    assert catalog['files'] == files
    assert set(SURFACES) <= {page['id'] for page in catalog['pages']}
    rows = []
    for page in catalog['pages']:
        decision = SURFACES.get(page['id'], dict(role='无独立集合列表', click='沿页面控件契约执行导航、表单、详情或状态恢复', refresh='重新进入读取当前上下文；编辑任务保留输入', reason='本页不是集合列表；动态Sheet内部集合另见触发条件审计'))
        controls = page['control_evidence']
        assert all(control['status'] == '当前源码通过' for control in controls)
        controller_evidence = []
        for path in page['controllers']:
            text = (DEMO / path).read_text(encoding='utf-8')
            controller_evidence.append(dict(path=path, sha256=hashlib.sha256((DEMO/path).read_bytes()).hexdigest(),
                storage_listener_lines=[n for n,line in enumerate(text.splitlines(),1) if "addEventListener('storage'" in line],
                refresh_label_lines=[n for n,line in enumerate(text.splitlines(),1) if '刷新' in line]))
        rows.append(dict(page=page['id'], title=page['title'], type=page['type'], **decision,
            long_press='不新增：使用可发现的点击／更多菜单，不隐藏关键动作' if page['id'] in SURFACES else '不适用独立列表',
            swipe='不新增：明确选择／详情操作；避免和滚动、浏览器返回竞争' if page['id'] in SURFACES else '不适用独立列表',
            pull_refresh='不新增：显式刷新或重入／数据事件更新，编辑候选不丢失' if page['id'] in SURFACES else '不适用独立列表',
            pagination='不新增远端分页；当前本地全集或固定选项／摘要→完整集合' if page['id'] in SURFACES else '不适用独立列表',
            controllers=page['controllers'], controller_source_evidence=controller_evidence, initial_control_evidence=controls,
            conditional_execution='待隐藏条件、刷新失败／取消和来源变化逐项终验'))
    assert len(rows) == 114 and source() == files
    value = dict(files=files, catalog_sha256=hashlib.sha256(catalog_path.read_bytes()).hexdigest(), pages=rows, declared_surfaces=len(SURFACES), accepted_pages=0)
    (ROOT / 'evidence/current/list-interaction-decisions.json').write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    def clean(value): return str(value).replace('|','／').replace('\n',' ')
    lines = ['# 114页列表与集合交互适用表', '',
        '按明确页面职责和当前控制器制定；不是用关键字搜索自动判定完成。全部页都列明适用或不适用理由。来源哈希与初始控件报告索引见list-interaction-decisions.json。114页最终验收仍0。', '',
        '## 通用决定', '',
        '- 当前本地模拟集合全量读取。摘要通过“全部”进入完整集合；固定选项与任务配置不增加网络分页。阅读翻页是内容导航。',
        '- 列表点击、显式更多菜单、危险确认优先。长按／横滑不新增独占动作；现有滚动和Sheet下滑关闭继续保留。',
        '- 有刷新按钮的列表沿用按钮与失败重试；本地事件更新或重入读取不等同于拉取真实服务。选择与编辑任务保护候选，不以自动刷新重置输入。',
        '- 下表是当前适用决定与源码行为说明；初始752条成功不证明所有刷新失败、弹层、跨标签条件。所有条件执行仍按状态审计补齐。', '',
        '| 页面 | 类型／集合 | 点击与更多 | 刷新方式 | 不增加长按／横滑／下拉／远端分页的依据 | 条件验收 |',
        '| --- | --- | --- | --- | --- | --- |']
    for row in rows:
        lines.append('| '+' | '.join(clean(row[key]) for key in ['page','role','click','refresh','reason','conditional_execution'])+' |')
    (ROOT / 'LIST_INTERACTIONS.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(json.dumps(dict(pages=len(rows), declared_surfaces=len(SURFACES), current_initial_controls=sum(len(row['initial_control_evidence']) for row in rows), accepted_pages=0)))

if __name__ == '__main__': main()
