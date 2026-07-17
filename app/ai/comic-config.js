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

const sourceOptions = [
  { value: '选择照片', label: '照片', detail: '从相册选择', icon: 'images-outline' },
  { value: '选择日记', label: '日记', detail: '从日记选择', icon: 'book-outline' },
  { value: '选择纪念日', label: '纪念日', detail: '从日期选择', icon: 'calendar-outline' },
];
const styleOptions = [
  { value: '童话绘本', icon: 'color-palette-outline' },
  { value: '水彩感', icon: 'water-outline' },
  { value: '温柔漫画', icon: 'chatbubble-ellipses-outline' },
];
const frameOptions = ['4 格', '6 格', '长图'];

export default function ComicConfigPage() {
  const addCreation = useFairyStore((state) => state.addCreation);
  const [source, setSource] = useState(sourceOptions[0].value);
  const [styleName, setStyleName] = useState(styleOptions[0].value);
  const [frameCount, setFrameCount] = useState(frameOptions[0]);
  const [title, setTitle] = useState('第一次约会的小漫画');
  const [prompt, setPrompt] = useState('把雨天约会画成温柔漫画，保留共撑一把伞的画面。');
  const [privateOnly, setPrivateOnly] = useState(true);
  const [highQuality, setHighQuality] = useState(true);
  const [toast, setToast] = useState(null);

  const handleGenerate = () => {
    if (!title.trim() || !prompt.trim()) {
      setToast({ message: '请先写下作品名称和想要的画面', tone: 'error' });
      return;
    }
    addCreation({
      type: '漫画',
      title,
      source,
      styleName: `${styleName} · ${frameCount}`,
      status: '生成中 · 正在整理故事分镜',
      icon: 'albums-outline',
      progress: 68,
    });
    router.push('/ai/progress');
  };

  return (
    <FairyPage backgroundName="creamPaper" topSpace={28} bottomSpace={64}>
      <View style={styles.content}>
        <FairyHeader showBack eyebrow="AI 童话工坊" title="把回忆画成漫画" subtitle="选择素材和画风，再告诉魔法画笔你最想保留的那一幕。" />

        <FairyCard style={styles.heroCard}>
          <FairyImage name="workshopCover" height={206} radius={24} resizeMode="cover" />
          <View style={styles.heroCopy}>
            <FairyTag tone="gold">AI 漫画</FairyTag>
            <Text style={styles.heroText}>画笔会把熟悉的回忆整理成温柔分镜，角色与色彩保持统一。</Text>
          </View>
        </FairyCard>

        <FairyCard style={styles.formCard}>
          <Text style={styles.sectionTitle}>作品信息</Text>
          <FairyInput label="作品名称" icon="albums-outline" value={title} onChangeText={setTitle} placeholder="例如：一起看海的那天" containerStyle={styles.inputGroup} />
          <FairyInput
            label="想要的画面"
            icon="sparkles-outline"
            value={prompt}
            onChangeText={setPrompt}
            multiline
            maxLength={200}
            placeholder="描述地点、动作和想保留的情绪……"
            helper={`${prompt.length}/200 · 描述越具体，故事越贴近你的想法。`}
            containerStyle={styles.inputGroup}
          />

          <Text style={styles.sectionTitle}>选择素材</Text>
          <View style={styles.optionGrid}>
            {sourceOptions.map((item) => {
              const active = source === item.value;
              return (
                <Pressable key={item.value} onPress={() => setSource(item.value)} style={({ pressed }) => [styles.sourceCard, active && styles.optionActive, pressed && styles.pressed]}>
                  <View style={[styles.optionIcon, active && styles.optionIconActive]}><Ionicons name={item.icon} size={22} color={active ? colors.primaryDeep : colors.textSoft} /></View>
                  <Text style={[styles.optionLabel, active && styles.optionLabelActive]}>{item.label}</Text>
                  <Text style={styles.optionDetail}>{item.detail}</Text>
                  {active ? <Ionicons name="checkmark-circle" size={19} color={colors.primaryDeep} style={styles.checkIcon} /> : null}
                </Pressable>
              );
            })}
          </View>

          <Text style={styles.sectionTitle}>选择风格</Text>
          <View style={styles.choiceRow}>
            {styleOptions.map((item) => {
              const active = styleName === item.value;
              return (
                <Pressable key={item.value} onPress={() => setStyleName(item.value)} style={({ pressed }) => [styles.choice, active && styles.choiceActive, pressed && styles.pressed]}>
                  <Ionicons name={item.icon} size={18} color={active ? colors.white : colors.accent} />
                  <Text style={[styles.choiceText, active && styles.choiceTextActive]}>{item.value}</Text>
                </Pressable>
              );
            })}
          </View>

          <Text style={styles.sectionTitle}>漫画格数</Text>
          <View style={styles.segmented}>
            {frameOptions.map((item) => {
              const active = frameCount === item;
              return (
                <Pressable key={item} onPress={() => setFrameCount(item)} style={({ pressed }) => [styles.segment, active && styles.segmentActive, pressed && styles.pressed]}>
                  <Text style={[styles.segmentText, active && styles.segmentTextActive]}>{item}</Text>
                </Pressable>
              );
            })}
          </View>

          <Text style={styles.sectionTitle}>隐私与画质</Text>
          <View style={styles.switchRow}>
            <View style={styles.switchCopy}>
              <Ionicons name="lock-closed-outline" size={19} color={colors.accent} />
              <View style={styles.switchTextWrap}><Text style={styles.switchTitle}>仅我们可见</Text><Text style={styles.switchText}>作品保留在双人空间</Text></View>
            </View>
            <Switch value={privateOnly} onValueChange={setPrivateOnly} trackColor={{ false: colors.border, true: colors.primary }} thumbColor={privateOnly ? colors.primaryDeep : colors.card} />
          </View>
          <View style={styles.switchRow}>
            <View style={styles.switchCopy}>
              <Ionicons name="star-outline" size={19} color={colors.gold} />
              <View style={styles.switchTextWrap}><Text style={styles.switchTitle}>高清画质</Text><Text style={styles.switchText}>细节更丰富，生成稍慢</Text></View>
            </View>
            <Switch value={highQuality} onValueChange={setHighQuality} trackColor={{ false: colors.border, true: colors.primary }} thumbColor={highQuality ? colors.primaryDeep : colors.card} />
          </View>
        </FairyCard>

        <Pressable onPress={() => router.push('/ai/character-profile')} style={({ pressed }) => [styles.characterRow, pressed && styles.pressed]}>
          <View style={styles.characterIcon}><Ionicons name="people-outline" size={21} color={colors.accent} /></View>
          <View style={styles.characterCopy}><Text style={styles.characterTitle}>默认情侣人设</Text><Text style={styles.characterText}>昵称、外形与服装氛围可继续调整</Text></View>
          <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
        </Pressable>

        <FairyButton title="生成漫画" onPress={handleGenerate} leftContent={<Ionicons name="color-wand-outline" size={21} color={colors.white} />} />
        <Text style={styles.estimate}>预计需要 1–2 分钟 · 离开页面后仍会继续</Text>
      </View>
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 760, alignSelf: 'center', paddingHorizontal: spacing.lg },
  heroCard: { padding: spacing.md, backgroundColor: colors.cardPink, marginTop: spacing.sm, marginBottom: spacing.lg },
  heroCopy: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.sm, paddingBottom: 0 },
  heroText: { flex: 1, color: colors.textSoft, fontSize: 12, lineHeight: 19 },
  formCard: { marginBottom: spacing.lg },
  sectionTitle: { color: colors.text, fontSize: 17, fontWeight: '900', marginBottom: spacing.md, marginTop: spacing.sm },
  inputGroup: { marginBottom: spacing.lg },
  optionGrid: { flexDirection: 'row', gap: spacing.sm, marginBottom: spacing.lg },
  sourceCard: { flex: 1, minWidth: 0, minHeight: 128, alignItems: 'center', padding: spacing.md, borderRadius: 20, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  optionActive: { borderColor: colors.primary, backgroundColor: colors.cardPink },
  optionIcon: { width: 42, height: 42, borderRadius: 15, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card },
  optionIconActive: { backgroundColor: '#FFE7EA' },
  optionLabel: { marginTop: spacing.sm, color: colors.text, fontSize: 14, fontWeight: '800' },
  optionLabelActive: { color: colors.primaryDeep },
  optionDetail: { marginTop: 3, color: colors.textSoft, fontSize: 10, textAlign: 'center' },
  checkIcon: { position: 'absolute', top: 7, right: 7 },
  choiceRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginBottom: spacing.lg },
  choice: { flexGrow: 1, minWidth: 110, minHeight: 46, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.xs, borderRadius: 18, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card },
  choiceActive: { borderColor: colors.primaryDeep, backgroundColor: colors.primaryDeep },
  choiceText: { color: colors.text, fontSize: 13, fontWeight: '700' },
  choiceTextActive: { color: colors.white },
  segmented: { flexDirection: 'row', padding: 3, marginBottom: spacing.lg, borderRadius: 18, backgroundColor: colors.background, borderWidth: 1, borderColor: colors.border },
  segment: { flex: 1, minHeight: 42, alignItems: 'center', justifyContent: 'center', borderRadius: 15 },
  segmentActive: { backgroundColor: colors.cardPink },
  segmentText: { color: colors.textSoft, fontSize: 13, fontWeight: '700' },
  segmentTextActive: { color: colors.primaryDeep },
  switchRow: { minHeight: 68, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', borderTopWidth: StyleSheet.hairlineWidth, borderTopColor: colors.border, gap: spacing.md },
  switchCopy: { flex: 1, flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  switchTextWrap: { flex: 1 },
  switchTitle: { color: colors.text, fontSize: 14, fontWeight: '800' },
  switchText: { marginTop: 3, color: colors.textSoft, fontSize: 11 },
  characterRow: { minHeight: 72, flexDirection: 'row', alignItems: 'center', padding: spacing.md, marginBottom: spacing.lg, borderRadius: 22, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card, gap: spacing.md },
  characterIcon: { width: 42, height: 42, borderRadius: 15, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  characterCopy: { flex: 1 },
  characterTitle: { color: colors.text, fontSize: 14, fontWeight: '800' },
  characterText: { marginTop: 4, color: colors.textSoft, fontSize: 11 },
  estimate: { marginTop: spacing.md, textAlign: 'center', color: colors.textSoft, fontSize: 11 },
  pressed: { opacity: 0.68 },
});
