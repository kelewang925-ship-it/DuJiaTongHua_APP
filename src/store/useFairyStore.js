import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { createJSONStorage, persist } from 'zustand/middleware';
import {
  coupleProfile,
  initialAnniversaries,
  initialCreations,
  initialRecords,
  initialTimeline,
} from '../data/mockData';

export const FAIRY_STORE_STORAGE_KEY = 'dujia-tonghua-fairy-store-v1';
const LEGACY_FAIRY_STORE_STORAGE_KEYS = ['dujia-tonghua-fairy-store-v2'];

const createId = (prefix) => `${prefix}-${Date.now()}`;

const emptyDraft = {
  title: '',
  content: '',
  mood: '开心',
  tags: ['开心', '约会', '日常'],
  attachments: [],
};

const initialCustomTags = [
  { id: 'tag-happy', name: '开心', category: '心情', icon: 'happy-outline' },
  { id: 'tag-miss', name: '想念', category: '心情', icon: 'heart-outline' },
  { id: 'tag-gentle', name: '温柔', category: '心情', icon: 'flower-outline' },
  { id: 'tag-home', name: '家', category: '地点', icon: 'home-outline' },
  { id: 'tag-cafe', name: '咖啡馆', category: '地点', icon: 'cafe-outline' },
  { id: 'tag-seaside', name: '海边', category: '地点', icon: 'water-outline' },
  { id: 'tag-anniversary', name: '周年', category: '纪念', icon: 'heart-circle-outline' },
  { id: 'tag-birthday', name: '生日', category: '纪念', icon: 'gift-outline' },
  { id: 'tag-first', name: '第一次', category: '纪念', icon: 'star-outline' },
  { id: 'tag-comic', name: '漫画', category: 'AI', icon: 'color-palette-outline' },
  { id: 'tag-video', name: '视频', category: 'AI', icon: 'play-circle-outline' },
];

const buildAiSteps = (type) => [
  '读取你们的回忆素材',
  type === '视频' ? '整理字幕、音乐和转场' : '整理故事分镜',
  type === '视频' ? '生成回忆放映机画面' : '绘制童话漫画页面',
  '放进童话工坊作品集',
];

const useFairyStore = create(
  persist(
    (set, get) => ({
      couple: coupleProfile,
      records: initialRecords,
      timeline: initialTimeline,
      creations: initialCreations,
      anniversaries: initialAnniversaries,
      activeAiJob: initialCreations[0] || null,
      draftDiary: emptyDraft,
      customTags: initialCustomTags,
      timeCapsules: [],

      updateDraftDiary: (patch) =>
        set((state) => ({
          draftDiary: {
            ...state.draftDiary,
            ...patch,
          },
        })),

      resetDraftDiary: () => set({ draftDiary: emptyDraft }),

      clearPersistedData: async () => {
        await Promise.all([
          AsyncStorage.removeItem(FAIRY_STORE_STORAGE_KEY),
          ...LEGACY_FAIRY_STORE_STORAGE_KEYS.map((key) => AsyncStorage.removeItem(key)),
        ]);
        set({
          couple: coupleProfile,
          records: initialRecords,
          timeline: initialTimeline,
          creations: initialCreations,
          anniversaries: initialAnniversaries,
          activeAiJob: initialCreations[0] || null,
          draftDiary: emptyDraft,
          customTags: initialCustomTags,
          timeCapsules: [],
        });
      },

      addCustomTag: ({ name, category = '心情', icon = 'pricetag-outline' }) => {
        const tag = { id: createId('tag'), name: name.trim(), category, icon };
        set((state) => ({ customTags: [...state.customTags, tag] }));
        return tag;
      },

      updateCustomTag: (id, patch) => set((state) => ({
        customTags: state.customTags.map((item) => item.id === id ? { ...item, ...patch, name: patch.name?.trim() || item.name } : item),
      })),

      removeCustomTag: (id) => set((state) => ({ customTags: state.customTags.filter((item) => item.id !== id) })),

      addTimeCapsule: ({ title, content, unlockDate, reminder = true, contentTypes = [] }) => {
        const capsule = { id: createId('capsule'), title: title.trim(), content: content.trim(), unlockDate, reminder, contentTypes, createdAt: new Date().toISOString() };
        set((state) => ({ timeCapsules: [capsule, ...state.timeCapsules] }));
        return capsule;
      },

      removeTimeCapsule: (id) => set((state) => ({ timeCapsules: state.timeCapsules.filter((item) => item.id !== id) })),

      toggleTimeCapsuleReminder: (id) => set((state) => ({
        timeCapsules: state.timeCapsules.map((item) => item.id === id ? { ...item, reminder: !item.reminder } : item),
      })),

      addDiaryRecord: ({ title, content, tags, mood, attachments = [] }) => {
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
      attachments,
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

      addPhotoRecord: ({ title, content, tags = ['照片'], photoCount = 3, photos = [] }) => {
    const safeTitle = title?.trim() || '新贴进绘本的一组照片';
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
      photos,
      createdAt: new Date().toISOString(),
    };

    const timelineItem = {
      id: createId('timeline'),
      recordId: record.id,
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

      removePhotoRecord: (id) => set((state) => ({
        records: state.records.filter((item) => item.id !== id),
        timeline: state.timeline.filter((item) => item.recordId !== id),
      })),

      addAnniversary: ({ title, date, note, type = 'heart', icon = 'heart-outline', repeatYearly = true, reminderDays = 3, coverColor = '#F5A3A8' }) => {
    const safeTitle = title?.trim() || '新的重要章节';
    const item = {
      id: createId('anniversary'),
      title: safeTitle,
      date: date?.trim() || '待设置日期',
      days: 0,
      icon,
      note: note?.trim() || '这是你们童话里值得记住的一章。',
      type,
      repeatYearly,
      reminderDays,
      coverColor,
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

      updateAnniversary: (id, patch) => {
        let updated = null;
        set((state) => ({
          anniversaries: state.anniversaries.map((item) => {
            if (item.id !== id) return item;
            updated = {
              ...item,
              ...patch,
              title: patch.title?.trim() || item.title,
              date: patch.date?.trim() || item.date,
              note: patch.note?.trim() || item.note || '这是你们童话里值得记住的一章。',
            };
            return updated;
          }),
        }));
        return updated;
      },

      addCreation: ({ type = '漫画', title, source, styleName, status, icon, progress }) => {
    const safeTitle = title?.trim() || (type === '视频' ? '新的回忆放映机' : '新的恋爱漫画');
    const safeSource = source || '童话工坊';
    const safeStyle = styleName || (type === '视频' ? '温柔字幕' : '童话绘本');
    const creation = {
      id: createId('creation'),
      type,
      title: safeTitle,
      source: safeSource,
      styleName: safeStyle,
      status: status || (type === '视频' ? '生成中 · 等待预览' : '生成中 · 正在绘制'),
      progress: progress || (type === '视频' ? 46 : 64),
      icon: icon || (type === '视频' ? 'film-outline' : 'albums-outline'),
      artwork: type === '视频' ? 'movie' : 'workshop',
      createdAt: new Date().toISOString(),
      steps: buildAiSteps(type),
      resultSummary:
        type === '视频'
          ? '将生成一段带字幕、音乐和柔和转场的回忆短片。'
          : '将生成一组适合收藏的童话漫画分镜。',
    };

    const timelineItem = {
      id: createId('timeline'),
      icon: 'sparkles-outline',
      title: `开始生成${type}《${safeTitle}》`,
      time: '刚刚',
      description: `${safeSource} · ${safeStyle} · 魔法正在发生。`,
      tag: 'AI',
    };

    set((state) => ({
      creations: [creation, ...state.creations],
      activeAiJob: creation,
      timeline: [timelineItem, ...state.timeline],
    }));

    return creation;
      },

      selectAiJob: (id) => {
        const job = get().creations.find((item) => item.id === id);
        if (job) {
          set({ activeAiJob: job });
        }
        return job;
      },

      removeCreation: (id) => set((state) => {
        const remaining = state.creations.filter((item) => item.id !== id);
        return {
          creations: remaining,
          activeAiJob: state.activeAiJob?.id === id ? remaining[0] || null : state.activeAiJob,
        };
      }),

      completeActiveAiJob: () => {
        const job = get().activeAiJob || get().creations[0];
        if (!job) return null;
        const resultSummary =
          job.resultSummary ||
          (job.type === '视频'
            ? '生成了一段带字幕、音乐和柔和转场的回忆短片。'
            : '生成了一组适合收藏的童话漫画分镜。');

        const doneJob = {
          ...job,
          progress: 100,
          status: job.type === '视频' ? '已生成 · 可预览回忆放映机' : '已生成 · 3 页绘本',
          resultSummary,
          steps: job.steps?.length ? job.steps : buildAiSteps(job.type),
          finishedAt: new Date().toISOString(),
        };

        const record = {
          id: createId('record-ai'),
          type: job.type,
          title: doneJob.title,
          date: '刚刚',
          content: resultSummary,
          icon: doneJob.icon,
          artwork: doneJob.artwork,
          tags: ['AI', job.type],
          mood: '魔法发生',
          likes: 0,
          createdAt: new Date().toISOString(),
        };

        const timelineItem = {
          id: createId('timeline'),
          icon: 'sparkles-outline',
          title: `${job.type}《${doneJob.title}》生成完成`,
          time: '刚刚',
          description: '作品已放进童话工坊，也同步到双人时间线。',
          tag: 'AI',
        };

        set((state) => ({
          creations: state.creations.map((item) => (item.id === job.id ? doneJob : item)),
          activeAiJob: doneJob,
          records: state.records.some((item) => item.title === doneJob.title && item.type === doneJob.type)
            ? state.records
            : [record, ...state.records],
          timeline: [timelineItem, ...state.timeline],
        }));

        return doneJob;
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
    }),
    {
      name: FAIRY_STORE_STORAGE_KEY,
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        couple: state.couple,
        records: state.records,
        timeline: state.timeline,
        creations: state.creations,
        anniversaries: state.anniversaries,
        activeAiJob: state.activeAiJob,
        draftDiary: state.draftDiary,
      }),
    }
  )
);

export default useFairyStore;
