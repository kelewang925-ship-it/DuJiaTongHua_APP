import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyDialog from '@/components/FairyDialog';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyInput from '@/components/FairyInput';
import FairyPage from '@/components/FairyPage';
import FairyTag from '@/components/FairyTag';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';
import { getApiMode } from '@/api/client';

const categories = [
  { id: '心情', icon: 'heart-outline', color: '#E9A4AE' },
  { id: '地点', icon: 'location-outline', color: '#D8A66B' },
  { id: '纪念', icon: 'gift-outline', color: '#E69B9B' },
  { id: 'AI', icon: 'color-wand-outline', color: '#C59AC7' },
];

export default function TagsPage() {
  const { width } = useWindowDimensions();
  const records = useFairyStore((state) => state.records);
  const customTags = useFairyStore((state) => state.customTags) || [];
  const addCustomTag = useFairyStore((state) => state.addCustomTag);
  const updateCustomTag = useFairyStore((state) => state.updateCustomTag);
  const removeCustomTag = useFairyStore((state) => state.removeCustomTag);
  const saveTagReal = useFairyStore((state) => state.saveTagReal);
  const updateTagReal = useFairyStore((state) => state.updateTagReal);
  const deleteTagReal = useFairyStore((state) => state.deleteTagReal);
  const [newTagName, setNewTagName] = useState('');
  const [newTagCategory, setNewTagCategory] = useState(categories[0].id);
  const [editingTag, setEditingTag] = useState(null);
  const [pendingDelete, setPendingDelete] = useState(null);
  const [activeTag, setActiveTag] = useState(null);
  const [error, setError] = useState('');
  const [toast, setToast] = useState(null);
  const compact = width < 640;

  const tagCounts = useMemo(() => records.reduce((bucket, record) => {
    (record.tags || []).forEach((name) => { bucket[name] = (bucket[name] || 0) + 1; });
    return bucket;
  }, {}), [records]);

  const groupedTags = useMemo(() => categories.map((category) => ({ ...category, tags: customTags.filter((item) => item.category === category.id) })), [customTags]);
  const filteredRecords = useMemo(() => activeTag ? records.filter((record) => (record.tags || []).includes(activeTag)) : [], [activeTag, records]);

  const saveTag = async () => {
    const name = newTagName.trim();
    if (!name) { setError('先给这枚标签取一个名字吧。'); return; }
    if (customTags.some((tag) => tag.name === name && tag.id !== editingTag?.id)) { setError('这枚标签已经存在了。'); return; }
    if (getApiMode() === 'real') {
      const result = editingTag ? await updateTagReal(editingTag.id, { name, category: newTagCategory }) : await saveTagReal({ name, category: newTagCategory });
      if (!result.success) { setToast({ tone: 'error', message: result.error?.message || '标签保存失败。' }); return; }
      setToast({ tone: 'success', message: editingTag ? `标签已更新为“${name}”。` : `“${name}”已贴进${newTagCategory}索引。` });
    } else if (editingTag) {
      updateCustomTag(editingTag.id, { name, category: newTagCategory });
      setToast({ tone: 'success', message: `标签已更新为“${name}”。` });
    } else {
      addCustomTag({ name, category: newTagCategory });
      setToast({ tone: 'success', message: `“${name}”已贴进${newTagCategory}索引。` });
    }
    setNewTagName(''); setEditingTag(null); setError('');
  };

  const startEdit = (tag) => { setEditingTag(tag); setNewTagName(tag.name); setNewTagCategory(tag.category); setError(''); };
  const confirmDelete = async () => {
    if (!pendingDelete) return;
    if (getApiMode() === 'real') {
      const result = await deleteTagReal(pendingDelete.id);
      if (!result.success) { setToast({ tone: 'error', message: result.error?.message || '删除失败。' }); setPendingDelete(null); return; }
    } else removeCustomTag(pendingDelete.id);
    if (activeTag === pendingDelete.name) setActiveTag(null);
    setToast({ tone: 'success', message: `“${pendingDelete.name}”已从标签册移除。` });
    setPendingDelete(null);
  };

  return (
    <FairyPage backgroundName="creamPaper" header={<FairyHeader showBack title="标签管理" right={<Text style={styles.headerCount}>{customTags.length} 枚</Text>} />} topSpace={22} bottomSpace={64} contentStyle={styles.pageContent} keyboardShouldPersistTaps="handled" keyboardDismissMode="on-drag" automaticallyAdjustKeyboardInsets showsVerticalScrollIndicator>
      <View style={styles.content}>
        <View style={styles.intro}><Text style={styles.introTitle}>给回忆贴上温柔的小标签</Text><Text style={styles.introText}>心情、地点和重要章节，都会变成找回故事的线索。</Text></View>

        <View style={styles.groupList}>{groupedTags.map((group) => <FairyCard key={group.id} style={styles.groupCard} padding={spacing.lg}><View style={styles.groupHeader}><View style={[styles.groupIcon, { backgroundColor: `${group.color}22` }]}><Ionicons name={group.icon} size={21} color={group.color} /></View><Text style={styles.groupTitle}>{group.id}</Text><Text style={styles.groupCount}>{group.tags.length} 枚</Text></View>{group.tags.length ? <View style={styles.tagCloud}>{group.tags.map((tag) => { const active = activeTag === tag.name; return <View key={tag.id} style={[styles.tagPill, active && styles.tagPillActive]}><Pressable onPress={() => setActiveTag(active ? null : tag.name)} style={({ pressed }) => [styles.tagMain, pressed && styles.pressed]}><Ionicons name={tag.icon || 'pricetag-outline'} size={16} color={active ? colors.white : group.color} /><Text style={[styles.tagName, active && styles.tagNameActive]}>{tag.name}</Text>{tagCounts[tag.name] ? <Text style={[styles.usageCount, active && styles.tagNameActive]}>{tagCounts[tag.name]}</Text> : null}</Pressable><Pressable accessibilityLabel={`编辑${tag.name}`} onPress={() => startEdit(tag)} style={({ pressed }) => [styles.tagAction, pressed && styles.pressed]}><Ionicons name="pencil-outline" size={15} color={active ? colors.white : colors.textSoft} /></Pressable><Pressable accessibilityLabel={`删除${tag.name}`} onPress={() => setPendingDelete(tag)} style={({ pressed }) => [styles.tagAction, pressed && styles.pressed]}><Ionicons name="trash-outline" size={15} color={active ? colors.white : colors.textSoft} /></Pressable></View>; })}</View> : <Text style={styles.emptyGroup}>这一类还没有标签。</Text>}</FairyCard>)}</View>

        <FairyCard style={styles.editorCard} padding={spacing.lg}>
          <View style={styles.editorTitleRow}><Ionicons name={editingTag ? 'pencil-outline' : 'add-circle-outline'} size={21} color={colors.primaryDeep} /><Text style={styles.editorTitle}>{editingTag ? '编辑标签' : '新增标签'}</Text>{editingTag ? <Pressable onPress={() => { setEditingTag(null); setNewTagName(''); setError(''); }} style={styles.cancelEdit}><Text style={styles.cancelEditText}>取消</Text></Pressable> : null}</View>
          <FairyInput value={newTagName} onChangeText={(text) => { setNewTagName(text); setError(''); }} maxLength={12} placeholder="输入新的标签名称" error={error} helper={`${newTagName.length}/12`} containerStyle={styles.inputWrap} />
          <View style={styles.categoryRow}>{categories.map((item) => <Pressable key={item.id} accessibilityRole="radio" accessibilityState={{ checked: newTagCategory === item.id }} onPress={() => setNewTagCategory(item.id)} style={({ pressed }) => [styles.categoryChip, newTagCategory === item.id && styles.categoryChipActive, pressed && styles.pressed]}><Ionicons name={item.icon} size={16} color={newTagCategory === item.id ? colors.white : item.color} /><Text style={[styles.categoryText, newTagCategory === item.id && styles.categoryTextActive]}>{item.id}</Text></Pressable>)}</View>
          <FairyButton title={editingTag ? '保存修改' : '添加标签'} onPress={saveTag} leftContent={<Ionicons name={editingTag ? 'checkmark-outline' : 'add-outline'} size={19} color={colors.white} />} />
        </FairyCard>

        {activeTag ? <View style={styles.related}><Text style={styles.relatedTitle}>与“{activeTag}”相关的记录</Text>{filteredRecords.length ? <View style={styles.recordList}>{filteredRecords.map((record) => <FairyCard key={record.id} style={styles.recordCard} padding={spacing.md}><Text style={styles.recordTitle}>{record.title}</Text><View style={styles.recordMeta}><FairyTag>{record.type}</FairyTag><Text style={styles.recordDate}>{record.date}</Text></View></FairyCard>)}</View> : <FairyEmptyState compact icon="book-outline" title="还没有贴过这枚标签" description="下次写日记或上传照片时，可以把它一起贴进故事。" />}</View> : null}
        <View style={styles.footer}><Ionicons name="star-outline" size={17} color={colors.gold} /><Text style={styles.footerText}>常用标签会让回忆更容易被找到</Text></View>
      </View>
      <FairyDialog visible={Boolean(pendingDelete)} title="删除这枚标签？" description={pendingDelete ? `“${pendingDelete.name}”会从标签册移除，既有记录内容不会被删除。` : ''} icon="trash-outline" confirmText="确认删除" onCancel={() => setPendingDelete(null)} onConfirm={confirmDelete} />
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 820 }, pressed: { opacity: 0.65 }, headerCount: { color: colors.gold, fontSize: 12, fontWeight: '900' },
  intro: { alignItems: 'center', marginBottom: spacing.xl }, introTitle: { color: colors.text, fontSize: 21, fontWeight: '900', textAlign: 'center' }, introText: { color: colors.textSoft, lineHeight: 20, textAlign: 'center', marginTop: spacing.sm },
  groupList: { gap: spacing.md }, groupCard: { backgroundColor: 'rgba(255,249,244,0.96)' }, groupHeader: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginBottom: spacing.md }, groupIcon: { width: 42, height: 42, borderRadius: 16, alignItems: 'center', justifyContent: 'center' }, groupTitle: { flex: 1, color: colors.text, fontSize: 19, fontWeight: '900' }, groupCount: { color: colors.textSoft, fontSize: 11, fontWeight: '800' }, tagCloud: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm }, tagPill: { minHeight: 42, flexDirection: 'row', alignItems: 'center', borderRadius: 18, backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.border, overflow: 'hidden' }, tagPillActive: { backgroundColor: colors.primaryDeep, borderColor: colors.primaryDeep }, tagMain: { minHeight: 42, flexDirection: 'row', alignItems: 'center', gap: 6, paddingLeft: spacing.md, paddingRight: spacing.sm }, tagName: { color: colors.text, fontSize: 12, fontWeight: '900' }, tagNameActive: { color: colors.white }, usageCount: { color: colors.textSoft, fontSize: 10 }, tagAction: { width: 34, height: 42, alignItems: 'center', justifyContent: 'center' }, emptyGroup: { color: colors.textSoft, fontSize: 12 },
  editorCard: { marginTop: spacing.xl, backgroundColor: 'rgba(255,249,244,0.97)' }, editorTitleRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginBottom: spacing.lg }, editorTitle: { flex: 1, color: colors.text, fontSize: 18, fontWeight: '900' }, cancelEdit: { minHeight: 40, justifyContent: 'center', paddingHorizontal: spacing.sm }, cancelEditText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' }, inputWrap: { marginBottom: spacing.md }, categoryRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginBottom: spacing.lg }, categoryChip: { flexGrow: 1, minWidth: 112, minHeight: 42, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, paddingHorizontal: spacing.md, borderRadius: 17, backgroundColor: colors.background, borderWidth: 1, borderColor: colors.border }, categoryChipActive: { backgroundColor: colors.primaryDeep, borderColor: colors.primaryDeep }, categoryText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' }, categoryTextActive: { color: colors.white },
  related: { marginTop: spacing.xl }, relatedTitle: { color: colors.text, fontSize: 18, fontWeight: '900', marginBottom: spacing.md }, recordList: { gap: spacing.sm }, recordCard: { backgroundColor: colors.card }, recordTitle: { color: colors.text, fontSize: 15, fontWeight: '900' }, recordMeta: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginTop: spacing.sm }, recordDate: { color: colors.textSoft, fontSize: 11 }, footer: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, marginTop: spacing.xxl }, footerText: { color: colors.textSoft, fontSize: 12 },
});
