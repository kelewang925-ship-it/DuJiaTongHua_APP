import { useState } from 'react';
import { Pressable, StyleSheet, Switch, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyInput from '../../src/components/FairyInput';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';
import { hasCapability } from '../../src/config/capabilities';

const sourceOptions = [
  { value: '照片', detail: '把相册剪成故事', image: 'albumCover' },
  { value: '日记', detail: '让文字成为旁白', image: 'homeCover' },
  { value: 'AI 漫画', detail: '让分镜开始播放', image: 'aiComicTriptych' },
];
const styleOptions = [
  { value: '绘本影片', icon: 'book-outline' },
  { value: '慢慢回忆', icon: 'videocam-outline' },
  { value: '纪念日', icon: 'calendar-outline' },
];
const durationOptions = ['15 秒', '30 秒', '60 秒'];
const musicOptions = ['钢琴轻语', '午后风铃', '星光慢歌'];
const coverOptions = [
  { id: 'sunset', image: 'homeCover', label: '晚霞' },
  { id: 'flowers', image: 'anniversaryCover', label: '花束' },
  { id: 'sky', image: 'albumCover', label: '晴空' },
  { id: 'night', image: 'coupleCover', label: '夜色' },
];

export default function VideoConfigPage() {
  const addCreation = useFairyStore((state) => state.addCreation);
  const [title, setTitle] = useState('春天散步纪念视频');
  const [source, setSource] = useState(sourceOptions[0].value);
  const [styleName, setStyleName] = useState(styleOptions[0].value);
  const [duration, setDuration] = useState(durationOptions[1]);
  const [music, setMusic] = useState(musicOptions[0]);
  const [autoCaption, setAutoCaption] = useState(true);
  const [softMusic, setSoftMusic] = useState(true);
  const [cover, setCover] = useState(coverOptions[0].id);
  const [toast, setToast] = useState(null);

  const handleGenerate = () => {
    if (!hasCapability('aiGeneration')) { setToast({ message: 'Real 模式暂未开放 AI 生成。', tone: 'info' }); return; }
    if (!title.trim()) {
      setToast({ message: '请先写下视频名称', tone: 'error' });
      return;
    }
    addCreation({
      type: '视频',
      title: title.trim(),
      source,
      styleName: `${styleName} · ${duration} · ${music}`,
      status: '生成中 · 正在整理镜头与声音',
      icon: 'film-outline',
      progress: 46,
    });
    router.push('/ai/progress');
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="AI 短视频" right={<Ionicons name="help-circle-outline" size={25} color={colors.textSoft} />} />}
      topSpace={18}
      bottomSpace={64}
    >
      <View style={styles.content}>
        <FairyCard style={styles.heroCard}>
          <FairyImage name="workshopCover" height={210} radius={22} framed={false} />
          <View style={styles.heroCopy}>
            <FairyTag tone="gold">回忆放映机</FairyTag>
            <Text style={styles.heroTitle}>把回忆剪成一段温柔小电影</Text>
            <Text style={styles.heroText}>画面、字幕和音乐会保持同一套绘本氛围。</Text>
          </View>
        </FairyCard>

        <FairyCard style={styles.formCard}>
          <FairyInput label="作品名称" icon="film-outline" value={title} onChangeText={setTitle} maxLength={30} placeholder="例如：一起散步的春天" containerStyle={styles.titleInput} />

          <SectionTitle title="选择回忆素材" />
          <View style={styles.sourceRow}>
            {sourceOptions.map((item) => {
              const active = source === item.value;
              return (
                <Pressable key={item.value} onPress={() => setSource(item.value)} style={({ pressed }) => [styles.sourceCard, active && styles.sourceActive, pressed && styles.pressed]}>
                  <FairyImage name={item.image} height={82} radius={14} framed={false} />
                  <Text style={[styles.sourceTitle, active && styles.activeText]}>{item.value}</Text>
                  <Text style={styles.sourceDetail}>{item.detail}</Text>
                  <View style={[styles.radio, active && styles.radioActive]}>{active ? <Ionicons name="checkmark" size={14} color={colors.white} /> : null}</View>
                </Pressable>
              );
            })}
          </View>

          <View style={styles.divider} />
          <SectionTitle title="视频风格" />
          <View style={styles.optionRow}>
            {styleOptions.map((item) => {
              const active = styleName === item.value;
              return (
                <Pressable key={item.value} onPress={() => setStyleName(item.value)} style={({ pressed }) => [styles.option, active && styles.optionActive, pressed && styles.pressed]}>
                  <Ionicons name={item.icon} size={20} color={active ? colors.primaryDeep : colors.textSoft} />
                  <Text style={[styles.optionText, active && styles.activeText]}>{item.value}</Text>
                </Pressable>
              );
            })}
          </View>

          <View style={styles.divider} />
          <SectionTitle title="视频时长" note={duration} />
          <View style={styles.segmentRow}>
            {durationOptions.map((item) => {
              const active = duration === item;
              return (
                <Pressable key={item} onPress={() => setDuration(item)} style={({ pressed }) => [styles.segment, active && styles.segmentActive, pressed && styles.pressed]}>
                  <Text style={[styles.segmentText, active && styles.activeText]}>{item}</Text>
                </Pressable>
              );
            })}
          </View>

          <View style={styles.divider} />
          <SectionTitle title="声音与字幕" />
          <SettingRow icon="chatbubble-ellipses-outline" title="自动字幕" detail="识别回忆文案并生成温柔字幕" value={autoCaption} onValueChange={setAutoCaption} />
          <SettingRow icon="musical-notes-outline" title="轻音乐" detail={softMusic ? music : '已关闭背景音乐'} value={softMusic} onValueChange={setSoftMusic} />
          {softMusic ? (
            <View style={styles.musicRow}>
              {musicOptions.map((item) => (
                <Pressable key={item} onPress={() => setMusic(item)} style={({ pressed }) => [styles.musicChip, music === item && styles.musicChipActive, pressed && styles.pressed]}>
                  <Text style={[styles.musicText, music === item && styles.activeText]}>{item}</Text>
                </Pressable>
              ))}
            </View>
          ) : null}
        </FairyCard>

        <FairyCard style={styles.coverCard}>
          <SectionTitle title="选择封面" note="最能代表这段回忆的一帧" />
          <View style={styles.coverRow}>
            {coverOptions.map((item) => {
              const active = cover === item.id;
              return (
                <Pressable key={item.id} onPress={() => setCover(item.id)} style={({ pressed }) => [styles.coverOption, active && styles.coverActive, pressed && styles.pressed]}>
                  <FairyImage name={item.image} height={114} radius={14} framed={false} />
                  <Text style={styles.coverLabel}>{item.label}</Text>
                  {active ? <View style={styles.coverBadge}><Ionicons name="heart" size={14} color={colors.white} /></View> : null}
                </Pressable>
              );
            })}
          </View>
        </FairyCard>

        <FairyButton title="生成视频" onPress={handleGenerate} leftContent={<Ionicons name="color-wand" size={20} color={colors.white} />} />
        <Text style={styles.estimate}>预计 1–3 分钟完成 · 作品会自动保存到创作历史</Text>
      </View>
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function SectionTitle({ title, note }) {
  return (
    <View style={styles.sectionHeading}>
      <View style={styles.sectionTitleWrap}><Ionicons name="sparkles" size={14} color={colors.gold} /><Text style={styles.sectionTitle}>{title}</Text></View>
      {note ? <Text style={styles.sectionNote}>{note}</Text> : null}
    </View>
  );
}

function SettingRow({ icon, title, detail, value, onValueChange }) {
  return (
    <View style={styles.settingRow}>
      <View style={styles.settingIcon}><Ionicons name={icon} size={21} color={colors.accent} /></View>
      <View style={styles.settingCopy}><Text style={styles.settingTitle}>{title}</Text><Text style={styles.settingDetail}>{detail}</Text></View>
      <Switch value={value} onValueChange={onValueChange} trackColor={{ false: colors.secondary, true: colors.primary }} thumbColor={colors.white} />
    </View>
  );
}

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 760, alignSelf: 'center' },
  heroCard: { marginBottom: spacing.lg, backgroundColor: colors.cardPink },
  heroCopy: { marginTop: spacing.md },
  heroTitle: { marginTop: spacing.md, color: colors.text, fontSize: 20, lineHeight: 28, fontWeight: '900' },
  heroText: { marginTop: spacing.xs, color: colors.textSoft, fontSize: 12, lineHeight: 20 },
  formCard: { marginBottom: spacing.lg },
  titleInput: { marginBottom: spacing.xl },
  sectionHeading: { minHeight: 28, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm, marginBottom: spacing.md },
  sectionTitleWrap: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  sectionTitle: { color: colors.text, fontSize: 17, fontWeight: '900' },
  sectionNote: { flexShrink: 1, textAlign: 'right', color: colors.primaryDeep, fontSize: 11, fontWeight: '800' },
  sourceRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  sourceCard: { position: 'relative', flexGrow: 1, minWidth: 150, width: '31%', padding: spacing.sm, borderRadius: 20, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  sourceActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  sourceTitle: { marginTop: spacing.sm, textAlign: 'center', color: colors.text, fontSize: 14, fontWeight: '900' },
  sourceDetail: { marginTop: 3, textAlign: 'center', color: colors.textSoft, fontSize: 10 },
  radio: { position: 'absolute', top: 4, right: 4, width: 24, height: 24, borderRadius: 12, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card, borderWidth: 1.5, borderColor: colors.primary },
  radioActive: { backgroundColor: colors.primaryDeep, borderColor: colors.white },
  divider: { height: 1, backgroundColor: colors.border, marginVertical: spacing.xl },
  optionRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  option: { flexGrow: 1, minWidth: 120, minHeight: 50, paddingHorizontal: spacing.md, borderRadius: 18, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.xs },
  optionActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  optionText: { color: colors.textSoft, fontSize: 13, fontWeight: '800' },
  activeText: { color: colors.primaryDeep },
  segmentRow: { flexDirection: 'row', padding: spacing.xs, borderRadius: 18, backgroundColor: colors.background },
  segment: { flex: 1, minHeight: 44, alignItems: 'center', justifyContent: 'center', borderRadius: 15 },
  segmentActive: { backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.primary },
  segmentText: { color: colors.textSoft, fontSize: 13, fontWeight: '700' },
  settingRow: { flexDirection: 'row', alignItems: 'center', minHeight: 66, gap: spacing.md, borderBottomWidth: 1, borderBottomColor: colors.border },
  settingIcon: { width: 42, height: 42, borderRadius: 15, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  settingCopy: { flex: 1, minWidth: 0 },
  settingTitle: { color: colors.text, fontSize: 14, fontWeight: '900' },
  settingDetail: { marginTop: 3, color: colors.textSoft, fontSize: 10, lineHeight: 16 },
  musicRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginTop: spacing.md },
  musicChip: { flexGrow: 1, minWidth: 100, minHeight: 38, alignItems: 'center', justifyContent: 'center', paddingHorizontal: spacing.sm, borderRadius: 15, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  musicChipActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  musicText: { color: colors.textSoft, fontSize: 11, fontWeight: '800' },
  coverCard: { marginBottom: spacing.xl, backgroundColor: colors.cardPink },
  coverRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  coverOption: { position: 'relative', width: '23.6%', minWidth: 118, padding: spacing.xs, borderRadius: 18, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card },
  coverActive: { borderColor: colors.primaryDeep },
  coverLabel: { paddingVertical: spacing.sm, textAlign: 'center', color: colors.text, fontSize: 11, fontWeight: '800' },
  coverBadge: { position: 'absolute', top: -6, right: -6, width: 26, height: 26, borderRadius: 13, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.primaryDeep, borderWidth: 2, borderColor: colors.white },
  estimate: { marginTop: spacing.md, textAlign: 'center', color: colors.textSoft, fontSize: 11 },
  pressed: { opacity: 0.68 },
});
