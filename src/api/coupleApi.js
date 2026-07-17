import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { mockCouple, mockUser } from './mockData';
import { fromDatabase } from './mappers';

const mockTimeline = [
  { id: 'event_001', title: '她写下了一篇日记', time: '今天 21:04', type: 'diary' },
  { id: 'event_002', title: '你们新增了 6 张照片', time: '昨天 18:30', type: 'photo' },
  { id: 'event_003', title: '童话漫画生成完成', time: '5月23日', type: 'ai' },
];

export async function getCoupleInfo() {
  if (!isMockMode()) {
    try {
      const { supabase, user, couple } = await getAuthenticatedContext();
      if (!couple) return createApiResponse({ user: fromDatabase(user), couple: null, status: 'unbound' });
      const partnerId = couple.user_a === user.id ? couple.user_b : couple.user_a;
      const { data: profiles, error } = await supabase.from('profiles').select('*').in('id', [user.id, partnerId].filter(Boolean));
      if (error) return createApiError(error, '获取情侣资料失败');
      return createApiResponse({ user: fromDatabase(profiles?.find((item) => item.id === user.id) || user), partner: fromDatabase(profiles?.find((item) => item.id === partnerId) || null), couple: fromDatabase(couple), status: couple.status });
    } catch (error) { return createApiError(error, '获取情侣资料失败'); }
  }

  return requestMock({
    user: mockUser,
    couple: mockCouple,
    status: 'active',
  });
}

export async function getCurrentCouple() {
  return getCoupleInfo();
}

export async function createInviteCode() {
  if (!isMockMode()) {
    try {
      const { supabase } = await getAuthenticatedContext();
      const { data, error } = await supabase.rpc('create_couple_invite');
      if (error) return createApiError(error, '创建邀请码失败');
      const value = fromDatabase(data);
      return createApiResponse({ code: value.inviteCode, expiresAt: value.inviteExpiresAt, couple: value });
    } catch (error) { return createApiError(error, '创建邀请码失败'); }
  }

  return requestMock({
    code: 'FAIRY520',
    expiresIn: 3600,
    expiresAt: new Date(Date.now() + 3600 * 1000).toISOString(),
  });
}

export async function bindCouple(inviteCode) {
  if (!isMockMode()) {
    try {
      const { supabase } = await getAuthenticatedContext();
      const { data, error } = await supabase.rpc('bind_couple_by_invite', { p_invite_code: inviteCode });
      if (error) return createApiError(error, '邀请码无效、已过期或当前账号已绑定');
      return createApiResponse({ couple: fromDatabase(data), bound: true });
    } catch (error) { return createApiError(error, '情侣绑定失败'); }
  }

  return requestMock({
    inviteCode,
    coupleId: mockCouple.id,
    status: 'active',
    bound: true,
  }, 600);
}

export async function bindCoupleByCode(code) {
  return bindCouple(code);
}

export async function updateCoupleInfo(payload = {}) {
  if (!isMockMode()) {
    try {
      const context = await getAuthenticatedContext();
      const { supabase, coupleId } = context;
      if (!coupleId) return createApiError('Missing couple', '请先完成情侣绑定');
      requireCouple(context);
      const { data, error } = await supabase.rpc('update_couple_started_at', { p_started_at: payload.startedAt || payload.started_at || null });
      if (error) return createApiError(error, '保存情侣资料失败');
      return createApiResponse(fromDatabase(data));
    } catch (error) { return createApiError(error, '保存情侣资料失败'); }
  }

  return requestMock({
    ...mockCouple,
    ...payload,
    updatedAt: new Date().toISOString(),
  }, 400);
}

export async function getCoupleTimeline() {
  if (!isMockMode()) {
    return createApiResponse([], { derived: true });
  }

  return requestMock(mockTimeline);
}
