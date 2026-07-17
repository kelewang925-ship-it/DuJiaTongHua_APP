import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase, normalizePhotoCollection } from './mappers';
import { mockPhotos } from './mockData';
import { deleteFile, uploadImage } from './storageApi';

const uniquePathPart = () => globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random().toString(16).slice(2)}`;

export async function getAlbumList() {
  if (isMockMode()) return requestMock([{ id: 'album_default', title: '我们的照片绘本', count: mockPhotos.length, photos: mockPhotos }]);
  try {
    const context = await getAuthenticatedContext(); requireCouple(context);
    const { data, error } = await context.supabase.from('photo_collections').select('*,photos(*)').eq('couple_id', context.coupleId).order('created_at', { ascending: false });
    return error ? createApiError(error, '加载相册失败') : createApiResponse((data || []).map(normalizePhotoCollection));
  } catch (error) { return createApiError(error, '加载相册失败'); }
}

export async function getPhotoTimeline(params = {}) {
  if (isMockMode()) return requestMock(typeof params.limit === 'number' ? mockPhotos.slice(0, params.limit) : mockPhotos);
  const result = await getAlbumList();
  if (!result.success) return result;
  const photos = result.data.flatMap((collection) => (collection.photos || []).map((photo) => ({ ...photo, collectionTitle: collection.title })));
  return createApiResponse(typeof params.limit === 'number' ? photos.slice(0, params.limit) : photos, { derived: true });
}

export async function getAlbumDetail(id = 'album_default') {
  if (isMockMode()) return requestMock({ id, title: '我们的照片绘本', photos: mockPhotos });
  try {
    const { supabase } = await getAuthenticatedContext();
    const { data, error } = await supabase.from('photo_collections').select('*,photos(*)').eq('id', id).single();
    return error ? createApiError(error, '加载相册详情失败') : createApiResponse(normalizePhotoCollection(data));
  } catch (error) { return createApiError(error, '加载相册详情失败'); }
}

export async function uploadPhoto(payload = {}) {
  if (isMockMode()) return requestMock({ id: `photo_${Date.now()}`, ...payload, type: 'photo', createdAt: new Date().toISOString() }, 500);
  try {
    const context = await getAuthenticatedContext(); requireCouple(context);
    const sourceFiles = payload.files || payload.photos || (payload.storagePath ? [{ storagePath: payload.storagePath }] : []);
    const files = [];
    for (const file of sourceFiles) {
      if (file.storagePath) { files.push(file); continue; }
      const path = `${context.coupleId}/${context.user.id}/${uniquePathPart()}`;
      const result = await uploadImage('photos', path, file.uri, { contentType: file.mimeType });
      if (!result.success) { await Promise.all(files.filter((item) => item.storagePath).map((item) => deleteFile('photos', item.storagePath))); return result; }
      files.push({ ...file, storagePath: result.data.path });
    }
    const { data: collection, error: collectionError } = await context.supabase.from('photo_collections').insert({
      couple_id: context.coupleId, uploader_id: context.user.id, title: payload.title?.trim() || '新的照片绘本', note: payload.note || payload.content || null, tags: payload.tags || [],
    }).select('*').single();
    if (collectionError) { await Promise.all(files.map((file) => deleteFile('photos', file.storagePath))); return createApiError(collectionError, '创建照片集失败'); }
    const rows = files.map((file, index) => ({
      couple_id: context.coupleId, uploader_id: context.user.id, collection_id: collection.id,
      title: file.title || payload.title || `照片 ${index + 1}`, note: file.note || payload.note || null,
      file_url: file.storagePath, storage_path: file.storagePath, thumbnail_url: file.thumbnailPath || null,
      taken_at: file.takenAt || payload.takenAt || null, tags: payload.tags || [],
    }));
    if (rows.length) {
      const { data: photos, error: photoError } = await context.supabase.from('photos').insert(rows).select('*');
      if (photoError) {
        await context.supabase.from('photo_collections').delete().eq('id', collection.id);
        await Promise.all(files.filter((file) => file.storagePath).map((file) => deleteFile('photos', file.storagePath)));
        return createApiError(photoError, '保存照片失败，已清理上传文件');
      }
      collection.photos = photos;
    }
    return createApiResponse(normalizePhotoCollection(collection));
  } catch (error) { return createApiError(error, '保存照片失败'); }
}

export async function deletePhoto(id) {
  if (isMockMode()) return requestMock({ id, deleted: true }, 300);
  try {
    const { supabase } = await getAuthenticatedContext();
    const { data, error } = await supabase.from('photos').select('storage_path').eq('id', id).single();
    if (error) return createApiError(error, '查找照片失败');
    const { error: deleteError } = await supabase.from('photos').delete().eq('id', id);
    if (deleteError) return createApiError(deleteError, '删除照片失败');
    if (data.storage_path) await deleteFile('photos', data.storage_path);
    return createApiResponse({ id, deleted: true });
  } catch (error) { return createApiError(error, '删除照片失败'); }
}
