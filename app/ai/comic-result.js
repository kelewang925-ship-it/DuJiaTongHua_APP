import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View, useWindowDimensions } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';
import { hasCapability } from '../../src/config/capabilities';

export default function ComicResultPage() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const { id } = useLocalSearchParams();
  const comicId = Array.isArray(id) ? id[0] : id;
  const creations = useFairyStore((state) => state.creations);
  const selectAiJob = useFairyStore((state) => state.selectAiJob);
  const [selectedBeat, setSelectedBeat] = useState(0);
  const [favorite, setFavorite] = useState(false);
  const [toast, setToast] = useState(null);
  const canGenerate = hasCapability('aiGeneration');

  const comic = useMemo(() => {
    if (comicId) return creations.find((item) => item.id === comicId && item.type === '漫画');
    return creations.find((item) => item.type === '漫画');
  }, [comicId, creations]);

  const storyBeats = Array.isArray(comic?.storyBeats) ? comic.storyBeats.filter(Boolean) : [];
  const activeBeat = storyBeats[selectedBeat] || storyBeats[0];
  const previewHeight = Math.min(240, Math.max(116, (Math.min(width, 760) - spacing.lg * 2) / 3));
  const unavailable = () => setToast({ message: 'Real 模式暂未开放 AI 作品保存与重新生成。', tone: 'info' });

  return (
    <FairyPage
      backgroundName="creamPaper"
      topSpace={28}
      bottomSpace={64}
      header={<FairyHeader showBack eyebrow="AI 童话工坊" title={comic ? '漫画作品详情' : '作品不存在'} subtitle={comic ? '查看这次真实创作保存下来的作品信息。' : '这份作品可能尚未生成、已经删除，或当前账号无权访问。'} />}
    >
      <View style={styles.content}>
        {comic ? (
          <>
            <FairyCard style={styles.heroCard}>
              <View style={styles.titleRow}>
                <View style={styles.titleCopy}>
                  <Text style={styles.comicTitle}>{comic.title || '未命名漫画'}</Text>
                  <Text style={styles.comicMeta}>{comic.styleName || '未标注风格'}</Text>
                </View>
                <Pressable
                  accessibilityRole="button"
                  accessibilityLabel={favorite ? '取消收藏漫画' : '收藏漫画'}
                  onPress={() => {
                    if (!canGenerate) { unavailable(); return; }
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
                <Text style={styles.status}>{comic.status || '状态未知'}</Text>
              </View>
              {comic.previewImageName ? (
                <>
                  <FairyImage name={comic.previewImageName} height={previewHeight} radius={22} resizeMode="cover" style={styles.previewImage} />
                  {comic.imageCaption ? <Text style={styles.imageCaption}>{comic.imageCaption}</Text> : null}
                </>
              ) : (
                <Text style={styles.missingPreview}>这份作品暂时没有可展示的预览图。</Text>
              )}
            </FairyCard>

            {storyBeats.length > 0 ? (
              <>
                <Text style={styles.sectionEyebrow}>故事分镜</Text>
                <View style={styles.beatGrid}>
                  {storyBeats.map((beat, index) => {
                    const active = selectedBeat === index;
                    return (
                      <Pressable key={`${beat.title || '分镜'}-${index}`} accessibilityRole="button" onPress={() => setSelectedBeat(index)} style={({ pressed }) => [styles.beatCard, active && styles.beatCardActive, pressed && styles.pressed]}>
                        <View style={[styles.beatIcon, active && styles.beatIconActive]}><Ionicons name={beat.icon || 'image-outline'} size={20} color={active ? colors.primaryDeep : colors.textSoft} /></View>
                        <Text style={[styles.beatTitle, active && styles.beatTitleActive]}>{beat.title || `分镜 ${index + 1}`}</Text>
                        <Text style={styles.beatIndex}>{String(index + 1).padStart(2, '0')}</Text>
                      </Pressable>
                    );
                  })}
                </View>
                {activeBeat ? (
                  <FairyCard style={styles.storyCard}>
                    <View style={styles.storyHeading}>
                      <Ionicons name={activeBeat.icon || 'image-outline'} size={20} color={colors.gold} />
                      <Text style={styles.storyTitle}>{activeBeat.title || '未命名分镜'}</Text>
                    </View>
                    <Text style={styles.storyText}>{activeBeat.copy || '这段分镜暂时没有文字说明。'}</Text>
                  </FairyCard>
                ) : null}
              </>
            ) : null}

            <View style={styles.actionRow}>
              <FairyButton title={canGenerate ? '保存到作品集' : '作品保存未开放'} onPress={() => canGenerate ? setToast({ message: '作品已保存到童话工坊', tone: 'success' }) : unavailable()} leftContent={<Ionicons name="bookmark-outline" size={20} color={colors.white} />} style={styles.actionButton} />
              <FairyButton title="分享预览" variant="secondary" onPress={() => router.push({ pathname: '/share-preview', params: { id: comic.id, type: 'comic' } })} leftContent={<Ionicons name="share-outline" size={20} color={colors.text} />} style={styles.actionButton} />
            </View>
            <FairyButton
              title={canGenerate ? '调整故事并重新生成' : '重新生成未开放'}
              variant="link"
              onPress={() => {
                if (!canGenerate) { unavailable(); return; }
                selectAiJob(comic.id);
                router.push('/ai/comic-config');
              }}
              leftContent={<Ionicons name="sparkles-outline" size={18} color={colors.accent} />}
              style={styles.editButton}
            />
            <FairyButton title="返回童话工坊" variant="secondary" onPress={() => router.replace('/(tabs)/workshop')} />
          </>
        ) : (
          <FairyEmptyState
            imageName="emptyAiHistory"
            title="没有找到这份漫画"
            description="它可能尚未生成、已经删除，或当前账号无权访问。返回童话工坊后可以选择其他真实作品。"
            actionTitle="返回童话工坊"
            onAction={() => router.replace('/(tabs)/workshop')}
          />
        )}
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
  missingPreview: { marginTop: spacing.md, color: colors.textSoft, lineHeight: 21, textAlign: 'center' },
  sectionEyebrow: { marginTop: spacing.xl, marginBottom: spacing.sm, marginLeft: spacing.xs, color: colors.textSoft, fontSize: 13, fontWeight: '800', letterSpacing: 1.2 },
  beatGrid: { flexDirection: 'row', gap: spacing.sm, flexWrap: 'wrap' },
  beatCard: { flexGrow: 1, flexBasis: 120, minHeight: 104, padding: spacing.md, borderRadius: 20, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card, alignItems: 'center' },
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
  actionRow: { flexDirection: 'row', gap: spacing.md },
  actionButton: { flex: 1 },
  editButton: { marginVertical: spacing.lg, alignSelf: 'center' },
  pressed: { opacity: 0.68 },
});
