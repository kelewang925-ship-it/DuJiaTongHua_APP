import { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';
import { hasCapability } from '../../src/config/capabilities';

const defaultSteps = ['整理回忆素材', '生成故事分镜', '为画面上色', '保存童话作品'];

export default function AiProgressPage() {
  const creations = useFairyStore((state) => state.creations) || [];
  const activeAiJob = useFairyStore((state) => state.activeAiJob);
  const completeActiveAiJob = useFairyStore((state) => state.completeActiveAiJob);
  const [toast, setToast] = useState(null);
  const canGenerate = hasCapability('aiGeneration');
  const job = activeAiJob || creations[0] || null;
  const progress = job ? Math.min(100, Math.max(0, job.progress || 0)) : 0;
  const steps = job?.steps?.length ? job.steps : defaultSteps;
  const isDone = Boolean(job) && (progress >= 100 || job.status?.includes('已生成'));

  const openResult = () => {
    if (!job) {
      setToast({ message: '当前没有可查看的生成任务。', tone: 'info' });
      return;
    }
    if (!canGenerate && !isDone) {
      setToast({ message: 'Real 模式暂未开放 AI 生成，不会模拟完成任务。', tone: 'info' });
      return;
    }
    const done = isDone ? job : completeActiveAiJob();
    if (!done) {
      setToast({ message: '当前没有可完成的本地模拟任务。', tone: 'error' });
      return;
    }
    if (done.type === '视频') {
      router.replace(done.id ? { pathname: '/ai/video-preview', params: { id: done.id } } : '/ai/video-preview');
      return;
    }
    router.replace({ pathname: '/ai/comic-result', params: done.id ? { id: done.id } : {} });
  };

  const header = (
    <FairyHeader
      showBack
      eyebrow="AI 魔法进行时"
      title={!job ? '暂无生成任务' : isDone ? '作品已经完成' : canGenerate ? '正在施一点童话魔法' : 'AI 生成未开放'}
      subtitle={!job ? '开始一次真实创作后，这里会展示对应任务的进度。' : isDone ? '画面已经收好，可以去预览这份新作品。' : canGenerate ? '可以放心离开页面，回来时仍能在创作历史中找到它。' : '当前 Real 模式不会创建或推进本地模拟任务。'}
    />
  );

  return (
    <FairyPage backgroundName="creamPaper" topSpace={28} bottomSpace={64} header={header}>
      <View style={styles.content}>
        {!job ? (
          <>
            <FairyEmptyState imageName="emptyAiHistory" title="还没有生成任务" description="从童话工坊发起一次漫画或视频创作后，再来这里查看真实进度。" />
            <FairyButton title="去童话工坊" onPress={() => router.replace('/(tabs)/workshop')} leftContent={<Ionicons name="color-wand-outline" size={20} color={colors.white} />} />
            <FairyButton title="查看创作历史" variant="link" style={styles.historyButton} onPress={() => router.push('/ai/history')} leftContent={<Ionicons name="time-outline" size={18} color={colors.accent} />} />
          </>
        ) : (
          <>
            <FairyCard style={styles.magicCard}>
              <View style={styles.magicTop}>
                <View style={styles.magicCopy}>
                  <FairyTag tone={isDone ? 'gold' : 'default'}>{job.type || 'AI 作品'}</FairyTag>
                  <Text style={styles.jobTitle}>{job.title}</Text>
                  <Text style={styles.meta}>{[job.source, job.styleName].filter(Boolean).join(' · ')}</Text>
                </View>
                <View style={styles.percentWrap}>
                  <Text style={styles.percent}>{progress}</Text>
                  <Text style={styles.percentUnit}>%</Text>
                </View>
              </View>

              <FairyImage name={job.type === '视频' ? 'workshopCover' : 'aiComicTriptych'} height={job.type === '视频' ? 206 : 142} radius={24} resizeMode="cover" style={styles.progressImage} />

              <View style={styles.progressHeading}>
                <Text style={styles.status}>{isDone ? '魔法已经完成' : job.status || '等待进度更新'}</Text>
                <Text style={styles.estimate}>{isDone ? '可以预览' : canGenerate ? '生成中' : '等待真实接口'}</Text>
              </View>
              <View style={styles.progressTrack}>
                <View style={[styles.progressFill, { width: `${progress}%` }]} />
              </View>
            </FairyCard>

            <FairyCard style={styles.stepCard}>
              <View style={styles.sectionHeading}>
                <Ionicons name="sparkles-outline" size={20} color={colors.gold} />
                <Text style={styles.sectionTitle}>生成步骤</Text>
              </View>
              {steps.map((item, index) => {
                const stepProgress = ((index + 1) / steps.length) * 100;
                const done = isDone || progress >= stepProgress;
                const active = !done && progress >= (index / steps.length) * 100;
                return (
                  <View key={item} style={styles.stepRow}>
                    <View style={styles.stepRail}>
                      <View style={[styles.stepDot, done && styles.stepDotDone, active && styles.stepDotActive]}>
                        {done ? <Ionicons name="checkmark" size={14} color={colors.white} /> : <Text style={styles.stepNumber}>{index + 1}</Text>}
                      </View>
                      {index < steps.length - 1 ? <View style={[styles.stepLine, done && styles.stepLineDone]} /> : null}
                    </View>
                    <View style={styles.stepCopy}>
                      <Text style={[styles.stepText, (done || active) && styles.stepTextActive]}>{item}</Text>
                      <Text style={styles.stepState}>{done ? '已完成' : active ? '进行中' : '等待中'}</Text>
                    </View>
                  </View>
                );
              })}
            </FairyCard>

            <View style={styles.notice}>
              <View style={styles.noticeIcon}><Ionicons name="notifications-outline" size={20} color={colors.accent} /></View>
              <View style={styles.noticeCopy}>
                <Text style={styles.noticeTitle}>{canGenerate ? '离开页面后也会继续' : '真实生成暂未开放'}</Text>
                <Text style={styles.noticeText}>{canGenerate ? '完成后会保存在童话工坊，本地提醒状态会同步更新。' : 'Mock 模式可体验生成进度；Real 模式不会模拟任务完成。'}</Text>
              </View>
            </View>

            <FairyButton title={isDone ? '查看完成作品' : canGenerate ? '模拟完成并查看作品' : 'AI 生成未开放'} onPress={openResult} leftContent={<Ionicons name={isDone ? 'book-outline' : 'color-wand-outline'} size={20} color={colors.white} />} />
            <FairyButton title="后台等待，去看看其他回忆" variant="secondary" style={styles.secondaryButton} onPress={() => router.replace('/(tabs)')} />
            <FairyButton title="查看创作历史" variant="link" style={styles.historyButton} onPress={() => router.push('/ai/history')} leftContent={<Ionicons name="time-outline" size={18} color={colors.accent} />} />
          </>
        )}
      </View>
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 720, alignSelf: 'center', paddingHorizontal: spacing.lg },
  magicCard: { backgroundColor: colors.cardPink, padding: spacing.lg, marginTop: spacing.sm },
  magicTop: { flexDirection: 'row', alignItems: 'flex-start', gap: spacing.md },
  magicCopy: { flex: 1, minWidth: 0 },
  jobTitle: { marginTop: spacing.sm, color: colors.text, fontSize: 20, fontWeight: '900', lineHeight: 27 },
  meta: { marginTop: 5, color: colors.textSoft, fontSize: 12, fontWeight: '600' },
  percentWrap: { flexDirection: 'row', alignItems: 'baseline' },
  percent: { color: colors.primaryDeep, fontSize: 38, fontWeight: '900' },
  percentUnit: { color: colors.primaryDeep, fontSize: 16, fontWeight: '800' },
  progressImage: { marginTop: spacing.lg, backgroundColor: colors.card },
  progressHeading: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: spacing.md, gap: spacing.md },
  status: { flex: 1, color: colors.text, fontSize: 13, fontWeight: '800' },
  estimate: { color: colors.textSoft, fontSize: 11 },
  progressTrack: { height: 11, borderRadius: 8, backgroundColor: colors.secondary, overflow: 'hidden', marginTop: spacing.sm },
  progressFill: { height: '100%', borderRadius: 8, backgroundColor: colors.primaryDeep },
  stepCard: { marginTop: spacing.lg, marginBottom: spacing.lg },
  sectionHeading: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginBottom: spacing.lg },
  sectionTitle: { color: colors.text, fontSize: 17, fontWeight: '900' },
  stepRow: { minHeight: 64, flexDirection: 'row' },
  stepRail: { width: 34, alignItems: 'center' },
  stepDot: { width: 28, height: 28, borderRadius: 14, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  stepDotDone: { borderColor: colors.primaryDeep, backgroundColor: colors.primaryDeep },
  stepDotActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  stepNumber: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  stepLine: { flex: 1, width: 2, backgroundColor: colors.border },
  stepLineDone: { backgroundColor: colors.primary },
  stepCopy: { flex: 1, paddingLeft: spacing.sm, paddingBottom: spacing.md },
  stepText: { color: colors.textSoft, fontSize: 15, fontWeight: '700' },
  stepTextActive: { color: colors.text },
  stepState: { marginTop: 4, color: colors.textSoft, fontSize: 11 },
  notice: { flexDirection: 'row', alignItems: 'center', padding: spacing.md, marginBottom: spacing.xl, borderRadius: 20, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card, gap: spacing.md },
  noticeIcon: { width: 40, height: 40, borderRadius: 15, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  noticeCopy: { flex: 1 },
  noticeTitle: { color: colors.text, fontSize: 14, fontWeight: '800' },
  noticeText: { marginTop: 4, color: colors.textSoft, fontSize: 12, lineHeight: 18 },
  secondaryButton: { marginTop: spacing.md },
  historyButton: { marginTop: spacing.lg, alignSelf: 'center' },
});