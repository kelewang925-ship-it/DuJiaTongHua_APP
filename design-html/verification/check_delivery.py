"""Check that the final evidence covers the current 114 HTML files."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
result=json.loads((ROOT/'ui-audit/full-suite-results.json').read_text(encoding='utf-8'))
assert len(manifest)==114 and len({x['id'] for x in manifest})==114
assert len({x['module_number'] for x in manifest})==8
assert result['pages']==114 and result['width_checks']==570
assert all(x['preview_matches_source'] and x['foundation'] and x['viewport_fit']
           and not x['missing_assets'] and not x['missing_routes'] for x in result['static'])
assert {x['id'] for x in result['records']}=={x['id'] for x in manifest}
for record in result['records']:
    page=ROOT/'pages'/f"{record['id']}.html"
    assert record['html_sha256']==hashlib.sha256(page.read_bytes()).hexdigest(),record['id']
    assert page.read_bytes()==(ROOT/'custom'/page.name).read_bytes()
    assert set(record['widths'])=={'320','375','390','414','430'}
    for width,m in record['widths'].items():
        assert m['documentWidth']==int(width) and m['fontLoaded'],(record['id'],width)
        assert not any(m[k] for k in ['smallTargets','textOverflow','clippedTargets',
            'overlappingButtons','unnamedButtons','brokenImages','pageErrors']),(record['id'],width,m)
        if width=='320':assert m['safeArea'],record['id']
for item in manifest:
    id=item['id']
    source=ROOT/'assets'/f'{id}-source.webp'
    assert Image.open(source).size==(item['width'],item['height']),id
    for path in [ROOT/'ui-audit/evidence/before'/f'{id}.webp',
                 ROOT/'ui-audit/evidence/after'/f'{id}.webp',
                 ROOT/'ui-audit/evidence/after'/f'{id}-320.png']:
        assert path.exists() and path.stat().st_size>0,path
        with Image.open(path) as image:assert abs(image.width/image.height-item['width']/item['height'])<.005,path
tests=sorted((ROOT/'ui-audit').glob('*interaction-results.json'))
assert len(tests)==8
groups=sum(len(json.loads(p.read_text(encoding='utf-8'))) for p in tests)
assert groups==66,groups
print('Delivery evidence passed: 114 current HTML hashes, 570 width checks, 114 safe areas, 342 screenshots and 66 interaction result groups')
