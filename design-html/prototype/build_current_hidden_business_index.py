"""Join current observed controls to exact fresh lifecycle/business evidence.

Historical crosswalks supply semantic correspondence only. References are
resolved by explicit case identity into newly executed reports, never rebound.
"""
import json
from collections import Counter
from pathlib import Path
from replay_current_initial_controls import ROOT, deps, sha, dump
from replay_current_hidden_business import OUT as RAW
from complete_current_hidden_business import OUT as FINAL
from replay_current_hidden_pickers import OUT as PICKERS


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    report = load(FINAL / 'results.json')
    assert report['complete'] and report['all_passed'] and report['dependencies'] == deps()
    assert load(PICKERS / 'execution.json')['all_passed']
    lifecycle_path = ROOT / 'evidence/current/overlay-lifecycle-20261031-final/results.json'
    lifecycle = load(lifecycle_path)
    catalog_path = RAW / 'catalog-overlays.json'
    catalog = load(catalog_path)
    drag_path = RAW / 'catalog-drag-results.json'
    drag = load(drag_path)
    assert lifecycle['dependencies'] == catalog['dependencies'] == deps()
    assert len(catalog['results']) == 24 and all(r['passed'] for r in catalog['results'])
    assert len(drag['results']) == 6 and all(r['passed'] for r in drag['results'])
    sources = {}

    def rows(path):
        if path not in sources:
            sources[path] = load(path)
        value = sources[path]
        return value['results']

    def ref(path, index):
        row = rows(path)[index]
        assert row['passed'] and not row.get('errors', []), (path, index)
        return dict(report=path.relative_to(ROOT).as_posix(), row=index, sha256=sha(path))

    def standalone(path):
        row = load(path)
        assert row['passed'] and not row.get('errors', [])
        return dict(report=path.relative_to(ROOT).as_posix(), row=None, sha256=sha(path))

    observations = []
    for observation in lifecycle['inventory']:
        i = observation['candidate_index']
        observations.append(dict(id='initial-' + str(i), page=observation['page'], selector=observation['selector'], trigger=observation['label'],
            title=observation['overlays'][0]['title'], controls=observation['overlays'][0]['controls'],
            lifecycle_evidence=[ref(lifecycle_path, n) for n, r in enumerate(lifecycle['results']) if r['candidate_index'] == i]))
    for observation in catalog['observations']:
        i = observation['historical_observation_index']
        observations.append(dict(id='catalog-' + str(i), page=observation['page'], selector=observation['selector'], trigger=observation['label'],
            title=observation['overlays'][0]['title'], controls=observation['overlays'][0]['controls'],
            lifecycle_evidence=[ref(catalog_path, n) for n, r in enumerate(catalog['results']) if r['historical_observation_index'] == i]
                               + [ref(drag_path, n) for n, r in enumerate(drag['results']) if r['historical_observation_index'] == i]))
    assert len(observations) == 110
    by_id = {o['id']: o for o in observations}
    items = [dict(observation=o['id'], control_index=j, page=o['page'], title=o['title'], trigger=o['trigger'],
                  control=c, lifecycle_evidence=o['lifecycle_evidence'], business_evidence=[], mapping_kind=None)
             for o in observations for j, c in enumerate(o['controls'])]
    assert len(items) == 302

    targets = {
        'hidden-choice-outcomes/results.json': RAW / 'verify_hidden_choice_outcomes/results.json',
        'hidden-auxiliary-outcomes/results.json': RAW / 'verify_hidden_auxiliary_outcomes/results.json',
        'hidden-workshop-outcomes/results.json': RAW / 'verify_hidden_workshop_outcomes/results.json',
        'hidden-settings-pet-outcomes/results.json': RAW / 'verify_hidden_settings_pet_outcomes/results.json',
        'overlay-form-save-results.json': FINAL / 'verify_overlay_form_saves/overlay-form-save-results.json',
        'confirmed-deletion-results.json': FINAL / 'verify_confirmed_deletions/confirmed-deletion-results.json',
        'identity-deletion-results.json': FINAL / 'verify_identity_deletions/identity-deletion-results.json',
    }
    identity_keys = ['observation_index', 'original_suite_case_id', 'mode', 'kind', 'control_label', 'case']

    def current_ref(old_path, old_index, target):
        old_row = load(old_path)['results'][old_index]
        identity = {k: old_row[k] for k in identity_keys if k in old_row}
        assert identity
        matches = [i for i, row in enumerate(rows(target)) if all(row.get(k) == v for k, v in identity.items())]
        assert len(matches) == 1, (old_path, identity, target)
        return ref(target, matches[0])

    prior_path = ROOT / 'evidence/current/hidden-behavior-crosswalk.json'
    prior = load(prior_path)
    inputs = load(RAW / 'inputs/current-observations.json')
    for prior_index, old in enumerate(prior['rows']):
        if old['page'].startswith('m08'):
            continue
        observation = inputs['results'][old['observation_index']]
        key = ('initial-' + str(observation['lifecycle_candidate_index']) if 'lifecycle_candidate_index' in observation
               else 'catalog-' + str(old['observation_index']))
        matches = [v for v in items if v['observation'] == key and all(v['control'].get(k) == old[k] for k in ['label', 'tag', 'type'])]
        assert len(matches) == 1, (key, old['label'], old['tag'], old['type'])
        item = matches[0]
        assert item['mapping_kind'] is None
        item.update(mapping_kind='current-literal-business-case', business_contract=old['business_contract'],
                    predecessor=dict(path=prior_path.relative_to(ROOT).as_posix(), sha256=sha(prior_path), row=prior_index, role='semantic correspondence only'))
        for evidence in old['evidence']:
            if evidence['report'] == 'overlay-exit-path-results.json':
                item['business_evidence'].extend(item['lifecycle_evidence'])
                item['mapping_kind'] = 'current-safe-close'
            else:
                target = targets[evidence['report']]
                item['business_evidence'].append(current_ref(ROOT / 'evidence/current' / evidence['report'], evidence['result_index'], target))
    book_prior_path = ROOT / 'evidence/current/book-v2-hidden/crosswalk.json'
    book_prior = load(book_prior_path)
    book_observations = load(ROOT / 'evidence/current/book-v2-hidden/inventory.json')['results']
    book_targets = {
        'book-v2-hidden-reading': RAW / 'verify_book_v2_hidden_reading/results.json',
        'book-v2-hidden-structure': RAW / 'verify_book_v2_hidden_structure/results.json',
        'book-v2-hidden-editors': FINAL / 'verify_book_v2_hidden_editors/results.json',
        'book-v2-hidden-forms': RAW / 'verify_book_v2_hidden_forms/results.json',
        'book-v2-hidden-edges': RAW / 'verify_book_v2_hidden_edges/results.json',
    }
    for prior_index, old in enumerate(book_prior['items']):
        previous = book_observations[old['observation']]
        matches = [o for o in observations if o['page'] == previous['page'] and o['trigger'] == previous['trigger'] and o['title'] == previous['expected_title']]
        assert len(matches) == 1
        observation = matches[0]
        candidates = [v for v in items if v['observation'] == observation['id'] and v['control_index'] == old['control_index'] and v['control']['label'] == old['control_label']]
        assert len(candidates) == 1
        item = candidates[0]
        assert item['mapping_kind'] is None
        item.update(mapping_kind=old['mapping_kind'], predecessor=dict(path=book_prior_path.relative_to(ROOT).as_posix(), sha256=sha(book_prior_path), row=prior_index, role='semantic correspondence only'))
        n = int(item['page'][-2:])
        label = item['control']['label']
        if old['mapping_kind'] == 'literal-cancel-button':
            contract = '取消／返回阅读：关闭弹层，保持底层页面和原存储，焦点回到触发器；有修改时先经过继续编辑／放弃保护。'
        elif n == 1:
            contract = '切换已成册／草稿／归档分类，不写入业务数据。' if label in ['已成册', '草稿', '归档'] else '打开选中的回忆册；章节、书页与原始素材保持，阅读位置按所选册恢复。'
        elif n in [5, 9, 10, 11, 12]:
            contract = ('编辑书页寄语；确认后更新父页候选，父页明确保存才落库。' if item['title'] == '一句话' else
                        '选择共同素材、替换／裁剪／移除照片或添加贴纸；只改变当前编辑候选，父页明确保存才落库，其他书页及原始素材保持。')
        elif n == 13:
            contract = '编辑章节／书页候选：新增、改名、移动、删除与边界反馈；重要删除经过确认，父页明确保存才落库，同时清理受影响页序／书签／锚点。'
        elif n == 16 and item['title'] == '共同回忆照片':
            contract = '调整照片预览缩放；返回阅读关闭预览，不改变书页照片或其他业务存储。'
        elif n == 16 and item['title'] == '回忆册目录':
            contract = '切换章节／缩略图／书签视图，或定位选中的实际书页；定位时更新阅读锚点，不更改原始内容。'
        elif n in [16, 17]:
            contract = '阅读工具操作：切换阅读模式／字号，或进入整理书页、封面主题、管理页面、返回书架；具名用例核对实际落点、阅读位置及往返上下文。'
        elif n == 21 and item['title'] == '书名':
            contract = '编辑书名，空值校验、继续编辑／放弃保持及明确保存后持久化；只改变目标册名称。'
        else:
            contract = '删除当前回忆册前明确确认；只删除目标册，其他册及原始素材保持，回到相应书架。'
        item['business_contract'] = contract
        for evidence in old['evidence']:
            old_path = ROOT / evidence['report']
            if old_path.parent.name == 'book-v2-overlay-cancel':
                item['business_evidence'].extend(item['lifecycle_evidence'])
            else:
                item['business_evidence'].append(current_ref(old_path, evidence['row'], book_targets[old_path.parent.name]))
    # These five actual pickers are new relative to the old hidden crosswalk.
    picker_path = PICKERS / 'picker-results.json'
    for key in ['initial-10', 'initial-15', 'initial-17', 'initial-20', 'initial-32']:
        observation = by_id[key]
        matched = [i for i, row in enumerate(rows(picker_path)) if row['page'] == observation['page'] and row['title'] == observation['title']]
        assert len(matched) == 5 and {rows(picker_path)[i]['width'] for i in matched} == {320, 360, 390, 414, 430}
        for item in [v for v in items if v['observation'] == key]:
            assert item['mapping_kind'] is None
            item['mapping_kind'] = 'current-picker-field-apply-cancel'
            item['business_contract'] = '实际选择及取消；应用更新父页候选值，取消保持原值；显式保存前不写入业务存储。字段关联、错误清理及五宽度观察另有对应结果。'
            item['business_evidence'] = [ref(picker_path, i) for i in matched]
            if item['control']['label'] == '不填写生日':
                item['mapping_kind'] = 'current-birthday-clear-save-retry'
                item['business_contract'] = '清空父页生日候选；保存失败保留候选和原存储；重试后清空生日持久化，重新打开仍为空，其他资料及存储保持。'
                item['business_evidence'] = [standalone(PICKERS / 'birthday-clear.json')]
    missing = [v for v in items if not v['business_evidence'] or v['mapping_kind'] is None]
    assert not missing, missing
    for item in items:
        # Repeated predicates may be shared by two fields; preserve references
        # once and retain explicit variant labels rather than counting as clicks.
        item['business_evidence'] = list({(v['report'], v['row']): v for v in item['business_evidence']}.values())
    index = dict(dependencies=deps(), business_summary_sha256=sha(FINAL / 'results.json'), picker_execution_sha256=sha(PICKERS / 'execution.json'),
                 lifecycle_sha256=sha(lifecycle_path), catalog_overlays_sha256=sha(catalog_path), catalog_drag_sha256=sha(drag_path), producer_sha256=sha(Path(__file__)),
                 observed_overlays=110, observed_controls=302, enabled_controls=sum(not v['control']['disabled'] for v in items),
                 mapped_controls=len(items), missing_controls=0, mapping_kinds=dict(Counter(v['mapping_kind'] for v in items)),
                 scope='Current observed 104 explicit manual entries plus six catalog dialogs. Every observed control is mapped to actual fresh consumer/lifecycle results; shared book fixture variants remain explicit. This is not 302 fresh business clicks, all conditional combinations or complete visual acceptance.',
                 observations=observations, items=items, human_accepted_pages=0)
    dump(FINAL / 'control-business-index.json', index)
    print(json.dumps({k: v for k, v in index.items() if k not in ['dependencies', 'observations', 'items']}))


if __name__ == '__main__':
    main()
