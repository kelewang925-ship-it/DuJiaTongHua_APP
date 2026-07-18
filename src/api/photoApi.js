import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { normalizePhotoCollection } from './mappers';
import { mockPhotos } from './mockData';
import { deleteFile, uploadImage, validateStoragePath } from './storageApi';
import { buildStoragePath } from './storagePaths';

async function cleanupFiles(files = []) {
  const ownedUploads = files.filter((item) => item?.storagePath && item?.createdByOperation === true);
  const results = await Promise.all(ownedUploads.map((item) => deleteFile('photos', item.storagePath)));
  return results.filter((result) => !result.success);
}

function withCleanupMeta(result, cleanupFailures = []) {
  return {
    ...result,
    meta: {
      ...(result.meta || {}),
      cleanupRequired: cleanupFailures.length > 0,
      failedCleanupCount: cleanupFailures.length,
    },
  };
}

function validateCollectionRow(collection, context, { requireOwner = false } = {}) {
  if (!collection?.id) return false;
  if ((collection.couple_id || collection.coupleId) !== context?.coupleId) return false;
  if (requireOwner && (collection.uploader_id || collection.uploaderId) !== context?.user?.id) return false;
  return (collection.photos || []).every((photo) => {
    const photoCoupleId = photo.couple_id || photo.coupleId;
    const collectionId = photo.collection_id || photo.collectionId;
    return Boolean(photo?.id && photoCoupleId === context.coupleId && collectionId === collection.id);
  });
}

async function attachSignedPhotoUrls(collection, context) {
  const normalized = normalizePhotoCollection(collection);
  const photos = await Promise.all((normalized.photos || []).map(async (photo) => {
    const storagePath = photo.storagePath || photo.fileUrl;
    validateStoragePath('photos', storagePath, context, { requireOwner: false });
    const { data, error } = await context.supabase.storage.from('photos').createSignedUrl(storagePath, 3600);
    const signedUrl = error ? null : data?.signedUrl || null;
    return {
      ...photo,
      storagePath,
      uri: signedUrl,
      signedUrl,
      imageAccessError: signedUrl ? null : 'signed_url_unavailable',
    };
  }));
  return { ...normalized, photos };
}

function withOperationContext(result, operation) {
  if (result?.success) return result;
  return {
    ...result,
    error: {
      ...(result?.error || {}),
      message: `${operation}失败：${result?.error?.message || '请稍后重试'}`,
    },
    meta: { ...(result?.meta || {}), operation },
  };
}

export async function getAlbumList() {
  if (isMockMode()) return requestMock([{ id: 'album_default', title: '我们的照片绘本', count: mockPhotos.length, photos: mockPhotos }]);
  try {
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const { data, error } = await context.supabase.from('photo_collections').select('*,photos(*)').eq('couple_id', context.coupleId).order('created_at', { ascending: false });
    if (error) return createApiError(error, '加载相册失败');
    const rows = data || [];
    if (rows.some((collection) => !validateCollectionRow(collection, context))) return createApiError('Album ownership mismatch', '相册数据包含不属于当前情侣空间的记录');
    const collections = await Promise.all(rows.map((collection) => attachSignedPhotoUrls(collection, context)));
    return createApiResponse(collections);
  } catch (error) {
    return createApiError(error, '加载相册失败');
  }
}

export async function getPhotoTimeline(params = {}) {
  if (isMockMode()) return requestMock(typeof params.limit === 'number' ? mockPhotos.slice(0, params.limit) : mockPhotos);
  const result = await getAlbumList();
  if (!result.success) return result;
  const photos = result.data.flatMap((collection) => (collection.photos || []).map((photo) => ({ ...photo, collectionId: collection.id, collectionTitle: collection.title })));
  return createApiResponse(typeof params.limit === 'number' ? photos.slice(0, params.limit) : photos, { derived: true });
}

export async function getAlbumDetail(id = 'album_default') {
  if (isMockMode()) return requestMock({ id, title: '我们的照片绘本', photos: mockPhotos });
  try {
    if (!id || id === 'album_default') return createApiError('Missing album id', '缺少相册标识，无法加载');
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const { data, error } = await context.supabase.from('photo_collections').select('*,photos(*)').eq('id', id).eq('couple_id', context.coupleId).maybeSingle();
    if (error) return createApiError(error, '加载相册详情失败');
    if (!validateCollectionRow(data, context)) return createApiError('Album not found', '相册不存在、无权限或已被删除');
    return createApiResponse(await attachSignedPhotoUrls(data, context));
  } catch (error) {
    return createApiError(error, '加载相册详情失败');
  }
}

export async function uploadPhoto(payload = {}) {
  if (isMockMode()) return requestMock({ id: `photo_${Date.now()}`, ...payload, type: 'photo', createdAt: new Date().toISOString() }, 500);

  const files = [];
  try {
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const sourceFiles = payload.files || payload.photos || (payload.storagePath ? [{ storagePath: payload.storagePath }] : []);
    if (!sourceFiles.length) return createApiError('Missing photos', '请至少选择一张照片');
    if (sourceFiles.length > 9) return createApiError('Too many photos', '单个照片集最多上传 9 张照片');

    for (const file of sourceFiles) {
      if (file.storagePath) {
        validateStoragePath('photos', file.storagePath, context);
        files.push({ ...file, createdByOperation: false });
        continue;
      }
      if (!file.uri) {
        const cleanupFailures = await cleanupFiles(files);
        return withCleanupMeta(createApiError('Missing photo URI', '存在无法读取的照片'), cleanupFailures);
      }
      const path = buildStoragePath(context.coupleId, context.user.id);
      const result = await uploadImage('photos', path, file.uri, { contentType: file.mimeType });
      if (!result.success) {
        const cleanupFailures = await cleanupFiles(files);
        return withCleanupMeta(withOperationContext(result, '私有图片上传'), cleanupFailures);
      }
      files.push({ ...file, storagePath: result.data.path, createdByOperation: true });
    }

    const { data: collection, error: collectionError } = await context.supabase.from('photo_collections').insert({
      couple_id: context.coupleId,
      uploader_id: context.user.id,
      title: payload.title?.trim() || '新的照片绘本',
      note: payload.note || payload.content || null,
      tags: payload.tags || [],
    }).select('*').maybeSingle();

    if (collectionError || !validateCollectionRow({ ...collection, photos: [] }, context, { requireOwner: true })) {
      const cleanupFailures = await cleanupFiles(files);
      return withCleanupMeta(withOperationContext(createApiError(collectionError || 'Photo collection write mismatch', '创建照片集失败，服务端未确认写入结果'), '创建照片集'), cleanupFailures);
    }

    const rows = files.map((file, index) => ({
      couple_id: context.coupleId,
      uploader_id: context.user.id,
      collection_id: collection.id,
      title: file.title || payload.title || `照片 ${index + 1}`,
      note: file.note || payload.note || null,
      file_url: file.storagePath,
      storage_path: file.storagePath,
      thumbnail_url: file.thumbnailPath || null,
      taken_at: file.takenAt || payload.takenAt || null,
      tags: payload.tags || [],
    }));

    const { data: photos, error: photoError } = await context.supabase.from('photos').insert(rows).select('*');
    const photoRowsValid = Array.isArray(photos) && photos.length === rows.length && photos.every((photo) => (photo.couple_id || photo.coupleId) === context.coupleId && (photo.collection_id || photo.collectionId) === collection.id && (photo.uploader_id || photo.uploaderId) === context.user.id);
    if (photoError || !photoRowsValid) {
      const { error: rollbackError } = await context.supabase.from('photo_collections').delete().eq('id', collection.id).eq('uploader_id', context.user.id);
      const cleanupFailures = await cleanupFiles(files);
      return withOperationContext(createApiError(photoError || 'Photo rows write mismatch', '保存照片失败，已尝试回滚照片集', {
        cleanupRequired: Boolean(rollbackError) || cleanupFailures.length > 0,
        failedCleanupCount: cleanupFailures.length,
      }), '写入照片记录');
    }

    return createApiResponse(await attachSignedPhotoUrls({ ...collection, photos }, context));
  } catch (error) {
    const cleanupFailures = await cleanupFiles(files);
    return withCleanupMeta(createApiError(error, '保存照片失败'), cleanupFailures);
  }
}

export async function deletePhoto(id) {
  if (isMockMode()) return requestMock({ id, deleted: true }, 300);
  try {
    if (!id) return createApiError('Missing photo collection id', '缺少照片集标识，无法删除');
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const { data: collection, error: findError } = await context.supabase.from('photo_collections').select('id,couple_id,uploader_id,photos(id,couple_id,collection_id,storage_path)').eq('id', id).eq('couple_id', context.coupleId).eq('uploader_id', context.user.id).maybeSingle();
    if (findError) return createApiError(findError, '找不到可删除的照片集，或当前账号没有权限');
    if (!validateCollectionRow(collection, context, { requireOwner: true })) return createApiError('Photo collection not found', '照片集不存在、无权限或已被删除');

    const { data: deleted, error: deleteError } = await context.supabase.from('photo_collections').delete().eq('id', id).eq('couple_id', context.coupleId).eq('uploader_id', context.user.id).select('id,couple_id,uploader_id').maybeSingle();
    if (deleteError) return createApiError(deleteError, '删除照片集失败');
    if (!validateCollectionRow({ ...deleted, photos: [] }, context, { requireOwner: true })) return createApiError('Photo collection not deleted', '照片集不存在、无权限或已被删除');

    const files = (collection.photos || []).map((photo) => ({ storagePath: photo.storage_path, createdByOperation: true }));
    const cleanupFailures = await cleanupFiles(files);
    if (cleanupFailures.length) return createApiError('Storage cleanup failed', '照片集已删除，但部分云端文件清理失败', { cleanupRequired: true, failedCount: cleanupFailures.length });
    return createApiResponse({ id: deleted.id, deleted: true });
  } catch (error) {
    return createApiError(error, '删除照片集失败');
  }
}
