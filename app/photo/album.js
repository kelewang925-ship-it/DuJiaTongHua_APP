import { useMemo, useState } from 'react';
import { Image, Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyDialog from '@/components/FairyDialog';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyPage from '@/components/FairyPage';
import FairyTag from '@/components/FairyTag';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';
import { getApiMode } from '@/api/client';

const filters = ['全部', '约会', '日常', '旅行', '晚霞'];
const mockFallbackImages = ['albumCover', 'homeCover', 'anniversaryCover', 'coupleCover'];
const getPhotoCount = (item) => Number.isFinite(Number(item?.photoCount)) ? Math.max(0, Number(item.photoCount)) : 0;

export default function AlbumPage() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const isReal = getApiMode() === 'real';
  const records = useFairyStore((state) => state.records);
  const removePhotoRecord = useFairyStore((state) => state.removePhotoRecord);
  const deletePhotoReal = useFairyStore((state) => state.deletePhotoReal);
  const [viewMode, setViewMode] = useState('grid');
  const [showFilters, setShowFilters] = useState(false);
  const [activeFilter, setActiveFilter] = useState('全部');
  const [expandedId, setExpandedId] = useState(null);
  const [pendingDelete, setPendingDelete] = useState(null);
  const [failedUris, setFailedUris] = useState([]);
  const [isDeleting, setIsDeleting] = useState(false);
  const [toast, setToast] = useState(null);
  const compact = width < 650;
  const photoRecords = useMemo(() => records.filter((item) => item.type === '照片'), [records]);
  const visibleRecords = useMemo(() => activeFilter === '全部' ? photoRecords : photoRecords.filter((item) => (item.tags || []).includes(activeFilter)), [activeFilter, photoRecords]);
  const totalPhotos = photoRecords.reduce((sum, item) => sum + getPhotoCount(item), 0);

  const confirmDelete = async () => {
    if (!pendingDelete || isDeleting) return;
    setIsDeleting(true);
    const result = isReal ? await deletePhotoReal(pendingDelete.id) : { success: removePhotoRecord(pendingDelete.id) };
    if (!result.success) {
      setIsDeleting(false);
      setToast({ tone: 'error', message: result.error?.message || '照片记录删除失败，请重试。' });
      return;
    }
    setPendingDelete(null);
    setIsDeleting(false);
    setToast({ tone: 'success', message: isReal ? '这组照片记录已从情侣空间删除。' : '这组 Mock 照片记录已从本地演示相册移除。' });
  };

  return (
    <FairyPage backgroundName="creamPaper" header={<FairyHeader showBack title="回忆相册" right={<Pressable accessibilityRole="button" onPress={() => setShowFilters((value) => !value)} style={({ pressed }) => [styles.headerFilter, showFilters && styles.headerFilterActive, pressed && styles.pressed]}><Ionicons name="filter-outline" size={19} color={showFilters ? colors.primaryDeep : colors.text} /><Text style={[styles.headerFilterText, showFilters && styles.headerFilterTextActive]}>筛选</Text></Pressable>} />} topSpace={22} bottomSpace={82} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <FairyCard style={[styles.heroCard, compact && styles.heroCardCompact]} padding={spacing.md}><View style={[styles.heroImage, compact && styles.heroImageCompact]}><FairyImage name="albumCover" height={compact ? 185 : 220} radius={22} framed={false} resizeMode="cover" /></View><View style={styles.heroCopy}><Text style={styles.heroTitle}>照片会长成回忆章节</Text><Text style={styles.heroText}>每一组画面都会同步到记录中心，成为你们时间线里的一页。</Text><View style={styles.summaryRow}><View><Text style={styles.summaryNum}>{totalPhotos}</Text><Text style={styles.summaryLabel}>已记录照片</Text></View><View style={styles.summaryDivider} /><View><Text style={styles.summaryNum}>{photoRecords.length}</Text><Text style={styles.summaryLabel}>组回忆</Text></View></View></View></FairyCard>

        <View style={styles.modeRow}><Pressable accessibilityRole="tab" accessibilityState={{ selected: viewMode === 'grid' }} onPress={() => setViewMode('grid')} style={({ pressed }) => [styles.mode, viewMode === 'grid' && styles.modeActive, pressed && styles.pressed]}><Ionicons name="grid-outline" size={18} color={viewMode === 'grid' ? colors.primaryDeep : colors.textSoft} /><Text style={[styles.modeText, viewMode === 'grid' && styles.modeTextActive]}>网格</Text></Pressable><Pressable accessibilityRole="tab" accessibilityState={{ selected: viewMode === 'timeline' }} onPress={() => setViewMode('timeline')} style={({ pressed }) => [styles.mode, viewMode === 'timeline' && styles.modeActive, pressed && styles.pressed]}><Ionicons name="list-outline" size={18} color={viewMode === 'timeline' ? colors.primaryDeep : colors.textSoft} /><Text style={[styles.modeText, viewMode === 'timeline' && styles.modeTextActive]}>时间线</Text></Pressable></View>
        {showFilters ? <View style={styles.filterRow}>{filters.map((filter) => <Pressable key={filter} onPress={() => setActiveFilter(filter)} style={({ pressed }) => [styles.filterChip, activeFilter === filter && styles.filterChipActive, pressed && styles.pressed]}><Text style={[styles.filterText, activeFilter === filter && styles.filterTextActive]}>{filter}</Text></Pressable>)}</View> : null}

        {!visibleRecords.length ? <FairyEmptyState imageName="emptyAlbum" title={activeFilter === '全部' ? '还没有照片' : `没有“${activeFilter}”照片`} description="选择一组照片，把幸福轻轻贴进回忆相册。" actionTitle={activeFilter === '全部' ? '上传照片' : '查看全部'} onAction={() => activeFilter === '全部' ? router.push('/photo/upload') : setActiveFilter('全部')} /> : viewMode === 'grid' ? <View style={styles.grid}>{visibleRecords.map((item, index) => <PhotoCard key={item.id} item={item} index={index} compact={compact} expanded={expandedId === item.id} failedUris={failedUris} isReal={isReal} onImageError={(uri) => setFailedUris((items) => items.includes(uri) ? items : [...items, uri])} onPress={() => setExpandedId((id) => id === item.id ? null : item.id)} onDelete={() => setPendingDelete(item)} />)}</View> : <View style={styles.timeline}>{visibleRecords.map((item, index) => <View key={item.id} style={styles.timelineRow}><View style={styles.timelineRail}><View style={styles.timelineDot} />{index < visibleRecords.length - 1 ? <View style={styles.timelineLine} /> : null}</View><FairyCard style={styles.timelineCard} padding={spacing.md}><View style={styles.timelineImage}><RecordImage item={item} index={index} height={145} failedUris={failedUris} isReal={isReal} onImageError={(uri) => setFailedUris((items) => items.includes(uri) ? items : [...items, uri])} /></View><View style={styles.timelineCopy}><Text style={styles.photoTitle}>{item.title}</Text><Text style={styles.photoDate}>{item.date} · {getPhotoCount(item) ? `${getPhotoCount(item)} 张` : '数量未记录'}</Text><Text numberOfLines={3} style={styles.photoDescription}>{item.content}</Text>{item.tags?.length ? <View style={styles.tagRow}>{item.tags.map((tag) => <FairyTag key={`${item.id}-${tag}`}>{tag}</FairyTag>)}</View> : null}<Pressable onPress={() => setPendingDelete(item)} style={({ pressed }) => [styles.deleteLink, pressed && styles.pressed]}><Ionicons name="trash-outline" size={16} color={colors.textSoft} /><Text style={styles.deleteLinkText}>移除记录</Text></Pressable></View></FairyCard></View>)}</View>}

        <FairyButton title="新增一组照片" onPress={() => router.push('/photo/upload')} style={styles.addButton} leftContent={<Ionicons name="add" size={22} color={colors.white} />} />
      </View>
      <FairyDialog visible={Boolean(pendingDelete)} title="移除这组照片？" description={pendingDelete ? (isReal ? `《${pendingDelete.title}》将从当前情侣空间删除，失败时会保留原记录。` : `《${pendingDelete.title}》只会从本地 Mock 记录中删除。`) : ''} icon="trash-outline" confirmText={isDeleting ? '正在删除……' : '确认移除'} onCancel={() => { if (!isDeleting) setPendingDelete(null); }} onConfirm={confirmDelete} />
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function PhotoCard({ item, index, compact, expanded, failedUris, isReal, onImageError, onPress, onDelete }) {
  const count = getPhotoCount(item);
  return <FairyCard onPress={onPress} style={styles.photoCard} padding={spacing.sm} accessibilityRole="button"><View style={styles.photoImage}><RecordImage item={item} index={index} height={compact ? 170 : 210} failedUris={failedUris} isReal={isReal} onImageError={onImageError} /></View><View style={styles.photoBody}><View style={styles.photoTop}><Text numberOfLines={2} style={styles.photoTitle}>{item.title}</Text><Text style={styles.photoCount}>{count ? `${count} 张` : '数量未记录'}</Text></View><Text style={styles.photoDate}>{item.date}</Text>{item.tags?.length ? <View style={styles.tagRow}>{item.tags.slice(0, 2).map((tag) => <FairyTag key={`${item.id}-${tag}`}>{tag}</FairyTag>)}</View> : null}{expanded ? <View style={styles.expanded}><Text style={styles.photoDescription}>{item.content}</Text><Pressable onPress={onDelete} style={({ pressed }) => [styles.deleteLink, pressed && styles.pressed]}><Ionicons name="trash-outline" size={16} color={colors.textSoft} /><Text style={styles.deleteLinkText}>移除记录</Text></Pressable></View> : null}</View></FairyCard>;
}

function RecordImage({ item, index, height, failedUris, isReal, onImageError }) {
  const uri = item.photos?.[0]?.uri;
  if (uri && !failedUris.includes(uri)) return <Image source={{ uri }} resizeMode="cover" style={[styles.realImage, { height }]} onError={() => onImageError(uri)} />;
  if (!isReal) return <FairyImage name={mockFallbackImages[index % mockFallbackImages.length]} height={height} radius={18} framed={false} resizeMode="cover" />;
  return <View style={[styles.missingImage, { height }]}><Ionicons name="image-outline" size={28} color={colors.textSoft} /><Text style={styles.missingImageText}>{uri ? '照片暂时无法加载' : '这组记录没有可用封面'}</Text></View>;
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 900 }, pressed: { opacity: 0.65 }, headerFilter: { width: 64, minHeight: 44, flexDirection: 'row', alignItems: 'center', justifyContent: 'flex-end', gap: 4 }, headerFilterActive: { opacity: 1 }, headerFilterText: { color: colors.text, fontSize: 12, fontWeight: '900' }, headerFilterTextActive: { color: colors.primaryDeep },
  heroCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.xl, backgroundColor: 'rgba(255,249,244,0.96)', marginBottom: spacing.xl }, heroCardCompact: { flexDirection: 'column' }, heroImage: { width: '48%' }, heroImageCompact: { width: '100%' }, heroCopy: { flex: 1, padding: spacing.lg }, heroTitle: { color: colors.text, fontSize: 22, fontWeight: '900' }, heroText: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.md }, summaryRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.xl, marginTop: spacing.xl }, summaryNum: { color: colors.primaryDeep, fontSize: 27, fontWeight: '900' }, summaryLabel: { color: colors.textSoft, fontSize: 11 }, summaryDivider: { width: 1, height: 42, backgroundColor: colors.border },
  modeRow: { flexDirection: 'row', alignSelf: 'center', minWidth: 330, padding: 5, borderRadius: 22, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, marginBottom: spacing.lg }, mode: { flex: 1, minHeight: 44, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, borderRadius: 17 }, modeActive: { backgroundColor: colors.cardPink }, modeText: { color: colors.textSoft, fontWeight: '800' }, modeTextActive: { color: colors.primaryDeep }, filterRow: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', gap: spacing.sm, marginBottom: spacing.lg }, filterChip: { minHeight: 40, paddingHorizontal: spacing.lg, alignItems: 'center', justifyContent: 'center', borderRadius: 17, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border }, filterChipActive: { backgroundColor: colors.primary, borderColor: colors.primaryDeep }, filterText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' }, filterTextActive: { color: colors.white },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.lg }, photoCard: { width: '48%', flexGrow: 1, minWidth: 270, backgroundColor: 'rgba(255,249,244,0.97)' }, photoImage: { overflow: 'hidden', borderRadius: 18 }, realImage: { width: '100%', borderRadius: 18, backgroundColor: colors.cardPink }, missingImage: { width: '100%', borderRadius: 18, alignItems: 'center', justifyContent: 'center', gap: spacing.sm, backgroundColor: colors.background, borderWidth: 1, borderColor: colors.border }, missingImageText: { color: colors.textSoft, fontSize: 11, fontWeight: '700' }, photoBody: { padding: spacing.md }, photoTop: { flexDirection: 'row', alignItems: 'flex-start', gap: spacing.sm }, photoTitle: { flex: 1, color: colors.text, fontSize: 17, fontWeight: '900' }, photoCount: { color: colors.primaryDeep, fontSize: 11, fontWeight: '900' }, photoDate: { color: colors.textSoft, fontSize: 11, marginTop: 5 }, tagRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginTop: spacing.md }, expanded: { marginTop: spacing.md, paddingTop: spacing.md, borderTopWidth: 1, borderTopColor: colors.border }, photoDescription: { color: colors.textSoft, lineHeight: 20 }, deleteLink: { minHeight: 40, flexDirection: 'row', alignItems: 'center', gap: spacing.sm, alignSelf: 'flex-start', marginTop: spacing.sm }, deleteLinkText: { color: colors.textSoft, fontSize: 11, fontWeight: '800' },
  timeline: { gap: 0 }, timelineRow: { flexDirection: 'row', gap: spacing.md }, timelineRail: { width: 22, alignItems: 'center' }, timelineDot: { width: 13, height: 13, borderRadius: 7, backgroundColor: colors.primaryDeep, marginTop: 30 }, timelineLine: { width: 2, flex: 1, minHeight: 220, backgroundColor: colors.border }, timelineCard: { flex: 1, flexDirection: 'row', gap: spacing.lg, backgroundColor: 'rgba(255,249,244,0.97)', marginBottom: spacing.lg }, timelineImage: { width: 180 }, timelineCopy: { flex: 1, minWidth: 0, padding: spacing.sm }, addButton: { marginTop: spacing.xl },
});