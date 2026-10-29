"""Verify local source lineage, current results and the exact presentation-only hooks."""
import json,subprocess
from pathlib import Path
from verify_record_presentation import ROOT,DEMO,PAGES,dependencies,sha

def main():
    baseline=ROOT/'evidence/baseline/record-presentation'
    current=ROOT/'evidence/current/record-presentation'
    changes={
        'assets/prototype-home.js':[(b'button.append(title,meta);section.append(button);',b"button.append(title,meta);window.PrototypeRecordPresentation?.decorate(button,item,'home');section.append(button);"),(b'button.append(title,excerpt,meta);list.append(button);',b"button.append(title,excerpt,meta);window.PrototypeRecordPresentation?.decorate(button,item,'search');list.append(button);")],
        'assets/prototype-diary.js':[(b'button.append(title,body,meta);list.append(button);',b"button.append(title,body,meta);window.PrototypeRecordPresentation?.decorate(button,item,'diary');list.append(button);")],
        'assets/prototype-photo.js':[(b'button.append(img,title);grid.append(button);',b"button.append(img,title);window.PrototypeRecordPresentation?.decorate(button,item,'album');grid.append(button);")]
    }
    for page,controller in [('m03-p02','home'),('m03-p04','home'),('m03-p06','diary'),('m03-p10','photo')]:
        for folder in ['custom','pages']:
            changes[f'{folder}/{page}.html']=[(b'',b'<link rel="stylesheet" href="../assets/prototype-record-presentation.css">'),(b'',b'<script src="../assets/prototype-record-presentation.js"></script>')]
        assert (DEMO/f'custom/{page}.html').read_bytes()==(DEMO/f'pages/{page}.html').read_bytes()
    for name,replacements in changes.items():
        raw=(DEMO/name).read_bytes()
        for old,new in replacements:assert raw.count(new)==1;raw=raw.replace(new,old,1)
        assert raw==(baseline/'source'/name).read_bytes(),name
    consumers=sorted(p.stem for p in (DEMO/'custom').glob('*.html') if 'prototype-record-presentation.js' in p.read_text(encoding='utf-8'))
    assert consumers==sorted(PAGES)
    green=json.loads((current/'results.json').read_text(encoding='utf-8'))
    assert green['dependency_files']==dependencies()
    assert green['producer_sha256']==sha(ROOT/'verify_record_presentation.py')
    assert green['fixture_sha256']==sha(ROOT/'verify_record_controls.py')
    assert len(green['results'])==71 and all(r['passed'] for r in green['results'])
    counts={kind:sum(r['kind']==kind for r in green['results']) for kind in {r['kind'] for r in green['results']}}
    assert counts=={'visual':20,'control':36,'extra':2,'hidden':2,'load-error':3,'image-error':4,'privacy':4}
    overflow=json.loads((ROOT/'evidence/current/record-collection-overflow/results.json').read_text(encoding='utf-8'))
    assert overflow['dependency_files']==dependencies() and len(overflow['results'])==10 and all(r['passed'] for r in overflow['results'])
    assert overflow['producer_sha256']==sha(ROOT/'verify_record_collection_overflow.py') and overflow['fixture_sha256']==sha(ROOT/'verify_record_controls.py')
    folders=[('record-presentation',20,0),('record-presentation-first-pass',71,45),('record-presentation-before-album-bounds',71,71),('record-presentation-album-bounds',5,0),('record-presentation-before-mask-specificity',71,66)]
    archived_sources=list((ROOT/'evidence/baseline').glob('record-presentation*/source'))
    for name,count,passed in folders:
        folder=ROOT/'evidence/baseline'/name;report=json.loads((folder/'results.json').read_text(encoding='utf-8'))
        assert len(report['results'])==count and sum(r['passed'] for r in report['results'])==passed
        assert report['producer_sha256']==sha(folder/'producer.py')
        for source,digest in report['dependency_files'].items():
            candidates=[DEMO/source]+[archive/source for archive in archived_sources]
            assert any(p.is_file() and sha(p)==digest for p in candidates),(name,source)
    for name in ['prototype-home.js','prototype-diary.js','prototype-photo.js','prototype-record-presentation.js']:
        subprocess.run([r'C:\Users\kele\.nvmd\bin\node.exe','--check',str(DEMO/'assets'/name)],check=True)
    result={'passed':True,'dependency_files':dependencies(),'exact_original_html_and_controller_reversal':True,'consumers':consumers,'current_cases':counts,'overflow_cases':10,'total':81,'human_accepted_pages':0,'scope':'Four record collections only. Paper ornament fidelity, grouping, typography and other module lists remain open. Original data/storage/route/filter/error handlers preserved byte-for-byte after removing four calls.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS81 browser cases,11 exact source reversals,4 mirrored consumers,archived red/green lineage and4 JavaScript syntax checks')

if __name__=='__main__':main()
