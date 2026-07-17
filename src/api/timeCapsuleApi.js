import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';

export async function getTimeCapsules() {
  if (isMockMode()) return requestMock([]);
  try {
    const { supabase } = await getAuthenticatedContext();
    const { data, error } = await supabase.rpc('get_time_capsules');
    return error ? createApiError(error, '加载时光胶囊失败') : createApiResponse(fromDatabase(data || []));
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
    if (!title || !content || !payload.unlockDate) return createApiError('Missing capsule fields', '请填写标题、密信内容和解锁日期');
    const reminderEnabled = payload.reminder ?? payload.reminderEnabled ?? true;
    const { data, error } = await context.supabase.from('time_capsules').insert({
      couple_id: coupleId,
      creator_id: context.user.id,
      title,
      content,
      unlock_date: payload.unlockDate,
      reminder_enabled: reminderEnabled,
      content_types: payload.contentTypes || [],
    }).select('*').single();
    return error ? createApiError(error, '创建时光胶囊失败') : createApiResponse({ ...fromDatabase(data), locked: true });
  } catch (error) {
    return createApiError(error, '创建时光胶囊失败');
  }
}

export async function updateTimeCapsule(id, payload = {}) {
  if (isMockMode()) return requestMock({ id, ...payload });
  try {
    const { supabase } = await getAuthenticatedContext();
    const { data, error } = await supabase.rpc('update_time_capsule', {
      p_id: id,
      p_title: payload.title?.trim(),
      p_content: payload.content?.trim(),
      p_unlock_date: payload.unlockDate,
      p_reminder_enabled: payload.reminder ?? payload.reminderEnabled ?? true,
      p_content_types: payload.contentTypes || [],
    });
    return error ? createApiError(error, '更新时光胶囊失败') : createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '更新时光胶囊失败');
  }
}

export async function deleteTimeCapsule(id) {
  if (isMockMode()) return requestMock({ id, deleted: true });
  try {
    const { supabase } = await getAuthenticatedContext();
    const { error } = await supabase.rpc('delete_time_capsule', { p_id: id });
    return error ? createApiError(error, '删除时光胶囊失败') : createApiResponse({ id, deleted: true });
  } catch (error) {
    return createApiError(error, '删除时光胶囊失败');
  }
}

export async function setTimeCapsuleReminder(id, enabled) {
  if (isMockMode()) return requestMock({ id, reminder: enabled });
  try {
    const { supabase } = await getAuthenticatedContext();
    const { error } = await supabase.rpc('set_time_capsule_reminder', { p_id: id, p_enabled: enabled });
    return error ? createApiError(error, '更新胶囊提醒失败') : createApiResponse({ id, reminder: enabled });
  } catch (error) {
    return createApiError(error, '更新胶囊提醒失败');
  }
}
