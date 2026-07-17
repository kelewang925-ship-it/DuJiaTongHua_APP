import { Platform } from 'react-native';
import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requestMock } from './client';

async function uriToUploadBody(uri) {
  const response = await fetch(uri);
  if (!response.ok) throw new Error('读取本地文件失败');
  return Platform.OS === 'web' ? response.blob() : response.arrayBuffer();
}

export async function uploadImage(bucket, path, localUri, options = {}) {
  if (!isMockMode()) {
    try { const { supabase } = await getAuthenticatedContext(); const body = await uriToUploadBody(localUri); const { data, error } = await supabase.storage.from(bucket).upload(path, body, { contentType: options.contentType || 'image/jpeg', upsert: false }); if (error) return createApiError(error, '上传图片失败'); return createApiResponse({ bucket, path: data.path, uploadedAt: new Date().toISOString() }); } catch (error) { return createApiError(error, '上传图片失败'); }
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
    try { const { supabase } = await getAuthenticatedContext(); const { data, error } = await supabase.storage.from(bucket).createSignedUrl(path, expiresIn); return error ? createApiError(error, '创建图片访问链接失败') : createApiResponse({ bucket, path, signedUrl: data.signedUrl, expiresIn }); } catch (error) { return createApiError(error, '创建图片访问链接失败'); }
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
    try { const { supabase } = await getAuthenticatedContext(); const { error } = await supabase.storage.from(bucket).remove([path]); return error ? createApiError(error, '删除文件失败') : createApiResponse({ bucket, path, deleted: true }); } catch (error) { return createApiError(error, '删除文件失败'); }
  }

  return requestMock({
    bucket,
    path,
    deleted: true,
  }, 300);
}
