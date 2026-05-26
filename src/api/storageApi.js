import { createApiError, isMockMode, requestMock } from './client';

export async function uploadImage(bucket, path, localUri, options = {}) {
  if (!isMockMode()) {
    return createApiError('Real storage API is not implemented yet.', '图片上传真实接口尚未接入');
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
    return createApiError('Real storage API is not implemented yet.', '签名链接真实接口尚未接入');
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
    return createApiError('Real storage API is not implemented yet.', '删除文件真实接口尚未接入');
  }

  return requestMock({
    bucket,
    path,
    deleted: true,
  }, 300);
}
