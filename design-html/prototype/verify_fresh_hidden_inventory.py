"""Bind refreshed direct-trigger hidden observations without accepting later actions."""
import argparse,json,hashlib
from verify_pet_controls import ROOT,source

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--session',type=int,required=True);parser.add_argument('--exit-code',type=int,required=True);args=parser.parse_args();assert args.exit_code==0
    files=source();out=ROOT/'evidence/current';report_path=out/'hidden-overlay-observations.json';report=json.loads(report_path.read_text(encoding='utf-8'));index_path=out/'hidden-overlay-index.json';index=json.loads(index_path.read_text(encoding='utf-8'));h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    assert report['files']==index['files']==files and report['candidates']==report['completed']==len(report['results'])==133
    assert all(r['passed']and not r['errors']for r in report['results']);opened=[r for r in report['results']if r['overlays']];assert len(opened)==99 and all(r['escape_preserved_storage']and r['focus_returned']for r in opened)
    assert len(index['pages'])==114 and len(index['hidden_controls'])==250 and index['report_sha256']==h(report_path)
    dependency=ROOT/'evidence/history/pre-hidden-refresh-a75e9e0/probe-source-page-contracts.json';assert h(dependency)==report['catalog_sha256'];assert json.loads(dependency.read_text(encoding='utf-8'))['files']==files
    for name,digest in report['fixture_scripts'].items():assert h(ROOT/name)==digest,name
    checkpoint=dict(files=files,execution=dict(session_id=args.session,exit_code=args.exit_code),observations=133,opened=99,hidden_controls=250,pages=114,report_sha256=h(report_path),index_sha256=h(index_path),probe_catalog_path=dependency.relative_to(ROOT).as_posix(),probe_catalog_sha256=h(dependency),script_sha256={name:h(ROOT/name)for name in ['audit_hidden_overlays.py','build_hidden_overlay_index.py','verify_fresh_hidden_inventory.py']},accepted_pages=0,scope='Direct trigger observations and clean Escape storage/focus preservation only. Action results/nested/dirty/submitting/source/layout remain separate gates.')
    (out/'fresh-hidden-inventory-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(pages=114,candidates=133,opened=99,hidden_controls=250,accepted_pages=0)))

if __name__=='__main__':main()
