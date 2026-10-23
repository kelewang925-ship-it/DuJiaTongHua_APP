const fs=require('fs'),path=require('path'),crypto=require('crypto');
const acornPath=process.argv[2],acorn=require(acornPath),base=process.cwd(),dir=path.join(base,'design-html/assets'),rows=[];
const h=s=>crypto.createHash('sha256').update(s).digest('hex'),files={};
function children(n){return Object.entries(n).flatMap(([k,v])=>k==='loc'?[]:Array.isArray(v)?v.filter(v=>v&&typeof v.type==='string'):v&&typeof v.type==='string'?[v]:[])}
for(const name of fs.readdirSync(dir).filter(n=>/^prototype-.*\.js$/.test(n))){
 const bytes=fs.readFileSync(path.join(dir,name)),s=bytes.toString('utf8'),tree=acorn.parse(s,{ecmaVersion:'latest',locations:true});files['assets/'+name]=h(bytes);
 function walk(n){
  if(n.type==='CallExpression'&&n.callee.type==='MemberExpression'&&n.callee.property.name==='busy'){
   const f=n.arguments[2];if(f&&['ArrowFunctionExpression','FunctionExpression'].includes(f.type)){
    const awaits=[],calls=[];function scan(v){if(v!==f&&['ArrowFunctionExpression','FunctionExpression','FunctionDeclaration'].includes(v.type))return;if(v.type==='AwaitExpression')awaits.push({line:v.loc.start.line,expression:s.slice(v.argument.start,v.argument.end)});if(v.type==='CallExpression')calls.push({line:v.loc.start.line,expression:s.slice(v.callee.start,v.callee.end)});for(const c of children(v))scan(c)}scan(f);
    rows.push({file:'assets/'+name,line:n.loc.start.line,operation:s.slice(n.arguments[1].start,n.arguments[1].end),async:!!f.async,awaits,calls,callback:s.slice(f.start,f.end)})
   }else rows.push({file:'assets/'+name,line:n.loc.start.line,unresolved_callback:f?s.slice(f.start,f.end):null})
  }for(const c of children(n))walk(c)
 }walk(tree)
}
const out={files,parser:{name:'acorn',version:acorn.version,sha256:h(fs.readFileSync(acornPath))},script_sha256:h(fs.readFileSync(__filename)),scope:'Static inventory of direct busy callbacks; await-free is not proof that transitive calls are synchronous. No runtime or final acceptance claim.',results:rows};
fs.mkdirSync('design-html/prototype/evidence/current/submission-await-audit',{recursive:true});
fs.writeFileSync('design-html/prototype/evidence/current/submission-await-audit/inventory.json',JSON.stringify(out,null,2)+'\n');
process.stdout.write(JSON.stringify({callbacks:rows.length,unresolved:rows.filter(v=>v.unresolved_callback).length,async:rows.filter(v=>v.async).length,withAwait:rows.filter(v=>v.awaits?.length).map(({file,line,awaits})=>({file,line,awaits}))},null,2));
