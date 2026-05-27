import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import FairyButton from '../src/components/FairyButton';
import FairyCard from '../src/components/FairyCard';
import FairyHeader from '../src/components/FairyHeader';
import FairyPage from '../src/components/FairyPage';
import FairyTag from '../src/components/FairyTag';
import FairyToast from '../src/components/FairyToast';
import colors from '../src/theme/colors';
import spacing from '../src/theme/spacing';

const plans = [
  { id: 'monthly', name: '月度故事卡', price: '¥18/月', desc: '适合轻量记录与临时扩容。' },
  { id: 'yearly', name: '年度收藏册', price: '¥168/年', desc: '更大空间和完整导出权益。', tone: 'gold' },
];

export default function MembershipPage() {
  const [activePlan, setActivePlan] = useState(plans[1].id);
  const [toastVisible, setToastVisible] = useState(false);

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="特殊页面"
        title="童话会员"
        subtitle="不是普通 VIP，而是让回忆被更完整、也更久地收藏。"
        right={<FairyTag tone="gold">琥珀金权益</FairyTag>}
      />

      <FairyCard style={styles.heroCard}>
        <View style={styles.heroIcon}>
          <Ionicons name="sparkles-outline" size={26} color={colors.gold} />
        </View>
        <Text style={styles.heroText}>会员权益围绕存储空间、导出质感、AI 创作额度和专属模板，不做无关功能堆叠。</Text>
      </FairyCard>

      <Text style={styles.sectionTitle}>核心权益</Text>
      <View style={styles.benefits}>
        {[
          '更大云空间：保存更多照片、漫画、视频',
          '高级导出模板：纸雕封面与章节装帧',
          'AI 额度扩展：更多漫画页与回忆放映机时长',
          '专属纪念日模板：节日与旅行版式',
        ].map((item) => (
          <FairyCard key={item} style={styles.benefitCard}>
            <Ionicons name="checkmark-circle-outline" size={18} color={colors.gold} />
            <Text style={styles.benefitText}>{item}</Text>
          </FairyCard>
        ))}
      </View>

      <Text style={styles.sectionTitle}>开通方案</Text>
      <View style={styles.planList}>
        {plans.map((plan) => {
          const active = plan.id === activePlan;
          return (
            <Pressable key={plan.id} onPress={() => setActivePlan(plan.id)}>
              <FairyCard style={[styles.planCard, active && styles.planCardActive]}>
                <View style={styles.planHead}>
                  <Text style={styles.planName}>{plan.name}</Text>
                  <FairyTag tone={plan.tone}>{active ? '已选择' : '可选择'}</FairyTag>
                </View>
                <Text style={styles.planPrice}>{plan.price}</Text>
                <Text style={styles.planDesc}>{plan.desc}</Text>
              </FairyCard>
            </Pressable>
          );
        })}
      </View>

      <View style={styles.actions}>
        <FairyButton title="开通童话会员（mock）" onPress={() => setToastVisible(true)} />
        <FairyButton title="稍后再决定" variant="secondary" onPress={() => {}} />
      </View>

      <FairyToast
        visible={toastVisible}
        tone="success"
        message="会员开通请求已进入 mock 流程。"
        onHide={() => setToastVisible(false)}
      />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  heroCard: { backgroundColor: colors.cardPink, marginBottom: spacing.xl, flexDirection: 'row', gap: spacing.md },
  heroIcon: {
    width: 46,
    height: 46,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFF5DF',
    borderWidth: 1,
    borderColor: colors.border,
  },
  heroText: { flex: 1, color: colors.textSoft, lineHeight: 21 },
  sectionTitle: { color: colors.text, fontSize: 18, fontWeight: '900', marginBottom: spacing.md },
  benefits: { gap: spacing.sm, marginBottom: spacing.xl },
  benefitCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, padding: spacing.md },
  benefitText: { color: colors.text, flex: 1, lineHeight: 20 },
  planList: { gap: spacing.md, marginBottom: spacing.xl },
  planCard: { padding: spacing.lg },
  planCardActive: { backgroundColor: '#FFF3F5' },
  planHead: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', gap: spacing.md },
  planName: { color: colors.text, fontSize: 17, fontWeight: '900' },
  planPrice: { color: colors.gold, fontSize: 22, fontWeight: '900', marginTop: spacing.sm },
  planDesc: { color: colors.textSoft, marginTop: spacing.xs },
  actions: { gap: spacing.md },
});
