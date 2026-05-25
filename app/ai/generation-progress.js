import { ScrollView, View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyBackButton from '../../src/components/FairyBackButton';

export default function GenerationProgressPage() {
  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>魔法正在发生</Text>
      <Text style={styles.subtitle}>正在把你们的回忆，一点点画成童话。</Text>

      <LinearGradient colors={['#FFF9F4', '#FFF0F2']} style={styles.magicCard}>
        <View style={styles.sparkleRing}>
          <Ionicons name="sparkles" size={42} color={colors.gold} />
        </View>
        <Text style={styles.progressNum}>68%</Text>
        <View style={styles.progressTrack}>
          <View style={styles.progressFill} />
        </View>
        <Text style={styles.progressText}>正在绘制第 2 页漫画分镜...</Text>
      </LinearGradient>

      <Text style={styles.section}>生成步骤</Text>
      <FairyCard style={styles.step}><Ionicons name="checkmark-circle" size={22} color={colors.primaryDeep} /><Text style={styles.stepText}>已读取你们的故事素材</Text></FairyCard>
      <FairyCard style={styles.step}><Ionicons name="checkmark-circle" size={22} color={colors.primaryDeep} /><Text style={styles.stepText}>已生成绘本风格脚本</Text></FairyCard>
      <FairyCard style={styles.stepActive}><Ionicons name="color-palette-outline" size={22} color={colors.gold} /><Text style={styles.stepText}>正在绘制漫画画面</Text></FairyCard>
      <FairyCard style={styles.step}><Ionicons name="ellipse-outline" size={22} color={colors.textSoft} /><Text style={styles.stepText}>等待生成最终成品</Text></FairyCard>

      <FairyButton title="稍后在创作历史查看" variant="secondary" />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  magicCard: { borderRadius: 32, padding: 24, alignItems: 'center', borderWidth: 1, borderColor: colors.border, marginBottom: 28 },
  sparkleRing: { width: 112, height: 112, borderRadius: 44, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 18 },
  progressNum: { color: colors.text, fontSize: 42, fontWeight: '900' },
  progressTrack: { width: '100%', height: 10, borderRadius: 10, backgroundColor: colors.secondary, marginTop: 16, overflow: 'hidden' },
  progressFill: { width: '68%', height: 10, backgroundColor: colors.primary, borderRadius: 10 },
  progressText: { color: colors.textSoft, marginTop: 14 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 16 },
  step: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 12 },
  stepActive: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 12, backgroundColor: colors.cardPink },
  stepText: { color: colors.text, fontWeight: '700' },
});
