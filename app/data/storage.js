import { useMemo, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyPage from '@/components/FairyPage';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';

export default function StoragePage() {
  const router = useRouter();
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const [toast, setToast] = useState(null);

  const metrics = useMemo(() => {
    const photoRecords = records.filter((item) => item.type === '照片');
    const photoCount = photoRecords.reduce((sum, item) => {
      const count = Number(item.photoCount);
      return sum + (Number.isFinite(count) && count > 0 ? count : 0);
    }, 0);
    const diaryCount = records.filter((item) => item.type === '日记').length;

    return {
      diaryCount,
      photoCollectionCount: photoRecords.length,
      photoCount,
      creationCount: creations.length,
    };
  }, [creations.length, records]);

  const items = [
    {
      key: 'diaries',
      label: '日记记录',
      icon: 'book-outline',
      value: `${metrics.diaryCount} 篇`,
      detail: '来自当前账号已加载的真实日记记录',
    },
    {
      key: 'photos',
      label: '照片与相册',
      icon: 'images-outline',
      value: `${metrics.photoCount} 张`,
      detail: `${metrics.photoCollectionCount} 个照片集；未上报照片数量的记录按 0 计算`,
    },
    {
      key: 'creations',
      label: '童话工坊作品',
      icon: 'sparkles-outline',
      value: `${metrics.creationCount} 个`,
      detail: '来自当前账号已加载的漫画或视频作品记录',
      tone: 'gold',
    },
  ];

  const explainUnavailable = () => {
    setToast({
      tone: 'info',
      message: '当前尚未接入设备缓存统计与清理能力，不会模拟清理成功。',
    });
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="存储空间" right="容量待接入" />}
      topSpace={28}
      bottomSpace={60}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
    >
      <View style={styles.content}>
        <View style={styles.intro}>
          <Text style={styles.introTitle}>给每一份珍贵回忆留好位置</Text>
          <Text style={styles.introText}>这里仅展示当前账号已加载的真实内容数量，不估算或伪造 GB 容量。</Text>
        </View>

        <FairyCard style={styles.heroCard} padding={spacing.lg}>
          <View style={styles.heroImage}>
            <FairyImage name="exportCover" height={128} radius={20} framed={false} resizeMode="cover" />
          </View>
          <View style={styles.heroCopy}>
            <Text style={styles.heroTitle}>容量统计尚未接入</Text>
            <Text style={styles.heroText}>准确的设备缓存、文件体积和云端配额需要由原生文件系统与服务端共同返回。当前页面不会用内容数量推算存储容量。</Text>
          </View>
        </FairyCard>

        <Text style={styles.sectionTitle}>已加载内容</Text>
        <View style={styles.storageList}>
          {items.map((item) => (
            <FairyCard key={item.key} style={styles.storageCard}>
              <View style={[styles.itemIcon, item.tone === 'gold' && styles.goldIcon]}>
                <Ionicons name={item.icon} size={22} color={item.tone === 'gold' ? colors.gold : colors.accent} />
              </View>
              <View style={styles.itemCopy}>
                <Text style={styles.itemTitle}>{item.label}</Text>
                <Text style={styles.itemDetail}>{item.detail}</Text>
              </View>
              <Text style={styles.itemValue}>{item.value}</Text>
            </FairyCard>
          ))}
        </View>

        <FairyCard style={styles.noticeCard}>
          <Ionicons name="information-circle-outline" size={24} color={colors.primaryDeep} />
          <View style={styles.noticeCopy}>
            <Text style={styles.noticeTitle}>缓存管理暂不可用</Text>
            <Text style={styles.noticeText}>在真实缓存扫描和删除 API 接入前，本页不会显示虚构缓存大小，也不会仅修改界面状态后宣称清理完成。</Text>
          </View>
        </FairyCard>

        <View style={styles.actions}>
          <FairyButton title="缓存清理暂未开放" disabled onPress={explainUnavailable} leftContent={<Ionicons name="trash-outline" size={19} color={colors.white} />} />
          <FairyButton title="了解童话会员空间" variant="secondary" onPress={() => router.push('/membership')} />
        </View>
      </View>

      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 820 },
  intro: { alignItems: 'center', marginBottom: spacing.xl },
  introTitle: { color: colors.text, fontSize: 18, fontWeight: '900', textAlign: 'center' },
  introText: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.sm, textAlign: 'center' },
  heroCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.lg, backgroundColor: colors.cardPink, marginBottom: spacing.xl },
  heroImage: { width: 150 },
  heroCopy: { flex: 1, minWidth: 0 },
  heroTitle: { color: colors.text, fontSize: 20, fontWeight: '900' },
  heroText: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.sm },
  sectionTitle: { color: colors.text, fontSize: 18, fontWeight: '900', marginBottom: spacing.md },
  storageList: { gap: spacing.md },
  storageCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.lg },
  itemIcon: { width: 46, height: 46, borderRadius: 18, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  goldIcon: { backgroundColor: '#FFF5DF' },
  itemCopy: { flex: 1, minWidth: 0 },
  itemTitle: { color: colors.text, fontSize: 16, fontWeight: '900' },
  itemDetail: { color: colors.textSoft, marginTop: 3, lineHeight: 19 },
  itemValue: { color: colors.primaryDeep, fontSize: 17, fontWeight: '900' },
  noticeCard: { flexDirection: 'row', alignItems: 'flex-start', gap: spacing.md, marginTop: spacing.xl, backgroundColor: 'rgba(255,249,244,0.96)' },
  noticeCopy: { flex: 1 },
  noticeTitle: { color: colors.text, fontSize: 15, fontWeight: '900' },
  noticeText: { color: colors.textSoft, lineHeight: 20, marginTop: spacing.xs },
  actions: { gap: spacing.md, marginTop: spacing.xl },
});
