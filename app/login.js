import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import FairyButton from '../src/components/FairyButton';
import FairyCard from '../src/components/FairyCard';
import FairyInput from '../src/components/FairyInput';
import FairyPage from '../src/components/FairyPage';
import FairySvgIcon from '../src/components/FairySvgIcon';
import colors from '../src/theme/colors';
import spacing from '../src/theme/spacing';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [passwordVisible, setPasswordVisible] = useState(false);

  const login = () => {
    setTimeout(() => router.push('/account/invite'), 350);
  };

  return (
    <FairyPage topSpace={28} bottomSpace={28} contentStyle={styles.pageContent}>
      <View style={styles.content}>
        <View style={styles.brandMark}><Ionicons name="heart" size={28} color={colors.primaryDeep} /></View>
        <Text style={styles.title}>独家童话</Text>
        <Text style={styles.subtitle}>打开只属于你们的恋爱绘本</Text>
        <View style={styles.stars}><FairySvgIcon name="fourPointStar" size={14} color={colors.gold} /><View style={styles.line} /><FairySvgIcon name="heart" size={16} color={colors.accent} /><View style={styles.line} /><FairySvgIcon name="fourPointStar" size={14} color={colors.gold} /></View>

        <FairyCard shadow="floating" radius={24} padding={spacing.xl} style={styles.form} contentStyle={styles.formContent}>
          <FairyInput label="邮箱" icon="mail-outline" value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address" />
          <FairyInput label="密码" icon="lock-closed-outline" value={password} onChangeText={setPassword} secureTextEntry={!passwordVisible} right={<Pressable hitSlop={10} onPress={() => setPasswordVisible((value) => !value)}><Ionicons name={passwordVisible ? 'eye-off-outline' : 'eye-outline'} size={20} color={colors.text} /></Pressable>} />
          <View style={styles.loginOptions}>
            <Pressable hitSlop={8} style={styles.rememberMe} onPress={() => setRememberMe((value) => !value)}><View style={[styles.checkbox, rememberMe && styles.checkboxChecked]}>{rememberMe ? <Ionicons name="checkmark" size={15} color={colors.white} /> : null}</View><Text style={styles.rememberText}>记住我</Text></Pressable>
            <FairyButton title="忘记密码" variant="link" textStyle={styles.linkButtonText} onPress={() => {}} />
          </View>
          <FairyButton title="登录" onPress={login} style={styles.loginButton} />
          <View style={styles.divider}><View style={styles.dividerLine} /><FairySvgIcon name="heart" size={22} color={colors.accent} /><View style={styles.dividerLine} /></View>
          <View style={styles.registerRow}><Text style={styles.registerHint}>还没有账号？</Text><Pressable onPress={() => {}}><Text style={styles.registerLink}>注册新账号</Text></Pressable></View>
        </FairyCard>
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center', justifyContent: 'center' },
  content: { width: '100%', maxWidth: 460, alignItems: 'center' },
  brandMark: { width: 64, height: 64, borderRadius: 24, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.border, transform: [{ rotate: '-5deg' }] },
  title: { color: colors.text, fontSize: 30, fontWeight: '900', marginTop: spacing.md },
  subtitle: { color: colors.textSoft, marginTop: 6, fontSize: 13 },
  stars: { width: 150, flexDirection: 'row', alignItems: 'center', gap: 8, marginVertical: spacing.xl },
  line: { flex: 1, height: 1, backgroundColor: colors.border },
  form: { width: '100%', marginBottom: spacing.lg },
  formContent: { backgroundColor: colors.card },
  loginOptions: { width: '100%', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: spacing.md },
  rememberMe: { flexDirection: 'row', alignItems: 'center', flexShrink: 1 },
  checkbox: { width: 18, height: 18, borderRadius: 5, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center', marginRight: spacing.sm },
  checkboxChecked: { backgroundColor: colors.primaryDeep, borderColor: colors.primaryDeep },
  rememberText: { color: colors.text, fontSize: 14, fontWeight: '700' },
  linkButtonText: { fontSize: 14 },
  loginButton: { width: '100%', marginTop: spacing.sm },
  divider: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, marginVertical: spacing.lg },
  dividerLine: { flex: 1, height: 1, backgroundColor: colors.border },
  registerRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', flexWrap: 'wrap', gap: 5 },
  registerHint: { color: colors.textSoft, fontSize: 14 },
  registerLink: { color: colors.primaryDeep, fontSize: 14, textDecorationLine: 'underline', fontWeight: '700' },
});
