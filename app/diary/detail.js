import { Image, ScrollView, StyleSheet, Text, View } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import Svg, { Path } from 'react-native-svg';

import FairyBackButton from '../../src/components/FairyBackButton';
import FairyBackgroundContainer from '../../src/components/FairyBackgroundContainer';
import FairyButton from '../../src/components/FairyButton';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyHeader from '../../src/components/FairyHeader';
import FairyPage from '../../src/components/FairyPage';
import FairyRichTextViewer from '../../src/components/FairyRichTextViewer';
import FairySvgIcon from '../../src/components/FairySvgIcon';
import FairyTag from '../../src/components/FairyTag';
import useFairyStore from '../../src/store/useFairyStore';
import colors from '../../src/theme/colors';
import { formatDiaryDate } from '../../src/utils/date';

function StarDividerLine({ style }) {
  return (
    <Svg height={4} viewBox="0 0 100 4" fill="none" preserveAspectRatio="none" style={style}>
      <Path d="M2 2H98" stroke={colors.yellow} strokeWidth={1.6} strokeLinecap="round" strokeDasharray="6 4" />
    </Svg>
  );
}

export default function DiaryDetailPage() {
  const { id } = useLocalSearchParams();
  const diaryId = Array.isArray(id) ? id[0] : id;
  const records = useFairyStore((state) => state.records) || [];
  const diary = records.find((item) => item.id === diaryId && item.type === '日记');

  if (!diary) {
    return (
      <FairyPage
        backgroundName="creamPaper"
        header={<FairyHeader showBack title="日记详情" />}
        topSpace={28}
        bottomSpace={64}
      >
        <FairyEmptyState
          icon="book-outline"
          title="没有找到这篇日记"
          description="这篇日记可能已被删除，或当前链接已经失效。"
          actionTitle="返回日记列表"
          onAction={() => router.replace('/(tabs)')}
        />
      </FairyPage>
    );
  }

  const openEditor = () => router.push({ pathname: '/diary/editor', params: { id: diary.id } });
  const openComic = () => router.push({ pathname: '/ai/text-to-comic', params: { id: diary.id } });
  const openShare = () => router.push({ pathname: '/share-preview', params: { id: diary.id, type: 'diary' } });

  return (
    <FairyPage
      scroll={false}
      topSpace={0}
      bottomSpace={0}
      contentStyle={styles.detailPageContent}
      header={(
        <FairyHeader
          showBack
          backName="rollback4"
          title={(
            <View style={styles.headerTitleRow}>
              <Text style={styles.headerTitle}>日记详情</Text>
              <FairySvgIcon name="softHeart" size={20} color="#F18D96" strokeWidth={2} />
            </View>
          )}
          right={<FairyBackButton name="moreDetails1" />}
        />
      )}
    >
      <View style={styles.detailLayout}>
        <View style={styles.detailTopModule}>
          <View style={styles.canvas}>
            <Image
              source={require('../../assets/images/diary-editor/image1-element-tape-top-left.png')}
              resizeMode="contain"
              style={[styles.profileDecoration, styles.tapeDecoration]}
            />
            <Image
              source={require('../../assets/images/diary-editor/image1-element-bookmark-top-right.png')}
              resizeMode="contain"
              style={[styles.profileDecoration, styles.bookmarkDecoration]}
            />
            <FairyBackgroundContainer source={require('../../assets/design-assets/diary-detail/image1.png')}>
              <View style={styles.paperContent}>
                <ScrollView showsVerticalScrollIndicator={false} style={styles.scrollContent}>
                  <Text style={styles.diaryTitle}>{diary.title?.trim() || '未命名日记'}</Text>
                  <View style={styles.dateRow}>
                    <Ionicons name="calendar-outline" size={15} color={colors.textSoft} />
                    <Text style={styles.date}>{formatDiaryDate(diary)}</Text>
                  </View>
                  {Array.isArray(diary.tags) && diary.tags.length ? (
                    <View style={styles.tags}>
                      {diary.tags.map((tag) => <FairyTag key={tag}>{tag}</FairyTag>)}
                    </View>
                  ) : null}
                  <View style={styles.starDivider}>
                    <StarDividerLine style={styles.starDividerLine} />
                    <View style={styles.starDividerIcon}>
                      <Ionicons name="star-outline" size={22} color={colors.yellow} />
                    </View>
                    <StarDividerLine style={styles.starDividerLine} />
                  </View>
                  <FairyRichTextViewer
                    html={diary.content}
                    fallback="这篇日记还没有正文。"
                    style={styles.bodyText}
                  />
                </ScrollView>
              </View>
            </FairyBackgroundContainer>
          </View>
        </View>

        <View style={styles.detailBottomModule}>
          <View style={styles.detailButtonRow}>
            <View style={styles.detailBottomSideModule}>
              <FairyButton title="编辑" backgroundName="buttonBackground8" style={styles.actionButton} textStyle={styles.actionText} onPress={openEditor} />
            </View>
            <View style={styles.detailBottomCenterModule}>
              <FairyButton title="文本转漫画" backgroundName="buttonBackground9" style={styles.actionButton} textStyle={styles.actionText} onPress={openComic} />
            </View>
            <View style={styles.detailBottomSideModule}>
              <FairyButton title="分享" backgroundName="buttonBackground10" style={styles.actionButton} textStyle={styles.actionText} onPress={openShare} />
            </View>
          </View>
          <Svg width={180} height={20} viewBox="0 0 330 32" fill="none" style={styles.footerDivider}>
            <Path d="M0 16H138" stroke="#DDB276" strokeWidth={2} strokeLinecap="round" />
            <Path d="M165 25C158 18 149 12 149 5.8C149 2.5 151.4 0.4 154.6 0.4C158.1 0.4 160.8 2.8 165 7.8C169.2 2.8 171.9 0.4 175.4 0.4C178.6 0.4 181 2.5 181 5.8C181 12 172 18 165 25Z" stroke="#F18D96" strokeWidth={2.6} strokeLinecap="round" strokeLinejoin="round" />
            <Path d="M192 16H330" stroke="#DDB276" strokeWidth={2} strokeLinecap="round" />
          </Svg>
        </View>
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  headerTitleRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6 },
  headerTitle: { color: colors.text, fontSize: 18, fontWeight: '900', lineHeight: 24, textAlign: 'center' },
  detailPageContent: { flex: 1 },
  detailLayout: { flex: 1, width: '100%' },
  detailTopModule: { paddingTop: 10, paddingBottom: 20, flex: 8 },
  detailBottomModule: { flex: 1.5, justifyContent: 'center' },
  canvas: { position: 'relative', width: '100%', height: '100%' },
  profileDecoration: { position: 'absolute', zIndex: 1 },
  tapeDecoration: { left: '3%', top: '-5%', width: '20%', height: '10%' },
  bookmarkDecoration: { right: '8%', width: '8%', height: '8%' },
  paperContent: { width: '80%', height: '90%' },
  scrollContent: { flex: 1 },
  detailButtonRow: { flexDirection: 'row', alignItems: 'center', columnGap: 8, marginBottom: 10 },
  detailBottomSideModule: { flex: 3 },
  detailBottomCenterModule: { flex: 4 },
  actionButton: { height: 55 },
  actionText: { color: '#6E3D34', fontSize: 16, lineHeight: 22 },
  footerDivider: { width: 180, height: 20, flexShrink: 0, alignSelf: 'center', marginTop: 5, marginBottom: 20 },
  diaryTitle: { color: colors.text, fontSize: 22, fontWeight: '900', textAlign: 'left', lineHeight: 40 },
  dateRow: { flexDirection: 'row', alignItems: 'center', gap: 5, marginTop: 8 },
  date: { color: colors.textSoft },
  tags: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 14 },
  starDivider: { flexDirection: 'row', alignItems: 'center', gap: 10, marginVertical: 22 },
  starDividerLine: { flex: 1 },
  starDividerIcon: { alignItems: 'center', justifyContent: 'center' },
  bodyText: { color: colors.text, fontSize: 16, lineHeight: 28 },
});