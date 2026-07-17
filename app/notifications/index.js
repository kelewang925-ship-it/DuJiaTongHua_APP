import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import FairyCard from '@/components/FairyCard';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyPage from '@/components/FairyPage';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';

const filters = ['全部', '互动', 'AI', '纪念日', '系统'];
const noticeSeed = [
  { id: 'notice-like', type: '互动', icon: 'heart', title: 'TA 喜欢了你的日记', subject: '晚霞散步', text: '这天的风真的很温柔。', time: '刚刚', read: false, target: '/couple/activity-detail', color: '#F5A3A8' },
  { id: 'notice-comment', type: '互动', icon: 'chatbubble-ellipses', title: '新的评论', subject: '晚霞散步', text: '下次还要一起去 ✨', time: '10 分钟前', read: false, target: '/comments', color: '#E7B9B6' },
  { id: 'notice-capsule', type: '系统', icon: 'mail-open', title: '时光胶囊提醒', subject: '写给未来的信快到开启日了', text: '2026.12.31 即将到来。', time: '昨天', read: false, target: '/time-capsule/settings', color: '#D8B384' },
  { id: 'notice-ai', type: 'AI', icon: 'color-wand', title: 'AI 漫画已完成', subject: '雨后散步', text: '快去看看你们的专属漫画吧～', time: '昨天', read: true, target: '/ai/history', color: '#C5AED3' },
  { id: 'notice-anniversary', type: '纪念日', icon: 'calendar', title: '纪念日还有 18 天', subject: '我们在一起纪念日', text: '一起期待这一天的到来吧。', time: '昨天', read: true, target: '/anniversary/countdown', color: '#EAB765' },
];

export default function NotificationsPage() {
  const router = useRouter();
  const [notices, setNotices] = useState(noticeSeed);
  const [activeFilter, setActiveFilter] = useState('全部');
  const [toast, setToast] = useState(null);
  const unreadCount = notices.filter((item) => !item.read).length;
  const visibleNotices = useMemo(() => activeFilter === '全部' ? notices : notices.filter((item) => item.type === activeFilter), [activeFilter, notices]);

  const markAllRead = () => {
    setNotices((items) => items.map((item) => ({ ...item, read: true })));
    setToast({ tone: 'success', message: unreadCount ? '所有互动便签都已读。' : '暂时没有新的未读通知。' });
  };

  const openNotice = (notice) => {
    setNotices((items) => items.map((item) => item.id === notice.id ? { ...item, read: true } : item));
    if (notice.target) router.push(notice.target);
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="互动通知" right={<Pressable accessibilityRole="button" onPress={markAllRead} style={({ pressed }) => [styles.readAll, pressed && styles.pressed]}><Text style={styles.readAllText}>全部已读</Text></Pressable>} />}
      topSpace={28}
      bottomSpace={60}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
    >
      <View style={styles.content}>
        <View style={styles.intro}><Text style={styles.introTitle}>每一次互动，都是童话里的星光</Text><Text style={styles.introText}>{unreadCount ? `有 ${unreadCount} 张新便签等你打开` : '今天的小信箱已经全部读完'}</Text></View>

        <View style={styles.filterRow}>
          {filters.map((filter) => <Pressable key={filter} accessibilityRole="button" accessibilityState={{ selected: activeFilter === filter }} onPress={() => setActiveFilter(filter)} style={({ pressed }) => [styles.filterChip, activeFilter === filter && styles.filterChipActive, pressed && styles.pressed]}><Text style={[styles.filterText, activeFilter === filter && styles.filterTextActive]}>{filter}</Text></Pressable>)}
        </View>

        {visibleNotices.length ? (
          <View style={styles.list}>
            {visibleNotices.map((item) => (
              <FairyCard key={item.id} onPress={() => openNotice(item)} style={[styles.noticeCard, item.read && styles.noticeCardRead]} padding={spacing.lg} accessibilityRole="button">
                <View style={[styles.noticeIcon, { backgroundColor: `${item.color}22` }]}><Ionicons name={item.icon} size={26} color={item.color} /></View>
                <View style={styles.noticeBody}>
                  <View style={styles.noticeTop}><Text style={styles.noticeTitle}>{item.title}</Text><Text style={styles.noticeTime}>{item.time}</Text>{!item.read ? <View style={styles.unreadDot} /> : null}</View>
                  <Text style={styles.noticeSubject}>{item.subject}</Text>
                  <Text style={styles.noticeText}>{item.text}</Text>
                  <View style={styles.noticeFooter}><View style={styles.typeTag}><Text style={styles.typeText}>{item.type}</Text></View><Ionicons name="chevron-forward" size={17} color={colors.textSoft} /></View>
                </View>
              </FairyCard>
            ))}
          </View>
        ) : <FairyEmptyState imageName="emptyNotification" title="这格小信箱暂时安静" description="换一个筛选看看，新的互动和提醒会很快落在这里。" actionTitle="回到全部" onAction={() => setActiveFilter('全部')} />}

        <View style={styles.footer}><Ionicons name="mail-outline" size={28} color={colors.gold} /><Text style={styles.footerText}>你们的每一次互动，都会被温柔收藏。</Text></View>
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
  noticeSubject: { color: colors.primaryDeep, fontSize: 13, fontWeight: '900', marginTop: spacing.sm }, noticeText: { color: colors.textSoft, lineHeight: 20, marginTop: 4 }, noticeFooter: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: spacing.md }, typeTag: { paddingHorizontal: spacing.md, paddingVertical: 4, borderRadius: 12, backgroundColor: colors.cardPink }, typeText: { color: colors.accent, fontSize: 10, fontWeight: '900' },
  footer: { alignItems: 'center', gap: spacing.sm, marginTop: spacing.xxl }, footerText: { color: colors.textSoft, fontSize: 12, textAlign: 'center' },
});
