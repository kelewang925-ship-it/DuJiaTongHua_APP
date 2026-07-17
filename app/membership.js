import { useState } from 'react';
import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyDialog from '@/components/FairyDialog';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyPage from '@/components/FairyPage';
import FairyTag from '@/components/FairyTag';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import { hasCapability } from '@/config/capabilities';

const benefits = [
  { icon: 'color-wand-outline', title: '更多 AI 生成次数', detail: '每月享更多 AI 生成机会，创作不受限', badge: '享更多次数' },
  { icon: 'document-text-outline', title: '高清导出 PDF', detail: '支持高清画质导出，保留每一份细节', badge: '高清无水印' },
  { icon: 'cloud-outline', title: '云备份空间', detail: '更大专属云空间，安全备份不担忧', badge: '更大存储空间' },
  { icon: 'book-outline', title: '专属封面模板', detail: '解锁更多精美封面，让绘本更独特', badge: '会员专属模板' },
  { icon: 'calendar-outline', title: '纪念日分享样式', detail: '更多精美分享样式，收藏美好时刻', badge: '更多样式' },
];
const plans = [
  { id: 'monthly', name: '月度会员', price: '¥18', unit: '/月', detail: '灵活开启 · 随时可取消' },
  { id: 'yearly', name: '年度会员', price: '¥168', unit: '/年', detail: '约 ¥14/月 · 节省 22%', recommended: true },
  { id: 'forever', name: '永久珍藏', price: '¥388', unit: '一次付费', detail: '永久有效 · 珍藏所有回忆' },
];

export default function MembershipPage() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const [activePlan, setActivePlan] = useState(plans[1].id);
  const [agreed, setAgreed] = useState(true);
  const [showConfirm, setShowConfirm] = useState(false);
  const [activatedPlan, setActivatedPlan] = useState(null);
  const [toast, setToast] = useState(null);
  const compact = width < 690;
  const selectedPlan = plans.find((item) => item.id === activePlan) || plans[1];

  const requestPurchase = () => {
    if (!hasCapability('membershipPayment')) { setToast({ tone: 'info', message: 'Real 模式暂未开放会员与支付。' }); return; }
    if (!agreed) {
      setToast({ tone: 'info', message: '请先阅读并同意《童话会员服务协议》。' });
      return;
    }
    setShowConfirm(true);
  };

  const confirmPurchase = () => {
    setActivatedPlan(selectedPlan.id);
    setShowConfirm(false);
    setToast({ tone: 'success', message: `${selectedPlan.name}体验权益已在本地开启。` });
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="童话会员" />}
      topSpace={20}
      bottomSpace={64}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
    >
      <View style={styles.content}>
        <FairyCard style={[styles.heroCard, compact && styles.heroCardCompact]} padding={spacing.md}>
          <View style={[styles.heroImage, compact && styles.heroImageCompact]}><FairyImage name="anniversaryShareCover" height={compact ? 210 : 250} radius={24} framed={false} resizeMode="cover" /></View>
          <View style={styles.heroCopy}><View style={styles.crown}><Ionicons name="diamond-outline" size={28} color={colors.gold} /></View><Text style={styles.heroTitle}>童话会员</Text><Text style={styles.heroSubtitle}>让更多回忆被温柔保存</Text><Text style={styles.heroText}>更大空间、更精致的导出与更多创作机会，专为你们的故事准备。</Text></View>
          <View style={styles.heroRibbon}><Text style={styles.heroRibbonText}>专属特权</Text></View>
        </FairyCard>

        <View style={styles.sectionHeading}><Ionicons name="sparkles-outline" size={18} color={colors.gold} /><Text style={styles.sectionTitle}>会员专属权益</Text><Ionicons name="sparkles-outline" size={18} color={colors.gold} /></View>
        <FairyCard style={styles.benefitsCard} padding={0}>{benefits.map((item, index) => <View key={item.title} style={[styles.benefitRow, index < benefits.length - 1 && styles.benefitDivider]}><View style={styles.benefitIcon}><Ionicons name={item.icon} size={25} color={colors.gold} /></View><View style={styles.benefitCopy}><Text style={styles.benefitTitle}>{item.title}</Text><Text style={styles.benefitDetail}>{item.detail}</Text></View><View style={styles.benefitBadge}><Text style={styles.benefitBadgeText}>{item.badge}</Text><Ionicons name="diamond" size={13} color={colors.gold} /></View></View>)}</FairyCard>

        <View style={[styles.sectionHeading, styles.planHeading]}><Ionicons name="heart-outline" size={17} color={colors.primaryDeep} /><Text style={styles.sectionTitle}>会员套餐</Text><Ionicons name="heart-outline" size={17} color={colors.primaryDeep} /></View>
        <View style={[styles.planList, compact && styles.planListCompact]}>{plans.map((plan) => { const active = plan.id === activePlan; return <Pressable key={plan.id} accessibilityRole="radio" accessibilityState={{ checked: active }} onPress={() => setActivePlan(plan.id)} style={({ pressed }) => [styles.planPressable, compact && styles.planPressableCompact, pressed && styles.pressed]}><FairyCard style={[styles.planCard, active && styles.planCardActive]} padding={spacing.lg} shadow={active ? 'card' : null}><View style={styles.planTop}><Text style={styles.planName}>{plan.name}</Text>{plan.recommended ? <FairyTag tone="gold">推荐</FairyTag> : null}</View><View style={styles.priceRow}><Text style={styles.planPrice}>{plan.price}</Text><Text style={styles.planUnit}>{plan.unit}</Text></View><View style={styles.planDivider} /><Text style={styles.planDetail}>{plan.detail}</Text>{active ? <View style={styles.planSelected}><Ionicons name="checkmark" size={15} color={colors.white} /></View> : null}</FairyCard></Pressable>; })}</View>

        <View style={styles.trustRow}>{[['shield-checkmark-outline', '安全加密存储'], ['heart-outline', '随时可取消'], ['lock-closed-outline', '隐私严格保护']].map(([icon, label]) => <View key={label} style={styles.trustItem}><Ionicons name={icon} size={17} color={colors.gold} /><Text style={styles.trustText}>{label}</Text></View>)}</View>

        <FairyButton title={activatedPlan === selectedPlan.id ? `${selectedPlan.name}已开启` : `开通${selectedPlan.name}`} disabled={activatedPlan === selectedPlan.id} onPress={requestPurchase} style={styles.purchaseButton} leftContent={<Ionicons name={activatedPlan === selectedPlan.id ? 'checkmark-circle-outline' : 'color-wand-outline'} size={21} color={colors.white} />} />
        <Pressable accessibilityRole="checkbox" accessibilityState={{ checked: agreed }} onPress={() => setAgreed((value) => !value)} style={({ pressed }) => [styles.agreement, pressed && styles.pressed]}><View style={[styles.agreementCheck, agreed && styles.agreementCheckActive]}>{agreed ? <Ionicons name="checkmark" size={12} color={colors.white} /> : null}</View><Text style={styles.agreementText}>开通即表示同意《童话会员服务协议》；当前为本地体验流程，不会产生真实扣款。</Text></Pressable>
        <Pressable onPress={() => router.back()} style={({ pressed }) => [styles.later, pressed && styles.pressed]}><Text style={styles.laterText}>稍后再决定</Text></Pressable>
      </View>
      <FairyDialog visible={showConfirm} title={`开启${selectedPlan.name}？`} description={`${selectedPlan.price}${selectedPlan.unit}。当前阶段仅验证会员选择和权益状态，不会连接支付或产生真实费用。`} icon="diamond-outline" confirmText="确认体验" onCancel={() => setShowConfirm(false)} onConfirm={confirmPurchase} />
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 860 }, pressed: { opacity: 0.65 },
  heroCard: { flexDirection: 'row', gap: spacing.xl, alignItems: 'center', backgroundColor: '#FFF7ED', position: 'relative', overflow: 'visible', marginBottom: spacing.xxl }, heroCardCompact: { flexDirection: 'column' }, heroImage: { width: '48%' }, heroImageCompact: { width: '100%' }, heroCopy: { flex: 1, alignItems: 'center', padding: spacing.lg }, crown: { width: 58, height: 58, borderRadius: 24, alignItems: 'center', justifyContent: 'center', backgroundColor: '#FFF0C9', borderWidth: 1, borderColor: colors.gold }, heroTitle: { color: colors.text, fontSize: 30, fontWeight: '900', marginTop: spacing.md }, heroSubtitle: { color: colors.primaryDeep, fontSize: 17, fontWeight: '900', marginTop: spacing.sm }, heroText: { color: colors.textSoft, lineHeight: 21, textAlign: 'center', marginTop: spacing.md }, heroRibbon: { position: 'absolute', right: -6, top: 16, paddingHorizontal: spacing.lg, paddingVertical: spacing.sm, backgroundColor: '#F2C96B', borderRadius: 12, transform: [{ rotate: '5deg' }] }, heroRibbonText: { color: colors.brown, fontSize: 11, fontWeight: '900' },
  sectionHeading: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.md, marginBottom: spacing.lg }, sectionTitle: { color: colors.text, fontSize: 20, fontWeight: '900' },
  benefitsCard: { backgroundColor: 'rgba(255,249,244,0.97)' }, benefitRow: { minHeight: 104, flexDirection: 'row', alignItems: 'center', gap: spacing.lg, padding: spacing.lg }, benefitDivider: { borderBottomWidth: 1, borderBottomColor: colors.border }, benefitIcon: { width: 58, height: 58, borderRadius: 22, alignItems: 'center', justifyContent: 'center', backgroundColor: '#FFF5DF', borderWidth: 1, borderColor: colors.border }, benefitCopy: { flex: 1, minWidth: 0 }, benefitTitle: { color: colors.text, fontSize: 17, fontWeight: '900' }, benefitDetail: { color: colors.textSoft, lineHeight: 20, marginTop: 5 }, benefitBadge: { flexDirection: 'row', alignItems: 'center', gap: 5, paddingHorizontal: spacing.md, paddingVertical: spacing.sm, borderRadius: 14, backgroundColor: '#FFF8E8' }, benefitBadgeText: { color: colors.gold, fontSize: 11, fontWeight: '900' },
  planHeading: { marginTop: spacing.xxl }, planList: { flexDirection: 'row', gap: spacing.md }, planListCompact: { flexDirection: 'column' }, planPressable: { flex: 1 }, planPressableCompact: { width: '100%' }, planCard: { minHeight: 190, backgroundColor: colors.card, position: 'relative' }, planCardActive: { backgroundColor: colors.cardPink, borderColor: colors.primaryDeep, borderWidth: 2 }, planTop: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm }, planName: { color: colors.text, fontSize: 17, fontWeight: '900' }, priceRow: { flexDirection: 'row', alignItems: 'baseline', gap: 4, marginTop: spacing.lg }, planPrice: { color: colors.primaryDeep, fontSize: 28, fontWeight: '900' }, planUnit: { color: colors.textSoft, fontSize: 12 }, planDivider: { height: 1, backgroundColor: colors.border, marginVertical: spacing.lg }, planDetail: { color: colors.textSoft, lineHeight: 20 }, planSelected: { position: 'absolute', right: 10, bottom: 10, width: 28, height: 28, borderRadius: 14, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.primaryDeep },
  trustRow: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', gap: spacing.xl, marginVertical: spacing.xl }, trustItem: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm }, trustText: { color: colors.textSoft, fontSize: 11, fontWeight: '800' }, purchaseButton: { minHeight: 58 }, agreement: { flexDirection: 'row', alignItems: 'flex-start', justifyContent: 'center', gap: spacing.sm, marginTop: spacing.md, paddingHorizontal: spacing.md }, agreementCheck: { width: 20, height: 20, borderRadius: 8, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card }, agreementCheckActive: { backgroundColor: colors.primaryDeep, borderColor: colors.primaryDeep }, agreementText: { flexShrink: 1, color: colors.textSoft, fontSize: 11, lineHeight: 18, textAlign: 'center' }, later: { minHeight: 48, alignItems: 'center', justifyContent: 'center', marginTop: spacing.sm }, laterText: { color: colors.accent, fontSize: 12, fontWeight: '800' },
});
