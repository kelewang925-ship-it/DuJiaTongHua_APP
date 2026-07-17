import { getAuthenticatedContext, isMockMode } from './client';

const COUPLE_REALTIME_TABLES = Object.freeze([
  'couples',
  'diaries',
  'diary_attachments',
  'photo_collections',
  'photos',
  'anniversaries',
  'custom_tags',
  'time_capsules',
  'comments',
]);

export async function subscribeToRealData({ onCoupleChange, onNotification, onStatus } = {}) {
  if (isMockMode()) return () => {};

  const context = await getAuthenticatedContext();
  const channels = [];
  let active = true;

  const runIfActive = (callback) => (payload) => {
    if (!active) return;
    callback?.(payload);
  };

  if (context.coupleId) {
    COUPLE_REALTIME_TABLES.forEach((table) => {
      const channel = context.supabase
        .channel(`couple:${context.coupleId}:${context.user.id}:${table}`)
        .on(
          'postgres_changes',
          { event: '*', schema: 'public', table, filter: `couple_id=eq.${context.coupleId}` },
          runIfActive(onCoupleChange)
        )
        .subscribe(runIfActive((status, error) => onStatus?.({ scope: 'couple', table, status, error })));
      channels.push(channel);
    });
  }

  const notificationChannel = context.supabase
    .channel(`notifications:${context.user.id}`)
    .on(
      'postgres_changes',
      { event: '*', schema: 'public', table: 'notifications', filter: `user_id=eq.${context.user.id}` },
      runIfActive(onNotification)
    )
    .subscribe(runIfActive((status, error) => onStatus?.({ scope: 'notifications', table: 'notifications', status, error })));
  channels.push(notificationChannel);

  return () => {
    if (!active) return;
    active = false;
    channels.forEach((channel) => context.supabase.removeChannel(channel));
  };
}
