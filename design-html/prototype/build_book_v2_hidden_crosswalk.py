"""Bind observed V2 hidden controls to explicit current outcomes and fixture variants."""
import json
from pathlib import Path
from datetime import datetime,timezone
from verify_book_v2_reconciliation import ROOT,dependencies,sha

SUITES={'reading':('book-v2-hidden-reading','verify_book_v2_hidden_reading.py',22),'structure':('book-v2-hidden-structure','verify_book_v2_hidden_structure.py',13),'editors':('book-v2-hidden-editors','verify_book_v2_hidden_editors.py',18),'forms':('book-v2-hidden-forms','verify_book_v2_hidden_forms.py',6),'edges':('book-v2-hidden-edges','verify_book_v2_hidden_edges.py',3),'cancel':('book-v2-overlay-cancel','verify_book_v2_overlay_cancel.py',31)}
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    files=dependencies();assert files==load(ROOT/'evidence/current/book-v2-controls/checkpoint.json')['dependency_files']
    inventory_path=ROOT/'evidence/current/book-v2-hidden/inventory.json';inventory=load(inventory_path);assert inventory['dependency_files']==files and len(inventory['results'])==31 and all(r['passed'] for r in inventory['results'])
    assert inventory['producer_sha256']==sha(ROOT/'audit_book_v2_hidden_controls.py')
    assert inventory['fixture_sha256']==sha(ROOT/'verify_book_controls.py') and inventory['snapshot_producer_sha256']==sha(ROOT/'audit_hidden_overlays.py')
    assert inventory['initial_report_sha256']==sha(ROOT/'evidence/current/book-v2-controls/results.json')
    reports={};paths={}
    for key,(folder,script,count) in SUITES.items():
        path=ROOT/f'evidence/current/{folder}/results.json';report=load(path)
        assert report['dependency_files']==files and report['producer_sha256']==sha(ROOT/script)
        assert len(report['results'])==count and all(r['passed'] for r in report['results']),key
        reports[key]=report;paths[key]=path
    reading=reports['reading'];assert reading['helpers_sha256']==sha(ROOT/'book_test_helpers.py')
    assert all(sha(ROOT/name)==digest for name,digest in reading['fixtures_sha256'].items())
    for key in ['editors','forms','edges','cancel']:assert reports[key]['fixture_sha256']==sha(ROOT/'verify_book_controls.py')
    assert reports['edges']['helpers_sha256']==sha(ROOT/'book_test_helpers.py')
    assert reports['editors']['original_contract_suite_sha256']==sha(ROOT/'verify_hidden_book_editor_outcomes.py')
    assert reports['editors']['current_inventory_sha256']==reports['cancel']['inventory_sha256']==sha(inventory_path)
    structure=reports['structure'];parent=ROOT/'evidence/current/book-v2-hidden-structure/before-locator-correction/results.json';old=load(parent)
    assert structure['prior_report_sha256']==sha(parent) and structure['retained_executions']==12 and structure['new_executions']==1
    assert old['producer_sha256']==sha(parent.parent/'verify_book_v2_hidden_structure.py')
    previous={r['case']:r for r in old['results']}
    for row in structure['results']:
        if row.get('retained_from'):assert previous[row['case']]=={k:v for k,v in row.items() if k!='retained_from'}
    def ref(suite,case=None,**criteria):
        matches=[(i,r) for i,r in enumerate(reports[suite]['results']) if (case is None or r.get('case')==case) and all(r.get(k)==v for k,v in criteria.items())];assert len(matches)==1,(suite,case,criteria)
        i,row=matches[0];return dict(report=paths[suite].relative_to(ROOT).as_posix(),row=i,case=row.get('case',row.get('control_label')),sha256=sha(paths[suite]))
    def editor(index,label):return [ref('editors',original_suite_case_id=index,control_label=label)]
    items=[]
    for observation_index,obs in enumerate(inventory['results']):
        n=int(obs['page'][-2:]);trigger=obs['trigger']
        for control_index,control in enumerate(obs['overlays'][0]['controls']):
            if not control['visible'] or control['disabled']:continue
            label=control['label'];kind='literal-business-path';evidence=[]
            if label in ['取消','继续编辑','返回阅读']:
                evidence=[ref('cancel',page=obs['page'],trigger=trigger,control_label=label)];kind='literal-cancel-button'
            elif n==1:
                evidence=[ref('reading','library-tabs' if label in ['已成册','草稿','归档'] else 'library-open-published')];kind='shared-library-path-with-explicit-book-variant'
            elif n==5:evidence=editor(101,label)
            elif n==9:evidence=editor(108 if trigger=='更换摘录' else 109,label)
            elif n==10:
                index={'照片 1 · 裁剪或替换':111,'照片 2 · 裁剪或替换':112,'照片 3 · 裁剪或替换':113,'添加照片':114,'添加贴纸':115}[trigger];evidence=editor(index,label)
            elif n==11:
                if trigger=='添加一句话':evidence=[ref('forms','quote-validation-parent-save'),ref('forms','quote-cancel')]
                else:evidence=editor(117 if trigger=='选择重要时刻' else 116,label)
            elif n==12:evidence=editor({'工坊作品':119,'换内容':120,'换照片':121}[trigger],label)
            elif n==13:
                if trigger=='新增章节':evidence=[ref('structure','chapter-add-validation-save')]
                elif trigger.startswith('章节操作'):
                    kind='shared-chapter-path-with-explicit-order-boundary-variants'
                    if label=='修改章节名':evidence=[ref('structure','chapter-rename-save'),ref('structure','chapter-rename-cancel')]
                    elif label in ['上移章节','下移章节']:evidence=[ref('structure','chapter-up-save' if label=='上移章节' else 'chapter-down-save'),ref('structure','chapter-boundary-feedback')]
                    elif label=='删除章节':evidence=[ref('forms','delete-chapter-with-pages'),ref('structure','chapter-move-delete-cancel-failure-retry'),ref('edges','delete-last-chapter-empty-cta')]
                else:
                    kind='shared-page-path-with-explicit-arrangement-variants'
                    if label=='上移一页':evidence=[ref('structure','page-order-delete-bookmark-cleanup'),ref('structure','page-boundary-feedback')]
                    elif label=='下移一页':evidence=[ref('edges','page-down-save'),ref('structure','page-boundary-feedback')]
                    elif label=='移动到另一章':evidence=[ref('structure','chapter-move-delete-cancel-failure-retry'),ref('structure','page-target-cancel'),ref('edges','move-without-other-chapter-feedback')]
                    elif label=='删除书页':evidence=[ref('structure','page-order-delete-bookmark-cleanup')]
            elif n==16:
                if trigger=='阅读设置与工具':evidence=[ref('reading',{'大字连续阅读':'menu-mode-roundtrip','放大字号':'menu-type-roundtrip','整理书页':'menu-organize','封面与主题':'menu-cover','管理这本回忆册':'menu-manage','返回书架':'menu-shelf'}[label])]
                elif trigger=='放大照片':evidence=[ref('reading','zoom-controls-return'),ref('reading','zoom-privacy-refresh')]
                elif label in ['章节','缩略图','书签']:evidence=[ref('reading',{'章节':'directory-chapter-page','缩略图':'directory-thumbnail-page','书签':'directory-bookmarked-page'}[label])]
                else:evidence=[ref('reading','directory-chapter-page'),ref('reading','directory-bookmarked-page')];kind='shared-directory-item-path-with-explicit-page-variants'
            elif n==21:evidence=[ref('forms','rename-validation-save'),ref('forms','rename-cancel')] if trigger=='修改书名' else [ref('forms','delete-confirm-only-target-book')]
            assert evidence,(obs['page'],trigger,label)
            items.append(dict(observation=observation_index,control_index=control_index,page=obs['page'],trigger=trigger,control_label=label,selector=control['selector'],mapping_kind=kind,evidence=evidence))
    assert len(items)==106
    edges=[]
    def edge(origin,destination,label,suite,case):edges.append(dict(origin=origin,destination=destination,label=label,evidence=ref(suite,case)))
    for row in reports['reading']['results']:
        case=row['case']
        if case.startswith('library-open-'):
            destination=row['effective'].split('/pages/')[-1].split('.html')[0];edge('m08-p01',destination,{'library-open-published':'选择已成册','library-open-draft':'选择草稿','library-open-archive':'选择归档册'}[case],'reading',case)
        elif case.startswith('menu-'):
            destination=row['effective'].split('/pages/')[-1].split('.html')[0];edge('m08-p16',destination,case.replace('menu-',''),'reading',case)
        elif case in ['directory-chapter-page','directory-thumbnail-page','directory-bookmarked-page']:
            edge('m08-p16','m08-p16','目录定位：'+case.replace('directory-',''),'reading',case)
    for row in reports['editors']['results']:
        edges.append(dict(origin=row['page'],destination=row['destination'],label=row['trigger']+'／'+row['control_label']+'后保存',evidence=ref('editors',original_suite_case_id=row['original_suite_case_id'],control_label=row['control_label'])))
    for case,origin,destination,label in [('quote-validation-parent-save','m08-p11','m08-p13','寄语确认后保存书页'),('delete-confirm-only-target-book','m08-p21','m08-p01','确认删除目标册，其他册仍保留'),('delete-chapter-with-pages','m08-p13','m08-p14','删除非空章节后保存排列')]:edge(origin,destination,label,'forms',case)
    for origin,destination,label in [('m08-p13','m08-p14','删除最后章节后保存空册'),('m08-p14','m08-p15','打开空册目录'),('m08-p15','m08-p08','空目录添加书页CTA')]:edge(origin,destination,label,'edges','delete-last-chapter-empty-cta')
    diagram=['flowchart TD']
    for item in edges:diagram.append('  '+item['origin'].replace('-','_')+' -->|"'+item['label'].replace('"','').replace('|','/')+'"| '+item['destination'].replace('-','_'))
    (ROOT/'BOOK_V2_HIDDEN_NAVIGATION.mmd').write_text('\n'.join(diagram)+'\n',encoding='utf-8')
    old_crosswalk=ROOT/'evidence/current/hidden-behavior-crosswalk.json'
    report=dict(assembled_at=datetime.now(timezone.utc).isoformat(),scope='31 observed V2 overlays/106 enabled control occurrences, not106 new executions or arbitrary conditional-state coverage. Shared library/chapter/page/directory paths explicitly use named fixture variants.',dependency_files=files,inventory_sha256=sha(inventory_path),business_outcome_cases=62,literal_cancel_cases=31,escape_observations=31,retained_structure_cases=12,current_batch_product_source_changes=0,mapped_control_occurrences=106,unmapped_observed_controls=0,human_accepted_pages=0,original250_crosswalk_sha256=sha(old_crosswalk),producer_sha256=sha(Path(__file__)),suite_reports={key:dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path)) for key,path in paths.items()},items=items,remaining_scope=['Conditional controls not present in these initial overlay snapshots, including populated standalone p17 bookmarks and library state changes across windows.','Complete state/failure/return correspondence and final41-requirement audit.','Remaining visual issues and human acceptance.'])
    report['tested_navigation_edges']=edges;report['navigation_artifact']='BOOK_V2_HIDDEN_NAVIGATION.mmd'
    (ROOT/'evidence/current/book-v2-hidden/crosswalk.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS106 observed control occurrences mapped;62 business outcomes,31 literal cancel cases,31 Escape observations; no product-source changes or human acceptance claim')

if __name__=='__main__':main()
