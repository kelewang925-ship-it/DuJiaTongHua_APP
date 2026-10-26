const fs = require('fs'), path = require('path'), crypto = require('crypto');
const acornPath = process.argv[2], acorn = require(acornPath);
const base = process.cwd(), root = path.join(base, 'design-html/prototype');
const beforePath = path.join(root, 'evidence/baseline/album-timeout/prototype-workshop-store.js');
const afterPath = path.join(base, 'design-html/assets/prototype-workshop-store.js');
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
function walk(node, visitor, ancestors = []) {
  if (!node || typeof node.type !== 'string') return;
  visitor(node, ancestors);
  for (const [key, value] of Object.entries(node)) {
    if (key === 'loc') continue;
    if (Array.isArray(value)) value.forEach(child => walk(child, visitor, [...ancestors, node]));
    else if (value && typeof value === 'object') walk(value, visitor, [...ancestors, node]);
  }
}
function analyze(bytes) {
  const text = bytes.toString('utf8').replace(/\r\n/g, '\n'), functions = [], calls = [];
  walk(acorn.parse(text, { ecmaVersion: 'latest', locations: true }), (node, ancestors) => {
    if (node.type === 'FunctionDeclaration' && node.id?.name === 'decodedImage') functions.push(node);
    if (node.type === 'CallExpression' && node.callee.type === 'Identifier' && node.callee.name === 'decodedImage')
      calls.push({ owner: [...ancestors].reverse().find(n => n.type === 'FunctionDeclaration')?.id?.name,
                   expression: text.slice(node.start, node.end) });
  });
  if (functions.length !== 1 || calls.length !== 2 || calls.some(call => call.owner !== 'album'))
    throw new Error('Unexpected decoder ownership/call sites');
  const fn = functions[0];
  return { outside: text.slice(0, fn.start) + '/* private decodedImage body */' + text.slice(fn.end),
           function_sha256: hash(text.slice(fn.start, fn.end)), calls };
}
const before = fs.readFileSync(beforePath), after = fs.readFileSync(afterPath);
const oldScope = analyze(before), currentScope = analyze(after);
if (oldScope.outside !== currentScope.outside) throw new Error('Product changes escape the private decoder');
const callers = [];
for (const file of fs.readdirSync(path.join(base, 'design-html/assets')).filter(n => /^prototype-.*\.js$/.test(n))) {
  const text = fs.readFileSync(path.join(base, 'design-html/assets', file), 'utf8');
  walk(acorn.parse(text, { ecmaVersion: 'latest', locations: true }), (node, ancestors) => {
    if (node.type === 'CallExpression' && node.callee.type === 'MemberExpression' && node.callee.property.name === 'album')
      callers.push({ file: 'assets/' + file, line: node.loc.start.line, expression: text.slice(node.start, node.end),
                     conditions: ancestors.filter(n => n.type === 'IfStatement').map(n => text.slice(n.test.start, n.test.end)) });
  });
}
if (callers.length !== 1 || callers[0].file !== 'assets/prototype-workshop.js') throw new Error('Unexpected album caller');
const report = { before_sha256: hash(before), after_sha256: hash(after), private_function: 'decodedImage',
  outside_function_unchanged: true, outside_function_sha256: hash(currentScope.outside),
  before_function_sha256: oldScope.function_sha256, after_function_sha256: currentScope.function_sha256,
  decoder_calls: currentScope.calls, album_callers: callers,
  parser: { name: 'acorn', version: acorn.version, sha256: hash(fs.readFileSync(acornPath)) },
  script_sha256: hash(fs.readFileSync(__filename)),
  scope: 'Static change containment and caller discovery only; not runtime or all-dependent-page acceptance.' };
fs.mkdirSync(path.join(root, 'evidence/current/album-timeout'), { recursive: true });
fs.writeFileSync(path.join(root, 'evidence/current/album-timeout/source-scope.json'), JSON.stringify(report, null, 2) + '\n');
process.stdout.write(JSON.stringify({ outside_function_unchanged: true, decoder_calls: currentScope.calls.length, album_callers: callers }) + '\n');
