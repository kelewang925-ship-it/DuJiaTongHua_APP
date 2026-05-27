import { useMemo } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';

export default function AnniversaryCountdownPage() {
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const target = anniversaries[1] || anniversaries[0];

  const days = useMemo(() => {
    const fallback = target?.days || 0;
    return fallback > 0 ? fallback : 24;
  }, [target]);

  return (
    <FairyPage>
      <FairyHeader showBack eyebrow="纪念日相关" title="纪念日倒计时" subtitle="把等待也变成有仪式感的一页。" right={<FairyTag tone="gold">还有 {days} 天</FairyTag>} />

      <FairyCard style={styles.card}>
        <Text style={styles.event}>{target?.title || '第一次旅行'}</Text>
        <Text style={styles.date}>{target?.date || '待设置日期'}</Text>
        <Text style={styles.count}>{days}</Text>
        <Text style={styles.unit}>天</Text>
      </FairyCard>

      <View style={styles.actions}>
        <FairyButton title="准备记录模板" onPress={() => {}} />
        <FairyButton title="去纪念日列表" variant="secondary" onPress={() => {}} />
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  card: { backgroundColor: colors.cardPink, alignItems: 'center', marginBottom: spacing.xl },
  event: { color: colors.text, fontSize: 22, fontWeight: '900' },
  date: { color: colors.textSoft, marginTop: spacing.sm },
  count: { color: colors.primaryDeep, fontSize: 64, fontWeight: '900', marginTop: spacing.md, lineHeight: 68 },
  unit: { color: colors.textSoft, fontSize: 14, fontWeight: '700' },
  actions: { gap: spacing.md },
});
