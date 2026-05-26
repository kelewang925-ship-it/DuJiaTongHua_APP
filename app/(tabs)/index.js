import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyImage from '../../src/components/FairyImage';
import FairyTag from '../../src/components/FairyTag';
import MemoryWall from '../../src/components/MemoryWall';
import useFairyStore from '../../src/store/useFairyStore';

const actions = [
  {
    icon: 'create-outline',
    label: '写日记',
    hint: '把今天写下来',
    href: '/diary/editor',
  },
  {
    icon: 'camera-outline',
    label: '传照片',
    hint: '收进相册',
    href: '/photo/upload',
  },
  {
    icon: 'sparkles-outline',
    label: '做漫画',
    hint: '交给童话工坊',
    href: '/ai/comic-config',
  },
  {
    icon: 'calendar-outline',
    label: '纪念日',
    hint: '记住重要日子',
    href: '/anniversary',
  },
];

export default function IndexPage() {
  const couple = useFairyStore((state) => state.couple);
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const anniversaries = useFairyStore((state) => state.anniversaries);

  const recentRecords = records.slice(0, 3);
  const diaryCount = records.filter((item) => item.type === '日记').length;
  const photoCount = records
    .filter((item) => item.type === '照片')
    .reduce((sum, item) => sum + (item.photoCount || 3), 0);

  const stats = [
    { label: '日记', value: diaryCount, icon: 'book-outline' },
    { label: '照片', value: photoCount, icon: 'images-outline' },
    { label: '作品', value: creations.length, icon: 'color-wand-outline' },
    { label: '纪念日', value: anniversaries.length, icon: 'heart-outline' },
  ];

  const openRecord = (record) => {
    if (record.type === '日记') {
      router.push('/diary/detail');
      return;
    }
    if (record.type === '照片') {
      router.push('/photo/album');
      return;
    }
    router.push('/(tabs)/workshop');
  };

  const openAction = (href) => {
    router.push(href);
  };

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <View>
          <Text style={styles.date}>2026年5月26日</Text>
          <Text style={styles.title}>独家童话</Text>
        </View>
        <Pressable style={styles.iconBtn} onPress={() => router.push('/photo/album')}>
          <Ionicons name="images-outline" size={22} color={colors.text} />
        </Pressable>
      </View>

      <FairyCard style={styles.hero}>
        <View style={styles.heroTextWrap}>
          <Text style={styles.badge}>今天的恋爱绘本</Text>
          <Text style={styles.heroTitle}>已经一起走过 {couple.loveDays} 天</Text>
          <Text style={styles.heroText}>{couple.statusText}</Text>
          <View style={styles.heroTags}>
            <FairyTag tone="pink">{couple.spaceName}</FairyTag>
            <FairyTag tone="gold">记录 {records.length} 条</FairyTag>
          </View>
        </View>
        <FairyImage name="homeCover" height={168} />
      </FairyCard>

      <View style={styles.statsGrid}>
        {stats.map((item) => (
          <FairyCard key={item.label} style={styles.statCard}>
            <View style={styles.statIcon}>
              <Ionicons name={item.icon} size={18} color={colors.accent} />
            </View>
            <Text style={styles.statValue}>{item.value}</Text>
            <Text style={styles.statLabel}>{item.label}</Text>
          </FairyCard>
        ))}
      </View>

      <View style={styles.sectionHeader}>
        <View>
          <Text style={styles.section}>今天想记录什么？</Text>
          <Text style={styles.sectionHint}>一键把日常放进你们的绘本里</Text>
        </View>
      </View>
      <View style={styles.actions}>
        {actions.map((item) => (
          <Pressable key={item.label} style={styles.action} onPress={() => openAction(item.href)}>
            <View style={styles.actionIcon}>
              <Ionicons name={item.icon} size={23} color={colors.accent} />
            </View>
            <Text style={styles.actionText}>{item.label}</Text>
            <Text style={styles.actionHint}>{item.hint}</Text>
          </Pressable>
        ))}
      </View>

      <FairyButton title="把今天写进童话" style={styles.cta} onPress={() => router.push('/diary/editor')} />

      <View style={styles.sectionRow}>
        <View>
          <Text style={styles.section}>最近记录</Text>
          <Text style={styles.sectionHint}>刚刚发生的温柔小事</Text>
        </View>
        <Pressable style={styles.textLink} onPress={() => router.push('/photo/album')}>
          <Text style={styles.textLinkLabel}>看相册</Text>
          <Ionicons name="chevron-forward" size={15} color={colors.accent} />
        </Pressable>
      </View>

      {recentRecords.length ? (
        <View style={styles.recentList}>
          {recentRecords.map((record) => (
            <Pressable key={record.id} style={styles.recentItem} onPress={() => openRecord(record)}>
              <View style={styles.recentIcon}>
                <Ionicons name={record.icon || 'heart-outline'} size={18} color={colors.accent} />
              </View>
              <View style={styles.recentText}>
                <Text style={styles.recentTitle} numberOfLines={1}>{record.title}</Text>
                <Text style={styles.recentContent} numberOfLines={2}>{record.content}</Text>
                <View style={styles.recentMeta}>
                  <FairyTag>{record.type}</FairyTag>
                  <Text style={styles.recentDate}>{record.date}</Text>
                </View>
              </View>
              <Ionicons name="chevron-forward" size={17} color={colors.textSoft} />
            </Pressable>
          ))}
        </View>
      ) : (
        <FairyEmptyState
          title="还没有记录"
          description="写下第一篇日记，或上传一组照片，首页就会开始长出你们的故事。"
          actionTitle="写第一篇日记"
          onAction={() => router.push('/diary/editor')}
          compact
        />
      )}

      <View style={styles.sectionRow}>
        <View>
          <Text style={styles.section}>最近的故事</Text>
          <Text style={styles.sectionHint}>像贴在纸上的回忆碎片</Text>
        </View>
        <View style={styles.stickerMark}>
          <Ionicons name="sparkles-outline" size={18} color={colors.gold} />
        </View>
      </View>
      {records.length ? (
        <MemoryWall records={records} onPress={openRecord} />
      ) : (
        <FairyEmptyState
          title="回忆墙还在等第一张贴纸"
          description="日记、照片和 AI 作品都会在这里变成可收藏的碎片。"
          compact
        />
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 62, paddingBottom: 124 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 },
  date: { color: colors.textSoft, fontSize: 12, marginBottom: 4 },
  title: { color: colors.text, fontSize: 31, fontWeight: '900' },
  iconBtn: { width: 44, height: 44, borderRadius: 18, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center' },
  hero: { marginBottom: 24, backgroundColor: colors.cardPink, paddingBottom: 18 },
  heroTextWrap: { marginBottom: 6 },
  badge: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 10 },
  heroTitle: { color: colors.text, fontSize: 25, fontWeight: '900', lineHeight: 32 },
  heroText: { color: colors.textSoft, marginTop: 8, fontSize: 14 },
  heroTags: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 14 },
  statsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 24 },
  statCard: { width: '47.8%', padding: 14, minHeight: 116 },
  statIcon: { width: 34, height: 34, borderRadius: 14, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.border, marginBottom: 10 },
  statValue: { color: colors.text, fontSize: 24, fontWeight: '900' },
  statLabel: { color: colors.textSoft, fontSize: 12, marginTop: 3, fontWeight: '700' },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 4 },
  sectionHint: { color: colors.textSoft, fontSize: 12 },
  sectionHeader: { marginBottom: 14 },
  sectionRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18 },
  stickerMark: { width: 38, height: 38, borderRadius: 16, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, transform: [{ rotate: '8deg' }] },
  actions: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 16 },
  action: { width: '47.8%', minHeight: 112, borderRadius: 24, backgroundColor: colors.card, justifyContent: 'center', borderWidth: 1, borderColor: colors.border, padding: 14 },
  actionIcon: { width: 42, height: 42, borderRadius: 16, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink, marginBottom: 10 },
  actionText: { color: colors.text, fontWeight: '900', fontSize: 14 },
  actionHint: { color: colors.textSoft, fontSize: 11, marginTop: 4, lineHeight: 16 },
  cta: { marginBottom: 26 },
  textLink: { flexDirection: 'row', alignItems: 'center', gap: 2, paddingLeft: 10, paddingVertical: 6 },
  textLinkLabel: { color: colors.accent, fontSize: 12, fontWeight: '800' },
  recentList: { gap: 12, marginBottom: 28 },
  recentItem: { flexDirection: 'row', alignItems: 'center', backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, borderRadius: 24, padding: 14 },
  recentIcon: { width: 42, height: 42, borderRadius: 16, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink, marginRight: 12 },
  recentText: { flex: 1 },
  recentTitle: { color: colors.text, fontSize: 15, fontWeight: '900' },
  recentContent: { color: colors.textSoft, fontSize: 12, lineHeight: 18, marginTop: 4 },
  recentMeta: { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 8 },
  recentDate: { color: colors.textSoft, fontSize: 11 },
});
