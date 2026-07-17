import { createApiError, createApiResponse, normalizeError } from '../api/client';

describe('API protocol', () => {
  test('success responses always expose the complete envelope', () => {
    expect(createApiResponse({ id: '1' }, { source: 'test' })).toEqual({
      success: true,
      data: { id: '1' },
      meta: { source: 'test' },
      error: null,
    });
  });

  test('error responses always expose the complete envelope', () => {
    const result = createApiError({ message: 'denied', code: '42501' }, 'fallback');
    expect(result.success).toBe(false);
    expect(result.data).toBeNull();
    expect(result.meta).toBeNull();
    expect(result.error.message).toBe('denied');
    expect(result.error.code).toBe('42501');
  });

  test.each([
    [{ message: 'JWT expired', status: 401 }, 'SESSION_EXPIRED'],
    [{ message: 'permission denied', code: '42501' }, 'PERMISSION_DENIED'],
    [{ message: 'Failed to fetch', name: 'TypeError' }, 'NETWORK_ERROR'],
    [{ message: 'duplicate key value', code: '23505' }, 'CONFLICT'],
  ])('normalizes operational error %p', (input, expectedCode) => {
    expect(normalizeError(input).code).toBe(expectedCode);
  });

  test('keeps a page-displayable fallback message', () => {
    expect(normalizeError(null, '请稍后重试').message).toBe('请稍后重试');
  });
});
