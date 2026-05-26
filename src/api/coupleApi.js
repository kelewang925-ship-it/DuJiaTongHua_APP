import { createApiError, isMockMode, requestMock } from './client';
import { mockCouple, mockUser } from './mockData';

const mockTimeline = [
  { id: 'event_001', title: '她写下了一篇日记', time: '今天 21:04', type: 'diary' },
  { id: 'event_002', title: '你们新增了 6 张照片', time: '昨天 18:30', type: 'photo' },
  { id: 'event_003', title: '童话漫画生成完成', time: '5月23日', type: 'ai' },
];

export async function getCoupleInfo() {
  if (!isMockMode()) {
    return createApiError('Real couple API is not implemented yet.', '情侣信息真实接口尚未接入');
  }

  return requestMock({
    user: mockUser,
    couple: mockCouple,
    status: 'active',
  });
}

export async function getCurrentCouple() {
  return getCoupleInfo();
}

export async function createInviteCode() {
  if (!isMockMode()) {
    return createApiError('Real couple API is not implemented yet.', '邀请码真实接口尚未接入');
  }

  return requestMock({
    code: 'FAIRY520',
    expiresIn: 3600,
    expiresAt: new Date(Date.now() + 3600 * 1000).toISOString(),
  });
}

export async function bindCouple(inviteCode) {
  if (!isMockMode()) {
    return createApiError('Real couple API is not implemented yet.', '情侣绑定真实接口尚未接入');
  }

  return requestMock({
    inviteCode,
    coupleId: mockCouple.id,
    status: 'active',
    bound: true,
  }, 600);
}

export async function bindCoupleByCode(code) {
  return bindCouple(code);
}

export async function updateCoupleInfo(payload = {}) {
  if (!isMockMode()) {
    return createApiError('Real couple API is not implemented yet.', '情侣资料真实接口尚未接入');
  }

  return requestMock({
    ...mockCouple,
    ...payload,
    updatedAt: new Date().toISOString(),
  }, 400);
}

export async function getCoupleTimeline() {
  if (!isMockMode()) {
    return createApiError('Real couple API is not implemented yet.', '情侣时间线真实接口尚未接入');
  }

  return requestMock(mockTimeline);
}
