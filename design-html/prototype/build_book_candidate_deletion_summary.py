"""Bind five arrangement deletion contracts and retain previous evidence layers."""
import hashlib,json
from verify_pet_controls import ROOT,source
from verify_book_candidate_deletions import SPECS,MODES
from build_confirmed_deletion_summary import main as build_direct_summary

def main():
    out=ROOT/'evidence/current';raw=(out/'book-candidate-deletion-results.json').read_bytes();report=json.loads(raw)
    observed_raw=(out/'hidden-overlay-observations.json').read_bytes();observed=json.loads(observed_raw);files=source()
    assert report['files']==observed['files']==files
    assert report['observations_sha256']==hashlib.sha256(observed_raw).hexdigest()
    assert {(r['observation_index'],r['mode'])for r in report['results']}=={(i,m)for i in SPECS for m in MODES}
    assert len(report['results'])==report['expected_cases']==25
    assert all(r['passed']and not r['errors']and r['candidate_deferred']for r in report['results'])
    contracts=[]
    for i,(kind,target)in SPECS.items():
        rows=[(n,r)for n,r in enumerate(report['results'])if r['observation_index']==i]
        contracts.append(dict(observation_index=i,page='m08-p13',kind=kind,target=target,result_indexes=[n for n,_ in rows],
            persistent_contract=next(r['persistent_contract']for _,r in rows if r['mode']=='save')))
    summary=dict(files=files,report_sha256=hashlib.sha256(raw).hexdigest(),contracts=contracts,cases=25,passed=25,accepted_pages=0)
    (out/'book-candidate-deletion-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# 回忆册章节与书页候选删除结果','',
        '5入口×5条件=25项当前执行：保存、返回后继续/放弃、演示保存失败后重试、真实空间不足后重试、另一处更新后拒绝旧编排并放弃。确认删除只改变当前候选，保存排列后才持久化。','',
        '种子为3页/2章节，每页已有补页、全页书签、最后阅读page-second、selected素材引用，以及另一册。核对删除章节连同其页、书页及补页消失、书签/最后阅读/selected正确清理、其他页补页和另一册保留、原始来源存储不变。保存检查包含两次快速DOM激活及Loading/禁用；未声称所有输入设备时序已覆盖。','',
        '外部更新测试仅另一处修改册名与updatedAt；当前编排保持、拒绝覆盖新数据，放弃后新数据保持。不是全部来源/权限/删除竞争条件。环境390×844减少动效；全114页最终验收仍0。','',
        '| 页面／观察索引 | 删除候选 | 保存后剩余章节 | 保存后剩余书页 | 书签／最后阅读 | 当前项数 |','| --- | --- | --- | --- | --- | ---: |']
    for r in contracts:
        d=r['persistent_contract'];lines.append('| m08-p13 / '+str(r['observation_index'])+' | '+r['kind']+' / '+r['target']+' | '+', '.join(v['id']for v in d['chapters'])+' | '+', '.join(v['id']for v in d['pages'])+' | '+', '.join(d['bookmarks'])+' / '+str(d['lastPage'])+' | 5 |')
    (ROOT/'BOOK_CANDIDATE_DELETIONS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    build_direct_summary()
    hidden=json.loads((out/'hidden-overlay-index.json').read_text(encoding='utf-8'))
    controls={(c['page'],c['observation_index'],c['control_index']):c['observed_control']for c in hidden['hidden_controls']}
    ledger=ROOT/'HIDDEN_CONTROL_BEHAVIORS.md';updated=[]
    for line in ledger.read_text(encoding='utf-8').splitlines():
        parts=line.split('|')
        if len(parts)>5 and parts[1].strip().startswith('m'):
            page,index,number=parts[1].strip().split(' / ');index=int(index);control=controls[(page,index,int(number))]
            if index in SPECS and control['label']in['删除章节','删除书页']:
                parts[4]=' 二层取消及确认后候选删除、返回继续/放弃、保存后清理引用、两种失败保持/重试、外部更新拒绝覆盖通过；原记录与另一册保持。其他来源/权限/竞争/布局继续 '
                line='|'.join(parts)
        updated.append(line)
    updated.insert(2,'章节／书页候选删除25项见[BOOK_CANDIDATE_DELETIONS](BOOK_CANDIDATE_DELETIONS.md)。重建完整账本使用build_book_candidate_deletion_summary.py，保留前序关闭、表单和记录删除证据层。')
    ledger.write_text('\n'.join(updated)+'\n',encoding='utf-8')
    assert source()==files;print(json.dumps(dict(entries=5,cases=25,passed=25,accepted_pages=0)))

if __name__=='__main__':main()
