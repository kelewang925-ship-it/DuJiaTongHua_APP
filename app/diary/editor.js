import { ScrollView, View, Text, TextInput, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';

export default function DiaryEditorPage() {
  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <Text style={styles.title}>写一页童话</Text>
      <Text style={styles.subtitle}>把今天的小事，悄悄收藏进你们的故事里。</Text>

      <FairyCard style={styles.card}>
        <Text style={styles.label}>今天的标题</Text>
        <TextInput style={styles.titleInput} placeholder="例如：一起散步的傍晚" placeholderTextColor={colors.textSoft} />
        <View style={styles.tags}>
          <FairyTag>开心</FairyTag>
          <FairyTag>约会</FairyTag>
          <FairyTag>日常</FairyTag>
        </View>
      </FairyCard>

      <FairyCard style={styles.editorCard}>
        <View style={styles.editorHeader}>
          <Ionicons name="create-outline" size={20} color={colors.accent} />
          <Text style={styles.label}>正文</Text>
        </View>
        <TextInput
          style={styles.bodyInput}
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

      <FairyButton title="保存这一页" />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 64, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  card: { marginBottom: 16 },
  label: { color: colors.text, fontSize: 15, fontWeight: '800' },
  titleInput: { marginTop: 12, minHeight: 48, color: colors.text, fontSize: 18, fontWeight: '700' },
  tags: { flexDirection: 'row', gap: 8, marginTop: 12 },
  editorCard: { marginBottom: 16 },
  editorHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 12 },
  bodyInput: { minHeight: 220, color: colors.text, fontSize: 16, lineHeight: 25 },
  photoCard: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 22, backgroundColor: colors.cardPink },
  photoTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  photoText: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
