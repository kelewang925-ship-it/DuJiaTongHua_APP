import { StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';

export default function BindConfirmPage() {
  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="账号与关联"
        title="绑定确认"
        subtitle="确认后，你们的记录会进入同一个私密空间。"
      />

      <FairyCard style={styles.card}>
        <View style={styles.row}>
          <FairyTag tone="gold">林小满</FairyTag>
          <Text style={styles.link}>与</Text>
          <FairyTag tone="gold">陆星河</FairyTag>
        </View>
        <Text style={styles.text}>绑定成功后，双方将共享日记、照片、纪念日和童话工坊作品。</Text>
      </FairyCard>

      <View style={styles.actions}>
        <FairyButton title="确认绑定" onPress={() => router.push('/account/couple-info')} />
        <FairyButton title="返回邀请码页" variant="secondary" onPress={() => router.push('/account/invite')} />
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  card: { backgroundColor: colors.cardPink, marginBottom: spacing.xl, alignItems: 'center' },
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  link: { color: colors.text, fontSize: 16, fontWeight: '800' },
  text: { color: colors.textSoft, textAlign: 'center', marginTop: spacing.md, lineHeight: 21 },
  actions: { gap: spacing.md },
});
