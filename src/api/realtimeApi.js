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

export async function subscribeToRealData({ onCoupleChange, onNotification, onStatus } = {}) {
  if (isMockMode()) return () => {};

  const context = await getAuthenticatedContext();
  const channels = [];
  let active = true;

  const runIfActive = (callback) => (...args) => {
    if (!active) return;
    callback?.(...args);
  };

  if (context.coupleId) {
    COUPLE_REALTIME_TARGETS.forEach(({ table, filterColumn }) => {
      const channel = context.supabase
        .channel(`couple:${context.coupleId}:${context.user.id}:${table}`)
        .on(
          'postgres_changes',
          { event: '*', schema: 'public', table, filter: `${filterColumn}=eq.${context.coupleId}` },
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
