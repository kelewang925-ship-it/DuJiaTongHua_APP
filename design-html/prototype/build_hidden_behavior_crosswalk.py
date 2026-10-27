"""Join concrete outcome evidence to the existing 250-control observation inventory.

Unmapped actions remain gaps. Handler strings and close counts never imply a
consumer's business outcome. Retained reports keep their original source hashes.
"""
import ast,hashlib,json,re,html
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CURRENT=ROOT/'evidence/current'
SAFE_CLOSE=['取消','关闭','知道了','先看看','继续编辑','继续生成','继续照顾','继续使用','继续创建时刻']
NAMES=['hidden-overlay-observations.json','overlay-exit-path-results.json','overlay-form-save-results.json','hidden-choice-outcomes/results.json','toast-feedback/checkpoint.json','album-timeout/checkpoint.json']

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    exit_script=ROOT/'verify_overlay_exit_paths.py'
    safe_declaration=next(n.value for n in ast.parse(exit_script.read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SAFE_CLOSE' for t in n.targets))
    assert ast.literal_eval(safe_declaration)==SAFE_CLOSE
    inputs={name:json.loads((CURRENT/name).read_text(encoding='utf-8')) for name in NAMES}
    observed=inputs[NAMES[0]];exits=inputs[NAMES[1]];forms=inputs[NAMES[2]];choices=inputs[NAMES[3]]
    assert len(observed['results'])==133
    assert len(choices['results'])==choices['expected_cases']==17 and all(r['passed'] and not r['errors'] for r in choices['results'])
    assert choices['observations_sha256']==sha(CURRENT/NAMES[0])
    assert choices['script_sha256']==sha(ROOT/'verify_hidden_choice_outcomes.py')
    for name in NAMES[:3]:
        original=inputs[name]
        if name!=NAMES[0]:assert original['observations_sha256']==sha(CURRENT/NAMES[0])
        delta=[k for k,v in original['files'].items() if sha(ROOT.parent/k)!=v]
        assert set(delta)=={'assets/prototype-ui.css','assets/prototype-ui.js','assets/prototype-workshop-store.js'},delta
    for k,v in choices['files'].items():assert sha(ROOT.parent/k)==v,k
    for k,v in choices['styles'].items():assert sha(ROOT.parent/k)==v,k
    rows=[]
    for index,observation in enumerate(observed['results']):
        for overlay_index,overlay in enumerate(observation['overlays']):
            controls=overlay['controls']
            # Reproduce the existing exit runner's exact declared safe-button priority.
            safe=next((label for label in SAFE_CLOSE if any(c['label']==label and c['tag'].lower()=='button' and not c['disabled'] for c in controls)),None)
            explicit=re.findall(r'<button\b[^>]*data-cancel="true"[^>]*>(.*?)</button>',overlay['html'],re.S)
            if explicit:
                assert len(explicit)==1
                safe=html.unescape(re.sub('<[^>]+>','',explicit[0])).strip()
                assert any(c['label']==safe and not c['disabled'] for c in controls)
            for number,c in enumerate(controls):
                refs=[];business=None;state='unmapped';associated=[]
                matches=[(i,r) for i,r in enumerate(choices['results']) if r['observation_index']==index and (r['control_label']==c['label'] or (r.get('native_field') and c['tag'].lower()=='select'))]
                if matches:
                    refs=[dict(report=NAMES[3],result_index=i) for i,r in matches]
                    business='；'.join(dict.fromkeys(r.get('result') or ('跳转 '+r['destination'] if 'destination' in r else '实际下载 '+r['download_name'] if 'download_name' in r else '剪贴板 '+r['clipboard'] if 'clipboard' in r else '筛选状态／实际卡片／持久化不变断言' if r['kind'] in ['diary','photo'] else '关闭后原页和数据保留') for i,r in matches))
                    state='live-business-evidence'
                elif c['type']=='submit':
                    matches=[(i,r) for i,r in enumerate(forms['results']) if r['observation_index']==index]
                    assert matches and all(r['passed'] and not r['errors'] for i,r in matches)
                    saved=[r for i,r in matches if r['mode']=='save'];assert len(saved)==1
                    business=saved[0]['key']+' :: '+saved[0]['stored_predicate']
                    refs=[dict(report=NAMES[2],result_index=i) for i,r in matches];state='retained-business-evidence'
                elif c['tag'].lower()=='button' and c['label']==safe:
                    matches=[(i,r) for i,r in enumerate(exits['results']) if r['observation_index']==index and r['method']=='button']
                    assert matches and all(r['passed'] and r['storage_preserved'] and r['underlying_page_preserved'] for i,r in matches)
                    business='安全关闭；本地数据与底层页面保留；焦点返回。表单有脏输入时经过未保存保护。'
                    refs=[dict(report=NAMES[1],result_index=i) for i,r in matches];state='retained-close-evidence'
                if c['tag'].lower() in ['input','textarea','select']:
                    associated=[dict(report=NAMES[2],result_index=i) for i,r in enumerate(forms['results']) if r['observation_index']==index]
                if c['disabled']:
                    state='disabled-declaration';business='当前译稿未提供，保持禁用；尚未补专项不可激活证据。'
                rows.append(dict(id=f'hidden-{index:03}-{overlay_index}-{number:02}',observation_index=index,overlay_index=overlay_index,control_index=number,page=observation['page'],opener=observation['selector'],title=overlay['title'],label=c['label'],tag=c['tag'],type=c['type'],disabled=c['disabled'],historical_selector=c['selector'],handler_declaration=c.get('own_events',[]),business_contract=business,status=state,evidence=refs,associated_form_evidence=associated))
    assert len(rows)==250 and len({r['id'] for r in rows})==250
    assert sum(r['disabled'] for r in rows)==1
    counts=dict(Counter(r['status'] for r in rows))
    assert counts=={'retained-close-evidence':95,'live-business-evidence':15,'unmapped':123,'retained-business-evidence':16,'disabled-declaration':1},counts
    report=dict(scope='Crosswalk of existing 250 observed controls, not a new page inventory or new full audit. Unmapped includes already-tested actions not yet associated; it does not imply product absence.',source_files=choices['files'],inputs_sha256={n:sha(CURRENT/n) for n in NAMES},exit_selection_script_sha256=sha(exit_script),builder_sha256=sha(Path(__file__)),summary=counts,rows=rows,accepted_pages=0,retained_source_policy='Original observations/close/form reports retain old source fingerprints. Only album decoder and Toast differ; linked scoped checkpoints explain retention. No old report was rerun or relabeled current. Native input association alone is not complete input validation.')
    out=CURRENT/'hidden-behavior-crosswalk.json'
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(controls=len(rows),summary=counts),ensure_ascii=False))

if __name__=='__main__':main()
