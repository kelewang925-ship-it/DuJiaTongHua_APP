import { useState } from 'react';
import { Image, Platform, Pressable, StyleSheet, Text, View, useWindowDimensions } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import FairyButton from '../src/components/FairyButton';
import FairyCard from '../src/components/FairyCard';
import FairyInput from '../src/components/FairyInput';
import FairyPage from '../src/components/FairyPage';
import FairySvgIcon from '../src/components/FairySvgIcon';
import colors from '../src/theme/colors';
import spacing from '../src/theme/spacing';
import { signInWithEmailPassword, signUpWithEmailPassword, resetPassword } from '../src/api/authApi';
import { message } from '../src/components/FairyMessage';

export default function LoginPage() {
  const isWeb = Platform.OS === 'web';
  const { width } = useWindowDimensions();
  const isCompact = !isWeb || width < 420;
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [registering, setRegistering] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const login = async () => {
    const normalizedEmail = email.trim().toLowerCase();
    if (!normalizedEmail.includes('@') || password.length < 6) { message.error('请输入有效邮箱和至少 6 位密码'); return; }
    setSubmitting(true);
    const result = registering
      ? await signUpWithEmailPassword(normalizedEmail, password, { nickname: normalizedEmail.split('@')[0] })
      : await signInWithEmailPassword(normalizedEmail, password);
    setSubmitting(false);
    if (!result.success) { message.error(result.error?.message || '操作失败，请稍后重试'); return; }
    if (registering && !result.data?.session) { message.success('注册成功，请先到邮箱完成验证'); return; }
    router.replace('/account/invite');
  };

  const forgotPassword = async () => {
    if (!email.trim().includes('@')) { message.info('请先输入注册邮箱'); return; }
    setSubmitting(true);
    const result = await resetPassword(email.trim());
    setSubmitting(false);
    result.success ? message.success('密码重置邮件已发送') : message.error(result.error?.message || '发送失败');
  };

  return (
    <FairyPage
      topSpace={isCompact ? 12 : 20}
      bottomSpace={isCompact ? 12 : 20}
      contentStyle={styles.pageContent}
    >
      <Image
        source={require('../assets/images/login-page/image1.png')}
        resizeMode="contain"
        style={[styles.heroImage, isCompact && styles.mobileTopImage]}
      />

      <FairyCard
        shadow="floating"
        radius={isCompact ? 22 : 24}
        padding={0}
        borderWidth={0}
        backgroundColor="transparent"
        shadowBackgroundColor={colors.card}
        shadowStyle={[styles.form, isCompact && styles.mobileForm]}
        contentStyle={[styles.formContent, isCompact && styles.mobileFormContent]}
      >
        <FairyInput
          label={(
            <View style={styles.inputLabelContent}>
              <Text style={[styles.inputLabelText, isCompact && styles.mobileInputLabel]}>邮箱</Text>
              <FairySvgIcon name="heart" size={12} color="#E9A09A" strokeWidth={1.8} />
            </View>
          )}
          icon="mail-outline"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
          containerStyle={isCompact && styles.mobileInputContainer}
          labelRowStyle={isCompact && styles.mobileLabelRow}
          inputWrapStyle={isCompact && styles.mobileInputWrap}
          inputStyle={isCompact && styles.mobileInputText}
        />
        <FairyInput
          label={(
            <View style={styles.inputLabelContent}>
              <Text style={[styles.inputLabelText, isCompact && styles.mobileInputLabel]}>密码</Text>
              <FairySvgIcon name="heart" size={12} color="#E9A09A" strokeWidth={1.8} />
            </View>
          )}
          icon="lock-closed-outline"
          value={password}
          onChangeText={setPassword}
          secureTextEntry={!passwordVisible}
          containerStyle={isCompact && styles.mobileInputContainer}
          labelRowStyle={isCompact && styles.mobileLabelRow}
          inputWrapStyle={isCompact && styles.mobileInputWrap}
          inputStyle={isCompact && styles.mobileInputText}
          right={
            <Pressable
              hitSlop={10}
              onPress={() => setPasswordVisible((value) => !value)}
            >
              <Ionicons
                name={passwordVisible ? 'eye-off-outline' : 'eye-outline'}
                size={20}
                color={colors.text}
              />
            </Pressable>
          }
        />

        <View style={styles.loginOptions}>
          <Pressable
            hitSlop={8}
            style={styles.rememberMe}
            onPress={() => setRememberMe((value) => !value)}
          >
            <View style={[styles.checkbox, rememberMe && styles.checkboxChecked]}>
              {rememberMe ? <Ionicons name="checkmark" size={15} color={colors.white} style={styles.checkIcon} /> : null}
            </View>
            <Text style={styles.rememberText}>记住我</Text>
          </Pressable>
          <FairyButton title="忘记密码" variant="link" textStyle={styles.linkButtonText} onPress={forgotPassword} disabled={submitting} />
        </View>

        <FairyButton
          title={submitting ? '处理中…' : registering ? '注册' : '登录'}
          onPress={login}
          disabled={submitting}
          backgroundName="buttonBackground3"
          style={styles.loginButton}
        />

        <View style={styles.divider}>
          <View style={styles.dividerLine} />
          {/* <Image
            source={require('../assets/images/icons/public/little-heart.png')}
            resizeMode="contain"
            style={styles.dividerHeart}
          /> */}
          <FairySvgIcon name="heart" size={25} color="#E9A09A" strokeWidth={1.5} style={{ marginLeft: 10, marginRight: 10 }} />
          <View style={styles.dividerLine} />
        </View>

        <View style={styles.registerRow}>
          <Text style={styles.registerHint}>还没有账号？</Text>
          <Pressable onPress={() => setRegistering((value) => !value)} disabled={submitting}>
            <Text style={styles.registerLink}>{registering ? '返回登录 >' : '注册新账号 >'}</Text>
          </Pressable>
        </View>
      </FairyCard>

      <Image
        source={require('../assets/images/login-page/image2.png')}
        resizeMode="contain"
        style={[styles.bottomImage, isCompact && styles.mobileBottomImage]}
      />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: {
    paddingHorizontal: 0,
  },
  heroImage: {
    width: '100%',
    height: 140,
  },
  mobileTopImage: {
    height: 120,
  },
  bottomImage: {
    width: '100%',
    height: 130,
  },
  mobileBottomImage: {
    height: 110,
  },
  form: {
    width: '80%',
    maxWidth: 420,
    alignSelf: 'center',
    marginBottom: spacing.lg,
  },
  formContent: {
    borderRadius: 24,
    borderWidth: 3,
    borderColor: colors.white,
    backgroundColor: 'rgba(255, 255, 255, 0.28)',
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.xl,
  },
  mobileForm: {
    width: '88%',
    maxWidth: '88%',
  },
  mobileFormContent: {
    borderRadius: 22,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.lg,
  },
  mobileInputContainer: {
    marginBottom: spacing.md,
  },
  mobileLabelRow: {
    marginBottom: spacing.xs,
  },
  inputLabelContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  inputLabelText: {
    color: colors.text,
    fontSize: 15,
    fontWeight: '800',
    marginRight: 10,
  },
  mobileInputLabel: {
    fontSize: 14,
  },
  mobileInputWrap: {
    minHeight: 46,
    borderRadius: 16,
    paddingHorizontal: spacing.md,
  },
  mobileInputText: {
    fontSize: 14,
    lineHeight: 20,
  },
  loginOptions: {
    width: '100%',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: spacing.md,
  },
  rememberMe: {
    flexDirection: 'row',
    alignItems: 'center',
    flexShrink: 1,
    marginRight: spacing.md,
  },
  checkbox: {
    width: 18,
    height: 18,
    borderRadius: 5,
    borderWidth: 1,
    borderColor: colors.white,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.sm,
    backgroundColor: 'rgba(255, 255, 255, 0.32)',
  },
  checkboxChecked: {
    backgroundColor: 'rgb(251, 180, 179)',
    borderColor: 'rgb(251, 180, 179)',
  },
  checkIcon: {
    backgroundColor: 'transparent',
  },
  rememberText: {
    color: colors.text,
    fontSize: 14,
    fontWeight: '700',
    flexShrink: 1,
  },
  linkButtonText: {
    fontSize: 14,
  },
  loginButton: {
    width: '100%',
    height: 60,
    alignSelf: 'center',
  },
  divider: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 5,
    marginBottom: 5,
  },
  dividerLine: {
    flex: 1,
    height: 1,
    backgroundColor: '#99999930',
  },
  dividerHeart: {
    width: 16,
    height: 16,
    flexShrink: 0,
    marginHorizontal: spacing.md,
  },
  registerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    flexWrap: 'wrap',
  },
  registerHint: {
    color: colors.text,
    fontSize: 14,
  },
  registerLink: {
    color: 'rgb(250, 187, 185)',
    fontSize: 14,
    textDecorationLine: 'underline',
    fontWeight: '700',
  },
});
