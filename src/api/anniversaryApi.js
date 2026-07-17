import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';

const mockAnniversaries = [
  { id: 'anniversary_001', title: '第一次见面', date: '2025-03-23', repeatType: 'yearly', description: '故事开始的那一天。', templateType: 'storybook', days: 428 },
  { id: 'anniversary_002', title: '第一次旅行', date: '2025-08-12', repeatType: 'yearly', description: '把夏天放进了同一张车票。', templateType: 'travel', days: 286 },
];

function buildPayload(payload = {}) {
  const result = {};
  if (payload.title !== undefined) result.title = payload.title?.trim();
  if (payload.date !== undefined) result.date = payload.date?.trim();
  if (payload.repeatType !== undefined || payload.repeatYearly !== undefined) {
    result.repeat_type = payload.repeatType || (payload.repeatYearly === false ? 'none' : 'yearly');
  }
  if (payload.description !== undefined || payload.note !== undefined) result.description = payload.description || payload.note || null;
  if (payload.templateType !== undefined || payload.type !== undefined) result.template_type = payload.templateType || payload.type || null;
  return result;
}

export async function getAnniversaries() {
  if (isMockMode()) return requestMock(mockAnniversaries);
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { data, error } = await context.supabase.from('anniversaries').select('*').eq('couple_id', coupleId).order('date');
    return error ? createApiError(error, '加载纪念日失败') : createApiResponse(fromDatabase(data || []));
  } catch (error) {
    return createApiError(error, '加载纪念日失败');
  }
}

export async function getAnniversaryList() { return getAnniversaries(); }

export async function getNextAnniversary() {
  if (isMockMode()) return requestMock(mockAnniversaries[0]);
  const result = await getAnniversaries();
  return result.success ? createApiResponse(result.data[0] || null) : result;
}

export async function createAnniversary(payload = {}) {
  if (isMockMode()) {
    return requestMock({ id: `anniversary_${Date.now()}`, title: payload.title?.trim() || '新的重要章节', date: payload.date?.trim() || '待设置日期', repeatType: payload.repeatType || 'yearly', description: payload.description?.trim() || payload.note?.trim() || '这是你们童话里值得记住的一章。', templateType: payload.templateType || 'storybook', days: 0, createdAt: new Date().toISOString() }, 400);
  }
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const values = buildPayload(payload);
    if (!values.title || !values.date) return createApiError('Missing anniversary fields', '请填写纪念日名称和日期');
    const { data, error } = await context.supabase.from('anniversaries').insert({ couple_id: coupleId, ...values }).select('*').single();
    return error ? createApiError(error, '创建纪念日失败') : createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '创建纪念日失败');
  }
}

export async function updateAnniversary(id, payload = {}) {
  if (isMockMode()) return requestMock({ id, ...payload, updatedAt: new Date().toISOString() }, 350);
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const values = buildPayload(payload);
    if (!Object.keys(values).length) return createApiError('Empty anniversary update', '没有可保存的纪念日修改');
    const { data, error } = await context.supabase.from('anniversaries').update(values).eq('id', id).eq('couple_id', coupleId).select('*').single();
    return error ? createApiError(error, '更新纪念日失败') : createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '更新纪念日失败');
  }
}

export async function deleteAnniversary(id) {
  if (isMockMode()) return requestMock({ id, deleted: true }, 300);
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const { error } = await context.supabase.from('anniversaries').delete().eq('id', id).eq('couple_id', coupleId);
    return error ? createApiError(error, '删除纪念日失败') : createApiResponse({ id, deleted: true });
  } catch (error) {
    return createApiError(error, '删除纪念日失败');
  }
}
