import { readFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const requirements = [
  ['app/ai/character-profile.js', 'aiGeneration'],
  ['app/ai/text-to-comic.js', 'aiGeneration'],
  ['app/ai/comic-config.js', 'aiGeneration'],
  ['app/ai/progress.js', 'aiGeneration'],
  ['app/ai/comic-result.js', 'aiGeneration'],
  ['app/ai/photo-to-comic.js', 'aiGeneration'],
  ['app/ai/video-config.js', 'aiGeneration'],
  ['app/ai/video-preview.js', 'aiGeneration'],
  ['app/ai/history.js', 'aiGeneration'],
  ['app/membership.js', 'membershipPayment'],
  ['app/data/pdf-export.js', 'pdfExport'],
  ['app/data/export-preview.js', 'pdfExport'],
  ['app/data/backup.js', 'cloudBackup'],
  ['app/share-preview.js', 'shareCardPersistence'],
  ['app/help-feedback.js', 'feedbackSubmission'],
  ['app/help-feedback.js', 'feedbackAttachment'],
  ['app/diary/editor.js', 'voiceAttachment'],
  ['app/diary/editor.js', 'locationAttachment'],
];

const forbiddenPagePatterns = [
  { pattern: /@supabase\/supabase-js/, message: 'page imports Supabase package directly' },
  { pattern: /\bgetSupabaseClient\b|\bcreateSupabaseClient\b/, message: 'page accesses Supabase Client directly' },
];

const mockWriteActions = ['addDiaryRecord', 'addPhotoRecord', 'addAnniversary', 'addCustomTag', 'addTimeCapsule', 'addCreation', 'completeActiveAiJob'];
const failures = [];
const cache = new Map();
async function source(relativePath) {
  if (!cache.has(relativePath)) cache.set(relativePath, await readFile(path.join(root, relativePath), 'utf8'));
  return cache.get(relativePath);
}

for (const [relativePath, capability] of requirements) {
  const text = await source(relativePath);
  if (!text.includes(capability) || !/hasCapability/.test(text)) failures.push(`${relativePath}: missing ${capability} Capability guard`);
  if (!text.includes('未开放')) failures.push(`${relativePath}: Real capability must display an explicit 未开放 message`);
}

const appFiles = [...new Set(requirements.map(([file]) => file))];
for (const relativePath of appFiles) {
  const text = await source(relativePath);
  for (const rule of forbiddenPagePatterns) if (rule.pattern.test(text)) failures.push(`${relativePath}: ${rule.message}`);
  const usedMockActions = mockWriteActions.filter((name) => new RegExp(`\\b${name}\\b`).test(text));
  if (usedMockActions.length && !/hasCapability|getApiMode/.test(text)) failures.push(`${relativePath}: mock write action lacks a Real/Mock guard (${usedMockActions.join(', ')})`);
}

if (failures.length) {
  console.error(`Real mode audit failed with ${failures.length} issue(s):`);
  failures.forEach((failure) => console.error(`  - ${failure}`));
  process.exitCode = 1;
} else {
  console.log(`Real mode audit passed for ${requirements.length} capability checks.`);
}
