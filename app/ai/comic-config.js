import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';

const stylesList = ['童话绘本', '暖色漫画', '手账贴纸'];
const sources = ['选择日记', '选择照片', '自由输入'];

export default function ComicConfigPage() {
  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <Text style={styles.title}>恋爱漫画</Text>
      <Text style={styles.subtitle}>让 AI 把你们的回忆画成一页页温柔的童话。</Text>

      <LinearGradient colors={['#FFF9F4', '#FFF0F2']} style={styles.hero}>
        <View style={styles.magic}><Ionicons name="sparkles" size={28} color={colors.gold} /></View>
        <Text style={styles.heroTitle}>把故事画成漫画</Text>
        <Text style={styles.heroText}>选择一段回忆，设置画风和角色，生成专属绘本片段。</Text>
      </LinearGradient>

      <Text style={styles.section}>选择素材</Text>
      <View style={styles.row}>
        {sources.map((item) => (
          <Pressable key={item} style={styles.choice}><Text style={styles.choiceText}>{item}</Text></Pressable>
        ))}
      </View>

      <Text style={styles.section}>漫画风格</Text>
      <View style={styles.row}>
        {stylesList.map((item, index) => (
          <Pressable key={item} style={[styles.choice, index === 0 && styles.activeChoice]}>
            <Text style={[styles.choiceText, index === 0 && styles.activeText]}>{item}</Text>
          </Pressable>
        ))}
      </View>

      <FairyCard style={styles.roleCard}>
        <View style={styles.roleHeader}>
          <Ionicons name="people-outline" size={22} color={colors.accent} />
          <Text style={styles.roleTitle}>人设管理</Text>
          <FairyTag>待完善</FairyTag>
        </View>
        <Text style={styles.roleText}>后续可为双方设置发型、服装、常用表情，让漫画角色更稳定。</Text>
      </FairyCard>

      <FairyCard style={styles.promptCard}>
        <Text style={styles.roleTitle}>生成提示</Text>
        <Text style={styles.roleText}>建议选择有情绪、有场景的小片段，例如散步、旅行、纪念日晚餐。</Text>
      </FairyCard>

      <FairyButton title="开始生成童话漫画" />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 64, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  hero: { borderRadius: 30, padding: 22, borderWidth: 1, borderColor: colors.border, marginBottom: 28 },
  magic: { width: 54, height: 54, borderRadius: 22, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 16 },
  heroTitle: { color: colors.text, fontSize: 24, fontWeight: '800' },
  heroText: { color: colors.textSoft, marginTop: 10, lineHeight: 22 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 14 },
  row: { flexDirection: 'row', gap: 10, marginBottom: 24 },
  choice: { flex: 1, minHeight: 48, borderRadius: 18, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  activeChoice: { backgroundColor: colors.primary },
  choiceText: { color: colors.text, fontSize: 13, fontWeight: '700' },
  activeText: { color: colors.white },
  roleCard: { marginBottom: 16 },
  roleHeader: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 12 },
  roleTitle: { color: colors.text, fontSize: 16, fontWeight: '800' },
  roleText: { color: colors.textSoft, lineHeight: 22 },
  promptCard: { marginBottom: 22, backgroundColor: colors.cardPink },
});
