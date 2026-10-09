"""Join closure and nested cancellation evidence without upgrading action coverage."""
import hashlib
import json
from verify_pet_controls import ROOT,source
from verify_nested_confirmations import CASES

def main():
    out=ROOT/'evidence/current';files=source()
    def read(name):
        path=out/name;value=json.loads(path.read_text(encoding='utf-8'));assert value['files']==files
        return value,hashlib.sha256(path.read_bytes()).hexdigest()
    observed,observed_sha=read('hidden-overlay-observations.json')
    exits,exits_sha=read('overlay-exit-path-results.json')
    nested,nested_sha=read('nested-confirmation-results.json')
    assert exits['observations_sha256']==nested['observations_sha256']==observed_sha
    expected=set()
    for index,row in enumerate(observed['results']):
        if not row['overlays']:continue
        overlay=row['overlays'][0];methods=['button','back','backdrop']+(['drag']if'prototype-sheet'in overlay['html'].split('>')[0]else[])
        for method in methods:expected.add((index,method,False))
        if any(c['type']=='submit'and c['visible']for c in overlay['controls']):
            for method in methods:expected.add((index,method,True))
    actual={(row['observation_index'],row['method'],row['dirty'])for row in exits['results']}
    assert actual==expected and len(actual)==len(exits['results'])==exits['cases']==exits['completed']==432
    assert {(row['observation_index'],row['method'])for row in nested['results']}=={(index,method)for index in CASES for method in ['button','back','backdrop']}
    assert len(nested['results'])==nested['expected_cases']==66
    for row in exits['results']+nested['results']:
        assert row['passed']and not row['errors']and row['storage_preserved']and row['underlying_page_preserved']
    assert all(row['focus_returned']for row in exits['results'])and all(row['safe_cancel_focus']for row in nested['results'])
    catalog=json.loads((out/'page-contracts.json').read_text(encoding='utf-8'));assert catalog['files']==files
    def clean(value):return str(value).replace('|','／').replace('\n',' ')
    lines=['# 已观察弹层：关闭与二层确认执行','',
        '432项关闭路径和66项第二层取消，共498项。适用范围由原报告的99个弹层入口、71个Sheet和16个保存表单明确决定。证明当前种子与390×844、减少动效环境；未执行全部选择／保存／删除结果、多层其他路径、提交取消与五宽度，不提升114页终验。','',
        '| 页面 | 本批关闭项 | 本批修改保护项 | 第二层取消项 | 最终验收 |','| --- | ---: | ---: | ---: | --- |']
    for page in catalog['pages']:
        rows=[row for row in exits['results']if row['page']==page['id']];deep=[row for row in nested['results']if row['page']==page['id']]
        lines.append(f"| {page['id']} | {len(rows)} | {sum(row['dirty']for row in rows)} | {len(deep)} | 未完成 |")
    lines+=['','## 入口与关闭方法','', '| 观察索引／页面 | 标题 | 无修改方法 | 修改后继续／放弃方法 |','| --- | --- | --- | --- |']
    for index,row in enumerate(observed['results']):
        if not row['overlays']:continue
        checks=[value for value in exits['results']if value['observation_index']==index]
        lines.append('| '+' | '.join(clean(value)for value in [str(index)+' / '+row['page'],row['overlays'][0]['title'],'、'.join(value['method']for value in checks if not value['dirty']),'、'.join(value['method']for value in checks if value['dirty'])or'无保存表单；候选取消不回填'])+' |')
    lines+=['','## 第二层危险／身份确认','', '| 观察索引／页面 | 选择动作 | 实际二层标题 | 取消方法 |','| --- | --- | --- | --- |']
    for index,(action,title)in CASES.items():
        row=observed['results'][index]
        lines.append('| '+' | '.join(clean(value)for value in [str(index)+' / '+row['page'],action,title,'按钮取消／浏览器返回／遮罩'])+' |')
    (ROOT/'OVERLAY_EXIT_PATHS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    hidden=json.loads((out/'hidden-overlay-index.json').read_text(encoding='utf-8'));assert hidden['files']==files
    behavior_lines=['# 250条隐藏控件的行为与剩余执行','',
        '每条保留观察、弹层和控件索引。下列证据栏只列本批可证明的部分；原生输入、已有处理函数及所属弹层关闭通过都不等于这个控件的全部效果通过。具体选择／保存／删除结果继续逐项执行。','',
        '| 页面／观察／控件索引 | 弹层 | 控件 | 已证明与待执行行为 |',
        '| --- | --- | --- | --- |']
    for control in hidden['hidden_controls']:
        index=control['observation_index'];c=control['observed_control'];pending='已观察处理候选；具体点击效果、不同条件与失败恢复待执行'
        if index in CASES and c['label']==CASES[index][0]:
            pending='已执行进入「'+CASES[index][1]+'」，三种取消不写入、保持页面且默认安全焦点；最终提交结果待执行'
        elif c['disabled']:pending='本观察条件禁用；允许条件、禁用理由及恢复后动作待逐项核对'
        elif c['native_input']:pending='原生输入／选择已观察；字段校验、候选回填与实际保存结果待逐项执行'
        elif c['type']=='submit':pending='保存表单四种修改后关闭的继续／放弃通过；校验、提交Loading、失败与成功结果待逐项执行'
        behavior_lines.append('| '+' | '.join(clean(value)for value in [control['page']+' / '+str(index)+' / '+str(control['control_index']),control['overlay_title'],c['label'],pending])+' |')
    assert len(hidden['hidden_controls'])==250
    (ROOT/'HIDDEN_CONTROL_BEHAVIORS.md').write_text('\n'.join(behavior_lines)+'\n',encoding='utf-8')
    value=dict(files=files,reports={'hidden-overlay-observations.json':observed_sha,'overlay-exit-path-results.json':exits_sha,'nested-confirmation-results.json':nested_sha},
        closure_cases=432,dirty_cases=sum(row['dirty']for row in exits['results']),nested_cases=66,total=498,accepted_pages=0)
    (out/'overlay-exit-summary.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert source()==files;print(json.dumps({key:value for key,value in value.items()if key not in ['files','reports']}))

if __name__=='__main__':main()
