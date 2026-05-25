import { requestMock } from './client';
import { mockCouple, mockUser } from './mockData';

export async function getCurrentCouple() {
  return requestMock({
    user: mockUser,
    couple: mockCouple,
  });
}

export async function createInviteCode() {
  return requestMock({ code: 'FAIRY520', expiresIn: 3600 });
}

export async function bindCoupleByCode(code) {
  return requestMock({ code, coupleId: mockCouple.id, bound: true }, 600);
}

export async function getCoupleTimeline() {
  return requestMock([
    { id: 'event_001', title: '她写下了一篇日记', time: '今天 21:04' },
    { id: 'event_002', title: '你们新增了 6 张照片', time: '昨天 18:30' },
    { id: 'event_003', title: '童话漫画生成完成', time: '5月23日' },
  ]);
}
