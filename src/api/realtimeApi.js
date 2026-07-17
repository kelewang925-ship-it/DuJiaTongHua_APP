import { getAuthenticatedContext, isMockMode } from './client';

const COUPLE_REALTIME_TARGETS = Object.freeze([
  { table: 'couples', filterColumn: 'id' },
  { table: 'diaries', filterColumn: 'couple_id' },
  { table: 'diary_attachments', filterColumn: 'couple_id' },
  { table: 'photo_collections', filterColumn: 'couple_id' },
  { table: 'photos', filterColumn: 'couple_id' },
  { table: 'anniversaries', filterColumn: 'couple_id' },
  { table: 'custom_tags', filterColumn: 'couple_id' },
  { table: 'time_capsules', filterColumn: 'couple_id' },
  { table: 'comments', filterColumn: 'couple_id' },
]);

const REALTIME_FAILURE_STATUSES = new Set(['CHANNEL_ERROR', 'TIMED_OUT', 'CLOSED']);

function createStatusPayload(scope, table, status, error) {
  const failed = REALTIME_FAILURE_STATUSES.has(status);
  return {
    scope,
    table,
    status,
    connected: status === 'SUBSCRIBED',
    failed,
    error: failed ? error || new Error(`Realtime ${table} subscription ${status}`) : null,
  };
}

export async function subscribeToRealData({ onCoupleChange, onNotification, onStatus } = {}) {
  if (isMockMode()) return () => {};

  const context = await getAuthenticatedContext();
  const channels = [];
  let active = true;

  const runIfActive = (callback) => (...args) => {
    if (!active) return;
    callback?.(...args);
  };

  const subscribeWithStatus = (channel, scope, table) => channel.subscribe(runIfActive((status, error) => {
    onStatus?.(createStatusPayload(scope, table, status, error));
  }));

  if (context.coupleId) {
    COUPLE_REALTIME_TARGETS.forEach(({ table, filterColumn }) => {
      const channel = context.supabase
        .channel(`couple:${context.coupleId}:${context.user.id}:${table}`)
        .on(
          'postgres_changes',
          { event: '*', schema: 'public', table, filter: `${filterColumn}=eq.${context.coupleId}` },
          runIfActive(onCoupleChange)
        );
      channels.push(subscribeWithStatus(channel, 'couple', table));
    });
  }

  const notificationChannel = context.supabase
    .channel(`notifications:${context.user.id}`)
    .on(
      'postgres_changes',
      { event: '*', schema: 'public', table: 'notifications', filter: `user_id=eq.${context.user.id}` },
      runIfActive(onNotification)
    );
  channels.push(subscribeWithStatus(notificationChannel, 'notifications', 'notifications'));

  return () => {
    if (!active) return;
    active = false;
    channels.forEach((channel) => context.supabase.removeChannel(channel));
  };
}