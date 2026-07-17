import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const appDir = path.join(root, 'app');
const routeExtensions = new Set(['.js', '.jsx', '.ts', '.tsx']);
const excludedBasenames = new Set(['_layout.js', '_layout.jsx', '_layout.ts', '_layout.tsx']);
const excludedPathParts = new Set(['dev-ui-lab']);

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await walk(absolute));
    else if (routeExtensions.has(path.extname(entry.name))) files.push(absolute);
  }
  return files;
}

function isExcluded(relativePath, source) {
  const parts = relativePath.split(path.sep);
  if (excludedBasenames.has(path.basename(relativePath))) return 'layout';
  if (parts.some((part) => excludedPathParts.has(part))) return 'dev-ui-wrapper';
  if (/\bRedirect\b/.test(source) && !/\bFairyPage\b/.test(source)) return 'redirect-only';
  return null;
}

function openingFairyPage(source) {
  return source.match(/<FairyPage\b[\s\S]*?>/)?.[0] || '';
}

function auditFile(relativePath, source) {
  const issues = [];
  const hasPage = /<FairyPage\b/.test(source);
  const hasHeader = /<FairyHeader\b/.test(source);
  const pageOpening = openingFairyPage(source);

  if (!hasPage) issues.push('ordinary route must render FairyPage');
  if (hasHeader && !/\bheader\s*=/.test(pageOpening)) {
    issues.push('FairyHeader must be passed through FairyPage.header');
  }
  if (/from\s+['"]@supabase\/supabase-js['"]|from\s+['"][^'"]*api\/client['"]/.test(source)
      && /getSupabaseClient|createSupabaseClient/.test(source)) {
    issues.push('page must not access Supabase Client directly');
  }

  return issues.map((message) => `${relativePath}: ${message}`);
}

const files = await walk(appDir);
const excluded = [];
const failures = [];
let audited = 0;

for (const file of files) {
  const relativePath = path.relative(root, file);
  const source = await readFile(file, 'utf8');
  const reason = isExcluded(relativePath, source);
  if (reason) {
    excluded.push(`${relativePath} (${reason})`);
    continue;
  }
  audited += 1;
  failures.push(...auditFile(relativePath, source));
}

console.log(`Audited ${audited} app routes.`);
console.log(`Excluded ${excluded.length} files: layout, redirect-only and dev-ui wrapper files.`);
if (excluded.length) excluded.forEach((item) => console.log(`  - ${item}`));

if (failures.length) {
  console.error(`\nPage structure audit failed with ${failures.length} issue(s):`);
  failures.forEach((failure) => console.error(`  - ${failure}`));
  process.exitCode = 1;
} else {
  console.log('\nPage structure audit passed.');
}
