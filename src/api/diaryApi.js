import { createApiError, isMockMode, requestMock } from './client';

const mockDiaries = [
  {
    id: 'diary_001',
    title: '一起散步的傍晚',
    content: '晚风很轻，普通的一天也像被温柔收藏起来。',
    mood: '开心',
    tags: ['散步', '日常'],
    date: '今天 20:18',
    createdAt: '2026-05-26T12:18:00.000Z',
  },
  {
    id: 'diary_002',
    title: '奶油蛋糕和你',
    content: '把蛋糕分成两半，好像连甜味都有了名字。',
    mood: '甜甜的',
    tags: ['约会', '甜品'],
    date: '昨天 16:42',
    createdAt: '2026-05-25T08:42:00.000Z',
  },
];

export async function getDiaryList(params = {}) {
  if (!isMockMode()) {
    return createApiError('Real diary API is not implemented yet.', '日记真实接口尚未接入');
  }

  const { limit } = params;
  const list = typeof limit === 'number' ? mockDiaries.slice(0, limit) : mockDiaries;
  return requestMock(list);
}

export async function getDiaryDetail(id) {
  if (!isMockMode()) {
    return createApiError('Real diary API is not implemented yet.', '日记详情真实接口尚未接入');
  }

  const diary = mockDiaries.find((item) => item.id === id) || mockDiaries[0];
  return requestMock(diary);
}

export async function createDiary(payload = {}) {
  if (!isMockMode()) {
    return createApiError('Real diary API is not implemented yet.', '创建日记真实接口尚未接入');
  }

  const diary = {
    id: `diary_${Date.now()}`,
    title: payload.title?.trim() || '今天的小小童话',
    content: payload.content?.trim() || '今天的故事，还没有完全写完。',
    mood: payload.mood || '开心',
    tags: payload.tags?.length ? payload.tags : ['日常'],
    date: '刚刚',
    createdAt: new Date().toISOString(),
  };

  return requestMock(diary, 500);
}

export async function updateDiary(id, payload = {}) {
  if (!isMockMode()) {
    return createApiError('Real diary API is not implemented yet.', '更新日记真实接口尚未接入');
  }

  return requestMock({
    id,
    ...payload,
    updatedAt: new Date().toISOString(),
  }, 400);
}

export async function deleteDiary(id) {
  if (!isMockMode()) {
    return createApiError('Real diary API is not implemented yet.', '删除日记真实接口尚未接入');
  }

  return requestMock({ id, deleted: true }, 300);
}
