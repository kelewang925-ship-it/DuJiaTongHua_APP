import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';

function normalizeContentTypes(value) {
  if (!Array.isArray(value)) return null;
  const normalized = [...new Set(value.map((item) => String(item || '').trim()).filter(Boolean))];
  return normalized.length ? normalized : null;
}

function isValidFutureDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(value || ''))) return false;
  const date = new Date(`${value}T00:00:00`);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return !Number.isNaN(date.getTime()) && date > today;
}

function isCapsuleUnlocked(capsule) {
  if (!capsule) return false;
  if (capsule.isUnlocked === true || capsule.unlocked === true) return true;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(capsule.unlockDate || ''))) return false;
  const unlockDate = new Date(`${capsule.unlockDate}T00:00:00`);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return !Number.isNaN(unlockDate.getTime()) && unlockDate <= today;
}

function sanitizeCapsule(value, coupleId = null) {
  const capsule = fromDatabase(value);
  if (!capsule) return null;
  if (coupleId && capsule.coupleId !== coupleId) return null;
  if (isCapsuleUnlocked(capsule)) return capsule;
  return { ...capsule, content: null };
}

function sanitizeCapsules(values, coupleId) {
  if (!Array.isArray(values)) return [];
  const capsules = values.map((value) => sanitizeCapsule(value, coupleId));
  return capsules.some((item) => !item) ? null : capsules;
}

export async function getTimeCapsules() {
  if (isMockMode()) return requestMock([]);
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { data, error } = await context.supabase.rpc('get_time_capsules');
    if (error) return createApiError(error, '加载时光胶囊失败');
    const capsules = sanitizeCapsules(data || [], coupleId);
    if (!capsules) return createApiError('Invalid capsule ownership', '时光胶囊数据归属异常，请刷新后重试');
    return createApiResponse(capsules);
  } catch (error) {
    return createApiError(error, '加载时光胶囊失败');
  }
}

export async function createTimeCapsule(payload = {}) {
  if (isMockMode()) return requestMock({ id: `capsule_${Date.now()}`, ...payload });
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const title = payload.title?.trim();
    const content = payload.content?.trim();
    const contentTypes = normalizeContentTypes(payload.contentTypes);
    if (!title || !content) return createApiError('Missing capsule fields', '请填写标题和密信内容');
    if (!isValidFutureDate(payload.unlockDate)) return createApiError('Invalid unlock date', '请选择晚于今天的有效解锁日期');
    if (!contentTypes) return createApiError('Missing content types', '至少选择一种封存内容');
    if (typeof payload.reminder !== 'boolean' && typeof payload.reminderEnabled !== 'boolean') return createApiError('Missing reminder choice', '请确认是否开启提醒');
    const reminderEnabled = payload.reminder ?? payload.reminderEnabled;
    const { data, error } = await context.supabase.from('time_capsules').insert({
      couple_id: coupleId,
      creator_id: context.user.id,
      title,
      content,
      unlock_date: payload.unlockDate,
      reminder_enabled: reminderEnabled,
      content_types: contentTypes,
    }).select('*').maybeSingle();
    if (error) return createApiError(error, '创建时光胶囊失败');
    const capsule = sanitizeCapsule(data, coupleId);
    if (!capsule?.id || capsule.creatorId !== context.user.id) return createApiError('Capsule creation mismatch', '胶囊创建结果与当前情侣空间或账号不匹配');
    return createApiResponse(capsule);
  } catch (error) {
    return createApiError(error, '创建时光胶囊失败');
  }
}

export async function updateTimeCapsule(id, payload = {}) {
  if (isMockMode()) return requestMock({ id, ...payload });
  try {
    if (!id) return createApiError('Missing capsule id', '缺少胶囊标识，无法更新');
    const contentTypes = normalizeContentTypes(payload.contentTypes);
    if (!payload.title?.trim() || !payload.content?.trim()) return createApiError('Missing capsule fields', '请填写标题和密信内容');
    if (!isValidFutureDate(payload.unlockDate)) return createApiError('Invalid unlock date', '请选择晚于今天的有效解锁日期');
    if (!contentTypes) return createApiError('Missing content types', '至少选择一种封存内容');
    if (typeof payload.reminder !== 'boolean' && typeof payload.reminderEnabled !== 'boolean') return createApiError('Missing reminder choice', '请确认是否开启提醒');
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { data, error } = await context.supabase.rpc('update_time_capsule', {
      p_id: id,
      p_title: payload.title.trim(),
      p_content: payload.content.trim(),
      p_unlock_date: payload.unlockDate,
      p_reminder_enabled: payload.reminder ?? payload.reminderEnabled,
      p_content_types: contentTypes,
    });
    if (error) return createApiError(error, '更新时光胶囊失败');
    const capsule = sanitizeCapsule(data, coupleId);
    if (!capsule?.id || capsule.id !== id) return createApiError('Capsule not updated', '胶囊不存在、无权限或已被删除');
    return createApiResponse(capsule);
  } catch (error) {
    return createApiError(error, '更新时光胶囊失败');
  }
}

export async function deleteTimeCapsule(id) {
  if (isMockMode()) return requestMock({ id, deleted: true });
  try {
    if (!id) return createApiError('Missing capsule id', '缺少胶囊标识，无法删除');
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const { data, error } = await context.supabase.rpc('delete_time_capsule', { p_id: id });
    if (error) return createApiError(error, '删除时光胶囊失败');
    const value = fromDatabase(data);
    const deletedId = value?.id || value?.deletedId || (value === true ? id : null);
    if (!deletedId || deletedId !== id) return createApiError('Capsule not deleted', '胶囊不存在、无权限或已被删除');
    return createApiResponse({ id: deletedId, deleted: true });
  } catch (error) {
    return createApiError(error, '删除时光胶囊失败');
  }
}

export async function setTimeCapsuleReminder(id, enabled) {
  if (isMockMode()) return requestMock({ id, reminder: enabled });
  try {
    if (!id) return createApiError('Missing capsule id', '缺少胶囊标识，无法更新提醒');
    if (typeof enabled !== 'boolean') return createApiError('Invalid reminder value', '提醒状态无效');
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const { data, error } = await context.supabase.rpc('set_time_capsule_reminder', { p_id: id, p_enabled: enabled });
    if (error) return createApiError(error, '更新胶囊提醒失败');
    const value = fromDatabase(data);
    const updatedId = value?.id || (value === true ? id : null);
    if (!updatedId || updatedId !== id) return createApiError('Reminder not updated', '胶囊不存在、无权限或已被删除');
    return createApiResponse({ id: updatedId, reminder: enabled });
  } catch (error) {
    return createApiError(error, '更新胶囊提醒失败');
  }
}
