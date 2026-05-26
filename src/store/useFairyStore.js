import { create } from 'zustand';
import {
  coupleProfile,
  initialAnniversaries,
  initialCreations,
  initialRecords,
  initialTimeline,
} from '../data/mockData';

const createRecordId = () => `record-${Date.now()}`;

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
      id: createRecordId(),
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
      id: `timeline-${Date.now()}`,
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

  getStats: () => {
    const { records, creations, anniversaries } = get();
    return {
      diaryCount: records.filter((item) => item.type === '日记').length,
      photoCount: records.filter((item) => item.type === '照片').length * 6,
      creationCount: creations.length,
      anniversaryCount: anniversaries.length,
    };
  },
}));

export default useFairyStore;
