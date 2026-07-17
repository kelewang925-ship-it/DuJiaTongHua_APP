import { createApiError, createApiResponse, normalizeError } from '../api/client';

describe('API response contract', () => {
  test('success response always exposes the four protocol fields', () => {
    expect(createApiResponse({ id: 'one' }, { cached: false })).toEqual({
      success: true,
      data: { id: 'one' },
      meta: { cached: false },
      error: null,
    });
  });

  test('error response is safe for page display', () => {
    const result = createApiError({ message: 'JWT expired', status: 401 }, '登录已失效');
    expect(result.success).toBe(false);
    expect(result.data).toBeNull();
    expect(result.meta).toBeNull();
    expect(result.error).toEqual(expect.objectContaining({
      message: expect.any(String),
      code: expect.any(String),
      category: expect.any(String),
      retryable: expect.any(Boolean),
    }));
  });

  test.each([
    [{ message: 'Failed to fetch' }, 'NETWORK_ERROR', 'network', true],
    [{ message: 'JWT expired', status: 401 }, 'SESSION_EXPIRED', 'session', false],
    [{ message: 'permission denied', status: 403 }, 'PERMISSION_DENIED', 'permission', false],
    [{ message: 'duplicate key value', code: '23505' }, '23505', 'conflict', false],
  ])('normalizes common errors', (input, code, category, retryable) => {
    expect(normalizeError(input)).toEqual(expect.objectContaining({ code, category, retryable }));
  });
});
