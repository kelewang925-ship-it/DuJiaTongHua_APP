import { createApiError, isMockMode, requestMock } from './client';

const mockAnniversaries = [
  {
    id: 'anniversary_001',
    title: '第一次见面',
    date: '2025-03-23',
    repeatType: 'yearly',
    description: '故事开始的那一天。',
    templateType: 'storybook',
    days: 428,
  },
  {
    id: 'anniversary_002',
    title: '第一次旅行',
    date: '2025-08-12',
    repeatType: 'yearly',
    description: '把夏天放进了同一张车票。',
    templateType: 'travel',
    days: 286,
  },
];

export async function getAnniversaries() {
  if (!isMockMode()) {
    return createApiError('Real anniversary API is not implemented yet.', '纪念日真实接口尚未接入');
  }

  return requestMock(mockAnniversaries);
}

export async function getAnniversaryList() {
  return getAnniversaries();
}

export async function getNextAnniversary() {
  if (!isMockMode()) {
    return createApiError('Real anniversary API is not implemented yet.', '下个纪念日真实接口尚未接入');
  }

  return requestMock(mockAnniversaries[0]);
}

export async function createAnniversary(payload = {}) {
  if (!isMockMode()) {
    return createApiError('Real anniversary API is not implemented yet.', '创建纪念日真实接口尚未接入');
  }

  const anniversary = {
    id: `anniversary_${Date.now()}`,
    title: payload.title?.trim() || '新的重要章节',
    date: payload.date?.trim() || '待设置日期',
    repeatType: payload.repeatType || 'yearly',
    description: payload.description?.trim() || payload.note?.trim() || '这是你们童话里值得记住的一章。',
    templateType: payload.templateType || 'storybook',
    days: 0,
    createdAt: new Date().toISOString(),
  };

  return requestMock(anniversary, 400);
}

export async function updateAnniversary(id, payload = {}) {
  if (!isMockMode()) {
    return createApiError('Real anniversary API is not implemented yet.', '更新纪念日真实接口尚未接入');
  }

  return requestMock({
    id,
    ...payload,
    updatedAt: new Date().toISOString(),
  }, 350);
}

export async function deleteAnniversary(id) {
  if (!isMockMode()) {
    return createApiError('Real anniversary API is not implemented yet.', '删除纪念日真实接口尚未接入');
  }

  return requestMock({ id, deleted: true }, 300);
}
