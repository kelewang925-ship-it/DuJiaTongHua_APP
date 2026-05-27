import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';

export default function CoupleInvitePage() {
  const [inviteCode] = useState('DFT520');
  const [toastVisible, setToastVisible] = useState(false);

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="账号与关联"
        title="情侣邀请"
        subtitle="生成一张温柔的小卡片，把对方邀请进双人宇宙。"
        right={<FairyTag tone="gold">{inviteCode}</FairyTag>}
      />

      <FairyCard style={styles.card}>
        <Text style={styles.title}>邀请码</Text>
        <Text style={styles.code}>{inviteCode}</Text>
        <Text style={styles.text}>当前为 mock 邀请流程，可继续到确认页模拟绑定成功。</Text>
      </FairyCard>

      <View style={styles.actions}>
        <FairyButton title="复制邀请码（mock）" onPress={() => setToastVisible(true)} />
        <FairyButton title="我已经收到邀请" variant="secondary" onPress={() => router.push('/account/bind-confirm')} />
      </View>

      <FairyToast visible={toastVisible} tone="success" message="邀请码已复制。" onHide={() => setToastVisible(false)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  card: { alignItems: 'center', backgroundColor: colors.cardPink, marginBottom: spacing.xl },
  title: { color: colors.textSoft, fontWeight: '700' },
  code: { color: colors.text, fontSize: 38, fontWeight: '900', letterSpacing: 2, marginTop: spacing.sm },
  text: { color: colors.textSoft, textAlign: 'center', marginTop: spacing.md, lineHeight: 21 },
  actions: { gap: spacing.md },
});
