import { useState } from 'react';
import { KeyboardAvoidingView, Platform, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../src/theme/colors';
import spacing from '../src/theme/spacing';
import FairyButton from '../src/components/FairyButton';
import FairyCard from '../src/components/FairyCard';
import FairyHeader from '../src/components/FairyHeader';
import FairyInput from '../src/components/FairyInput';
import FairyPage from '../src/components/FairyPage';
import FairyTag from '../src/components/FairyTag';
import FairyToast from '../src/components/FairyToast';
import { getApiMode } from '../src/api/client';
import { signInWithEmailPassword, signInWithOtp, signUpWithEmailPassword, upsertProfile } from '../src/api/authApi';

export default function LoginPage() {
  const [mode, setMode] = useState('signin');
  const [email, setEmail] = useState('test@example.com');
  const [password, setPassword] = useState('12345678');
  const [nickname, setNickname] = useState('童话收藏家');
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);
  const apiMode = getApiMode();
  const isSignup = mode === 'signup';

  const showToast = (message, tone = 'info') => setToast({ message, tone, key: Date.now() });

  const validate = () => {
    if (!email.trim() || !email.includes('@')) {
      showToast('请填写有效邮箱', 'error');
      return false;
    }
    if (!password || password.length < 6) {
      showToast('密码至少需要 6 位', 'error');
      return false;
    }
    return true;
  };

  const enterApp = () => router.replace('/(tabs)');

  const handleSubmit = async () => {
    if (!validate()) return;
    setLoading(true);

    const result = isSignup
      ? await signUpWithEmailPassword(email.trim(), password, { nickname })
      : await signInWithEmailPassword(email.trim(), password);

    if (!result.success) {
      setLoading(false);
      showToast(result.error.message, 'error');
      return;
    }

    if (isSignup || apiMode === 'mock') {
      await upsertProfile({ nickname, avatar_text: (nickname || '童').slice(0, 1) });
    }

    setLoading(false);
    showToast('登录成功', 'success');
    setTimeout(enterApp, 350);
  };

  const handleOtp = async () => {
    if (!email.trim() || !email.includes('@')) {
      showToast('请先填写有效邮箱', 'error');
      return;
    }

    setLoading(true);
    const result = await signInWithOtp(email.trim());
    setLoading(false);

    if (!result.success) {
      showToast(result.error.message, 'error');
      return;
    }

    showToast(apiMode === 'mock' ? 'Mock 模式已模拟发送邮件' : '登录邮件已发送', 'success');
  };

  return (
    <KeyboardAvoidingView style={styles.flex} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <FairyPage>
        <FairyHeader
          eyebrow="账号与关联"
          title="登录 / 授权"
          subtitle="先确认身份，再打开只属于你们两个人的童话。"
          right={<FairyTag tone={apiMode === 'real' ? 'gold' : 'pink'}>{apiMode === 'real' ? 'Real' : 'Mock'}</FairyTag>}
        />

        <FairyCard style={styles.hero}>
          <View style={styles.heroIcon}>
            <Ionicons name="lock-closed-outline" size={24} color={colors.accent} />
          </View>
          <Text style={styles.heroTitle}>欢迎回来</Text>
          <Text style={styles.heroText}>
            {apiMode === 'real' ? '当前使用 Supabase Auth 邮箱认证。' : '当前为 mock 模式，可以直接使用示例账号进入。'}
          </Text>
        </FairyCard>

        <View style={styles.switchRow}>
          <FairyButton title="邮箱登录" variant={isSignup ? 'secondary' : 'primary'} onPress={() => setMode('signin')} style={styles.switchButton} disabled={loading} />
          <FairyButton title="注册账号" variant={isSignup ? 'primary' : 'secondary'} onPress={() => setMode('signup')} style={styles.switchButton} disabled={loading} />
        </View>

        {isSignup ? (
          <FairyInput label="昵称" icon="person-outline" value={nickname} onChangeText={setNickname} placeholder="童话昵称" autoCapitalize="none" />
        ) : null}

        <FairyInput label="邮箱" icon="mail-outline" value={email} onChangeText={setEmail} placeholder="you@example.com" autoCapitalize="none" keyboardType="email-address" />
        <FairyInput label="密码" icon="key-outline" value={password} onChangeText={setPassword} placeholder="至少 6 位" secureTextEntry autoCapitalize="none" />

        <FairyButton title={loading ? '处理中...' : isSignup ? '注册并进入' : '进入独家童话'} onPress={handleSubmit} disabled={loading} style={styles.mainAction} />
        <FairyButton title="发送邮箱登录链接" variant="secondary" onPress={handleOtp} disabled={loading} />
      </FairyPage>

      <FairyToast key={toast?.key} visible={!!toast} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1, backgroundColor: colors.background },
  hero: { backgroundColor: colors.cardPink, marginBottom: spacing.lg },
  heroIcon: { width: 48, height: 48, borderRadius: 18, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, marginBottom: spacing.md },
  heroTitle: { color: colors.text, fontSize: 24, fontWeight: '900' },
  heroText: { color: colors.textSoft, lineHeight: 22, marginTop: spacing.sm },
  switchRow: { flexDirection: 'row', gap: spacing.md, marginBottom: spacing.lg },
  switchButton: { flex: 1 },
  mainAction: { marginTop: spacing.sm, marginBottom: spacing.md },
});
