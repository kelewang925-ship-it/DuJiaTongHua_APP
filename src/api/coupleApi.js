import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { mockCouple, mockUser } from './mockData';
import { fromDatabase } from './mappers';

const mockTimeline = [
  { id: 'event_001', title: '她写下了一篇日记', time: '今天 21:04', type: 'diary' },
  { id: 'event_002', title: '你们新增了 6 张照片', time: '昨天 18:30', type: 'photo' },
  { id: 'event_003', title: '童话漫画生成完成', time: '5月23日', type: 'ai' },
];

export async function getCoupleInfo() {
  if (isMockMode()) return requestMock({ user: mockUser, couple: mockCouple, status: 'active' });
  try {
    const { supabase, user, couple } = await getAuthenticatedContext();
    if (!couple) return createApiResponse({ user: fromDatabase(user), partner: null, couple: null, status: 'unbound' });
    const partnerId = couple.user_a === user.id ? couple.user_b : couple.user_a;
    const { data: profiles, error } = await supabase.from('profiles').select('*').in('id', [user.id, partnerId].filter(Boolean));
    if (error) return createApiError(error, '获取情侣资料失败');
    return createApiResponse({
      user: fromDatabase(profiles?.find((item) => item.id === user.id) || user),
      partner: fromDatabase(profiles?.find((item) => item.id === partnerId) || null),
      couple: fromDatabase(couple),
      status: couple.status,
    });
  } catch (error) {
    return createApiError(error, '获取情侣资料失败');
  }
}

export async function getCurrentCouple() { return getCoupleInfo(); }

export async function createInviteCode() {
  if (isMockMode()) return requestMock({ code: 'FAIRY520', expiresIn: 3600, expiresAt: new Date(Date.now() + 3600 * 1000).toISOString() });
  try {
    const { supabase } = await getAuthenticatedContext();
    const { data, error } = await supabase.rpc('create_couple_invite');
    if (error) return createApiError(error, '创建邀请码失败');
    const value = fromDatabase(data);
    if (!value?.inviteCode) return createApiError('Missing invite code', '邀请码创建失败，请稍后重试');
    return createApiResponse({ code: value.inviteCode, expiresAt: value.inviteExpiresAt, couple: value });
  } catch (error) {
    return createApiError(error, '创建邀请码失败');
  }
}

export async function bindCouple(inviteCode) {
  const normalizedCode = String(inviteCode || '').trim().toUpperCase();
  if (!normalizedCode) return createApiError('Missing invite code', '请输入邀请码');
  if (isMockMode()) return requestMock({ inviteCode: normalizedCode, coupleId: mockCouple.id, status: 'active', bound: true }, 600);
  try {
    const { supabase } = await getAuthenticatedContext();
    const { data, error } = await supabase.rpc('bind_couple_by_invite', { p_invite_code: normalizedCode });
    if (error) return createApiError(error, '邀请码无效、已过期、属于本人或当前账号已绑定');
    return createApiResponse({ couple: fromDatabase(data), bound: true });
  } catch (error) {
    return createApiError(error, '情侣绑定失败');
  }
}

export async function bindCoupleByCode(code) { return bindCouple(code); }

export async function updateCoupleInfo(payload = {}) {
  if (isMockMode()) return requestMock({ ...mockCouple, ...payload, updatedAt: new Date().toISOString() }, 400);
  try {
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const startedAt = payload.startedAt || payload.started_at;
    if (!startedAt) return createApiError('Missing started date', '请选择恋爱开始日期');
    const { data, error } = await context.supabase.rpc('update_couple_started_at', { p_started_at: startedAt });
    return error ? createApiError(error, '保存情侣资料失败') : createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '保存情侣资料失败');
  }
}

export async function getCoupleTimeline() {
  if (isMockMode()) return requestMock(mockTimeline);
  return createApiResponse([], { derived: true, source: 'store.records+anniversaries' });
}
