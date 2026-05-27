import { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import FairyButton from '../src/components/FairyButton';
import FairyCard from '../src/components/FairyCard';
import FairyHeader from '../src/components/FairyHeader';
import FairyInput from '../src/components/FairyInput';
import FairyPage from '../src/components/FairyPage';
import FairyTag from '../src/components/FairyTag';
import FairyToast from '../src/components/FairyToast';
import colors from '../src/theme/colors';
import spacing from '../src/theme/spacing';

export default function LoginPage() {
  const [name, setName] = useState('林小满');
  const [phone, setPhone] = useState('');
  const [toastVisible, setToastVisible] = useState(false);

  const login = () => {
    setToastVisible(true);
    setTimeout(() => router.push('/account/invite'), 350);
  };

  return (
    <FairyPage>
      <FairyHeader
        eyebrow="账号与关联"
        title="登录 / 授权"
        subtitle="先确认身份，再打开只属于你们两个人的童话。"
        right={<FairyTag tone="gold">安全进入</FairyTag>}
      />

      <FairyCard style={styles.hero}>
        <Text style={styles.heroTitle}>欢迎回来</Text>
        <Text style={styles.heroText}>当前为 mock 登录流程，登录后会进入情侣关联步骤。</Text>
      </FairyCard>

      <FairyCard style={styles.form}>
        <FairyInput label="你的昵称" icon="person-outline" value={name} onChangeText={setName} />
        <FairyInput label="手机号（可选）" icon="phone-portrait-outline" value={phone} onChangeText={setPhone} />
        <View style={styles.actions}>
          <FairyButton title="进入独家童话" onPress={login} />
          <FairyButton title="先去首页看看" variant="secondary" onPress={() => router.push('/(tabs)')} />
        </View>
      </FairyCard>

      <FairyToast
        visible={toastVisible}
        tone="success"
        message="登录成功，正在前往情侣关联。"
        onHide={() => setToastVisible(false)}
      />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  hero: { backgroundColor: colors.cardPink, marginBottom: spacing.lg },
  heroTitle: { color: colors.text, fontSize: 20, fontWeight: '900' },
  heroText: { color: colors.textSoft, lineHeight: 22, marginTop: spacing.sm },
  form: { marginBottom: spacing.lg },
  actions: { gap: spacing.md },
});
