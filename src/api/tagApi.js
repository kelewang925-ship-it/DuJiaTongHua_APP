import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';

const mockTags = [];
const validCategories = new Set(['心情', '地点', '纪念', 'AI']);

function normalizeCategory(value) {
  const category = typeof value === 'string' ? value.trim() : '';
  return validCategories.has(category) ? category : null;
}

export async function getTags() {
  if (isMockMode()) return requestMock(mockTags);
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { data, error } = await context.supabase.from('custom_tags').select('*').eq('couple_id', coupleId).order('created_at');
    return error ? createApiError(error, '加载标签失败') : createApiResponse(fromDatabase(data || []));
  } catch (error) {
    return createApiError(error, '加载标签失败');
  }
}

export async function createTag(payload = {}) {
  if (isMockMode()) return requestMock({ id: `tag_${Date.now()}`, ...payload });
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const name = payload.name?.trim();
    const category = normalizeCategory(payload.category);
    if (!name) return createApiError('Missing tag name', '请输入标签名称');
    if (!category) return createApiError('Invalid tag category', '请选择有效的标签分类');

    const values = {
      couple_id: coupleId,
      created_by: context.user.id,
      name,
      category,
    };
    if (payload.icon !== undefined && String(payload.icon).trim()) values.icon = String(payload.icon).trim();

    const { data, error } = await context.supabase.from('custom_tags').insert(values).select('*').single();
    if (error) return createApiError(error, '创建标签失败');
    if (!data?.id) return createApiError('Missing created tag', '标签创建结果无效，请刷新后重试');
    return createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '创建标签失败');
  }
}

export async function updateTag(id, payload = {}) {
  if (isMockMode()) return requestMock({ id, ...payload });
  try {
    if (!id) return createApiError('Missing tag id', '缺少标签标识，无法保存');
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const values = {};
    if (payload.name !== undefined) values.name = payload.name?.trim();
    if (payload.category !== undefined) {
      const category = normalizeCategory(payload.category);
      if (!category) return createApiError('Invalid tag category', '请选择有效的标签分类');
      values.category = category;
    }
    if (payload.icon !== undefined) values.icon = payload.icon ? String(payload.icon).trim() : null;
    if (values.name === '') return createApiError('Missing tag name', '请输入标签名称');
    if (!Object.keys(values).length) return createApiError('Empty tag update', '没有可保存的标签修改');
    const { data, error } = await context.supabase.from('custom_tags').update(values).eq('id', id).eq('couple_id', coupleId).select('*').maybeSingle();
    if (error) return createApiError(error, '更新标签失败');
    if (!data?.id) return createApiError('Tag not updated', '标签不存在、无权限或已被删除');
    return createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '更新标签失败');
  }
}

export async function deleteTag(id) {
  if (isMockMode()) return requestMock({ id, deleted: true });
  try {
    if (!id) return createApiError('Missing tag id', '缺少标签标识，无法删除');
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { data, error } = await context.supabase.from('custom_tags').delete().eq('id', id).eq('couple_id', coupleId).select('id').maybeSingle();
    if (error) return createApiError(error, '删除标签失败');
    if (!data?.id) return createApiError('Tag not deleted', '标签不存在、无权限或已被删除');
    return createApiResponse({ id: data.id, deleted: true });
  } catch (error) {
    return createApiError(error, '删除标签失败');
  }
}
