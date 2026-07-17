import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { mockCouple, mockUser } from './mockData';
import { fromDatabase } from './mappers';

const mockTimeline = [
  { id: 'event_001', title: '她写下了一篇日记', time: '今天 21:04', type: 'diary' },
  { id: 'event_002', title: '你们新增了 6 张照片', time: '昨天 18:30', type: 'photo' },
  { id: 'event_003', title: '童话漫画生成完成', time: '5月23日', type: 'ai' },
];

function isValidDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(value || ''))) return false;
  const date = new Date(`${value}T00:00:00`);
  return !Number.isNaN(date.getTime()) && date.toISOString().slice(0, 10) === value;
}

function normalizeInviteCode(value) {
  const code = String(value || '').trim().toUpperCase();
  return /^[A-Z0-9]{4,32}$/.test(code) ? code : null;
}

function isActiveCouple(couple) {
  return Boolean(couple?.id && couple.status === 'active');
}

function isCoupleMember(couple, userId) {
  const userA = couple?.userA || couple?.user_a;
  const userB = couple?.userB || couple?.user_b;
  return Boolean(userId && (userA === userId || userB === userId));
}

export async function getCoupleInfo() {
  if (isMockMode()) return requestMock({ user: mockUser, couple: mockCouple, status: 'active' });
  try {
    const { supabase, user, couple } = await getAuthenticatedContext();
    if (!user?.id) return createApiError('Missing authenticated user', '当前登录用户信息无效');
    if (!couple) return createApiResponse({ user: fromDatabase(user), partner: null, couple: null, status: 'unbound' });
    if (!isActiveCouple(couple) || !isCoupleMember(couple, user.id)) {
      return createApiResponse({
        user: fromDatabase(user),
        partner: null,
        couple: null,
        status: couple.status || 'inactive',
      }, { relationshipIsolated: true });
    }
    const partnerId = couple.user_a === user.id ? couple.user_b : couple.user_a;
    if (!partnerId) return createApiError('Missing partner id', '情侣关系缺少伴侣信息，请联系支持');
    const { data: profiles, error } = await supabase.from('profiles').select('*').in('id', [user.id, partnerId]);
    if (error) return createApiError(error, '获取情侣资料失败');
    const ownProfile = profiles?.find((item) => item.id === user.id) || null;
    const partnerProfile = profiles?.find((item) => item.id === partnerId) || null;
    return createApiResponse({
      user: fromDatabase(ownProfile || user),
      partner: fromDatabase(partnerProfile),
      couple: fromDatabase(couple),
      status: couple.status,
      profileComplete: Boolean(ownProfile),
      partnerProfileAvailable: Boolean(partnerProfile),
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
    const code = normalizeInviteCode(value?.inviteCode);
    if (!code) return createApiError('Missing invite code', '邀请码创建结果无效，请稍后重试');
    const expiresAt = value?.inviteExpiresAt || null;
    if (expiresAt && Number.isNaN(new Date(expiresAt).getTime())) return createApiError('Invalid invite expiry', '邀请码有效期数据无效，请重新生成');
    return createApiResponse({ code, expiresAt, couple: value });
  } catch (error) {
    return createApiError(error, '创建邀请码失败');
  }
}

export async function bindCouple(inviteCode) {
  const normalizedCode = normalizeInviteCode(inviteCode);
  if (!normalizedCode) return createApiError('Invalid invite code', '请输入有效的邀请码');
  if (isMockMode()) return requestMock({ inviteCode: normalizedCode, coupleId: mockCouple.id, status: 'active', bound: true }, 600);
  try {
    const { supabase, user } = await getAuthenticatedContext();
    const { data, error } = await supabase.rpc('bind_couple_by_invite', { p_invite_code: normalizedCode });
    if (error) return createApiError(error, '邀请码无效、已过期、属于本人或当前账号已绑定');
    const couple = fromDatabase(data);
    if (!couple?.id) return createApiError('Missing bound couple', '绑定结果无效，请刷新情侣资料后确认');
    if (couple.status !== 'active') return createApiError('Inactive couple binding', '情侣关系尚未生效，请稍后重试');
    if (!isCoupleMember(couple, user?.id)) return createApiError('Binding membership mismatch', '绑定结果与当前账号不匹配，请重新登录后确认');
    return createApiResponse({ couple, bound: true });
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
    const startedAt = String(payload.startedAt || payload.started_at || '').trim();
    if (!isValidDate(startedAt)) return createApiError('Invalid started date', '请选择有效的恋爱开始日期');
    const { data, error } = await context.supabase.rpc('update_couple_started_at', { p_started_at: startedAt });
    if (error) return createApiError(error, '保存情侣资料失败');
    const value = fromDatabase(data);
    if (!value?.id || !isCoupleMember(value, context.user.id)) return createApiError('Couple not updated', '情侣资料不存在、无权限或未成功保存');
    return createApiResponse(value);
  } catch (error) {
    return createApiError(error, '保存情侣资料失败');
  }
}

export async function getCoupleTimeline() {
  if (isMockMode()) return requestMock(mockTimeline);
  return createApiResponse([], { derived: true, source: 'store.records+anniversaries' });
}
