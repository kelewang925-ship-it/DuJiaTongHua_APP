"""Use actual manual/auto operations to verify shared scope exclusions."""
import runpy,json,sys
from verify_pet_controls import ROOT,source
runpy.run_path(str(ROOT/'audit_backup_scope.py'))
v=json.loads((ROOT/'evidence/current/backup-scope-observations.json').read_text(encoding='utf-8'));assert v['files']==source();rows=[]
for row in v['results']:
 rows.append(dict(case=row['mode']+'-shared-scope',passed=not row['private_moment_in_shared_backup']and not row['draft_moment_in_shared_backup']and not row['private_anniversary_in_shared_backup']and not row['private_capsule_in_shared_backup']and row['accessible_content_retained']and not row['errors'],errors=row['errors']))
out=ROOT/'evidence'/('baseline'if '--baseline'in sys.argv else'current');out.mkdir(parents=True,exist_ok=True);(out/'backup-scope-results.json').write_text(json.dumps(dict(files=v['files'],results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(rows)
raise SystemExit(0 if all(r['passed']for r in rows)else 1)
