import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';

const mockTags = [];
const validCategories = new Set(['心情', '地点', '纪念', 'AI']);
const MAX_TAG_NAME_LENGTH = 32;
const MAX_TAG_ICON_LENGTH = 64;

function normalizeCategory(value) {
  const category = typeof value === 'string' ? value.trim() : '';
  return validCategories.has(category) ? category : null;
}

function normalizeTag(value, coupleId) {
  const tag = fromDatabase(value);
  if (!tag?.id || tag.coupleId !== coupleId) return null;
  return tag;
}

function normalizeTagName(value) {
  const name = String(value || '').trim();
  return name && name.length <= MAX_TAG_NAME_LENGTH ? name : null;
}

function normalizeTagIcon(value) {
  if (value === undefined) return undefined;
  if (value === null || value === '') return null;
  const icon = String(value).trim();
  return icon && icon.length <= MAX_TAG_ICON_LENGTH ? icon : null;
}

export async function getTags() {
  if (isMockMode()) return requestMock(mockTags);
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { data, error } = await context.supabase.from('custom_tags').select('*').eq('couple_id', coupleId).order('created_at');
    if (error) return createApiError(error, '加载标签失败');
    const tags = (data || []).map((item) => normalizeTag(item, coupleId));
    if (tags.some((item) => !item)) return createApiError('Invalid tag ownership', '标签数据归属异常，请刷新后重试');
    return createApiResponse(tags);
  } catch (error) {
    return createApiError(error, '加载标签失败');
  }
}

export async function createTag(payload = {}) {
  if (isMockMode()) return requestMock({ id: `tag_${Date.now()}`, ...payload });
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const name = normalizeTagName(payload.name);
    const category = normalizeCategory(payload.category);
    const icon = normalizeTagIcon(payload.icon);
    if (!name) return createApiError('Invalid tag name', `请输入 1-${MAX_TAG_NAME_LENGTH} 个字符的标签名称`);
    if (!category) return createApiError('Invalid tag category', '请选择有效的标签分类');
    if (payload.icon !== undefined && icon === null && payload.icon !== null && payload.icon !== '') return createApiError('Invalid tag icon', '标签图标格式无效');

    const values = { couple_id: coupleId, created_by: context.user.id, name, category };
    if (icon !== undefined) values.icon = icon;

    const { data, error } = await context.supabase.from('custom_tags').insert(values).select('*').maybeSingle();
    if (error) return createApiError(error, '创建标签失败');
    const tag = normalizeTag(data, coupleId);
    if (!tag || tag.createdBy !== context.user.id) return createApiError('Tag creation mismatch', '标签创建结果与当前情侣空间或账号不匹配');
    return createApiResponse(tag);
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
    if (payload.name !== undefined) {
      const name = normalizeTagName(payload.name);
      if (!name) return createApiError('Invalid tag name', `请输入 1-${MAX_TAG_NAME_LENGTH} 个字符的标签名称`);
      values.name = name;
    }
    if (payload.category !== undefined) {
      const category = normalizeCategory(payload.category);
      if (!category) return createApiError('Invalid tag category', '请选择有效的标签分类');
      values.category = category;
    }
    if (payload.icon !== undefined) {
      const icon = normalizeTagIcon(payload.icon);
      if (icon === null && payload.icon !== null && payload.icon !== '') return createApiError('Invalid tag icon', '标签图标格式无效');
      values.icon = icon;
    }
    if (!Object.keys(values).length) return createApiError('Empty tag update', '没有可保存的标签修改');
    const { data, error } = await context.supabase.from('custom_tags').update(values).eq('id', id).eq('couple_id', coupleId).select('*').maybeSingle();
    if (error) return createApiError(error, '更新标签失败');
    const tag = normalizeTag(data, coupleId);
    if (!tag) return createApiError('Tag not updated', '标签不存在、无权限或已被删除');
    return createApiResponse(tag);
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
    const { data, error } = await context.supabase.from('custom_tags').delete().eq('id', id).eq('couple_id', coupleId).select('id,couple_id').maybeSingle();
    if (error) return createApiError(error, '删除标签失败');
    if (!data?.id || data.couple_id !== coupleId) return createApiError('Tag not deleted', '标签不存在、无权限或已被删除');
    return createApiResponse({ id: data.id, deleted: true });
  } catch (error) {
    return createApiError(error, '删除标签失败');
  }
}
