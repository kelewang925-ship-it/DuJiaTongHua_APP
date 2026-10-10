"""Bind declared form results to evidence and update hidden control coverage."""
import hashlib,json
from verify_pet_controls import ROOT,source
from verify_overlay_form_saves import SPECS,CANDIDATES
from build_overlay_exit_summary import main as build_exit_summary

def main():
    out=ROOT/'evidence/current';path=out/'overlay-form-save-results.json';raw=path.read_bytes();report=json.loads(raw);files=source()
    observed_raw=(out/'hidden-overlay-observations.json').read_bytes();observed=json.loads(observed_raw)
    assert report['files']==observed['files']==files and report['observations_sha256']==hashlib.sha256(observed_raw).hexdigest()
    expected={(index,mode)for index in SPECS for mode in ['save','quota-retry','invalid']if mode!='invalid'or index!=52}
    actual={(row['observation_index'],row['mode'])for row in report['results']}
    assert actual==expected and len(actual)==len(report['results'])==report['expected_cases']==47
    assert all(row['passed']and not row['errors']for row in report['results'])
    contracts=[]
    for index,(values,key,predicate)in SPECS.items():
        original=observed['results'][index]
        contracts.append(dict(observation_index=index,page=original['page'],title=original['overlays'][0]['title'],values=values,key=key,predicate=predicate,
            candidate_parent_save=index in CANDIDATES,result_indexes=[n for n,row in enumerate(report['results'])if row['observation_index']==index],
            remaining='other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts'))
    def clean(value):return str(value).replace('|','／').replace('\n',' ')
    lines=['# 已观察保存表单的结果与失败恢复','',
        '16个入口、47项当前执行：16成功、16定向本地空间失败后重试、15空值拒绝（固定动效Select无空值选项）。检查提交loading/disabled、两次快速DOM激活、输入保持与明确存储结果谓词。空值测试只证明首错，不代替逐字段所有校验。','',
        '14个表单直接持久化；寄语／章节先回填候选，父页面保存才写入。QuotaExceededError仅在测试上下文针对目标localStorage键抛一次；生产函数未替换。未声称所有网络／权限／失效失败已覆盖。','',
        '| 观察索引／页面 | 表单 | 声明有效输入 | 写入方式／键 | 当前项数 | 剩余 |','| --- | --- | --- | --- | ---: | --- |']
    for row in contracts:
        lines.append('| '+' | '.join(clean(value)for value in [str(row['observation_index'])+' / '+row['page'],row['title'],'；'.join(key+'='+value for key,value in row['values'].items()),('候选→父页保存 / 'if row['candidate_parent_save']else'直接持久化 / ')+row['key'],len(row['result_indexes']),row['remaining']])+' |')
    (ROOT/'OVERLAY_FORM_SAVES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    summary=dict(files=files,report_sha256=hashlib.sha256(raw).hexdigest(),contracts=contracts,cases=47,passed=47,accepted_pages=0)
    (out/'overlay-form-save-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # Rebuild the existing baseline ledger before applying the new form evidence layer.
    build_exit_summary()
    ledger=ROOT/'HIDDEN_CONTROL_BEHAVIORS.md';text=ledger.read_text(encoding='utf-8');updated=[]
    hidden=json.loads((out/'hidden-overlay-index.json').read_text(encoding='utf-8'));assert hidden['files']==files
    controls={(control['page'],control['observation_index'],control['control_index']):control['observed_control']for control in hidden['hidden_controls']}
    for line in text.splitlines():
        parts=line.split('|')
        if len(parts)>5 and parts[1].strip().startswith('m'):
            page,index,number=parts[1].strip().split(' / ');index=int(index);control=controls[(page,index,int(number))]
            if index in SPECS:
                if control['type']=='submit':
                    parts[4]=' 声明有效输入提交、Loading/禁用、存储失败保持后重试及明确结果通过；寄语/章节含父页保存。其他校验、提交取消与来源条件继续 '
                elif control['native_input']and control['label']in SPECS[index][0]:
                    parts[4]=' 声明有效值输入及失败后的字段快照保持通过；空值首错不证明本字段全部校验，其他输入条件继续 '
                line='|'.join(parts)
        updated.append(line)
    updated.insert(2,'表单当前47项明确结果见[OVERLAY_FORM_SAVES](OVERLAY_FORM_SAVES.md)；原关闭/二层取消证据与其他控件剩余范围保留。')
    ledger.write_text('\n'.join(updated)+'\n',encoding='utf-8')
    assert source()==files;print(json.dumps(dict(forms=len(contracts),save_cases=47,direct_forms=14,parent_save_forms=2,accepted_pages=0)))

if __name__=='__main__':main()
