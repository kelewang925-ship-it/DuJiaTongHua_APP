import { requestMock } from './client';

export async function createDiary(payload) {
  return requestMock({
    id: `diary_${Date.now()}`,
    ...payload,
  }, 500);
}

export async function getDiaryList() {
  return requestMock([
    { id: 'diary_001', title: '一起散步的傍晚', date: '今天 20:18' },
    { id: 'diary_002', title: '奶油蛋糕和你', date: '昨天 16:42' },
  ]);
}

export async function getDiaryDetail(id) {
  return requestMock({
    id,
    title: '一起散步的傍晚',
    content: '晚风很轻，普通的一天也像被温柔收藏起来。',
  });
}
