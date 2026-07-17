import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';

const mockAnniversaries = [
  {
    id: 'anniversary_001',
    title: '第一次见面',
    date: '2025-03-23',
    repeatType: 'yearly',
    description: '故事开始的那一天。',
    templateType: 'storybook',
    days: 428,
  },
  {
    id: 'anniversary_002',
    title: '第一次旅行',
    date: '2025-08-12',
    repeatType: 'yearly',
    description: '把夏天放进了同一张车票。',
    templateType: 'travel',
    days: 286,
  },
];

export async function getAnniversaries() {
  if (!isMockMode()) {
    try { const { supabase, coupleId } = await getAuthenticatedContext(); requireCouple({ coupleId }); const { data, error } = await supabase.from('anniversaries').select('*').eq('couple_id', coupleId).order('date'); return error ? createApiError(error, '加载纪念日失败') : createApiResponse(fromDatabase(data)); } catch (error) { return createApiError(error, '加载纪念日失败'); }
  }

  return requestMock(mockAnniversaries);
}

export async function getAnniversaryList() {
  return getAnniversaries();
}

export async function getNextAnniversary() {
  if (!isMockMode()) {
    const result = await getAnniversaries(); return result.success ? createApiResponse(result.data[0] || null) : result;
  }

  return requestMock(mockAnniversaries[0]);
}

export async function createAnniversary(payload = {}) {
  if (!isMockMode()) {
    try { const context = await getAuthenticatedContext(); const coupleId = requireCouple(context); const { data, error } = await context.supabase.from('anniversaries').insert({ couple_id: coupleId, title: payload.title, date: payload.date, repeat_type: payload.repeatType || (payload.repeatYearly === false ? 'none' : 'yearly'), description: payload.description || payload.note || null, template_type: payload.templateType || payload.type || null }).select('*').single(); return error ? createApiError(error, '创建纪念日失败') : createApiResponse(fromDatabase(data)); } catch (error) { return createApiError(error, '创建纪念日失败'); }
  }

  const anniversary = {
    id: `anniversary_${Date.now()}`,
    title: payload.title?.trim() || '新的重要章节',
    date: payload.date?.trim() || '待设置日期',
    repeatType: payload.repeatType || 'yearly',
    description: payload.description?.trim() || payload.note?.trim() || '这是你们童话里值得记住的一章。',
    templateType: payload.templateType || 'storybook',
    days: 0,
    createdAt: new Date().toISOString(),
  };

  return requestMock(anniversary, 400);
}

export async function updateAnniversary(id, payload = {}) {
  if (!isMockMode()) {
    try { const { supabase } = await getAuthenticatedContext(); const { data, error } = await supabase.from('anniversaries').update({ title: payload.title, date: payload.date, repeat_type: payload.repeatType || (payload.repeatYearly === false ? 'none' : undefined), description: payload.description || payload.note, template_type: payload.templateType || payload.type }).eq('id', id).select('*').single(); return error ? createApiError(error, '更新纪念日失败') : createApiResponse(fromDatabase(data)); } catch (error) { return createApiError(error, '更新纪念日失败'); }
  }

  return requestMock({
    id,
    ...payload,
    updatedAt: new Date().toISOString(),
  }, 350);
}

export async function deleteAnniversary(id) {
  if (!isMockMode()) {
    try { const { supabase } = await getAuthenticatedContext(); const { error } = await supabase.from('anniversaries').delete().eq('id', id); return error ? createApiError(error, '删除纪念日失败') : createApiResponse({ id, deleted: true }); } catch (error) { return createApiError(error, '删除纪念日失败'); }
  }

  return requestMock({ id, deleted: true }, 300);
}
