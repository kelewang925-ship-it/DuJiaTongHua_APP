import { getAuthenticatedContext, isMockMode } from './client';

export async function subscribeToRealData({ onCoupleChange, onNotification } = {}) {
  if (isMockMode()) return () => {};

  const context = await getAuthenticatedContext();
  const channels = [];
  let active = true;

  const runIfActive = (callback) => (payload) => {
    if (!active) return;
    callback?.(payload);
  };

  if (context.coupleId) {
    channels.push(
      context.supabase
        .channel(`couple:${context.coupleId}:${context.user.id}`)
        .on(
          'postgres_changes',
          { event: '*', schema: 'public', table: '*', filter: `couple_id=eq.${context.coupleId}` },
          runIfActive(onCoupleChange)
        )
        .subscribe()
    );
  }

  channels.push(
    context.supabase
      .channel(`notifications:${context.user.id}`)
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'notifications', filter: `user_id=eq.${context.user.id}` },
        runIfActive(onNotification)
      )
      .subscribe()
  );

  return () => {
    if (!active) return;
    active = false;
    channels.forEach((channel) => context.supabase.removeChannel(channel));
  };
}
