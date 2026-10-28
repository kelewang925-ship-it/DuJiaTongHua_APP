"""Run existing book contracts without overwriting their historical evidence."""
from pathlib import Path
import ast, sys

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'evidence/current/book-v2/regressions';OUT.mkdir(parents=True,exist_ok=True)
ALLOWED={'flow','states','extended','structure','editor_draft','global','image_variants'}
name=sys.argv[1]
if name not in ALLOWED:raise SystemExit('unknown suite')
source=ROOT/f'verify_book_{name}.py'
class EvidenceLocation(ast.NodeTransformer):
 def visit_Assign(self,node):
  if any(isinstance(t,ast.Name) and t.id=='OUT' for t in node.targets):
   node.value=ast.Call(func=ast.Name(id='Path',ctx=ast.Load()),args=[ast.Constant(str(OUT))],keywords=[])
  return self.generic_visit(node)
tree=EvidenceLocation().visit(ast.parse(source.read_text(encoding='utf-8')));ast.fix_missing_locations(tree)
sys.argv=[str(source)]
exec(compile(tree,str(source),'exec'),{'__name__':'__main__','__file__':str(source)})
