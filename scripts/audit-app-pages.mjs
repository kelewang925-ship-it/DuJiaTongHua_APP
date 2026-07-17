import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const APP_DIR = path.join(ROOT, 'app');
const EXTENSIONS = new Set(['.js', '.jsx', '.ts', '.tsx']);
const EXCLUDED_BASENAMES = new Set(['_layout.js', '_layout.jsx', '_layout.ts', '_layout.tsx']);
const EXCLUDED_PATH_PARTS = new Set(['dev-ui-lab']);

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) return walk(full);
    return [full];
  });
}

function isRedirectOnly(source) {
  return /<Redirect\b/.test(source) && !/<(?:View|ScrollView|FairyPage|SafeAreaView)\b/.test(source);
}

function isExcluded(file, source) {
  const relative = path.relative(APP_DIR, file).split(path.sep);
  return EXCLUDED_BASENAMES.has(path.basename(file))
    || relative.some((part) => EXCLUDED_PATH_PARTS.has(part))
    || isRedirectOnly(source);
}

const failures = [];
const exclusions = [];

for (const file of walk(APP_DIR).filter((item) => EXTENSIONS.has(path.extname(item)))) {
  const source = fs.readFileSync(file, 'utf8');
  const relative = path.relative(ROOT, file).replaceAll(path.sep, '/');

  if (isExcluded(file, source)) {
    exclusions.push(relative);
    continue;
  }

  const importsFairyPage = /(?:from\s+['"][^'"]*FairyPage['"]|import\s+FairyPage\b)/.test(source);
  const rendersFairyPage = /<FairyPage\b/.test(source);
  if (!importsFairyPage || !rendersFairyPage) {
    failures.push(`${relative}: ordinary route must import and render FairyPage`);
    continue;
  }

  const rendersHeader = /<FairyHeader\b/.test(source);
  const hasTopUi = rendersHeader || /showBack\b|title=|right=/.test(source);
  if (hasTopUi) {
    const headerProp = /<FairyPage[\s\S]*?\bheader=\{[\s\S]*?<FairyHeader\b/.test(source);
    if (!headerProp) failures.push(`${relative}: FairyHeader must be supplied through FairyPage.header`);
  }

  if (/(?:getSupabaseClient|createSupabaseClient|@supabase\/supabase-js|src\/api\/client)/.test(source)) {
    failures.push(`${relative}: page must not import or call Supabase client directly`);
  }
}

console.log(`Audited app routes. Excluded ${exclusions.length} layout/redirect/dev wrappers.`);
if (exclusions.length) console.log(`Excluded: ${exclusions.join(', ')}`);
if (failures.length) {
  console.error(failures.join('\n'));
  process.exitCode = 1;
} else {
  console.log('All audited app routes satisfy FairyPage/FairyHeader and API boundary rules.');
}
