import 'react-native-url-polyfill/auto';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { createClient } from '@supabase/supabase-js';

const configuredMode = String(process.env.EXPO_PUBLIC_API_MODE || 'mock').trim().toLowerCase();
export const API_MODE = configuredMode === 'real' || configuredMode === 'mock' ? configuredMode : 'disabled';

let supabaseClient;

export function getApiMode() {
  return API_MODE;
}

export function isMockMode() {
  return API_MODE === 'mock';
}

export async function delay(ms = 300) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function withRequestTimeout(promise, timeoutMs = 12000, message = '请求超时') {
  let timer = null;
  try {
    return await Promise.race([
      Promise.resolve(promise),
      new Promise((_, reject) => {
        timer = setTimeout(() => {
          const error = new Error(message);
          error.code = 'NETWORK_TIMEOUT';
          reject(error);
        }, timeoutMs);
      }),
    ]);
  } finally {
    if (timer) clearTimeout(timer);
  }
}

export function createApiResponse(data, meta = null) {
  return { success: true, data, meta, error: null };
}

function inferErrorCode(error) {
  const explicit = String(error?.code || error?.status || error?.name || '');
  const message = String(error?.message || error?.error_description || error || '').toLowerCase();
  if (explicit === '401' || explicit === 'AuthSessionMissingError' || message.includes('not authenticated') || message.includes('未登录') || message.includes('jwt')) return 'SESSION_EXPIRED';
  if (explicit === '403' || explicit === '42501' || message.includes('permission') || message.includes('row-level security') || message.includes('rls')) return 'PERMISSION_DENIED';
  if (explicit === '408' || explicit === '429' || explicit === 'NETWORK_TIMEOUT' || /^5\d\d$/.test(explicit) || explicit === 'TypeError' && message.includes('fetch') || message.includes('network') || message.includes('fetch') || message.includes('timeout')) return 'NETWORK_ERROR';
  if (explicit === '23505' || explicit === '409' || message.includes('duplicate') || message.includes('unique')) return 'CONFLICT';
  if (explicit === 'REAL_MODE_NOT_CONFIGURED' || explicit === 'INVALID_API_MODE') return explicit;
  return explicit || 'REQUEST_ERROR';
}

function classifyError(code) {
  if (code === 'SESSION_EXPIRED') return { category: 'session', retryable: false };
  if (code === 'PERMISSION_DENIED') return { category: 'permission', retryable: false };
  if (code === 'NETWORK_ERROR') return { category: 'network', retryable: true };
  if (code === 'CONFLICT') return { category: 'conflict', retryable: false };
  if (code === 'REAL_MODE_NOT_CONFIGURED' || code === 'INVALID_API_MODE') return { category: 'configuration', retryable: false };
  return { category: 'request', retryable: false };
}

export function normalizeError(error, fallbackMessage = '请求失败，请稍后再试') {
  if (!error) return { message: fallbackMessage, code: 'UNKNOWN_ERROR', category: 'request', retryable: false, raw: null };
  const code = inferErrorCode(error);
  const classification = classifyError(code);
  let message = typeof error === 'string' ? error : error.message || error.error_description || fallbackMessage;
  if (code === 'SESSION_EXPIRED') message = '登录状态已失效，请重新登录';
  if (code === 'PERMISSION_DENIED') message = '当前账号没有权限执行此操作';
  if (code === 'NETWORK_ERROR') message = '网络连接失败，请检查网络后重试';
  if (code === 'INVALID_API_MODE') message = 'API 模式配置无效，请检查 EXPO_PUBLIC_API_MODE';
  if (!message || (code === 'REQUEST_ERROR' && typeof error === 'string')) message = fallbackMessage;
  return { message, code, ...classification, raw: error };
}

export function createApiError(error, fallbackMessage, meta = null) {
  return { success: false, data: null, meta, error: normalizeError(error, fallbackMessage) };
}

export function isSessionError(resultOrError) {
  const error = resultOrError?.error || resultOrError;
  return normalizeError(error).category === 'session';
}

export async function requestMock(data, ms = 300, meta = null) {
  if (!isMockMode()) {
    const error = new Error('Mock request is unavailable outside mock mode');
    error.code = 'INVALID_API_MODE';
    return createApiError(error, '当前环境不允许使用模拟请求');
  }
  await delay(ms);
  return createApiResponse(data, meta);
}

export function assertRealModeReady() {
  if (API_MODE === 'mock') return true;
  if (API_MODE !== 'real') {
    const error = new Error(`Unsupported API mode: ${configuredMode || '(empty)'}`);
    error.code = 'INVALID_API_MODE';
    throw error;
  }
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
  return { url: process.env.EXPO_PUBLIC_SUPABASE_URL || '', anonKey: process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || '' };
}

export function createSupabaseClient() {
  assertRealModeReady();
  if (supabaseClient) return supabaseClient;
  const { url, anonKey } = getSupabaseConfig();
  supabaseClient = createClient(url, anonKey, {
    auth: { storage: AsyncStorage, autoRefreshToken: true, persistSession: true, detectSessionInUrl: false },
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
  const user = userData?.user;
  if (!user?.id || user.id !== sessionUser.id) {
    const error = new Error('登录状态与服务端用户不匹配');
    error.code = 'SESSION_EXPIRED';
    throw error;
  }
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
