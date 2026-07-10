import { ScrollView, View, Text, StyleSheet, Pressable, Image } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyTag from '../../src/components/FairyTag';
import FairyRichTextViewer from '../../src/components/FairyRichTextViewer';
import useFairyStore from '../../src/store/useFairyStore';

import FairyPage from '../../src/components/FairyPage';
import FairyHeader from '../../src/components/FairyHeader';
import FairySvgIcon from '../../src/components/FairySvgIcon';
import FairyBackgroundContainer from '../../src/components/FairyBackgroundContainer';
import { formatDiaryDate } from '../../src/utils/date';
import Svg, { Path } from 'react-native-svg';

function StarDividerLine({ style }) {
  return (
    <Svg height={4} viewBox="0 0 100 4" fill="none" preserveAspectRatio="none" style={style}>
      <Path
        d="M2 2H98"
        stroke={colors.yellow}
        strokeWidth={1.6}
        strokeLinecap="round"
        strokeDasharray="6 4"
      />
    </Svg>
  );
}

export default function DiaryDetailPage() {
  const records = useFairyStore((state) => state.records);
  const diary = records.find((item) => item.type === '日记');

  if (!diary) {
    return (
      <ScrollView style={styles.page} contentContainerStyle={styles.content}>
        <FairyBackButton />
        <Text style={styles.title}>日记详情</Text>
        <Text style={styles.subtitle}>这里会收藏你们写下的每一页。</Text>
        <FairyEmptyState
          icon="book-outline"
          title="还没有日记"
          description="先写下一点点今天的故事，再回来查看这一页。"
          actionTitle="去写日记"
          onAction={() => router.replace('/diary/editor')}
        />
      </ScrollView>
    );
  }

  console.log(diary)

  return (
    <FairyPage
      scroll={false}
      topSpace={0}
      bottomSpace={0}
      contentStyle={styles.detailPageContent}
      header={
        <FairyHeader
          showBack
          backName="rollback4"
          title={<View style={styles.headerTitleRow}>
            <Text style={styles.headerTitle}>日记详情</Text>
            <FairySvgIcon name="softHeart" size={20} color="#F18D96" strokeWidth={2} />
          </View>}
          right={<FairyBackButton name="moreDetails1" />}
        />
      }
    >
      <View style={styles.detailLayout}>
        <View style={styles.detailTopModule}>
          <View style={{ position: 'relative', width: '100%', height: '100%' }}>
            <Image
              source={require('../../assets/images/diary-editor/image1-element-tape-top-left.png')}
              resizeMode="contain"
              style={[
                styles.profileDecoration,
                {
                  left: '3%',
                  top: '-5%',
                  width: '20%',
                  height: '10%'
                },
              ]}
            />
            <Image
              source={require('../../assets/images/diary-editor/image1-element-bookmark-top-right.png')}
              resizeMode="contain"
              style={[
                styles.profileDecoration,
                {
                  right: '8%',
                  width: '8%',
                  height: '8%'
                },
              ]}
            />
            <FairyBackgroundContainer
              source={require('../../assets/design-assets/diary-detail/image1.png')}
              style={{}}
            >
              <View style={{ width: '80%', height: '90%' }}>
                <ScrollView showsVerticalScrollIndicator={false} style={{ flex: 1 }} >
                  <View>
                    <Text style={styles.diaryTitle}>{diary.title || '今天的小小童话'}</Text>
                  </View>
                  <View style={styles.dateRow}>
                    <Ionicons name="calendar-outline" size={15} color={colors.textSoft} />
                    <Text style={styles.date}>{formatDiaryDate(diary)}</Text>
                  </View>
                  <View style={styles.tags}>
                    {(diary.tags || ['日记']).map((tag) => <FairyTag key={tag}>{tag}</FairyTag>)}
                  </View>
                  <View style={styles.starDivider}>
                    <StarDividerLine style={styles.starDividerLine} />
                    <View style={styles.starDividerIcon}>
                      <Ionicons name="star-outline" size={22} color={colors.yellow} />
                    </View>
                    <StarDividerLine style={styles.starDividerLine} />
                  </View>
                  {/* {diary.mood ? (
                    <View style={styles.moodPill}>
                      <Ionicons name="heart-outline" size={14} color={colors.primaryDeep} />
                      <Text style={styles.moodText}>{diary.mood}</Text>
                    </View>
                  ) : null} */}
                  <FairyRichTextViewer
                    html={diary.content}
                    fallback="今天的故事，还没有完全写完。"
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
              <FairyButton
                title="编辑"
                backgroundName="buttonBackground8"
                style={{ height: 55 }}
                textStyle={{ color: '#6E3D34', fontSize: 16, lineHeight: 22, }}
              />
            </View>
            <View style={styles.detailBottomCenterModule}>
              <FairyButton
                title="文本转漫画"
                backgroundName="buttonBackground9"
                style={{ height: 55 }}
                textStyle={{ color: '#6E3D34', fontSize: 16, lineHeight: 22, }}
              />
            </View>
            <View style={styles.detailBottomSideModule}>
              <FairyButton
                title="分享"
                backgroundName="buttonBackground10"
                style={{ height: 55 }}
                textStyle={{ color: '#6E3D34', fontSize: 16, lineHeight: 22, }}
              />
            </View>
          </View>
          <Svg width={180} height={20} viewBox="0 0 330 32" fill="none" style={{ width: 180, height: 20, flexShrink: 0, alignSelf: 'center', marginTop: 5, marginBottom: 20 }}>
            <Path
              d="M0 16H92"
              stroke="#DDB276"
              strokeWidth={2}
              strokeLinecap="round"
            />
            <Path
              d="M92 16C98 16 99 20 104 20C109 20 109 12 115 12C121 12 121 20 126 20C131 20 132 16 138 16"
              stroke="#DDB276"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <Path
              d="M165 25C158 18 149 12 149 5.8C149 2.5 151.4 0.4 154.6 0.4C158.1 0.4 160.8 2.8 165 7.8C169.2 2.8 171.9 0.4 175.4 0.4C178.6 0.4 181 2.5 181 5.8C181 12 172 18 165 25Z"
              stroke="#F18D96"
              strokeWidth={2.6}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <Path
              d="M192 16C198 16 199 20 204 20C209 20 209 12 215 12C221 12 221 20 226 20C231 20 232 16 238 16"
              stroke="#DDB276"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <Path
              d="M238 16H330"
              stroke="#DDB276"
              strokeWidth={2}
              strokeLinecap="round"
            />
          </Svg>
        </View>
      </View>

    </FairyPage>
    // <ScrollView style={styles.page} contentContainerStyle={styles.content}>
    //   <FairyBackButton />
    //   <Text style={styles.title}>日记详情</Text>
    //   <Text style={styles.subtitle}>这一页，是你们童话里被收藏的一天。</Text>

    //   <FairyCard style={styles.coverCard}>
    //     <View style={styles.coverIcon}>
    //       <Ionicons name={diary.icon || 'book-outline'} size={30} color={colors.gold} />
    //     </View>
    //     <Text style={styles.diaryTitle}>{diary.title || '今天的小小童话'}</Text>
    //     <Text style={styles.date}>{diary.date || '刚刚'}</Text>
    //     <View style={styles.tags}>
    //       {(diary.tags || ['日记']).map((tag) => <FairyTag key={tag}>{tag}</FairyTag>)}
    //     </View>
    //     {diary.mood ? (
    //       <View style={styles.moodPill}>
    //         <Ionicons name="heart-outline" size={14} color={colors.primaryDeep} />
    //         <Text style={styles.moodText}>{diary.mood}</Text>
    //       </View>
    //     ) : null}
    //   </FairyCard>

    //   <FairyCard style={styles.bodyCard}>
    //     <Text style={styles.sectionTitle}>正文</Text>
    //     <FairyRichTextViewer
    //       html={diary.content}
    //       fallback="今天的故事，还没有完全写完。"
    //       style={styles.bodyText}
    //     />
    //   </FairyCard>

    //   <FairyCard style={styles.magicCard}>
    //     <View style={styles.magicHeader}>
    //       <Ionicons name="sparkles-outline" size={22} color={colors.accent} />
    //       <Text style={styles.sectionTitle}>把这一页变成漫画</Text>
    //     </View>
    //     <Text style={styles.magicText}>AI 可以根据这篇日记生成专属童话漫画，并同步到童话工坊。</Text>
    //     <Pressable style={styles.inlineAction} onPress={() => router.push('/ai/text-to-comic')}>
    //       <Text style={styles.inlineActionText}>去生成漫画</Text>
    //       <Ionicons name="chevron-forward" size={16} color={colors.primaryDeep} />
    //     </Pressable>
    //   </FairyCard>

    //   <FairyButton title="继续写一页" onPress={() => router.push('/diary/editor')} />
    // </ScrollView>
  );
}

const styles = StyleSheet.create({
  headerTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
  },
  headerTitle: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '900',
    lineHeight: 24,
    textAlign: 'center',
  },
  detailPageContent: {
    flex: 1,
  },
  detailLayout: {
    flex: 1,
    width: '100%',
  },
  detailTopModule: {
    paddingTop: 10,
    paddingBottom: 20,
    flex: 8,
  },
  detailBottomModule: {
    flex: 1.5,
    justifyContent: 'center',
  },
  detailButtonRow: {
    flexDirection: 'row',
    alignItems: 'center',
    columnGap: 8,
    marginBottom: 10
  },
  detailBottomSideModule: {
    flex: 3,
  },
  detailBottomCenterModule: {
    flex: 4,
  },
  profileDecoration: {
    position: 'absolute',
    zIndex: 1,
  },
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  // title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  coverCard: { alignItems: 'center', backgroundColor: colors.cardPink, marginBottom: 16 },
  coverIcon: { width: 64, height: 64, borderRadius: 24, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 14 },
  diaryTitle: { color: colors.text, fontSize: 22, fontWeight: '900', textAlign: 'left', lineHeight: 40 },
  dateRow: { flexDirection: 'row', alignItems: 'center', gap: 5, marginTop: 8 },
  date: { color: colors.textSoft },
  tags: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 14 },
  starDivider: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    marginTop: 10,
    // marginBottom: 12,
  },
  starDividerLine: {
    flex: 4,
  },
  starDividerIcon: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  moodPill: { flexDirection: 'row', alignItems: 'center', gap: 5, marginTop: 14, paddingHorizontal: 12, paddingVertical: 7, borderRadius: 18, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border },
  moodText: { color: colors.primaryDeep, fontSize: 12, fontWeight: '800' },
  bodyCard: { marginBottom: 16 },
  sectionTitle: { color: colors.text, fontSize: 17, fontWeight: '800' },
  bodyText: { color: colors.text, fontSize: 16, lineHeight: 27 },
  magicCard: { marginBottom: 22 },
  magicHeader: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 10 },
  magicText: { color: colors.textSoft, lineHeight: 22 },
  inlineAction: { marginTop: 14, flexDirection: 'row', alignItems: 'center', gap: 4 },
  inlineActionText: { color: colors.primaryDeep, fontWeight: '800' },
});
