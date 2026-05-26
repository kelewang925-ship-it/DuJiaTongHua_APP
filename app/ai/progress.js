import { ScrollView, View, Text, StyleSheet } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import useFairyStore from '../../src/store/useFairyStore';

export default function AiProgressPage() {
  const creations = useFairyStore((state) => state.creations);
  const job = creations[0] || {
    title: '新的童话作品',
    type: '漫画',
    status: '生成中 · 正在绘制',
  };
  const progress = job.type === '视频' ? 48 : 64;

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>魔法生成中</Text>
      <Text style={styles.subtitle}>请稍等，回忆正在纸页上慢慢浮现。</Text>

      <LinearGradient colors={['#FFF9F4', '#FFF0F2']} style={styles.magicCard}>
        <View style={styles.circleOuter}>
          <View style={styles.circleInner}>
            <Ionicons name={job.type === '视频' ? 'film-outline' : 'sparkles'} size={42} color={colors.gold} />
          </View>
        </View>
        <Text style={styles.jobType}>{job.type || 'AI作品'}</Text>
        <Text style={styles.jobTitle}>{job.title}</Text>
        <Text style={styles.status}>{job.status}</Text>
        <Text style={styles.percent}>{progress}%</Text>
        <View style={styles.progressTrack}>
          <View style={[styles.progressFill, { width: `${progress}%` }]} />
        </View>
      </LinearGradient>

      <FairyCard style={styles.stepCard}>
        <Text style={styles.stepTitle}>正在进行</Text>
        <View style={styles.step}><Ionicons name="checkmark-circle" size={18} color={colors.primaryDeep} /><Text style={styles.stepText}>读取你们的回忆素材</Text></View>
        <View style={styles.step}><Ionicons name="checkmark-circle" size={18} color={colors.primaryDeep} /><Text style={styles.stepText}>整理故事分镜</Text></View>
        <View style={styles.step}><Ionicons name="sparkles" size={18} color={colors.gold} /><Text style={styles.stepText}>{job.type === '视频' ? '生成字幕、音乐和转场' : '绘制童话漫画页面'}</Text></View>
      </FairyCard>

      <FairyCard style={styles.tipCard}>
        <Text style={styles.tipTitle}>温柔提示</Text>
        <Text style={styles.tipText}>生成完成后会出现在童话工坊的创作历史中，也已经同步到情侣空间动态里。</Text>
      </FairyCard>

      <FairyButton title="去童话工坊查看" onPress={() => router.replace('/(tabs)/workshop')} />
      <FairyButton title="先去看看其他回忆" variant="secondary" style={styles.secondary} onPress={() => router.replace('/(tabs)')} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  magicCard: { borderRadius: 32, padding: 24, alignItems: 'center', borderWidth: 1, borderColor: colors.border, marginBottom: 18 },
  circleOuter: { width: 150, height: 150, borderRadius: 60, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 18 },
  circleInner: { width: 98, height: 98, borderRadius: 42, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  jobType: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 8 },
  jobTitle: { color: colors.text, fontSize: 20, fontWeight: '800', textAlign: 'center' },
  status: { color: colors.textSoft, marginTop: 8, fontSize: 13 },
  percent: { color: colors.primaryDeep, fontSize: 38, fontWeight: '900', marginTop: 10 },
  progressTrack: { width: '100%', height: 12, borderRadius: 10, backgroundColor: colors.secondary, overflow: 'hidden', marginTop: 14 },
  progressFill: { height: 12, borderRadius: 10, backgroundColor: colors.primary },
  stepCard: { marginBottom: 16 },
  stepTitle: { color: colors.text, fontSize: 17, fontWeight: '800', marginBottom: 12 },
  step: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 10 },
  stepText: { color: colors.text, fontSize: 14 },
  tipCard: { backgroundColor: colors.cardPink, marginBottom: 22 },
  tipTitle: { color: colors.text, fontWeight: '800', fontSize: 16, marginBottom: 8 },
  tipText: { color: colors.textSoft, lineHeight: 22 },
  secondary: { marginTop: 12 },
});
