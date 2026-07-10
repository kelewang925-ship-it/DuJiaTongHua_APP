import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Alert, AppState, Image, Platform, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import colors from '../../src/theme/colors';
import FairyInput from '../../src/components/FairyInput';
import useFairyStore from '../../src/store/useFairyStore';
import FairyPage from '../../src/components/FairyPage';
import FairyHeader from '../../src/components/FairyHeader';
import FairyBackgroundContainer from '../../src/components/FairyBackgroundContainer';
import FairySvgIcon from '../../src/components/FairySvgIcon';
import FairyRichTextEditor from '../../src/components/FairyRichTextEditor';
import { richTextToPlainText } from '../../src/utils/richText';

const MAX_CONTENT_LENGTH = 2000;
const AUTO_SAVE_INTERVAL = 8000;

export default function DiaryEditorPage() {
  const draftDiary = useFairyStore((state) => state.draftDiary);
  const updateDraftDiary = useFairyStore((state) => state.updateDraftDiary);
  const addDiaryRecord = useFairyStore((state) => state.addDiaryRecord);
  const [selectedMood] = useState(draftDiary.mood || '开心');
  const [tagText] = useState((draftDiary.tags || []).join('、'));
  const [isSaving, setIsSaving] = useState(false);

  const editorRef = useRef(null);
  const draftContentRef = useRef(draftDiary.content || '');
  const editorDirtyRef = useRef(false);
  const committingRef = useRef(false);
  const pageScrollRef = useRef(null);
  const editorLayoutYRef = useRef(0);

  const readEditorContent = useCallback(() => {
    const content = editorRef.current?.getHTML?.();
    if (typeof content === 'string') {
      draftContentRef.current = content;
    }
    return draftContentRef.current;
  }, []);

  const flushDraftContent = useCallback(() => {
    if (committingRef.current || !editorDirtyRef.current) {
      return draftContentRef.current;
    }

    const nextContent = editorRef.current?.flush?.() ?? readEditorContent();
    draftContentRef.current = nextContent || '';

    if (useFairyStore.getState().draftDiary.content !== draftContentRef.current) {
      updateDraftDiary({ content: draftContentRef.current });
    }

    editorDirtyRef.current = false;
    editorRef.current?.markSaved?.();
    return draftContentRef.current;
  }, [readEditorContent, updateDraftDiary]);

  useEffect(() => {
    const subscription = AppState.addEventListener('change', (state) => {
      if (state !== 'active') flushDraftContent();
    });

    const autoSaveTimer = setInterval(() => {
      if (editorDirtyRef.current && !committingRef.current) {
        flushDraftContent();
      }
    }, AUTO_SAVE_INTERVAL);

    return () => {
      subscription.remove();
      clearInterval(autoSaveTimer);
      if (!committingRef.current) flushDraftContent();
    };
  }, [flushDraftContent]);

  const focusEditorInViewport = useCallback(() => {
    // iOS 已由 automaticallyAdjustKeyboardInsets 处理，避免双重滚动导致页面跳动。
    if (Platform.OS !== 'android') return;

    setTimeout(() => {
      pageScrollRef.current?.scrollTo({
        y: Math.max(0, editorLayoutYRef.current - 24),
        animated: true,
      });
    }, 180);
  }, []);

  const parsedTags = useMemo(
    () =>
      tagText
        .split(/[、,，\s]+/)
        .map((tag) => tag.trim())
        .filter(Boolean)
        .slice(0, 5),
    [tagText]
  );

  const handleEditorChange = useCallback(({ html }) => {
    draftContentRef.current = html || '';
  }, []);

  const handleEditorDirtyChange = useCallback((dirty) => {
    editorDirtyRef.current = dirty;
  }, []);

  const handleEditorBlur = useCallback(() => {
    flushDraftContent();
  }, [flushDraftContent]);

  const handleSave = useCallback(() => {
    const content = readEditorContent();
    const plainText = richTextToPlainText(content, { trim: false });

    if (editorRef.current?.isOverLimit?.() || Array.from(plainText).length > MAX_CONTENT_LENGTH) {
      Alert.alert('内容过长', `正文最多输入 ${MAX_CONTENT_LENGTH} 个字符，请删减后再保存。`);
      return;
    }

    if (!draftDiary.title.trim() && !plainText.trim()) {
      Alert.alert('还没有内容', '先写下一点点今天的故事吧。');
      return;
    }

    committingRef.current = true;
    editorDirtyRef.current = false;
    setIsSaving(true);

    addDiaryRecord({
      title: draftDiary.title,
      content,
      tags: parsedTags.length ? parsedTags : [selectedMood, '日常'],
      mood: selectedMood,
    });

    draftContentRef.current = '';
    editorRef.current?.markSaved?.();

    setTimeout(() => {
      setIsSaving(false);
      router.replace('/diary/detail');
    }, 550);
  }, [addDiaryRecord, draftDiary.title, parsedTags, readEditorContent, selectedMood]);

  return (
    <FairyPage
      topSpace={0}
      scrollRef={pageScrollRef}
      keyboardShouldPersistTaps="handled"
      keyboardDismissMode={Platform.OS === 'ios' ? 'interactive' : 'on-drag'}
      automaticallyAdjustKeyboardInsets={Platform.OS !== 'web'}
      header={
        <FairyHeader
          showBack
          title={
            <View>
              <Text style={styles.headerTitle}>写日记</Text>
            </View>
          }
          right={isSaving ? '保存中...' : '存草稿'}
        />
      }
    >
      <View style={styles.subtitleRow}>
        <Text style={styles.subtitle}>把今天写进故事书里</Text>
        <FairySvgIcon name="fourPointStar" size={12} />
      </View>

      <View style={styles.paperWrap}>
        <Image
          source={require('../../assets/images/diary-editor/image1-element-tape-top-left.png')}
          resizeMode="contain"
          style={[styles.profileDecoration, styles.tapeDecoration]}
        />
        <Image
          source={require('../../assets/images/diary-editor/image1-element-bookmark-top-right.png')}
          resizeMode="contain"
          style={[styles.profileDecoration, styles.bookmarkDecoration]}
        />
        <Image
          source={require('../../assets/images/diary-editor/image1-element-flowers-top-right.png')}
          resizeMode="contain"
          style={[styles.profileDecoration, styles.flowerDecoration]}
        />
        <Image
          source={require('../../assets/images/diary-editor/image1-element-notebook-pen-bottom-right.png')}
          resizeMode="contain"
          style={[styles.profileDecoration, styles.notebookDecoration]}
        />

        <FairyBackgroundContainer
          source={require('../../assets/images/diary-editor/image1-cleaned.png')}
          style={styles.diaryPaper}
        >
          <View
            onLayout={(event) => {
              editorLayoutYRef.current = event.nativeEvent.layout.y;
            }}
            style={styles.diaryPaperContent}
          >
            <FairyInput
              label="标题"
              value={draftDiary.title}
              onChangeText={(title) => updateDraftDiary({ title: title.slice(0, 30) })}
              placeholder="给这段回忆起个名字"
              maxLength={30}
              multiline
              inputWrapStyle={styles.relationNoteWrap}
              inputStyle={styles.relationNoteInput}
              helperInside
              helperStyle={styles.relationNoteCounter}
              helper={`${draftDiary.title.length}/30`}
            />

            <FairyRichTextEditor
              ref={editorRef}
              initialValue={draftDiary.content}
              height={Platform.OS === 'web' ? 420 : 420}
              maxLength={MAX_CONTENT_LENGTH}
              placeholder="写下今天的小故事..."
              onChange={handleEditorChange}
              onDirtyChange={handleEditorDirtyChange}
              onFocus={focusEditorInViewport}
              onBlur={handleEditorBlur}
            />
          </View>
        </FairyBackgroundContainer>
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  headerTitle: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '900',
    lineHeight: 24,
    textAlign: 'center',
  },
  subtitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
  },
  subtitle: {
    fontSize: 12,
  },
  paperWrap: {
    position: 'relative',
    width: '100%',
    marginTop: 20,
  },
  profileDecoration: {
    position: 'absolute',
    zIndex: 1,
  },
  tapeDecoration: {
    left: '5%',
    top: '-5%',
    width: '20%',
    height: '10%',
  },
  bookmarkDecoration: {
    right: '8%',
    width: '8%',
    height: '8%',
  },
  flowerDecoration: {
    zIndex: -1,
    right: '-1%',
    top: '-5%',
    width: '8%',
    height: '8%',
  },
  notebookDecoration: {
    right: '-2%',
    bottom: '-2%',
    width: '20%',
    height: '14%',
  },
  relationNoteWrap: {
    minHeight: 30,
    alignItems: 'flex-start',
    paddingTop: 10,
    paddingBottom: 20,
    backgroundColor: '#fff',
  },
  relationNoteInput: {
    minHeight: 30,
    lineHeight: 16,
    paddingTop: 0,
  },
  relationNoteCounter: {
    color: colors.textSoft,
  },
  diaryPaper: {
    width: '100%',
    minHeight: 680,
  },
  diaryPaperContent: {
    width: '80%',
    marginLeft: '5%',
    minHeight: 620,
    paddingVertical: 42,
  },
});
