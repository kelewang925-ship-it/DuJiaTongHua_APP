import { useState } from 'react';
import { Image, Platform, Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import FairyButton from '../src/components/FairyButton';
import FairyCard from '../src/components/FairyCard';
import FairyHeader from '../src/components/FairyHeader';
import FairyInput from '../src/components/FairyInput';
import FairyPage from '../src/components/FairyPage';
import FairySvgIcon from '../src/components/FairySvgIcon';
import FairyTag from '../src/components/FairyTag';
import FairyToast from '../src/components/FairyToast';
import colors from '../src/theme/colors';
import shadows from '../src/theme/shadows';
import spacing from '../src/theme/spacing';

export default function LoginPage() {
  const isWeb = Platform.OS === 'web';
  const [name, setName] = useState('林小满');
  const [phone, setPhone] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [toastVisible, setToastVisible] = useState(false);

  const login = () => {
    setToastVisible(true);
    setTimeout(() => router.push('/account/invite'), 350);
  };

  return (
    <FairyPage
      // backgroundName="softPink"
      topSpace={20}
      bottomSpace={20}
      contentStyle={styles.pageContent}
    // showsVerticalScrollIndicator
    >
      <Image
        source={require('../assets/images/login-page/image1.png')}
        resizeMode="stretch"
        style={{ width: '100%', height: 140 }}
      />

      <View style={[styles.form, !isWeb && styles.mobileForm]}>
        <FairyInput
          label={(
            <View style={styles.inputLabelContent}>
              <Text style={[styles.inputLabelText, !isWeb && styles.mobileInputLabel]}>邮箱</Text>
              <FairySvgIcon name="heart" size={12} color="#E9A09A" strokeWidth={1.8} />
            </View>
          )}
          icon="mail-outline"
          value={name}
          onChangeText={setName}
          containerStyle={!isWeb && styles.mobileInputContainer}
          labelRowStyle={!isWeb && styles.mobileLabelRow}
          inputWrapStyle={!isWeb && styles.mobileInputWrap}
          inputStyle={!isWeb && styles.mobileInputText}
        />
        <FairyInput
          label={(
            <View style={styles.inputLabelContent}>
              <Text style={[styles.inputLabelText, !isWeb && styles.mobileInputLabel]}>密码</Text>
              <FairySvgIcon name="heart" size={12} color="#E9A09A" strokeWidth={1.8} />
            </View>
          )}
          icon="lock-closed-outline"
          value={phone}
          onChangeText={setPhone}
          secureTextEntry={!passwordVisible}
          containerStyle={!isWeb && styles.mobileInputContainer}
          labelRowStyle={!isWeb && styles.mobileLabelRow}
          inputWrapStyle={!isWeb && styles.mobileInputWrap}
          inputStyle={!isWeb && styles.mobileInputText}
          right={
            <Pressable onPress={() => setPasswordVisible((value) => !value)}>
              <Ionicons
                name={passwordVisible ? 'eye-off-outline' : 'eye-outline'}
                size={20}
                color={colors.text}
              />
            </Pressable>
          }
        />

        <View style={styles.loginOptions}>
          <Pressable style={styles.rememberMe} onPress={() => setRememberMe((value) => !value)}>
            <View style={[styles.checkbox, rememberMe && styles.checkboxChecked]}>
              {rememberMe ? <Ionicons name="checkmark" size={15} color={colors.white} style={styles.checkIcon} /> : null}
            </View>
            <Text style={styles.rememberText}>记住我</Text>
          </Pressable>
          <FairyButton title="忘记密码" variant="link" textStyle={{ fontSize: 14 }} onPress={() => { }} />
        </View>

        <FairyButton
          title="登录"
          onPress={login}
          backgroundName="buttonBackground3"
          style={styles.loginButton}
        />

        <View style={styles.divider}>
          <View style={styles.dividerLine} />
          <Image
            source={require('../assets/images/icons/public/little-heart.png')}
            resizeMode="contain"
            style={styles.dividerHeart}
          />
          <View style={styles.dividerLine} />
        </View>

        <View style={styles.registerRow}>
          <Text style={styles.registerHint}>还没有账号？</Text>
          <Pressable onPress={() => {}}>
            <Text style={styles.registerLink}>注册新账号&gt;</Text>
          </Pressable>
        </View>
      </View>

      <Image
        source={require('../assets/images/login-page/image2.png')}
        resizeMode="stretch"
        style={{ width: '100%', height: 130 }}
      />
      {/*       


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
      /> */}
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: {
    paddingHorizontal: 0,
  },
  hero: { backgroundColor: colors.cardPink, marginBottom: spacing.lg },
  heroTitle: { color: colors.text, fontSize: 20, fontWeight: '900' },
  heroText: { color: colors.textSoft, lineHeight: 22, marginTop: spacing.sm },
  form: {
    width: '80%',
    maxWidth: 420,
    alignSelf: 'center',
    borderRadius: 24,
    borderWidth: 3,
    borderColor: colors.white,
    backgroundColor: 'rgba(255, 255, 255, 0.28)',
    marginBottom: spacing.lg,
    padding: 20,
    ...shadows.floating,
  },
  mobileForm: {
    width: '86%',
    borderRadius: 22,
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
    gap: 10,
  },
  inputLabelText: {
    color: colors.text,
    fontSize: 15,
    fontWeight: '800',
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
  actions: { gap: spacing.md },
  loginOptions: {
    width: '100%',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: spacing.md,
    fontSize: 12,
  },
  rememberMe: {
    flexDirection: 'row',
    alignItems: 'center',
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
  },
  loginButton: {
    width: "100%",
    height: 60,
    alignSelf: 'center',
  },
  divider: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
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
  },
  registerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
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
