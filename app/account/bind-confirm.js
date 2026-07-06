import { Image, StyleSheet, Text, View } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import FairyBackgroundContainer from '../../src/components/FairyBackgroundContainer';
import FairyButton from '../../src/components/FairyButton';
import FairyHeader from '../../src/components/FairyHeader';
import FairyPage from '../../src/components/FairyPage';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';

const defaultUserName = '林小满';
const defaultInviteCode = 'DT-4286';

function getStringParam(value, fallback) {
  if (Array.isArray(value)) {
    return value[0] || fallback;
  }

  return typeof value === 'string' && value ? value : fallback;
}

export default function BindConfirmPage() {
  const params = useLocalSearchParams();
  const userName = getStringParam(params.name, defaultUserName);
  const inviteCode = getStringParam(params.code, defaultInviteCode);

  return (
    <FairyPage
      header={<FairyHeader showBack />}
      topSpace={0}
    >
      <Image
        source={require('../../assets/images/couple-bind-confirm-page/image1.png')}
        resizeMode="contain"
        style={styles.heroImage}
      />

      <FairyBackgroundContainer
        source={require('../../assets/images/buttonImages/buttonBackground4.png')}
        style={styles.waitingButton}
      >
        <View style={styles.waitingStatusContent}>
          <Ionicons name="hourglass-outline" size={16} color={colors.brown} />
          <Text style={styles.waitingStatusText}>等待确认</Text>
        </View>
      </FairyBackgroundContainer>

      <FairyBackgroundContainer
        source={require('../../assets/images/couple-bind-confirm-page/image2.png')}
        resizeMode="contain"
        style={styles.bindCard}
      >
        <View style={styles.bindCardContent}>
          <View style={styles.avatarFrame}>
            <Image
              source={require('../../assets/images/avatar/man.png')}
              resizeMode="cover"
              style={styles.avatarImage}
            />
            <Image
              source={require('../../assets/images/couple-bind-confirm-page/image3.png')}
              resizeMode="contain"
              style={styles.avatarFrameImage}
            />
          </View>

          <Text style={styles.userName} numberOfLines={1} adjustsFontSizeToFit minimumFontScale={0.72}>
            {userName}
          </Text>

          <View style={styles.divider}>
            <View style={styles.dividerLine} />
            <Image
              source={require('../../assets/images/icons/public/little-heart.png')}
              resizeMode="contain"
              style={styles.dividerHeart}
            />
            <View style={styles.dividerLine} />
          </View>

          <FairyBackgroundContainer
            source={require('../../assets/images/couple-bind-confirm-page/image5.png')}
            style={styles.inviteCodeBg}
          >
            <View style={styles.inviteCodeRow}>
              <Ionicons name="mail-outline" size={20} color="#A56E66" style={styles.inviteCodeIcon} />
              <Text style={styles.inviteCodeText} numberOfLines={1} adjustsFontSizeToFit minimumFontScale={0.72}>
                来自邀请码 {inviteCode}
              </Text>
            </View>
          </FairyBackgroundContainer>
        </View>
      </FairyBackgroundContainer>

      <FairyBackgroundContainer
        source={require('../../assets/images/couple-bind-confirm-page/image4.png')}
        style={styles.storyCard}
      >
        <View>
          <Text style={styles.storyText}>绑定后，你们将拥有</Text>
          <Text style={styles.storyText}>只属于两个人的故事空间</Text>
        </View>
      </FairyBackgroundContainer>

      <View style={styles.actions}>
        <FairyButton
          title="确认绑定"
          backgroundName="buttonBackground5"
          style={styles.receivedButton}
          textStyle={[styles.receivedButtonText, styles.confirmButtonText]}
        />
        <FairyButton
          title="不是TA / 返回"
          backgroundName="buttonBackground6"
          style={styles.receivedButton}
          textStyle={[styles.receivedButtonText, styles.cancelButtonText]}
        />
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  heroImage: {
    width: '90%',
    height: 110,
    alignSelf: 'center',
  },
  waitingButton: {
    width: 120,
    height: 30,
    alignSelf: 'center',
  },
  waitingStatusContent: {
    width: '100%',
    height: '100%',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  waitingStatusText: {
    fontSize: 14,
    fontWeight: '700',
    color: colors.brown,
  },
  bindCard: {
    width: '100%',
    height: 340,
    alignSelf: 'center',
    paddingTop: 15
  },
  bindCardContent: {
    width: '60%',
    maxWidth: 220,
    height: '86%',
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarFrame: {
    position: 'relative',
    width: '80%',
    aspectRatio: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarImage: {
    position: 'absolute',
    width: '72%',
    height: '72%',
    borderRadius: 999,
    zIndex: 1,
  },
  avatarFrameImage: {
    position: 'absolute',
    width: '100%',
    height: '100%',
    zIndex: 2,
  },
  userName: {
    width: '100%',
    color: '#70433D',
    fontSize: 20,
    textAlign: 'center',
    marginBottom: 6,
  },
  inviteCodeBg: {
    width: 220,
    height: 50,
    alignSelf: 'center',
  },
  inviteCodeRow: {
    width: '100%',
    height: '100%',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 14,
    transform: [{ translateY: -5 }],
  },
  inviteCodeIcon: {
    marginRight: 6,
    flexShrink: 0,
  },
  inviteCodeText: {
    color: '#A56E66',
    fontSize: 15,
    lineHeight: 20,
    flexShrink: 1,
  },
  storyCard: {
    width: '90%',
    height: 80,
    alignSelf: 'center',
  },
  storyText: {
    textAlign: 'center',
  },
  actions: {
    width: '100%',
  },
  receivedButton: {
    width: '80%',
    height: 50,
    alignSelf: 'center',
    marginTop: 5,
    marginBottom: 5,
    paddingHorizontal: 12,
  },
  receivedButtonText: {
    fontSize: 16,
  },
  confirmButtonText: {
    color: colors.white,
  },
  cancelButtonText: {
    color: colors.black,
  },
  divider: {
    width: '100%',
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
});
