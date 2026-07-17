import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';

const validTargetTypes = new Set(['diary', 'photo']);
const targetTables = { diary: 'diaries', photo: 'photos' };
const MAX_COMMENT_LENGTH = 1000;

function normalizeTargetType(value) {
  const normalized = String(value || '').trim().toLowerCase();
  return validTargetTypes.has(normalized) ? normalized : null;
}

function normalizeComment(value, { coupleId, targetType, targetId } = {}) {
  const comment = fromDatabase(value);
  if (!comment?.id || comment.coupleId !== coupleId) return null;
  if (targetType && comment.targetType !== targetType) return null;
  if (targetId && comment.targetId !== targetId) return null;
  return comment;
}

async function verifyCommentTarget(context, coupleId, targetType, targetId) {
  const table = targetTables[targetType];
  const { data, error } = await context.supabase
    .from(table)
    .select('id,couple_id')
    .eq('id', targetId)
    .eq('couple_id', coupleId)
    .maybeSingle();
  if (error) return createApiError(error, '验证评论目标失败');
  if (!data?.id || data.couple_id !== coupleId) return createApiError('Comment target unavailable', '评论目标不存在、无权限或已被删除');
  return createApiResponse({ id: data.id, type: targetType });
}

export async function getComments(targetType, targetId) {
  if (isMockMode()) return requestMock([]);
  try {
    const normalizedType = normalizeTargetType(targetType);
    const normalizedId = String(targetId || '').trim();
    if (!normalizedType || !normalizedId) return createApiError('Invalid comment target', '评论目标无效，请从具体日记或照片进入');
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const targetResult = await verifyCommentTarget(context, coupleId, normalizedType, normalizedId);
    if (!targetResult.success) return targetResult;
    const { data, error } = await context.supabase
      .from('comments')
      .select('*,profiles:author_id(nickname,avatar_text,avatar_url)')
      .eq('couple_id', coupleId)
      .eq('target_type', normalizedType)
      .eq('target_id', normalizedId)
      .order('created_at', { ascending: false });
    if (error) return createApiError(error, '加载评论失败');
    const comments = (data || []).map((item) => normalizeComment(item, { coupleId, targetType: normalizedType, targetId: normalizedId }));
    if (comments.some((item) => !item)) return createApiError('Invalid comment ownership', '评论数据归属异常，请刷新后重试');
    return createApiResponse(comments);
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
    if (content.length > MAX_COMMENT_LENGTH) return createApiError('Comment too long', `评论最多 ${MAX_COMMENT_LENGTH} 个字符`);
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const targetResult = await verifyCommentTarget(context, coupleId, normalizedType, normalizedId);
    if (!targetResult.success) return targetResult;
    const { data, error } = await context.supabase.from('comments').insert({
      couple_id: coupleId,
      author_id: context.user.id,
      target_type: normalizedType,
      target_id: normalizedId,
      content,
    }).select('*,profiles:author_id(nickname,avatar_text,avatar_url)').maybeSingle();
    if (error) return createApiError(error, '发送评论失败');
    const comment = normalizeComment(data, { coupleId, targetType: normalizedType, targetId: normalizedId });
    if (!comment?.id || comment.authorId !== context.user.id) return createApiError('Comment creation mismatch', '评论发送结果与当前账号或目标不匹配');
    return createApiResponse(comment);
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
    const { data, error } = await context.supabase.from('comments').delete().eq('id', id).eq('couple_id', coupleId).eq('author_id', context.user.id).select('id,couple_id,author_id').maybeSingle();
    if (error) return createApiError(error, '删除评论失败');
    if (!data?.id || data.couple_id !== coupleId || data.author_id !== context.user.id) return createApiError('Comment not deleted', '评论不存在、无权限或已被删除');
    return createApiResponse({ id: data.id, deleted: true });
  } catch (error) {
    return createApiError(error, '删除评论失败');
  }
}
