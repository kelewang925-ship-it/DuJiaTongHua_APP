import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requestMock } from './client';
import { fromDatabase } from './mappers';

export async function getNotifications() {
  if (isMockMode()) return requestMock([]);
  try {
    const context = await getAuthenticatedContext();
    const { data, error } = await context.supabase.from('notifications').select('*').eq('user_id', context.user.id).order('created_at', { ascending: false });
    if (error) return createApiError(error, '加载通知失败');
    const rows = data || [];
    const invalid = rows.find((item) => !item?.id || item.user_id !== context.user.id);
    if (invalid) return createApiError('Notification ownership mismatch', '通知数据归属异常，请重新登录后重试');
    return createApiResponse(fromDatabase(rows));
  } catch (error) {
    return createApiError(error, '加载通知失败');
  }
}

export async function markNotificationRead(id) {
  if (isMockMode()) return requestMock({ id, readAt: new Date().toISOString() });
  try {
    if (!id) return createApiError('Missing notification id', '缺少通知标识，无法标记已读');
    const context = await getAuthenticatedContext();
    const readAt = new Date().toISOString();
    const { data, error } = await context.supabase
      .from('notifications')
      .update({ read_at: readAt })
      .eq('id', id)
      .eq('user_id', context.user.id)
      .select('id, user_id, read_at')
      .maybeSingle();
    if (error) return createApiError(error, '标记通知已读失败');
    if (!data?.id || data.user_id !== context.user.id) return createApiError('Notification not updated', '通知不存在、无权限或已被删除');
    return createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '标记通知已读失败');
  }
}

export async function markAllNotificationsRead() {
  if (isMockMode()) return requestMock({ readAt: new Date().toISOString(), updatedIds: [] });
  try {
    const context = await getAuthenticatedContext();
    const readAt = new Date().toISOString();
    const { data, error } = await context.supabase
      .from('notifications')
      .update({ read_at: readAt })
      .eq('user_id', context.user.id)
      .is('read_at', null)
      .select('id, user_id');
    if (error) return createApiError(error, '全部标记已读失败');
    const rows = data || [];
    if (rows.some((item) => !item?.id || item.user_id !== context.user.id)) return createApiError('Notification ownership mismatch', '通知更新结果归属异常，请刷新后重试');
    return createApiResponse({ readAt, updatedIds: rows.map((item) => item.id) });
  } catch (error) {
    return createApiError(error, '全部标记已读失败');
  }
}