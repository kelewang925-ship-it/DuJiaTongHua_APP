import { createApiError, isMockMode, requestMock } from './client';
import { mockPhotos } from './mockData';

export async function getPhotoTimeline(params = {}) {
  if (!isMockMode()) {
    return createApiError('Real photo API is not implemented yet.', '照片真实接口尚未接入');
  }

  const { limit } = params;
  const list = typeof limit === 'number' ? mockPhotos.slice(0, limit) : mockPhotos;
  return requestMock(list);
}

export async function getAlbumList() {
  if (!isMockMode()) {
    return createApiError('Real photo API is not implemented yet.', '相册真实接口尚未接入');
  }

  return requestMock([
    {
      id: 'album_default',
      title: '我们的照片绘本',
      count: mockPhotos.length,
      coverTitle: mockPhotos[0]?.title || '第一张照片',
    },
  ]);
}

export async function uploadPhoto(payload = {}) {
  if (!isMockMode()) {
    return createApiError('Real photo API is not implemented yet.', '照片上传真实接口尚未接入');
  }

  const photo = {
    id: `photo_${Date.now()}`,
    title: payload.title?.trim() || '新的照片',
    note: payload.note?.trim() || payload.content?.trim() || '这张照片还没有写下说明。',
    fileUrl: payload.fileUrl || payload.localUri || null,
    thumbnailUrl: payload.thumbnailUrl || payload.localUri || null,
    date: payload.date || '今天',
    tags: payload.tags?.length ? payload.tags : ['照片'],
    type: 'photo',
    takenAt: payload.takenAt || new Date().toISOString(),
    createdAt: new Date().toISOString(),
  };

  return requestMock(photo, 500);
}

export async function getAlbumDetail(albumId = 'album_default') {
  if (!isMockMode()) {
    return createApiError('Real photo API is not implemented yet.', '相册详情真实接口尚未接入');
  }

  return requestMock({
    id: albumId,
    title: '我们的照片绘本',
    photos: mockPhotos,
  });
}

export async function deletePhoto(id) {
  if (!isMockMode()) {
    return createApiError('Real photo API is not implemented yet.', '删除照片真实接口尚未接入');
  }

  return requestMock({ id, deleted: true }, 300);
}
