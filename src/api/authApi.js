import { createApiError, createApiResponse, getSupabaseClient, isMockMode, requestMock, withRequestTimeout } from './client';
import { fromDatabase } from './mappers';
import { mockUser } from './mockData';

const MAX_NICKNAME_LENGTH = 32;
const MAX_AVATAR_TEXT_LENGTH = 4;
const MAX_AVATAR_URL_LENGTH = 2048;

function normalizeEmail(email) {
  return String(email || '').trim().toLowerCase();
}

function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function normalizeSessionPayload(sessionPayload) {
  const session = sessionPayload?.session || null;
  const user = sessionPayload?.user || session?.user || null;
  return {
    session,
    user: user ? fromDatabase(user) : null,
    requiresEmailConfirmation: Boolean(user && !session),
  };
}

function validateAuthIdentity(data, expectedEmail, { requireSession = false } = {}) {
  const normalized = normalizeSessionPayload(data);
  const sessionUserId = normalized.session?.user?.id || null;
  const userId = normalized.user?.id || null;
  const returnedEmail = normalizeEmail(normalized.user?.email || normalized.session?.user?.email);
  if (!userId) return createApiError('Missing auth user', '认证结果缺少用户信息，请重试');
  if (requireSession && !normalized.session) return createApiError('Missing auth session', '登录未返回有效会话，请重试');
  if (normalized.session && sessionUserId !== userId) return createApiError('Auth user mismatch', '认证会话与用户信息不匹配，请重新登录');
  if (expectedEmail && returnedEmail !== expectedEmail) return createApiError('Auth email mismatch', '认证结果与提交邮箱不匹配，请重新登录');
  return createApiResponse(normalized, { requiresEmailConfirmation: normalized.requiresEmailConfirmation });
}

function normalizeAvatarUrl(value) {
  if (value === undefined || value === null || value === '') return null;
  const url = String(value).trim();
  if (!url || url.length > MAX_AVATAR_URL_LENGTH) return null;
  try {
    const parsed = new URL(url);
    return parsed.protocol === 'https:' || parsed.protocol === 'http:' ? url : null;
  } catch {
    return null;
  }
}

function normalizeSignupProfile(profile = {}) {
  const nickname = String(profile.nickname || '').trim();
  if (nickname.length > MAX_NICKNAME_LENGTH) return { error: createApiError('Nickname too long', `昵称最多 ${MAX_NICKNAME_LENGTH} 个字符`) };
  const avatarText = String(profile.avatarText || profile.avatar_text || '').trim();
  if (avatarText.length > MAX_AVATAR_TEXT_LENGTH) return { error: createApiError('Invalid avatar text', `头像文字最多 ${MAX_AVATAR_TEXT_LENGTH} 个字符`) };
  const rawAvatarUrl = profile.avatarUrl ?? profile.avatar_url ?? null;
  const avatarUrl = normalizeAvatarUrl(rawAvatarUrl);
  if (rawAvatarUrl && !avatarUrl) return { error: createApiError('Invalid avatar URL', '头像链接必须是有效的 HTTP 或 HTTPS 地址') };
  return {
    data: {
      ...(nickname ? { nickname } : {}),
      ...(avatarText ? { avatar_text: avatarText } : {}),
      ...(avatarUrl ? { avatar_url: avatarUrl } : {}),
    },
  };
}

export async function getCurrentSession() {
  if (isMockMode()) {
    return requestMock({
      session: { access_token: 'mock_access_token', user: mockUser },
      user: mockUser,
      requiresEmailConfirmation: false,
    });
  }
  try {
    const supabase = getSupabaseClient();
    const { data: sessionData, error: sessionError } = await supabase.auth.getSession();
    if (sessionError) return createApiError(sessionError, '获取登录状态失败');
    const session = sessionData?.session || null;
    if (!session) return createApiResponse({ session: null, user: null, requiresEmailConfirmation: false });

    const { data: userData, error: userError } = await withRequestTimeout(
      supabase.auth.getUser(),
      4000,
      '登录状态校验超时，请检查网络后重试',
    );
    if (userError) return createApiError(userError, '登录状态已失效，请重新登录');
    const verifiedUser = userData?.user || null;
    if (!verifiedUser?.id || verifiedUser.id !== session.user?.id) {
      return createApiError('Session user mismatch', '登录状态与当前账号不匹配，请重新登录');
    }
    return createApiResponse(normalizeSessionPayload({ session, user: verifiedUser }));
  } catch (error) {
    return createApiError(error, '获取登录状态失败');
  }
}

export async function signInWithEmailPassword(email, password) {
  const normalizedEmail = normalizeEmail(email);
  if (!validateEmail(normalizedEmail)) return createApiError('Invalid email', '请输入有效邮箱');
  if (String(password || '').length < 6) return createApiError('Invalid password', '密码至少需要 6 位');
  if (isMockMode()) {
    return requestMock({
      session: { access_token: 'mock_access_token', user: { ...mockUser, email: normalizedEmail } },
      user: { ...mockUser, email: normalizedEmail },
      requiresEmailConfirmation: false,
    }, 500);
  }
  try {
    const supabase = getSupabaseClient();
    const { data, error } = await supabase.auth.signInWithPassword({ email: normalizedEmail, password });
    if (error) return createApiError(error, '邮箱、密码或邮箱验证状态不正确');
    return validateAuthIdentity(data, normalizedEmail, { requireSession: true });
  } catch (error) {
    return createApiError(error, '登录失败，请稍后再试');
  }
}

export async function signUpWithEmailPassword(email, password, profile = {}) {
  const normalizedEmail = normalizeEmail(email);
  if (!validateEmail(normalizedEmail)) return createApiError('Invalid email', '请输入有效邮箱');
  if (String(password || '').length < 6) return createApiError('Invalid password', '密码至少需要 6 位');
  const normalizedProfile = normalizeSignupProfile(profile);
  if (normalizedProfile.error) return normalizedProfile.error;
  if (isMockMode()) {
    const user = { ...mockUser, email: normalizedEmail, ...normalizedProfile.data };
    return requestMock({ session: { access_token: 'mock_access_token', user }, user, requiresEmailConfirmation: false }, 600);
  }
  try {
    const supabase = getSupabaseClient();
    const { data, error } = await supabase.auth.signUp({
      email: normalizedEmail,
      password,
      options: { data: normalizedProfile.data },
    });
    if (error) return createApiError(error, '注册失败，请检查邮箱或密码');
    return validateAuthIdentity(data, normalizedEmail);
  } catch (error) {
    return createApiError(error, '注册失败，请稍后再试');
  }
}

export async function signInWithOtp(email) {
  const normalizedEmail = normalizeEmail(email);
  if (!validateEmail(normalizedEmail)) return createApiError('Invalid email', '请输入有效邮箱');
  if (isMockMode()) return requestMock({ email: normalizedEmail, sent: true, message: 'Mock 模式已模拟发送登录邮件' }, 500);
  try {
    const supabase = getSupabaseClient();
    const { data, error } = await supabase.auth.signInWithOtp({ email: normalizedEmail, options: { shouldCreateUser: true } });
    return error ? createApiError(error, '发送登录邮件失败') : createApiResponse({ ...data, email: normalizedEmail, sent: true });
  } catch (error) {
    return createApiError(error, '发送登录邮件失败');
  }
}

export async function signOut() {
  if (isMockMode()) return requestMock({ signedOut: true }, 300);
  try {
    const supabase = getSupabaseClient();
    const { error } = await supabase.auth.signOut();
    return error ? createApiError(error, '退出登录失败') : createApiResponse({ signedOut: true });
  } catch (error) {
    return createApiError(error, '退出登录失败');
  }
}

export function subscribeToAuthState(callback) {
  if (isMockMode()) return () => {};
  const supabase = getSupabaseClient();
  const { data } = supabase.auth.onAuthStateChange((event, session) => {
    callback({ event, session, user: session?.user ? fromDatabase(session.user) : null });
  });
  return () => data.subscription.unsubscribe();
}

export async function resetPassword(email) {
  const normalizedEmail = normalizeEmail(email);
  if (!validateEmail(normalizedEmail)) return createApiError('Invalid email', '请输入有效邮箱');
  if (isMockMode()) return requestMock({ email: normalizedEmail, sent: true }, 400);
  try {
    const supabase = getSupabaseClient();
    const { error } = await supabase.auth.resetPasswordForEmail(normalizedEmail);
    return error ? createApiError(error, '发送重置邮件失败') : createApiResponse({ email: normalizedEmail, sent: true });
  } catch (error) {
    return createApiError(error, '发送重置邮件失败');
  }
}

export async function upsertProfile(profile = {}) {
  if (isMockMode()) return requestMock({ ...mockUser, ...profile }, 400);
  try {
    const supabase = getSupabaseClient();
    const { data: sessionData, error: sessionError } = await supabase.auth.getUser();
    if (sessionError) return createApiError(sessionError, '获取用户信息失败');
    const userId = sessionData?.user?.id;
    if (!userId) return createApiError('Missing user id', '当前用户未登录');
    const nickname = String(profile.nickname || sessionData.user.email || '童话收藏家').trim();
    if (!nickname) return createApiError('Missing nickname', '请输入昵称');
    if (nickname.length > MAX_NICKNAME_LENGTH) return createApiError('Nickname too long', `昵称最多 ${MAX_NICKNAME_LENGTH} 个字符`);
    const avatarText = String(profile.avatarText || profile.avatar_text || nickname.slice(0, 1) || '童').trim();
    if (!avatarText || avatarText.length > MAX_AVATAR_TEXT_LENGTH) return createApiError('Invalid avatar text', `头像文字需为 1-${MAX_AVATAR_TEXT_LENGTH} 个字符`);
    const rawAvatarUrl = profile.avatarUrl ?? profile.avatar_url ?? null;
    const avatarUrl = normalizeAvatarUrl(rawAvatarUrl);
    if (rawAvatarUrl && !avatarUrl) return createApiError('Invalid avatar URL', '头像链接必须是有效的 HTTP 或 HTTPS 地址');
    const payload = {
      id: userId,
      nickname,
      avatar_url: avatarUrl,
      avatar_text: avatarText,
    };
    const { data, error } = await supabase.from('profiles').upsert(payload, { onConflict: 'id' }).select('*').maybeSingle();
    if (error) return createApiError(error, '保存用户资料失败');
    if (!data?.id || data.id !== userId) return createApiError('Profile write mismatch', '用户资料保存结果与当前账号不匹配');
    return createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '保存用户资料失败');
  }
}
