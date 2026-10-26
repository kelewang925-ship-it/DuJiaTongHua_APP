// Inventory actual failNext call expressions; declarations are not call sites.
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const acornPath = process.argv[2], acorn = require(acornPath);
const root = path.join(process.cwd(), 'design-html'), assets = path.join(root, 'assets');
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const files = {}, candidates = [], dynamic_sites = [];
function walk(node, visit) {
  if (!node || typeof node.type !== 'string') return;
  visit(node);
  for (const [key, value] of Object.entries(node)) {
    if (key === 'loc') continue;
    if (Array.isArray(value)) value.forEach(child => walk(child, visit));
    else if (value && typeof value === 'object') walk(value, visit);
  }
}
for (const file of fs.readdirSync(assets).filter(name => /^prototype-.*\.js$/.test(name)).sort()) {
  const raw = fs.readFileSync(path.join(assets, file)), text = raw.toString('utf8');
  files[file] = hash(raw);
  walk(acorn.parse(text, { ecmaVersion: 'latest', locations: true }), node => {
    if (node.type !== 'CallExpression') return;
    const callee = node.callee;
    const name = callee.type === 'Identifier' ? callee.name :
      callee.type === 'MemberExpression' ?
        (callee.computed ? callee.property.value : callee.property.name) : null;
    if (name !== 'failNext') return;
    const arg = node.arguments[0], site = { file, line: node.loc.start.line };
    if (arg?.type === 'Literal' && typeof arg.value === 'string')
      candidates.push({ operation: arg.value, ...site });
    else dynamic_sites.push({ ...site, expression: arg ? text.slice(arg.start, arg.end) : '(missing)' });
  });
}
const report = {
  candidates, dynamic_sites, files,
  literal_operation_count: new Set(candidates.map(row => row.operation)).size,
  excluded_definition: { file: 'prototype-ui.js', reason: 'AST call expressions exclude helper declarations.' },
  parser: { name: 'acorn', version: acorn.version, sha256: hash(fs.readFileSync(acornPath)) },
  script_sha256: hash(fs.readFileSync(__filename)),
  scope: 'Static failNext call sites, including dynamic argument expressions. References do not prove failure consumption or branch coverage.'
};
fs.writeFileSync(path.join(root, 'prototype/evidence/current/failure-operation-candidates.json'), JSON.stringify(report, null, 2) + '\n');
process.stdout.write(JSON.stringify({ literal_operations: report.literal_operation_count, literal_sites: candidates.length, dynamic_sites: dynamic_sites.length }) + '\n');
