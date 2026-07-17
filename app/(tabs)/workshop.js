import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

import FairyCard from '@/components/FairyCard';
import FairyImage from '@/components/FairyImage';
import FairyIllustration from '@/components/FairyIllustration';
import FairyPage from '@/components/FairyPage';
import FairySticker from '@/components/FairySticker';
import FairyTag from '@/components/FairyTag';
import WorkshopCard from '@/components/WorkshopCard';
import useFairyStore from '@/store/useFairyStore';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';

const entrances = [
  ['color-palette-outline', '恋爱漫画', '把日记或照片画成童话漫画', '/ai/comic-config'],
  ['videocam-outline', '回忆放映机', '生成带字幕和音乐的纪念视频', '/ai/video-config'],
  ['document-text-outline', '文字转漫画', '直接把一段故事变成绘本分镜', '/ai/text-to-comic'],
  ['camera-outline', '照片转漫画', '把一张回忆照片变成漫画场景', '/ai/photo-to-comic'],
];

export default function WorkshopPage() {
  const { width } = useWindowDimensions();
  const compact = width < 700;
  const creations = useFairyStore((state) => state.creations);
  const selectAiJob = useFairyStore((state) => state.selectAiJob);
  const latestJob = creations[0];

  const openCreation = (id) => {
    const current = creations.find((item) => item.id === id);
    selectAiJob(id);
    if (current?.type === '漫画') {
      router.push(`/ai/comic-result?id=${id}`);
      return;
    }
    router.push('/ai/progress');
  };

  return (
    <FairyPage backgroundName="creamPaper" tabSafe topSpace={28} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
      <View style={styles.titleRow}><View><Text style={styles.eyebrow}>把回忆变成温柔的绘本魔法</Text><Text style={styles.title}>AI 童话工坊</Text></View><Pressable accessibilityRole="button" onPress={() => router.push('/drafts')} style={({ pressed }) => [styles.draftButton, pressed && styles.pressed]}><Ionicons name="save-outline" size={20} color={colors.text} /><Text style={styles.draftText}>草稿箱</Text></Pressable></View>
      <LinearGradient colors={['#FFF9F4', '#FFF0F2']} style={[styles.hero, !compact && styles.heroWide]}>
        <FairySticker name="tapePink" size={72} rotate="-8deg" style={styles.tapeSticker} />
        <FairySticker name="magicWand" size={52} rotate="12deg" style={styles.magicSticker} />
        <FairySticker name="star" size={38} rotate="-10deg" style={styles.starSticker} />
        <FairySticker name="heart" size={34} rotate="8deg" style={styles.heartSticker} />
        <FairySticker name="flower" size={36} rotate="-6deg" style={styles.flowerSticker} />
        <View style={[styles.heroCopy, !compact && styles.heroCopyWide]}>
          <View style={styles.magicIcon}>
            <Ionicons name="sparkles" size={28} color={colors.gold} />
          </View>
          <Text style={styles.heroTitle}>把回忆变成童话</Text>
          <Text style={styles.heroText}>从日记、照片或一段文字开始，创建漫画和回忆短片。</Text>
          {latestJob ? (
            <Pressable style={styles.latestPill} onPress={() => openCreation(latestJob.id)}>
              <Ionicons name={latestJob.icon} size={16} color={colors.primaryDeep} />
              <Text style={styles.latestText}>最近作品：{latestJob.title}</Text>
            </Pressable>
          ) : null}
        </View>
        <View style={[styles.heroImage, compact && styles.heroImageCompact]}><FairyImage name="workshopCover" height={compact ? 190 : 270} framed={false} radius={22} resizeMode="cover" /></View>
      </LinearGradient>

      <Text style={styles.section}>创作入口</Text>
      <View style={styles.grid}>
        {entrances.map(([icon, title, description, href]) => (
          <Pressable key={title} style={({ pressed }) => [styles.entry, !compact && styles.entryWide, pressed && styles.pressed]} onPress={() => router.push(href)}>
            <WorkshopCard icon={icon} title={title} description={description} />
          </Pressable>
        ))}
      </View>

      <Text style={styles.section}>创作历史</Text>
      {creations.map((item) => (
        <Pressable key={item.id} onPress={() => openCreation(item.id)} style={({ pressed }) => pressed && styles.pressed}>
          <FairyCard style={styles.history}>
            <FairyIllustration scene={item.artwork} width={92} height={82} />
            <View style={styles.historyBody}>
              <View style={styles.historyMeta}>
                <FairyTag tone={item.progress === 100 ? 'gold' : 'default'}>{item.type}</FairyTag>
                <Text style={styles.historyStatus}>{item.status}</Text>
              </View>
              <Text style={styles.historyTitle}>{item.title}</Text>
              <Text style={styles.historyText}>{item.source || '童话工坊'} · {item.styleName || '默认风格'}</Text>
            </View>
            <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
          </FairyCard>
        </Pressable>
      ))}
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 980 },
  pressed: { opacity: 0.68 },
  titleRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.lg, marginBottom: spacing.xl },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900' },
  draftButton: { minWidth: 72, minHeight: 58, alignItems: 'center', justifyContent: 'center', borderRadius: 20, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border },
  draftText: { color: colors.textSoft, fontSize: 10, fontWeight: '900', marginTop: 3 },
  hero: { borderRadius: 30, padding: 18, borderWidth: 1, borderColor: colors.border, marginBottom: 28, overflow: 'visible' },
  heroWide: { flexDirection: 'row', alignItems: 'center', gap: spacing.xxl, padding: spacing.xxl },
  heroCopy: { marginBottom: 8 },
  heroCopyWide: { flex: 1, paddingLeft: spacing.lg },
  heroImage: { width: '50%', minWidth: 320 },
  heroImageCompact: { width: '100%', minWidth: 0 },
  magicIcon: { width: 54, height: 54, borderRadius: 22, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 14 },
  heroTitle: { color: colors.text, fontSize: 24, fontWeight: '900' },
  heroText: { color: colors.textSoft, marginTop: 10, lineHeight: 22 },
  latestPill: { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 14, paddingVertical: 9, paddingHorizontal: 12, borderRadius: 16, backgroundColor: colors.white, borderWidth: 1, borderColor: colors.border },
  latestText: { color: colors.text, fontSize: 12, fontWeight: '800', flex: 1 },
  tapeSticker: { top: -22, left: 24 },
  magicSticker: { top: 10, right: 16 },
  starSticker: { top: 118, right: 26 },
  heartSticker: { top: 182, left: 18 },
  flowerSticker: { top: 230, right: 68 },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 16 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 14, marginBottom: 28 },
  entry: { width: '47.8%' },
  entryWide: { width: '23.5%', flexGrow: 1 },
  history: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14, padding: 14 },
  historyBody: { flex: 1 },
  historyMeta: { flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: 8, marginBottom: 7 },
  historyStatus: { color: colors.textSoft, fontSize: 12, fontWeight: '700' },
  historyTitle: { color: colors.text, fontWeight: '900', fontSize: 15 },
  historyText: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
