import { Platform } from 'react-native';
import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requestMock } from './client';
import { parseStoragePath } from './storagePaths';

const ALLOWED_BUCKETS = new Set(['avatars', 'photos', 'diary-attachments']);

async function uriToUploadBody(uri) {
  if (!uri || typeof uri !== 'string') throw new Error('请选择有效的本地文件');
  const response = await fetch(uri);
  if (!response.ok) throw new Error('读取本地文件失败');
  return Platform.OS === 'web' ? response.blob() : response.arrayBuffer();
}

export function validateStoragePath(bucket, path, context, { requireOwner = true } = {}) {
  if (!ALLOWED_BUCKETS.has(bucket)) throw new Error('不支持的文件存储类型');
  const parsed = parseStoragePath(path);
  if (!parsed) throw new Error('文件路径必须符合 coupleId/userId/uuid');
  if (!context?.coupleId || parsed.coupleId !== context.coupleId) throw new Error('文件不属于当前情侣空间');
  if (requireOwner && (!context?.user?.id || parsed.userId !== context.user.id)) throw new Error('只能操作当前用户拥有的文件');
  return parsed;
}

export async function uploadImage(bucket, path, localUri, options = {}) {
  if (isMockMode()) {
    return requestMock({ bucket, path, localUri, publicUrl: localUri || `mock://${bucket}/${path}`, contentType: options.contentType || 'image/jpeg', uploadedAt: new Date().toISOString() }, 500);
  }
  try {
    const context = await getAuthenticatedContext();
    validateStoragePath(bucket, path, context);
    const body = await uriToUploadBody(localUri);
    const { data, error } = await context.supabase.storage.from(bucket).upload(path, body, {
      contentType: options.contentType || 'image/jpeg',
      upsert: false,
    });
    return error ? createApiError(error, '上传图片失败') : createApiResponse({ bucket, path: data.path, uploadedAt: new Date().toISOString() });
  } catch (error) {
    return createApiError(error, '上传图片失败');
  }
}

export async function getSignedUrl(bucket, path, expiresIn = 3600) {
  if (isMockMode()) return requestMock({ bucket, path, signedUrl: `mock://${bucket}/${path}?expiresIn=${expiresIn}`, expiresIn });
  try {
    const context = await getAuthenticatedContext();
    validateStoragePath(bucket, path, context, { requireOwner: false });
    const safeExpiresIn = Math.min(Math.max(Number(expiresIn) || 3600, 60), 86400);
    const { data, error } = await context.supabase.storage.from(bucket).createSignedUrl(path, safeExpiresIn);
    return error ? createApiError(error, '创建图片访问链接失败') : createApiResponse({ bucket, path, signedUrl: data.signedUrl, expiresIn: safeExpiresIn });
  } catch (error) {
    return createApiError(error, '创建图片访问链接失败');
  }
}

export async function deleteFile(bucket, path) {
  if (isMockMode()) return requestMock({ bucket, path, deleted: true }, 300);
  try {
    const context = await getAuthenticatedContext();
    validateStoragePath(bucket, path, context);
    const { error } = await context.supabase.storage.from(bucket).remove([path]);
    return error ? createApiError(error, '删除文件失败') : createApiResponse({ bucket, path, deleted: true });
  } catch (error) {
    return createApiError(error, '删除文件失败');
  }
}
