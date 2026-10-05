"""Reject stale page/control evidence before joining it to current observations."""
from pathlib import Path
import hashlib,json

def current_source_fingerprint():
    root=Path(__file__).resolve().parent
    report=json.loads((root/'evidence/current/current-runtime-summary.json').read_text(encoding='utf-8'))
    for path,digest in report['files'].items():
        assert hashlib.sha256((root.parent/path).read_bytes()).hexdigest()==digest, 'Runtime observation is stale: '+path
    return hashlib.sha256(json.dumps(report['files'],sort_keys=True).encode()).hexdigest()
