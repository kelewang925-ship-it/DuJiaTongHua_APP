import { createApiError, createApiResponse, normalizeError, withRequestTimeout } from '../api/client';

describe('API protocol', () => {
  test('success responses always expose the complete envelope', () => {
    expect(createApiResponse({ id: '1' }, { source: 'test' })).toEqual({
      success: true,
      data: { id: '1' },
      meta: { source: 'test' },
      error: null,
    });
  });

  test('error responses expose normalized public codes and retain raw details', () => {
    const input = { message: 'denied', code: '42501' };
    const result = createApiError(input, 'fallback');
    expect(result.success).toBe(false);
    expect(result.data).toBeNull();
    expect(result.meta).toBeNull();
    expect(result.error.message).toBe('当前账号没有权限执行此操作');
    expect(result.error.code).toBe('PERMISSION_DENIED');
    expect(result.error.category).toBe('permission');
    expect(result.error.raw).toBe(input);
  });

  test.each([
    [{ message: 'JWT expired', status: 401 }, 'SESSION_EXPIRED'],
    [{ message: 'permission denied', code: '42501' }, 'PERMISSION_DENIED'],
    [{ message: 'Failed to fetch', name: 'TypeError' }, 'NETWORK_ERROR'],
    [{ message: 'duplicate key value', code: '23505' }, 'CONFLICT'],
  ])('normalizes operational error %p', (input, expectedCode) => {
    expect(normalizeError(input).code).toBe(expectedCode);
  });

  test('returns a retryable network error when a guarded request times out', async () => {
    await expect(withRequestTimeout(new Promise(() => {}), 1, '请求超时')).rejects.toMatchObject({
      code: 'NETWORK_TIMEOUT',
      message: '请求超时',
    });
    expect(normalizeError({ code: 'NETWORK_TIMEOUT', message: '请求超时' })).toEqual(expect.objectContaining({
      code: 'NETWORK_ERROR',
      category: 'network',
      retryable: true,
    }));
  });

  test('keeps a page-displayable fallback message', () => {
    expect(normalizeError(null, '请稍后重试').message).toBe('请稍后重试');
  });
});
