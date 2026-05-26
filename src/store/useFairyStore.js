import { create } from 'zustand';
import {
  coupleProfile,
  initialAnniversaries,
  initialCreations,
  initialRecords,
  initialTimeline,
} from '../data/mockData';

const createId = (prefix) => `${prefix}-${Date.now()}`;

const emptyDraft = {
  title: '',
  content: '',
  mood: '开心',
  tags: ['开心', '约会', '日常'],
};

const useFairyStore = create((set, get) => ({
  couple: coupleProfile,
  records: initialRecords,
  timeline: initialTimeline,
  creations: initialCreations,
  anniversaries: initialAnniversaries,
  draftDiary: emptyDraft,

  updateDraftDiary: (patch) =>
    set((state) => ({
      draftDiary: {
        ...state.draftDiary,
        ...patch,
      },
    })),

  resetDraftDiary: () => set({ draftDiary: emptyDraft }),

  addDiaryRecord: ({ title, content, tags, mood }) => {
    const safeTitle = title?.trim() || '今天的小小童话';
    const safeContent = content?.trim() || '今天的故事，还没有完全写完。';
    const now = new Date();
    const record = {
      id: createId('record'),
      type: '日记',
      title: safeTitle,
      date: '刚刚',
      content: safeContent,
      icon: 'book-outline',
      artwork: 'memory',
      tags: tags?.length ? tags : ['日常'],
      mood: mood || '开心',
      likes: 0,
      createdAt: now.toISOString(),
    };

    const timelineItem = {
      id: createId('timeline'),
      icon: 'book-outline',
      title: `写下了《${safeTitle}》`,
      time: '刚刚',
      description: safeContent,
      tag: '日记',
    };

    set((state) => ({
      records: [record, ...state.records],
      timeline: [timelineItem, ...state.timeline],
      draftDiary: emptyDraft,
    }));

    return record;
  },

  addPhotoRecord: ({ title, content, tags = ['照片'], photoCount = 3 }) => {
    const safeTitle = title?.trim() || '新贴进绘本的一张照片';
    const safeContent = content?.trim() || `新增了 ${photoCount} 张照片，等待被写进故事里。`;
    const record = {
      id: createId('photo'),
      type: '照片',
      title: safeTitle,
      date: '刚刚',
      content: safeContent,
      icon: 'image-outline',
      artwork: 'album',
      tags,
      mood: '被收藏',
      likes: 0,
      photoCount,
      createdAt: new Date().toISOString(),
    };

    const timelineItem = {
      id: createId('timeline'),
      icon: 'image-outline',
      title: `新增了 ${photoCount} 张照片`,
      time: '刚刚',
      description: safeTitle,
      tag: '照片',
    };

    set((state) => ({
      records: [record, ...state.records],
      timeline: [timelineItem, ...state.timeline],
    }));

    return record;
  },

  addAnniversary: ({ title, date, note }) => {
    const safeTitle = title?.trim() || '新的重要章节';
    const item = {
      id: createId('anniversary'),
      title: safeTitle,
      date: date?.trim() || '待设置日期',
      days: 0,
      icon: 'heart-outline',
      note: note?.trim() || '这是你们童话里值得记住的一章。',
    };

    const timelineItem = {
      id: createId('timeline'),
      icon: 'calendar-outline',
      title: `添加了纪念日《${safeTitle}》`,
      time: '刚刚',
      description: item.note,
      tag: '纪念日',
    };

    set((state) => ({
      anniversaries: [item, ...state.anniversaries],
      timeline: [timelineItem, ...state.timeline],
    }));

    return item;
  },

  addCreation: ({ type = '漫画', title, status, icon }) => {
    const safeTitle = title?.trim() || (type === '视频' ? '新的回忆放映机' : '新的恋爱漫画');
    const creation = {
      id: createId('creation'),
      type,
      title: safeTitle,
      status: status || (type === '视频' ? '生成中 · 等待预览' : '生成中 · 正在绘制'),
      icon: icon || (type === '视频' ? 'film-outline' : 'albums-outline'),
    };

    const timelineItem = {
      id: createId('timeline'),
      icon: 'sparkles-outline',
      title: `开始生成${type}《${safeTitle}》`,
      time: '刚刚',
      description: '魔法正在把回忆变成可以收藏的作品。',
      tag: 'AI',
    };

    set((state) => ({
      creations: [creation, ...state.creations],
      timeline: [timelineItem, ...state.timeline],
    }));

    return creation;
  },

  getStats: () => {
    const { records, creations, anniversaries } = get();
    return {
      diaryCount: records.filter((item) => item.type === '日记').length,
      photoCount: records
        .filter((item) => item.type === '照片')
        .reduce((sum, item) => sum + (item.photoCount || 3), 0),
      creationCount: creations.length,
      anniversaryCount: anniversaries.length,
    };
  },
}));

export default useFairyStore;
