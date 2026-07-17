import { createApiError, createApiResponse, getSupabaseClient, isMockMode, requestMock } from './client';
import { fromDatabase } from './mappers';
import { mockUser } from './mockData';

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
    const { data, error } = await supabase.auth.getSession();
    return error ? createApiError(error, '获取登录状态失败') : createApiResponse(normalizeSessionPayload(data));
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
    return error ? createApiError(error, '邮箱、密码或邮箱验证状态不正确') : createApiResponse(normalizeSessionPayload(data));
  } catch (error) {
    return createApiError(error, '登录失败，请稍后再试');
  }
}

export async function signUpWithEmailPassword(email, password, profile = {}) {
  const normalizedEmail = normalizeEmail(email);
  if (!validateEmail(normalizedEmail)) return createApiError('Invalid email', '请输入有效邮箱');
  if (String(password || '').length < 6) return createApiError('Invalid password', '密码至少需要 6 位');
  if (isMockMode()) {
    const user = { ...mockUser, email: normalizedEmail, ...profile };
    return requestMock({ session: { access_token: 'mock_access_token', user }, user, requiresEmailConfirmation: false }, 600);
  }
  try {
    const supabase = getSupabaseClient();
    const { data, error } = await supabase.auth.signUp({
      email: normalizedEmail,
      password,
      options: { data: profile },
    });
    if (error) return createApiError(error, '注册失败，请检查邮箱或密码');
    const normalized = normalizeSessionPayload(data);
    return createApiResponse(normalized, { requiresEmailConfirmation: normalized.requiresEmailConfirmation });
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
    const payload = {
      id: userId,
      nickname,
      avatar_url: profile.avatarUrl ?? profile.avatar_url ?? null,
      avatar_text: profile.avatarText || profile.avatar_text || nickname.slice(0, 1) || '童',
    };
    const { data, error } = await supabase.from('profiles').upsert(payload, { onConflict: 'id' }).select('*').single();
    return error ? createApiError(error, '保存用户资料失败') : createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '保存用户资料失败');
  }
}
