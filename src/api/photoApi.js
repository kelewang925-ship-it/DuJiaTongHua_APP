import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { normalizePhotoCollection } from './mappers';
import { mockPhotos } from './mockData';
import { deleteFile, uploadImage, validateStoragePath } from './storageApi';
import { buildStoragePath } from './storagePaths';

async function cleanupFiles(files = []) {
  const results = await Promise.all(files.filter((item) => item?.storagePath).map((item) => deleteFile('photos', item.storagePath)));
  return results.filter((result) => !result.success);
}

export async function getAlbumList() {
  if (isMockMode()) return requestMock([{ id: 'album_default', title: '我们的照片绘本', count: mockPhotos.length, photos: mockPhotos }]);
  try {
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const { data, error } = await context.supabase.from('photo_collections').select('*,photos(*)').eq('couple_id', context.coupleId).order('created_at', { ascending: false });
    return error ? createApiError(error, '加载相册失败') : createApiResponse((data || []).map(normalizePhotoCollection));
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
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const { data, error } = await context.supabase.from('photo_collections').select('*,photos(*)').eq('id', id).eq('couple_id', context.coupleId).single();
    return error ? createApiError(error, '加载相册详情失败') : createApiResponse(normalizePhotoCollection(data));
  } catch (error) {
    return createApiError(error, '加载相册详情失败');
  }
}

export async function uploadPhoto(payload = {}) {
  if (isMockMode()) return requestMock({ id: `photo_${Date.now()}`, ...payload, type: 'photo', createdAt: new Date().toISOString() }, 500);
  try {
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const sourceFiles = payload.files || payload.photos || (payload.storagePath ? [{ storagePath: payload.storagePath }] : []);
    if (!sourceFiles.length) return createApiError('Missing photos', '请至少选择一张照片');
    if (sourceFiles.length > 9) return createApiError('Too many photos', '单个照片集最多上传 9 张照片');

    const files = [];
    for (const file of sourceFiles) {
      if (file.storagePath) {
        validateStoragePath('photos', file.storagePath, context);
        files.push(file);
        continue;
      }
      if (!file.uri) {
        const cleanupFailures = await cleanupFiles(files);
        return createApiError('Missing photo URI', '存在无法读取的照片', { cleanupRequired: cleanupFailures.length > 0 });
      }
      const path = buildStoragePath(context.coupleId, context.user.id);
      const result = await uploadImage('photos', path, file.uri, { contentType: file.mimeType });
      if (!result.success) {
        const cleanupFailures = await cleanupFiles(files);
        return { ...result, meta: { ...(result.meta || {}), cleanupRequired: cleanupFailures.length > 0 } };
      }
      files.push({ ...file, storagePath: result.data.path });
    }

    const { data: collection, error: collectionError } = await context.supabase.from('photo_collections').insert({
      couple_id: context.coupleId,
      uploader_id: context.user.id,
      title: payload.title?.trim() || '新的照片绘本',
      note: payload.note || payload.content || null,
      tags: payload.tags || [],
    }).select('*').single();

    if (collectionError) {
      const cleanupFailures = await cleanupFiles(files);
      return createApiError(collectionError, '创建照片集失败', { cleanupRequired: cleanupFailures.length > 0 });
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
    if (photoError) {
      const { error: rollbackError } = await context.supabase.from('photo_collections').delete().eq('id', collection.id).eq('uploader_id', context.user.id);
      const cleanupFailures = await cleanupFiles(files);
      return createApiError(photoError, '保存照片失败，已尝试回滚照片集', { cleanupRequired: Boolean(rollbackError) || cleanupFailures.length > 0 });
    }

    return createApiResponse(normalizePhotoCollection({ ...collection, photos }));
  } catch (error) {
    return createApiError(error, '保存照片失败');
  }
}

export async function deletePhoto(id) {
  if (isMockMode()) return requestMock({ id, deleted: true }, 300);
  try {
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const { data: collection, error: findError } = await context.supabase.from('photo_collections').select('id,uploader_id,photos(storage_path)').eq('id', id).eq('couple_id', context.coupleId).eq('uploader_id', context.user.id).single();
    if (findError) return createApiError(findError, '找不到可删除的照片集，或当前账号没有权限');

    const { data: deleted, error: deleteError } = await context.supabase.from('photo_collections').delete().eq('id', id).eq('couple_id', context.coupleId).eq('uploader_id', context.user.id).select('id').single();
    if (deleteError || !deleted) return createApiError(deleteError || 'Photo collection not deleted', '删除照片集失败');

    const files = (collection.photos || []).map((photo) => ({ storagePath: photo.storage_path }));
    const cleanupFailures = await cleanupFiles(files);
    if (cleanupFailures.length) return createApiError('Storage cleanup failed', '照片集已删除，但部分云端文件清理失败', { cleanupRequired: true, failedCount: cleanupFailures.length });
    return createApiResponse({ id, deleted: true });
  } catch (error) {
    return createApiError(error, '删除照片集失败');
  }
}
