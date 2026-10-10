"""Bind actual14-component observations and local declaration candidates."""
import hashlib,json
from verify_pet_controls import ROOT,DEMO,source
from audit_component_coverage import SELECTORS

def main():
    out=ROOT/'evidence/current';raw=(out/'component-coverage-observations.json').read_bytes();report=json.loads(raw);files=source()
    assert report['files']==files and len(report['static_pages'])==114 and len(report['observations'])==228
    assert {(r['page'],r['scenario'])for r in report['observations']}=={(p['page'],s)for p in report['static_pages']for s in['empty','populated']}
    assert all(r['passed']and not r['errors']and set(r['observed']['counts'])==set(SELECTORS)for r in report['observations'])
    assert hashlib.sha256((out/'page-contracts.json').read_bytes()).hexdigest()==report['catalog_sha256']
    baseline_raw=(ROOT/'evidence/baseline/component-coverage-before-route-fix.json').read_bytes();baseline=json.loads(baseline_raw)
    assert hashlib.sha256(baseline_raw).hexdigest()==report['retained_baseline_sha256']
    assert len(report['retained_indices'])==225 and len(report['replayed_indices'])==3
    assert sorted(report['retained_indices']+report['replayed_indices'])==list(range(228))
    assert all(baseline['observations'][i]==report['observations'][i] for i in report['retained_indices'])
    assert {(report['observations'][i]['page'],report['observations'][i]['scenario'])for i in report['replayed_indices']}=={(p,'empty')for p in ['m05-p03','m05-p04','m05-p05']}
    assert all(report['observations'][i]['generated_draft_contract']for i in report['replayed_indices'])
    for p in report['static_pages']:
        for name,digest in p['dependencies'].items():assert hashlib.sha256((DEMO/name).read_bytes()).hexdigest()==digest,name
    totals={name:dict(observations_present=sum(r['observed']['counts'][name]>0 for r in report['observations']),rendered_instances=sum(r['observed']['counts'][name]for r in report['observations']))for name in SELECTORS}
    tokens={name:dict(values=sorted({r['observed']['tokens'][name]for r in report['observations']}),resolved_observations=sum(bool(r['observed']['tokens'][name])for r in report['observations']))for name in report['tokens']}
    lines=['# 114页组件与Token当前覆盖观察','',
        '空/有数据各观察一次，共228次；本表计参与布局且visibility非hidden的共享组件类，不证明屏内热区、隐藏/瞬态条件或视觉终验。E/P为两个种子的实际数量。重定向实际页保存在机器报告；不能把请求页的旧画板当作实际运行页。','',
        '组件工厂存在、控制器调用候选、实际类出现和已验证行为是四类证据。本批仅证明前述源码/运行观察；没有自动接受任何局部组件保留例外。原画板颜色字面量可能用于插画，后续按具体选择器确认其语义。','',
        '| 请求页 | '+' | '.join(SELECTORS)+' |','| --- | '+' | '.join('---:'for _ in SELECTORS)+' |']
    for p in report['static_pages']:
        pair=[next(r for r in report['observations']if r['page']==p['page']and r['scenario']==s)for s in['empty','populated']]
        lines.append('| '+p['page']+' | '+' | '.join(str(pair[0]['observed']['counts'][name])+'/'+str(pair[1]['observed']['counts'][name])for name in SELECTORS)+' |')
    lines+=['','## 已确认的接入缺口与下一步','',
        '稳定初始状态中没有Loading不能说明没有实现瞬态Loading。源码明确：回忆册load使用共享skeleton；首页搜索、日记、相册、时刻、纪念日、胶囊、工坊、宠物数据加载仍有局部文本Loading。下一步按这些load函数接入共享Loading，并维持原装载、错误/重试、焦点、禁用与数据规则。','',
        'Card/Avatar/Tag/Divider等工厂是否在产品控制器使用，需结合下面的调用候选和运行矩阵；未出现的类型不得标为全量接入完成。Input/Textarea/Header等特定分支和原画板局部样式继续审计。','',
        '| 页 | 局部颜色字面量数 | 内联CSS变量引用数 | 控制器共享调用候选数 |','| --- | ---: | ---: | ---: |']
    for p in report['static_pages']:lines.append('| '+p['page']+' | '+str(len(p['inline_colors']))+' | '+str(len(p['inline_variable_references']))+' | '+str(len(p['controller_shared_call_candidates']))+' |')
    (ROOT/'COMPONENT_COVERAGE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    token_lines=['# 共享Token声明与根节点计算值','',
        '228次同宽度运行的根节点计算值。非根作用域变量可能为空，需检查其具体元素；不同值也可能是合法主题/状态差异，不能直接当作错误。仅列当前声明和观察，不宣称局部样式已经统一。','',
        '| Token | 不同计算值 | 非空观察次数 |','| --- | --- | ---: |']
    for name,value in tokens.items():token_lines.append('| '+name+' | '+'；'.join(v.replace('|','／')or'（根节点空值）'for v in value['values'])+' | '+str(value['resolved_observations'])+'/228 |')
    (ROOT/'TOKEN_COVERAGE.md').write_text('\n'.join(token_lines)+'\n',encoding='utf-8')
    summary=dict(files=files,report_sha256=hashlib.sha256(raw).hexdigest(),pages=114,observations=228,component_types=14,component_totals=totals,tokens=tokens,accepted_pages=0)
    (out/'component-coverage-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert source()==files;print(json.dumps(dict(pages=114,observations=228,types=14,tokens=len(tokens),component_totals=totals)))

if __name__=='__main__':main()
