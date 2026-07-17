import 'react-native-url-polyfill/auto';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { createClient } from '@supabase/supabase-js';

export const API_MODE = process.env.EXPO_PUBLIC_API_MODE || 'mock';

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

export function createApiResponse(data, meta) {
  return {
    success: true,
    data,
    meta: meta || null,
    error: null,
  };
}

export function normalizeError(error, fallbackMessage = '请求失败，请稍后再试') {
  if (!error) {
    return {
      message: fallbackMessage,
      code: 'UNKNOWN_ERROR',
      raw: null,
    };
  }

  if (typeof error === 'string') {
    return {
      message: error,
      code: 'ERROR_MESSAGE',
      raw: error,
    };
  }

  return {
    message: error.message || error.error_description || fallbackMessage,
    code: error.code || error.status || error.name || 'REQUEST_ERROR',
    raw: error,
  };
}

export function createApiError(error, fallbackMessage) {
  return {
    success: false,
    data: null,
    meta: null,
    error: normalizeError(error, fallbackMessage),
  };
}

export async function requestMock(data, ms = 300, meta) {
  await delay(ms);
  return createApiResponse(data, meta);
}

export function assertRealModeReady() {
  if (isMockMode()) return true;

  const missing = [];
  if (!process.env.EXPO_PUBLIC_SUPABASE_URL) missing.push('EXPO_PUBLIC_SUPABASE_URL');
  if (!process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY) missing.push('EXPO_PUBLIC_SUPABASE_ANON_KEY');

  if (missing.length) {
    throw new Error(`Real API mode is enabled but missing env vars: ${missing.join(', ')}`);
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
  const { data: userData, error: userError } = await supabase.auth.getUser();
  if (userError) throw userError;
  const user = userData?.user;
  if (!user) throw new Error('当前用户未登录');

  const { data: couple, error: coupleError } = await supabase
    .from('couples')
    .select('*')
    .or(`user_a.eq.${user.id},user_b.eq.${user.id}`)
    .eq('status', 'active')
    .maybeSingle();
  if (coupleError) throw coupleError;
  return { supabase, user, couple, coupleId: couple?.id || null };
}

export function requireCouple(context) {
  if (!context?.coupleId) throw new Error('请先完成情侣绑定');
  return context.coupleId;
}
