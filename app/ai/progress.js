import { ScrollView, View, Text, StyleSheet } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';
import useFairyStore from '../../src/store/useFairyStore';

export default function AiProgressPage() {
  const creations = useFairyStore((state) => state.creations);
  const activeAiJob = useFairyStore((state) => state.activeAiJob);
  const completeActiveAiJob = useFairyStore((state) => state.completeActiveAiJob);
  const job = activeAiJob || creations[0] || {
    title: '新的童话作品',
    type: '漫画',
    status: '生成中 · 正在绘制',
    progress: 64,
    source: '童话工坊',
    styleName: '童话绘本',
    icon: 'sparkles',
    steps: ['读取你们的回忆素材', '整理故事分镜', '绘制童话画面', '放进童话工坊作品集'],
    resultSummary: '将生成一组适合收藏的童话作品。',
  };
  const progress = job.progress || 64;
  const steps = job.steps?.length
    ? job.steps
    : ['读取你们的回忆素材', '整理故事分镜', '绘制童话画面', '放进童话工坊作品集'];
  const isDone = progress >= 100 || job.status?.includes('已生成');

  const handleComplete = () => {
    completeActiveAiJob();
    router.replace('/(tabs)/workshop');
  };

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>{isDone ? '作品已经完成' : '魔法生成中'}</Text>
      <Text style={styles.subtitle}>这里展示最新 mock AI 任务的状态、进度和作品信息。</Text>

      <LinearGradient colors={['#FFF9F4', '#FFF0F2']} style={styles.magicCard}>
        <View style={styles.circleOuter}>
          <View style={styles.circleInner}>
            <Ionicons name={job.type === '视频' ? 'film-outline' : 'sparkles'} size={42} color={colors.gold} />
          </View>
        </View>
        <FairyTag tone={isDone ? 'gold' : 'default'}>{job.type || 'AI作品'}</FairyTag>
        <Text style={styles.jobTitle}>{job.title}</Text>
        <Text style={styles.status}>{job.status}</Text>
        <Text style={styles.percent}>{progress}%</Text>
        <View style={styles.progressTrack}>
          <View style={[styles.progressFill, { width: `${progress}%` }]} />
        </View>
        <Text style={styles.meta}>{job.source} · {job.styleName}</Text>
      </LinearGradient>

      <FairyCard style={styles.stepCard}>
        <Text style={styles.stepTitle}>生成步骤</Text>
        {steps.map((item, index) => {
          const done = isDone || index < 2;
          const active = !isDone && index === 2;
          return (
            <View key={item} style={styles.step}>
              <Ionicons
                name={done ? 'checkmark-circle' : active ? 'sparkles' : 'ellipse-outline'}
                size={18}
                color={done ? colors.primaryDeep : active ? colors.gold : colors.textSoft}
              />
              <Text style={styles.stepText}>{item}</Text>
            </View>
          );
        })}
      </FairyCard>

      <FairyCard style={styles.resultCard}>
        <Text style={styles.resultTitle}>{isDone ? '作品预览' : '即将生成'}</Text>
        <Text style={styles.resultText}>{job.resultSummary}</Text>
        <View style={styles.previewGrid}>
          <View style={styles.previewPage}><Text style={styles.previewText}>01</Text></View>
          <View style={styles.previewPage}><Text style={styles.previewText}>02</Text></View>
          <View style={styles.previewPage}><Text style={styles.previewText}>03</Text></View>
        </View>
      </FairyCard>

      <FairyButton title={isDone ? '回到童话工坊' : '模拟完成并查看作品'} onPress={isDone ? () => router.replace('/(tabs)/workshop') : handleComplete} />
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
  jobTitle: { color: colors.text, fontSize: 20, fontWeight: '800', textAlign: 'center', marginTop: 10 },
  status: { color: colors.textSoft, marginTop: 8, fontSize: 13 },
  percent: { color: colors.primaryDeep, fontSize: 38, fontWeight: '900', marginTop: 10 },
  progressTrack: { width: '100%', height: 12, borderRadius: 10, backgroundColor: colors.secondary, overflow: 'hidden', marginTop: 14 },
  progressFill: { height: 12, borderRadius: 10, backgroundColor: colors.primary },
  meta: { color: colors.textSoft, marginTop: 12, fontSize: 12, fontWeight: '700' },
  stepCard: { marginBottom: 16 },
  stepTitle: { color: colors.text, fontSize: 17, fontWeight: '800', marginBottom: 12 },
  step: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 10 },
  stepText: { color: colors.text, fontSize: 14 },
  resultCard: { backgroundColor: colors.cardPink, marginBottom: 22 },
  resultTitle: { color: colors.text, fontWeight: '800', fontSize: 16, marginBottom: 8 },
  resultText: { color: colors.textSoft, lineHeight: 22 },
  previewGrid: { flexDirection: 'row', gap: 10, marginTop: 16 },
  previewPage: { flex: 1, aspectRatio: 0.78, borderRadius: 18, backgroundColor: colors.white, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' },
  previewText: { color: colors.gold, fontWeight: '900', fontSize: 20 },
  secondary: { marginTop: 12 },
});
