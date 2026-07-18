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
import { createApiError, createApiResponse, getApiMode, withRequestTimeout } from '../api/client';
import { getCurrentSession } from '../api/authApi';
import { getCoupleInfo } from '../api/coupleApi';
import { getDiaryList, createDiary, deleteDiary } from '../api/diaryApi';
import { getAlbumList, uploadPhoto, deletePhoto } from '../api/photoApi';
import { getAnniversaries, createAnniversary, updateAnniversary as updateAnniversaryApi, deleteAnniversary } from '../api/anniversaryApi';
import { getTags, createTag, updateTag, deleteTag } from '../api/tagApi';
import { getTimeCapsules, createTimeCapsule, deleteTimeCapsule, setTimeCapsuleReminder } from '../api/timeCapsuleApi';
import { getNotifications, markNotificationRead, markAllNotificationsRead } from '../api/notificationApi';
import { subscribeToRealData } from '../api/realtimeApi';
import { getStorageKey } from '../config/storageNamespaces';

const IS_REAL_MODE = getApiMode() === 'real';
export const FAIRY_STORE_STORAGE_KEY = getStorageKey(getApiMode());
const LEGACY_FAIRY_STORE_STORAGE_KEYS = ['dujia-tonghua-fairy-store-v2'];

const createId = (prefix) => `${prefix}-${Date.now()}`;
let stopRealtime = null;
let realtimeIdentity = null;
let sessionEpoch = 0;
let coreLoadPromise = null;
let coreLoadIdentity = null;
let refreshTimer = null;

const realInitialState = {
  couple: null,
  records: [],
  timeline: [],
  creations: [],
  anniversaries: [],
  activeAiJob: null,
  customTags: [],
  timeCapsules: [],
  notifications: [],
};

export const deriveTimeline = (records = [], anniversaries = []) => [
  ...records.map((item) => ({
    id: `record-${item.id}`,
    recordId: item.id,
    title: item.title,
    description: item.content || item.note,
    time: item.createdAt || item.date,
    tag: item.type || '记录',
  })),
  ...anniversaries.map((item) => ({
    id: `anniversary-${item.id}`,
    title: item.title,
    description: item.description || item.note,
    time: item.date,
    tag: '纪念日',
  })),
].sort((a, b) => String(b.time || '').localeCompare(String(a.time || '')));

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

const mockInitialState = {
  couple: coupleProfile,
  records: initialRecords,
  timeline: initialTimeline,
  creations: initialCreations,
  anniversaries: initialAnniversaries,
  activeAiJob: initialCreations[0] || null,
  customTags: initialCustomTags,
  timeCapsules: [],
  notifications: [],
};

const buildAiSteps = (type) => [
  '读取你们的回忆素材',
  type === '视频' ? '整理字幕、音乐和转场' : '整理故事分镜',
  type === '视频' ? '生成回忆放映机画面' : '绘制童话漫画页面',
  '放进童话工坊作品集',
];

function stopRealtimeSafely() {
  if (refreshTimer) {
    clearTimeout(refreshTimer);
    refreshTimer = null;
  }
  if (stopRealtime) stopRealtime();
  stopRealtime = null;
  realtimeIdentity = null;
}

function sessionUserId(session) {
  return session?.user?.id || null;
}

function realOnlyError() {
  return createApiError('Mock-only store action in Real mode', 'Real 模式不能使用本地模拟写入');
}

const useFairyStore = create(
  persist(
    (set, get) => {
      const setRequestState = (key, loading, error = null) => set((state) => ({
        loading: { ...state.loading, [key]: loading },
        errors: { ...state.errors, [key]: error },
      }));

      const runRealWrite = async (key, operation, { refresh = true } = {}) => {
        if (!IS_REAL_MODE) return realOnlyError();
        setRequestState(key, true, null);
        const epoch = sessionEpoch;
        const result = await operation();
        if (epoch !== sessionEpoch) return createApiError('Session changed', '登录状态已变化，请重试');
        if (!result.success) {
          setRequestState(key, false, result.error);
          return result;
        }
        if (refresh) {
          const refreshResult = await get().loadCoreData({ force: true });
          if (!refreshResult.success) {
            setRequestState(key, false, refreshResult.error);
            return createApiResponse(result.data, {
              ...(result.meta || {}),
              serverWriteConfirmed: true,
              refreshFailed: true,
              refreshError: refreshResult.error,
            });
          }
        }
        setRequestState(key, false, null);
        return result;
      };

      return {
        ...(IS_REAL_MODE ? realInitialState : mockInitialState),
        session: null,
        profile: null,
        loading: {},
        errors: {},
        draftDiary: emptyDraft,

        resetForSession: async (session = null) => {
          sessionEpoch += 1;
          coreLoadPromise = null;
          coreLoadIdentity = null;
          stopRealtimeSafely();
          const userId = sessionUserId(session);
          if (IS_REAL_MODE) useFairyStore.persist.setOptions({ name: getStorageKey('real', userId) });
          set({ ...realInitialState, session, profile: null, loading: {}, errors: {}, draftDiary: emptyDraft });
          return createApiResponse({ session, userId });
        },

        loadCoreData: async ({ force = false } = {}) => {
          if (!IS_REAL_MODE) return createApiResponse({ mode: 'mock' });
          const currentSession = get().session;
          const userId = sessionUserId(currentSession);
          if (!userId) return createApiError('Missing session', '当前用户未登录');
          const epoch = sessionEpoch;
          const identity = `${userId}:${epoch}`;
          if (!force && coreLoadPromise && coreLoadIdentity === identity) return coreLoadPromise;

          coreLoadIdentity = identity;
          coreLoadPromise = (async () => {
            setRequestState('bootstrap', true, null);
            const coupleResult = await withRequestTimeout(
              getCoupleInfo(),
              12000,
              '加载情侣关系超时，请检查网络后重试',
            ).catch((error) => createApiError(error, '加载情侣关系超时，请检查网络后重试'));
            if (epoch !== sessionEpoch || userId !== sessionUserId(get().session)) return createApiError('Session changed', '登录状态已变化，请重试');
            if (!coupleResult.success) {
              setRequestState('bootstrap', false, coupleResult.error);
              return coupleResult;
            }

            if (!coupleResult.data?.couple) {
              stopRealtimeSafely();
              set({
                ...realInitialState,
                session: get().session,
                profile: coupleResult.data?.user || null,
                couple: coupleResult.data,
                loading: { bootstrap: false },
                errors: {},
              });
              return createApiResponse(coupleResult.data);
            }

            const moduleResults = await withRequestTimeout(Promise.all([
              getDiaryList(),
              getAlbumList(),
              getAnniversaries(),
              getTags(),
              getTimeCapsules(),
              getNotifications(),
            ]), 12000, '加载首页数据超时，请检查网络后重试').catch((error) => [
              createApiError(error, '加载首页数据超时，请检查网络后重试'),
            ]);
            const [diaryResult, albumResult, anniversaryResult, tagResult, capsuleResult, notificationResult] = moduleResults;
            if (epoch !== sessionEpoch || userId !== sessionUserId(get().session)) return createApiError('Session changed', '登录状态已变化，请重试');
            const failed = [diaryResult, albumResult, anniversaryResult, tagResult, capsuleResult, notificationResult].find((result) => !result?.success);
            if (failed) {
              setRequestState('bootstrap', false, failed.error);
              return failed;
            }

            const diaries = (diaryResult.data || []).map((item) => ({ ...item, type: '日记' }));
            const photos = (albumResult.data || []).map((item) => ({ ...item, type: '照片', photoCount: item.photos?.length || item.photoCount || 0 }));
            const records = [...diaries, ...photos];
            set({
              couple: coupleResult.data,
              profile: coupleResult.data?.user || null,
              records,
              anniversaries: anniversaryResult.data || [],
              customTags: tagResult.data || [],
              timeCapsules: capsuleResult.data || [],
              notifications: notificationResult.data || [],
              timeline: deriveTimeline(records, anniversaryResult.data || []),
              loading: { bootstrap: false },
              errors: {},
            });

            const coupleId = coupleResult.data.couple.id;
            const nextRealtimeIdentity = `${userId}:${coupleId}`;
            if (realtimeIdentity !== nextRealtimeIdentity) {
              stopRealtimeSafely();
              realtimeIdentity = nextRealtimeIdentity;
              try {
                stopRealtime = await subscribeToRealData({
                  onCoupleChange: () => {
                    if (epoch !== sessionEpoch || userId !== sessionUserId(get().session)) return;
                    if (refreshTimer) clearTimeout(refreshTimer);
                    refreshTimer = setTimeout(() => {
                      refreshTimer = null;
                      get().loadCoreData({ force: true });
                    }, 120);
                  },
                  onNotification: async () => {
                    if (epoch !== sessionEpoch || userId !== sessionUserId(get().session)) return;
                    const result = await getNotifications();
                    if (result.success && epoch === sessionEpoch && userId === sessionUserId(get().session)) set({ notifications: result.data });
                  },
                  onStatus: (status) => {
                    if (epoch !== sessionEpoch || userId !== sessionUserId(get().session)) return;
                    if (status.failed) setRequestState('realtime', false, createApiError(status.error, `实时同步频道 ${status.table} 连接失败`).error);
                    else if (status.connected) setRequestState('realtime', false, null);
                  },
                });
              } catch (error) {
                stopRealtime = null;
                realtimeIdentity = null;
                setRequestState('realtime', false, createApiError(error, '实时同步初始化失败').error);
              }
            }
            return createApiResponse({ userId, coupleId });
          })();

          try {
            return await coreLoadPromise;
          } finally {
            if (coreLoadIdentity === identity) {
              coreLoadPromise = null;
              coreLoadIdentity = null;
            }
          }
        },

        bootstrapApp: async () => {
          if (!IS_REAL_MODE) return createApiResponse({ mode: 'mock' });
          const bootstrapEpoch = ++sessionEpoch;
          stopRealtimeSafely();
          const result = await getCurrentSession();
          if (bootstrapEpoch !== sessionEpoch) return createApiError('Superseded bootstrap', '登录状态已变化，请重试');
          if (!result.success || !result.data?.session) {
            await get().resetForSession(null);
            return result.success ? createApiError('Missing session', '当前用户未登录') : result;
          }
          const userId = result.data.user?.id || result.data.session.user?.id;
          useFairyStore.persist.setOptions({ name: getStorageKey('real', userId) });
          await useFairyStore.persist.rehydrate();
          if (bootstrapEpoch !== sessionEpoch) return createApiError('Superseded rehydrate', '登录状态已变化，请重试');
          set({ ...realInitialState, session: result.data.session, profile: null, loading: {}, errors: {}, draftDiary: get().draftDiary || emptyDraft });
          return get().loadCoreData({ force: true });
        },

        refreshCoreData: () => get().loadCoreData({ force: true }),
        refreshNotifications: async () => {
          if (!IS_REAL_MODE) return createApiResponse({ mode: 'mock' });
          const epoch = sessionEpoch;
          const userId = sessionUserId(get().session);
          if (!userId) return createApiError('Missing session', '当前用户未登录');
          setRequestState('notifications', true, null);
          const result = await getNotifications();
          if (epoch !== sessionEpoch || userId !== sessionUserId(get().session)) {
            return createApiError('Session changed', '登录状态已变化，请重试');
          }
          if (!result.success) {
            setRequestState('notifications', false, result.error);
            return result;
          }
          set((state) => ({
            notifications: result.data || [],
            loading: { ...state.loading, notifications: false },
            errors: { ...state.errors, notifications: null },
          }));
          return result;
        },
        saveDiaryReal: (payload) => runRealWrite('saveDiary', () => createDiary(payload)),
        deleteDiaryReal: (id) => runRealWrite('deleteDiary', () => deleteDiary(id)),
        savePhotoCollectionReal: (payload) => runRealWrite('savePhoto', () => uploadPhoto(payload)),
        deletePhotoReal: (id) => runRealWrite('deletePhoto', () => deletePhoto(id)),
        saveAnniversaryReal: (payload) => runRealWrite('saveAnniversary', () => createAnniversary(payload)),
        updateAnniversaryReal: (id, payload) => runRealWrite('updateAnniversary', () => updateAnniversaryApi(id, payload)),
        deleteAnniversaryReal: (id) => runRealWrite('deleteAnniversary', () => deleteAnniversary(id)),
        saveTagReal: (payload) => runRealWrite('saveTag', () => createTag(payload)),
        updateTagReal: (id, payload) => runRealWrite('updateTag', () => updateTag(id, payload)),
        deleteTagReal: (id) => runRealWrite('deleteTag', () => deleteTag(id)),
        saveTimeCapsuleReal: (payload) => runRealWrite('saveTimeCapsule', () => createTimeCapsule(payload)),
        deleteTimeCapsuleReal: (id) => runRealWrite('deleteTimeCapsule', () => deleteTimeCapsule(id)),
        setTimeCapsuleReminderReal: async (id, enabled) => {
          const previousItem = get().timeCapsules.find((item) => item.id === id) || null;
          set((state) => ({ timeCapsules: state.timeCapsules.map((item) => item.id === id ? { ...item, reminder: enabled, reminderEnabled: enabled } : item) }));
          const result = await runRealWrite('capsuleReminder', () => setTimeCapsuleReminder(id, enabled), { refresh: false });
          if (!result.success && previousItem) {
            set((state) => ({ timeCapsules: state.timeCapsules.map((item) => item.id === id ? previousItem : item) }));
          }
          return result;
        },
        markNotificationRead: async (id) => {
          const previousItem = get().notifications.find((item) => item.id === id) || null;
          const optimisticReadAt = new Date().toISOString();
          set((state) => ({ notifications: state.notifications.map((item) => item.id === id ? { ...item, readAt: optimisticReadAt } : item) }));
          const result = await markNotificationRead(id);
          if (!result.success && previousItem) {
            set((state) => ({ notifications: state.notifications.map((item) => item.id === id && item.readAt === optimisticReadAt ? previousItem : item) }));
          }
          return result;
        },
        markAllNotificationsRead: async () => {
          const previousById = new Map(get().notifications.map((item) => [item.id, item]));
          const optimisticReadAt = new Date().toISOString();
          set((state) => ({ notifications: state.notifications.map((item) => ({ ...item, readAt: optimisticReadAt })) }));
          const result = await markAllNotificationsRead();
          if (!result.success) {
            set((state) => ({ notifications: state.notifications.map((item) => item.readAt === optimisticReadAt && previousById.has(item.id) ? previousById.get(item.id) : item) }));
          }
          return result;
        },

        updateDraftDiary: (patch) => set((state) => ({ draftDiary: { ...state.draftDiary, ...patch } })),
        resetDraftDiary: () => set({ draftDiary: emptyDraft }),
        clearPersistedData: async () => {
          const userKey = getStorageKey('real', sessionUserId(get().session));
          stopRealtimeSafely();
          sessionEpoch += 1;
          coreLoadPromise = null;
          coreLoadIdentity = null;
          const keys = [...new Set([
            FAIRY_STORE_STORAGE_KEY,
            getStorageKey('real'),
            userKey,
            ...LEGACY_FAIRY_STORE_STORAGE_KEYS,
          ].filter(Boolean))];
          const results = await Promise.allSettled(keys.map((key) => AsyncStorage.removeItem(key)));
          if (IS_REAL_MODE) useFairyStore.persist.setOptions({ name: getStorageKey('real') });
          set(IS_REAL_MODE ? { ...realInitialState, session: null, profile: null, draftDiary: emptyDraft, loading: {}, errors: {} } : { ...mockInitialState, session: null, profile: null, draftDiary: emptyDraft, loading: {}, errors: {} });
          const failedKeys = results.flatMap((result, index) => result.status === 'rejected' ? [keys[index]] : []);
          return createApiResponse({ cleared: failedKeys.length === 0, failedKeys }, { cleanupIncomplete: failedKeys.length > 0 });
        },

        addCustomTag: ({ name, category = '心情', icon = 'pricetag-outline' }) => {
          if (IS_REAL_MODE) return null;
          const tag = { id: createId('tag'), name: name.trim(), category, icon };
          set((state) => ({ customTags: [...state.customTags, tag] }));
          return tag;
        },
        updateCustomTag: (id, patch) => {
          if (IS_REAL_MODE) return null;
          set((state) => ({ customTags: state.customTags.map((item) => item.id === id ? { ...item, ...patch, name: patch.name?.trim() || item.name } : item) }));
          return get().customTags.find((item) => item.id === id) || null;
        },
        removeCustomTag: (id) => {
          if (IS_REAL_MODE) return false;
          set((state) => ({ customTags: state.customTags.filter((item) => item.id !== id) }));
          return true;
        },
        addTimeCapsule: ({ title, content, unlockDate, reminder = true, contentTypes = [] }) => {
          if (IS_REAL_MODE) return null;
          const capsule = { id: createId('capsule'), title: title.trim(), content: content.trim(), unlockDate, reminder, contentTypes, createdAt: new Date().toISOString() };
          set((state) => ({ timeCapsules: [capsule, ...state.timeCapsules] }));
          return capsule;
        },
        removeTimeCapsule: (id) => {
          if (IS_REAL_MODE) return false;
          set((state) => ({ timeCapsules: state.timeCapsules.filter((item) => item.id !== id) }));
          return true;
        },
        toggleTimeCapsuleReminder: async (id) => {
          const item = get().timeCapsules.find((capsule) => capsule.id === id);
          const enabled = !(item?.reminder ?? item?.reminderEnabled);
          if (IS_REAL_MODE) return get().setTimeCapsuleReminderReal(id, enabled);
          set((state) => ({ timeCapsules: state.timeCapsules.map((capsule) => capsule.id === id ? { ...capsule, reminder: enabled } : capsule) }));
          return createApiResponse({ id, reminder: enabled });
        },

        addDiaryRecord: ({ title, content, tags, mood, attachments = [] }) => {
          if (IS_REAL_MODE) return null;
          const safeTitle = title?.trim() || '今天的小小童话';
          const safeContent = content?.trim() || '今天的故事，还没有完全写完。';
          const record = { id: createId('record'), type: '日记', title: safeTitle, date: '刚刚', content: safeContent, icon: 'book-outline', artwork: 'memory', tags: tags?.length ? tags : ['日常'], mood: mood || '开心', likes: 0, attachments, createdAt: new Date().toISOString() };
          set((state) => ({ records: [record, ...state.records], timeline: deriveTimeline([record, ...state.records], state.anniversaries), draftDiary: emptyDraft }));
          return record;
        },
        addPhotoRecord: ({ title, content, tags = ['照片'], photoCount = 3, photos = [] }) => {
          if (IS_REAL_MODE) return null;
          const safeTitle = title?.trim() || '新贴进绘本的一组照片';
          const record = { id: createId('photo'), type: '照片', title: safeTitle, date: '刚刚', content: content?.trim() || `新增了 ${photoCount} 张照片，等待被写进故事里。`, icon: 'image-outline', artwork: 'album', tags, mood: '被收藏', likes: 0, photoCount, photos, createdAt: new Date().toISOString() };
          set((state) => ({ records: [record, ...state.records], timeline: deriveTimeline([record, ...state.records], state.anniversaries) }));
          return record;
        },
        removePhotoRecord: (id) => {
          if (IS_REAL_MODE) return false;
          set((state) => { const records = state.records.filter((item) => item.id !== id); return { records, timeline: deriveTimeline(records, state.anniversaries) }; });
          return true;
        },
        addAnniversary: ({ title, date, note, type = 'heart', icon = 'heart-outline', repeatYearly = true, reminderDays = 3, coverColor = '#F5A3A8' }) => {
          if (IS_REAL_MODE) return null;
          const item = { id: createId('anniversary'), title: title?.trim() || '新的重要章节', date: date?.trim() || '待设置日期', days: 0, icon, note: note?.trim() || '这是你们童话里值得记住的一章。', type, repeatYearly, reminderDays, coverColor };
          set((state) => { const anniversaries = [item, ...state.anniversaries]; return { anniversaries, timeline: deriveTimeline(state.records, anniversaries) }; });
          return item;
        },
        updateAnniversary: (id, patch) => {
          if (IS_REAL_MODE) return null;
          let updated = null;
          set((state) => {
            const anniversaries = state.anniversaries.map((item) => {
              if (item.id !== id) return item;
              updated = { ...item, ...patch, title: patch.title?.trim() || item.title, date: patch.date?.trim() || item.date, note: patch.note?.trim() || item.note || '这是你们童话里值得记住的一章。' };
              return updated;
            });
            return { anniversaries, timeline: deriveTimeline(state.records, anniversaries) };
          });
          return updated;
        },
        addCreation: ({ type = '漫画', title, source, styleName, status, icon, progress }) => {
          if (IS_REAL_MODE) return null;
          const safeTitle = title?.trim() || (type === '视频' ? '新的回忆放映机' : '新的恋爱漫画');
          const creation = { id: createId('creation'), type, title: safeTitle, source: source || '童话工坊', styleName: styleName || (type === '视频' ? '温柔字幕' : '童话绘本'), status: status || (type === '视频' ? '生成中 · 等待预览' : '生成中 · 正在绘制'), progress: progress || (type === '视频' ? 46 : 64), icon: icon || (type === '视频' ? 'film-outline' : 'albums-outline'), artwork: type === '视频' ? 'movie' : 'workshop', createdAt: new Date().toISOString(), steps: buildAiSteps(type), resultSummary: type === '视频' ? '将生成一段带字幕、音乐和柔和转场的回忆短片。' : '将生成一组适合收藏的童话漫画分镜。' };
          set((state) => ({ creations: [creation, ...state.creations], activeAiJob: creation }));
          return creation;
        },
        selectAiJob: (id) => {
          const job = get().creations.find((item) => item.id === id);
          if (job) set({ activeAiJob: job });
          return job;
        },
        removeCreation: (id) => {
          if (IS_REAL_MODE) return false;
          set((state) => { const remaining = state.creations.filter((item) => item.id !== id); return { creations: remaining, activeAiJob: state.activeAiJob?.id === id ? remaining[0] || null : state.activeAiJob }; });
          return true;
        },
        completeActiveAiJob: () => {
          if (IS_REAL_MODE) return null;
          const job = get().activeAiJob || get().creations[0];
          if (!job) return null;
          const resultSummary = job.resultSummary || (job.type === '视频' ? '生成了一段带字幕、音乐和柔和转场的回忆短片。' : '生成了一组适合收藏的童话漫画分镜。');
          const doneJob = { ...job, progress: 100, status: job.type === '视频' ? '已生成 · 可预览回忆放映机' : '已生成 · 3 页绘本', resultSummary, steps: job.steps?.length ? job.steps : buildAiSteps(job.type), finishedAt: new Date().toISOString() };
          const record = { id: createId('record-ai'), type: job.type, title: doneJob.title, date: '刚刚', content: resultSummary, icon: doneJob.icon, artwork: doneJob.artwork, tags: ['AI', job.type], mood: '魔法发生', likes: 0, createdAt: new Date().toISOString() };
          set((state) => {
            const records = state.records.some((item) => item.title === doneJob.title && item.type === doneJob.type) ? state.records : [record, ...state.records];
            return { creations: state.creations.map((item) => item.id === job.id ? doneJob : item), activeAiJob: doneJob, records, timeline: deriveTimeline(records, state.anniversaries) };
          });
          return doneJob;
        },
        getStats: () => {
          const { records, creations, anniversaries } = get();
          return { diaryCount: records.filter((item) => item.type === '日记').length, photoCount: records.filter((item) => item.type === '照片').reduce((sum, item) => sum + (item.photoCount || 0), 0), creationCount: creations.length, anniversaryCount: anniversaries.length };
        },
      };
    },
    {
      name: FAIRY_STORE_STORAGE_KEY,
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        draftDiary: state.draftDiary,
        ...(IS_REAL_MODE ? {} : { couple: state.couple, records: state.records, timeline: state.timeline, creations: state.creations, anniversaries: state.anniversaries, activeAiJob: state.activeAiJob, customTags: state.customTags, timeCapsules: state.timeCapsules }),
      }),
    }
  )
);

export default useFairyStore;
