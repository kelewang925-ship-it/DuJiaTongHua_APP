import { requestMock } from './client';

const anniversaries = [
  { id: 'ann_001', title: '第一次见面', date: '2025.03.23', type: 'first_meet' },
  { id: 'ann_002', title: '第一次旅行', date: '2025.06.18', type: 'travel' },
  { id: 'ann_003', title: '恋爱纪念日', date: '2025.05.20', type: 'love' },
];

export async function getAnniversaryList() {
  return requestMock(anniversaries);
}

export async function createAnniversary(payload) {
  return requestMock({ id: `ann_${Date.now()}`, ...payload }, 500);
}

export async function updateAnniversary(id, payload) {
  return requestMock({ id, ...payload }, 500);
}

export async function deleteAnniversary(id) {
  return requestMock({ id });
}
