"""Scope the editable sketch patch independently from pending V2 integration."""
import importlib.util,json
from pathlib import Path
from verify_book_v2_reconciliation import ROOT,DEMO,dependencies,sha

def load(p):return json.loads(p.read_text(encoding='utf-8'))
def module(p,name):
    spec=importlib.util.spec_from_file_location(name,p);result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result
def main():
    baseline=ROOT/'evidence/baseline/book-template-previews';current=ROOT/'evidence/current/book-template-previews'
    red=load(baseline/'results.json');green=load(current/'results.json');files=dependencies()
    assert len(red['results'])==5 and not any(r['passed'] for r in red['results'])
    assert len(green['results'])==11 and all(r['passed'] for r in green['results'])
    assert green['dependency_files']==files
    assert green['producer_sha256']==sha(ROOT/'verify_book_template_previews.py')
    assert red['producer_sha256']==sha(baseline/'verifier.py')
    changed={p for p,h in red['dependency_files'].items() if files.get(p)!=h}
    assert changed=={'assets/prototype-book-v2.css','custom/m08-p08.html','pages/m08-p08.html'},changed
    assert files.keys()==red['dependency_files'].keys()
    style=(DEMO/'assets/prototype-book-v2.css').read_bytes();added=(baseline/'added-style.css').read_bytes()
    assert style.endswith(added) and style[:-len(added)]==(baseline/'style.css').read_bytes()
    old=module(baseline/'generator.py','old_book_generator');new=module(ROOT/'build_book_v2.py','current_book_generator')
    assert old.SCRIPTS==new.SCRIPTS
    assert all(old.content[n]==new.content[n] for n in range(1,22) if n!=8)
    for folder in ['custom','pages']:
        html=(DEMO/f'{folder}/m08-p08.html').read_bytes();chunk=new.content[8][1].encode()
        assert html.count(chunk)==1
        assert html.replace(chunk,old.content[8][1].encode(),1)==(baseline/f'source-{folder}.html').read_bytes()
    assert (DEMO/'custom/m08-p08.html').read_bytes()==(DEMO/'pages/m08-p08.html').read_bytes()
    inventory=load(ROOT/'evidence/current/book-v2-controls/inventory.json')
    assert len(inventory['results'])==21 and all(r['passed'] for r in inventory['results']) and inventory['dependency_files']==files
    actionable=[dict(page=r['page'],**c) for r in inventory['results'] for c in r['controls'] if c['visible'] and not c['disabled'] and not c['blocked_by_modal']]
    report=dict(passed=True,scope='Template sketches and unchanged six destinations only; inventory is observation, not full interaction verification.',dependency_files=files,changed_sources=sorted(changed),browser_cases=11,observed_book_pages=21,observed_actionable_controls=len(actionable),source_reversal=True,other20_generator_contents_preserved=True,human_accepted_pages=0,producer_sha256=sha(Path(__file__)))
    (current/'checkpoint.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS exact CSS/HTML reversal, other20 generator contents, 11 sketch/route cases, current21-page inventory;',len(actionable),'observed actionable controls')

if __name__=='__main__':main()
