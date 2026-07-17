import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyDialog from '@/components/FairyDialog';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyPage from '@/components/FairyPage';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';
import { richTextToPlainText } from '@/utils/richText';

const filters = ['全部', '日记', '照片', 'AI 创作'];

export default function DraftsPage() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const draftDiary = useFairyStore((state) => state.draftDiary);
  const creations = useFairyStore((state) => state.creations);
  const resetDraftDiary = useFairyStore((state) => state.resetDraftDiary);
  const removeCreation = useFairyStore((state) => state.removeCreation);
  const [activeFilter, setActiveFilter] = useState('全部');
  const [pendingDelete, setPendingDelete] = useState(null);
  const [showClearDialog, setShowClearDialog] = useState(false);
  const [toast, setToast] = useState(null);
  const compact = width < 650;

  const drafts = useMemo(() => {
    const items = [];
    if (draftDiary?.title || richTextToPlainText(draftDiary?.content)) {
      items.push({ id: 'draft-diary', category: '日记', title: draftDiary.title || '未命名日记', description: richTextToPlainText(draftDiary.content) || '这一页还没有写完，灵感正在等待回来。', target: '/diary/editor', imageName: 'homeCover', time: '自动保存' });
    }
    creations.filter((item) => item.status?.includes('草稿')).forEach((item) => items.push({ id: item.id, category: 'AI 创作', title: item.title, description: item.resultSummary || `${item.source || '童话工坊'} · ${item.styleName || '还在构思中的作品'}`, target: item.type === '视频' ? '/ai/video-config' : '/ai/comic-config', imageName: item.type === '视频' ? 'homeCover' : 'workshopCover', time: formatDraftTime(item.createdAt), creationId: item.id }));
    return items;
  }, [creations, draftDiary]);

  const visibleDrafts = useMemo(() => activeFilter === '全部' ? drafts : drafts.filter((item) => item.category === activeFilter), [activeFilter, drafts]);

  const deleteDraft = (item) => {
    if (item.id === 'draft-diary') resetDraftDiary();
    else if (item.creationId) removeCreation(item.creationId);
    setPendingDelete(null);
    setToast({ tone: 'success', message: `《${item.title}》已从草稿箱移除。` });
  };

  const clearAllDrafts = () => {
    resetDraftDiary();
    drafts.filter((item) => item.creationId).forEach((item) => removeCreation(item.creationId));
    setShowClearDialog(false);
    setToast({ tone: 'success', message: '草稿箱已经清理完成。' });
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="草稿箱" right={<Pressable disabled={!drafts.length} onPress={() => setShowClearDialog(true)} style={({ pressed }) => [styles.clearAction, !drafts.length && styles.disabled, pressed && styles.pressed]}><Text style={styles.clearActionText}>清理</Text></Pressable>} />}
      topSpace={24}
      bottomSpace={64}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
    >
      <View style={styles.content}>
        <View style={styles.intro}><Text style={styles.introTitle}>没写完的故事，也被好好收着</Text><Text style={styles.introText}>{drafts.length ? `共有 ${drafts.length} 份灵感等待继续` : '现在没有搁置的灵感，去写下新的一页吧'}</Text></View>

        <View style={styles.filters}>{filters.map((item) => <Pressable key={item} onPress={() => setActiveFilter(item)} style={({ pressed }) => [styles.filter, activeFilter === item && styles.filterActive, pressed && styles.pressed]}><Text style={[styles.filterText, activeFilter === item && styles.filterTextActive]}>{item}</Text></Pressable>)}</View>

        {visibleDrafts.length ? <View style={styles.list}>{visibleDrafts.map((item) => <FairyCard key={item.id} style={[styles.item, compact && styles.itemCompact]} padding={spacing.md}><View style={[styles.imageWrap, compact && styles.imageWrapCompact]}><FairyImage name={item.imageName} height={compact ? 180 : 190} radius={20} framed={false} resizeMode="cover" /><View style={styles.ribbon}><Ionicons name={item.category === '日记' ? 'book-outline' : item.category === '照片' ? 'camera-outline' : 'color-wand-outline'} size={16} color={colors.accent} /><Text style={styles.ribbonText}>{item.category}</Text></View></View><View style={styles.itemBody}><Text numberOfLines={2} style={styles.title}>{item.title}</Text><Text numberOfLines={3} style={styles.description}>{item.description}</Text><View style={styles.timeRow}><Ionicons name="time-outline" size={15} color={colors.textSoft} /><Text style={styles.time}>最后编辑：{item.time}</Text></View><View style={styles.actions}><Pressable accessibilityLabel={`删除${item.title}`} onPress={() => setPendingDelete(item)} style={({ pressed }) => [styles.deleteButton, pressed && styles.pressed]}><Ionicons name="trash-outline" size={18} color={colors.textSoft} /><Text style={styles.deleteText}>删除</Text></Pressable><FairyButton title="继续编辑" onPress={() => router.push(item.target)} style={styles.continueButton} leftContent={<Ionicons name="create-outline" size={18} color={colors.white} />} /></View></View></FairyCard>)}</View> : <FairyEmptyState imageName="emptyDiary" title={activeFilter === '全部' ? '草稿箱是空的' : `没有${activeFilter}草稿`} description="没写完的故事会自动收藏在这里，随时都能回来继续。" actionTitle={activeFilter === '全部' ? '去写一篇日记' : '查看全部草稿'} onAction={() => activeFilter === '全部' ? router.push('/diary/editor') : setActiveFilter('全部')} />}

        <View style={styles.footer}><Ionicons name="heart-outline" size={18} color={colors.primaryDeep} /><Text style={styles.footerText}>没写完的故事，也被好好收着</Text></View>
      </View>
      <FairyDialog visible={Boolean(pendingDelete)} title="删除这份草稿？" description={pendingDelete ? `《${pendingDelete.title}》删除后无法恢复。` : ''} icon="trash-outline" confirmText="确认删除" onCancel={() => setPendingDelete(null)} onConfirm={() => pendingDelete && deleteDraft(pendingDelete)} />
      <FairyDialog visible={showClearDialog} title="清理全部草稿？" description={`将删除当前 ${drafts.length} 份草稿，已经发布或生成完成的内容不会受影响。`} icon="file-tray-outline" confirmText="全部清理" onCancel={() => setShowClearDialog(false)} onConfirm={clearAllDrafts} />
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function formatDraftTime(value) {
  if (!value) return '最近';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '最近' : date.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 820 }, pressed: { opacity: 0.65 }, disabled: { opacity: 0.35 },
  clearAction: { width: 64, minHeight: 44, alignItems: 'flex-end', justifyContent: 'center' }, clearActionText: { color: colors.text, fontSize: 14, fontWeight: '900' },
  intro: { alignItems: 'center', marginBottom: spacing.xl }, introTitle: { color: colors.text, fontSize: 20, fontWeight: '900', textAlign: 'center' }, introText: { color: colors.textSoft, fontSize: 12, marginTop: spacing.sm },
  filters: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, padding: spacing.sm, borderRadius: 24, backgroundColor: 'rgba(255,249,244,0.9)', borderWidth: 1, borderColor: colors.border, marginBottom: spacing.xl }, filter: { flexGrow: 1, minWidth: 112, minHeight: 44, paddingHorizontal: spacing.lg, borderRadius: 18, alignItems: 'center', justifyContent: 'center' }, filterActive: { backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.primaryDeep }, filterText: { color: colors.textSoft, fontWeight: '800' }, filterTextActive: { color: colors.primaryDeep },
  list: { gap: spacing.lg }, item: { flexDirection: 'row', gap: spacing.xl, backgroundColor: 'rgba(255,249,244,0.97)' }, itemCompact: { flexDirection: 'column' }, imageWrap: { width: 245, position: 'relative' }, imageWrapCompact: { width: '100%' }, ribbon: { position: 'absolute', left: 10, top: 10, flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: spacing.md, paddingVertical: spacing.sm, borderRadius: 14, backgroundColor: 'rgba(255,240,242,0.94)', borderWidth: 1, borderColor: colors.border }, ribbonText: { color: colors.accent, fontSize: 12, fontWeight: '900' },
  itemBody: { flex: 1, minWidth: 0, padding: spacing.md, justifyContent: 'center' }, title: { color: colors.text, fontSize: 20, lineHeight: 27, fontWeight: '900' }, description: { color: colors.textSoft, lineHeight: 22, marginTop: spacing.md }, timeRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginTop: spacing.lg }, time: { color: colors.textSoft, fontSize: 12 }, actions: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, marginTop: spacing.lg, paddingTop: spacing.md, borderTopWidth: 1, borderTopColor: colors.border }, deleteButton: { minHeight: 48, flexDirection: 'row', alignItems: 'center', gap: spacing.sm, paddingHorizontal: spacing.sm }, deleteText: { color: colors.textSoft, fontWeight: '800' }, continueButton: { flex: 1, maxWidth: 220 },
  footer: { flexDirection: 'row', justifyContent: 'center', alignItems: 'center', gap: spacing.sm, marginTop: spacing.xxl }, footerText: { color: colors.textSoft, fontSize: 12 },
});
