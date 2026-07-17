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

const faqs = [
  { id: 'account', icon: 'key-outline', title: '账号绑定', question: '如何绑定或更换情侣账号？', answer: '进入“更多功能 → 情侣信息”，可以查看当前关系信息。需要更换绑定时，请先确认双方的重要数据已经完成备份，再按页面提示解除并重新邀请。' },
  { id: 'ai', icon: 'color-wand-outline', title: 'AI 生成', question: 'AI 漫画或视频生成失败怎么办？', answer: '先确认网络可用，再到“创作历史”查看任务状态。生成中的作品可以继续等待；失败任务可返回配置页重新发起，原始日记和照片不会被删除。' },
  { id: 'pdf', icon: 'document-text-outline', title: 'PDF 导出', question: '导出时失败或没有反应怎么办？', answer: '可以先缩小日期范围或减少高清图片数量，再重新生成预览。如果仍然失败，请在下方写明使用的导出范围、纸张和清晰度，我们会据此排查。' },
  { id: 'backup', icon: 'cloud-upload-outline', title: '数据备份', question: '如何备份或恢复我的故事数据？', answer: '从“更多功能 → 数据备份恢复”创建备份。恢复前请确认备份时间与空间占用，恢复操作不会自动覆盖未确认的数据。' },
  { id: 'member', icon: 'diamond-outline', title: '会员权益', question: '会员包含哪些特权和服务？', answer: '当前会员体验覆盖更大存储空间、高清 PDF、更多 AI 创作次数、专属封面与分享样式。实际支付服务尚未接入，不会产生真实扣款。' },
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
  const [submitted, setSubmitted] = useState(null);
  const [toast, setToast] = useState(null);
  const compact = width < 640;

  const submitFeedback = () => {
    const text = content.trim();
    if (text.length < 8) {
      setError('请至少写下 8 个字，方便我们理解具体情况。');
      setToast({ tone: 'error', message: '反馈描述还需要更具体一些。' });
      return;
    }
    const selectedType = issueTypes.find((item) => item.id === issueType);
    const ticket = `TH-${String(Date.now()).slice(-6)}`;
    setSubmitted({ ticket, type: selectedType?.label || '问题反馈', summary: text.slice(0, 46), contact: contact.trim() });
    setError('');
    setContent('');
    setContact('');
    setToast({ tone: 'success', message: `反馈已收进信箱，受理编号 ${ticket}` });
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
          <View style={styles.heroCopy}><Text style={styles.heroTitle}>遇到问题可以告诉我们</Text><Text style={styles.heroText}>你的每一个建议，都会让独家童话变得更好。</Text><View style={styles.heroNote}><Ionicons name="heart-outline" size={15} color={colors.primaryDeep} /><Text style={styles.heroNoteText}>我们会认真读每一封小信</Text></View></View>
          <View style={[styles.heroImage, compact && styles.heroImageCompact]}><FairyImage name="emptyNotification" height={compact ? 170 : 190} radius={22} framed={false} resizeMode="cover" /></View>
        </FairyCard>

        <View style={styles.sectionHeading}><Ionicons name="star-outline" size={20} color={colors.gold} /><Text style={styles.sectionTitle}>常见问题</Text></View>
        <FairyCard style={styles.faqCard} padding={0}>{faqs.map((faq, index) => { const expanded = faq.id === expandedFaq; return <View key={faq.id} style={index < faqs.length - 1 && styles.faqDivider}><Pressable accessibilityRole="button" accessibilityState={{ expanded }} onPress={() => setExpandedFaq(expanded ? null : faq.id)} style={({ pressed }) => [styles.faqButton, pressed && styles.pressed]}><View style={styles.faqIcon}><Ionicons name={faq.icon} size={23} color={expanded ? colors.primaryDeep : colors.gold} /></View><View style={styles.faqCopy}><Text style={styles.faqTitle}>{faq.title}</Text><Text style={styles.faqQuestion}>{faq.question}</Text></View><Ionicons name={expanded ? 'chevron-up' : 'chevron-down'} size={20} color={expanded ? colors.primaryDeep : colors.textSoft} /></Pressable>{expanded ? <View style={styles.answer}><Ionicons name="heart-outline" size={16} color={colors.primaryDeep} /><Text style={styles.answerText}>{faq.answer}</Text></View> : null}</View>; })}</FairyCard>

        <FairyCard style={styles.feedbackCard} padding={spacing.xl}>
          <View style={styles.feedbackHeading}><View style={styles.feedbackTitleRow}><Ionicons name="mail-outline" size={23} color={colors.primaryDeep} /><Text style={styles.feedbackTitle}>反馈与建议</Text></View><Text style={styles.feedbackSubtitle}>描述越具体，我们越容易找到问题</Text></View>

          <Text style={styles.fieldLabel}>问题类型</Text>
          <View style={styles.typeRow}>{issueTypes.map((item) => { const active = issueType === item.id; return <Pressable key={item.id} accessibilityRole="radio" accessibilityState={{ checked: active }} onPress={() => setIssueType(item.id)} style={({ pressed }) => [styles.typeOption, active && styles.typeOptionActive, pressed && styles.pressed]}><Ionicons name={item.icon} size={18} color={active ? colors.primaryDeep : colors.textSoft} /><Text style={[styles.typeText, active && styles.typeTextActive]}>{item.label}</Text></Pressable>; })}</View>

          <FairyInput label="问题描述" value={content} onChangeText={(value) => { setContent(value); if (error) setError(''); }} multiline maxLength={500} placeholder="写下你遇到的问题、操作步骤或想要的功能……" helper={`${content.length}/500`} helperInside error={error} containerStyle={styles.inputWrap} />
          <FairyInput label="联系方式（选填）" icon="mail-outline" value={contact} onChangeText={setContact} maxLength={80} autoCapitalize="none" placeholder="邮箱或其他方便联系你的方式" containerStyle={styles.contactInput} />

          <View style={styles.attachmentNote}><View style={styles.attachmentIcon}><Ionicons name="camera-outline" size={20} color={colors.textSoft} /></View><View style={styles.attachmentCopy}><Text style={styles.attachmentTitle}>问题截图（可选）</Text><Text style={styles.attachmentText}>跨平台图片选择与上传服务尚未接入；当前请在描述中写明页面和操作步骤。</Text></View></View>
          <FairyButton title="提交反馈" onPress={submitFeedback} leftContent={<Ionicons name="paper-plane-outline" size={19} color={colors.white} />} />
        </FairyCard>

        {submitted ? <FairyCard style={styles.receiptCard} padding={spacing.lg}><View style={styles.receiptIcon}><Ionicons name="checkmark-circle-outline" size={26} color={colors.primaryDeep} /></View><View style={styles.receiptCopy}><Text style={styles.receiptTitle}>上一封反馈已收件</Text><Text style={styles.receiptMeta}>{submitted.ticket} · {submitted.type}{submitted.contact ? ' · 已留联系方式' : ''}</Text><Text numberOfLines={2} style={styles.receiptSummary}>{submitted.summary}</Text></View></FairyCard> : null}
        <View style={styles.footer}><Ionicons name="heart-outline" size={16} color={colors.primaryDeep} /><Text style={styles.footerText}>我们会认真读每一封小信</Text><Ionicons name="heart-outline" size={16} color={colors.primaryDeep} /></View>
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
  receiptCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, backgroundColor: colors.cardPink }, receiptIcon: { width: 50, height: 50, borderRadius: 20, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card }, receiptCopy: { flex: 1, minWidth: 0 }, receiptTitle: { color: colors.text, fontSize: 15, fontWeight: '900' }, receiptMeta: { color: colors.primaryDeep, fontSize: 11, fontWeight: '800', marginTop: 4 }, receiptSummary: { color: colors.textSoft, lineHeight: 18, marginTop: 5 },
  footer: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.md, marginTop: spacing.xxl }, footerText: { color: colors.textSoft, fontSize: 12 },
});
