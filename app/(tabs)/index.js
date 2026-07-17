import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyImage from '@/components/FairyImage';
import FairyPage from '@/components/FairyPage';
import FairyRequestState from '@/components/FairyRequestState';
import FairySticker from '@/components/FairySticker';
import FairyTag from '@/components/FairyTag';
import MemoryWall from '@/components/MemoryWall';
import { getApiMode } from '@/api/client';
import useFairyStore from '@/store/useFairyStore';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import { deriveHomeRelationshipView } from '@/utils/homeRelationshipView';
import { richTextToPlainText } from '@/utils/richText';

const actions = [
  { icon: 'create-outline', label: '写日记', hint: '把今天写下来', href: '/diary/editor' },
  { icon: 'camera-outline', label: '传照片', hint: '收进相册', href: '/photo/upload' },
  { icon: 'sparkles-outline', label: '做漫画', hint: '交给童话工坊', href: '/ai/comic-config' },
  { icon: 'calendar-outline', label: '纪念日', hint: '记住重要日子', href: '/anniversary' },
];

export default function IndexPage() {
  const { width } = useWindowDimensions();
  const compact = width < 680;
  const isReal = getApiMode() === 'real';
  const coupleState = useFairyStore((state) => state.couple);
  const records = useFairyStore((state) => state.records) || [];
  const creations = useFairyStore((state) => state.creations) || [];
  const anniversaries = useFairyStore((state) => state.anniversaries) || [];
  const loading = useFairyStore((state) => Boolean(state.loading?.bootstrap));
  const loadError = useFairyStore((state) => state.errors?.bootstrap || null);
  const refreshCoreData = useFairyStore((state) => state.refreshCoreData);
  const relationship = deriveHomeRelationshipView(coupleState, { isReal });
  const canShowHome = !isReal || relationship.bound;

  const recentRecords = records.slice(0, 3);
  const diaryCount = records.filter((item) => item.type === '日记').length;
  const photoCount = records
    .filter((item) => item.type === '照片')
    .reduce((sum, item) => sum + (Number(item.photoCount) || (isReal ? 0 : 3)), 0);
  const today = new Intl.DateTimeFormat('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date()).replaceAll('/', '.');

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

  const realHeroTitle = relationship.loveDays == null
    ? '恋爱起始日未提供'
    : `已经一起走过 ${relationship.loveDays} 天`;
  const realHeroText = relationship.userName || relationship.partnerName
    ? `${relationship.userName || '我的昵称未提供'} 和 ${relationship.partnerName || '伴侣昵称未提供'}`
    : '双方昵称尚未提供';

  return (
    <FairyPage backgroundName="creamPaper" tabSafe topSpace={28} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <View style={styles.header}>
          <View>
            <Text style={styles.date}>{today}</Text>
            <Text style={styles.title}>独家童话</Text>
          </View>
          <Pressable accessibilityRole="button" accessibilityLabel="打开回忆相册" style={({ pressed }) => [styles.iconBtn, pressed && styles.pressed]} onPress={() => router.push('/photo/album')}>
            <Ionicons name="images-outline" size={22} color={colors.text} />
            <Text style={styles.iconBtnText}>相册</Text>
          </Pressable>
        </View>

        {isReal ? <FairyRequestState loading={loading} error={loadError} onRetry={refreshCoreData} /> : null}

        {!loading && !loadError && isReal && !relationship.bound ? (
          <FairyEmptyState
            imageName="emptyDiary"
            title="尚未完成情侣绑定"
            description="绑定成功并由后端确认关系后，首页才会展示你们的共同记录。"
            actionTitle="邀请或绑定 TA"
            onAction={() => router.push('/account/invite')}
          />
        ) : null}

        {!loading && !loadError && canShowHome ? (
          <>
            <FairyCard style={[styles.hero, !compact && styles.heroWide]}>
              <FairySticker name="tapePink" size={70} rotate="-8deg" style={styles.tapeSticker} />
              <FairySticker name="heart" size={34} rotate="10deg" style={styles.heartSticker} />
              <FairySticker name="star" size={36} rotate="-8deg" style={styles.starSticker} />
              <View style={[styles.heroTextWrap, !compact && styles.heroTextWide]}>
                <Text style={styles.badge}>今天的恋爱绘本</Text>
                <Text style={styles.heroTitle}>{isReal ? realHeroTitle : `已经一起走过 ${relationship.loveDays} 天`}</Text>
                <Text style={styles.heroText}>{isReal ? realHeroText : relationship.statusText}</Text>
                <View style={styles.heroTags}>
                  <FairyTag tone="pink">{isReal ? relationship.spaceName : relationship.spaceName}</FairyTag>
                  {isReal && relationship.statusText ? <FairyTag tone="gold">{relationship.statusText}</FairyTag> : null}
                  <FairyTag tone="gold">记录 {records.length} 条</FairyTag>
                </View>
              </View>
              <View style={[styles.heroImage, compact && styles.heroImageCompact]}><FairyImage name="homeCover" height={compact ? 190 : 260} framed={false} radius={22} resizeMode="cover" /></View>
            </FairyCard>

            <View style={styles.statsGrid}>
              {stats.map((item) => (
                <FairyCard key={item.label} style={[styles.statCard, !compact && styles.statCardWide]}>
                  <View style={styles.statIcon}><Ionicons name={item.icon} size={18} color={colors.accent} /></View>
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
                <Pressable key={item.label} style={({ pressed }) => [styles.action, !compact && styles.actionWide, pressed && styles.pressed]} onPress={() => router.push(item.href)}>
                  <View style={styles.actionIcon}><Ionicons name={item.icon} size={23} color={colors.accent} /></View>
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
                    <View style={styles.recentIcon}><Ionicons name={record.icon || 'heart-outline'} size={18} color={colors.accent} /></View>
                    <View style={styles.recentText}>
                      <Text style={styles.recentTitle} numberOfLines={1}>{record.title}</Text>
                      <Text style={styles.recentContent} numberOfLines={2}>{richTextToPlainText(record.content)}</Text>
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
              <FairyEmptyState imageName="emptyDiary" title="还没有记录" description="写下第一篇日记，或上传一组照片，首页就会开始长出你们的故事。" actionTitle="写第一篇日记" onAction={() => router.push('/diary/editor')} />
            )}

            <View style={styles.sectionRow}>
              <View>
                <Text style={styles.section}>最近的故事</Text>
                <Text style={styles.sectionHint}>像贴在纸上的回忆碎片</Text>
              </View>
              <View style={styles.stickerMark}>
                <FairySticker name="star" size={30} rotate="8deg" style={styles.inlineSticker} />
              </View>
            </View>
            {records.length ? <MemoryWall records={records} onPress={openRecord} /> : <FairyEmptyState imageName="emptyDiary" title="回忆墙还在等第一张贴纸" description="日记、照片和 AI 作品都会在这里变成可收藏的碎片。" />}
          </>
        ) : null}
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 980 },
  pressed: { opacity: 0.68 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 },
  date: { color: colors.textSoft, fontSize: 12, marginBottom: 4 },
  title: { color: colors.text, fontSize: 31, fontWeight: '900' },
  iconBtn: { minWidth: 64, minHeight: 58, borderRadius: 20, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  iconBtnText: { color: colors.textSoft, fontSize: 10, fontWeight: '800', marginTop: 2 },
  hero: { marginBottom: 24, backgroundColor: colors.cardPink, paddingBottom: 18, overflow: 'visible' },
  heroWide: { flexDirection: 'row', alignItems: 'center', gap: spacing.xxl, padding: spacing.xxl },
  heroTextWrap: { marginBottom: 6 },
  heroTextWide: { flex: 1, paddingLeft: spacing.lg },
  heroImage: { flex: 1, minWidth: 280 },
  heroImageCompact: { width: '100%', minWidth: 0 },
  tapeSticker: { top: -20, left: 26 },
  heartSticker: { top: 18, right: 22 },
  starSticker: { top: 198, right: 34 },
  badge: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 10 },
  heroTitle: { color: colors.text, fontSize: 25, fontWeight: '900', lineHeight: 32 },
  heroText: { color: colors.textSoft, marginTop: 8, fontSize: 14 },
  heroTags: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 14 },
  statsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 24 },
  statCard: { width: '47.8%', padding: 14, minHeight: 116 },
  statCardWide: { width: '23.5%', flexGrow: 1 },
  statIcon: { width: 34, height: 34, borderRadius: 14, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.border, marginBottom: 10 },
  statValue: { color: colors.text, fontSize: 24, fontWeight: '900' },
  statLabel: { color: colors.textSoft, fontSize: 12, marginTop: 3, fontWeight: '700' },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 4 },
  sectionHint: { color: colors.textSoft, fontSize: 12 },
  sectionHeader: { marginBottom: 14 },
  sectionRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18 },
  stickerMark: { width: 38, height: 38, borderRadius: 16, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, transform: [{ rotate: '8deg' }] },
  inlineSticker: { position: 'relative' },
  actions: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 16 },
  action: { width: '47.8%', minHeight: 112, borderRadius: 24, backgroundColor: colors.card, justifyContent: 'center', borderWidth: 1, borderColor: colors.border, padding: 14 },
  actionWide: { width: '23.5%', flexGrow: 1 },
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
