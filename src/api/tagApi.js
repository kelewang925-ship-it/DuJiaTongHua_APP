import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';

const mockTags = [];

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
    if (!name) return createApiError('Missing tag name', '请输入标签名称');
    const { data, error } = await context.supabase.from('custom_tags').insert({
      couple_id: coupleId,
      created_by: context.user.id,
      name,
      category: payload.category || '心情',
      icon: payload.icon || 'pricetag-outline',
    }).select('*').single();
    return error ? createApiError(error, '创建标签失败') : createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '创建标签失败');
  }
}

export async function updateTag(id, payload = {}) {
  if (isMockMode()) return requestMock({ id, ...payload });
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const values = {};
    if (payload.name !== undefined) values.name = payload.name?.trim();
    if (payload.category !== undefined) values.category = payload.category;
    if (payload.icon !== undefined) values.icon = payload.icon;
    if (values.name === '') return createApiError('Missing tag name', '请输入标签名称');
    if (!Object.keys(values).length) return createApiError('Empty tag update', '没有可保存的标签修改');
    const { data, error } = await context.supabase.from('custom_tags').update(values).eq('id', id).eq('couple_id', coupleId).select('*').single();
    return error ? createApiError(error, '更新标签失败') : createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '更新标签失败');
  }
}

export async function deleteTag(id) {
  if (isMockMode()) return requestMock({ id, deleted: true });
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { error } = await context.supabase.from('custom_tags').delete().eq('id', id).eq('couple_id', coupleId);
    return error ? createApiError(error, '删除标签失败') : createApiResponse({ id, deleted: true });
  } catch (error) {
    return createApiError(error, '删除标签失败');
  }
}
