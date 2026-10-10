"""Validate exact deletion cases and layer their evidence into the hidden ledger."""
import hashlib,json
from verify_pet_controls import ROOT,source
from verify_confirmed_deletions import SPECS
from build_overlay_form_save_summary import main as build_form_summary

def main():
    out=ROOT/'evidence/current';raw=(out/'confirmed-deletion-results.json').read_bytes();report=json.loads(raw)
    observed_raw=(out/'hidden-overlay-observations.json').read_bytes();observed=json.loads(observed_raw);files=source()
    assert report['files']==observed['files']==files
    assert report['observations_sha256']==hashlib.sha256(observed_raw).hexdigest()
    expected={(i,m)for i in SPECS for m in ['success','semantic-retry','quota-retry']}
    assert {(r['observation_index'],r['mode'])for r in report['results']}==expected
    assert len(report['results'])==report['expected_cases']==45
    assert all(r['passed']and not r['errors']for r in report['results'])
    contracts=[]
    for i,(kind,operation,destination)in SPECS.items():
        rows=[(n,r)for n,r in enumerate(report['results'])if r['observation_index']==i]
        assert len({r['target_id']for _,r in rows})==1
        contracts.append(dict(observation_index=i,page=observed['results'][i]['page'],key='dujia-prototype-'+kind,
            target_id=rows[0][1]['target_id'],operation=operation,destination=destination,result_indexes=[n for n,_ in rows]))
    summary=dict(files=files,report_sha256=hashlib.sha256(raw).hexdigest(),contracts=contracts,cases=45,passed=45,accepted_pages=0)
    (out/'confirmed-deletion-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# 已观察记录类确认删除结果','',
        '15个入口、45项当前检查：确认成功、演示操作失败后重试、真实一次空间不足后重试各15项。核对目标移除、同集合其他记录保持、关联和其他存储保持、实际落点。失败保持全量localStorage且留在原页；重新打开操作菜单并确认后重试。','',
        '标签另给一条已有记录写入被删标签与保留标签，核对记录正文和保留标签不变。空间不足在标签事务的第二次records写入抛出，验证tags回滚后重试。自动备份允许按现有策略更新，未声称验证所有备份内容。','',
        '本批不覆盖删除过程中正文/权限变化、所有来源返回或快速重复激活；账号/宠物身份删除、章节和书页候选→保存排列仍继续。114页最终验收仍0。','',
        '| 页面／观察索引 | 存储目标 | 演示失败操作 | 成功落点 | 当前项数 |','| --- | --- | --- | --- | ---: |']
    for r in contracts:lines.append('| '+r['page']+' / '+str(r['observation_index'])+' | '+r['key']+' / '+r['target_id']+' | '+r['operation']+' | '+(r['destination']or'当前标签列表重绘')+' | 3 |')
    (ROOT/'CONFIRMED_DELETIONS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    build_form_summary()
    ledger=ROOT/'HIDDEN_CONTROL_BEHAVIORS.md';hidden=json.loads((out/'hidden-overlay-index.json').read_text(encoding='utf-8'))
    controls={(c['page'],c['observation_index'],c['control_index']):c['observed_control']for c in hidden['hidden_controls']}
    updated=[]
    for line in ledger.read_text(encoding='utf-8').splitlines():
        parts=line.split('|')
        if len(parts)>5 and parts[1].strip().startswith('m'):
            page,index,number=parts[1].strip().split(' / ');index=int(index);control=controls[(page,index,int(number))]
            if index in SPECS and control['label'].startswith('删除'):
                parts[4]=' 二层确认取消及确认后删除结果、演示失败/空间不足保持与重试通过；同集合和关联存储核对。删除途中变化、其他来源和重复激活继续 '
                line='|'.join(parts)
        updated.append(line)
    updated.insert(2,'记录类删除当前45项结果见[CONFIRMED_DELETIONS](CONFIRMED_DELETIONS.md)。重新生成此账本使用build_confirmed_deletion_summary.py，以保留关闭、表单和删除三阶段证据。')
    ledger.write_text('\n'.join(updated)+'\n',encoding='utf-8')
    assert source()==files
    print(json.dumps(dict(entries=15,cases=45,passed=45,accepted_pages=0)))

if __name__=='__main__':main()
