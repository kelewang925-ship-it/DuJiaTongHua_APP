const fs=require('fs'),path=require('path'),crypto=require('crypto');
const acorn=require(process.argv[2]),root=process.cwd();
const hash=value=>crypto.createHash('sha256').update(value).digest('hex');
const base=path.join(root,'design-html/prototype/evidence/baseline/toast-feedback');
const before=fs.readFileSync(path.join(base,'prototype-ui.js'));
const after=fs.readFileSync(path.join(root,'design-html/assets/prototype-ui.js'));
const source=after.toString('utf8'), counts={positionFunction:0,toastCall:0,noticeDeclaration:0,handoffBranches:0};
const REMOVED=Symbol('declared scope removal');
const compact=value=>value.replace(/\s+/g,'');
function plain(value){
 if(Array.isArray(value))return value.map(plain);
 if(!value||typeof value!=='object')return value;
 return Object.fromEntries(Object.entries(value).filter(([key])=>!['start','end','loc','raw'].includes(key)).map(([key,v])=>[key,plain(v)]));
}
function transform(node,owners=[]){
 if(!node||typeof node!=='object')return node;
 if(Array.isArray(node))return node.map(n=>transform(n,owners)).filter(n=>n!==REMOVED);
 if(node.type==='FunctionDeclaration'&&node.id.name==='positionToast'){counts.positionFunction++;return REMOVED;}
 const currentOwners=node.type==='FunctionDeclaration'?[...owners,node.id.name]:owners;
 const code=node.start===undefined?'':compact(source.slice(node.start,node.end));
 if(node.type==='ExpressionStatement'&&code==="positionToast(node,document.querySelector('dialog[open]:not(.prototype-closing)'));" ){
  if(currentOwners.at(-1)!=='toast')throw Error('Toast placement call escaped owner');counts.toastCall++;return REMOVED;
 }
 if(node.type==='VariableDeclaration'&&code==="constnotice=dialog.querySelector('.prototype-toast');"){
  if(currentOwners.at(-1)!=='finish')throw Error('Notice declaration escaped close');counts.noticeDeclaration++;return REMOVED;
 }
 if(node.type==='IfStatement'&&['if(notice)document.body.append(notice);','if(notice)positionToast(notice);'].includes(code)){
  if(currentOwners.at(-1)!=='finish')throw Error('Handoff escaped close');counts.handoffBranches++;return REMOVED;
 }
 return Object.fromEntries(Object.entries(node).map(([key,v])=>[key,transform(v,currentOwners)]));
}
const parse=bytes=>acorn.parse(bytes.toString('utf8'),{ecmaVersion:'latest'});
const left=plain(transform(parse(after))),right=plain(parse(before));
function difference(a,b,at='root'){
 if(JSON.stringify(a)===JSON.stringify(b))return null;
 if(!a||!b||typeof a!=='object'||typeof b!=='object')return {at,current:a,before:b};
 if(Array.isArray(a)&&a.length!==b.length)return {at,current_length:a.length,before_length:b.length};
 for(const key of new Set([...Object.keys(a),...Object.keys(b)])){const result=difference(a[key],b[key],at+'.'+key);if(result)return result;}
 return {at};
}
if(JSON.stringify(left)!==JSON.stringify(right))throw Error('Other UI semantics changed: '+JSON.stringify(difference(left,right)));
if(JSON.stringify(counts)!==JSON.stringify({positionFunction:1,toastCall:1,noticeDeclaration:1,handoffBranches:2}))throw Error('Unexpected edits');
const oldCSS=fs.readFileSync(path.join(base,'prototype-ui.css'));
const newCSS=fs.readFileSync(path.join(root,'design-html/assets/prototype-ui.css'));
const rule='.prototype-toast[data-host=dialog]{top:max(var(--prototype-space-sm),var(--ui-safe-top,0px));bottom:auto}';
const normalized=newCSS.toString('utf8').replace(/\r\n/g,'\n');
if(normalized.split(rule).length!==2||normalized.replace(rule+'\n','')!==oldCSS.toString('utf8').replace(/\r\n/g,'\n'))throw Error('Other CSS changed');
const report={ui_before_sha256:hash(before),ui_after_sha256:hash(after),css_before_sha256:hash(oldCSS),css_after_sha256:hash(newCSS),
 changed_scope:counts,other_ui_ast_equal:true,other_css_text_equal:true,script_sha256:hash(fs.readFileSync(__filename)),
 parser:{version:acorn.version,sha256:hash(fs.readFileSync(process.argv[2]))},
 scope:'Static containment: only private Toast placement, its call, notice handoff in modal.finish and one Toast CSS rule differ. Not runtime or human visual acceptance.'};
const out=path.join(root,'design-html/prototype/evidence/current/toast-feedback/source-scope.json');
fs.writeFileSync(out,JSON.stringify(report,null,2)+'\n');process.stdout.write(JSON.stringify({other_ui_ast_equal:true,other_css_text_equal:true,changed_scope:counts})+'\n');
