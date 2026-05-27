import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import FairyCard from '../../src/components/FairyCard';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyHeader from '../../src/components/FairyHeader';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';

const filters = ['全部', '互动', 'AI', '纪念日', '系统'];

const noticeSeed = [
  {
    id: 'notice-like',
    type: '互动',
    event: 'like',
    icon: 'heart-outline',
    title: '小满喜欢了你的那篇日记',
    text: '“雨后便利店”这一页被她悄悄贴了小爱心。',
    time: '刚刚',
    read: false,
    tone: undefined,
    target: '/couple/activity-detail',
  },
  {
    id: 'notice-comment',
    type: '互动',
    event: 'comment',
    icon: 'chatbubble-ellipses-outline',
    title: '星河留下了一句悄悄话',
    text: '“下次还走这条路，顺便买热可可。”',
    time: '12 分钟前',
    read: false,
    tone: undefined,
    target: '/comments',
  },
  {
    id: 'notice-ai',
    type: 'AI',
    event: 'ai_done',
    icon: 'sparkles-outline',
    title: '童话工坊的漫画已经完成',
    text: '《第一次坐末班车》正在等你们翻开。',
    time: '今天 15:20',
    read: true,
    tone: 'gold',
    target: '/(tabs)/workshop',
  },
  {
    id: 'notice-anniversary',
    type: '纪念日',
    event: 'anniversary',
    icon: 'calendar-outline',
    title: '纪念日小铃铛',
    text: '第一次旅行还有 24 天，可以准备一张手写小卡片。',
    time: '昨天',
    read: true,
    tone: undefined,
    target: '/anniversary',
  },
  {
    id: 'notice-system',
    type: '系统',
    event: 'system',
    icon: 'notifications-outline',
    title: '夜间提醒已切换为轻声模式',
    text: '系统会在 22:00 后只保留重要提示，守住你们的安静时光。',
    time: '昨天',
    read: false,
    tone: undefined,
    target: '/settings',
  },
];

export default function NotificationsPage() {
  const router = useRouter();
  const [notices, setNotices] = useState(noticeSeed);
  const [activeFilter, setActiveFilter] = useState('全部');

  const unreadCount = notices.filter((item) => !item.read).length;
  const visibleNotices = useMemo(() => {
    if (activeFilter === '全部') return notices;
    return notices.filter((item) => item.type === activeFilter);
  }, [activeFilter, notices]);

  const openNotice = (notice) => {
    setNotices((items) => items.map((item) => (item.id === notice.id ? { ...item, read: true } : item)));
    if (notice.target) {
      router.push(notice.target);
    }
  };

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="互动相关"
        title="互动通知"
        subtitle="喜欢、评论、纪念日和魔法完成提醒，都像纸页边缘的小便签。"
        right={<FairyTag tone={unreadCount ? 'gold' : undefined}>{unreadCount} 条未读</FairyTag>}
      />

      <FairyCard style={styles.summaryCard}>
        <View style={styles.summaryIcon}>
          <Ionicons name="mail-open-outline" size={28} color={colors.gold} />
        </View>
        <View style={styles.summaryText}>
          <Text style={styles.summaryTitle}>今天的故事有新回应</Text>
          <Text style={styles.summaryDesc}>点开任意便签会自动标记为已读，并跳转到对应章节页面。</Text>
        </View>
      </FairyCard>

      <View style={styles.filterRow}>
        {filters.map((filter) => (
          <Pressable
            key={filter}
            onPress={() => setActiveFilter(filter)}
            style={[styles.filterChip, activeFilter === filter && styles.filterChipActive]}
          >
            <Text style={[styles.filterText, activeFilter === filter && styles.filterTextActive]}>{filter}</Text>
          </Pressable>
        ))}
      </View>

      {visibleNotices.length ? (
        <View style={styles.list}>
          {visibleNotices.map((item) => (
            <Pressable key={item.id} onPress={() => openNotice(item)}>
              <FairyCard style={[styles.noticeCard, item.read && styles.noticeCardRead]}>
                <View style={[styles.noticeIcon, item.tone === 'gold' && styles.goldIcon]}>
                  <Ionicons name={item.icon} size={22} color={item.tone === 'gold' ? colors.gold : colors.accent} />
                </View>
                <View style={styles.noticeBody}>
                  <View style={styles.noticeTop}>
                    <Text style={styles.noticeTitle}>{item.title}</Text>
                    {!item.read ? <View style={styles.unreadDot} /> : null}
                  </View>
                  <Text style={styles.noticeText}>{item.text}</Text>
                  <View style={styles.noticeMeta}>
                    <FairyTag tone={item.tone}>{item.type}</FairyTag>
                    <Text style={styles.noticeTime}>{item.time}</Text>
                  </View>
                </View>
              </FairyCard>
            </Pressable>
          ))}
        </View>
      ) : (
        <FairyEmptyState
          compact
          icon="notifications-off-outline"
          title="这格小信箱暂时安静"
          description="换一个筛选看看，新的互动和提醒会很快落在这里。"
          actionTitle="回到全部"
          onAction={() => setActiveFilter('全部')}
        />
      )}
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  summaryCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.lg,
    backgroundColor: colors.cardPink,
    marginBottom: spacing.lg,
  },
  summaryIcon: {
    width: 58,
    height: 58,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFF5DF',
    borderWidth: 1,
    borderColor: colors.border,
  },
  summaryText: {
    flex: 1,
  },
  summaryTitle: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '900',
  },
  summaryDesc: {
    color: colors.textSoft,
    lineHeight: 21,
    marginTop: spacing.xs,
  },
  filterRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  filterChip: {
    borderRadius: 18,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
  },
  filterChipActive: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
  filterText: {
    color: colors.textSoft,
    fontWeight: '800',
  },
  filterTextActive: {
    color: colors.white,
  },
  list: {
    gap: spacing.md,
  },
  noticeCard: {
    flexDirection: 'row',
    gap: spacing.md,
    padding: spacing.lg,
  },
  noticeCardRead: {
    opacity: 0.72,
  },
  noticeIcon: {
    width: 46,
    height: 46,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.cardPink,
  },
  goldIcon: {
    backgroundColor: '#FFF5DF',
  },
  noticeBody: {
    flex: 1,
  },
  noticeTop: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  noticeTitle: {
    flex: 1,
    color: colors.text,
    fontSize: 16,
    fontWeight: '900',
  },
  unreadDot: {
    width: 9,
    height: 9,
    borderRadius: 9,
    backgroundColor: colors.primaryDeep,
  },
  noticeText: {
    color: colors.textSoft,
    lineHeight: 21,
    marginTop: spacing.xs,
  },
  noticeMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginTop: spacing.md,
  },
  noticeTime: {
    color: colors.textSoft,
    fontSize: 12,
  },
});
