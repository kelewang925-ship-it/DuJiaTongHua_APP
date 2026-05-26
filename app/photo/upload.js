import { useState } from 'react';
import { Alert, ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';
import FairyInput from '../../src/components/FairyInput';
import FairyBackButton from '../../src/components/FairyBackButton';
import useFairyStore from '../../src/store/useFairyStore';

const tagOptions = ['约会', '日常', '旅行', '晚餐', '合照'];

export default function PhotoUploadPage() {
  const addPhotoRecord = useFairyStore((state) => state.addPhotoRecord);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [selectedTags, setSelectedTags] = useState(['约会', '日常']);
  const [photoCount, setPhotoCount] = useState(3);
  const [isSaving, setIsSaving] = useState(false);
  const [savedTitle, setSavedTitle] = useState('');

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

    setIsSaving(true);
    const record = addPhotoRecord({
      title,
      content,
      tags: selectedTags.length ? selectedTags : ['照片'],
      photoCount,
    });

    setSavedTitle(record.title);
    setTimeout(() => {
      setIsSaving(false);
      router.replace('/photo/album');
    }, 550);
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
        <FairyInput
          label="照片标题"
          icon="pricetag-outline"
          value={title}
          onChangeText={setTitle}
          placeholder="例如：奶油蛋糕和你"
          helper="当前是模拟上传，保存后会生成一组照片记录。"
        />
        <FairyInput
          label="小备注"
          icon="chatbubble-ellipses-outline"
          value={content}
          onChangeText={setContent}
          multiline
          placeholder="这一刻有什么想记住的？"
          helper="标题和备注至少填写一项。"
        />
        <Text style={styles.label}>照片标签</Text>
        <View style={styles.tags}>
          {tagOptions.map((tag) => (
            <Pressable key={tag} onPress={() => toggleTag(tag)}>
              <FairyTag tone={selectedTags.includes(tag) ? 'gold' : 'default'}>{tag}</FairyTag>
            </Pressable>
          ))}
        </View>
      </FairyCard>

      {savedTitle ? (
        <FairyCard style={styles.successCard}>
          <Ionicons name="checkmark-circle-outline" size={22} color={colors.accent} />
          <View style={styles.successTextWrap}>
            <Text style={styles.successTitle}>上传完成</Text>
            <Text style={styles.successText}>《{savedTitle}》已经放进回忆相册。</Text>
          </View>
        </FairyCard>
      ) : null}

      <FairyButton
        title={isSaving ? '正在保存...' : '保存到回忆相册'}
        onPress={handleSave}
        disabled={isSaving}
      />
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
  label: { color: colors.text, fontSize: 15, fontWeight: '800', marginBottom: 10 },
  tags: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  successCard: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 16, backgroundColor: '#FFF5DF' },
  successTextWrap: { flex: 1 },
  successTitle: { color: colors.text, fontSize: 15, fontWeight: '900' },
  successText: { color: colors.textSoft, fontSize: 12, marginTop: 3, lineHeight: 18 },
});
