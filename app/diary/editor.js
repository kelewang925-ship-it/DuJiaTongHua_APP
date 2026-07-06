import { useMemo, useState } from 'react';
import { Alert, ScrollView, View, Text, StyleSheet, Pressable, Image } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';
import FairyInput from '../../src/components/FairyInput';
import FairyBackButton from '../../src/components/FairyBackButton';
import useFairyStore from '../../src/store/useFairyStore';

import FairyPage from '../../src/components/FairyPage';
import FairyHeader from '../../src/components/FairyHeader';
import FairyBackgroundContainer from '../../src/components/FairyBackgroundContainer';
import FairySvgIcon from '../../src/components/FairySvgIcon';
import FairyRichTextEditor from '../../src/components/FairyRichTextEditor';

const moodOptions = ['开心', '想念', '日常', '约会', '旅行'];

export default function DiaryEditorPage() {
  const draftDiary = useFairyStore((state) => state.draftDiary);
  const updateDraftDiary = useFairyStore((state) => state.updateDraftDiary);
  const addDiaryRecord = useFairyStore((state) => state.addDiaryRecord);
  const [selectedMood, setSelectedMood] = useState(draftDiary.mood || '开心');
  const [tagText, setTagText] = useState((draftDiary.tags || []).join('、'));
  const [isSaving, setIsSaving] = useState(false);
  const [savedTitle, setSavedTitle] = useState('');

  const canSave = useMemo(
    () => draftDiary.title.trim().length > 0 || draftDiary.content.trim().length > 0,
    [draftDiary.content, draftDiary.title]
  );

  const parsedTags = useMemo(
    () =>
      tagText
        .split(/[、,，\s]+/)
        .map((tag) => tag.trim())
        .filter(Boolean)
        .slice(0, 5),
    [tagText]
  );

  const handleSave = () => {
    if (!canSave) {
      Alert.alert('还没有内容', '先写下一点点今天的故事吧。');
      return;
    }

    setIsSaving(true);
    const record = addDiaryRecord({
      title: draftDiary.title,
      content: draftDiary.content,
      tags: parsedTags.length ? parsedTags : [selectedMood, '日常'],
      mood: selectedMood,
    });

    setSavedTitle(record.title);
    setTimeout(() => {
      setIsSaving(false);
      router.replace('/diary/detail');
    }, 550);
  };

  return (
    <FairyPage
      topSpace={0}
      header={
        <FairyHeader
          showBack
          title={<View><Text style={styles.title}>写日记</Text></View>}
          right="存草稿"
        />
      }
    >
      <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 4 }}>
        <Text style={{ fontSize: 12 }} >把今天写进故事书里</Text>
        <FairySvgIcon name="fourPointStar" size={12} />
      </View>
      {/* <FairyBackgroundContainer
        source={require('../../assets/images/diary-editor/image1.png')}
        style={{ width: '100%', aspectRatio: 993 / 1453 }}
      >
        <View style={{ width: '75%', height: '80%', backgroundColor: '#fff' }}>
          <Text>111</Text>
        </View>
      </FairyBackgroundContainer> */}
      <View style={{ position: 'relative', width: '100%', marginTop: 20 }}>

        <Image
          source={require('../../assets/images/diary-editor/image1-element-tape-top-left.png')}
          resizeMode="contain"
          style={[
            styles.profileDecoration,
            {
              left: '5%',
              top: '-5%',
              width: '20%',
              height: '10%'
            },
          ]}
        />
        <Image
          source={require('../../assets/images/diary-editor/image1-element-bookmark-top-right.png')}
          resizeMode="contain"
          style={[
            styles.profileDecoration,
            {
              right: '8%',
              width: '8%',
              height: '8%'
            },
          ]}
        />
        <Image
          source={require('../../assets/images/diary-editor/image1-element-flowers-top-right.png')}
          resizeMode="contain"
          style={[
            styles.profileDecoration,
            {
              zIndex: -1,
              right: '-1%',
              top: '-5%',
              width: '8%',
              height: '8%'
            },
          ]}
        />
        <Image
          source={require('../../assets/images/diary-editor/image1-element-notebook-pen-bottom-right.png')}
          resizeMode="contain"
          style={[
            styles.profileDecoration,
            {
              right: '-2%',
              bottom: '-2%',
              width: '20%',
              height: '14%'
            },
          ]}
        />
        <FairyBackgroundContainer
          source={require('../../assets/images/diary-editor/image1-cleaned.png')}
          style={{ width: '100%', aspectRatio: 993 / 1453 }}
        >
          <View style={{ marginLeft: '5%', width: '80%', height: '85%' }}>
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
              height={420}
              maxLength={2000}
              placeholder="写下今天的小故事..."
              value={draftDiary.content}
              onChange={({ html }) => {
                updateDraftDiary({ content: html });
              }}
            />
          </View>
        </FairyBackgroundContainer>
      </View>

    </FairyPage>
    // <ScrollView style={styles.page} contentContainerStyle={styles.content}>
    //   <FairyBackButton />
    //   <Text style={styles.title}>写一页童话</Text>
    //   <Text style={styles.subtitle}>把今天的小事，悄悄收藏进你们的故事里。</Text>

    //   <FairyCard style={styles.card}>
    //     <FairyInput
    //       label="今天的标题"
    //       icon="bookmark-outline"
    //       value={draftDiary.title}
    //       onChangeText={(title) => updateDraftDiary({ title })}
    //       placeholder="例如：一起散步的傍晚"
    //       helper="标题可以留空，保存时会自动生成一个温柔的小标题。"
    //       containerStyle={styles.inputGroup}
    //     />
    //     <Text style={styles.label}>心情标签</Text>
    //     <View style={styles.tags}>
    //       {moodOptions.map((item) => (
    //         <Pressable
    //           key={item}
    //           onPress={() => {
    //             setSelectedMood(item);
    //             updateDraftDiary({ mood: item });
    //           }}
    //         >
    //           <FairyTag tone={selectedMood === item ? 'gold' : 'default'}>{item}</FairyTag>
    //         </Pressable>
    //       ))}
    //     </View>
    //     <FairyInput
    //       label="故事标签"
    //       icon="pricetag-outline"
    //       value={tagText}
    //       onChangeText={(text) => {
    //         setTagText(text);
    //         updateDraftDiary({
    //           tags: text
    //             .split(/[、,，\s]+/)
    //             .map((tag) => tag.trim())
    //             .filter(Boolean)
    //             .slice(0, 5),
    //         });
    //       }}
    //       placeholder="日常、约会、散步"
    //       helper="用顿号、逗号或空格分隔，最多保留 5 个标签。"
    //       containerStyle={styles.tagInput}
    //     />
    //   </FairyCard>

    //   <FairyCard style={styles.editorCard}>
    //     <FairyInput
    //       label="正文"
    //       icon="create-outline"
    //       value={draftDiary.content}
    //       onChangeText={(content) => updateDraftDiary({ content })}
    //       multiline
    //       placeholder="今天发生了什么值得被记住的小事？"
    //       helper="正文和标题至少填写一项，就可以保存。"
    //       containerStyle={styles.inputGroup}
    //       inputStyle={styles.bodyInput}
    //     />
    //   </FairyCard>

    //   <FairyCard style={styles.photoCard}>
    //     <Ionicons name="image-outline" size={24} color={colors.accent} />
    //     <View style={{ flex: 1 }}>
    //       <Text style={styles.photoTitle}>添加照片</Text>
    //       <Text style={styles.photoText}>让这一页更像一本真的绘本。</Text>
    //     </View>
    //   </FairyCard>

    //   {savedTitle ? (
    //     <FairyCard style={styles.successCard}>
    //       <Ionicons name="checkmark-circle-outline" size={22} color={colors.accent} />
    //       <View style={styles.successTextWrap}>
    //         <Text style={styles.successTitle}>保存成功</Text>
    //         <Text style={styles.successText}>《{savedTitle}》已经放进你们的童话里。</Text>
    //       </View>
    //     </FairyCard>
    //   ) : null}

    //   <FairyButton
    //     title={isSaving ? '正在保存...' : '保存这一页'}
    //     onPress={handleSave}
    //     disabled={!canSave || isSaving}
    //   />
    // </ScrollView>
  );
}

const styles = StyleSheet.create({
  title: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '900',
    lineHeight: 24,
    textAlign: 'center',
  },
  profileDecoration: {
    position: 'absolute',
    zIndex: 1,
  },
  relationNoteWrap: {
    minHeight: 30,
    alignItems: 'flex-start',
    paddingTop: 10,
    paddingBottom: 20,
    backgroundColor: '#fff'
  },
  relationNoteInput: {
    minHeight: 30,
    lineHeight: 16,
    paddingTop: 0,
  },
  relationNoteCounter: {
    color: colors.textSoft,
  },
  diaryRichTextEditor: {
    marginTop: 10,
    height: '72%',
  },
  // page: { flex: 1, backgroundColor: colors.background },
  // content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  // title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  // subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  // card: { marginBottom: 16 },
  // inputGroup: { marginBottom: 0 },
  // label: { color: colors.text, fontSize: 15, fontWeight: '800', marginTop: 8 },
  // tags: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 12 },
  // tagInput: { marginTop: 18, marginBottom: 0 },
  // editorCard: { marginBottom: 16 },
  // bodyInput: { minHeight: 190 },
  // photoCard: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 22, backgroundColor: colors.cardPink },
  // photoTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  // photoText: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  // successCard: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 16, backgroundColor: '#FFF5DF' },
  // successTextWrap: { flex: 1 },
  // successTitle: { color: colors.text, fontSize: 15, fontWeight: '900' },
  // successText: { color: colors.textSoft, fontSize: 12, marginTop: 3, lineHeight: 18 },
});
