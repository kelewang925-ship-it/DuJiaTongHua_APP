import { createApiError, isMockMode, requestMock } from './client';
import { mockAiJobs } from './mockData';

const creationHistory = [
  { id: 'creation_001', title: '第一次约会的小漫画', type: 'comic', status: 'done' },
  { id: 'creation_002', title: '春天散步纪念视频', type: 'video', status: 'draft' },
];

function createJobPayload(type, payload = {}) {
  return {
    id: `job_${Date.now()}`,
    type,
    title: payload.title?.trim() || (type === 'video' ? '新的回忆放映机' : '新的恋爱漫画'),
    sourceType: payload.sourceType || 'text',
    sourceIds: payload.sourceIds || [],
    text: payload.text || '',
    style: payload.style || 'storybook',
    characterProfile: payload.characterProfile || null,
    status: 'processing',
    progress: 1,
    resultUrls: [],
    errorMessage: null,
    createdAt: new Date().toISOString(),
  };
}

export async function createComicJob(payload = {}) {
  if (!isMockMode()) {
    return createApiError('Real AI API is not implemented yet.', 'AI 漫画真实接口尚未接入');
  }

  return requestMock(createJobPayload('comic', payload), 600);
}

export async function createVideoJob(payload = {}) {
  if (!isMockMode()) {
    return createApiError('Real AI API is not implemented yet.', 'AI 视频真实接口尚未接入');
  }

  return requestMock(createJobPayload('video', payload), 600);
}

export async function getAiJobDetail(id) {
  if (!isMockMode()) {
    return createApiError('Real AI API is not implemented yet.', 'AI 任务真实接口尚未接入');
  }

  const job = mockAiJobs.find((item) => item.id === id) || mockAiJobs[0];
  return requestMock({
    type: 'comic',
    sourceType: 'diary',
    sourceIds: [],
    resultUrls: [],
    errorMessage: null,
    ...job,
  });
}

export async function getAiCreationHistory() {
  if (!isMockMode()) {
    return createApiError('Real AI API is not implemented yet.', 'AI 创作历史真实接口尚未接入');
  }

  return requestMock(creationHistory);
}

export async function retryAiJob(id) {
  if (!isMockMode()) {
    return createApiError('Real AI API is not implemented yet.', 'AI 重试真实接口尚未接入');
  }

  return requestMock({
    id,
    status: 'processing',
    progress: 1,
    retriedAt: new Date().toISOString(),
  }, 400);
}
