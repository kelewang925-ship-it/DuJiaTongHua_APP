"""Bounded literal Modal call inventory, distinct from executable interaction evidence."""
import re,json
from verify_pet_controls import ROOT,DEMO,source
files=source();rows=[]
for p in(DEMO/'assets').glob('prototype-*.js'):
 s=p.read_text(encoding='utf-8')
 for m in re.finditer(r'(?:(?:UI|PrototypeUI)\.modal|(?<![\w.])modal)\(\{',s):
  start=m.end()-1;i=start;depth=0;quote=None;escape=False
  while i<len(s):
   ch=s[i]
   if quote:
    if escape:escape=False
    elif ch=='\\':escape=True
    elif ch==quote:quote=None
   elif ch in "'\"`":quote=ch
   elif ch=='{':depth+=1
   elif ch=='}':
    depth-=1
    if not depth:break
   i+=1
  body=s[start:i+1];title=re.search(r'title\s*:\s*([^,\n]+)',body);confirm=re.search(r'confirm\s*:\s*([^,\n}]+)',body)
  if not title:continue # Function signature and sheet forwarding are not product callsites.
  rows.append(dict(file=p.name,line=s.count('\n',0,m.start())+1,title=title.group(1),confirm=confirm.group(1)if confirm else'default/choices',danger=bool(re.search(r'danger\s*:\s*true',body)),choices='actions:'in body))
assert files==source();(ROOT/'evidence/current/danger-modal-callsite-inventory.json').write_text(json.dumps(dict(files=files,scope='Literal Modal calls only; excludes Sheet choices/forms and is not executed coverage',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Literal Modal calls:',len(rows),'explicit destructive final:',sum(r['danger']for r in rows))
