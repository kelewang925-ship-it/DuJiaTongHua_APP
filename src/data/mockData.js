export const coupleProfile = {
  userName: '林小满',
  partnerName: '陆星河',
  loveStartDate: '2025-03-23',
  loveDays: 428,
  statusText: '今天也被好好爱着。',
  spaceName: '我们的小小宇宙',
};

export const initialRecords = [
  {
    id: 'record-diary-001',
    type: '日记',
    title: '一起散步的傍晚',
    date: '今天 20:18',
    content: '晚风很轻，普通的一天也像被温柔收藏起来。',
    icon: 'book-outline',
    artwork: 'memory',
    tags: ['日常', '开心'],
    mood: '被爱着',
    likes: 128,
    createdAt: '2026-05-25T20:18:00.000Z',
  },
  {
    id: 'record-photo-001',
    type: '照片',
    title: '奶油蛋糕和你',
    date: '昨天 16:42',
    content: '上传了 6 张照片，准备把这一天变成漫画。',
    icon: 'camera-outline',
    artwork: 'album',
    tags: ['照片', '约会'],
    mood: '甜甜的',
    likes: 96,
    createdAt: '2026-05-24T16:42:00.000Z',
  },
  {
    id: 'record-ai-001',
    type: '漫画',
    title: '第一次约会的小漫画',
    date: '5月23日',
    content: '童话工坊已经把这段回忆画成 3 页绘本。',
    icon: 'sparkles-outline',
    artwork: 'workshop',
    tags: ['AI', '漫画'],
    mood: '魔法发生',
    likes: 152,
    createdAt: '2026-05-23T11:30:00.000Z',
  },
];

export const initialTimeline = [
  {
    id: 'timeline-001',
    icon: 'book-outline',
    title: '她写下了一篇日记',
    time: '今天 21:04',
    description: '关于今天一起走过的那条小路。',
    tag: '日记',
  },
  {
    id: 'timeline-002',
    icon: 'image-outline',
    title: '你们新增了 6 张照片',
    time: '昨天 18:30',
    description: '黄昏、甜点和两个人的影子。',
    tag: '照片',
  },
  {
    id: 'timeline-003',
    icon: 'sparkles-outline',
    title: '童话漫画生成完成',
    time: '5月23日',
    description: '新的绘本章节已经放进收藏册。',
    tag: 'AI',
  },
  {
    id: 'timeline-004',
    icon: 'calendar-outline',
    title: '第一次旅行快到了',
    time: '还有 24 天',
    description: '可以提前准备一页专属记录模板。',
    tag: '纪念日',
  },
];

export const initialCreations = [
  {
    id: 'creation-001',
    type: '漫画',
    title: '第一次约会的小漫画',
    status: '已生成 · 3 页绘本',
    icon: 'albums-outline',
    artwork: 'workshop',
  },
  {
    id: 'creation-002',
    type: '视频',
    title: '春天散步纪念视频',
    status: '草稿中 · 可继续编辑',
    icon: 'film-outline',
    artwork: 'movie',
  },
];

export const initialAnniversaries = [
  {
    id: 'anniversary-001',
    title: '在一起纪念日',
    date: '2025-03-23',
    days: 428,
    icon: 'heart-outline',
  },
  {
    id: 'anniversary-002',
    title: '第一次一起旅行',
    date: '2025-07-12',
    days: 24,
    icon: 'airplane-outline',
  },
  {
    id: 'anniversary-003',
    title: '第一次交换礼物',
    date: '2025-05-20',
    days: 370,
    icon: 'gift-outline',
  },
];
