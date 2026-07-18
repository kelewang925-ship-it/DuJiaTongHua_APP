import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { AppState, Image, Platform, Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { router } from 'expo-router';

import FairyBackgroundContainer from '@/components/FairyBackgroundContainer';
import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyHeader from '@/components/FairyHeader';
import FairyInput from '@/components/FairyInput';
import FairyPage from '@/components/FairyPage';
import FairyRichTextEditor from '@/components/FairyRichTextEditor';
import FairySvgIcon from '@/components/FairySvgIcon';
import FairyToast from '@/components/FairyToast';
import useFairyStore from '@/store/useFairyStore';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import { richTextToPlainText } from '@/utils/richText';
import { getApiMode } from '@/api/client';
import { hasCapability } from '@/config/capabilities';

const MAX_CONTENT_LENGTH = 2000;
const AUTO_SAVE_INTERVAL = 8000;
const moods = [
  { id: '开心', icon: 'sunny-outline' },
  { id: '想念', icon: 'heart-outline' },
  { id: '温柔', icon: 'flower-outline' },
  { id: '小确幸', icon: 'star-outline' },
];
const tags = [
  { id: '约会', icon: 'calendar-outline' },
  { id: '旅行', icon: 'briefcase-outline' },
  { id: '日常', icon: 'home-outline' },
];

export default function DiaryEditorPage() {
  const { width } = useWindowDimensions();
  const compact = width < 650;
  const draftDiary = useFairyStore((state) => state.draftDiary);
  const updateDraftDiary = useFairyStore((state) => state.updateDraftDiary);
  const addDiaryRecord = useFairyStore((state) => state.addDiaryRecord);
  const saveDiaryReal = useFairyStore((state) => state.saveDiaryReal);
  const [selectedMood, setSelectedMood] = useState(draftDiary.mood || '开心');
  const [selectedTags, setSelectedTags] = useState(() => (draftDiary.tags || []).filter((tag) => !moods.some((mood) => mood.id === tag)).slice(0, 3));
  const [attachments, setAttachments] = useState(draftDiary.attachments || []);
  const [isSaving, setIsSaving] = useState(false);
  const [toast, setToast] = useState(null);

  const editorRef = useRef(null);
  const draftContentRef = useRef(draftDiary.content || '');
  const editorDirtyRef = useRef(false);
  const committingRef = useRef(false);
  const pageScrollRef = useRef(null);
  const editorLayoutYRef = useRef(0);

  const diaryDate = useMemo(() => new Intl.DateTimeFormat('zh-CN', { month: 'long', day: 'numeric', weekday: 'short' }).format(new Date()), []);
  const mergedTags = useMemo(() => Array.from(new Set([selectedMood, ...selectedTags])), [selectedMood, selectedTags]);

  const readEditorContent = useCallback(() => {
    const content = editorRef.current?.getHTML?.();
    if (typeof content === 'string') draftContentRef.current = content;
    return draftContentRef.current;
  }, []);

  const flushDraftContent = useCallback(() => {
    if (committingRef.current || !editorDirtyRef.current) return draftContentRef.current;
    const nextContent = editorRef.current?.flush?.() ?? readEditorContent();
    draftContentRef.current = nextContent || '';
    if (useFairyStore.getState().draftDiary.content !== draftContentRef.current) updateDraftDiary({ content: draftContentRef.current });
    editorDirtyRef.current = false;
    editorRef.current?.markSaved?.();
    return draftContentRef.current;
  }, [readEditorContent, updateDraftDiary]);

  useEffect(() => {
    const subscription = AppState.addEventListener('change', (state) => { if (state !== 'active') flushDraftContent(); });
    const autoSaveTimer = setInterval(() => { if (editorDirtyRef.current && !committingRef.current) flushDraftContent(); }, AUTO_SAVE_INTERVAL);
    return () => {
      subscription.remove();
      clearInterval(autoSaveTimer);
      if (!committingRef.current) flushDraftContent();
    };
  }, [flushDraftContent]);

  const focusEditorInViewport = useCallback(() => {
    if (Platform.OS !== 'android') return;
    setTimeout(() => pageScrollRef.current?.scrollTo({ y: Math.max(0, editorLayoutYRef.current - 24), animated: true }), 180);
  }, []);

  const persistChoices = useCallback((patch = {}) => {
    updateDraftDiary({ mood: selectedMood, tags: mergedTags, attachments, ...patch });
  }, [attachments, mergedTags, selectedMood, updateDraftDiary]);

  const chooseMood = (mood) => {
    setSelectedMood(mood);
    updateDraftDiary({ mood, tags: Array.from(new Set([mood, ...selectedTags])), attachments });
  };

  const toggleTag = (tag) => {
    const nextTags = selectedTags.includes(tag) ? selectedTags.filter((item) => item !== tag) : [...selectedTags, tag];
    setSelectedTags(nextTags);
    updateDraftDiary({ tags: Array.from(new Set([selectedMood, ...nextTags])), attachments });
  };

  const pickAttachments = async () => {
    try {
      const result = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ['images'], allowsMultipleSelection: true, selectionLimit: 3, quality: 0.82, orderedSelection: true });
      if (result.canceled) return;
      const next = result.assets.slice(0, 3).map(({ uri, width: imageWidth, height: imageHeight, fileName, mimeType }) => ({ uri, width: imageWidth, height: imageHeight, fileName, mimeType }));
      setAttachments(next);
      updateDraftDiary({ attachments: next, mood: selectedMood, tags: mergedTags });
    } catch (error) {
      setToast({ tone: 'error', message: '暂时无法打开系统相册，请检查照片权限后再试。' });
    }
  };

  const showUnavailableAttachment = (capability, label) => {
    if (!hasCapability(capability)) {
      setToast({ tone: 'info', message: `Real 模式暂未开放${label}附件。` });
      return;
    }
    setToast({ tone: 'info', message: `Mock 模式保留${label}附件视觉演示，当前不会写入业务数据。` });
  };

  const handleSaveDraft = () => {
    const content = editorRef.current?.flush?.() ?? readEditorContent();
    draftContentRef.current = content || '';
    editorDirtyRef.current = false;
    editorRef.current?.markSaved?.();
    persistChoices({ content: draftContentRef.current });
    setToast({ tone: 'success', message: '草稿已经安静地收进草稿箱。' });
  };

  const handleSave = useCallback(async () => {
    const content = readEditorContent();
    const plainText = richTextToPlainText(content, { trim: false });
    if (editorRef.current?.isOverLimit?.() || Array.from(plainText).length > MAX_CONTENT_LENGTH) {
      setToast({ tone: 'error', message: `正文最多输入 ${MAX_CONTENT_LENGTH} 个字符，请删减后再保存。` });
      return;
    }
    if (!draftDiary.title.trim() && !plainText.trim()) {
      setToast({ tone: 'error', message: '先写下一点点今天的故事吧。' });
      return;
    }
    committingRef.current = true;
    editorDirtyRef.current = false;
    setIsSaving(true);
    const payload = { title: draftDiary.title, content, tags: mergedTags, mood: selectedMood, attachments };
    const result = getApiMode() === 'real' ? await saveDiaryReal(payload) : { success: true, data: addDiaryRecord(payload) };
    if (!result.success) { committingRef.current = false; setIsSaving(false); setToast({ tone: 'error', message: result.error?.message || '保存失败，请重试。' }); return; }
    draftContentRef.current = '';
    editorRef.current?.markSaved?.();
    setToast({ tone: 'success', message: '这一页已经写进你们的故事书。' });
    setTimeout(() => {
      setIsSaving(false);
      const diaryId = result.data?.id;
      router.replace(diaryId ? { pathname: '/diary/detail', params: { id: diaryId } } : '/(tabs)');
    }, 650);
  }, [addDiaryRecord, attachments, draftDiary.title, mergedTags, readEditorContent, saveDiaryReal, selectedMood]);

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="写日记" right={<Pressable accessibilityRole="button" disabled={isSaving} onPress={handleSaveDraft} style={({ pressed }) => [styles.draftButton, pressed && styles.pressed]}><Ionicons name="save-outline" size={17} color={colors.text} /><Text style={styles.draftText}>存草稿</Text></Pressable>} />}
      topSpace={18}
      bottomSpace={64}
      contentStyle={styles.pageContent}
      scrollRef={pageScrollRef}
      keyboardShouldPersistTaps="handled"
      keyboardDismissMode={Platform.OS === 'ios' ? 'interactive' : 'on-drag'}
      automaticallyAdjustKeyboardInsets={Platform.OS !== 'web'}
      showsVerticalScrollIndicator
    >
      <View style={styles.content}>
        <View style={styles.intro}><Text style={styles.introTitle}>把今天折进故事书里</Text><FairySvgIcon name="fourPointStar" size={13} /><Text style={styles.date}>{diaryDate}</Text></View>

        <View style={styles.paperWrap}>
          <Image source={require('../../assets/images/diary-editor/image1-element-tape-top-left.png')} resizeMode="contain" style={[styles.decoration, styles.tape]} />
          <Image source={require('../../assets/images/diary-editor/image1-element-bookmark-top-right.png')} resizeMode="contain" style={[styles.decoration, styles.bookmark]} />
          <Image source={require('../../assets/images/diary-editor/image1-element-flowers-top-right.png')} resizeMode="contain" style={[styles.decoration, styles.flowers]} />
          <Image source={require('../../assets/images/diary-editor/image1-element-notebook-pen-bottom-right.png')} resizeMode="contain" style={[styles.decoration, styles.notebook]} />
          <FairyBackgroundContainer source={require('../../assets/images/diary-editor/image1-cleaned.png')} style={styles.diaryPaper}>
            <View onLayout={(event) => { editorLayoutYRef.current = event.nativeEvent.layout.y; }} style={[styles.diaryPaperContent, compact && styles.diaryPaperContentCompact]}>
              <FairyInput label="标题" editable={!isSaving} value={draftDiary.title} onChangeText={(title) => updateDraftDiary({ title: title.slice(0, 30) })} placeholder="给这段回忆起个名字" maxLength={30} multiline inputWrapStyle={styles.titleWrap} inputStyle={styles.titleInput} helperInside helperStyle={styles.counter} helper={`${draftDiary.title.length}/30`} />
              <FairyRichTextEditor ref={editorRef} initialValue={draftDiary.content} height={compact ? 410 : 470} maxLength={MAX_CONTENT_LENGTH} placeholder="写下今天的小故事……" onChange={({ html }) => { draftContentRef.current = html || ''; }} onDirtyChange={(dirty) => { editorDirtyRef.current = dirty; }} onFocus={focusEditorInViewport} onBlur={flushDraftContent} />
            </View>
          </FairyBackgroundContainer>
        </View>

        <FairyCard style={styles.optionCard} padding={spacing.xl}><SectionTitle title="心情" icon="heart-outline" /><View style={styles.optionRow}>{moods.map((mood) => <Choice key={mood.id} label={mood.id} icon={mood.icon} active={selectedMood === mood.id} onPress={() => chooseMood(mood.id)} />)}</View></FairyCard>
        <FairyCard style={styles.optionCard} padding={spacing.xl}><SectionTitle title="日记标签" icon="star-outline" /><View style={styles.optionRow}>{tags.map((tag) => <Choice key={tag.id} label={tag.id} icon={tag.icon} active={selectedTags.includes(tag.id)} onPress={() => toggleTag(tag.id)} />)}</View></FairyCard>
        <FairyCard style={styles.optionCard} padding={spacing.xl}>
          <SectionTitle title="添加附件" icon="attach-outline" />
          <View style={styles.attachmentRow}>
            <Pressable accessibilityRole="button" disabled={isSaving} onPress={pickAttachments} style={({ pressed }) => [styles.attachmentButton, pressed && styles.pressed]}><Ionicons name="images-outline" size={25} color={colors.primaryDeep} /><Text style={styles.attachmentText}>{attachments.length ? `已选 ${attachments.length} 张` : '图片'}</Text></Pressable>
            <Pressable accessibilityRole="button" disabled={isSaving} onPress={() => showUnavailableAttachment('voiceAttachment', '语音')} style={({ pressed }) => [styles.attachmentButtonUnavailable, pressed && styles.pressed]}><Ionicons name="mic-outline" size={25} color={colors.textSoft} /><Text style={styles.attachmentTextMuted}>语音·未开放</Text></Pressable>
            <Pressable accessibilityRole="button" disabled={isSaving} onPress={() => showUnavailableAttachment('locationAttachment', '位置')} style={({ pressed }) => [styles.attachmentButtonUnavailable, pressed && styles.pressed]}><Ionicons name="location-outline" size={25} color={colors.textSoft} /><Text style={styles.attachmentTextMuted}>位置·未开放</Text></Pressable>
          </View>
          {attachments.length ? <View style={styles.previewRow}>{attachments.map((item, index) => <View key={item.uri} style={styles.previewWrap}><Image source={{ uri: item.uri }} resizeMode="cover" style={styles.preview} /><Pressable accessibilityLabel={`移除第${index + 1}张附件`} disabled={isSaving} onPress={() => { const next = attachments.filter((_, itemIndex) => itemIndex !== index); setAttachments(next); updateDraftDiary({ attachments: next }); }} style={styles.removeAttachment}><Ionicons name="close" size={14} color={colors.white} /></Pressable></View>)}</View> : null}
        </FairyCard>

        <FairyButton title={isSaving ? '正在保存……' : '保存日记'} disabled={isSaving} onPress={handleSave} leftContent={<Ionicons name="star-outline" size={20} color={colors.white} />} />
        <View style={styles.privacy}><Ionicons name="lock-closed" size={14} color={colors.gold} /><Text style={styles.privacyText}>仅你们可见，记录安心又私密</Text></View>
      </View>
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function SectionTitle({ title, icon }) {
  return <View style={styles.sectionTitleRow}><Text style={styles.sectionTitle}>{title}</Text><Ionicons name={icon} size={20} color={colors.primaryDeep} /></View>;
}

function Choice({ label, icon, active, onPress }) {
  return <Pressable accessibilityRole="checkbox" accessibilityState={{ checked: active }} onPress={onPress} style={({ pressed }) => [styles.choice, active && styles.choiceActive, pressed && styles.pressed]}><Ionicons name={icon} size={21} color={active ? colors.primaryDeep : colors.accent} /><Text style={[styles.choiceText, active && styles.choiceTextActive]}>{label}</Text>{active ? <Ionicons name="checkmark-circle" size={16} color={colors.primaryDeep} /> : null}</Pressable>;
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 900 }, pressed: { opacity: 0.65 },
  draftButton: { minWidth: 64, minHeight: 44, flexDirection: 'row', alignItems: 'center', justifyContent: 'flex-end', gap: 4 }, draftText: { color: colors.text, fontSize: 12, fontWeight: '900' },
  intro: { flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'center', gap: 6, marginBottom: spacing.lg }, introTitle: { color: colors.text, fontSize: 17, fontWeight: '900' }, date: { width: '100%', color: colors.textSoft, fontSize: 11, textAlign: 'center' },
  paperWrap: { position: 'relative', width: '100%', marginBottom: spacing.xl }, decoration: { position: 'absolute', zIndex: 2 }, tape: { left: '3%', top: -26, width: 150, height: 80, transform: [{ rotate: '-7deg' }] }, bookmark: { right: '7%', top: -8, width: 62, height: 90 }, flowers: { right: -8, top: -32, width: 74, height: 94, zIndex: 0 }, notebook: { right: -12, bottom: -18, width: 180, height: 150 }, diaryPaper: { width: '100%', minHeight: 670 }, diaryPaperContent: { width: '84%', marginLeft: '7%', minHeight: 620, paddingTop: 66, paddingBottom: 72 }, diaryPaperContentCompact: { width: '88%', marginLeft: '6%', paddingTop: 58 },
  titleWrap: { minHeight: 88, alignItems: 'flex-start', paddingTop: 14, paddingBottom: 24, backgroundColor: 'rgba(255,250,244,0.88)' }, titleInput: { minHeight: 34, lineHeight: 20, paddingTop: 0 }, counter: { color: colors.textSoft },
  optionCard: { backgroundColor: 'rgba(255,249,244,0.96)', marginBottom: spacing.lg }, sectionTitleRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginBottom: spacing.lg }, sectionTitle: { color: colors.text, fontSize: 18, fontWeight: '900' }, optionRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md }, choice: { minWidth: 135, flexGrow: 1, minHeight: 50, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, paddingHorizontal: spacing.lg, borderRadius: 20, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border }, choiceActive: { backgroundColor: colors.cardPink, borderColor: colors.primaryDeep }, choiceText: { color: colors.text, fontWeight: '800' }, choiceTextActive: { color: colors.primaryDeep },
  attachmentRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md }, attachmentButton: { minWidth: 170, flexGrow: 1, minHeight: 76, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.md, borderRadius: 20, borderWidth: 1, borderStyle: 'dashed', borderColor: colors.primaryDeep, backgroundColor: colors.cardPink }, attachmentButtonUnavailable: { minWidth: 170, flexGrow: 1, minHeight: 76, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.md, borderRadius: 20, borderWidth: 1, borderStyle: 'dashed', borderColor: colors.border, backgroundColor: colors.background }, attachmentText: { color: colors.primaryDeep, fontWeight: '900' }, attachmentTextMuted: { color: colors.textSoft, fontSize: 12, fontWeight: '800' }, previewRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginTop: spacing.lg }, previewWrap: { position: 'relative', width: 92, height: 92 }, preview: { width: '100%', height: '100%', borderRadius: 16, backgroundColor: colors.cardPink }, removeAttachment: { position: 'absolute', top: -5, right: -5, width: 24, height: 24, borderRadius: 12, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.accent },
  privacy: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, marginTop: spacing.lg }, privacyText: { color: colors.textSoft, fontSize: 11 },
});
