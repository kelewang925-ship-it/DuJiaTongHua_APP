import { createApiError, createApiResponse, getSupabaseClient, isMockMode, requestMock } from './client';
import { mockUser } from './mockData';

function normalizeSessionPayload(sessionPayload) {
  const session = sessionPayload?.session || null;
  const user = sessionPayload?.user || session?.user || null;

  return {
    session,
    user,
  };
}

export async function getCurrentSession() {
  if (isMockMode()) {
    return requestMock({
      session: {
        access_token: 'mock_access_token',
        user: mockUser,
      },
      user: mockUser,
    });
  }

  try {
    const supabase = getSupabaseClient();
    const { data, error } = await supabase.auth.getSession();
    if (error) return createApiError(error, '获取登录状态失败');
    return createApiResponse(normalizeSessionPayload(data));
  } catch (error) {
    return createApiError(error, '获取登录状态失败');
  }
}

export async function signInWithEmailPassword(email, password) {
  if (isMockMode()) {
    return requestMock({
      session: {
        access_token: 'mock_access_token',
        user: {
          ...mockUser,
          email,
        },
      },
      user: {
        ...mockUser,
        email,
      },
    }, 500);
  }

  try {
    const supabase = getSupabaseClient();
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) return createApiError(error, '邮箱或密码不正确');
    return createApiResponse(normalizeSessionPayload(data));
  } catch (error) {
    return createApiError(error, '登录失败，请稍后再试');
  }
}

export async function signUpWithEmailPassword(email, password, profile = {}) {
  if (isMockMode()) {
    return requestMock({
      session: {
        access_token: 'mock_access_token',
        user: {
          ...mockUser,
          email,
          ...profile,
        },
      },
      user: {
        ...mockUser,
        email,
        ...profile,
      },
    }, 600);
  }

  try {
    const supabase = getSupabaseClient();
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: profile,
      },
    });
    if (error) return createApiError(error, '注册失败，请检查邮箱或密码');
    return createApiResponse(normalizeSessionPayload(data));
  } catch (error) {
    return createApiError(error, '注册失败，请稍后再试');
  }
}

export async function signInWithOtp(email) {
  if (isMockMode()) {
    return requestMock({
      email,
      sent: true,
      message: 'Mock 模式已模拟发送登录邮件',
    }, 500);
  }

  try {
    const supabase = getSupabaseClient();
    const { data, error } = await supabase.auth.signInWithOtp({
      email,
      options: {
        shouldCreateUser: true,
      },
    });
    if (error) return createApiError(error, '发送登录邮件失败');
    return createApiResponse({ ...data, email, sent: true });
  } catch (error) {
    return createApiError(error, '发送登录邮件失败');
  }
}

export async function signOut() {
  if (isMockMode()) {
    return requestMock({ signedOut: true }, 300);
  }

  try {
    const supabase = getSupabaseClient();
    const { error } = await supabase.auth.signOut();
    if (error) return createApiError(error, '退出登录失败');
    return createApiResponse({ signedOut: true });
  } catch (error) {
    return createApiError(error, '退出登录失败');
  }
}

export function subscribeToAuthState(callback) {
  if (isMockMode()) return () => {};
  const supabase = getSupabaseClient();
  const { data } = supabase.auth.onAuthStateChange((event, session) => callback({ event, session, user: session?.user || null }));
  return () => data.subscription.unsubscribe();
}

export async function resetPassword(email) {
  if (isMockMode()) return requestMock({ email, sent: true }, 400);
  try {
    const supabase = getSupabaseClient();
    const { error } = await supabase.auth.resetPasswordForEmail(email);
    if (error) return createApiError(error, '发送重置邮件失败');
    return createApiResponse({ email, sent: true });
  } catch (error) {
    return createApiError(error, '发送重置邮件失败');
  }
}

export async function upsertProfile(profile = {}) {
  if (isMockMode()) {
    return requestMock({
      ...mockUser,
      ...profile,
    }, 400);
  }

  try {
    const supabase = getSupabaseClient();
    const { data: sessionData, error: sessionError } = await supabase.auth.getUser();
    if (sessionError) return createApiError(sessionError, '获取用户信息失败');

    const userId = sessionData?.user?.id;
    if (!userId) return createApiError('Missing user id', '当前用户未登录');

    const payload = {
      id: userId,
      nickname: profile.nickname || sessionData.user.email || '童话收藏家',
      avatar_url: profile.avatar_url || null,
      avatar_text: profile.avatar_text || profile.nickname?.slice(0, 1) || '童',
    };

    const { data, error } = await supabase
      .from('profiles')
      .upsert(payload, { onConflict: 'id' })
      .select('*')
      .single();

    if (error) return createApiError(error, '保存用户资料失败');
    return createApiResponse(data);
  } catch (error) {
    return createApiError(error, '保存用户资料失败');
  }
}
