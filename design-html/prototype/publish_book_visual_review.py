"""Add the twenty remaining original comparisons without changing acceptance."""
import json
from pathlib import Path
from datetime import datetime,timezone
from verify_book_v2_reconciliation import ROOT,DEMO,sha

def load(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    queue_path=ROOT/'queue.json';review_path=ROOT/'evidence/current/visual-self-review/results.json'
    q=load(queue_path);review=load(review_path);old={r['page_id'] for r in review['results']}
    assert len(old)==94 and len(q)==114
    prior=ROOT/'evidence/current/book-visual-review/prior-94-results.json';assert not prior.exists();prior.write_bytes(review_path.read_bytes())
    captures=load(ROOT/'evidence/current/book-visual-review/captures.json');assert len(captures['results'])==21 and all(r['passed'] for r in captures['results'])
    notes=load(ROOT/'book_visual_observations.json');assert len(notes)==21
    added=[];observed=datetime.now(timezone.utc).isoformat()
    for capture in captures['results']:
        identity=capture['page'];item=next(p for p in q if p['id']==identity)
        assert sha(ROOT/capture['legacy_screenshot'])==capture['legacy_screenshot_sha256']
        assert sha(ROOT/capture['current_screenshot'])==capture['current_screenshot_sha256']
        # These screenshots predate the documented default-selection patch.
        # Their recorded source fingerprint remains unchanged.
        if identity in old:continue
        findings=['P2-VIS-TYPE']
        if identity in ['m08-p03','m08-p06','m08-p13','m08-p15']:findings.append('P2-VIS-RECORD-SKIN')
        if identity=='m08-p08':findings+=['P2-VIS-BOOK-CHOICE','P2-VIS-BOOK-TEMPLATE-PREVIEW']
        if identity=='m08-p19':findings.append('P2-VIS-CONTROL-SKIN')
        row=dict(page_id=identity,reviewed_at=observed,reviewer='Codex（图像对照自检，非人工验收）',original_design_reference=capture['original_design_reference'],original_export=capture['original_export'],original_export_sha256=capture['original_export_sha256'],screenshot=capture['legacy_screenshot'],screenshot_sha256=capture['legacy_screenshot_sha256'],finding_ids=findings,observation=notes[identity],detail='BOOK_VISUAL_REVIEW.md',human_reviewer=None,accepted=False,current_version_comparison=dict(screenshot=capture['current_screenshot'],sha256=capture['current_screenshot_sha256'],capture_report='evidence/current/book-visual-review/captures.json',note='V2 layout differs from original; comparison is not a fidelity approval. Capture predates default-choice repair.'))
        item['visual_self_review']=row
        for finding in findings:
            if not any(x.get('id')==finding for x in item['issues']):item['issues'].append(dict(id=finding,reference='BOOK_VISUAL_REVIEW.md',status='observed-open-visual-difference'))
        added.append(row)
    assert len(added)==20
    review['results']+=added;review.update(reviewed_pages=114,remaining_self_review=0)
    assert len({x['page_id'] for x in review['results']})==114
    assert review['results'][:94]==load(prior)['results']
    write(review_path,review);write(queue_path,q)
    state_path=ROOT/'evidence/current/current-evidence-state.json';state=load(state_path)
    state['current_visual_self_review_pages']=114
    state['book_visual_review']=dict(report='evidence/current/book-visual-review/captures.json',observations='book_visual_observations.json',scope='20 new original/legacy comparisons and 21 V2 captures; self-review only, human acceptance remains0; existing full-source evidence requires V2 reconciliation.')
    write(state_path,state)
    print('Published 20 new reviews; 114 unique pages; prior94 observations and all acceptance states retained.')

if __name__=='__main__':main()
