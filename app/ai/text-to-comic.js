import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
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

const styleOptions = [
  { value: '童话绘本', icon: 'color-palette-outline' },
  { value: '轻柔水彩', icon: 'water-outline' },
  { value: '手帐贴纸', icon: 'bookmarks-outline' },
];
const frameOptions = ['四格', '六格', '连续页'];
const fallbackStory = '晚霞落下来时，我们沿着河边慢慢散步。风很轻，你把我的手握得更紧了一点。';

function toPlainStory(value) {
  if (!value) return '';
  return String(value)
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>\s*<p[^>]*>/gi, '\n\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'")
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

export default function TextToComicPage() {
  const addCreation = useFairyStore((state) => state.addCreation);
  const records = useFairyStore((state) => state.records);
  const latestDiary = records.find((item) => item.type === '日记');
  const diaryText = (toPlainStory(latestDiary?.content) || fallbackStory).slice(0, 800);
  const [sourceMode, setSourceMode] = useState(latestDiary ? 'diary' : 'free');
  const [storyText, setStoryText] = useState(diaryText);
  const [styleName, setStyleName] = useState(styleOptions[0].value);
  const [frameCount, setFrameCount] = useState(frameOptions[0]);
  const [toast, setToast] = useState(null);
  const canGenerate = hasCapability('aiGeneration');

  const chooseSource = (mode) => {
    setSourceMode(mode);
    if (mode === 'diary') setStoryText(diaryText);
    if (mode === 'free' && storyText === diaryText) setStoryText('');
  };

  const handleGenerate = () => {
    if (!canGenerate) {
      setToast({ message: 'Real 模式暂未开放 AI 生成，不会创建本地模拟任务。', tone: 'info' });
      return;
    }
    if (!storyText.trim()) {
      setToast({ message: '先写下一段想变成漫画的故事吧', tone: 'error' });
      return;
    }
    const creation = addCreation({
      type: '漫画',
      title: sourceMode === 'diary' && latestDiary ? `${latestDiary.title} · 漫画版` : '文字长出的童话漫画',
      source: sourceMode === 'diary' ? '最近日记' : '自由文本',
      styleName: `${styleName} · ${frameCount}`,
      status: '生成中 · 正在拆分文字分镜',
      icon: 'document-text-outline',
      progress: 58,
    });
    if (!creation) {
      setToast({ message: '当前模式无法创建本地模拟任务。', tone: 'error' });
      return;
    }
    router.push('/ai/progress');
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      topSpace={28}
      bottomSpace={64}
      header={<FairyHeader showBack eyebrow="AI 童话工坊" title="让文字长出画面" subtitle="从日记里挑一段，或者亲手写下想变成漫画的故事。" />}
    >
      <View style={styles.content}>
        <FairyCard style={styles.sourceCard}>
          <Text style={styles.sectionTitle}>来源选择</Text>
          <View style={styles.sourceTabs}>
            <SourceTab active={sourceMode === 'diary'} icon="book-outline" label="来自日记" onPress={() => chooseSource('diary')} />
            <SourceTab active={sourceMode === 'free'} icon="create-outline" label="自由输入" onPress={() => chooseSource('free')} />
          </View>
          {sourceMode === 'diary' ? (
            <View style={styles.diaryPreview}>
              <View style={styles.diaryIcon}><Ionicons name="book" size={22} color={colors.primaryDeep} /></View>
              <View style={styles.diaryCopy}>
                <Text style={styles.diaryLabel}>已选择最近日记</Text>
                <Text style={styles.diaryTitle}>{latestDiary?.title || '晚霞散步'}</Text>
                <Text style={styles.diaryDate}>{latestDiary?.date || '一段温柔的日常回忆'}</Text>
              </View>
              <Ionicons name="checkmark-circle" size={21} color={colors.primaryDeep} />
            </View>
          ) : null}
        </FairyCard>

        <FairyCard style={styles.editorCard}>
          <FairyInput
            label="故事文本"
            icon="document-text-outline"
            value={storyText}
            onChangeText={setStoryText}
            multiline
            maxLength={800}
            placeholder="写下地点、动作、情绪和一句想保留的话……"
            helper={`${storyText.length}/800 · 越具体的场景越容易形成连贯分镜。`}
            containerStyle={styles.inputGroup}
          />

          <Text style={styles.sectionTitle}>画面风格</Text>
          <View style={styles.optionRow}>
            {styleOptions.map((item) => {
              const active = styleName === item.value;
              return (
                <Pressable key={item.value} onPress={() => setStyleName(item.value)} style={({ pressed }) => [styles.styleChoice, active && styles.choiceActive, pressed && styles.pressed]}>
                  <Ionicons name={item.icon} size={19} color={active ? colors.primaryDeep : colors.textSoft} />
                  <Text style={[styles.choiceText, active && styles.choiceTextActive]}>{item.value}</Text>
                </Pressable>
              );
            })}
          </View>

          <Text style={styles.sectionTitle}>分镜数量</Text>
          <View style={styles.optionRow}>
            {frameOptions.map((item) => {
              const active = frameCount === item;
              return (
                <Pressable key={item} onPress={() => setFrameCount(item)} style={({ pressed }) => [styles.frameChoice, active && styles.choiceActive, pressed && styles.pressed]}>
                  <Text style={[styles.choiceText, active && styles.choiceTextActive]}>{item}</Text>
                </Pressable>
              );
            })}
          </View>
        </FairyCard>

        <FairyCard style={styles.previewCard}>
          <FairyImage name="aiComicTriptych" height={132} radius={20} resizeMode="cover" />
          <View style={styles.previewCopy}>
            <View style={styles.previewHeading}><Ionicons name="color-wand-outline" size={19} color={colors.gold} /><Text style={styles.previewTitle}>生成后还可以继续编辑</Text></View>
            <Text style={styles.previewText}>支持调整顺序、修改标题与重新生成画面。</Text>
          </View>
          <FairyTag tone="gold">{styleName} · {frameCount}</FairyTag>
        </FairyCard>

        <FairyButton title={canGenerate ? '开始生成' : 'AI 生成未开放'} onPress={handleGenerate} leftContent={<Ionicons name="sparkles" size={20} color={colors.white} />} />
        <Text style={styles.estimate}>{canGenerate ? '预计 1–2 分钟 · 作品会自动保存在创作历史' : 'Real 模式不会创建本地模拟作品'}</Text>
      </View>
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function SourceTab({ active, icon, label, onPress }) {
  return (
    <Pressable onPress={onPress} style={({ pressed }) => [styles.sourceTab, active && styles.sourceTabActive, pressed && styles.pressed]}>
      <Ionicons name={icon} size={21} color={active ? colors.primaryDeep : colors.textSoft} />
      <Text style={[styles.sourceTabText, active && styles.sourceTabTextActive]}>{label}</Text>
      {active ? <Ionicons name="checkmark-circle" size={18} color={colors.primaryDeep} /> : null}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 760, alignSelf: 'center', paddingHorizontal: spacing.lg },
  sourceCard: { marginTop: spacing.sm, marginBottom: spacing.lg },
  sectionTitle: { color: colors.text, fontSize: 17, fontWeight: '900', marginBottom: spacing.md },
  sourceTabs: { flexDirection: 'row', gap: spacing.sm },
  sourceTab: { flex: 1, minHeight: 54, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingHorizontal: spacing.sm, borderRadius: 18, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background, gap: spacing.xs },
  sourceTabActive: { borderColor: colors.primary, backgroundColor: colors.cardPink },
  sourceTabText: { color: colors.textSoft, fontSize: 13, fontWeight: '700' },
  sourceTabTextActive: { color: colors.text },
  diaryPreview: { minHeight: 82, flexDirection: 'row', alignItems: 'center', padding: spacing.md, marginTop: spacing.md, borderRadius: 20, backgroundColor: colors.background, gap: spacing.md },
  diaryIcon: { width: 46, height: 46, borderRadius: 16, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  diaryCopy: { flex: 1, minWidth: 0 },
  diaryLabel: { color: colors.textSoft, fontSize: 10, fontWeight: '700' },
  diaryTitle: { marginTop: 3, color: colors.text, fontSize: 15, fontWeight: '900' },
  diaryDate: { marginTop: 3, color: colors.textSoft, fontSize: 11 },
  editorCard: { marginBottom: spacing.lg },
  inputGroup: { marginBottom: spacing.xl },
  optionRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginBottom: spacing.xl },
  styleChoice: { flexGrow: 1, minWidth: 110, minHeight: 48, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingHorizontal: spacing.sm, borderRadius: 18, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background, gap: spacing.xs },
  frameChoice: { flex: 1, minWidth: 82, minHeight: 46, alignItems: 'center', justifyContent: 'center', borderRadius: 17, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  choiceActive: { borderColor: colors.primary, backgroundColor: colors.cardPink },
  choiceText: { color: colors.textSoft, fontSize: 13, fontWeight: '700' },
  choiceTextActive: { color: colors.primaryDeep },
  previewCard: { marginBottom: spacing.xl, backgroundColor: colors.cardPink },
  previewCopy: { marginVertical: spacing.md },
  previewHeading: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  previewTitle: { color: colors.text, fontSize: 15, fontWeight: '900' },
  previewText: { marginTop: 5, color: colors.textSoft, fontSize: 12, lineHeight: 19 },
  estimate: { marginTop: spacing.md, textAlign: 'center', color: colors.textSoft, fontSize: 11 },
  pressed: { opacity: 0.68 },
});
