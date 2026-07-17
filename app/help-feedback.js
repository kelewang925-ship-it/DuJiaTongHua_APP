import { useState } from 'react';
import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyInput from '@/components/FairyInput';
import FairyPage from '@/components/FairyPage';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import { getApiMode } from '@/api/client';
import { hasCapability } from '@/config/capabilities';

const faqs = [
  { id: 'account', icon: 'key-outline', title: '账号绑定', question: '如何绑定或更换情侣账号？', answer: '进入“更多功能 → 情侣信息”，可以查看当前关系信息。需要更换绑定时，请先确认双方的重要数据已经完成备份，再按页面提示解除并重新邀请。' },
  { id: 'ai', icon: 'color-wand-outline', title: 'AI 生成', question: 'AI 漫画或视频生成失败怎么办？', answer: 'Real 模式下 AI 生成尚未开放；Mock 模式可用于验证页面体验。' },
  { id: 'pdf', icon: 'document-text-outline', title: 'PDF 导出', question: '导出时失败或没有反应怎么办？', answer: 'Real 模式下 PDF 生成尚未开放；Mock 模式可用于验证封面和版式选择。' },
  { id: 'backup', icon: 'cloud-upload-outline', title: '数据备份', question: '如何备份或恢复我的故事数据？', answer: 'Real 模式下云备份尚未开放；当前不会把本地演示状态当作真实云端备份。' },
  { id: 'member', icon: 'diamond-outline', title: '会员权益', question: '会员包含哪些特权和服务？', answer: '当前会员页面用于展示权益方案，Real 模式支付尚未开放，不会产生真实扣款或模拟开通成功。' },
];
const issueTypes = [
  { id: 'feature', label: '功能问题', icon: 'construct-outline' },
  { id: 'content', label: '内容建议', icon: 'bulb-outline' },
  { id: 'other', label: '其他问题', icon: 'chatbubble-ellipses-outline' },
];

export default function HelpFeedbackPage() {
  const { width } = useWindowDimensions();
  const [expandedFaq, setExpandedFaq] = useState('pdf');
  const [issueType, setIssueType] = useState(issueTypes[0].id);
  const [content, setContent] = useState('');
  const [contact, setContact] = useState('');
  const [error, setError] = useState('');
  const [toast, setToast] = useState(null);
  const compact = width < 640;
  const mode = getApiMode();
  const canSubmitFeedback = hasCapability('feedbackSubmission', mode);
  const canAttachFeedback = hasCapability('feedbackAttachment', mode);

  const submitFeedback = () => {
    if (!canSubmitFeedback) {
      setToast({ tone: 'info', message: '反馈服务尚未接入。当前内容不会发送，也不会生成模拟工单。' });
      return;
    }

    const text = content.trim();
    if (text.length < 8) {
      setError('请至少写下 8 个字，方便检查表单体验。');
      setToast({ tone: 'error', message: '反馈描述还需要更具体一些。' });
      return;
    }

    setError('');
    setToast({
      tone: 'info',
      message: '当前仅完成表单校验预览，内容未发送，输入将继续保留。',
    });
  };

  const openAttachment = () => {
    if (!canAttachFeedback) {
      setToast({ tone: 'info', message: '反馈附件服务尚未接入，当前不会选择或上传文件。' });
      return;
    }
    setToast({ tone: 'info', message: '当前仅展示附件入口，不会上传文件。' });
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="帮助与反馈" />}
      topSpace={22}
      bottomSpace={64}
      contentStyle={styles.pageContent}
      keyboardShouldPersistTaps="handled"
      keyboardDismissMode="on-drag"
      automaticallyAdjustKeyboardInsets
      showsVerticalScrollIndicator
    >
      <View style={styles.content}>
        <FairyCard style={[styles.heroCard, compact && styles.heroCardCompact]} padding={spacing.md}>
          <View style={styles.heroCopy}><Text style={styles.heroTitle}>遇到问题可以先记录下来</Text><Text style={styles.heroText}>反馈服务接入后，这里会成为正式的问题提交入口。</Text><View style={styles.heroNote}><Ionicons name="information-circle-outline" size={15} color={colors.primaryDeep} /><Text style={styles.heroNoteText}>当前填写内容不会发送</Text></View></View>
          <View style={[styles.heroImage, compact && styles.heroImageCompact]}><FairyImage name="emptyNotification" height={compact ? 170 : 190} radius={22} framed={false} resizeMode="cover" /></View>
        </FairyCard>

        <View style={styles.sectionHeading}><Ionicons name="star-outline" size={20} color={colors.gold} /><Text style={styles.sectionTitle}>常见问题</Text></View>
        <FairyCard style={styles.faqCard} padding={0}>{faqs.map((faq, index) => { const expanded = faq.id === expandedFaq; return <View key={faq.id} style={index < faqs.length - 1 && styles.faqDivider}><Pressable accessibilityRole="button" accessibilityState={{ expanded }} onPress={() => setExpandedFaq(expanded ? null : faq.id)} style={({ pressed }) => [styles.faqButton, pressed && styles.pressed]}><View style={styles.faqIcon}><Ionicons name={faq.icon} size={23} color={expanded ? colors.primaryDeep : colors.gold} /></View><View style={styles.faqCopy}><Text style={styles.faqTitle}>{faq.title}</Text><Text style={styles.faqQuestion}>{faq.question}</Text></View><Ionicons name={expanded ? 'chevron-up' : 'chevron-down'} size={20} color={expanded ? colors.primaryDeep : colors.textSoft} /></Pressable>{expanded ? <View style={styles.answer}><Ionicons name="heart-outline" size={16} color={colors.primaryDeep} /><Text style={styles.answerText}>{faq.answer}</Text></View> : null}</View>; })}</FairyCard>

        <FairyCard style={styles.feedbackCard} padding={spacing.xl}>
          <View style={styles.feedbackHeading}><View style={styles.feedbackTitleRow}><Ionicons name="mail-outline" size={23} color={colors.primaryDeep} /><Text style={styles.feedbackTitle}>反馈草稿</Text></View><Text style={styles.feedbackSubtitle}>可检查填写体验，但当前不会发送到服务端</Text></View>
          <Text style={styles.fieldLabel}>问题类型</Text>
          <View style={styles.typeRow}>{issueTypes.map((item) => { const active = issueType === item.id; return <Pressable key={item.id} accessibilityRole="radio" accessibilityState={{ checked: active }} onPress={() => setIssueType(item.id)} style={({ pressed }) => [styles.typeOption, active && styles.typeOptionActive, pressed && styles.pressed]}><Ionicons name={item.icon} size={18} color={active ? colors.primaryDeep : colors.textSoft} /><Text style={[styles.typeText, active && styles.typeTextActive]}>{item.label}</Text></Pressable>; })}</View>
          <FairyInput label="问题描述" value={content} onChangeText={(value) => { setContent(value); if (error) setError(''); }} multiline maxLength={500} placeholder="写下你遇到的问题、操作步骤或想要的功能……" helper={`${content.length}/500`} helperInside error={error} containerStyle={styles.inputWrap} />
          <FairyInput label="联系方式（选填）" icon="mail-outline" value={contact} onChangeText={setContact} maxLength={80} autoCapitalize="none" placeholder="邮箱或其他方便联系你的方式" containerStyle={styles.contactInput} />
          <Pressable accessibilityRole="button" onPress={openAttachment} style={({ pressed }) => [styles.attachmentNote, pressed && styles.pressed]}><View style={styles.attachmentIcon}><Ionicons name="camera-outline" size={20} color={colors.textSoft} /></View><View style={styles.attachmentCopy}><Text style={styles.attachmentTitle}>问题截图（未接入）</Text><Text style={styles.attachmentText}>当前不会选择或上传文件，可先在描述中写明页面和操作步骤。</Text></View></Pressable>
          <FairyButton title={canSubmitFeedback ? '检查反馈草稿' : '反馈提交未开放'} onPress={submitFeedback} leftContent={<Ionicons name="document-text-outline" size={19} color={colors.white} />} />
        </FairyCard>

        <View style={styles.footer}><Ionicons name="information-circle-outline" size={16} color={colors.primaryDeep} /><Text style={styles.footerText}>正式反馈 API 接入前不会生成工单或受理编号</Text></View>
      </View>
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 800 }, pressed: { opacity: 0.65 },
  heroCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.xl, backgroundColor: 'rgba(255,249,244,0.96)', marginBottom: spacing.xxl }, heroCardCompact: { flexDirection: 'column-reverse' }, heroCopy: { flex: 1, padding: spacing.lg }, heroTitle: { color: colors.text, fontSize: 23, lineHeight: 31, fontWeight: '900' }, heroText: { color: colors.textSoft, lineHeight: 22, marginTop: spacing.md }, heroNote: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginTop: spacing.xl }, heroNoteText: { color: colors.primaryDeep, fontSize: 12, fontWeight: '800' }, heroImage: { width: '46%' }, heroImageCompact: { width: '100%' },
  sectionHeading: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginBottom: spacing.md }, sectionTitle: { color: colors.text, fontSize: 21, fontWeight: '900' },
  faqCard: { backgroundColor: 'rgba(255,249,244,0.96)', marginBottom: spacing.xxl }, faqDivider: { borderBottomWidth: 1, borderBottomColor: colors.border }, faqButton: { minHeight: 82, flexDirection: 'row', alignItems: 'center', gap: spacing.md, paddingHorizontal: spacing.lg, paddingVertical: spacing.md }, faqIcon: { width: 46, height: 46, borderRadius: 18, alignItems: 'center', justifyContent: 'center', backgroundColor: '#FFF6E8', borderWidth: 1, borderColor: colors.border }, faqCopy: { flex: 1, minWidth: 0 }, faqTitle: { color: colors.text, fontSize: 16, fontWeight: '900' }, faqQuestion: { color: colors.textSoft, fontSize: 12, marginTop: 5 }, answer: { flexDirection: 'row', alignItems: 'flex-start', gap: spacing.sm, marginHorizontal: spacing.lg, marginBottom: spacing.lg, padding: spacing.lg, borderRadius: 18, backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.border }, answerText: { flex: 1, color: colors.text, lineHeight: 22 },
  feedbackCard: { backgroundColor: 'rgba(255,249,244,0.97)', marginBottom: spacing.lg }, feedbackHeading: { marginBottom: spacing.xl }, feedbackTitleRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm }, feedbackTitle: { color: colors.text, fontSize: 21, fontWeight: '900' }, feedbackSubtitle: { color: colors.textSoft, fontSize: 12, marginTop: spacing.sm }, fieldLabel: { color: colors.text, fontSize: 15, fontWeight: '800', marginBottom: spacing.sm },
  typeRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginBottom: spacing.lg }, typeOption: { flexGrow: 1, minWidth: 140, minHeight: 44, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, paddingHorizontal: spacing.md, borderRadius: 18, backgroundColor: colors.background, borderWidth: 1, borderColor: colors.border }, typeOptionActive: { backgroundColor: colors.cardPink, borderColor: colors.primaryDeep }, typeText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' }, typeTextActive: { color: colors.primaryDeep }, inputWrap: { marginBottom: spacing.lg }, contactInput: { marginBottom: spacing.lg },
  attachmentNote: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.md, borderRadius: 18, backgroundColor: colors.background, borderWidth: 1, borderStyle: 'dashed', borderColor: colors.border, marginBottom: spacing.lg }, attachmentIcon: { width: 42, height: 42, borderRadius: 16, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card }, attachmentCopy: { flex: 1 }, attachmentTitle: { color: colors.text, fontSize: 13, fontWeight: '900' }, attachmentText: { color: colors.textSoft, fontSize: 11, lineHeight: 17, marginTop: 3 },
  footer: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.md, marginTop: spacing.xxl }, footerText: { color: colors.textSoft, fontSize: 12 },
});