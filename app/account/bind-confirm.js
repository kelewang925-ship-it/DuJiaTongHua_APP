import { Image, StyleSheet, Text, View } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { useRef, useState } from 'react';
import { Ionicons } from '@expo/vector-icons';
import FairyBackgroundContainer from '../../src/components/FairyBackgroundContainer';
import FairyButton from '../../src/components/FairyButton';
import FairyHeader from '../../src/components/FairyHeader';
import FairyPage from '../../src/components/FairyPage';
import FairyRequestState from '../../src/components/FairyRequestState';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import FairySvgIcon from '../../src/components/FairySvgIcon';
import { bindCoupleByCode } from '../../src/api/coupleApi';
import { getApiMode } from '../../src/api/client';
import { message } from '../../src/components/FairyMessage';
import useFairyStore from '../../src/store/useFairyStore';

const defaultUserName = '林小满';
const defaultInviteCode = 'FAIRY520';
const INVITE_CODE_PATTERN = /^[A-Z0-9]{6,12}$/;

function getStringParam(value, fallback = '') {
  if (Array.isArray(value)) return value[0] || fallback;
  return typeof value === 'string' && value ? value : fallback;
}

export default function BindConfirmPage() {
  const params = useLocalSearchParams();
  const isReal = getApiMode() === 'real';
  const suppliedName = getStringParam(params.name, isReal ? '' : defaultUserName).trim();
  const inviteCode = getStringParam(params.code, isReal ? '' : defaultInviteCode).trim().toUpperCase();
  const validInviteCode = INVITE_CODE_PATTERN.test(inviteCode);
  const [submitting, setSubmitting] = useState(false);
  const submissionLock = useRef(false);
  const [pageError, setPageError] = useState(validInviteCode ? null : { code: 'INVALID_INVITE', message: '邀请码缺失或格式无效，请返回邀请页重新输入。' });
  const loadCoreData = useFairyStore((state) => state.loadCoreData);

  const confirmBind = async () => {
    if (!validInviteCode || submissionLock.current) return;
    submissionLock.current = true;
    setSubmitting(true);
    setPageError(null);
    const result = await bindCoupleByCode(inviteCode);
    if (!result.success || !result.data?.bound || !result.data?.couple?.id) {
      submissionLock.current = false;
      setSubmitting(false);
      const error = result.error || { code: 'UNCONFIRMED_BIND', message: '后端没有确认情侣关系已创建，请重试。' };
      setPageError(error);
      message.error(error.message);
      return;
    }
    const refreshResult = await loadCoreData({ force: true });
    setSubmitting(false);
    if (!refreshResult.success) {
      submissionLock.current = false;
      setPageError(refreshResult.error);
      message.error(refreshResult.error?.message || '情侣关系已由后端确认，但当前页面无法重新加载，请重新登录查看。');
      return;
    }
    message.success('情侣关系已由后端确认');
    router.replace('/(tabs)');
  };

  return (
    <FairyPage header={<FairyHeader showBack />} topSpace={0}>
      <Image source={require('../../assets/images/couple-bind-confirm-page/image1.png')} resizeMode="contain" style={styles.heroImage} />

      {pageError ? <FairyRequestState error={pageError} onRetry={validInviteCode ? confirmBind : () => router.replace('/account/invite')} compact /> : (
        <>
          <FairyBackgroundContainer source={require('../../assets/images/buttonImages/buttonBackground4.png')} style={styles.waitingButton}>
            <View style={styles.waitingStatusContent}><Ionicons name="hourglass-outline" size={16} color={colors.brown} /><Text style={styles.waitingStatusText}>{submitting ? '正在绑定' : '等待确认'}</Text></View>
          </FairyBackgroundContainer>

          <FairyBackgroundContainer source={require('../../assets/images/couple-bind-confirm-page/image2.png')} resizeMode="contain" style={styles.bindCard}>
            <View style={styles.bindCardContent}>
              <View style={styles.avatarFrame}>
                <View style={styles.avatarPlaceholder}><Ionicons name="person-outline" size={44} color={colors.textSoft} /></View>
                <Image source={require('../../assets/images/couple-bind-confirm-page/image3.png')} resizeMode="contain" style={styles.avatarFrameImage} />
              </View>
              <Text style={styles.userName} numberOfLines={2}>{suppliedName || '邀请人资料未提供'}</Text>
              <Text style={styles.identityHint}>{isReal ? '绑定前无法验证邀请人昵称或头像，请确认邀请码来源可信。' : 'Mock 演示邀请人'}</Text>
              <View style={styles.divider}><View style={styles.dividerLine} /><FairySvgIcon name="heart" size={20} color="#E9A09A" strokeWidth={1.5} style={{ marginLeft: 5, marginRight: 5 }} /><View style={styles.dividerLine} /></View>
              <FairyBackgroundContainer source={require('../../assets/images/couple-bind-confirm-page/image5.png')} style={styles.inviteCodeBg}>
                <View style={styles.inviteCodeRow}><Ionicons name="mail-outline" size={20} color="#A56E66" style={styles.inviteCodeIcon} /><Text style={styles.inviteCodeText} numberOfLines={1} adjustsFontSizeToFit minimumFontScale={0.72}>邀请码 {inviteCode}</Text></View>
              </FairyBackgroundContainer>
            </View>
          </FairyBackgroundContainer>

          <FairyBackgroundContainer source={require('../../assets/images/couple-bind-confirm-page/image4.png')} style={styles.storyCard}>
            <View><Text style={styles.storyText}>确认后将请求后端创建情侣关系</Text><Text style={styles.storyText}>只有后端返回真实关系记录才会显示成功</Text></View>
          </FairyBackgroundContainer>

          <View style={styles.actions}>
            <FairyButton title={submitting ? '绑定中…' : '确认绑定'} onPress={confirmBind} disabled={submitting} backgroundName="buttonBackground5" style={styles.receivedButton} textStyle={[styles.receivedButtonText, styles.confirmButtonText]} />
            <FairyButton title="不是 TA / 返回" onPress={() => router.back()} disabled={submitting} backgroundName="buttonBackground6" style={styles.receivedButton} textStyle={[styles.receivedButtonText, styles.cancelButtonText]} />
          </View>
        </>
      )}
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  heroImage: { width: '90%', height: 110, alignSelf: 'center' },
  waitingButton: { width: 120, height: 30, alignSelf: 'center' },
  waitingStatusContent: { width: '100%', height: '100%', flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8 },
  waitingStatusText: { fontSize: 14, fontWeight: '700', color: colors.brown },
  bindCard: { width: '100%', height: 370, alignSelf: 'center', paddingTop: 15 },
  bindCardContent: { width: '66%', maxWidth: 250, height: '90%', alignItems: 'center', justifyContent: 'center' },
  avatarFrame: { position: 'relative', width: '70%', aspectRatio: 1, alignItems: 'center', justifyContent: 'center' },
  avatarPlaceholder: { position: 'absolute', width: '68%', height: '68%', borderRadius: 999, zIndex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  avatarFrameImage: { position: 'absolute', width: '100%', height: '100%', zIndex: 2 },
  userName: { width: '100%', color: '#70433D', fontSize: 18, textAlign: 'center', marginBottom: 4 },
  identityHint: { color: colors.textSoft, fontSize: 10, lineHeight: 15, textAlign: 'center', paddingHorizontal: 6 },
  inviteCodeBg: { width: 220, height: 50, alignSelf: 'center' },
  inviteCodeRow: { width: '100%', height: '100%', flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingHorizontal: 14, transform: [{ translateY: -5 }] },
  inviteCodeIcon: { marginRight: 6, flexShrink: 0 },
  inviteCodeText: { color: '#A56E66', fontSize: 15, lineHeight: 20, flexShrink: 1 },
  storyCard: { width: '90%', height: 80, alignSelf: 'center' }, storyText: { textAlign: 'center', fontSize: 12, color: colors.textSoft },
  actions: { width: '100%', alignItems: 'center' },
  receivedButton: { width: '80%', height: 50, alignSelf: 'center', marginTop: 5, marginBottom: 5, paddingHorizontal: 12 },
  receivedButtonText: { fontSize: 16 }, confirmButtonText: { color: colors.white }, cancelButtonText: { color: colors.black },
  divider: { width: '100%', flexDirection: 'row', alignItems: 'center', gap: spacing.md, marginTop: 5, marginBottom: 5 },
  dividerLine: { flex: 1, height: 1, backgroundColor: '#99999930' },
});
