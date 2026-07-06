import { useState } from 'react';
import { Share, StyleSheet, Text, TextInput, View, Image } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import FairyBackgroundContainer from '../../src/components/FairyBackgroundContainer';
import FairyButton from '../../src/components/FairyButton';
import FairyHeader from '../../src/components/FairyHeader';
import FairyPage from '../../src/components/FairyPage';
import FairySvgIcon from '../../src/components/FairySvgIcon';
import { message } from '../../src/components/FairyMessage';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';

export default function CoupleInvitePage() {
  const [inviteCode] = useState('DT-4286');
  const [receivedInviteCode, setReceivedInviteCode] = useState('');

  const shareInvite = async () => {
    try {
      await Share.share({
        title: '独家童话邀请',
        message: `邀请你加入我的独家童话，邀请码：${inviteCode}`,
      });
    } catch (error) {
      message.error('当前浏览器不支持分享，请复制邀请码发送给 TA。');
    }
  };

  const viewReceivedInvite = () => {
    const code = receivedInviteCode.trim();
    if (!code) {
      message.info('请输入 TA 分享的邀请码。');
      return;
    }

    router.push(`/account/bind-confirm?code=${encodeURIComponent(code)}`);
  };

  return (
    <FairyPage
      topSpace={0}
      bottomSpace={10}
      header={
        <FairyHeader
          title="邀请 TA 加入"
          right={<Image source={require('../../assets/images/love2.png')} resizeMode="contain" style={{ width: 30, height: 30 }} />}
        />
      }
      // bottomSpace={20}
      // contentStyle={styles.pageContent}
    >
      <Image
        source={require('../../assets/images/couple-invite-page/image2.png')}
        resizeMode="contain"
        style={{ width: '100%', height: 120 }}
      />
      <View style={styles.inviteCardWrap}>
        <Image
          source={require('../../assets/images/couple-invite-page/image1.png')}
          resizeMode="cover"
          style={styles.inviteCardImage}
        />
        <View pointerEvents="none" style={styles.inviteCodeWrap}>
          <Text style={styles.inviteCode} numberOfLines={1} adjustsFontSizeToFit minimumFontScale={0.72}>
            {inviteCode}
          </Text>
        </View>
      </View>

      <FairyBackgroundContainer
        source={require('../../assets/images/buttonImages/buttonBackground4.png')}
        style={styles.waitingButton}
      >
        <View style={styles.waitingStatusContent}>
          <Ionicons name="hourglass-outline" size={16} color={colors.brown} />
          <Text style={styles.waitingStatusText}>等待绑定</Text>
        </View>
      </FairyBackgroundContainer>

      <View style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', marginBottom: 20, marginTop: 15 }}>
        <FairyButton
          title="复制邀请码"
          backgroundName="buttonBackground2"
          style={{ width: '47%', height: 45 }}
          imagePosition={'right'}
          rightContent={<Ionicons name="copy-outline" size={18} color={colors.white} />}
          onPress={() => message.success('邀请码已复制。')}
        />
        <FairyButton
          title="分享邀请"
          backgroundName="buttonBackground1"
          textStyle={{ color: colors.brown }}
          style={{ width: '47%', height: 45 }}
          imagePosition={'right'}
          rightContent={<Ionicons name="share-outline" size={18} color={colors.brown} />}
          onPress={shareInvite}
        />
      </View>

      <View style={styles.receivedInviteWrap}>
        <Image
          source={require('../../assets/images/couple-invite-page/image5.png')}
          resizeMode="stretch"
          style={styles.receivedInviteBg}
        />
        <View style={styles.receivedInviteContent}>
          <View style={styles.receivedTitleRow}>
            <FairySvgIcon name="fourPointStar" size={18} />
            <Text style={styles.receivedTitle}>我收到的邀请码</Text>
            <FairySvgIcon name="fourPointStar" size={18} />
          </View>
          <Text style={styles.receivedSubtitle}>输入 TA 分享给你的邀请码，查看并确认邀请</Text>
          <View style={styles.receivedActionRow}>
            <View style={styles.receivedInputBox}>
              <TextInput
                value={receivedInviteCode}
                onChangeText={setReceivedInviteCode}
                placeholder="请输入邀请码"
                placeholderTextColor="#C79B92"
                autoCapitalize="characters"
                style={styles.receivedInput}
              />
              <Ionicons name="copy-outline" size={18} color="#D58E88" style={styles.receivedInputIcon} />
            </View>
            <FairyButton
              title="查看邀请"
              backgroundName="buttonBackground2"
              style={styles.receivedButton}
              textStyle={styles.receivedButtonText}
              imagePosition="right"
              rightContent={<Ionicons name="search-outline" size={12} color={colors.white} />}
              onPress={viewReceivedInvite}
            />
          </View>
        </View>
      </View>

      <Image
        source={require('../../assets/images/couple-invite-page/image3.png')}
        resizeMode="contain"
        style={{ width: '100%', height: 150 }}
      />
      <Image
        source={require('../../assets/images/couple-invite-page/image4.png')}
        resizeMode="contain"
        style={{ width: '100%', height: 70 }}
      />

    </FairyPage>
  );
}

const styles = StyleSheet.create({
  card: { alignItems: 'center', backgroundColor: colors.cardPink, marginBottom: spacing.xl },
  title: { color: colors.textSoft, fontWeight: '700' },
  code: { color: colors.text, fontSize: 38, fontWeight: '900', letterSpacing: 2, marginTop: spacing.sm },
  text: { color: colors.textSoft, textAlign: 'center', marginTop: spacing.md, lineHeight: 21 },
  actions: { gap: spacing.md },
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
  receivedInviteWrap: {
    position: 'relative',
    width: '100%',
    aspectRatio: 1600 / 719,
    marginBottom: 18,
  },
  receivedInviteBg: {
    width: '100%',
    height: '100%',
  },
  receivedInviteContent: {
    ...StyleSheet.absoluteFillObject,
    // paddingHorizontal: '7%',
    padding: 25,
    alignItems: 'center',
  },
  receivedTitle: {
    color: colors.brown,
    fontSize: 16,
    fontWeight: '900',
  },
  receivedTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
    marginBottom: 4,
  },
  receivedSubtitle: {
    color: colors.textSoft,
    fontSize: 12,
    fontWeight: '700',
    textAlign: 'center',
    marginBottom: 14,
  },
  receivedActionRow: {
    width: '100%',
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  receivedInputBox: {
    flex: 1,
    height: 40,
    borderRadius: 18,
    borderWidth: 1.5,
    borderStyle: 'dashed',
    borderColor: '#DFA49E',
    backgroundColor: 'rgba(255, 255, 255, 0.38)',
    paddingHorizontal: 14,
    flexDirection: 'row',
    alignItems: 'center',
  },
  receivedInput: {
    flex: 1,
    minWidth: 0,
    color: colors.brown,
    fontSize: 12,
    fontWeight: '800',
    paddingVertical: 0,
    outlineStyle: 'none',
    outlineWidth: 0,
    borderWidth: 0,
  },
  receivedInputIcon: {
    flexShrink: 0,
    marginLeft: 8,
  },
  receivedButton: {
    width: 120,
    height: 40,
    paddingHorizontal: 12,
  },
  receivedButtonText: {
    color: colors.white,
    fontSize: 12,
  },
  inviteCardWrap: {
    position: 'relative',
    width: '100%',
    aspectRatio: 1.2,
    alignSelf: 'center',
  },
  inviteCardImage: {
    width: '100%',
    height: '100%',
  },
  inviteCodeWrap: {
    position: 'absolute',
    left: '23%',
    right: '23%',
    top: '39%',
    height: '18%',
    alignItems: 'center',
    justifyContent: 'center',
  },
  inviteCode: {
    color: colors.text,
    fontSize: 32,
    fontWeight: '900',
    letterSpacing: 3,
    textAlign: 'center',
    width: '100%',
  },
});
