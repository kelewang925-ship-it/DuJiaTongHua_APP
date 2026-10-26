"""Enrich the existing114-page queue; never infer human approval from automated evidence."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--design-root', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'queue.json'
    original = json.loads(path.read_text(encoding='utf-8'))
    queue = json.loads(json.dumps(original))
    manifest = {r['id']: r for r in json.loads((ROOT.parent / 'manifest.json').read_text(encoding='utf-8'))}
    assert len(queue) == len(manifest) == 114
    assert {q['id'] for q in queue} == set(manifest)
    now = datetime.now(timezone.utc).isoformat()
    for row in queue:
        identity = row['id']
        entry = manifest[identity]
        design = args.design_root / entry['source'].replace('\\', '/')
        export = ROOT.parent / 'assets' / (identity + '-source.webp')
        html = ROOT.parent / 'custom' / (identity + '.html')
        public = ROOT.parent / 'pages' / (identity + '.html')
        assert all(p.is_file() for p in [design, export, html, public]), identity
        # Repository-relative export is portable; original PNG belongs to the
        # separate project-docs workspace and must not masquerade as a repo file.
        additions = dict(
            design_path=export.relative_to(REPO).as_posix(),
            original_design_reference=dict(
                workspace='DuJiaTongHua_Project_Docs', base='新模块分布',
                path=entry['source'].replace('\\', '/'),
                sha256=hashlib.sha256(design.read_bytes()).hexdigest()),
            html_path=html.relative_to(REPO).as_posix(),
            preview_path=public.relative_to(REPO).as_posix(),
            development_status='进行中', interaction_status='进行中', visual_status='待验收',
            golden_page='待核实',
            issues=[dict(reference='ACCEPTANCE_REQUIREMENTS.md',
                         summary='完整流程及适用动态条件仍在验证，现有局部证据不等于整页终验'),
                    dict(reference='../../docs/html-development-standards.md',
                         summary='人工视觉对照、验收责任人及黄金名单待核实')],
            last_verification=dict(
                verified_at=now, verifier='Codex（本次仅核对路径与证据索引）',
                verification_kind='metadata-and-paths', viewport_css_px=None,
                browser_and_dpr=None, screenshot_path=None,
                console_or_check_log='update_acceptance_metadata.py --design-root <项目设计稿目录>',
                interaction_cases=[], visual_differences=[],
                result='114页路径齐全；交互及人工视觉验收状态未提升',
                human_reviewer=None, human_reviewed_at=None),
            automated_evidence=dict(
                initial_controls='evidence/current/current-initial-replay/checkpoint.json',
                initial_quality='evidence/current/initial-quality/checkpoint.json',
                source_note='各报告保留真实执行时源码指纹；后续单函数相册修复另见album-timeout/checkpoint.json，不能将历史报告视作全量新跑'))
        for key, value in additions.items():
            row.setdefault(key, value)
    # Existing implementation, behavior evidence and approval fields survive.
    assert all(all(new[k] == value for k, value in old.items()) for old, new in zip(original, queue))
    report = dict(pages=len(queue), original_pngs=114, source_exports=114, html=114,
                  new_fields=sorted(set(queue[0]) - set(original[0])),
                  human_approval_inferred=False, writes='queue.json only' if args.apply else 'preview only')
    print(json.dumps(report, ensure_ascii=False))
    if args.apply:
        path.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
