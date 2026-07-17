import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const apiDir = path.join(root, 'src/api');
const entries = (await readdir(apiDir)).filter((name) => name.endsWith('Api.js')).sort();
const failures = [];

for (const name of entries) {
  const relative = `src/api/${name}`;
  const source = await readFile(path.join(apiDir, name), 'utf8');
  if (!/createApiResponse/.test(source) || !/createApiError/.test(source)) {
    failures.push(`${relative}: must use the shared API response envelope`);
  }
  if (/return\s+\{\s*success\s*:/.test(source)) {
    failures.push(`${relative}: must not construct API envelopes manually`);
  }
  if (/\.from\(|\.rpc\(|\.storage\./.test(source) && !/try\s*\{/.test(source)) {
    failures.push(`${relative}: Real client operations must be caught and normalized`);
  }
  if (/\.insert\(|\.update\(|\.delete\(/.test(source) && !/isMockMode\(\)/.test(source)) {
    failures.push(`${relative}: write APIs must declare a Mock/Real boundary`);
  }
  if (/\.from\(['"](?:diaries|photos|photo_collections|anniversaries|custom_tags|comments)['"]\)/.test(source)
      && !/couple_id|coupleId|requireCouple/.test(source)) {
    failures.push(`${relative}: couple-owned queries must include couple scope`);
  }
}

if (failures.length) {
  console.error(`API contract audit failed with ${failures.length} issue(s):`);
  failures.forEach((failure) => console.error(`  - ${failure}`));
  process.exitCode = 1;
} else {
  console.log(`API contract audit passed for ${entries.length} API modules.`);
}
