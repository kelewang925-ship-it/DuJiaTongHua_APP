import { useState } from 'react';
import { StyleSheet, View, Image, Text } from 'react-native';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyInput from '../../src/components/FairyInput';
import FairyPage from '../../src/components/FairyPage';
import FairySvgIcon from '../../src/components/FairySvgIcon';
import RoundedDashedBorder from '../../src/components/RoundedDashedBorder';
import colors from '../../src/theme/colors';

export default function CoupleInfoPage() {
  const [myName, setMyName] = useState('林小满');
  const [partnerName, setPartnerName] = useState('陆星河');
  const [startDate, setStartDate] = useState('2025-03-23');
  const [relationNote, setRelationNote] = useState('');

  return (
    <FairyPage
      topSpace={0}
      header={<FairyHeader showBack />}
    >
      <View style={styles.titleBlock}>
        <View style={styles.cornerImageWrap}>
          <Image
            source={require('../../assets/images/couple-profile-setup-page/image1.png')}
            resizeMode="contain"
            style={styles.cornerImage}
          />
        </View>
        <Text style={styles.titleText}>情侣资料</Text>
        <Text style={styles.subtitleText}>先把故事主角写进书里</Text>
      </View>

      <View style={styles.profileCardsRow}>
        <View style={{ width: '48%' }}>
          <FairyCard
            shadow="modal"
            radius={20}
            padding={0}
            borderWidth={0}
            backgroundColor="transparent"
            shadowStyle={styles.profileCard}
            contentStyle={styles.profileCardSurface}
          >
            <Image
              source={require('../../assets/images/decoration/image1.png')}
              resizeMode="contain"
              style={[styles.profileDecoration, styles.profileDecorationTopLeft, { width: 70, height: 50 }]}
            />
            <Image
              source={require('../../assets/images/decoration/image2.png')}
              resizeMode="contain"
              style={[styles.profileDecoration, styles.profileDecorationBottomLeft, { width: 50, height: 100 }]}
            />
            <RoundedDashedBorder strokeColor="#f3ccc6" style={styles.profileCardDashedBorder}>
              <View style={styles.profileCardContent}>
                <View style={styles.profileNameRow}>
                  <FairySvgIcon name="fourPointStar" size={18} />
                  <Text style={styles.profileNameText}>我</Text>
                  <FairySvgIcon name="fourPointStar" size={18} />
                </View>
                <View style={styles.profileStarWrap}>

                </View>
                <FairyButton
                  title="更换头像"
                  backgroundName="buttonBackground7"
                  style={{ width: '100%', height: 40, }}
                  textStyle={{ color: colors.pencilBrown }}
                  imagePosition="left"
                  leftContent={<FairySvgIcon name="pencilEdit" size={18} color={colors.pencilBrown} strokeWidth={5} />}
                />
              </View>
            </RoundedDashedBorder>
          </FairyCard>
        </View>
        <View style={{ width: '48%' }}>
          <FairyCard
            shadow="modal"
            radius={20}
            padding={0}
            borderWidth={0}
            backgroundColor="transparent"
            shadowStyle={styles.profileCard}
            contentStyle={styles.profileCardSurface}
          >
            <Image
              source={require('../../assets/images/decoration/image3.png')}
              resizeMode="contain"
              style={[styles.profileDecoration, styles.profileDecorationTopRight, { width: 50, height: 50 }]}
            />
            <RoundedDashedBorder strokeColor="#f3ccc6" style={styles.profileCardDashedBorder}>
              <View style={styles.profileCardContent}>
                <View style={styles.profileNameRow}>
                  <FairySvgIcon name="fourPointStar" size={18} />
                  <Text style={styles.profileNameText}>TA</Text>
                  <FairySvgIcon name="fourPointStar" size={18} />
                </View>
                <View style={styles.profileStarWrap}>

                </View>
                <FairyButton
                  title="更换头像"
                  backgroundName="buttonBackground7"
                  style={{ width: '100%', height: 40, }}
                  textStyle={{ color: colors.pencilBrown }}
                  imagePosition="left"
                  leftContent={<FairySvgIcon name="pencilEdit" size={18} color={colors.pencilBrown} strokeWidth={5} />}
                />
              </View>
            </RoundedDashedBorder>
          </FairyCard>
        </View>
      </View>


      <FairyCard
        shadow="floating"
        radius={25}
        padding={0}
        borderWidth={0}
        backgroundColor="transparent"
        shadowStyle={[styles.dashedFormShadow, { position: 'relative', marginTop: 20 }]}
        contentStyle={styles.dashedFormBox}
      >
        <Image
          source={require('../../assets/images/decoration/image4.png')}
          resizeMode="contain"
          style={[styles.profileDecoration, { right: 20, top: 0 }, { width: 50, height: 50 }]}
        />
        <Image
          source={require('../../assets/images/decoration/image6.png')}
          resizeMode="contain"
          style={[styles.profileDecoration, { right: -10, bottom: 100 }, { width: 40, height: 70 }]}
        />
        <RoundedDashedBorder strokeColor="#f3ccc6" style={{ width: '100%', height: '100%', paddingLeft: 20, paddingRight: 20, paddingTop: 15, paddingBottom: 5 }}>
          <View style={{ width: '100%', height: '100%' }}>
            <FairyInput
              label={(
                <View style={styles.inputLabelContent}>
                  <Text style={styles.inputLabelText}>我的昵称</Text>
                  <FairySvgIcon name="heart" size={12} color="#E9A09A" strokeWidth={1.8} />
                </View>
              )}
              icon="person-outline"
              value={myName}
              onChangeText={setMyName}
            />
            <FairyInput
              label={(
                <View style={styles.inputLabelContent}>
                  <Text style={styles.inputLabelText}>伴侣昵称</Text>
                  <FairySvgIcon name="heart" size={12} color="#E9A09A" strokeWidth={1.8} />
                </View>
              )}
              icon="people-outline"
              value={partnerName}
              onChangeText={setPartnerName}
            />
            <FairyInput
              label={(
                <View style={styles.inputLabelContent}>
                  <Text style={styles.inputLabelText}>恋爱起始日</Text>
                  <FairySvgIcon name="heart" size={12} color="#E9A09A" strokeWidth={1.8} />
                </View>
              )}
              icon="calendar-outline"
              value={startDate}
              onChangeText={setStartDate}
            />
            <FairyInput
              label={(
                <View style={styles.inputLabelContent}>
                  <Text style={styles.inputLabelText}>关系备注</Text>
                  <FairySvgIcon name="heart" size={12} color="#E9A09A" strokeWidth={1.8} />
                </View>
              )}
              value={relationNote}
              onChangeText={(text) => setRelationNote(text.slice(0, 50))}
              maxLength={50}
              multiline
              inputWrapStyle={styles.relationNoteWrap}
              inputStyle={styles.relationNoteInput}
              helperInside
              helperStyle={styles.relationNoteCounter}
              helper={`${relationNote.length}/50`}
            />
          </View>
        </RoundedDashedBorder>
      </FairyCard>

      <FairyButton
        title="保存资料"
        backgroundName="buttonBackground3"
        style={styles.saveButton}
      />

      <View style={{ position: 'relative', }}>

        <Image
          source={require('../../assets/images/decoration/image5.png')}
          resizeMode="contain"
          style={[styles.profileDecoration, { left: 20 }, { width: 30, height: 30 }]}
        />

        <View style={styles.visibilityHint}>
          <FairySvgIcon name="lock" size={18} color={colors.pencilBrown} strokeWidth={1.8} />
          <Text style={styles.visibilityHintText}>仅对你们可见</Text>
        </View>
      </View>
    </FairyPage >
  );
}

const styles = StyleSheet.create({
  cornerImage: {
    width: 80,
    height: 80 / (1057 / 1020),
  },
  cornerImageWrap: {
    position: 'absolute',
    right: 0,
    top: -30,
    width: 80,
    height: 80 / (1057 / 1020),
    alignItems: 'flex-end',
    justifyContent: 'center',
    zIndex: 50,
  },
  titleBlock: {
    alignItems: 'center',
    marginBottom: 20,
    position: 'relative',
    zIndex: 10,
  },
  titleText: {
    color: colors.text,
    fontSize: 40,
    letterSpacing: 4,
    lineHeight: 52,
    textAlign: 'center',
  },
  subtitleText: {
    color: '#C6887F',
    fontSize: 22,
    letterSpacing: 5,
    lineHeight: 34,
    textAlign: 'center',
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
  relationNoteWrap: {
    minHeight: 50,
    alignItems: 'flex-start',
    paddingTop: 14,
    paddingBottom: 26,
  },
  relationNoteInput: {
    minHeight: 50,
    lineHeight: 22,
    paddingTop: 0,
  },
  relationNoteCounter: {
    color: colors.textSoft,
  },
  profileCardsRow: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    position: 'relative',
    zIndex: 0,
  },
  profileCard: {
    width: '100%',
  },
  profileCardSurface: {
    backgroundColor: '#FFF7F4',
    overflow: 'visible',
    position: 'relative',
    borderRadius: 20,
    padding: 8,
  },
  profileCardDashedBorder: {
    width: '100%',
    height: '100%',
    padding: 8,
  },
  profileCardContent: {
    width: '100%',
    height: '100%',
    padding: 20,
    justifyContent: 'space-between',
  },
  profileStarWrap: {
    alignItems: 'center',
    justifyContent: 'center',
    height: 100
  },
  profileNameRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
  },
  profileNameText: {
    textAlign: 'center',
    lineHeight: 22,
  },
  profileDecoration: {
    position: 'absolute',
    // width: 70,
    zIndex: 1,
  },
  profileDecorationTopLeft: {
    top: -20,
    left: 8,
  },
  profileDecorationBottomLeft: {
    left: -25,
    bottom: 5,
  },
  profileDecorationTopRight: {
    top: -20,
    right: -10,
  },
  saveButton: {
    width: "70%",
    height: 60,
    alignSelf: 'center',
    marginTop: 20,
  },
  visibilityHint: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    marginTop: 12,
  },
  visibilityHintText: {
    color: colors.pencilBrown,
    fontSize: 13,
    fontWeight: '700',
    lineHeight: 18,
  },
  dashedFormBox: {
    padding: 8,
    backgroundColor: '#fcf2e7',
    borderRadius: 25,
    overflow: 'visible',
  },
  dashedFormShadow: {
  },
});
