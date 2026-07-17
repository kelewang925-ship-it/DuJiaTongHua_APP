import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';

export async function getComments(targetType, targetId) {
  if (isMockMode()) return requestMock([]);
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { data, error } = await context.supabase
      .from('comments')
      .select('*,profiles:author_id(nickname,avatar_text,avatar_url)')
      .eq('couple_id', coupleId)
      .eq('target_type', targetType)
      .eq('target_id', targetId)
      .order('created_at');
    return error ? createApiError(error, '加载评论失败') : createApiResponse(fromDatabase(data || []));
  } catch (error) {
    return createApiError(error, '加载评论失败');
  }
}

export async function createComment(payload = {}) {
  if (isMockMode()) return requestMock({ id: `comment_${Date.now()}`, ...payload, createdAt: new Date().toISOString() });
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const content = payload.content?.trim();
    if (!payload.targetType || !payload.targetId || !content) return createApiError('Missing comment fields', '请输入评论内容');
    const { data, error } = await context.supabase.from('comments').insert({
      couple_id: coupleId,
      author_id: context.user.id,
      target_type: payload.targetType,
      target_id: payload.targetId,
      content,
    }).select('*').single();
    return error ? createApiError(error, '发送评论失败') : createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '发送评论失败');
  }
}

export async function deleteComment(id) {
  if (isMockMode()) return requestMock({ id, deleted: true });
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { error } = await context.supabase.from('comments').delete().eq('id', id).eq('couple_id', coupleId).eq('author_id', context.user.id);
    return error ? createApiError(error, '删除评论失败') : createApiResponse({ id, deleted: true });
  } catch (error) {
    return createApiError(error, '删除评论失败');
  }
}
