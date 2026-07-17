import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyInput from '@/components/FairyInput';
import FairyPage from '@/components/FairyPage';
import FairyTag from '@/components/FairyTag';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';

const coverOptions = [
  { id: 'sunset', image: 'homeCover', label: '晚霞' },
  { id: 'flowers', image: 'anniversaryCover', label: '花束' },
  { id: 'sky', image: 'albumCover', label: '晴空' },
  { id: 'night', image: 'coupleCover', label: '夜色' },
];
const musicOptions = ['轻柔', '甜一点', '安静'];
const clips = [
  { image: 'homeCover', label: '相遇', time: '00:05' },
  { image: 'albumCover', label: '散步', time: '00:05' },
  { image: 'anniversaryCover', label: '花束', time: '00:06' },
  { image: 'coupleCover', label: '晚霞', time: '00:05' },
];

export default function VideoPreviewPage() {
  const creations = useFairyStore((state) => state.creations);
  const latestVideo = creations.find((item) => item.type === '视频') || creations[0];
  const [playing, setPlaying] = useState(false);
  const [cover, setCover] = useState(coverOptions[0].id);
  const [subtitle, setSubtitle] = useState('把晚霞藏进回忆里');
  const [music, setMusic] = useState(musicOptions[0]);
  const [toast, setToast] = useState(null);
  const activeCover = coverOptions.find((item) => item.id === cover) || coverOptions[0];

  const saveVideo = () => setToast({ message: '视频已保存到创作历史', tone: 'success' });
  const shareVideo = () => setToast({ message: '分享卡片已经准备好', tone: 'success' });

  return (
    <FairyPage backgroundName="creamPaper" header={<FairyHeader showBack title="视频预览" right={<Pressable onPress={saveVideo} hitSlop={10}><Ionicons name="save-outline" size={24} color={colors.text} /></Pressable>} />} topSpace={18} bottomSpace={64}>
      <View style={styles.content}>
        <Text style={styles.subtitle}>每一帧，都是我们的童话</Text>

        <FairyCard style={styles.playerCard}>
          <View style={styles.player}>
            <FairyImage name={activeCover.image} height={360} radius={22} framed={false} />
            <View style={styles.playerShade} />
            <Pressable onPress={() => setPlaying((value) => !value)} style={({ pressed }) => [styles.playButton, pressed && styles.pressed]}>
              <Ionicons name={playing ? 'pause' : 'play'} size={31} color={colors.brown} />
            </Pressable>
            <Text style={styles.playerTitle}>{latestVideo?.title || '我们的晚霞小电影'}</Text>
            <View style={styles.progressTrack}><View style={[styles.progressFill, { width: playing ? '58%' : '18%' }]} /></View>
            <View style={styles.timeRow}><Text style={styles.timeText}>{playing ? '00:17' : '00:00'}</Text><Text style={styles.timeText}>00:30</Text></View>
          </View>
        </FairyCard>

        <FairyCard style={styles.editCard}>
          <SectionTitle icon="image-outline" title="封面" />
          <View style={styles.coverRow}>
            {coverOptions.map((item) => {
              const active = cover === item.id;
              return (
                <Pressable key={item.id} onPress={() => setCover(item.id)} style={({ pressed }) => [styles.coverOption, active && styles.coverActive, pressed && styles.pressed]}>
                  <FairyImage name={item.image} height={116} radius={13} framed={false} />
                  <Text style={styles.coverLabel}>{item.label}</Text>
                  {active ? <View style={styles.check}><Ionicons name="checkmark" size={14} color={colors.white} /></View> : null}
                </Pressable>
              );
            })}
          </View>
        </FairyCard>

        <FairyCard style={styles.editCard}>
          <SectionTitle icon="chatbubble-ellipses-outline" title="字幕" />
          <FairyInput value={subtitle} onChangeText={setSubtitle} maxLength={32} placeholder="写下一句片中字幕" containerStyle={styles.noMargin} />
        </FairyCard>

        <FairyCard style={styles.editCard}>
          <SectionTitle icon="musical-notes-outline" title="音乐" />
          <View style={styles.musicRow}>
            {musicOptions.map((item) => (
              <Pressable key={item} onPress={() => setMusic(item)} style={({ pressed }) => [styles.musicChip, music === item && styles.musicActive, pressed && styles.pressed]}>
                <Text style={[styles.musicText, music === item && styles.musicTextActive]}>{item}</Text>
              </Pressable>
            ))}
          </View>
          <View style={styles.songRow}><Ionicons name="musical-note" size={20} color={colors.primaryDeep} /><View style={styles.songCopy}><Text style={styles.songTitle}>晚风与心事</Text><Text style={styles.songTime}>01:23 · {music}版</Text></View><Ionicons name="play-circle-outline" size={28} color={colors.accent} /></View>
        </FairyCard>

        <FairyCard style={styles.editCard}>
          <SectionTitle icon="film-outline" title="片段" note="点击可编辑" />
          <View style={styles.clipRow}>
            {clips.map((item, index) => (
              <Pressable key={item.label} onPress={() => setToast({ message: `已选中第 ${index + 1} 个片段`, tone: 'info' })} style={({ pressed }) => [styles.clip, pressed && styles.pressed]}>
                <FairyImage name={item.image} height={102} radius={12} framed={false} />
                <View style={styles.clipMeta}><Text style={styles.clipIndex}>{index + 1}</Text><Text style={styles.clipTime}>{item.time}</Text></View>
              </Pressable>
            ))}
          </View>
        </FairyCard>

        <View style={styles.actionRow}>
          <FairyButton title="保存视频" onPress={saveVideo} style={styles.actionButton} leftContent={<Ionicons name="save-outline" size={19} color={colors.white} />} />
          <FairyButton title="分享给 TA" variant="secondary" onPress={shareVideo} style={styles.actionButton} leftContent={<Ionicons name="heart-outline" size={19} color={colors.text} />} />
        </View>
        <Pressable onPress={() => router.push('/ai/video-config')} style={styles.regenerate}><Ionicons name="refresh-outline" size={17} color={colors.textSoft} /><Text style={styles.regenerateText}>重新生成视频</Text></Pressable>
      </View>
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function SectionTitle({ icon, title, note }) {
  return <View style={styles.sectionHeading}><View style={styles.sectionTitleWrap}><Ionicons name={icon} size={19} color={colors.gold} /><Text style={styles.sectionTitle}>{title}</Text></View>{note ? <Text style={styles.sectionNote}>{note}</Text> : null}</View>;
}

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 760, alignSelf: 'center' },
  subtitle: { marginBottom: spacing.lg, textAlign: 'center', color: colors.textSoft, fontSize: 14, fontWeight: '700' },
  playerCard: { marginBottom: spacing.lg, backgroundColor: colors.cardPink },
  player: { position: 'relative', overflow: 'hidden', borderRadius: 22 },
  playerShade: { ...StyleSheet.absoluteFillObject, backgroundColor: 'rgba(55,34,31,0.15)' },
  playButton: { position: 'absolute', left: '50%', top: '45%', marginLeft: -31, marginTop: -31, width: 62, height: 62, borderRadius: 31, alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(255,249,244,0.9)', borderWidth: 2, borderColor: colors.white },
  playerTitle: { position: 'absolute', left: spacing.xl, right: spacing.xl, bottom: 52, color: colors.white, fontSize: 23, fontWeight: '900', textAlign: 'center', textShadowColor: 'rgba(40,25,20,0.4)', textShadowOffset: { width: 0, height: 1 }, textShadowRadius: 5 },
  progressTrack: { position: 'absolute', left: spacing.lg, right: spacing.lg, bottom: 30, height: 4, borderRadius: 2, backgroundColor: 'rgba(255,255,255,0.55)' },
  progressFill: { height: 4, borderRadius: 2, backgroundColor: colors.primary },
  timeRow: { position: 'absolute', left: spacing.lg, right: spacing.lg, bottom: 8, flexDirection: 'row', justifyContent: 'space-between' },
  timeText: { color: colors.white, fontSize: 10, fontWeight: '800' },
  editCard: { marginBottom: spacing.lg },
  sectionHeading: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm, marginBottom: spacing.md },
  sectionTitleWrap: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  sectionTitle: { color: colors.text, fontSize: 17, fontWeight: '900' },
  sectionNote: { color: colors.textSoft, fontSize: 11 },
  coverRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  coverOption: { position: 'relative', minWidth: 118, width: '23.6%', padding: spacing.xs, borderRadius: 17, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  coverActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  coverLabel: { paddingVertical: spacing.sm, textAlign: 'center', color: colors.text, fontSize: 11, fontWeight: '800' },
  check: { position: 'absolute', top: -6, right: -6, width: 25, height: 25, borderRadius: 13, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.primaryDeep, borderWidth: 2, borderColor: colors.white },
  noMargin: { marginBottom: 0 },
  musicRow: { flexDirection: 'row', gap: spacing.sm },
  musicChip: { flex: 1, minHeight: 42, alignItems: 'center', justifyContent: 'center', borderRadius: 16, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  musicActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  musicText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  musicTextActive: { color: colors.primaryDeep },
  songRow: { marginTop: spacing.md, flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.md, borderRadius: 18, backgroundColor: colors.background },
  songCopy: { flex: 1 },
  songTitle: { color: colors.text, fontSize: 13, fontWeight: '900' },
  songTime: { marginTop: 3, color: colors.textSoft, fontSize: 10 },
  clipRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  clip: { width: '23.6%', minWidth: 118, padding: spacing.xs, borderRadius: 16, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  clipMeta: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: spacing.xs },
  clipIndex: { color: colors.primaryDeep, fontSize: 11, fontWeight: '900' },
  clipTime: { color: colors.textSoft, fontSize: 10 },
  actionRow: { flexDirection: 'row', gap: spacing.md },
  actionButton: { flex: 1 },
  regenerate: { minHeight: 48, marginTop: spacing.md, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm },
  regenerateText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  pressed: { opacity: 0.68 },
});
