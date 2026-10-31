"""Publish source-bound component/token observations without discarding history."""
import json
from pathlib import Path
from collections import Counter
from replay_current_initial_controls import ROOT,DEMO,deps,sha,dump

def main():
    folder=ROOT/'evidence/current/components-20261031';path=folder/'results.json';data=json.loads(path.read_text(encoding='utf-8'))
    assert data['complete'] and data['all_passed']
    files={**deps(),'prototype/components.html':sha(ROOT/'components.html')};assert data['dependencies']==files
    rows=data['component_contracts'];pages=data['page_observations'];kinds=list(pages[0]['observation']['components'])
    ids={v['id'] for v in json.loads((DEMO/'manifest.json').read_text(encoding='utf-8'))}
    assert len(rows)==56 and len(pages)==114 and {r['page'] for r in pages}==ids
    assert {(r['component'],r['width'],r['motion']) for r in rows}=={(k,w,m) for k in kinds for w in [320,430] for m in ['no-preference','reduce']}
    assert all(r['passed'] and not r['errors'] for r in rows+pages)
    for sub,mapping in [('source',files),('fixtures',data['fixture_sha256'])]:
        for n,h in mapping.items():
            assert sha(folder/sub/n)==h,n
            if sub=='fixtures':assert sha(ROOT/n)==h,n
    tokens={name:{'values':sorted({p['observation']['tokens'][name] for p in pages}),'resolved':sum(bool(p['observation']['tokens'][name]) for p in pages)} for name in data['tokens']}
    required=['--prototype-paper','--prototype-ink','--prototype-accent','--prototype-font-family','--prototype-font-body','--prototype-font-note','--prototype-font-title','--prototype-space-xs','--prototype-space-sm','--prototype-space-md','--prototype-space-lg','--prototype-space-xl','--prototype-space-xxl','--prototype-radius-sm','--prototype-radius-md','--prototype-radius','--prototype-shadow','--prototype-touch','--prototype-control-height']
    for name in required:assert tokens[name]['resolved']==114 and len(tokens[name]['values'])==1,name
    history=ROOT/'evidence/history/pre-current-components-af7c4b1';history.mkdir(parents=True,exist_ok=True)
    preserved={}
    for name in ['COMPONENT_COVERAGE.md','TOKEN_COVERAGE.md']:
        target=history/name;assert not target.exists();target.write_bytes((ROOT/name).read_bytes());preserved[name]=sha(target)
    dump(history/'manifest.json',{'files':preserved,'relative_links_resolve_against':'design-html/prototype','scope':'Original228 empty/populated historical observations and previous notes preserved byte-for-byte; new114 canonical observations do not replace that scenario count.'})
    totals={k:{'pages_present':sum(p['observation']['components'][k]>0 for p in pages),'instances':sum(p['observation']['components'][k] for p in pages)} for k in kinds}
    lines=['# 当前组件契约与114页初态观察','','14类组件在320／430px、普通／减少动效下共56项契约全部新执行通过。另114页各使用现有canonical种子重新观察一次，记录实际可操作区域中的组件类；p20原生弹窗打开时背景排除。','','工厂契约检查实际点击、键盘、禁用／Loading、错误恢复、回调、弹层返回与焦点、头像图片失败、标签动作和静态节点语义。它不等于所有业务条件通过；类数量也不等于组件接入验收。原画板元素保留决定见[ORIGINAL_COMPONENT_DECISIONS](ORIGINAL_COMPONENT_DECISIONS.md)。','','| 类型 | 出现页数 | 实例数 | 工厂契约 |','| --- | ---: | ---: | --- |']
    for name,value in totals.items():lines.append(f'| {name} | {value["pages_present"]} | {value["instances"]} | 四配置通过 |')
    lines+=['','## 逐页实际数量','','0表示本次初态可操作区域未出现对应共享类，不表示工厂未实现；Header等原画板元素按保留决定处理。Loading／弹窗等瞬态或条件组件另有专项证据，不用稳定初态零数量判定缺失。','','| 页 | '+' | '.join(kinds)+' |','| --- | '+' | '.join('---:' for _ in kinds)+' |']
    for page in pages:lines.append('| '+page['page']+' | '+' | '.join(str(page['observation']['components'][k]) for k in kinds)+' |')
    lines+=['','## 来源与边界','','[当前执行](evidence/current/components-20261031/results.json)保留202项依赖（含组件评审HTML）、测试存档、每个契约和观察行。原228次空／有数据观察的[旧表](evidence/history/pre-current-components-af7c4b1/COMPONENT_COVERAGE.md)保留原版本；本次114次canonical观察不伪称重新执行228个情形。','','完整动态接入、局部Token、视觉差异和原41项终审继续；人工验收0。']
    (ROOT/'COMPONENT_COVERAGE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    lines=['# 当前共享Token根节点观察','','2026-10-31，114个canonical页面、390px宽、减少动效下实际读取43项共享变量。核心颜色、字体、间距、圆角、阴影和控件尺寸在114页均非空且值一致。根变量一致不证明局部CSS已完全采用变量，也不等于像素或人工验收。','','| Token | 实际不同值 | 非空页数 |','| --- | --- | ---: |']
    for name,value in tokens.items():lines.append('| '+name+' | '+'；'.join(v.replace('|','／') or '（根节点空值）' for v in value['values'])+' | '+str(value['resolved'])+'/114 |')
    lines+=['','## 来源与剩余','','[实际报告](evidence/current/components-20261031/results.json)逐页存有原始值与源码／样式指纹。旧228次观察及504处等值迁移说明已[归档](evidence/history/pre-current-components-af7c4b1/TOKEN_COVERAGE.md)，其历史指纹不改写为新源码。','','原画板的绘画、位置和有依据的局部皮肤继续按保留决定核对；不能仅因局部存在颜色字面量就替换成统一值。局部选择器、状态与主题的Token使用及完整41项终审继续，人工验收0。']
    (ROOT/'TOKEN_COVERAGE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    value={'passed':True,'report_sha256':sha(path),'producer_sha256':sha(ROOT/'publish_current_components.py'),'component_contracts':56,'canonical_pages':114,'tokens':tokens,'component_totals':totals,'core_token_names':required,'history':preserved,'artifacts':{n:sha(ROOT/n) for n in ['COMPONENT_COVERAGE.md','TOKEN_COVERAGE.md']},'human_accepted_pages':0}
    dump(folder/'summary.json',value);print('Published56 component contracts,114 canonical observations and43 root token values; history preserved.')

if __name__=='__main__':main()
