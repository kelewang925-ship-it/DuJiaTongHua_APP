import { useEffect, useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import FairyCard from '@/components/FairyCard';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyPage from '@/components/FairyPage';
import FairyRequestState from '@/components/FairyRequestState';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import { getApiMode } from '@/api/client';
import useFairyStore from '@/store/useFairyStore';

const filters = ['全部', '互动', 'AI', '纪念日', '系统', '其他'];
const noticeSeed = [
  { id: 'notice-like', type: '互动', icon: 'heart', title: 'TA 喜欢了你的日记', subject: '晚霞散步', text: '这天的风真的很温柔。', time: '刚刚', read: false, target: '/couple/activity-detail', color: '#F5A3A8' },
  { id: 'notice-comment', type: '互动', icon: 'chatbubble-ellipses', title: '新的评论', subject: '晚霞散步', text: '下次还要一起去', time: '10 分钟前', read: false, target: '/comments', color: '#E7B9B6' },
  { id: 'notice-capsule', type: '系统', icon: 'mail-open', title: '时光胶囊提醒', subject: '写给未来的信快到开启日了', text: '2026.12.31 即将到来。', time: '昨天', read: false, target: '/time-capsule/settings', color: '#D8B384' },
  { id: 'notice-ai', type: 'AI', icon: 'color-wand', title: 'AI 漫画已完成', subject: '雨后散步', text: '快去看看你们的专属漫画吧。', time: '昨天', read: true, target: '/ai/history', color: '#C5AED3' },
  { id: 'notice-anniversary', type: '纪念日', icon: 'calendar', title: '纪念日还有 18 天', subject: '我们在一起纪念日', text: '一起期待这一天的到来吧。', time: '昨天', read: true, target: '/anniversary/countdown', color: '#EAB765' },
];

const noticePresentation = {
  互动: { icon: 'chatbubble-ellipses', color: '#E7B9B6' },
  AI: { icon: 'color-wand', color: '#C5AED3' },
  纪念日: { icon: 'calendar', color: '#EAB765' },
  系统: { icon: 'notifications-outline', color: '#D8B384' },
  其他: { icon: 'mail-outline', color: '#9A8D88' },
};

function mapNoticeType(value) {
  if (value === 'anniversary') return '纪念日';
  if (value === 'system') return '系统';
  if (value === 'ai') return 'AI';
  if (value === 'interaction' || value === 'like' || value === 'comment') return '互动';
  return '其他';
}

function formatNoticeTime(value) {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '';
  return date.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
}

export default function NotificationsPage() {
  const router = useRouter();
  const isReal = getApiMode() === 'real';
  const realNotices = useFairyStore((state) => state.notifications) || [];
  const loading = useFairyStore((state) => Boolean(state.loading?.notifications || state.loading?.bootstrap || state.loading?.modules));
  const loadError = useFairyStore((state) => state.errors?.notifications || state.errors?.bootstrap || state.errors?.modules || null);
  const refreshNotifications = useFairyStore((state) => state.refreshNotifications);
  const markNotificationRead = useFairyStore((state) => state.markNotificationRead);
  const markAllNotificationsRead = useFairyStore((state) => state.markAllNotificationsRead);
  const [mockNotices, setMockNotices] = useState(noticeSeed);
  const notices = isReal ? realNotices.map((item) => {
    const type = mapNoticeType(item.type);
    const presentation = noticePresentation[type];
    return {
      ...item,
      type,
      read: Boolean(item.readAt),
      text: item.content || '',
      time: formatNoticeTime(item.createdAt),
      subject: item.targetType || '',
      icon: presentation.icon,
      color: presentation.color,
      target: null,
    };
  }) : mockNotices;
  const [activeFilter, setActiveFilter] = useState('全部');
  const [submitting, setSubmitting] = useState(false);
  const [toast, setToast] = useState(null);
  useEffect(() => {
    if (isReal) refreshNotifications();
  }, [isReal, refreshNotifications]);
  const unreadCount = notices.filter((item) => !item.read).length;
  const visibleNotices = useMemo(() => activeFilter === '全部' ? notices : notices.filter((item) => item.type === activeFilter), [activeFilter, notices]);

  const markAllRead = async () => {
    if (submitting || loading || loadError) return;
    if (!unreadCount) {
      setToast({ tone: 'success', message: '暂时没有新的未读通知。' });
      return;
    }
    if (isReal) {
      setSubmitting(true);
      const result = await markAllNotificationsRead();
      setSubmitting(false);
      if (!result.success) {
        setToast({ tone: 'error', message: result.error?.message || '通知状态更新失败。' });
        return;
      }
    } else {
      setMockNotices((items) => items.map((item) => ({ ...item, read: true })));
    }
    setToast({ tone: 'success', message: '所有通知都已标记为已读。' });
  };

  const openNotice = async (notice) => {
    if (submitting) return;
    if (isReal && !notice.read) {
      setSubmitting(true);
      const result = await markNotificationRead(notice.id);
      setSubmitting(false);
      if (!result.success) {
        setToast({ tone: 'error', message: result.error?.message || '通知状态更新失败。' });
        return;
      }
    } else if (!isReal) {
      setMockNotices((items) => items.map((item) => item.id === notice.id ? { ...item, read: true } : item));
    }
    if (notice.target) router.push(notice.target);
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="互动通知" right={<Pressable accessibilityRole="button" disabled={submitting || loading || Boolean(loadError)} onPress={markAllRead} style={({ pressed }) => [styles.readAll, (pressed || submitting) && styles.pressed]}><Text style={styles.readAllText}>{submitting ? '处理中' : '全部已读'}</Text></Pressable>} />}
      topSpace={28}
      bottomSpace={60}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
    >
      <View style={styles.content}>
        {!loading && !loadError ? <View style={styles.intro}><Text style={styles.introTitle}>每一次互动，都是童话里的星光</Text><Text style={styles.introText}>{unreadCount ? `有 ${unreadCount} 条新通知等你查看` : '当前没有未读通知'}</Text></View> : null}

        {isReal ? <FairyRequestState loading={loading} error={loadError} onRetry={refreshNotifications} /> : null}
        {!loading && !loadError ? (
          <>
            <View style={styles.filterRow}>
              {filters.map((filter) => <Pressable key={filter} accessibilityRole="button" accessibilityState={{ selected: activeFilter === filter }} onPress={() => setActiveFilter(filter)} style={({ pressed }) => [styles.filterChip, activeFilter === filter && styles.filterChipActive, pressed && styles.pressed]}><Text style={[styles.filterText, activeFilter === filter && styles.filterTextActive]}>{filter}</Text></Pressable>)}
            </View>

            {visibleNotices.length ? (
              <View style={styles.list}>
                {visibleNotices.map((item) => (
                  <FairyCard key={item.id} onPress={() => openNotice(item)} style={[styles.noticeCard, item.read && styles.noticeCardRead]} padding={spacing.lg} accessibilityRole="button">
                    <View style={[styles.noticeIcon, { backgroundColor: `${item.color}22` }]}><Ionicons name={item.icon} size={26} color={item.color} /></View>
                    <View style={styles.noticeBody}>
                      <View style={styles.noticeTop}><Text style={styles.noticeTitle}>{item.title || '未命名通知'}</Text>{item.time ? <Text style={styles.noticeTime}>{item.time}</Text> : null}{!item.read ? <View style={styles.unreadDot} /> : null}</View>
                      {item.subject ? <Text style={styles.noticeSubject}>{item.subject}</Text> : null}
                      {item.text ? <Text style={styles.noticeText}>{item.text}</Text> : null}
                      <View style={styles.noticeFooter}><View style={styles.typeTag}><Text style={styles.typeText}>{item.type}</Text></View>{item.target ? <Ionicons name="chevron-forward" size={17} color={colors.textSoft} /> : <Text style={styles.noTargetText}>仅通知</Text>}</View>
                    </View>
                  </FairyCard>
                ))}
              </View>
            ) : <FairyEmptyState imageName="emptyNotification" title="暂无通知" description={activeFilter === '全部' ? '当前账号还没有收到通知。' : `当前没有“${activeFilter}”类型的通知。`} actionTitle={activeFilter === '全部' ? undefined : '回到全部'} onAction={activeFilter === '全部' ? undefined : () => setActiveFilter('全部')} />}
          </>
        ) : null}

        <View style={styles.footer}><Ionicons name="mail-outline" size={28} color={colors.gold} /><Text style={styles.footerText}>{isReal ? '通知内容来自当前账号的服务端记录' : 'Mock 模式展示本地演示通知'}</Text></View>
      </View>
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 760 }, pressed: { opacity: 0.65 },
  readAll: { minWidth: 62, minHeight: 44, alignItems: 'flex-end', justifyContent: 'center' }, readAllText: { color: colors.primaryDeep, fontSize: 12, fontWeight: '900' },
  intro: { alignItems: 'center', marginBottom: spacing.xl }, introTitle: { color: colors.text, fontSize: 18, fontWeight: '900', textAlign: 'center' }, introText: { color: colors.textSoft, fontSize: 12, marginTop: spacing.sm },
  filterRow: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', gap: spacing.sm, marginBottom: spacing.xl }, filterChip: { minHeight: 40, paddingHorizontal: spacing.xl, borderRadius: 18, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card }, filterChipActive: { borderColor: colors.primaryDeep, backgroundColor: colors.primary }, filterText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' }, filterTextActive: { color: colors.white },
  list: { gap: spacing.md }, noticeCard: { flexDirection: 'row', gap: spacing.lg, backgroundColor: 'rgba(255,249,244,0.96)' }, noticeCardRead: { opacity: 0.68 }, noticeIcon: { width: 58, height: 58, borderRadius: 22, alignItems: 'center', justifyContent: 'center' }, noticeBody: { flex: 1, minWidth: 0 },
  noticeTop: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm }, noticeTitle: { flex: 1, color: colors.text, fontSize: 16, fontWeight: '900' }, noticeTime: { color: colors.textSoft, fontSize: 11 }, unreadDot: { width: 9, height: 9, borderRadius: 5, backgroundColor: '#E96B70' },
  noticeSubject: { color: colors.primaryDeep, fontSize: 13, fontWeight: '900', marginTop: spacing.sm }, noticeText: { color: colors.textSoft, lineHeight: 20, marginTop: 4 }, noticeFooter: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: spacing.md }, typeTag: { paddingHorizontal: spacing.md, paddingVertical: 4, borderRadius: 12, backgroundColor: colors.cardPink }, typeText: { color: colors.accent, fontSize: 10, fontWeight: '900' }, noTargetText: { color: colors.textSoft, fontSize: 10, fontWeight: '800' },
  footer: { alignItems: 'center', gap: spacing.sm, marginTop: spacing.xxl }, footerText: { color: colors.textSoft, fontSize: 12, textAlign: 'center' },
});
