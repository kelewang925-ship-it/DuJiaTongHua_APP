"""Current identity deletion evidence; older hidden evidence remains historical."""
import hashlib,json
from verify_pet_controls import ROOT,source
from verify_identity_deletions import SPECS,MODES

def main():
    out=ROOT/'evidence/current';raw=(out/'identity-deletion-results.json').read_bytes();report=json.loads(raw);files=source()
    expected={(i,m)for i in SPECS for m in MODES+(['quota-late-retry']if i==59 else[])}
    assert report['files']==files
    assert len(report['results'])==report['expected_cases']==13
    assert {(r['observation_index'],r['mode'])for r in report['results']}==expected
    assert all(r['passed']and not r['errors']for r in report['results'])
    observed_raw=(out/'hidden-overlay-observations.json').read_bytes()
    assert report['observations_sha256']==hashlib.sha256(observed_raw).hexdigest()
    contracts=[dict(observation_index=i,page=next(r['page']for r in report['results']if r['observation_index']==i),identity_label=values[1],submit=values[2],operation=values[3],destination=values[5],result_indexes=[n for n,r in enumerate(report['results'])if r['observation_index']==i])for i,values in SPECS.items()]
    summary=dict(files=files,report_sha256=hashlib.sha256(raw).hexdigest(),contracts=contracts,cases=13,passed=13,accepted_pages=0,
                 historical_observation_changed_files=report['historical_observation_changed_files'])
    (out/'identity-deletion-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'IDENTITY_DELETIONS.md').write_text('''# 身份确认删除与失败恢复

当前13项检查：账号7项、宠物6项。两者成功、空输入、错误身份、修改后继续/放弃、演示失败后重试、一次空间不足后重试；账号另测第二次内容写入失败后的回滚。

账号验证码284631，注销成功进入m01-p01；清理dujia-/fairy-本地与会话键，七类内容保留空集合（pet=null），无关哨兵键保留。宠物确认当前名字，成功进入m07-p04，仅pet=null，普通日记/照片及其他存储保留。失败保存完整存储及输入，重试须再次明确提交。

P1：原注销先删除全部本地数据，再写空集合；写入失败导致数据丢失。已改为先建立空内容，再移除账号资料，失败恢复快照。测试覆盖一次可恢复异常；持续存储不可用不属于这批成功恢复证明。

历史隐藏观察仅复用两个入口selector与标题，当前运行再次核对。允许变化仅prototype-preferences.js；并未把旧99弹层/250控件、旧初始控件或前序保存/删除证据标为当前。完整114页流程验收仍未完成。
''',encoding='utf-8')
    assert source()==files;print(json.dumps(dict(cases=13,passed=13,accepted_pages=0)))

if __name__=='__main__':main()
