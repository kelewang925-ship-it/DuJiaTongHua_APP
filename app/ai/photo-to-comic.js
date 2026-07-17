import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
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
import { hasCapability } from '../../src/config/capabilities';

const photoOptions = [
  { id: 'rain', image: 'homeCover', label: '雨天散步' },
  { id: 'city', image: 'albumCover', label: '城市晴空' },
  { id: 'flowers', image: 'anniversaryCover', label: '花束纪念' },
  { id: 'lamp', image: 'coupleCover', label: '晚风路灯' },
  { id: 'letters', image: 'timeCapsuleCover', label: '时光来信' },
];
const styleOptions = [
  { value: '绘本风', icon: 'color-palette-outline' },
  { value: '手绘漫画', icon: 'pencil-outline' },
  { value: '水彩童话', icon: 'water-outline' },
];
const moodOptions = [
  { value: '温柔', icon: 'flower-outline' },
  { value: '明亮', icon: 'sunny-outline' },
  { value: '复古', icon: 'camera-outline' },
];
const detailOptions = ['柔和', '适中', '精细'];

export default function PhotoToComicPage() {
  const addCreation = useFairyStore((state) => state.addCreation);
  const [selectedPhotos, setSelectedPhotos] = useState(photoOptions.slice(0, 4).map((item) => item.id));
  const [styleName, setStyleName] = useState(styleOptions[0].value);
  const [mood, setMood] = useState(moodOptions[0].value);
  const [detail, setDetail] = useState(detailOptions[1]);
  const [toast, setToast] = useState(null);

  const selectedItems = useMemo(
    () => photoOptions.filter((item) => selectedPhotos.includes(item.id)),
    [selectedPhotos],
  );

  const togglePhoto = (id) => {
    setSelectedPhotos((current) => {
      if (current.includes(id)) return current.filter((item) => item !== id);
      if (current.length >= 6) {
        setToast({ message: '一次最多选择 6 张照片', tone: 'info' });
        return current;
      }
      return [...current, id];
    });
  };

  const addFromAlbum = () => {
    const next = photoOptions.find((item) => !selectedPhotos.includes(item.id));
    if (!next) {
      setToast({ message: '这组回忆照片已经全部加入', tone: 'success' });
      return;
    }
    togglePhoto(next.id);
  };

  const generate = () => {
    if (!hasCapability('aiGeneration')) { setToast({ message: 'Real 模式暂未开放 AI 生成。', tone: 'info' }); return; }
    if (!selectedPhotos.length) {
      setToast({ message: '请至少选择一张照片', tone: 'error' });
      return;
    }
    addCreation({
      type: '漫画',
      title: '照片里的温柔小漫画',
      source: `${selectedPhotos.length} 张照片`,
      styleName: `${styleName} · ${mood} · ${detail}`,
      status: '生成中 · 正在统一人物与画面色彩',
      icon: 'images-outline',
      progress: 62,
    });
    router.push('/ai/progress');
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="照片转漫画" right={<Ionicons name="help-circle-outline" size={25} color={colors.textSoft} />} />}
      topSpace={18}
      bottomSpace={64}
    >
      <View style={styles.content}>
        <View style={styles.intro}>
          <Ionicons name="sparkles" size={19} color={colors.gold} />
          <Text style={styles.introText}>把照片变成绘本一页</Text>
        </View>

        <FairyCard style={styles.photoCard}>
          <SectionTitle title="选择照片" note={`已选 ${selectedPhotos.length} 张`} />
          <View style={styles.photoGrid}>
            {photoOptions.slice(0, 4).map((item) => {
              const active = selectedPhotos.includes(item.id);
              return (
                <Pressable key={item.id} onPress={() => togglePhoto(item.id)} style={({ pressed }) => [styles.photoTile, active && styles.photoTileActive, pressed && styles.pressed]}>
                  <FairyImage name={item.image} height={118} radius={16} framed={false} />
                  <Text style={styles.photoLabel}>{item.label}</Text>
                  <View style={[styles.check, active && styles.checkActive]}>
                    {active ? <Ionicons name="checkmark" size={17} color={colors.white} /> : null}
                  </View>
                </Pressable>
              );
            })}
            <Pressable onPress={addFromAlbum} style={({ pressed }) => [styles.addTile, pressed && styles.pressed]}>
              <Ionicons name="add" size={34} color={colors.primaryDeep} />
              <Text style={styles.addText}>添加照片</Text>
            </Pressable>
          </View>
        </FairyCard>

        <FairyCard style={styles.optionCard}>
          <SectionTitle title="漫画风格" />
          <OptionRow options={styleOptions} value={styleName} onChange={setStyleName} />
          <View style={styles.divider} />
          <SectionTitle title="画面氛围" />
          <OptionRow options={moodOptions} value={mood} onChange={setMood} />
          <View style={styles.divider} />
          <SectionTitle title="细节强度" note={detail} />
          <View style={styles.segmentRow}>
            {detailOptions.map((item) => {
              const active = detail === item;
              return (
                <Pressable key={item} onPress={() => setDetail(item)} style={({ pressed }) => [styles.segment, active && styles.segmentActive, pressed && styles.pressed]}>
                  <Text style={[styles.segmentText, active && styles.segmentTextActive]}>{item}</Text>
                </Pressable>
              );
            })}
          </View>
        </FairyCard>

        <FairyCard style={styles.previewCard}>
          <SectionTitle title="漫画预览" note="生成后可继续编辑" />
          <View style={styles.previewGrid}>
            {(selectedItems.length ? selectedItems : photoOptions).slice(0, 4).map((item) => (
              <FairyImage key={item.id} name={item.image} height={104} radius={12} framed={false} style={styles.previewImage} />
            ))}
          </View>
          <View style={styles.previewMeta}>
            <FairyTag tone="gold">{styleName}</FairyTag>
            <Text style={styles.previewText}>{mood}氛围 · {detail}细节</Text>
          </View>
        </FairyCard>

        <FairyButton title="生成漫画" onPress={generate} leftContent={<Ionicons name="color-wand" size={20} color={colors.white} />} />
        <Text style={styles.estimate}>预计 1–2 分钟生成 · 离开页面后仍会继续</Text>
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

function OptionRow({ options, value, onChange }) {
  return (
    <View style={styles.optionRow}>
      {options.map((item) => {
        const active = value === item.value;
        return (
          <Pressable key={item.value} onPress={() => onChange(item.value)} style={({ pressed }) => [styles.option, active && styles.optionActive, pressed && styles.pressed]}>
            <Ionicons name={item.icon} size={20} color={active ? colors.primaryDeep : colors.textSoft} />
            <Text style={[styles.optionText, active && styles.optionTextActive]}>{item.value}</Text>
            {active ? <Ionicons name="checkmark-circle" size={17} color={colors.primaryDeep} /> : null}
          </Pressable>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 760, alignSelf: 'center' },
  intro: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, marginBottom: spacing.lg },
  introText: { color: colors.textSoft, fontSize: 14, fontWeight: '700' },
  photoCard: { marginBottom: spacing.lg },
  sectionHeading: { minHeight: 28, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm, marginBottom: spacing.md },
  sectionTitleWrap: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  sectionTitle: { color: colors.text, fontSize: 17, fontWeight: '900' },
  sectionNote: { color: colors.primaryDeep, fontSize: 12, fontWeight: '800' },
  photoGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md },
  photoTile: { position: 'relative', width: '47.8%', borderRadius: 20, padding: spacing.xs, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border },
  photoTileActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  photoLabel: { paddingVertical: spacing.sm, textAlign: 'center', color: colors.text, fontSize: 12, fontWeight: '800' },
  check: { position: 'absolute', top: -7, right: -7, width: 29, height: 29, borderRadius: 15, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card, borderWidth: 2, borderColor: colors.primary },
  checkActive: { backgroundColor: colors.primaryDeep, borderColor: colors.white },
  addTile: { width: '47.8%', minHeight: 158, borderRadius: 20, borderWidth: 1.5, borderStyle: 'dashed', borderColor: colors.primary, backgroundColor: 'rgba(255,249,244,0.62)', alignItems: 'center', justifyContent: 'center' },
  addText: { marginTop: spacing.sm, color: colors.textSoft, fontSize: 13, fontWeight: '800' },
  optionCard: { marginBottom: spacing.lg },
  optionRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  option: { flexGrow: 1, minWidth: 118, minHeight: 52, paddingHorizontal: spacing.md, borderRadius: 18, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.xs },
  optionActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  optionText: { color: colors.textSoft, fontSize: 13, fontWeight: '800' },
  optionTextActive: { color: colors.text },
  divider: { height: 1, backgroundColor: colors.border, marginVertical: spacing.xl },
  segmentRow: { flexDirection: 'row', padding: spacing.xs, borderRadius: 18, backgroundColor: colors.background },
  segment: { flex: 1, minHeight: 42, alignItems: 'center', justifyContent: 'center', borderRadius: 15 },
  segmentActive: { backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.primary },
  segmentText: { color: colors.textSoft, fontSize: 13, fontWeight: '700' },
  segmentTextActive: { color: colors.primaryDeep, fontWeight: '900' },
  previewCard: { marginBottom: spacing.xl, backgroundColor: colors.cardPink },
  previewGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  previewImage: { width: '48.8%' },
  previewMeta: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm, marginTop: spacing.md },
  previewText: { flex: 1, textAlign: 'right', color: colors.textSoft, fontSize: 11 },
  estimate: { marginTop: spacing.md, textAlign: 'center', color: colors.textSoft, fontSize: 11 },
  pressed: { opacity: 0.68 },
});
