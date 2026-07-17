import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';

const mockTags = [];
export async function getTags() {
  if (isMockMode()) return requestMock(mockTags);
  try { const c = await getAuthenticatedContext(); requireCouple(c); const { data, error } = await c.supabase.from('custom_tags').select('*').eq('couple_id', c.coupleId).order('created_at'); return error ? createApiError(error) : createApiResponse(fromDatabase(data || [])); } catch (error) { return createApiError(error); }
}
export async function createTag(payload) {
  if (isMockMode()) return requestMock({ id: `tag_${Date.now()}`, ...payload });
  try { const c = await getAuthenticatedContext(); requireCouple(c); const { data, error } = await c.supabase.from('custom_tags').insert({ couple_id: c.coupleId, created_by: c.user.id, name: payload.name.trim(), category: payload.category || '心情', icon: payload.icon || 'pricetag-outline' }).select('*').single(); return error ? createApiError(error) : createApiResponse(fromDatabase(data)); } catch (error) { return createApiError(error); }
}
export async function updateTag(id, payload) { if (isMockMode()) return requestMock({ id, ...payload }); try { const { supabase } = await getAuthenticatedContext(); const { data, error } = await supabase.from('custom_tags').update({ name: payload.name, category: payload.category, icon: payload.icon }).eq('id', id).select('*').single(); return error ? createApiError(error) : createApiResponse(fromDatabase(data)); } catch (error) { return createApiError(error); } }
export async function deleteTag(id) { if (isMockMode()) return requestMock({ id, deleted: true }); try { const { supabase } = await getAuthenticatedContext(); const { error } = await supabase.from('custom_tags').delete().eq('id', id); return error ? createApiError(error) : createApiResponse({ id, deleted: true }); } catch (error) { return createApiError(error); } }
