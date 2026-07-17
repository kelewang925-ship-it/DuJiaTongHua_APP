import { useCallback, useEffect, useState } from 'react';
import { StyleSheet, View, Image, Text } from 'react-native';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyInput from '../../src/components/FairyInput';
import FairyPage from '../../src/components/FairyPage';
import FairyRequestState from '../../src/components/FairyRequestState';
import FairySvgIcon from '../../src/components/FairySvgIcon';
import FairyToast from '../../src/components/FairyToast';
import RoundedDashedBorder from '../../src/components/RoundedDashedBorder';
import colors from '../../src/theme/colors';
import { getApiMode } from '../../src/api/client';
import { getCoupleInfo, updateCoupleInfo } from '../../src/api/coupleApi';
import { updateProfile } from '../../src/api/profileApi';
import useFairyStore from '../../src/store/useFairyStore';

export default function CoupleInfoPage() {
  const isReal = getApiMode() === 'real';
  const refreshCoreData = useFairyStore((state) => state.refreshCoreData);
  const [myName, setMyName] = useState(isReal ? '' : '林小满');
  const [partnerName, setPartnerName] = useState(isReal ? '' : '陆星河');
  const [startDate, setStartDate] = useState(isReal ? '' : '2025-03-23');
  const [relationNote, setRelationNote] = useState('');
  const [loading, setLoading] = useState(isReal);
  const [loadError, setLoadError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [toast, setToast] = useState(null);

  const loadProfile = useCallback(async () => {
    if (!isReal) return;
    setLoading(true);
    setLoadError(null);
    const result = await getCoupleInfo();
    setLoading(false);
    if (!result.success) {
      setLoadError(result.error);
      return;
    }
    setMyName(result.data?.user?.nickname || '童话收藏家');
    setPartnerName(result.data?.partner?.nickname || '等待 TA 加入');
    setStartDate(result.data?.couple?.startedAt || '');
  }, [isReal]);

  useEffect(() => { loadProfile(); }, [loadProfile]);

  const showAvatarUnavailable = () => {
    setToast({ tone: 'info', message: isReal ? 'Real 模式暂未开放头像上传。' : 'Mock 模式暂不保存头像文件。' });
  };

  const saveProfile = async () => {
    if (submitting) return;
    if (!myName.trim()) {
      setToast({ tone: 'error', message: '请填写你的昵称。' });
      return;
    }
    if (!/^\d{4}-\d{2}-\d{2}$/.test(startDate)) {
      setToast({ tone: 'error', message: '请按 YYYY-MM-DD 填写恋爱起始日。' });
      return;
    }
    if (!isReal) {
      setToast({ tone: 'success', message: '情侣资料已保存到 Mock 演示状态。' });
      return;
    }

    setSubmitting(true);
    const profileResult = await updateProfile({ nickname: myName });
    if (!profileResult.success) {
      setSubmitting(false);
      setToast({ tone: 'error', message: profileResult.error?.message || '个人资料保存失败。' });
      return;
    }
    const coupleResult = await updateCoupleInfo({ startedAt: startDate });
    if (!coupleResult.success) {
      setSubmitting(false);
      setToast({ tone: 'error', message: coupleResult.error?.message || '恋爱起始日保存失败。' });
      return;
    }
    const refreshResult = await refreshCoreData();
    setSubmitting(false);
    if (!refreshResult.success) {
      setToast({ tone: 'error', message: refreshResult.error?.message || '资料已保存，但刷新失败，请重新进入页面。' });
      return;
    }
    setToast({ tone: 'success', message: '情侣资料已经安全保存。' });
  };

  return (
    <FairyPage topSpace={0} header={<FairyHeader showBack />}>
      <View style={styles.titleBlock}>
        <View style={styles.cornerImageWrap}>
          <Image source={require('../../assets/images/couple-profile-setup-page/image1.png')} resizeMode="contain" style={styles.cornerImage} />
        </View>
        <Text style={styles.titleText}>情侣资料</Text>
        <Text style={styles.subtitleText}>先把故事主角写进书里</Text>
      </View>

      <FairyRequestState loading={loading} error={loadError} onRetry={loadProfile} />
      {!loading && !loadError ? (
        <>
          <View style={styles.profileCardsRow}>
            <View style={{ width: '48%' }}>
              <FairyCard shadow="modal" radius={20} padding={0} borderWidth={0} backgroundColor="transparent" shadowStyle={styles.profileCard} contentStyle={styles.profileCardSurface}>
                <Image source={require('../../assets/images/decoration/image1.png')} resizeMode="contain" style={[styles.profileDecoration, styles.profileDecorationTopLeft, { width: 70, height: 50 }]} />
                <Image source={require('../../assets/images/decoration/image2.png')} resizeMode="contain" style={[styles.profileDecoration, styles.profileDecorationBottomLeft, { width: 50, height: 100 }]} />
                <RoundedDashedBorder strokeColor="#f3ccc6" style={styles.profileCardDashedBorder}>
                  <View style={styles.profileCardContent}>
                    <View style={styles.profileNameRow}><FairySvgIcon name="fourPointStar" size={18} /><Text style={styles.profileNameText}>我</Text><FairySvgIcon name="fourPointStar" size={18} /></View>
                    <View style={styles.profileStarWrap}><Text style={styles.avatarLetter}>{myName.slice(0, 1) || '我'}</Text></View>
                    <FairyButton title="更换头像" onPress={showAvatarUnavailable} backgroundName="buttonBackground7" style={{ width: '100%', height: 40 }} textStyle={{ color: colors.pencilBrown }} imagePosition="left" leftContent={<FairySvgIcon name="pencilEdit" size={18} color={colors.pencilBrown} strokeWidth={5} />} />
                  </View>
                </RoundedDashedBorder>
              </FairyCard>
            </View>
            <View style={{ width: '48%' }}>
              <FairyCard shadow="modal" radius={20} padding={0} borderWidth={0} backgroundColor="transparent" shadowStyle={styles.profileCard} contentStyle={styles.profileCardSurface}>
                <Image source={require('../../assets/images/decoration/image3.png')} resizeMode="contain" style={[styles.profileDecoration, styles.profileDecorationTopRight, { width: 50, height: 50 }]} />
                <RoundedDashedBorder strokeColor="#f3ccc6" style={styles.profileCardDashedBorder}>
                  <View style={styles.profileCardContent}>
                    <View style={styles.profileNameRow}><FairySvgIcon name="fourPointStar" size={18} /><Text style={styles.profileNameText}>TA</Text><FairySvgIcon name="fourPointStar" size={18} /></View>
                    <View style={styles.profileStarWrap}><Text style={styles.avatarLetter}>{partnerName.slice(0, 1) || 'TA'}</Text></View>
                    <FairyButton title="伴侣头像只读" disabled backgroundName="buttonBackground7" style={{ width: '100%', height: 40 }} textStyle={{ color: colors.pencilBrown }} imagePosition="left" leftContent={<FairySvgIcon name="pencilEdit" size={18} color={colors.pencilBrown} strokeWidth={5} />} />
                  </View>
                </RoundedDashedBorder>
              </FairyCard>
            </View>
          </View>

          <FairyCard shadow="floating" radius={25} padding={0} borderWidth={0} backgroundColor="transparent" shadowStyle={[styles.dashedFormShadow, { position: 'relative', marginTop: 20 }]} contentStyle={styles.dashedFormBox}>
            <Image source={require('../../assets/images/decoration/image4.png')} resizeMode="contain" style={[styles.profileDecoration, { right: 20, top: 0 }, { width: 50, height: 50 }]} />
            <Image source={require('../../assets/images/decoration/image6.png')} resizeMode="contain" style={[styles.profileDecoration, { right: -10, bottom: 100 }, { width: 40, height: 70 }]} />
            <RoundedDashedBorder strokeColor="#f3ccc6" style={{ width: '100%', height: '100%', paddingLeft: 20, paddingRight: 20, paddingTop: 15, paddingBottom: 5 }}>
              <View style={{ width: '100%', height: '100%' }}>
                <FairyInput label={<View style={styles.inputLabelContent}><Text style={styles.inputLabelText}>我的昵称</Text><FairySvgIcon name="heart" size={12} color="#E9A09A" strokeWidth={1.8} /></View>} icon="person-outline" editable={!submitting} value={myName} onChangeText={setMyName} />
                <FairyInput label={<View style={styles.inputLabelContent}><Text style={styles.inputLabelText}>伴侣昵称</Text><FairySvgIcon name="heart" size={12} color="#E9A09A" strokeWidth={1.8} /></View>} icon="people-outline" editable={false} value={partnerName} helper="伴侣昵称由对方账号资料同步" />
                <FairyInput label={<View style={styles.inputLabelContent}><Text style={styles.inputLabelText}>恋爱起始日</Text><FairySvgIcon name="heart" size={12} color="#E9A09A" strokeWidth={1.8} /></View>} icon="calendar-outline" editable={!submitting} value={startDate} onChangeText={setStartDate} maxLength={10} placeholder="YYYY-MM-DD" />
                <FairyInput label={<View style={styles.inputLabelContent}><Text style={styles.inputLabelText}>关系备注</Text><FairySvgIcon name="heart" size={12} color="#E9A09A" strokeWidth={1.8} /></View>} editable={!isReal && !submitting} value={relationNote} onChangeText={(text) => setRelationNote(text.slice(0, 50))} maxLength={50} multiline inputWrapStyle={styles.relationNoteWrap} inputStyle={styles.relationNoteInput} helperInside helperStyle={styles.relationNoteCounter} helper={isReal ? 'Real 模式暂未开放关系备注保存' : `${relationNote.length}/50`} />
              </View>
            </RoundedDashedBorder>
          </FairyCard>

          <FairyButton title={submitting ? '正在保存…' : '保存资料'} disabled={submitting} onPress={saveProfile} backgroundName="buttonBackground3" style={styles.saveButton} />
          <View style={{ position: 'relative' }}>
            <Image source={require('../../assets/images/decoration/image5.png')} resizeMode="contain" style={[styles.profileDecoration, { left: 20 }, { width: 30, height: 30 }]} />
            <View style={styles.visibilityHint}><FairySvgIcon name="lock" size={18} color={colors.pencilBrown} strokeWidth={1.8} /><Text style={styles.visibilityHintText}>仅对你们可见</Text></View>
          </View>
        </>
      ) : null}
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  cornerImage: { width: 80, height: 80 / (1057 / 1020) },
  cornerImageWrap: { position: 'absolute', right: 0, top: -30, width: 80, height: 80 / (1057 / 1020), alignItems: 'flex-end', justifyContent: 'center', zIndex: 50 },
  titleBlock: { alignItems: 'center', marginBottom: 20, position: 'relative', zIndex: 10 },
  titleText: { color: colors.text, fontSize: 40, letterSpacing: 4, lineHeight: 52, textAlign: 'center' },
  subtitleText: { color: '#C6887F', fontSize: 22, letterSpacing: 5, lineHeight: 34, textAlign: 'center' },
  inputLabelContent: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  inputLabelText: { color: colors.text, fontSize: 15, fontWeight: '800' },
  relationNoteWrap: { minHeight: 50, alignItems: 'flex-start', paddingTop: 14, paddingBottom: 26 },
  relationNoteInput: { minHeight: 50, lineHeight: 22, paddingTop: 0 },
  relationNoteCounter: { color: colors.textSoft },
  profileCardsRow: { display: 'flex', flexDirection: 'row', justifyContent: 'space-between', position: 'relative', zIndex: 0 },
  profileCard: { width: '100%' },
  profileCardSurface: { backgroundColor: '#FFF7F4', overflow: 'visible', position: 'relative', borderRadius: 20, padding: 8 },
  profileCardDashedBorder: { width: '100%', height: '100%', padding: 8 },
  profileCardContent: { width: '100%', height: '100%', padding: 20, justifyContent: 'space-between' },
  profileStarWrap: { alignItems: 'center', justifyContent: 'center', height: 100 },
  avatarLetter: { color: colors.pencilBrown, fontSize: 34, fontWeight: '900' },
  profileNameRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 4 },
  profileNameText: { textAlign: 'center', lineHeight: 22 },
  profileDecoration: { position: 'absolute', zIndex: 1 },
  profileDecorationTopLeft: { top: -20, left: 8 },
  profileDecorationBottomLeft: { left: -25, bottom: 5 },
  profileDecorationTopRight: { top: -20, right: -10 },
  saveButton: { width: '70%', height: 60, alignSelf: 'center', marginTop: 20 },
  visibilityHint: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6, marginTop: 12 },
  visibilityHintText: { color: colors.pencilBrown, fontSize: 13, fontWeight: '700', lineHeight: 18 },
  dashedFormBox: { padding: 8, backgroundColor: '#fcf2e7', borderRadius: 25, overflow: 'visible' },
  dashedFormShadow: {},
});
