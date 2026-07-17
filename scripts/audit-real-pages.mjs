import { readFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const requirements = [
  { file: 'app/account/couple-info.js', request: true, submit: true, mode: true },
  { file: 'app/account/invite.js', request: true, submit: false, mode: false },
  { file: 'app/account/bind-confirm.js', request: true, submit: true, mode: true },
  { file: 'app/comments/index.js', request: true, submit: true, mode: true },
  { file: 'app/notifications/index.js', request: true, submit: true, mode: true },
  { file: 'app/tags/index.js', request: true, submit: true, mode: true },
  { file: 'app/time-capsule/settings.js', request: true, submit: true, mode: true },
  { file: 'app/anniversary/edit.js', request: false, submit: true, mode: true },
  { file: 'app/diary/editor.js', request: false, submit: true, mode: true },
  { file: 'app/photo/upload.js', request: false, submit: true, mode: true },
  { file: 'app/search.js', request: false, submit: false, mode: false, derived: true },
  { file: 'app/couple/story-detail.js', request: false, submit: false, mode: false, derived: true },
];

const submitStatePattern = /\b(?:isSaving|saving|submitting|uploading)\b/i;
const failures = [];
for (const rule of requirements) {
  const source = await readFile(path.join(root, rule.file), 'utf8');
  if (rule.request && !/FairyRequestState/.test(source)) failures.push(`${rule.file}: missing loading/error/retry state`);
  if (rule.request && !/onRetry=/.test(source)) failures.push(`${rule.file}: missing retry action`);
  if (rule.submit && !submitStatePattern.test(source)) failures.push(`${rule.file}: missing submit-in-progress state`);
  if (rule.mode && !/getApiMode|isMockMode|hasCapability/.test(source)) failures.push(`${rule.file}: missing explicit Real/Mock boundary`);
  if (rule.derived && !/useFairyStore/.test(source)) failures.push(`${rule.file}: search/timeline must derive from loaded store data`);
  if (/@supabase\/supabase-js|getSupabaseClient|createSupabaseClient/.test(source)) failures.push(`${rule.file}: page accesses Supabase directly`);
}

if (failures.length) {
  console.error(`Real page audit failed with ${failures.length} issue(s):`);
  failures.forEach((failure) => console.error(`  - ${failure}`));
  process.exitCode = 1;
} else {
  console.log(`Real page audit passed for ${requirements.length} critical routes.`);
}
