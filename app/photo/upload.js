import { ScrollView, View, Text, TextInput, StyleSheet, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';
import FairyBackButton from '../../src/components/FairyBackButton';

export default function PhotoUploadPage() {
  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>添加照片</Text>
      <Text style={styles.subtitle}>把今天的画面，轻轻贴进你们的童话绘本。</Text>

      <FairyCard style={styles.uploadCard}>
        <View style={styles.uploadIcon}>
          <Ionicons name="image-outline" size={34} color={colors.accent} />
        </View>
        <Text style={styles.uploadTitle}>选择照片</Text>
        <Text style={styles.uploadText}>后续会接入系统相册，支持多图上传。</Text>
      </FairyCard>

      <FairyCard style={styles.formCard}>
        <Text style={styles.label}>照片标题</Text>
        <TextInput style={styles.input} placeholder="例如：奶油蛋糕和你" placeholderTextColor={colors.textSoft} />
        <Text style={styles.label}>小备注</Text>
        <TextInput style={styles.note} multiline textAlignVertical="top" placeholder="这一刻有什么想记住的？" placeholderTextColor={colors.textSoft} />
        <View style={styles.tags}>
          <FairyTag>约会</FairyTag>
          <FairyTag>日常</FairyTag>
          <FairyTag>旅行</FairyTag>
        </View>
      </FairyCard>

      <FairyButton title="保存到回忆相册" />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  uploadCard: { alignItems: 'center', justifyContent: 'center', minHeight: 210, marginBottom: 16, backgroundColor: colors.cardPink },
  uploadIcon: { width: 78, height: 78, borderRadius: 30, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', marginBottom: 14, borderWidth: 1, borderColor: colors.border },
  uploadTitle: { color: colors.text, fontSize: 20, fontWeight: '800' },
  uploadText: { color: colors.textSoft, marginTop: 8, fontSize: 13 },
  formCard: { marginBottom: 22 },
  label: { color: colors.text, fontWeight: '800', fontSize: 15, marginBottom: 10 },
  input: { minHeight: 46, color: colors.text, fontSize: 16, marginBottom: 18 },
  note: { minHeight: 120, color: colors.text, fontSize: 15, lineHeight: 23, marginBottom: 14 },
  tags: { flexDirection: 'row', gap: 8 },
});
