"""Publish a source-bound initial catalog only after its full replay passes."""
import argparse,json,re,shutil
from pathlib import Path
from urllib.parse import urlparse
from replay_current_initial_controls import ROOT,DEMO,deps,sha

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def clean(v):return str(v).replace('|','／').replace('\n',' / ').replace('\r','')
def page_id(url):
    m=re.search(r'm\d{2}-p\d{2}',urlparse(url).path);return m[0] if m else None

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--report',required=True);args=parser.parse_args();path=(ROOT/args.report).resolve();assert path.is_relative_to(ROOT)
    report=read(path);assert report['complete'] and report['all_passed'] and not report['inventory_errors']
    assert report['dependencies']==deps();assert all(r['passed'] and not r['errors'] for r in report['results'])
    assert all(sha(ROOT/n)==h for n,h in report['fixture_sha256'].items())
    legacy_path=ROOT/'evidence/current/page-contracts.json';legacy=read(legacy_path);manifest=read(DEMO/'manifest.json');ids={v['id'] for v in manifest}
    inventory=report['inventory'];assert len(inventory)==114 and {v['page'] for v in inventory}==ids
    observed={(v['page'],c['selector']) for v in inventory for c in v['controls']}
    assert len(observed)==sum(len(v['controls']) for v in inventory)
    actual={(v['page'],v['selector']) for v in report['results']};assert len(actual)==len(report['results']) and observed==actual
    for id in ids:assert (DEMO/'custom'/f'{id}.html').read_bytes()==(DEMO/'pages'/f'{id}.html').read_bytes(),id
    relative=path.relative_to(ROOT).as_posix();out=path.parent;contract_relative=(out/'contracts.json').relative_to(ROOT).as_posix()
    by_id={v['id']:v for v in legacy['pages']};rows=[];edges=[]
    indexed={(v['page'],v['selector']):(i,v) for i,v in enumerate(report['results'])}
    for i,entry in enumerate(inventory):
        id=entry['page'];before=by_id[id];controls=[]
        for c in entry['controls']:
            index,result=indexed[(id,c['selector'])]
            controls.append({'page':id,'selector':c['selector'],'label':c['label'],'contract':result['contract'],'report':relative,'result_index':index,'status':'当前源码实际执行通过','effective':result['effective'],'execution':result['execution']})
            target=page_id(result['effective']);assert target in ids,(id,result['effective'])
            if target!=id:edges.append({'source':id,'target':target,'label':c['label'],'contract':result['contract'],'actual_url':result['effective'],'report':relative,'result_index':index})
        rows.append({'id':id,'title':before['title'],'type':before['type'],'required_states':before['required_states'],'html':f'pages/{id}.html','html_sha256':sha(DEMO/'pages'/f'{id}.html'),'fixture_group':entry['group'],'initial_url':entry['effective'],'inventory_index':i,'initial_controls':controls,'observed_disabled_controls':[{'label':c['label'],'selector':c['selector']} for c in entry['observed']['controls'] if c['visible'] and c['disabled']],'acceptance':'Only the declared initial fixture is verified. Other states, hidden outcomes, journeys and visual acceptance remain separate.'})
    result={'scope':'Current114 declared initial fixtures and all their accessible enabled controls. Real observed destinations only. Not whole-product, hidden-state or visual acceptance.','dependencies':deps(),'report':relative,'report_sha256':sha(path),'legacy_taxonomy_source':'evidence/current/page-contracts.json','legacy_taxonomy_sha256':sha(legacy_path),'pages':rows,'edges':edges,'human_accepted_pages':0,'producer_sha256':sha(Path(__file__))}
    write(out/'contracts.json',result)
    history=ROOT/'evidence/history/pre-current-initial-catalog-8cce41c';history.mkdir(parents=True,exist_ok=True)
    for n in ['PAGE_CATALOG.md','CURRENT_NAVIGATION.md','CONTROL_BEHAVIORS.md','queue.json','README.md','ACCEPTANCE_REQUIREMENTS.md','ISSUES.md']:
        if not(history/n).exists():shutil.copy2(ROOT/n,history/n)
    queue=read(history/'queue.json');assert len(queue)==114
    for q in queue:
        entry=next(v for v in rows if v['id']==q['id']);q['page_contract']=contract_relative+'#'+q['id'];q['current_initial_control_checks']=len(entry['initial_controls'])
        q['current_initial_control_evidence']={'report':relative,'report_sha256':sha(path),'inventory_index':entry['inventory_index'],'scope':'Declared initial fixture only; full page acceptance unchanged.'}
    write(ROOT/'queue.json',queue)
    intro=f'本轮114页初态观察与{len(report["results"])}项控件结果均对应当前源码；实际导航{len(edges)}条。每次操作使用独立本地模拟数据。逐项结果：[{relative}]({relative})；机器可读合同：[{contract_relative}]({contract_relative})。'
    boundary='这里只证明声明初态的可用控件，不替代隐藏／条件分支、全部错误／返回／长输入、连续流程、原稿视觉及原41项完整验收。旧全量JSON与原图保留历史版本，不将旧报告重绑为新源码。'
    catalog=['# 当前114页页面清单','',intro,'',boundary,'','| 页面 | 名称 | 页面类型 | 初态控件 | 实际入口页 | 实际出口页 |','| --- | --- | --- | ---: | --- | --- |']
    for p in rows:
        incoming=sorted({e['source'] for e in edges if e['target']==p['id']});outgoing=sorted({e['target'] for e in edges if e['source']==p['id']})
        catalog.append('| '+' | '.join(map(clean,[p['id'],p['title'],p['type'],len(p['initial_controls']),', '.join(incoming) or '本轮初态未观察到；条件入口另审',', '.join(outgoing) or '本轮无跨页结果；本页交互见合同']))+' |')
    catalog+=['','初态URL、每个selector／行为合同／实际落点／报告行索引及禁用观察均见机器合同。原稿页面角色及所需状态沿用既有逐页分类，不因初态通过取消其他状态要求。','', '历史页面表保存在`evidence/history/pre-current-initial-catalog-8cce41c/PAGE_CATALOG.md`。完整状态矩阵仍为STATE_MATRIX；其存在不代表当前全部状态已通过。']
    (ROOT/'PAGE_CATALOG.md').write_text('\n'.join(catalog)+'\n',encoding='utf-8')
    nav=['# 当前页面导航与来源','',intro,'',boundary,'','本轮实线关系图：[CURRENT_INITIAL_NAVIGATION.mmd](CURRENT_INITIAL_NAVIGATION.mmd)。原PAGE_RELATIONSHIPS与回忆册隐藏关系图保留各自历史范围；完整条件图仍需按当前证据统一。','','| 来源页 | 操作 | 当前行为合同 | 实际目标 | 实际URL | 结果行 |','| --- | --- | --- | --- | --- | --- |']
    for e in edges:nav.append('| '+' | '.join(map(clean,[e['source'],e['label'],e['contract'],e['target'],e['actual_url'],e['result_index']]))+' |')
    nav+=['','同文档操作、弹层、输入及无跨页动作均保留在逐控件合同中，不虚构为页面跳转。当前初态没有入边不等于死路；需结合条件／隐藏流程验证。历史导航正文保存在`evidence/history/pre-current-initial-catalog-8cce41c/CURRENT_NAVIGATION.md`。']
    (ROOT/'CURRENT_NAVIGATION.md').write_text('\n'.join(nav)+'\n',encoding='utf-8')
    graph=['flowchart TD','  %% Current observed initial-control destinations only; other conditions remain separate.']
    for p in rows:graph.append('  '+p['id'].replace('-','_')+'["'+p['id']+' · '+p['type']+'"]')
    for e in edges:graph.append('  '+e['source'].replace('-','_')+' -->|"'+clean(e['label']).replace('"','').replace('<','').replace('>','')+'"| '+e['target'].replace('-','_'))
    (ROOT/'CURRENT_INITIAL_NAVIGATION.mmd').write_text('\n'.join(graph)+'\n',encoding='utf-8')
    behaviors=['# 当前控件行为与执行清单','',intro,'',boundary,'','| 页面 | 控件 | 明确行为合同 | 实际URL | 结果行 |','| --- | --- | --- | --- | --- |']
    for p in rows:
        for c in p['initial_controls']:behaviors.append('| '+' | '.join(map(clean,[p['id'],c['label'],c['contract'],c['effective'],c['result_index']]))+' |')
    behaviors+=['','原隐藏250控件及回忆册V2106次控件出现的对应表保留执行版本，入口见BOOK_V2_HIDDEN_OUTCOMES。原控件正文及阶段说明在`evidence/history/pre-current-initial-catalog-8cce41c/CONTROL_BEHAVIORS.md`；不将其自动计入本轮新执行。']
    (ROOT/'CONTROL_BEHAVIORS.md').write_text('\n'.join(behaviors)+'\n',encoding='utf-8')
    readme=(ROOT/'README.md').read_text(encoding='utf-8');old='[逐页机器可读合同](evidence/current/page-contracts.json)';new=f'[逐页机器可读合同]({contract_relative})'
    if old in readme:readme=readme.replace(old,new,1)
    (ROOT/'README.md').write_text(readme,encoding='utf-8')
    print('Published114 current initial page contracts;',len(report['results']),'controls;',len(edges),'actual navigation results; other acceptance flags unchanged')

if __name__=='__main__':main()
