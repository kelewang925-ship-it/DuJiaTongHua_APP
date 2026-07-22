import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Switch, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyDialog from '@/components/FairyDialog';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyInput from '@/components/FairyInput';
import FairyPage from '@/components/FairyPage';
import FairyRequestState from '@/components/FairyRequestState';
import FairyTag from '@/components/FairyTag';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';
import { getApiMode } from '@/api/client';

const contentTypes = [
  { id: '日记', icon: 'book-outline' },
  { id: '照片', icon: 'images-outline' },
  { id: 'AI作品', icon: 'color-wand-outline' },
  { id: '纪念日', icon: 'calendar-outline' },
];

export default function TimeCapsuleSettingsPage() {
  const { width } = useWindowDimensions();
  const isReal = getApiMode() === 'real';
  const capsules = useFairyStore((state) => state.timeCapsules) || [];
  const loading = useFairyStore((state) => Boolean(state.loading?.bootstrap || state.loading?.modules));
  const loadError = useFairyStore((state) => state.errors?.bootstrap || state.errors?.modules || null);
  const refreshCoreData = useFairyStore((state) => state.refreshCoreData);
  const addTimeCapsule = useFairyStore((state) => state.addTimeCapsule);
  const removeTimeCapsule = useFairyStore((state) => state.removeTimeCapsule);
  const toggleTimeCapsuleReminder = useFairyStore((state) => state.toggleTimeCapsuleReminder);
  const saveTimeCapsuleReal = useFairyStore((state) => state.saveTimeCapsuleReal);
  const deleteTimeCapsuleReal = useFairyStore((state) => state.deleteTimeCapsuleReal);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [unlockDate, setUnlockDate] = useState('');
  const [selectedTypes, setSelectedTypes] = useState([]);
  const [reminder, setReminder] = useState(true);
  const [error, setError] = useState({});
  const [pendingDelete, setPendingDelete] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [toast, setToast] = useState(null);
  const compact = width < 650;

  const futureHint = useMemo(() => getFutureHint(unlockDate), [unlockDate]);
  const toggleType = (type) => setSelectedTypes((items) => items.includes(type) ? items.filter((item) => item !== type) : [...items, type]);

  const createCapsule = async () => {
    const nextError = {};
    if (!title.trim()) nextError.title = '请给胶囊取一个名字。';
    if (content.trim().length < 10) nextError.content = '至少写下 10 个字，留给未来的心意会更完整。';
    if (!/^\d{4}-\d{2}-\d{2}$/.test(unlockDate) || !futureHint.valid) nextError.date = '请输入晚于今天的有效日期（YYYY-MM-DD）。';
    if (!selectedTypes.length) nextError.types = '至少选择一种一起封存的内容。';
    if (Object.keys(nextError).length) { setError(nextError); setToast({ tone: 'error', message: '还有几处需要补充后才能封存。' }); return; }
    if (submitting) return;
    setSubmitting(true);
    const payload = { title: title.trim(), content: content.trim(), unlockDate, reminder, contentTypes: selectedTypes };
    const result = isReal ? await saveTimeCapsuleReal(payload) : { success: true, data: addTimeCapsule(payload) };
    setSubmitting(false);
    if (!result.success) { setToast({ tone: 'error', message: result.error?.message || '胶囊保存失败。' }); return; }
    const capsule = result.data;
    setTitle('');
    setContent('');
    setUnlockDate('');
    setSelectedTypes([]);
    setReminder(true);
    setError({});
    setToast({ tone: 'success', message: `《${capsule.title}》已锁进时光胶囊。` });
  };

  const confirmDelete = async () => {
    if (!pendingDelete || submitting) return;
    setSubmitting(true);
    const result = isReal ? await deleteTimeCapsuleReal(pendingDelete.id) : { success: true, data: removeTimeCapsule(pendingDelete.id) };
    setSubmitting(false);
    setPendingDelete(null);
    setToast(result.success ? { tone: 'success', message: '这枚胶囊已安全移除。' } : { tone: 'error', message: result.error?.message || '移除失败。' });
  };

  const toggleReminder = async (capsule) => {
    if (submitting) return;
    setSubmitting(true);
    const result = await toggleTimeCapsuleReminder(capsule.id);
    setSubmitting(false);
    if (!result?.success) setToast({ tone: 'error', message: result?.error?.message || '提醒状态更新失败。' });
  };

  return (
    <FairyPage backgroundName="creamPaper" header={<FairyHeader showBack title="时光胶囊" right={<Text style={styles.headerCount}>{capsules.length} 枚</Text>} />} topSpace={22} bottomSpace={64} contentStyle={styles.pageContent} keyboardShouldPersistTaps="handled" keyboardDismissMode="on-drag" automaticallyAdjustKeyboardInsets showsVerticalScrollIndicator>
      <View style={styles.content}>
        <FairyCard style={[styles.heroCard, compact && styles.heroCardCompact]} padding={spacing.md}><View style={styles.heroCopy}><Text style={styles.heroTitle}>未来开启的小秘密</Text><Text style={styles.heroText}>在未来的某一天，一起打开这份只属于你们的心意。</Text><View style={styles.futureTag}><Ionicons name="lock-closed-outline" size={15} color={colors.gold} /><Text style={styles.futureTagText}>保存后在打开日期前不可查看正文</Text></View></View><View style={[styles.heroImage, compact && styles.heroImageCompact]}><FairyImage name="timeCapsuleCover" height={compact ? 190 : 230} radius={22} framed={false} resizeMode="cover" /></View></FairyCard>

        {isReal ? <FairyRequestState loading={loading} error={loadError} onRetry={refreshCoreData} /> : null}
        {!loading && !loadError ? (
          <>
            <FairyCard style={styles.formCard} padding={spacing.xl}>
              <FairyInput label="胶囊标题" editable={!submitting} icon="bookmark-outline" value={title} onChangeText={(text) => { setTitle(text); setError((items) => ({ ...items, title: '' })); }} maxLength={28} placeholder="例如：写给一周年后的我们" error={error.title} />
              <FairyInput label="打开日期" editable={!submitting} icon="calendar-outline" value={unlockDate} onChangeText={(text) => { setUnlockDate(text); setError((items) => ({ ...items, date: '' })); }} maxLength={10} keyboardType="numbers-and-punctuation" placeholder="YYYY-MM-DD" error={error.date} helper={futureHint.valid ? futureHint.label : '选择未来想开启的那一天'} />
              <FairyInput label="胶囊内容" editable={!submitting} value={content} onChangeText={(text) => { setContent(text); setError((items) => ({ ...items, content: '' })); }} multiline maxLength={500} placeholder="把想对未来说的话写在这里……" error={error.content} helper={`${content.length}/500`} helperInside containerStyle={styles.contentInput} />
              <View style={styles.lockNote}><Ionicons name="shield-checkmark-outline" size={17} color={colors.gold} /><Text style={styles.lockNoteText}>胶囊一旦保存，在打开日期前只能查看标题、日期和内容类型。</Text></View>
              <Text style={styles.fieldLabel}>一起封存</Text><View style={styles.typeRow}>{contentTypes.map((type) => { const selected = selectedTypes.includes(type.id); return <Pressable key={type.id} disabled={submitting} accessibilityRole="checkbox" accessibilityState={{ checked: selected }} onPress={() => { toggleType(type.id); setError((items) => ({ ...items, types: '' })); }} style={({ pressed }) => [styles.typeChip, selected && styles.typeChipActive, pressed && styles.pressed]}><Ionicons name={type.icon} size={18} color={selected ? colors.white : colors.textSoft} /><Text style={[styles.typeText, selected && styles.typeTextActive]}>{type.id}</Text></Pressable>; })}</View>{error.types ? <Text style={styles.typeError}>{error.types}</Text> : null}
              <View style={styles.reminderRow}><View style={styles.reminderIcon}><Ionicons name="notifications-outline" size={22} color={colors.gold} /></View><View style={styles.reminderCopy}><Text style={styles.reminderTitle}>开启提醒</Text><Text style={styles.reminderText}>在打开日期当天提醒我们一起开启</Text></View><Switch disabled={submitting} value={reminder} onValueChange={setReminder} trackColor={{ false: '#E9D7D2', true: colors.primary }} thumbColor={colors.white} /></View>
              <FairyButton title={submitting ? '正在封存…' : '保存胶囊'} disabled={submitting} onPress={createCapsule} leftContent={<Ionicons name="lock-closed-outline" size={19} color={colors.white} />} />
            </FairyCard>

            <View style={styles.sectionRow}><Text style={styles.sectionTitle}>已经封存</Text><Text style={styles.sectionCount}>{capsules.length} 枚</Text></View>
            {capsules.length ? <View style={styles.list}>{capsules.map((capsule) => <FairyCard key={capsule.id} style={styles.itemCard} padding={spacing.lg}><View style={styles.itemTop}><View style={styles.itemLock}><Ionicons name="lock-closed" size={19} color={colors.gold} /></View><View style={styles.itemCopy}><Text style={styles.itemTitle}>{capsule.title}</Text><Text style={styles.itemDate}>{capsule.unlockDate} 开启</Text></View><Pressable accessibilityLabel={`删除${capsule.title}`} disabled={submitting} onPress={() => setPendingDelete(capsule)} style={({ pressed }) => [styles.deleteAction, pressed && styles.pressed]}><Ionicons name="trash-outline" size={19} color={colors.textSoft} /></Pressable></View><View style={styles.sealedContent}><Ionicons name="mail-closed-outline" size={18} color={colors.primaryDeep} /><Text style={styles.sealedText}>正文已封存 · 到期前不可查看</Text></View><View style={styles.itemFooter}><View style={styles.tagRow}>{(capsule.contentTypes || []).map((type) => <FairyTag key={`${capsule.id}-${type}`}>{type}</FairyTag>)}</View><Pressable disabled={submitting} onPress={() => toggleReminder(capsule)} style={({ pressed }) => [styles.reminderToggle, pressed && styles.pressed]}><Ionicons name={(capsule.reminder ?? capsule.reminderEnabled) ? 'notifications' : 'notifications-off-outline'} size={16} color={(capsule.reminder ?? capsule.reminderEnabled) ? colors.primaryDeep : colors.textSoft} /><Text style={[styles.reminderToggleText, (capsule.reminder ?? capsule.reminderEnabled) && styles.reminderToggleTextActive]}>{(capsule.reminder ?? capsule.reminderEnabled) ? '已提醒' : '未提醒'}</Text></Pressable></View></FairyCard>)}</View> : <FairyEmptyState imageName="emptyDiary" title="还没有封存胶囊" description="创建第一枚胶囊，让今天的故事在未来发光。" />}
          </>
        ) : null}
        <View style={styles.footer}><Ionicons name="heart-outline" size={16} color={colors.primaryDeep} /><Text style={styles.footerText}>保存后将为你和 TA 锁定这份心意</Text></View>
      </View>
      <FairyDialog visible={Boolean(pendingDelete)} title="移除这枚胶囊？" description={pendingDelete ? `《${pendingDelete.title}》及其中封存的内容会被删除。` : ''} icon="trash-outline" confirmText={submitting ? '正在移除…' : '确认移除'} onCancel={() => !submitting && setPendingDelete(null)} onConfirm={confirmDelete} />
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function getFutureHint(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return { valid: false, label: '' };
  const date = new Date(`${value}T00:00:00`);
  const today = new Date(); today.setHours(0, 0, 0, 0);
  if (Number.isNaN(date.getTime()) || date <= today) return { valid: false, label: '' };
  const days = Math.ceil((date.getTime() - today.getTime()) / 86400000);
  return { valid: true, label: `距离开启还有 ${days} 天` };
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 800 }, pressed: { opacity: 0.65 }, headerCount: { color: colors.gold, fontSize: 12, fontWeight: '900' },
  heroCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.xl, backgroundColor: 'rgba(255,249,244,0.96)', marginBottom: spacing.xl }, heroCardCompact: { flexDirection: 'column-reverse' }, heroCopy: { flex: 1, padding: spacing.lg }, heroTitle: { color: colors.text, fontSize: 23, fontWeight: '900' }, heroText: { color: colors.textSoft, lineHeight: 22, marginTop: spacing.md }, futureTag: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginTop: spacing.xl }, futureTagText: { flex: 1, color: colors.gold, fontSize: 11, fontWeight: '800' }, heroImage: { width: '46%' }, heroImageCompact: { width: '100%' },
  formCard: { backgroundColor: 'rgba(255,249,244,0.97)', marginBottom: spacing.xl }, contentInput: { marginBottom: spacing.md }, lockNote: { flexDirection: 'row', alignItems: 'flex-start', gap: spacing.sm, padding: spacing.md, borderRadius: 16, backgroundColor: '#FFF8E8', marginBottom: spacing.lg }, lockNoteText: { flex: 1, color: colors.textSoft, fontSize: 11, lineHeight: 18 }, fieldLabel: { color: colors.text, fontSize: 15, fontWeight: '800', marginBottom: spacing.sm }, typeRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm }, typeChip: { flexGrow: 1, minWidth: 125, minHeight: 44, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, paddingHorizontal: spacing.md, borderRadius: 17, backgroundColor: colors.background, borderWidth: 1, borderColor: colors.border }, typeChipActive: { backgroundColor: colors.primaryDeep, borderColor: colors.primaryDeep }, typeText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' }, typeTextActive: { color: colors.white }, typeError: { color: colors.primaryDeep, fontSize: 12, fontWeight: '700', marginTop: spacing.sm }, reminderRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, paddingVertical: spacing.lg, marginVertical: spacing.lg, borderTopWidth: 1, borderBottomWidth: 1, borderColor: colors.border }, reminderIcon: { width: 48, height: 48, borderRadius: 18, alignItems: 'center', justifyContent: 'center', backgroundColor: '#FFF5DF' }, reminderCopy: { flex: 1 }, reminderTitle: { color: colors.text, fontSize: 15, fontWeight: '900' }, reminderText: { color: colors.textSoft, fontSize: 11, marginTop: 4 },
  sectionRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: spacing.md }, sectionTitle: { color: colors.text, fontSize: 19, fontWeight: '900' }, sectionCount: { color: colors.textSoft, fontSize: 11, fontWeight: '800' }, list: { gap: spacing.md }, itemCard: { backgroundColor: 'rgba(255,249,244,0.96)' }, itemTop: { flexDirection: 'row', alignItems: 'center', gap: spacing.md }, itemLock: { width: 46, height: 46, borderRadius: 18, alignItems: 'center', justifyContent: 'center', backgroundColor: '#FFF5DF' }, itemCopy: { flex: 1 }, itemTitle: { color: colors.text, fontSize: 17, fontWeight: '900' }, itemDate: { color: colors.gold, fontSize: 11, fontWeight: '800', marginTop: 4 }, deleteAction: { width: 44, height: 44, alignItems: 'center', justifyContent: 'center' }, sealedContent: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, padding: spacing.md, borderRadius: 16, backgroundColor: colors.cardPink, marginTop: spacing.md }, sealedText: { color: colors.primaryDeep, fontSize: 12, fontWeight: '800' }, itemFooter: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.md, marginTop: spacing.md }, tagRow: { flex: 1, flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm }, reminderToggle: { minHeight: 40, flexDirection: 'row', alignItems: 'center', gap: 5, paddingHorizontal: spacing.sm }, reminderToggleText: { color: colors.textSoft, fontSize: 11, fontWeight: '800' }, reminderToggleTextActive: { color: colors.primaryDeep }, footer: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, marginTop: spacing.xxl }, footerText: { color: colors.textSoft, fontSize: 12 },
});
