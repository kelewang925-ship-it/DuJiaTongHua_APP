import { StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import FairyButton from '../src/components/FairyButton';
import FairyCard from '../src/components/FairyCard';
import FairyHeader from '../src/components/FairyHeader';
import FairyPage from '../src/components/FairyPage';
import FairyTag from '../src/components/FairyTag';
import colors from '../src/theme/colors';
import spacing from '../src/theme/spacing';

export default function OnboardingPage() {
  return (
    <FairyPage>
      <FairyHeader
        eyebrow="首次使用"
        title="欢迎来到独家童话"
        subtitle="这里不是打卡工具，而是一本慢慢写满的恋爱绘本。"
        right={<FairyTag>第一章</FairyTag>}
      />

      <FairyCard style={styles.card}>
        <Text style={styles.title}>把每一天写成童话</Text>
        <Text style={styles.text}>记录日记、照片、纪念日，再用童话工坊把回忆变成漫画和放映机。</Text>
      </FairyCard>

      <View style={styles.actions}>
        <FairyButton title="开始书写" onPress={() => router.push('/login')} />
        <FairyButton title="直接进入首页" variant="secondary" onPress={() => router.push('/(tabs)')} />
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  card: { backgroundColor: colors.cardPink, marginBottom: spacing.xl },
  title: { color: colors.text, fontSize: 20, fontWeight: '900' },
  text: { color: colors.textSoft, lineHeight: 22, marginTop: spacing.sm },
  actions: { gap: spacing.md },
});
