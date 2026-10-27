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
NAMES+=['confirmed-deletion-results.json','book-candidate-deletion-results.json','identity-deletion-results.json','hidden-auxiliary-outcomes/results.json']
NAMES+=['hidden-settings-pet-outcomes/results.json']
NAMES+=['hidden-workshop-outcomes/results.json']
NAMES+=['hidden-book-editor-outcomes/results.json']
NAMES+=['hidden-book-structure-outcomes/results.json']
NAMES+=['pet-home-visual/checkpoint.json']
NAMES+=['relationship-day-counter/checkpoint.json']
NAMES+=['photo-detail-image-bounds/checkpoint.json']

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def assignment(path,name):
    return next(n.value for n in ast.parse(path.read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
def main():
    exit_script=ROOT/'verify_overlay_exit_paths.py'
    safe_declaration=next(n.value for n in ast.parse(exit_script.read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SAFE_CLOSE' for t in n.targets))
    assert ast.literal_eval(safe_declaration)==SAFE_CLOSE
    inputs={name:json.loads((CURRENT/name).read_text(encoding='utf-8')) for name in NAMES}
    observed=inputs[NAMES[0]];exits=inputs[NAMES[1]];forms=inputs[NAMES[2]];choices=inputs[NAMES[3]]
    pet_patch=inputs[NAMES[14]]
    relationship_patch=inputs[NAMES[15]]
    photo_patch=inputs[NAMES[16]]
    assert photo_patch['baseline_files']==relationship_patch['files']
    assert photo_patch['changed_files']==['custom/m03-p12.html'] and photo_patch['html_body_and_scripts_unchanged']
    assert photo_patch['verifier_sha256']==sha(ROOT/'verify_photo_detail_image_bounds.py')
    for path,digest in photo_patch['artifacts_sha256'].items():assert sha(ROOT/path)==digest,path
    assert relationship_patch['baseline_files']==pet_patch['files']
    assert set(relationship_patch['changed_files'])=={'assets/prototype-relationship.js','custom/m02-p06.html'} and relationship_patch['other_controller_ast_equal']
    for path,digest in relationship_patch['artifacts_sha256'].items():assert sha(ROOT/path)==digest,path
    assert pet_patch['baseline_files']==choices['files']
    assert pet_patch['changed_files']==['custom/m07-p03.html'] and pet_patch['html_body_and_scripts_unchanged']
    assert pet_patch['verifier_sha256']==sha(ROOT/'verify_pet_home_visual_text.py')
    for path,digest in pet_patch['artifacts_sha256'].items():assert sha(ROOT/path)==digest,path
    assert len(observed['results'])==133
    assert len(choices['results'])==choices['expected_cases']==17 and all(r['passed'] and not r['errors'] for r in choices['results'])
    assert choices['observations_sha256']==sha(CURRENT/NAMES[0])
    assert choices['script_sha256']==sha(ROOT/'verify_hidden_choice_outcomes.py')
    for name in NAMES[:3]+NAMES[6:9]:
        original=inputs[name]
        if name!=NAMES[0]:assert original['observations_sha256']==sha(CURRENT/NAMES[0])
        delta=[k for k,v in original['files'].items() if sha(ROOT.parent/k)!=v]
        assert set(delta)=={'assets/prototype-ui.css','assets/prototype-ui.js','assets/prototype-workshop-store.js','custom/m07-p03.html','assets/prototype-relationship.js','custom/m02-p06.html','custom/m03-p12.html'},delta
    for k,v in photo_patch['files'].items():assert sha(ROOT.parent/k)==v,k
    for k,v in choices['styles'].items():assert sha(ROOT.parent/k)==v,k
    for name,script,total in [(NAMES[9],'verify_hidden_auxiliary_outcomes.py',9),(NAMES[10],'verify_hidden_settings_pet_outcomes.py',24),(NAMES[11],'verify_hidden_workshop_outcomes.py',14),(NAMES[12],'verify_hidden_book_editor_outcomes.py',18),(NAMES[13],'verify_hidden_book_structure_outcomes.py',16)]:
        auxiliary=inputs[name]
        assert auxiliary['files']==choices['files'] and len(auxiliary['results'])==auxiliary['expected_cases']==total
        assert auxiliary['script_sha256']==sha(ROOT/script)
        assert auxiliary['observations_sha256']==sha(CURRENT/NAMES[0])
        assert all(r['passed'] and not r['errors'] for r in auxiliary['results'])
        for fixture,digest in auxiliary.get('fixture_scripts',{}).items():assert sha(ROOT/fixture)==digest
        if 'fixture_script_sha256' in auxiliary:assert auxiliary['fixture_script_sha256']==sha(ROOT/'verify_book_controls.py')
    live=[(name,i,r) for name in [NAMES[3],NAMES[9],NAMES[10],NAMES[11],NAMES[12],NAMES[13]] for i,r in enumerate(inputs[name]['results'])]
    nested=ast.literal_eval(assignment(ROOT/'verify_nested_confirmations.py','CASES'))
    declarations=assignment(ROOT/'verify_overlay_form_saves.py','SPECS')
    field_specs={ast.literal_eval(key):[ast.literal_eval(k) for k in value.elts[0].keys] for key,value in zip(declarations.keys,declarations.values)}
    for name,total in zip(NAMES[6:9],[45,25,13]):
        assert len(inputs[name]['results'])==inputs[name]['expected_cases']==total
        assert all(r['passed'] and not r['errors'] for r in inputs[name]['results'])
    rows=[]
    for index,observation in enumerate(observed['results']):
        for overlay_index,overlay in enumerate(observation['overlays']):
            controls=overlay['controls']
            fields=[c for c in controls if c['tag'].lower() in ['input','textarea','select']]
            if index in field_specs:
                assert len(fields)==len(field_specs[index])
                assert all(label in html.unescape(overlay['html']) for label in field_specs[index])
            # Reproduce the existing exit runner's exact declared safe-button priority.
            safe=next((label for label in SAFE_CLOSE if any(c['label']==label and c['tag'].lower()=='button' and not c['disabled'] for c in controls)),None)
            explicit=re.findall(r'<button\b[^>]*data-cancel="true"[^>]*>(.*?)</button>',overlay['html'],re.S)
            if explicit:
                assert len(explicit)==1
                safe=html.unescape(re.sub('<[^>]+>','',explicit[0])).strip()
                assert any(c['label']==safe and not c['disabled'] for c in controls)
            for number,c in enumerate(controls):
                refs=[];business=None;state='unmapped';associated=[]
                matches=[(name,i,r) for name,i,r in live if r['observation_index']==index and (r['control_label']==c['label'] or (r.get('native_field') and c['tag'].lower()=='select') or (c['tag'].lower() in ['input','textarea','select'] and c['label'] in r.get('native_controls',[])))]
                if matches:
                    refs=[dict(report=name,result_index=i) for name,i,r in matches]
                    business='；'.join(dict.fromkeys(r.get('result') or ('跳转 '+r['destination'] if 'destination' in r else '实际下载 '+r['download_name'] if 'download_name' in r else '剪贴板 '+r['clipboard'] if 'clipboard' in r else '筛选状态／实际卡片／持久化不变断言' if r['kind'] in ['diary','photo'] else '关闭后原页和数据保留') for name,i,r in matches))
                    state='live-business-evidence'
                elif index in nested and c['label']==nested[index][0]:
                    matches=[(name,i,r) for name in NAMES[6:9] for i,r in enumerate(inputs[name]['results']) if r['observation_index']==index]
                    assert matches
                    refs=[dict(report=name,result_index=i) for name,i,r in matches]
                    modes={r['mode'] for name,i,r in matches}
                    if matches[0][0]==NAMES[6]:
                        assert modes=={'success','semantic-retry','quota-retry'}
                        assert all(r['siblings_preserved'] and r['related_storage_preserved'] for name,i,r in matches)
                        first=matches[0][2]
                        business=f'二层确认「{nested[index][1]}」；删除 {first["key"]} 中 {first["target_id"]}；其他记录／相关存储保留；语义失败与容量失败可重试；落点 '+str(first['destination'])
                    elif matches[0][0]==NAMES[7]:
                        assert modes=={'save','discard','semantic-retry','quota-retry','external-update'}
                        assert all(r['candidate_deferred'] for name,i,r in matches)
                        business='二层确认后仅更新编排候选；父页保存才持久化章节／书页及关联索引；放弃保留原始册，失败可重试，外部更新不被旧候选覆盖。'
                    else:
                        assert {'success','blank','wrong','dirty-cancel','semantic-retry','quota-retry'}<=modes
                        business='打开二层身份确认，校验验证码／宠物名；脏输入可继续或放弃；确认后只清理声明数据边界，语义／容量失败保留输入与数据并可重试。'
                    state='retained-business-evidence'
                elif c in fields and index in field_specs:
                    matches=[(i,r) for i,r in enumerate(forms['results']) if r['observation_index']==index]
                    saved=next(r for i,r in matches if r['mode']=='save')
                    label=field_specs[index][fields.index(c)]
                    business='原表单按明确标签「'+label+'」填写／选择；实际提交后检查 '+saved['key']+' :: '+saved['stored_predicate']+'；只证明声明输入及校验／重试案例，不推断任意输入。'
                    refs=[dict(report=NAMES[2],result_index=i) for i,r in matches];state='retained-field-evidence'
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
                if c['disabled'] and state=='live-business-evidence':state='live-disabled-evidence'
                elif c['disabled']:
                    state='disabled-declaration';business='当前译稿未提供，保持禁用；尚未补专项不可激活证据。'
                rows.append(dict(id=f'hidden-{index:03}-{overlay_index}-{number:02}',observation_index=index,overlay_index=overlay_index,control_index=number,page=observation['page'],opener=observation['selector'],title=overlay['title'],label=c['label'],tag=c['tag'],type=c['type'],disabled=c['disabled'],historical_selector=c['selector'],handler_declaration=c.get('own_events',[]),business_contract=business,status=state,evidence=refs,associated_form_evidence=associated))
    assert len(rows)==250 and len({r['id'] for r in rows})==250
    assert sum(r['disabled'] for r in rows)==1
    counts=dict(Counter(r['status'] for r in rows))
    assert counts=={'retained-close-evidence':94,'live-business-evidence':98,'retained-business-evidence':38,'retained-field-evidence':19,'live-disabled-evidence':1},counts
    assert all(r['business_contract'] and r['evidence'] for r in rows)
    producers=['verify_overlay_exit_paths.py','verify_overlay_form_saves.py','verify_nested_confirmations.py','verify_confirmed_deletions.py','verify_book_candidate_deletions.py','verify_identity_deletions.py']
    report=dict(scope='Crosswalk of existing 250 observed controls, not a new page inventory or new full audit.',source_files=photo_patch['files'],base_behavior_source_files=choices['files'],inputs_sha256={n:sha(CURRENT/n) for n in NAMES},contract_scripts_sha256={n:sha(ROOT/n) for n in producers},exit_selection_script_sha256=sha(exit_script),builder_sha256=sha(Path(__file__)),summary=counts,rows=rows,accepted_pages=0,retained_source_policy='Original observations/close/form/deletion reports retain old source fingerprints. Album,Toast,pet CSS,profile day display and photo image bounds have explicit preservation checkpoints.98 business cases keep their original pre-visual source;25 pet checks and20 profile checks retain scope through exact CSS/body preservation or equal original action AST. Photo-only grid dimensions retain original body/scripts/shared assets with25 focused cases. No old report was rerun or relabeled current. Native field evidence proves declared input and submission cases, not arbitrary input validation.')
    out=CURRENT/'hidden-behavior-crosswalk.json'
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(controls=len(rows),summary=counts),ensure_ascii=False))

if __name__=='__main__':main()
