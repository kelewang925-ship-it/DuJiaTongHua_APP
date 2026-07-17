import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View, useWindowDimensions } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';

const storyBeats = [
  { icon: 'flower-outline', title: '花树下', copy: '黄昏把第一次并肩散步，染成了温柔的桃粉色。' },
  { icon: 'umbrella-outline', title: '春雨里', copy: '一把小伞刚好装下两个人，也装下了那天的心动。' },
  { icon: 'moon-outline', title: '月光边', copy: '夜色安静下来，萤火替你们记住没有说出口的话。' },
];

export default function ComicResultPage() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const { id } = useLocalSearchParams();
  const creations = useFairyStore((state) => state.creations);
  const selectAiJob = useFairyStore((state) => state.selectAiJob);
  const [selectedBeat, setSelectedBeat] = useState(0);
  const [favorite, setFavorite] = useState(false);
  const [toast, setToast] = useState(null);

  const comic = useMemo(() => {
    const comicId = Array.isArray(id) ? id[0] : id;
    if (comicId) return creations.find((item) => item.id === comicId && item.type === '漫画');
    return creations.find((item) => item.type === '漫画');
  }, [creations, id]);

  const title = comic?.title || '我们的春日小夜曲';
  const status = comic?.status || '已生成 · 可以收藏';
  const styleName = comic?.styleName || '温柔童话绘本';
  const previewHeight = Math.min(240, Math.max(116, (Math.min(width, 760) - spacing.lg * 2) / 3));

  return (
    <FairyPage backgroundName="creamPaper" topSpace={28} bottomSpace={64}>
      <View style={styles.content}>
        <FairyHeader showBack eyebrow="AI 童话工坊" title="漫画已经画好啦" subtitle="三段小小分镜，把同一份喜欢从黄昏一直收藏到月光里。" />

        <FairyCard style={styles.heroCard}>
          <View style={styles.titleRow}>
            <View style={styles.titleCopy}>
              <Text style={styles.comicTitle}>{title}</Text>
              <Text style={styles.comicMeta}>{styleName} · 三幕故事</Text>
            </View>
            <Pressable
              accessibilityRole="button"
              accessibilityLabel={favorite ? '取消收藏漫画' : '收藏漫画'}
              onPress={() => {
                setFavorite((value) => !value);
                setToast({ message: favorite ? '已取消收藏' : '已经放进作品收藏', tone: 'success' });
              }}
              style={({ pressed }) => [styles.favoriteButton, pressed && styles.pressed]}
            >
              <Ionicons name={favorite ? 'heart' : 'heart-outline'} size={22} color={colors.primaryDeep} />
            </Pressable>
          </View>
          <View style={styles.tagRow}>
            <FairyTag tone="gold">漫画</FairyTag>
            <Text style={styles.status}>{status}</Text>
          </View>
          <FairyImage name="aiComicTriptych" height={previewHeight} radius={22} resizeMode="cover" style={styles.previewImage} />
          <Text style={styles.imageCaption}>AI 绘本预览 · 花树、春雨与月夜</Text>
        </FairyCard>

        <Text style={styles.sectionEyebrow}>故事分镜</Text>
        <View style={styles.beatGrid}>
          {storyBeats.map((beat, index) => {
            const active = selectedBeat === index;
            return (
              <Pressable key={beat.title} accessibilityRole="button" onPress={() => setSelectedBeat(index)} style={({ pressed }) => [styles.beatCard, active && styles.beatCardActive, pressed && styles.pressed]}>
                <View style={[styles.beatIcon, active && styles.beatIconActive]}>
                  <Ionicons name={beat.icon} size={20} color={active ? colors.primaryDeep : colors.textSoft} />
                </View>
                <Text style={[styles.beatTitle, active && styles.beatTitleActive]}>{beat.title}</Text>
                <Text style={styles.beatIndex}>0{index + 1}</Text>
              </Pressable>
            );
          })}
        </View>

        <FairyCard style={styles.storyCard}>
          <View style={styles.storyHeading}>
            <Ionicons name={storyBeats[selectedBeat].icon} size={20} color={colors.gold} />
            <Text style={styles.storyTitle}>{storyBeats[selectedBeat].title}</Text>
          </View>
          <Text style={styles.storyText}>{storyBeats[selectedBeat].copy}</Text>
          <View style={styles.divider} />
          <Text style={styles.noteLabel}>创作说明</Text>
          <Text style={styles.noteText}>画面使用温柔纸感与暖色光影生成。你可以继续调整标题和故事，再保存为分享卡片。</Text>
        </FairyCard>

        <View style={styles.actionRow}>
          <FairyButton
            title="保存到作品集"
            onPress={() => setToast({ message: '作品已保存到童话工坊', tone: 'success' })}
            leftContent={<Ionicons name="bookmark-outline" size={20} color={colors.white} />}
            style={styles.actionButton}
          />
          <FairyButton
            title="分享预览"
            variant="secondary"
            onPress={() => router.push('/share-preview')}
            leftContent={<Ionicons name="share-outline" size={20} color={colors.text} />}
            style={styles.actionButton}
          />
        </View>
        <FairyButton
          title="调整故事并重新生成"
          variant="link"
          onPress={() => {
            if (comic?.id) selectAiJob(comic.id);
            router.push('/ai/comic-config');
          }}
          leftContent={<Ionicons name="sparkles-outline" size={18} color={colors.accent} />}
          style={styles.editButton}
        />
        <FairyButton title="返回童话工坊" variant="secondary" onPress={() => router.replace('/(tabs)/workshop')} />
      </View>

      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 760, alignSelf: 'center', paddingHorizontal: spacing.lg },
  heroCard: { padding: spacing.lg, backgroundColor: colors.cardPink, marginTop: spacing.sm },
  titleRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  titleCopy: { flex: 1, minWidth: 0 },
  comicTitle: { color: colors.text, fontSize: 20, fontWeight: '900', lineHeight: 27 },
  comicMeta: { color: colors.textSoft, marginTop: 5, fontSize: 12, fontWeight: '600' },
  favoriteButton: { width: 44, height: 44, borderRadius: 16, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border },
  tagRow: { flexDirection: 'row', alignItems: 'center', marginTop: spacing.md, gap: spacing.sm },
  status: { color: colors.accent, fontSize: 12, fontWeight: '700' },
  previewImage: { marginTop: spacing.md, backgroundColor: colors.card },
  imageCaption: { marginTop: spacing.sm, textAlign: 'center', color: colors.textSoft, fontSize: 11 },
  sectionEyebrow: { marginTop: spacing.xl, marginBottom: spacing.sm, marginLeft: spacing.xs, color: colors.textSoft, fontSize: 13, fontWeight: '800', letterSpacing: 1.2 },
  beatGrid: { flexDirection: 'row', gap: spacing.sm },
  beatCard: { flex: 1, minWidth: 0, minHeight: 104, padding: spacing.md, borderRadius: 20, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card, alignItems: 'center' },
  beatCardActive: { borderColor: colors.primary, backgroundColor: colors.cardPink },
  beatIcon: { width: 38, height: 38, borderRadius: 14, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.background },
  beatIconActive: { backgroundColor: '#FFE7EA' },
  beatTitle: { marginTop: spacing.sm, color: colors.textSoft, fontSize: 13, fontWeight: '800' },
  beatTitleActive: { color: colors.text },
  beatIndex: { position: 'absolute', top: 8, right: 10, color: colors.border, fontSize: 11, fontWeight: '900' },
  storyCard: { marginTop: spacing.md, marginBottom: spacing.xl },
  storyHeading: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  storyTitle: { color: colors.text, fontSize: 17, fontWeight: '900' },
  storyText: { marginTop: spacing.sm, color: colors.text, fontSize: 15, lineHeight: 24 },
  divider: { height: StyleSheet.hairlineWidth, backgroundColor: colors.border, marginVertical: spacing.md },
  noteLabel: { color: colors.accent, fontSize: 12, fontWeight: '800' },
  noteText: { marginTop: 5, color: colors.textSoft, fontSize: 13, lineHeight: 21 },
  actionRow: { flexDirection: 'row', gap: spacing.md },
  actionButton: { flex: 1 },
  editButton: { marginVertical: spacing.lg, alignSelf: 'center' },
  pressed: { opacity: 0.68 },
});
