"""Index actual hidden DOM without treating absent observations as exhaustive coverage."""
import hashlib
import json
from verify_pet_controls import ROOT, source

def main():
    out=ROOT/'evidence/current';path=out/'hidden-overlay-observations.json'
    report=json.loads(path.read_text(encoding='utf-8'));catalog=json.loads((out/'page-contracts.json').read_text(encoding='utf-8'))
    assert report['files']==catalog['files']==source()
    assert report['completed']==report['candidates']==len(report['results'])
    assert all(row['passed']and not row['errors']for row in report['results'])
    pages=[];controls=[]
    for page in catalog['pages']:
        observations=[row for row in report['results']if row['page']==page['id']]
        indexes=[index for index,row in enumerate(report['results'])if row['page']==page['id']]
        for index in indexes:
            row=report['results'][index]
            for overlay_index,overlay in enumerate(row['overlays']):
                for control_index,control in enumerate(overlay['controls']):
                    controls.append(dict(page=page['id'],observation_index=index,overlay_index=overlay_index,control_index=control_index,
                        trigger=row['selector'],trigger_label=row['label'],overlay_title=overlay['title'],observed_control=control,
                        execution='observed in open overlay; individual action and dirty/nested conditions pending'))
        pages.append(dict(page=page['id'],type=page['type'],observations=indexes,
            candidate_triggers=len(observations),opened=sum(bool(row['overlays'])for row in observations),
            no_overlay_in_fixture=sum(not row['overlays']for row in observations),
            hidden_controls=sum(len(overlay['controls'])for row in observations for overlay in row['overlays']),
            remaining='other/indirect triggers, nested actions, dirty closure, submitting cancellation, sources and five-width layouts'))
    value=dict(files=report['files'],report_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),pages=pages,hidden_controls=controls,accepted_pages=0)
    (out/'hidden-overlay-index.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    def clean(text):return str(text).replace('|','／').replace('\n',' ')
    lines=['# 运行时隐藏弹层与控件目录','',
        '使用八模块既有种子，独立浏览器上下文直接触发133个候选。报告保存实际弹层DOM、控件、处理函数、尺寸及焦点。当前只证明观察到的弹层与无修改时Escape关闭、存储保持、可用触发按钮焦点恢复；未观察到弹层不证明其他条件无弹层。','',
        '下表覆盖全部114页，不提升页面终验。空白观察的页仍需间接触发、空/失败/缺失条件审计。按钮具体提交、第二层弹窗、修改后关闭、提交途中取消、所有来源与五宽度继续。机器索引的observation_index等字段指向原报告，不靠标题去重忽略不同入口。','',
        '| 页面 | 类型 | 候选观察 | 出现弹层 | 当前条件无弹层 | 弹层控件观察 | 剩余 |',
        '| --- | --- | ---: | ---: | ---: | ---: | --- |']
    for page in pages:
        lines.append('| '+' | '.join(clean(page[key])for key in ['page','type','candidate_triggers','opened','no_overlay_in_fixture','hidden_controls'])+' | 间接／多层／dirty／提交取消／来源／布局 |')
    lines+=['','## 实际触发与弹层','', '| 页与报告索引 | 触发 | 观察结果 | 标题／可见控件 |','| --- | --- | --- | --- |']
    for index,row in enumerate(report['results']):
        details='；'.join(overlay['title']+'：'+'、'.join(control['label']for control in overlay['controls']if control['visible'])for overlay in row['overlays'])
        lines.append('| '+' | '.join(clean(value)for value in [row['page']+' / '+str(index),row['label'],row['outcome'],details or '当前直接触发未观察到弹层'])+' |')
    (ROOT/'HIDDEN_OVERLAYS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    assert source()==report['files']
    print(json.dumps(dict(pages=len(pages),candidate_triggers=len(report['results']),overlay_triggers=sum(page['opened']for page in pages),hidden_controls=len(controls),accepted_pages=0)))

if __name__=='__main__':main()
