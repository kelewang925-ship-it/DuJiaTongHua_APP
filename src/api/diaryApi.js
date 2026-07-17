import { createApiError, createApiResponse, getAuthenticatedContext, isMockMode, requireCouple, requestMock } from './client';
import { compactPayload, fromDatabase } from './mappers';
import { deleteFile, uploadImage, validateStoragePath } from './storageApi';
import { buildStoragePath } from './storagePaths';

const mockDiaries = [
  { id: 'diary_001', title: '一起散步的傍晚', content: '晚风很轻，普通的一天也像被温柔收藏起来。', mood: '开心', tags: ['散步', '日常'], date: '今天 20:18', createdAt: '2026-05-26T12:18:00.000Z' },
  { id: 'diary_002', title: '奶油蛋糕和你', content: '把蛋糕分成两半，好像连甜味都有了名字。', mood: '甜甜的', tags: ['约会', '甜品'], date: '昨天 16:42', createdAt: '2026-05-25T08:42:00.000Z' },
];

async function cleanupAttachments(items = []) {
  const ownedItems = items.filter((item) => item?.storagePath && item.createdByOperation);
  const results = await Promise.all(ownedItems.map((item) => deleteFile('diary-attachments', item.storagePath)));
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

function isOwnedDiary(row, context) {
  const coupleId = row?.coupleId || row?.couple_id;
  const authorId = row?.authorId || row?.author_id;
  return Boolean(row?.id && coupleId === context?.coupleId && authorId === context?.user?.id);
}

export async function getDiaryList(params = {}) {
  if (isMockMode()) return requestMock(typeof params.limit === 'number' ? mockDiaries.slice(0, params.limit) : mockDiaries);
  try {
    const context = await getAuthenticatedContext();
    requireCouple(context);
    let query = context.supabase.from('diaries').select('*, diary_attachments(*)').eq('couple_id', context.coupleId).order('created_at', { ascending: false });
    if (typeof params.limit === 'number') query = query.limit(params.limit);
    const { data, error } = await query;
    if (error) return createApiError(error, '加载日记失败');
    const rows = data || [];
    if (rows.some((item) => (item.couple_id || item.coupleId) !== context.coupleId)) return createApiError('Diary ownership mismatch', '日记列表包含不属于当前情侣空间的数据');
    return createApiResponse(fromDatabase(rows));
  } catch (error) {
    return createApiError(error, '加载日记失败');
  }
}

export async function getDiaryDetail(id) {
  if (isMockMode()) return requestMock(mockDiaries.find((item) => item.id === id) || mockDiaries[0]);
  try {
    if (!id) return createApiError('Missing diary id', '缺少日记标识，无法加载');
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const { data, error } = await context.supabase.from('diaries').select('*, diary_attachments(*)').eq('id', id).eq('couple_id', context.coupleId).maybeSingle();
    if (error) return createApiError(error, '加载日记详情失败');
    if (!data?.id || (data.couple_id || data.coupleId) !== context.coupleId) return createApiError('Diary not found', '日记不存在、无权限或已被删除');
    return createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '加载日记详情失败');
  }
}

export async function createDiary(payload = {}) {
  if (isMockMode()) {
    return requestMock({ id: `diary_${Date.now()}`, title: payload.title?.trim() || '今天的小小童话', content: payload.content?.trim() || '今天的故事，还没有完全写完。', mood: payload.mood || '开心', tags: payload.tags?.length ? payload.tags : ['日常'], date: '刚刚', createdAt: new Date().toISOString() }, 500);
  }

  const uploaded = [];
  try {
    const context = await getAuthenticatedContext();
    const coupleId = requireCouple(context);
    const sourceAttachments = payload.attachments || [];
    if (sourceAttachments.length > 3) return createApiError('Too many attachments', '一篇日记最多添加 3 张图片');

    for (const attachment of sourceAttachments) {
      if (attachment.storagePath) {
        validateStoragePath('diary-attachments', attachment.storagePath, context);
        uploaded.push({
          storagePath: attachment.storagePath,
          contentType: attachment.mimeType || attachment.contentType || 'image/jpeg',
          createdByOperation: false,
        });
        continue;
      }
      if (!attachment.uri) {
        const cleanupFailures = await cleanupAttachments(uploaded);
        return createApiError('Missing attachment URI', '存在无法读取的日记附件', {
          cleanupRequired: cleanupFailures.length > 0,
          failedCleanupCount: cleanupFailures.length,
        });
      }
      const path = buildStoragePath(coupleId, context.user.id);
      const result = await uploadImage('diary-attachments', path, attachment.uri, { contentType: attachment.mimeType });
      if (!result.success) {
        const cleanupFailures = await cleanupAttachments(uploaded);
        return withCleanupMeta(result, cleanupFailures);
      }
      uploaded.push({
        storagePath: result.data.path,
        contentType: attachment.mimeType || 'image/jpeg',
        createdByOperation: true,
      });
    }

    const { data, error } = await context.supabase.from('diaries').insert({
      couple_id: coupleId,
      author_id: context.user.id,
      title: payload.title?.trim() || '今天的小小童话',
      content: payload.content || '',
      mood: payload.mood || null,
      tags: payload.tags || [],
      is_private: Boolean(payload.isPrivate),
    }).select('*').maybeSingle();

    if (error || !isOwnedDiary(data, context)) {
      const cleanupFailures = await cleanupAttachments(uploaded);
      return createApiError(error || 'Diary write mismatch', '创建日记失败，服务端未确认写入结果', {
        cleanupRequired: cleanupFailures.length > 0,
        failedCleanupCount: cleanupFailures.length,
      });
    }

    if (uploaded.length) {
      const { error: attachmentError } = await context.supabase.from('diary_attachments').insert(uploaded.map((item) => ({ diary_id: data.id, couple_id: coupleId, uploader_id: context.user.id, storage_path: item.storagePath, content_type: item.contentType })));
      if (attachmentError) {
        const { error: rollbackError } = await context.supabase.from('diaries').delete().eq('id', data.id).eq('author_id', context.user.id).eq('couple_id', coupleId);
        const cleanupFailures = await cleanupAttachments(uploaded);
        return createApiError(attachmentError, '保存日记附件失败，已尝试回滚日记', {
          cleanupRequired: Boolean(rollbackError) || cleanupFailures.length > 0,
          failedCleanupCount: cleanupFailures.length,
        });
      }
    }

    return createApiResponse(fromDatabase({ ...data, diary_attachments: uploaded.map((item) => ({ storage_path: item.storagePath, content_type: item.contentType })) }));
  } catch (error) {
    const cleanupFailures = await cleanupAttachments(uploaded);
    return createApiError(error, '创建日记失败', {
      cleanupRequired: cleanupFailures.length > 0,
      failedCleanupCount: cleanupFailures.length,
    });
  }
}

export async function updateDiary(id, payload = {}) {
  if (isMockMode()) return requestMock({ id, ...payload, updatedAt: new Date().toISOString() }, 400);
  try {
    if (!id) return createApiError('Missing diary id', '缺少日记标识，无法保存');
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const values = compactPayload({ title: payload.title?.trim(), content: payload.content, mood: payload.mood, tags: payload.tags, is_private: payload.isPrivate });
    if (!Object.keys(values).length) return createApiError('Empty diary update', '没有可保存的日记修改');
    if (values.title === '') return createApiError('Missing diary title', '日记标题不能为空');
    const { data, error } = await context.supabase.from('diaries').update(values).eq('id', id).eq('author_id', context.user.id).eq('couple_id', context.coupleId).select('*').maybeSingle();
    if (error) return createApiError(error, '更新日记失败');
    if (!isOwnedDiary(data, context)) return createApiError('Diary not updated', '日记不存在、无权限或已被删除');
    return createApiResponse(fromDatabase(data));
  } catch (error) {
    return createApiError(error, '更新日记失败');
  }
}

export async function deleteDiary(id) {
  if (isMockMode()) return requestMock({ id, deleted: true }, 300);
  try {
    if (!id) return createApiError('Missing diary id', '缺少日记标识，无法删除');
    const context = await getAuthenticatedContext();
    requireCouple(context);
    const { data: attachments, error: attachmentQueryError } = await context.supabase.from('diary_attachments').select('storage_path').eq('diary_id', id).eq('couple_id', context.coupleId).eq('uploader_id', context.user.id);
    if (attachmentQueryError) return createApiError(attachmentQueryError, '读取日记附件失败');

    const { data: deleted, error } = await context.supabase.from('diaries').delete().eq('id', id).eq('author_id', context.user.id).eq('couple_id', context.coupleId).select('id, couple_id, author_id').maybeSingle();
    if (error) return createApiError(error, '删除日记失败');
    if (!isOwnedDiary(deleted, context)) return createApiError('Diary not deleted', '日记不存在、无权限或已被删除');

    const persistedAttachments = (attachments || []).map((item) => ({ storagePath: item.storage_path, createdByOperation: true }));
    const cleanupFailures = await cleanupAttachments(persistedAttachments);
    if (cleanupFailures.length) return createApiError('Attachment cleanup failed', '日记已删除，但部分附件清理失败', { cleanupRequired: true, failedCount: cleanupFailures.length });
    return createApiResponse({ id: deleted.id, deleted: true });
  } catch (error) {
    return createApiError(error, '删除日记失败');
  }
}