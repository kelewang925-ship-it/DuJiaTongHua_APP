import { requestMock } from './client';
import { mockPhotos } from './mockData';

export async function getPhotoTimeline() {
  return requestMock(mockPhotos);
}

export async function uploadPhoto(payload) {
  const photo = {
    id: `photo_${Date.now()}`,
    title: payload?.title || '新的照片',
    date: payload?.date || '今天',
    type: 'photo',
  };
  return requestMock(photo, 500);
}

export async function getAlbumDetail(albumId) {
  return requestMock({ id: albumId, photos: mockPhotos });
}
