import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { fromDatabase } from './mappers';
import { deleteFile, uploadImage } from './storageApi';

const uniquePathPart = () => globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random().toString(16).slice(2)}`;

const mockDiaries = [
  {
    id: 'diary_001',
    title: '一起散步的傍晚',
    content: '晚风很轻，普通的一天也像被温柔收藏起来。',
    mood: '开心',
    tags: ['散步', '日常'],
    date: '今天 20:18',
    createdAt: '2026-05-26T12:18:00.000Z',
  },
  {
    id: 'diary_002',
    title: '奶油蛋糕和你',
    content: '把蛋糕分成两半，好像连甜味都有了名字。',
    mood: '甜甜的',
    tags: ['约会', '甜品'],
    date: '昨天 16:42',
    createdAt: '2026-05-25T08:42:00.000Z',
  },
];

export async function getDiaryList(params = {}) {
  if (!isMockMode()) {
    try { const { supabase, coupleId } = await getAuthenticatedContext(); requireCouple({ coupleId }); const query = supabase.from('diaries').select('*, diary_attachments(*)').eq('couple_id', coupleId).order('created_at', { ascending: false }); const { data, error } = typeof params.limit === 'number' ? await query.limit(params.limit) : await query; return error ? createApiError(error, '加载日记失败') : createApiResponse(fromDatabase(data)); } catch (error) { return createApiError(error, '加载日记失败'); }
  }

  const { limit } = params;
  const list = typeof limit === 'number' ? mockDiaries.slice(0, limit) : mockDiaries;
  return requestMock(list);
}

export async function getDiaryDetail(id) {
  if (!isMockMode()) {
    try { const { supabase } = await getAuthenticatedContext(); const { data, error } = await supabase.from('diaries').select('*, diary_attachments(*)').eq('id', id).single(); return error ? createApiError(error, '加载日记详情失败') : createApiResponse(fromDatabase(data)); } catch (error) { return createApiError(error, '加载日记详情失败'); }
  }

  const diary = mockDiaries.find((item) => item.id === id) || mockDiaries[0];
  return requestMock(diary);
}

export async function createDiary(payload = {}) {
  if (!isMockMode()) {
    try {
      const context = await getAuthenticatedContext(); const coupleId = requireCouple(context);
      const uploaded = [];
      for (const attachment of payload.attachments || []) {
        const path = `${coupleId}/${context.user.id}/${uniquePathPart()}`;
        const result = await uploadImage('diary-attachments', path, attachment.uri, { contentType: attachment.mimeType });
        if (!result.success) { await Promise.all(uploaded.map((item) => deleteFile('diary-attachments', item.storagePath))); return result; }
        uploaded.push({ storagePath: result.data.path, contentType: attachment.mimeType || 'image/jpeg' });
      }
      const { data, error } = await context.supabase.from('diaries').insert({ couple_id: coupleId, author_id: context.user.id, title: payload.title?.trim() || '今天的小小童话', content: payload.content || '', mood: payload.mood || null, tags: payload.tags || [], is_private: Boolean(payload.isPrivate) }).select('*').single();
      if (error) { await Promise.all(uploaded.map((item) => deleteFile('diary-attachments', item.storagePath))); return createApiError(error, '创建日记失败'); }
      if (uploaded.length) {
        const { error: attachmentError } = await context.supabase.from('diary_attachments').insert(uploaded.map((item) => ({ diary_id: data.id, couple_id: coupleId, uploader_id: context.user.id, storage_path: item.storagePath, content_type: item.contentType })));
        if (attachmentError) { await context.supabase.from('diaries').delete().eq('id', data.id); await Promise.all(uploaded.map((item) => deleteFile('diary-attachments', item.storagePath))); return createApiError(attachmentError, '保存日记附件失败，已回滚'); }
      }
      return createApiResponse(fromDatabase({ ...data, diary_attachments: uploaded }));
    } catch (error) { return createApiError(error, '创建日记失败'); }
  }

  const diary = {
    id: `diary_${Date.now()}`,
    title: payload.title?.trim() || '今天的小小童话',
    content: payload.content?.trim() || '今天的故事，还没有完全写完。',
    mood: payload.mood || '开心',
    tags: payload.tags?.length ? payload.tags : ['日常'],
    date: '刚刚',
    createdAt: new Date().toISOString(),
  };

  return requestMock(diary, 500);
}

export async function updateDiary(id, payload = {}) {
  if (!isMockMode()) {
    try { const { supabase } = await getAuthenticatedContext(); const { data, error } = await supabase.from('diaries').update({ title: payload.title, content: payload.content, mood: payload.mood, tags: payload.tags, is_private: payload.isPrivate }).eq('id', id).select('*').single(); return error ? createApiError(error, '更新日记失败') : createApiResponse(fromDatabase(data)); } catch (error) { return createApiError(error, '更新日记失败'); }
  }

  return requestMock({
    id,
    ...payload,
    updatedAt: new Date().toISOString(),
  }, 400);
}

export async function deleteDiary(id) {
  if (!isMockMode()) {
    try { const { supabase } = await getAuthenticatedContext(); const { data: attachments } = await supabase.from('diary_attachments').select('storage_path').eq('diary_id', id); const { error } = await supabase.from('diaries').delete().eq('id', id); if (error) return createApiError(error, '删除日记失败'); await Promise.all((attachments || []).map((item) => deleteFile('diary-attachments', item.storage_path))); return createApiResponse({ id, deleted: true }); } catch (error) { return createApiError(error, '删除日记失败'); }
  }

  return requestMock({ id, deleted: true }, 300);
}
