import { getAuthenticatedContext, isMockMode } from './client';

export async function subscribeToRealData({ onCoupleChange, onNotification } = {}) {
  if (isMockMode()) return () => {};
  const c = await getAuthenticatedContext();
  const channels = [];
  if (c.coupleId) {
    channels.push(c.supabase.channel(`couple:${c.coupleId}`).on('postgres_changes', { event: '*', schema: 'public', table: '*', filter: `couple_id=eq.${c.coupleId}` }, onCoupleChange || (() => {})).subscribe());
  }
  channels.push(c.supabase.channel(`notifications:${c.user.id}`).on('postgres_changes', { event: '*', schema: 'public', table: 'notifications', filter: `user_id=eq.${c.user.id}` }, onNotification || (() => {})).subscribe());
  return () => { channels.forEach((channel) => c.supabase.removeChannel(channel)); };
}
