import { Platform } from 'react-native';
import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requestMock } from './client';

const ALLOWED_BUCKETS = new Set(['avatars', 'photos', 'diary-attachments']);

async function uriToUploadBody(uri) {
  if (!uri || typeof uri !== 'string') throw new Error('请选择有效的本地文件');
  const response = await fetch(uri);
  if (!response.ok) throw new Error('读取本地文件失败');
  return Platform.OS === 'web' ? response.blob() : response.arrayBuffer();
}

export function validateStoragePath(bucket, path, context) {
  if (!ALLOWED_BUCKETS.has(bucket)) throw new Error('不支持的文件存储类型');
  if (!path || typeof path !== 'string') throw new Error('文件路径无效');
  const parts = path.split('/').filter(Boolean);
  if (parts.length !== 3) throw new Error('文件路径必须符合 coupleId/userId/fileName');
  if (!context?.coupleId || parts[0] !== context.coupleId) throw new Error('文件不属于当前情侣空间');
  if (!context?.user?.id || parts[1] !== context.user.id) throw new Error('只能操作当前用户拥有的文件');
  if (!parts[2] || parts[2] === '.' || parts[2] === '..') throw new Error('文件名无效');
  return true;
}

export async function uploadImage(bucket, path, localUri, options = {}) {
  if (!isMockMode()) {
    try {
      const context = await getAuthenticatedContext();
      validateStoragePath(bucket, path, context);
      const body = await uriToUploadBody(localUri);
      const { data, error } = await context.supabase.storage.from(bucket).upload(path, body, {
        contentType: options.contentType || 'image/jpeg',
        upsert: false,
      });
      if (error) return createApiError(error, '上传图片失败');
      return createApiResponse({ bucket, path: data.path, uploadedAt: new Date().toISOString() });
    } catch (error) {
      return createApiError(error, '上传图片失败');
    }
  }

  return requestMock({
    bucket,
    path,
    localUri,
    publicUrl: localUri || `mock://${bucket}/${path}`,
    contentType: options.contentType || 'image/jpeg',
    uploadedAt: new Date().toISOString(),
  }, 500);
}

export async function getSignedUrl(bucket, path, expiresIn = 3600) {
  if (!isMockMode()) {
    try {
      const context = await getAuthenticatedContext();
      if (!ALLOWED_BUCKETS.has(bucket)) throw new Error('不支持的文件存储类型');
      if (!path || typeof path !== 'string') throw new Error('文件路径无效');
      const parts = path.split('/').filter(Boolean);
      if (parts.length !== 3 || parts[0] !== context.coupleId) throw new Error('文件不属于当前情侣空间');
      const safeExpiresIn = Math.min(Math.max(Number(expiresIn) || 3600, 60), 86400);
      const { data, error } = await context.supabase.storage.from(bucket).createSignedUrl(path, safeExpiresIn);
      return error
        ? createApiError(error, '创建图片访问链接失败')
        : createApiResponse({ bucket, path, signedUrl: data.signedUrl, expiresIn: safeExpiresIn });
    } catch (error) {
      return createApiError(error, '创建图片访问链接失败');
    }
  }

  return requestMock({
    bucket,
    path,
    signedUrl: `mock://${bucket}/${path}?expiresIn=${expiresIn}`,
    expiresIn,
  });
}

export async function deleteFile(bucket, path) {
  if (!isMockMode()) {
    try {
      const context = await getAuthenticatedContext();
      validateStoragePath(bucket, path, context);
      const { error } = await context.supabase.storage.from(bucket).remove([path]);
      return error ? createApiError(error, '删除文件失败') : createApiResponse({ bucket, path, deleted: true });
    } catch (error) {
      return createApiError(error, '删除文件失败');
    }
  }

  return requestMock({ bucket, path, deleted: true }, 300);
}
