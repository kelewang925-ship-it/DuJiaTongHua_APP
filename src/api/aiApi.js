import { requestMock } from './client';
import { mockAiJobs } from './mockData';

export async function createComicJob(payload) {
  return requestMock({
    id: `job_${Date.now()}`,
    title: payload?.title || '新的恋爱漫画',
    status: 'processing',
    progress: 1,
  }, 600);
}

export async function getAiJobDetail(id) {
  const job = mockAiJobs.find((item) => item.id === id) || mockAiJobs[0];
  return requestMock(job);
}

export async function getAiCreationHistory() {
  return requestMock([
    { id: 'creation_001', title: '第一次约会的小漫画', type: 'comic', status: 'done' },
    { id: 'creation_002', title: '春天散步纪念视频', type: 'video', status: 'draft' },
  ]);
}
