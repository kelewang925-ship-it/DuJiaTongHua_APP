import { normalizeDateOnly } from '../api/mappers';

const DAY_MS = 86400000;

export function deriveLoveDays(value, now = new Date()) {
  const normalized = normalizeDateOnly(value);
  if (!normalized) return null;

  const [year, month, day] = normalized.split('-').map(Number);
  const startUtc = Date.UTC(year, month - 1, day);
  const current = now instanceof Date ? now : new Date(now);
  if (Number.isNaN(current.getTime())) return null;
  const currentUtc = Date.UTC(current.getUTCFullYear(), current.getUTCMonth(), current.getUTCDate());
  if (startUtc > currentUtc) return null;
  return Math.floor((currentUtc - startUtc) / DAY_MS) + 1;
}

export function deriveHomeRelationshipView(coupleState, { isReal, now = new Date() } = {}) {
  if (!isReal) {
    return {
      bound: Boolean(coupleState),
      loveDays: coupleState?.loveDays ?? null,
      statusText: coupleState?.statusText || '',
      spaceName: coupleState?.spaceName || '',
      userName: coupleState?.userName || '',
      partnerName: coupleState?.partnerName || '',
      relation: coupleState || null,
    };
  }

  const relation = coupleState?.couple || null;
  const relationshipStatus = relation?.status || coupleState?.status || null;
  const bound = Boolean(relation?.id && relationshipStatus === 'active');
  const userName = coupleState?.user?.nickname || '';
  const partnerName = coupleState?.partner?.nickname || '';
  const explicitSpaceName = typeof relation?.spaceName === 'string' ? relation.spaceName.trim() : '';

  return {
    bound,
    relation,
    loveDays: bound ? deriveLoveDays(relation?.startedAt, now) : null,
    statusText: bound ? '已绑定' : relationshipStatus === 'pending' ? '等待绑定' : '',
    spaceName: bound ? (explicitSpaceName || '空间名称未提供') : '',
    userName,
    partnerName,
  };
}
