import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';

const validTargetTypes = new Set(['diary', 'photo']);

function normalizeTargetType(value) {
  const normalized = String(value || '').trim().toLowerCase();
  return validTargetTypes.has(normalized) ? normalized : null;
}

export async function getComments(targetType, targetId) {
  if (isMockMode()) return requestMock([]);
  try {
    const normalizedType = normalizeTargetType(targetType);
    const normalizedId = String(targetId || '').trim();
    if (!normalizedType || !normalizedId) return createApiError('Invalid comment target', '评论目标无效，请从具体日记或照片进入');
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { data, error } = await context.supabase
      .from('comments')
      .select('*,profiles:author_id(nickname,avatar_text,avatar_url)')
      .eq('couple_id', coupleId)
      .eq('target_type', normalizedType)
      .eq('target_id', normalizedId)
      .order('created_at', { ascending: false });
    return error ? createApiError(error, '加载评论失败') : createApiResponse(fromDatabase(data || []));
  } catch (error) {
    return createApiError(error, '加载评论失败');
  }
}

export async function createComment(payload = {}) {
  if (isMockMode()) return requestMock({ id: `comment_${Date.now()}`, ...payload, createdAt: new Date().toISOString() });
  try {
    const normalizedType = normalizeTargetType(payload.targetType);
    const normalizedId = String(payload.targetId || '').trim();
    const content = payload.content?.trim();
    if (!normalizedType || !normalizedId || !content) return createApiError('Missing comment fields', '评论目标或内容无效');
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { data, error } = await context.supabase.from('comments').insert({
      couple_id: coupleId,
      author_id: context.user.id,
      target_type: normalizedType,
      target_id: normalizedId,
      content,
    }).select('*,profiles:author_id(nickname,avatar_text,avatar_url)').single();
    if (error) return createApiError(error, '发送评论失败');
    if (!data?.id) return createApiError('Missing created comment', '评论发送结果无效，请刷新后确认');
    return createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '发送评论失败');
  }
}

export async function deleteComment(id) {
  if (isMockMode()) return requestMock({ id, deleted: true });
  try {
    if (!id) return createApiError('Missing comment id', '缺少评论标识，无法删除');
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { data, error } = await context.supabase.from('comments').delete().eq('id', id).eq('couple_id', coupleId).eq('author_id', context.user.id).select('id').maybeSingle();
    if (error) return createApiError(error, '删除评论失败');
    if (!data?.id) return createApiError('Comment not deleted', '评论不存在、无权限或已被删除');
    return createApiResponse({ id: data.id, deleted: true });
  } catch (error) {
    return createApiError(error, '删除评论失败');
  }
}
