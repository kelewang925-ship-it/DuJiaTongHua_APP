import { useState } from 'react';
import { Alert, ScrollView, View, Text, TextInput, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';
import FairyBackButton from '../../src/components/FairyBackButton';
import useFairyStore from '../../src/store/useFairyStore';

const tagOptions = ['约会', '日常', '旅行', '晚餐', '合照'];

export default function PhotoUploadPage() {
  const addPhotoRecord = useFairyStore((state) => state.addPhotoRecord);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [selectedTags, setSelectedTags] = useState(['约会', '日常']);
  const [photoCount, setPhotoCount] = useState(3);

  const toggleTag = (tag) => {
    setSelectedTags((current) =>
      current.includes(tag) ? current.filter((item) => item !== tag) : [...current, tag]
    );
  };

  const handleSave = () => {
    if (!title.trim() && !content.trim()) {
      Alert.alert('还没有照片故事', '给这组照片起个小标题，或者写一句备注吧。');
      return;
    }

    addPhotoRecord({ title, content, tags: selectedTags, photoCount });
    router.replace('/(tabs)');
  };

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>添加照片</Text>
      <Text style={styles.subtitle}>把今天的画面，轻轻贴进你们的童话绘本。</Text>

      <FairyCard style={styles.uploadCard}>
        <View style={styles.uploadIcon}>
          <Ionicons name="image-outline" size={34} color={colors.accent} />
        </View>
        <Text style={styles.uploadTitle}>模拟选择 {photoCount} 张照片</Text>
        <Text style={styles.uploadText}>后续可接入系统相册；当前先完成记录流转。</Text>
        <View style={styles.countRow}>
          {[1, 3, 6].map((count) => (
            <Pressable key={count} onPress={() => setPhotoCount(count)}>
              <FairyTag tone={photoCount === count ? 'gold' : 'default'}>{count} 张</FairyTag>
            </Pressable>
          ))}
        </View>
      </FairyCard>

      <FairyCard style={styles.formCard}>
        <Text style={styles.label}>照片标题</Text>
        <TextInput
          style={styles.input}
          value={title}
          onChangeText={setTitle}
          placeholder="例如：奶油蛋糕和你"
          placeholderTextColor={colors.textSoft}
        />
        <Text style={styles.label}>小备注</Text>
        <TextInput
          style={styles.note}
          value={content}
          onChangeText={setContent}
          multiline
          textAlignVertical="top"
          placeholder="这一刻有什么想记住的？"
          placeholderTextColor={colors.textSoft}
        />
        <View style={styles.tags}>
          {tagOptions.map((tag) => (
            <Pressable key={tag} onPress={() => toggleTag(tag)}>
              <FairyTag tone={selectedTags.includes(tag) ? 'gold' : 'default'}>{tag}</FairyTag>
            </Pressable>
          ))}
        </View>
      </FairyCard>

      <FairyButton title="保存到回忆相册" onPress={handleSave} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  uploadCard: { alignItems: 'center', justifyContent: 'center', minHeight: 230, marginBottom: 16, backgroundColor: colors.cardPink },
  uploadIcon: { width: 78, height: 78, borderRadius: 30, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', marginBottom: 14, borderWidth: 1, borderColor: colors.border },
  uploadTitle: { color: colors.text, fontSize: 20, fontWeight: '800' },
  uploadText: { color: colors.textSoft, marginTop: 8, fontSize: 13, textAlign: 'center' },
  countRow: { flexDirection: 'row', gap: 8, marginTop: 16 },
  formCard: { marginBottom: 22 },
  label: { color: colors.text, fontWeight: '800', fontSize: 15, marginBottom: 10 },
  input: { minHeight: 46, color: colors.text, fontSize: 16, marginBottom: 18 },
  note: { minHeight: 120, color: colors.text, fontSize: 15, lineHeight: 23, marginBottom: 14 },
  tags: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
});
