import { useMemo, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyPage from '@/components/FairyPage';
import FairyDialog from '@/components/FairyDialog';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';

const totalStorage = 10;

export default function StoragePage() {
  const router = useRouter();
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const [cacheSize, setCacheSize] = useState(0.42);
  const [selectedKeys, setSelectedKeys] = useState(['cache']);
  const [message, setMessage] = useState('');
  const [dialogVisible, setDialogVisible] = useState(false);
  const [toastVisible, setToastVisible] = useState(false);

  const storageItems = useMemo(() => {
    const photoCount = records
      .filter((item) => item.type === '照片')
      .reduce((sum, item) => sum + (item.photoCount || 3), 0);
    const aiCount = creations.length;

    return [
      {
        key: 'photos',
        label: '照片与相册',
        icon: 'images-outline',
        size: Math.max(1.2, photoCount * 0.18),
        detail: `${photoCount} 张照片 · 原图与缩略图`,
      },
      {
        key: 'ai',
        label: '童话工坊作品',
        icon: 'sparkles-outline',
        size: Math.max(0.8, aiCount * 0.26),
        detail: `${aiCount} 个漫画/视频草稿`,
        tone: 'gold',
      },
      {
        key: 'exports',
        label: '导出回忆册',
        icon: 'document-text-outline',
        size: 0.36,
        detail: 'PDF 预览与旧版本导出',
      },
      {
        key: 'cache',
        label: '临时纸屑缓存',
        icon: 'file-tray-outline',
        size: cacheSize,
        detail: '可安全清理的本地 mock 缓存',
      },
    ];
  }, [cacheSize, creations.length, records]);

  const usedStorage = storageItems.reduce((sum, item) => sum + item.size, 0);
  const percent = Math.min(100, Math.round((usedStorage / totalStorage) * 100));
  const cleanableSize = storageItems
    .filter((item) => selectedKeys.includes(item.key) && item.key === 'cache')
    .reduce((sum, item) => sum + item.size, 0);

  const toggleSelected = (key) => {
    setSelectedKeys((keys) => (keys.includes(key) ? keys.filter((item) => item !== key) : [...keys, key]));
    setMessage('');
  };

  const cleanSelected = () => {
    setDialogVisible(false);
    if (!selectedKeys.includes('cache') || cacheSize === 0) {
      setMessage('当前选中的章节没有可清理内容，回忆仍好好放着。');
      setToastVisible(true);
      return;
    }
    setCacheSize(0);
    setSelectedKeys((keys) => keys.filter((key) => key !== 'cache'));
    setMessage('临时纸屑已经扫进小纸篓，珍贵回忆没有被移动。');
    setToastVisible(true);
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="存储空间" right={`${usedStorage.toFixed(1)}GB`} />}
      topSpace={28}
      bottomSpace={60}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
    >
      <View style={styles.content}>
        <View style={styles.intro}>
          <Text style={styles.introTitle}>给每一份珍贵回忆留好位置</Text>
          <Text style={styles.introText}>查看照片、童话工坊作品、导出文件和临时缓存占用。</Text>
        </View>

        <FairyCard style={styles.heroCard} padding={spacing.lg}>
          <View style={styles.heroTop}>
            <View style={styles.heroImage}>
              <FairyImage name="exportCover" height={108} radius={20} framed={false} resizeMode="cover" />
            </View>
            <View style={styles.heroCopy}>
              <Text style={styles.heroTitle}>已使用 {usedStorage.toFixed(1)} GB / {totalStorage} GB</Text>
              <Text style={styles.heroText}>回忆还有很多位置，当前占用为本地模拟估算。</Text>
            </View>
          </View>
          <View style={styles.progressTrack}>
            <View style={[styles.progressFill, { width: `${percent}%` }]} />
          </View>
          <View style={styles.progressMeta}>
            <Text style={styles.progressText}>{percent}% 已使用</Text>
            <Text style={styles.progressText}>剩余 {(totalStorage - usedStorage).toFixed(1)} GB</Text>
          </View>
          <View style={styles.legendRow}>
            {storageItems.map((item) => <View key={item.key} style={styles.legendItem}><View style={[styles.legendDot, item.tone === 'gold' && styles.legendDotGold, item.key === 'cache' && styles.legendDotCache]} /><Text style={styles.legendText}>{item.label} {item.size.toFixed(1)}GB</Text></View>)}
          </View>
        </FairyCard>

      <Text style={styles.sectionTitle}>空间分布</Text>
      <View style={styles.storageList}>
        {storageItems.map((item) => {
          const selected = selectedKeys.includes(item.key);
          const canClean = item.key === 'cache';
          return (
            <FairyCard key={item.key} onPress={() => toggleSelected(item.key)} style={[styles.storageCard, selected && styles.storageCardActive]} accessibilityRole="button" accessibilityState={{ selected }}>
                <View style={[styles.itemIcon, item.tone === 'gold' && styles.goldIcon]}>
                  <Ionicons name={item.icon} size={22} color={item.tone === 'gold' ? colors.gold : colors.accent} />
                </View>
                <View style={styles.itemCopy}>
                  <Text style={styles.itemTitle}>{item.label}</Text>
                  <Text style={styles.itemDetail}>{item.detail}</Text>
                  <View style={styles.itemBar}>
                    <View style={[styles.itemBarFill, { width: `${Math.min(100, (item.size / usedStorage) * 100)}%` }]} />
                  </View>
                </View>
                <View style={styles.itemRight}>
                  <Text style={styles.itemSize}>{item.size.toFixed(2)}GB</Text>
                  <View style={[styles.checkDot, selected && styles.checkDotActive]}>
                    {selected ? <Ionicons name="checkmark" size={13} color={colors.white} /> : null}
                  </View>
                  {!canClean ? <Text style={styles.keepText}>保留</Text> : null}
                </View>
            </FairyCard>
          );
        })}
      </View>

      <FairyCard style={styles.cleanCard}>
        <Text style={styles.cleanTitle}>本次可清理</Text>
        <Text style={styles.cleanSize}>{cleanableSize.toFixed(2)}GB</Text>
        <Text style={styles.cleanText}>只会清理临时缓存，不会动到日记、照片、漫画或导出文件。</Text>
      </FairyCard>

      {message ? (
        <FairyCard style={styles.messageCard}>
          <Ionicons name="sparkles-outline" size={22} color={colors.gold} />
          <Text style={styles.messageText}>{message}</Text>
        </FairyCard>
      ) : null}

        <View style={styles.actions}>
          <FairyButton title="清理选中的临时缓存" onPress={() => setDialogVisible(true)} disabled={!selectedKeys.length} leftContent={<Ionicons name="trash-outline" size={19} color={colors.white} />} />
          <FairyButton title="查看童话会员空间" variant="secondary" onPress={() => router.push('/membership')} />
        </View>
      </View>
      <FairyDialog visible={dialogVisible} icon="trash-outline" title="清理临时缓存" description="这次操作只会清理临时缓存，不会删除任何日记、照片、AI 作品或导出回忆册。" confirmText="确认清理" cancelText="再想想" onCancel={() => setDialogVisible(false)} onConfirm={cleanSelected} />
      <FairyToast visible={toastVisible} tone="success" message={message} onHide={() => setToastVisible(false)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 820 },
  intro: { alignItems: 'center', marginBottom: spacing.xl },
  introTitle: { color: colors.text, fontSize: 18, fontWeight: '900', textAlign: 'center' },
  introText: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.sm, textAlign: 'center' },
  heroCard: {
    backgroundColor: colors.cardPink,
    marginBottom: spacing.xl,
  },
  heroTop: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.lg,
  },
  heroImage: { width: 132 },
  heroCopy: {
    flex: 1,
  },
  heroTitle: {
    color: colors.text,
    fontSize: 20,
    fontWeight: '900',
  },
  heroText: {
    color: colors.textSoft,
    lineHeight: 21,
    marginTop: spacing.xs,
  },
  progressTrack: {
    height: 12,
    borderRadius: 8,
    backgroundColor: colors.card,
    overflow: 'hidden',
    marginTop: spacing.xl,
  },
  progressFill: {
    height: '100%',
    borderRadius: 8,
    backgroundColor: colors.primary,
  },
  progressMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: spacing.sm,
  },
  progressText: {
    color: colors.textSoft,
    fontSize: 12,
    fontWeight: '700',
  },
  legendRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginTop: spacing.lg },
  legendItem: { flexDirection: 'row', alignItems: 'center', gap: 5, paddingHorizontal: spacing.sm, paddingVertical: 6, borderRadius: 13, backgroundColor: 'rgba(255,249,244,0.74)' },
  legendDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: colors.primaryDeep },
  legendDotGold: { backgroundColor: colors.gold },
  legendDotCache: { backgroundColor: '#A9BE9B' },
  legendText: { color: colors.textSoft, fontSize: 10, fontWeight: '800' },
  sectionTitle: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '900',
    marginBottom: spacing.md,
  },
  storageList: {
    gap: spacing.md,
  },
  storageCard: {
    flexDirection: 'row',
    gap: spacing.md,
    padding: spacing.lg,
  },
  storageCardActive: {
    backgroundColor: '#FFF3F5',
  },
  itemIcon: {
    width: 46,
    height: 46,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.cardPink,
  },
  goldIcon: {
    backgroundColor: '#FFF5DF',
  },
  itemCopy: {
    flex: 1,
  },
  itemTitle: {
    color: colors.text,
    fontSize: 16,
    fontWeight: '900',
  },
  itemDetail: {
    color: colors.textSoft,
    marginTop: 3,
    lineHeight: 19,
  },
  itemBar: {
    height: 7,
    borderRadius: 6,
    backgroundColor: colors.secondary,
    overflow: 'hidden',
    marginTop: spacing.sm,
  },
  itemBarFill: {
    height: '100%',
    borderRadius: 6,
    backgroundColor: colors.gold,
  },
  itemRight: {
    alignItems: 'flex-end',
    gap: spacing.xs,
  },
  itemSize: {
    color: colors.text,
    fontWeight: '900',
  },
  checkDot: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    alignItems: 'center',
    justifyContent: 'center',
  },
  checkDotActive: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
  keepText: {
    color: colors.textSoft,
    fontSize: 11,
  },
  cleanCard: {
    marginTop: spacing.xl,
    marginBottom: spacing.lg,
    backgroundColor: '#FFF5DF',
  },
  cleanTitle: {
    color: colors.textSoft,
    fontWeight: '800',
  },
  cleanSize: {
    color: colors.text,
    fontSize: 30,
    fontWeight: '900',
    marginTop: spacing.xs,
  },
  cleanText: {
    color: colors.textSoft,
    lineHeight: 21,
    marginTop: spacing.sm,
  },
  messageCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    marginBottom: spacing.lg,
  },
  messageText: {
    flex: 1,
    color: colors.text,
    lineHeight: 21,
  },
  actions: {
    gap: spacing.md,
  },
});
