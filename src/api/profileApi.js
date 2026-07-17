import {
  createApiError,
  createApiResponse,
  getAuthenticatedContext,
  isMockMode,
  requestMock,
} from './client';
import { compactPayload, fromDatabase } from './mappers';
import { mockUser } from './mockData';

export async function getProfile() {
  if (isMockMode()) return requestMock(mockUser);
  try {
    const context = await getAuthenticatedContext();
    const { data, error } = await context.supabase
      .from('profiles')
      .select('*')
      .eq('id', context.user.id)
      .single();
    return error ? createApiError(error, '加载个人资料失败') : createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '加载个人资料失败');
  }
}

export async function updateProfile(payload = {}) {
  if (isMockMode()) {
    return requestMock({
      ...mockUser,
      ...payload,
      nickname: payload.nickname?.trim() || mockUser.nickname,
      updatedAt: new Date().toISOString(),
    });
  }

  try {
    const context = await getAuthenticatedContext();
    const updates = compactPayload({
      nickname: payload.nickname?.trim(),
      avatarUrl: payload.avatarUrl,
      avatarText: payload.avatarText,
    });
    if (!updates.nickname && !updates.avatar_url && !updates.avatar_text) {
      return createApiError('Empty profile update', '没有需要保存的资料修改');
    }
    const { data, error } = await context.supabase
      .from('profiles')
      .update(updates)
      .eq('id', context.user.id)
      .select('*')
      .single();
    return error ? createApiError(error, '保存个人资料失败') : createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '保存个人资料失败');
  }
}
