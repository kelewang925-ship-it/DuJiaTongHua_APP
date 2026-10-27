/* Remove only the three added display nodes in the profile-page branch. */
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=__dirname,parserPath=process.argv[2];
if(!parserPath)throw Error('Pass the installed acorn module path');
const acorn=require(parserPath),sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const baseline=path.join(root,'evidence/baseline/relationship-day-counter');
const current=path.join(root,'evidence/current/relationship-day-counter');
const before=path.join(baseline,'prototype-relationship.js'),after=path.join(root,'../assets/prototype-relationship.js');
const REMOVED=Symbol('removed'),counts={function:0,listener:0,initial:0};
function normalize(node,inProfile=false,remove=false){
 if(node===null||typeof node!=='object')return node;
 if(Array.isArray(node))return node.map(n=>normalize(n,inProfile,remove)).filter(n=>n!==REMOVED);
 if(node.type==='IfStatement'&&node.test?.type==='BinaryExpression'&&node.test.left?.name==='id'&&node.test.right?.value==='m02-p06')inProfile=true;
 if(remove&&inProfile){
  if(node.type==='FunctionDeclaration'&&node.id?.name==='paintProfileDays'){counts.function++;return REMOVED;}
  const e=node.type==='ExpressionStatement'?node.expression:null;
  if(e?.type==='CallExpression'&&e.callee?.name==='paintProfileDays'&&e.arguments.length===0){counts.initial++;return REMOVED;}
  if(e?.type==='CallExpression'&&e.callee?.type==='MemberExpression'&&e.callee.property?.name==='addEventListener'&&e.arguments[0]?.value==='input'&&e.arguments[1]?.name==='paintProfileDays'){
   const owner=e.callee.object;
   if(owner?.type!=='MemberExpression'||owner.property?.name!=='met'||owner.object?.property?.name!=='elements'||owner.object.object?.name!=='form')throw Error('Unexpected listener owner');
   counts.listener++;return REMOVED;
  }
 }
 const result={};
 for(const[k,v]of Object.entries(node)){
  if(['start','end','loc','range','raw'].includes(k))continue;
  const normalized=normalize(v,inProfile,remove);if(normalized!==REMOVED)result[k]=normalized;
 }
 return result;
}
const parse=p=>acorn.parse(fs.readFileSync(p,'utf8'),{ecmaVersion:'latest',sourceType:'script'});
if(JSON.stringify(normalize(parse(before)))!==JSON.stringify(normalize(parse(after),false,true)))throw Error('Non-display JavaScript changed');
if(JSON.stringify(counts)!==JSON.stringify({function:1,listener:1,initial:1}))throw Error('Unexpected display patch shape');
const htmlBefore=path.join(baseline,'m02-p06.html'),htmlAfter=path.join(root,'../custom/m02-p06.html');
const text=p=>fs.readFileSync(p,'utf8').replace(/\r\n/g,'\n');
const extra='<script src="../assets/prototype-dates.js"></script>',placeholder='<b>—</b>';
let html=text(htmlAfter);if(html.split(extra).length!==2||html.split(placeholder).length!==2)throw Error('Unexpected HTML patch shape');
html=html.replace(extra,'').replace(placeholder,'<b>214</b>');if(html!==text(htmlBefore))throw Error('Unrelated profile markup changed');
const value={masked_nodes:counts,other_controller_ast_equal:true,html_changes:['existing date helper script','static214 replaced by neutral placeholder'],files_sha256:Object.fromEntries([before,after,htmlBefore,htmlAfter].map(p=>[path.relative(root,p).replaceAll('\\','/'),sha(p)])),parser_sha256:sha(parserPath),auditor_sha256:sha(__filename)};
fs.writeFileSync(path.join(current,'source-scope.json'),JSON.stringify(value,null,2)+'\n');
process.stdout.write('Verified: profile display nodes only; all original actions and other page branches retain equal AST\n');
