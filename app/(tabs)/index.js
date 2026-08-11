import { Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyPage from '@/components/FairyPage';
import FairySection from '@/components/FairySection';
import FairyTag from '@/components/FairyTag';
import MemoryWall from '@/components/MemoryWall';
import useFairyStore from '@/store/useFairyStore';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import { richTextToPlainText } from '@/utils/richText';

const actions = [
  { icon: 'create-outline', label: '写日记', hint: '把今天写下来', href: '/diary/editor' },
  { icon: 'camera-outline', label: '传照片', hint: '收进相册', href: '/photo/upload' },
  { icon: 'sparkles-outline', label: '做漫画', hint: '交给童话工坊', href: '/ai/comic-config' },
  { icon: 'calendar-outline', label: '纪念日', hint: '记住重要日子', href: '/anniversary' },
];

export default function IndexPage() {
  const couple = useFairyStore((state) => state.couple);
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const recentRecords = records.slice(0, 3);
  const diaryCount = records.filter((item) => item.type === '日记').length;
  const photoCount = records.filter((item) => item.type === '照片').reduce((sum, item) => sum + (item.photoCount || 3), 0);
  const today = new Intl.DateTimeFormat('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
    .format(new Date())
    .replaceAll('/', '.');

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

  return (
    <FairyPage tabSafe topSpace={28} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <View style={styles.header}>
          <View>
            <Text style={styles.date}>{today}</Text>
            <Text style={styles.title}>独家童话</Text>
          </View>
          <Pressable
            accessibilityRole="button"
            accessibilityLabel="打开回忆相册"
            style={({ pressed }) => [styles.iconButton, pressed && styles.pressed]}
            onPress={() => router.push('/photo/album')}
          >
            <Ionicons name="images-outline" size={22} color={colors.text} />
            <Text style={styles.iconButtonText}>相册</Text>
          </Pressable>
        </View>

        <FairyCard style={styles.hero} contentStyle={styles.heroContent}>
          <View style={styles.heroOrb} />
          <View style={styles.heroCopy}>
            <Text style={styles.eyebrow}>今天的恋爱绘本</Text>
            <Text style={styles.heroTitle}>已经一起走过 {couple.loveDays} 天</Text>
            <Text style={styles.heroText}>{couple.statusText}</Text>
            <View style={styles.tagRow}>
              <FairyTag tone="pink">{couple.spaceName}</FairyTag>
              <FairyTag tone="gold">记录 {records.length} 条</FairyTag>
            </View>
          </View>
          <View style={styles.heroMark}>
            <Ionicons name="heart" size={30} color={colors.primaryDeep} />
            <Text style={styles.heroMarkText}>只属于你们</Text>
          </View>
        </FairyCard>

        <View style={styles.statsGrid}>
          {stats.map((item) => (
            <FairyCard key={item.label} style={styles.statCard} padding={spacing.md}>
              <View style={styles.statIcon}><Ionicons name={item.icon} size={18} color={colors.accent} /></View>
              <Text style={styles.statValue}>{item.value}</Text>
              <Text style={styles.statLabel}>{item.label}</Text>
            </FairyCard>
          ))}
        </View>

        <FairySection title="今天想记录什么？" description="一键把日常放进你们的绘本">
          <View style={styles.actions}>
            {actions.map((item) => (
              <Pressable
                key={item.label}
                style={({ pressed }) => [styles.action, pressed && styles.pressed]}
                onPress={() => router.push(item.href)}
              >
                <View style={styles.actionIcon}><Ionicons name={item.icon} size={22} color={colors.accent} /></View>
                <Text style={styles.actionText}>{item.label}</Text>
                <Text style={styles.actionHint}>{item.hint}</Text>
              </Pressable>
            ))}
          </View>
        </FairySection>

        <FairyButton title="把今天写进童话" style={styles.cta} onPress={() => router.push('/diary/editor')} />

        <FairySection title="最近记录" description="刚刚发生的温柔小事" actionLabel="看相册" onAction={() => router.push('/photo/album')}>
          {recentRecords.length ? (
            <View style={styles.recentList}>
              {recentRecords.map((record) => (
                <Pressable key={record.id} style={styles.recentItem} onPress={() => openRecord(record)}>
                  <View style={styles.recentIcon}><Ionicons name={record.icon || 'heart-outline'} size={18} color={colors.accent} /></View>
                  <View style={styles.recentText}>
                    <Text style={styles.recentTitle} numberOfLines={1}>{record.title}</Text>
                    <Text style={styles.recentContent} numberOfLines={2}>{richTextToPlainText(record.content)}</Text>
                    <View style={styles.recentMeta}><FairyTag>{record.type}</FairyTag><Text style={styles.recentDate}>{record.date}</Text></View>
                  </View>
                  <Ionicons name="chevron-forward" size={17} color={colors.textSoft} />
                </Pressable>
              ))}
            </View>
          ) : (
            <FairyEmptyState imageName="emptyDiary" title="还没有记录" description="写下第一篇日记，首页就会开始长出你们的故事。" actionTitle="写第一篇日记" onAction={() => router.push('/diary/editor')} />
          )}
        </FairySection>

        <FairySection title="最近的故事" description="日记、照片和 AI 作品都会在这里留下痕迹">
          {records.length ? <MemoryWall records={records} onPress={openRecord} /> : <FairyEmptyState imageName="emptyDiary" title="回忆墙还在等第一张贴纸" description="从今天开始，收藏你们的故事碎片。" />}
        </FairySection>
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 960 },
  pressed: { opacity: 0.68 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 },
  date: { color: colors.textSoft, fontSize: 12, marginBottom: 4 },
  title: { color: colors.text, fontSize: 31, fontWeight: '900' },
  iconButton: { minWidth: 64, minHeight: 58, borderRadius: 20, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  iconButtonText: { color: colors.textSoft, fontSize: 10, fontWeight: '800', marginTop: 2 },
  hero: { marginBottom: 24, backgroundColor: colors.cardPink, overflow: 'hidden' },
  heroContent: { minHeight: 208, flexDirection: 'row', alignItems: 'center', gap: spacing.lg, position: 'relative' },
  heroCopy: { flex: 1, zIndex: 1 },
  heroOrb: { position: 'absolute', width: 190, height: 190, right: -52, top: -38, borderRadius: 95, backgroundColor: '#FAD0D8', opacity: 0.72 },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 10 },
  heroTitle: { color: colors.text, fontSize: 25, lineHeight: 32, fontWeight: '900' },
  heroText: { color: colors.textSoft, marginTop: 8, fontSize: 14, lineHeight: 21 },
  tagRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 14 },
  heroMark: { width: 112, height: 112, borderRadius: 56, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.paper, borderWidth: 1, borderColor: colors.border, transform: [{ rotate: '4deg' }] },
  heroMarkText: { marginTop: 5, color: colors.accent, fontSize: 10, fontWeight: '800' },
  statsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 24 },
  statCard: { width: '23.5%', minWidth: 132, flexGrow: 1, minHeight: 116 },
  statIcon: { width: 34, height: 34, borderRadius: 14, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.border, marginBottom: 10 },
  statValue: { color: colors.text, fontSize: 24, fontWeight: '900' },
  statLabel: { color: colors.textSoft, fontSize: 12, marginTop: 3, fontWeight: '700' },
  actions: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  action: { width: '47.8%', minHeight: 112, borderRadius: 24, backgroundColor: colors.card, justifyContent: 'center', borderWidth: 1, borderColor: colors.border, padding: 14 },
  actionIcon: { width: 42, height: 42, borderRadius: 16, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink, marginBottom: 10 },
  actionText: { color: colors.text, fontWeight: '900', fontSize: 14 },
  actionHint: { color: colors.textSoft, fontSize: 11, marginTop: 4, lineHeight: 16 },
  cta: { marginBottom: 26 },
  recentList: { gap: 12 },
  recentItem: { flexDirection: 'row', alignItems: 'center', backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, borderRadius: 24, padding: 14 },
  recentIcon: { width: 42, height: 42, borderRadius: 16, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink, marginRight: 12 },
  recentText: { flex: 1, minWidth: 0 },
  recentTitle: { color: colors.text, fontSize: 15, fontWeight: '900' },
  recentContent: { color: colors.textSoft, fontSize: 12, lineHeight: 18, marginTop: 4 },
  recentMeta: { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 8 },
  recentDate: { color: colors.textSoft, fontSize: 11 },
});
