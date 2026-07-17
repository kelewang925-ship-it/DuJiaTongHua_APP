import { deriveHomeRelationshipView, deriveLoveDays } from '../utils/homeRelationshipView';

describe('home relationship view', () => {
  const now = new Date('2026-07-18T12:00:00.000Z');

  test('Real mode accepts couple=null without throwing or inventing a relationship', () => {
    expect(() => deriveHomeRelationshipView(null, { isReal: true, now })).not.toThrow();
    expect(deriveHomeRelationshipView(null, { isReal: true, now })).toEqual(expect.objectContaining({
      bound: false,
      relation: null,
      loveDays: null,
      spaceName: '',
    }));
  });

  test('Real active wrapper derives relationship data from the nested relation', () => {
    const view = deriveHomeRelationshipView({
      user: { id: 'user-b', nickname: '小满' },
      partner: { id: 'user-a', nickname: '星河' },
      couple: { id: 'couple-1', status: 'active', startedAt: '2026-07-17' },
      status: 'active',
    }, { isReal: true, now });

    expect(view).toEqual(expect.objectContaining({
      bound: true,
      loveDays: 2,
      userName: '小满',
      partnerName: '星河',
      statusText: '已绑定',
      spaceName: '空间名称未提供',
    }));
  });

  test('Real unbound wrapper stays unbound and exposes no Mock relationship fields', () => {
    const view = deriveHomeRelationshipView({
      user: { id: 'user-b', nickname: '小满' },
      partner: null,
      couple: null,
      status: 'unbound',
    }, { isReal: true, now });

    expect(view.bound).toBe(false);
    expect(view.loveDays).toBeNull();
    expect(view.spaceName).toBe('');
  });

  test.each([undefined, '', 'not-a-date', '2026-02-30', '2026-07-19'])('missing, invalid or future startedAt %p never fabricates love days', (startedAt) => {
    expect(deriveLoveDays(startedAt, now)).toBeNull();
  });

  test('Mock mode preserves the existing flattened demonstration fields', () => {
    const mock = {
      loveDays: 428,
      statusText: '今天也被好好爱着',
      spaceName: '我们的小小宇宙',
      userName: '林小满',
      partnerName: '陆星河',
    };

    expect(deriveHomeRelationshipView(mock, { isReal: false, now })).toEqual(expect.objectContaining(mock));
  });
});
