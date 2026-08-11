import { Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyCard from '@/components/FairyCard';
import FairyIllustration from '@/components/FairyIllustration';
import FairyPage from '@/components/FairyPage';
import FairySection from '@/components/FairySection';
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
    <FairyPage tabSafe topSpace={28} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <View style={styles.titleRow}>
          <View style={styles.titleCopy}>
            <Text style={styles.eyebrow}>把回忆变成温柔的绘本魔法</Text>
            <Text style={styles.title}>童话工坊</Text>
          </View>
          <Pressable accessibilityRole="button" onPress={() => router.push('/drafts')} style={({ pressed }) => [styles.draftButton, pressed && styles.pressed]}>
            <Ionicons name="save-outline" size={20} color={colors.text} />
            <Text style={styles.draftText}>草稿箱</Text>
          </Pressable>
        </View>

        <FairyCard style={styles.hero} contentStyle={styles.heroContent}>
          <View style={styles.heroOrb} />
          <View style={styles.heroCopy}>
            <View style={styles.magicIcon}><Ionicons name="sparkles" size={28} color={colors.gold} /></View>
            <Text style={styles.heroTitle}>把回忆变成童话</Text>
            <Text style={styles.heroText}>从日记、照片或一段文字开始，创建漫画和回忆短片。</Text>
            {latestJob ? (
              <Pressable style={styles.latestPill} onPress={() => openCreation(latestJob.id)}>
                <Ionicons name={latestJob.icon || 'sparkles-outline'} size={16} color={colors.primaryDeep} />
                <Text style={styles.latestText} numberOfLines={1}>最近作品：{latestJob.title}</Text>
              </Pressable>
            ) : null}
          </View>
          <View style={styles.heroMark}><Ionicons name="color-wand-outline" size={34} color={colors.gold} /><Text style={styles.heroMarkText}>魔法正在发生</Text></View>
        </FairyCard>

        <FairySection title="创作入口" description="选择一种方式，让故事开始生长">
          <View style={styles.grid}>
            {entrances.map(([icon, title, description, href]) => (
              <Pressable key={title} style={({ pressed }) => [styles.entry, pressed && styles.pressed]} onPress={() => router.push(href)}>
                <WorkshopCard icon={icon} title={title} description={description} />
              </Pressable>
            ))}
          </View>
        </FairySection>

        <FairySection title="创作历史" description="每一次生成，都是故事的一页">
          {creations.length ? creations.map((item) => (
            <Pressable key={item.id} onPress={() => openCreation(item.id)} style={({ pressed }) => pressed && styles.pressed}>
              <FairyCard style={styles.history} padding={spacing.md}>
                <FairyIllustration scene={item.artwork} width={72} height={64} />
                <View style={styles.historyBody}>
                  <View style={styles.historyMeta}><FairyTag tone={item.progress === 100 ? 'gold' : 'default'}>{item.type}</FairyTag><Text style={styles.historyStatus}>{item.status}</Text></View>
                  <Text style={styles.historyTitle} numberOfLines={1}>{item.title}</Text>
                  <Text style={styles.historyText} numberOfLines={1}>{item.source || '童话工坊'} · {item.styleName || '默认风格'}</Text>
                </View>
                <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
              </FairyCard>
            </Pressable>
          )) : (
            <FairyCard style={styles.emptyHistory}>
              <Ionicons name="sparkles-outline" size={28} color={colors.gold} />
              <Text style={styles.emptyTitle}>还没有作品</Text>
              <Text style={styles.emptyText}>选择一个创作入口，把回忆交给魔法画笔。</Text>
            </FairyCard>
          )}
        </FairySection>
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 960 },
  pressed: { opacity: 0.68 },
  titleRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.lg, marginBottom: spacing.xl },
  titleCopy: { flex: 1 },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900' },
  draftButton: { minWidth: 72, minHeight: 58, alignItems: 'center', justifyContent: 'center', borderRadius: 20, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border },
  draftText: { color: colors.textSoft, fontSize: 10, fontWeight: '900', marginTop: 3 },
  hero: { marginBottom: 28, backgroundColor: colors.goldSurface || colors.bg.gold, overflow: 'hidden' },
  heroContent: { minHeight: 220, flexDirection: 'row', alignItems: 'center', gap: spacing.lg, position: 'relative' },
  heroOrb: { position: 'absolute', width: 220, height: 220, right: -72, top: -44, borderRadius: 110, backgroundColor: '#F7E8D5', opacity: 0.9 },
  heroCopy: { flex: 1, zIndex: 1 },
  magicIcon: { width: 54, height: 54, borderRadius: 22, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 14 },
  heroTitle: { color: colors.text, fontSize: 24, fontWeight: '900' },
  heroText: { color: colors.textSoft, marginTop: 10, lineHeight: 22 },
  latestPill: { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 14, paddingVertical: 9, paddingHorizontal: 12, borderRadius: 16, backgroundColor: colors.white, borderWidth: 1, borderColor: colors.border },
  latestText: { color: colors.text, fontSize: 12, fontWeight: '800', flex: 1 },
  heroMark: { width: 118, height: 118, borderRadius: 59, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.white, borderWidth: 1, borderColor: colors.border, transform: [{ rotate: '-4deg' }] },
  heroMarkText: { marginTop: 6, color: colors.accent, fontSize: 10, fontWeight: '800' },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 14 },
  entry: { width: '47.8%', flexGrow: 1, minWidth: 150 },
  history: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14 },
  historyBody: { flex: 1, minWidth: 0 },
  historyMeta: { flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: 8, marginBottom: 7 },
  historyStatus: { color: colors.textSoft, fontSize: 12, fontWeight: '700' },
  historyTitle: { color: colors.text, fontWeight: '900', fontSize: 15 },
  historyText: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  emptyHistory: { alignItems: 'center', backgroundColor: colors.cardPink },
  emptyTitle: { color: colors.text, marginTop: 10, fontSize: 16, fontWeight: '900' },
  emptyText: { color: colors.textSoft, marginTop: 5, fontSize: 12, textAlign: 'center' },
});
