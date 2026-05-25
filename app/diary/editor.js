import { useMemo, useState } from 'react';
import { Alert, ScrollView, View, Text, TextInput, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';
import FairyBackButton from '../../src/components/FairyBackButton';
import useFairyStore from '../../src/store/useFairyStore';

const moodOptions = ['开心', '想念', '日常', '约会', '旅行'];

export default function DiaryEditorPage() {
  const draftDiary = useFairyStore((state) => state.draftDiary);
  const updateDraftDiary = useFairyStore((state) => state.updateDraftDiary);
  const addDiaryRecord = useFairyStore((state) => state.addDiaryRecord);
  const [selectedMood, setSelectedMood] = useState(draftDiary.mood || '开心');

  const canSave = useMemo(
    () => draftDiary.title.trim().length > 0 || draftDiary.content.trim().length > 0,
    [draftDiary.content, draftDiary.title]
  );

  const handleSave = () => {
    if (!canSave) {
      Alert.alert('还没有内容', '先写下一点点今天的故事吧。');
      return;
    }

    addDiaryRecord({
      title: draftDiary.title,
      content: draftDiary.content,
      tags: draftDiary.tags,
      mood: selectedMood,
    });

    router.replace('/(tabs)');
  };

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>写一页童话</Text>
      <Text style={styles.subtitle}>把今天的小事，悄悄收藏进你们的故事里。</Text>

      <FairyCard style={styles.card}>
        <Text style={styles.label}>今天的标题</Text>
        <TextInput
          style={styles.titleInput}
          value={draftDiary.title}
          onChangeText={(title) => updateDraftDiary({ title })}
          placeholder="例如：一起散步的傍晚"
          placeholderTextColor={colors.textSoft}
        />
        <Text style={styles.label}>心情标签</Text>
        <View style={styles.tags}>
          {moodOptions.map((item) => (
            <Pressable key={item} onPress={() => setSelectedMood(item)}>
              <FairyTag tone={selectedMood === item ? 'gold' : 'default'}>{item}</FairyTag>
            </Pressable>
          ))}
        </View>
      </FairyCard>

      <FairyCard style={styles.editorCard}>
        <View style={styles.editorHeader}>
          <Ionicons name="create-outline" size={20} color={colors.accent} />
          <Text style={styles.label}>正文</Text>
        </View>
        <TextInput
          style={styles.bodyInput}
          value={draftDiary.content}
          onChangeText={(content) => updateDraftDiary({ content })}
          multiline
          textAlignVertical="top"
          placeholder="今天发生了什么值得被记住的小事？"
          placeholderTextColor={colors.textSoft}
        />
      </FairyCard>

      <FairyCard style={styles.photoCard}>
        <Ionicons name="image-outline" size={24} color={colors.accent} />
        <View style={{ flex: 1 }}>
          <Text style={styles.photoTitle}>添加照片</Text>
          <Text style={styles.photoText}>让这一页更像一本真的绘本。</Text>
        </View>
      </FairyCard>

      <FairyButton title="保存这一页" onPress={handleSave} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  card: { marginBottom: 16 },
  label: { color: colors.text, fontSize: 15, fontWeight: '800', marginTop: 8 },
  titleInput: { marginTop: 12, minHeight: 48, color: colors.text, fontSize: 18, fontWeight: '700' },
  tags: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 12 },
  editorCard: { marginBottom: 16 },
  editorHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 12 },
  bodyInput: { minHeight: 220, color: colors.text, fontSize: 16, lineHeight: 25 },
  photoCard: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 22, backgroundColor: colors.cardPink },
  photoTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  photoText: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
