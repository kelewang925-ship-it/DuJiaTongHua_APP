import 'react-native-url-polyfill/auto';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { createClient } from '@supabase/supabase-js';

const configuredMode = String(process.env.EXPO_PUBLIC_API_MODE || 'mock').toLowerCase();
export const API_MODE = configuredMode === 'real' ? 'real' : 'mock';

let supabaseClient;

export function getApiMode() {
  return API_MODE;
}

export function isMockMode() {
  return API_MODE !== 'real';
}

export async function delay(ms = 300) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function createApiResponse(data, meta = null) {
  return {
    success: true,
    data,
    meta,
    error: null,
  };
}

function inferErrorCode(error) {
  const explicit = error?.code || error?.status || error?.name;
  if (explicit) return String(explicit);
  const message = String(error?.message || error?.error_description || error || '').toLowerCase();
  if (message.includes('not authenticated') || message.includes('未登录') || message.includes('jwt')) return 'SESSION_EXPIRED';
  if (message.includes('permission') || message.includes('row-level security') || message.includes('rls')) return 'PERMISSION_DENIED';
  if (message.includes('network') || message.includes('fetch') || message.includes('timeout')) return 'NETWORK_ERROR';
  if (message.includes('duplicate') || message.includes('unique')) return 'CONFLICT';
  return 'REQUEST_ERROR';
}

export function normalizeError(error, fallbackMessage = '请求失败，请稍后再试') {
  if (!error) {
    return { message: fallbackMessage, code: 'UNKNOWN_ERROR', raw: null };
  }

  if (typeof error === 'string') {
    const code = inferErrorCode(error);
    const message = code === 'REQUEST_ERROR' ? (fallbackMessage || error) : error;
    return { message, code, raw: error };
  }

  const code = inferErrorCode(error);
  let message = error.message || error.error_description || fallbackMessage;
  if (code === 'SESSION_EXPIRED') message = '登录状态已失效，请重新登录';
  if (code === 'PERMISSION_DENIED') message = '当前账号没有权限执行此操作';
  if (code === 'NETWORK_ERROR') message = '网络连接失败，请检查网络后重试';
  return { message, code, raw: error };
}

export function createApiError(error, fallbackMessage, meta = null) {
  return {
    success: false,
    data: null,
    meta,
    error: normalizeError(error, fallbackMessage),
  };
}

export function isSessionError(resultOrError) {
  const error = resultOrError?.error || resultOrError;
  const code = normalizeError(error).code;
  return code === 'SESSION_EXPIRED' || code === 'AuthSessionMissingError' || code === '401';
}

export async function requestMock(data, ms = 300, meta = null) {
  await delay(ms);
  return createApiResponse(data, meta);
}

export function assertRealModeReady() {
  if (isMockMode()) return true;
  const missing = [];
  if (!process.env.EXPO_PUBLIC_SUPABASE_URL) missing.push('EXPO_PUBLIC_SUPABASE_URL');
  if (!process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY) missing.push('EXPO_PUBLIC_SUPABASE_ANON_KEY');
  if (missing.length) {
    const error = new Error(`Real API mode is enabled but missing env vars: ${missing.join(', ')}`);
    error.code = 'REAL_MODE_NOT_CONFIGURED';
    throw error;
  }
  return true;
}

export function getSupabaseConfig() {
  return {
    url: process.env.EXPO_PUBLIC_SUPABASE_URL || '',
    anonKey: process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || '',
  };
}

export function createSupabaseClient() {
  assertRealModeReady();
  if (supabaseClient) return supabaseClient;
  const { url, anonKey } = getSupabaseConfig();
  supabaseClient = createClient(url, anonKey, {
    auth: {
      storage: AsyncStorage,
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: false,
    },
  });
  return supabaseClient;
}

export function getSupabaseClient() {
  return createSupabaseClient();
}

export async function getAuthenticatedContext() {
  const supabase = getSupabaseClient();
  const { data: sessionData, error: sessionError } = await supabase.auth.getSession();
  if (sessionError) throw sessionError;
  const sessionUser = sessionData?.session?.user;
  if (!sessionUser) {
    const error = new Error('当前用户未登录');
    error.code = 'SESSION_EXPIRED';
    throw error;
  }

  const { data: userData, error: userError } = await supabase.auth.getUser();
  if (userError) throw userError;
  const user = userData?.user || sessionUser;
  const { data: couple, error: coupleError } = await supabase
    .from('couples')
    .select('*')
    .or(`user_a.eq.${user.id},user_b.eq.${user.id}`)
    .eq('status', 'active')
    .maybeSingle();
  if (coupleError) throw coupleError;
  return { supabase, session: sessionData.session, user, couple, coupleId: couple?.id || null };
}

export function requireCouple(context) {
  if (!context?.coupleId) {
    const error = new Error('请先完成情侣绑定');
    error.code = 'COUPLE_REQUIRED';
    throw error;
  }
  return context.coupleId;
}
