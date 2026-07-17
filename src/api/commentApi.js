import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';

export async function getComments(targetType, targetId) {
  if (isMockMode()) return requestMock([]);
  try { const c = await getAuthenticatedContext(); requireCouple(c); const { data, error } = await c.supabase.from('comments').select('*,profiles:author_id(nickname,avatar_text,avatar_url)').eq('couple_id', c.coupleId).eq('target_type', targetType).eq('target_id', targetId).order('created_at'); return error ? createApiError(error) : createApiResponse(fromDatabase(data || [])); } catch (error) { return createApiError(error); }
}
export async function createComment(payload) {
  if (isMockMode()) return requestMock({ id: `comment_${Date.now()}`, ...payload, createdAt: new Date().toISOString() });
  try { const c = await getAuthenticatedContext(); requireCouple(c); const { data, error } = await c.supabase.from('comments').insert({ couple_id: c.coupleId, author_id: c.user.id, target_type: payload.targetType, target_id: payload.targetId, content: payload.content.trim() }).select('*').single(); return error ? createApiError(error) : createApiResponse(fromDatabase(data)); } catch (error) { return createApiError(error); }
}
export async function deleteComment(id) { if (isMockMode()) return requestMock({ id, deleted: true }); try { const { supabase } = await getAuthenticatedContext(); const { error } = await supabase.from('comments').delete().eq('id', id); return error ? createApiError(error) : createApiResponse({ id, deleted: true }); } catch (error) { return createApiError(error); } }
