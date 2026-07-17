import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyPage from '@/components/FairyPage';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';

const templates = [
  { id: 'firstMeet', name: '相识纪念', subtitle: '回忆第一次心动', image: 'anniversaryShareCover', icon: 'heart-outline', questions: ['那天，我们在哪里相识？', '最打动你的瞬间是？', '想对当时的 TA 说？'] },
  { id: 'birthday', name: '生日', subtitle: '写给特别的 TA', image: 'sharePreviewCover', icon: 'gift-outline', questions: ['今年最想送出的祝福？', '准备了什么小惊喜？', '下一岁想一起完成什么？'] },
  { id: 'travel', name: '旅行', subtitle: '收藏路上的风景', image: 'albumCover', icon: 'airplane-outline', questions: ['这次旅程从哪里出发？', '最舍不得错过的风景？', '想再一起去哪里？'] },
  { id: 'firstDate', name: '第一次约会', subtitle: '记住初见的瞬间', image: 'coupleCover', icon: 'mail-open-outline', questions: ['约会前最期待什么？', '哪一刻偷偷心动了？', '回家后第一句话是？'] },
  { id: 'ordinary', name: '普通纪念日', subtitle: '记录平凡也闪光的日子', image: 'homeCover', icon: 'flower-outline', questions: ['今天发生了哪件小事？', 'TA 哪个动作让你微笑？', '想把今天留给未来吗？'] },
];

export default function AnniversaryTemplatePage() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const [selectedId, setSelectedId] = useState(templates[0].id);
  const [previewPage, setPreviewPage] = useState(0);
  const [toast, setToast] = useState(null);
  const selected = useMemo(() => templates.find((item) => item.id === selectedId) || templates[0], [selectedId]);
  const wide = width >= 760;
  const compact = width < 390;
  const target = anniversaries[1] || anniversaries[0] || null;

  const selectTemplate = (id) => {
    setSelectedId(id);
    setPreviewPage(0);
  };

  const header = (
    <FairyHeader
      showBack
      title="纪念日记录模板"
      right={(
        <Pressable accessibilityRole="button" onPress={() => setToast({ message: '先选模板预览问题，再进入编辑页补充纪念日资料。', tone: 'info' })} style={({ pressed }) => [styles.helpButton, pressed && styles.pressed]}>
          <Ionicons name="help-circle-outline" size={25} color={colors.accent} />
        </Pressable>
      )}
    />
  );

  return (
    <FairyPage backgroundName="creamPaper" topSpace={28} bottomSpace={60} contentStyle={styles.pageContent} showsVerticalScrollIndicator header={header}>
      <View style={styles.content}>
        <View style={styles.intro}>
          <Text style={styles.introTitle}>选择一个专属模板，记录属于我们的故事</Text>
          <Text style={styles.introText}>模板会准备好温柔的问题和照片位置，你只需要把回忆填进去。</Text>
        </View>

        <FairyCard padding={0} radius={28} style={styles.countdownCard} contentStyle={styles.countdownContent}>
          <View style={styles.countdownImage}>
            <FairyImage name="anniversaryCover" height={compact ? 130 : 156} radius={24} framed={false} resizeMode="cover" />
          </View>
          <View style={styles.countdownCopy}>
            {target ? (
              <>
                <Text style={styles.countdownTitle}>{target.title}</Text>
                <View style={styles.countdownDaysRow}>
                  <Text style={styles.countdownLabel}>还有</Text>
                  <Text style={styles.countdownDays}>{Number.isFinite(Number(target.days)) ? Number(target.days) : 0}</Text>
                  <Text style={styles.countdownLabel}>天</Text>
                </View>
                <View style={styles.dateRow}>
                  <Ionicons name="calendar-outline" size={16} color={colors.primaryDeep} />
                  <Text style={styles.dateText}>{target.date?.replaceAll('-', '.') || '日期待补充'}</Text>
                </View>
              </>
            ) : (
              <>
                <Text style={styles.countdownTitle}>还没有纪念日章节</Text>
                <Text style={styles.emptyCountdownText}>模板可以先预览。创建纪念日后，这里会展示真实日期与倒计时。</Text>
                <Pressable accessibilityRole="button" onPress={() => router.push('/anniversary/edit')} style={({ pressed }) => [styles.createLink, pressed && styles.pressed]}>
                  <Text style={styles.createLinkText}>先创建纪念日</Text>
                  <Ionicons name="arrow-forward" size={15} color={colors.primaryDeep} />
                </Pressable>
              </>
            )}
            <Text style={styles.countdownHint}>每一个重要的日子，都值得被珍藏。</Text>
          </View>
        </FairyCard>

        <View style={styles.sectionHeading}>
          <View style={styles.sectionTitleRow}>
            <Ionicons name="flower-outline" size={21} color={colors.primaryDeep} />
            <Text style={styles.sectionTitle}>选择模板</Text>
          </View>
          <Text style={styles.sectionMeta}>{templates.length} 套绘本版式</Text>
        </View>

        <View style={styles.templateGrid}>
          {templates.map((item) => {
            const active = item.id === selectedId;
            return (
              <FairyCard key={item.id} padding={spacing.sm} radius={22} style={[styles.templateCard, wide && styles.templateCardWide, active && styles.templateCardActive]} contentStyle={styles.templateContent} onPress={() => selectTemplate(item.id)} accessibilityRole="button" accessibilityState={{ selected: active }}>
                <View style={styles.templateImageWrap}>
                  <FairyImage name={item.image} height={wide ? 172 : 146} radius={16} framed={false} resizeMode="cover" />
                  <View style={styles.templateIcon}><Ionicons name={item.icon} size={18} color={colors.primaryDeep} /></View>
                  {active ? <View style={styles.check}><Ionicons name="checkmark" size={21} color={colors.white} /></View> : null}
                </View>
                <Text numberOfLines={1} style={styles.templateName}>{item.name}</Text>
                <Text numberOfLines={2} style={styles.templateSubtitle}>{item.subtitle}</Text>
                <View style={[styles.radio, active && styles.radioActive]}>{active ? <View style={styles.radioDot} /> : null}</View>
              </FairyCard>
            );
          })}
        </View>

        <FairyCard style={styles.previewCard} padding={compact ? spacing.lg : spacing.xl}>
          <View style={styles.previewHeading}>
            <View style={styles.sectionTitleRow}>
              <Ionicons name="sparkles-outline" size={20} color={colors.gold} />
              <Text style={styles.sectionTitle}>模板预览</Text>
            </View>
            <Text style={styles.previewName}>{selected.name}</Text>
          </View>

          <View style={[styles.previewBody, wide && styles.previewBodyWide]}>
            <View style={[styles.previewCover, wide && styles.previewCoverWide]}>
              <FairyImage name={selected.image} height={wide ? 286 : 220} radius={20} framed={false} resizeMode="cover" />
              <View style={styles.previewRibbon}><Text style={styles.previewRibbonText}>{selected.name}</Text></View>
            </View>
            <View style={styles.questionCard}>
              {selected.questions.map((question, index) => {
                const highlighted = index === previewPage;
                return (
                  <Pressable key={question} onPress={() => setPreviewPage(index)} style={({ pressed }) => [styles.questionRow, highlighted && styles.questionRowActive, pressed && styles.pressed]}>
                    <View style={[styles.questionIcon, highlighted && styles.questionIconActive]}>
                      <Ionicons name={index === 0 ? 'heart-outline' : index === 1 ? 'star-outline' : 'flower-outline'} size={17} color={highlighted ? colors.white : colors.primaryDeep} />
                    </View>
                    <View style={styles.questionCopy}>
                      <Text style={[styles.questionText, highlighted && styles.questionTextActive]}>{question}</Text>
                      <View style={styles.answerLine} />
                    </View>
                  </Pressable>
                );
              })}
              <View style={styles.photoSlot}>
                <Ionicons name="images-outline" size={24} color={colors.accent} />
                <Text style={styles.photoSlotText}>照片位置会在记录页保留</Text>
              </View>
            </View>
          </View>

          <View style={styles.dots}>
            {selected.questions.map((_, index) => (
              <Pressable key={index} accessibilityLabel={`预览第 ${index + 1} 个问题`} onPress={() => setPreviewPage(index)} style={[styles.dot, index === previewPage && styles.dotActive]} />
            ))}
          </View>
        </FairyCard>

        <FairyButton title="使用这个模板" onPress={() => router.push(`/anniversary/edit?template=${selected.id}`)} leftContent={<Ionicons name="sparkles-outline" size={19} color={colors.white} />} />
      </View>
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 860 },
  helpButton: { width: 44, height: 44, alignItems: 'center', justifyContent: 'center' },
  intro: { alignItems: 'center', marginTop: spacing.md, marginBottom: spacing.xl },
  introTitle: { color: colors.text, fontSize: 18, fontWeight: '900', textAlign: 'center' },
  introText: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.sm, textAlign: 'center' },
  countdownCard: { marginBottom: spacing.xxl, overflow: 'hidden' },
  countdownContent: { minHeight: 174, padding: spacing.sm, flexDirection: 'row', alignItems: 'center', gap: spacing.lg },
  countdownImage: { width: '38%', minWidth: 112 },
  countdownCopy: { flex: 1, paddingVertical: spacing.md, paddingRight: spacing.md },
  countdownTitle: { color: colors.text, fontSize: 19, fontWeight: '900' },
  countdownDaysRow: { flexDirection: 'row', alignItems: 'flex-end', marginTop: 4 },
  countdownLabel: { color: colors.text, fontSize: 14, fontWeight: '800', marginBottom: 7 },
  countdownDays: { color: '#E98188', fontSize: 38, lineHeight: 44, fontWeight: '900', marginHorizontal: spacing.sm },
  dateRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginTop: spacing.xs },
  dateText: { color: colors.textSoft, fontSize: 13, fontWeight: '800' },
  emptyCountdownText: { color: colors.textSoft, fontSize: 12, lineHeight: 19, marginTop: spacing.sm },
  createLink: { minHeight: 36, flexDirection: 'row', alignItems: 'center', gap: spacing.xs, marginTop: spacing.sm },
  createLinkText: { color: colors.primaryDeep, fontSize: 12, fontWeight: '900' },
  countdownHint: { color: colors.textSoft, fontSize: 11, marginTop: spacing.sm },
  sectionHeading: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.md, marginBottom: spacing.md },
  sectionTitleRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  sectionTitle: { color: colors.text, fontSize: 20, fontWeight: '900' },
  sectionMeta: { color: colors.textSoft, fontSize: 12 },
  templateGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md, marginBottom: spacing.xxl },
  templateCard: { width: '47.5%', minWidth: 0 },
  templateCardWide: { width: '31.7%' },
  templateCardActive: { transform: [{ translateY: -3 }] },
  templateContent: { position: 'relative', alignItems: 'center', borderColor: 'transparent' },
  templateImageWrap: { width: '100%', position: 'relative' },
  templateIcon: { position: 'absolute', left: spacing.sm, top: spacing.sm, width: 34, height: 34, borderRadius: 15, alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(255,249,244,0.92)' },
  check: { position: 'absolute', right: -5, top: -5, width: 34, height: 34, borderRadius: 17, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.primaryDeep, borderWidth: 2, borderColor: colors.white },
  templateName: { color: colors.text, fontSize: 15, fontWeight: '900', marginTop: spacing.md, textAlign: 'center' },
  templateSubtitle: { minHeight: 34, color: colors.textSoft, fontSize: 11, lineHeight: 16, marginTop: 4, textAlign: 'center' },
  radio: { width: 22, height: 22, borderRadius: 11, borderWidth: 1.5, borderColor: colors.accent, alignItems: 'center', justifyContent: 'center', marginTop: spacing.sm },
  radioActive: { borderColor: colors.primaryDeep },
  radioDot: { width: 12, height: 12, borderRadius: 6, backgroundColor: colors.primaryDeep },
  previewCard: { marginBottom: spacing.lg, backgroundColor: 'rgba(255,249,244,0.96)' },
  previewHeading: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.md, marginBottom: spacing.lg },
  previewName: { flexShrink: 1, color: colors.primaryDeep, fontSize: 13, fontWeight: '900', textAlign: 'right' },
  previewBody: { gap: spacing.lg },
  previewBodyWide: { flexDirection: 'row', alignItems: 'stretch' },
  previewCover: { position: 'relative' },
  previewCoverWide: { width: '38%' },
  previewRibbon: { position: 'absolute', left: spacing.md, right: spacing.md, bottom: spacing.md, paddingVertical: spacing.sm, borderRadius: 15, alignItems: 'center', backgroundColor: 'rgba(255,249,244,0.9)' },
  previewRibbonText: { color: colors.text, fontSize: 14, fontWeight: '900' },
  questionCard: { flex: 1, gap: spacing.sm },
  questionRow: { minHeight: 64, padding: spacing.md, borderRadius: 18, flexDirection: 'row', alignItems: 'center', gap: spacing.md, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  questionRowActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  questionIcon: { width: 34, height: 34, borderRadius: 14, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  questionIconActive: { backgroundColor: colors.primaryDeep },
  questionCopy: { flex: 1 },
  questionText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  questionTextActive: { color: colors.text },
  answerLine: { height: 1, backgroundColor: colors.border, marginTop: spacing.sm },
  photoSlot: { minHeight: 54, borderRadius: 17, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, borderWidth: 1, borderStyle: 'dashed', borderColor: colors.border },
  photoSlotText: { color: colors.textSoft, fontSize: 11, fontWeight: '700' },
  dots: { flexDirection: 'row', justifyContent: 'center', gap: spacing.sm, marginTop: spacing.lg },
  dot: { width: 8, height: 8, borderRadius: 4, backgroundColor: colors.secondary },
  dotActive: { width: 22, backgroundColor: colors.primaryDeep },
  pressed: { opacity: 0.68 },
});