import { useEffect, useMemo, useState } from 'react';
import { Pressable, StyleSheet, Switch, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams, useRouter } from 'expo-router';
import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyInput from '@/components/FairyInput';
import FairyPage from '@/components/FairyPage';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';
import { getApiMode } from '@/api/client';

const typeOptions = [
  { key: 'heart', label: '相识', icon: 'heart-outline' },
  { key: 'birthday', label: '生日', icon: 'gift-outline' },
  { key: 'travel', label: '旅行', icon: 'airplane-outline' },
  { key: 'custom', label: '自定义', icon: 'star-outline' },
];
const coverColors = ['#F5A3A8', '#F5C1A9', '#F6D997', '#BFCDAA', '#D3BED8', '#AED0DF'];
const reminderOptions = [1, 3, 7];
const templateMap = {
  firstMeet: { title: '第一次见面纪念日', note: '那天的天气、表情和第一句话都很值得写下。', type: 'heart' },
  travel: { title: '第一次旅行纪念日', note: '把路线、照片和那顿饭的味道都留在这一页。', type: 'travel' },
  birthday: { title: '生日纪念章节', note: '写下你准备的小惊喜和那天的愿望。', type: 'birthday' },
  firstDate: { title: '第一次约会纪念日', note: '记下第一次并肩走过的路、说过的话和悄悄心动的瞬间。', type: 'heart' },
  ordinary: { title: '属于我们的普通纪念日', note: '平凡日子里的小小闪光，也值得被温柔收藏。', type: 'custom' },
};

function inferType(item) {
  if (item?.type) return item.type;
  if (item?.icon?.includes('airplane')) return 'travel';
  if (item?.icon?.includes('gift')) return 'birthday';
  return 'heart';
}

export default function AnniversaryEditPage() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const params = useLocalSearchParams();
  const id = Array.isArray(params.id) ? params.id[0] : params.id;
  const template = Array.isArray(params.template) ? params.template[0] : params.template;
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const addAnniversary = useFairyStore((state) => state.addAnniversary);
  const updateAnniversary = useFairyStore((state) => state.updateAnniversary);
  const saveAnniversaryReal = useFairyStore((state) => state.saveAnniversaryReal);
  const updateAnniversaryReal = useFairyStore((state) => state.updateAnniversaryReal);
  const target = useMemo(() => anniversaries.find((item) => item.id === id), [anniversaries, id]);
  const templatePreset = template ? templateMap[template] : null;
  const requestedEdit = Boolean(id);
  const missingTarget = requestedEdit && !target;
  const isEditMode = Boolean(target);
  const compact = width < 390;

  const [title, setTitle] = useState('');
  const [date, setDate] = useState('');
  const [note, setNote] = useState('');
  const [type, setType] = useState('heart');
  const [repeatYearly, setRepeatYearly] = useState(true);
  const [reminderDays, setReminderDays] = useState(3);
  const [coverColor, setCoverColor] = useState(coverColors[0]);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [toast, setToast] = useState({ visible: false, message: '', tone: 'success' });

  useEffect(() => {
    if (target) {
      setTitle(target.title || '');
      setDate(target.date || '');
      setNote(target.note || target.description || '');
      setType(inferType(target));
      setRepeatYearly(target.repeatYearly ?? target.repeatType !== 'none');
      setReminderDays(target.reminderDays || 3);
      setCoverColor(target.coverColor || coverColors[0]);
      return;
    }
    if (!requestedEdit && templatePreset) {
      setTitle(templatePreset.title);
      setNote(templatePreset.note);
      setType(templatePreset.type);
    }
  }, [requestedEdit, target, templatePreset]);

  const selectedType = typeOptions.find((item) => item.key === type) || typeOptions[0];

  const save = async () => {
    if (submitting) return;
    if (missingTarget) {
      setToast({ visible: true, message: '这条纪念日记录不存在或已被删除，无法继续编辑。', tone: 'error' });
      return;
    }
    if (!title.trim()) {
      setError('请写下这一章的标题。');
      return;
    }
    if (!/^\d{4}[-./]\d{2}[-./]\d{2}$/.test(date.trim())) {
      setError('请按 YYYY-MM-DD 填写完整日期。');
      return;
    }
    const payload = {
      title: title.trim(),
      date: date.trim().replaceAll('.', '-').replaceAll('/', '-'),
      note,
      type,
      icon: selectedType.icon,
      repeatYearly,
      reminderDays,
      coverColor,
    };
    setSubmitting(true);
    try {
      if (getApiMode() === 'real') {
        const result = isEditMode ? await updateAnniversaryReal(target.id, payload) : await saveAnniversaryReal(payload);
        if (!result.success) {
          setToast({ visible: true, message: result.error?.message || '保存失败，请重试。', tone: 'error' });
          return;
        }
      } else if (isEditMode) {
        updateAnniversary(target.id, payload);
      } else {
        addAnniversary(payload);
      }
      setToast({ visible: true, message: isEditMode ? '纪念章节已经更新。' : '新的纪念章节已经写进故事册。', tone: 'success' });
      setTimeout(() => router.replace('/anniversary'), 650);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <FairyPage backgroundName="creamPaper" topSpace={28} bottomSpace={60} contentStyle={styles.pageContent} showsVerticalScrollIndicator keyboardShouldPersistTaps="handled" keyboardDismissMode="on-drag" automaticallyAdjustKeyboardInsets header={<FairyHeader showBack title={isEditMode ? '编辑纪念日' : requestedEdit ? '纪念日不存在' : '新增纪念日'} />}>
      <View style={styles.content}>
        {missingTarget ? (
          <FairyEmptyState imageName="emptyDiary" title="没有找到这条纪念日" description="它可能已经被删除，或当前账号无权访问。返回纪念日列表后可以选择其他记录。" actionTitle="返回纪念日列表" onAction={() => router.replace('/anniversary')} />
        ) : (
          <>
            <View style={styles.intro}><Text style={styles.introTitle}>给重要日子做一枚书签</Text><Text style={styles.introText}>日期、提醒和封面颜色都可以慢慢挑，只有你们可见。</Text></View>
            <FairyCard style={styles.formCard} padding={compact ? spacing.lg : spacing.xl}>
              <View style={styles.heroRow}><View style={styles.heroCopy}><Text style={styles.heroTitle}>纪念日资料</Text><Text style={styles.heroText}>写下名称和日期，之后可以在倒计时页继续准备记录与分享封面。</Text></View><View style={styles.heroImage}><FairyImage name="anniversaryCover" height={92} radius={18} framed={false} /></View></View>
              <FairyInput label="纪念日名称" icon="heart-outline" value={title} onChangeText={(text) => { setTitle(text); setError(''); }} placeholder="例如：相识纪念日" maxLength={32} />
              <FairyInput label="日期" icon="calendar-outline" value={date} onChangeText={(text) => { setDate(text); setError(''); }} placeholder="2026-06-28" keyboardType="numbers-and-punctuation" maxLength={10} />
              <Text style={styles.fieldLabel}>类型</Text>
              <View style={styles.optionRow}>{typeOptions.map((item) => { const active = item.key === type; return <Pressable key={item.key} accessibilityRole="button" accessibilityState={{ selected: active }} onPress={() => setType(item.key)} style={({ pressed }) => [styles.typeOption, active && styles.typeOptionActive, pressed && styles.pressed]}><Ionicons name={item.icon} size={19} color={active ? colors.primaryDeep : colors.accent} /><Text style={[styles.typeText, active && styles.typeTextActive]}>{item.label}</Text></Pressable>; })}</View>
              <View style={styles.settingRow}><View style={styles.settingCopy}><Text style={styles.settingTitle}>每年重复</Text><Text style={styles.settingText}>每年在同一天重新开始倒计时</Text></View><Switch accessibilityLabel="每年重复" value={repeatYearly} onValueChange={setRepeatYearly} trackColor={{ false: '#E7D9D4', true: '#F2B5B8' }} thumbColor={repeatYearly ? '#FFF9F4' : '#F8F6F2'} /></View>
              <Text style={styles.fieldLabel}>提醒</Text>
              <View style={styles.reminderRow}>{reminderOptions.map((days) => { const active = days === reminderDays; return <Pressable key={days} onPress={() => setReminderDays(days)} style={({ pressed }) => [styles.reminderOption, active && styles.reminderActive, pressed && styles.pressed]}><Ionicons name="notifications-outline" size={17} color={active ? colors.primaryDeep : colors.textSoft} /><Text style={[styles.reminderText, active && styles.reminderTextActive]}>提前 {days} 天</Text></Pressable>; })}</View>
              <Text style={styles.fieldLabel}>封面与颜色</Text>
              <View style={styles.coverRow}><Pressable onPress={() => setToast({ visible: true, message: '当前阶段使用绘本封面预览，真实上传将在后续业务接入。', tone: 'info' })} style={({ pressed }) => [styles.coverPreview, pressed && styles.pressed]}><Ionicons name="image-outline" size={23} color={colors.accent} /><Text style={styles.coverPreviewText}>选择封面</Text></Pressable><View style={styles.swatches}>{coverColors.map((value) => { const active = value === coverColor; return <Pressable key={value} accessibilityLabel={`选择封面颜色 ${value}`} onPress={() => setCoverColor(value)} style={[styles.swatch, { backgroundColor: value }, active && styles.swatchActive]}>{active ? <Ionicons name="checkmark" size={21} color={colors.white} /> : null}</Pressable>; })}</View></View>
              <FairyInput label="备注" icon="create-outline" value={note} onChangeText={(text) => { setNote(text); setError(''); }} placeholder="写下这一天的特别意义吧……" multiline maxLength={200} helper={`${note.length}/200`} error={error} />
            </FairyCard>
            <FairyButton title={submitting ? '正在保存…' : isEditMode ? '保存纪念日修改' : '保存纪念日'} disabled={submitting} onPress={save} leftContent={<Ionicons name="sparkles-outline" size={19} color={colors.white} />} />
            <View style={styles.privacyRow}><Ionicons name="lock-closed-outline" size={14} color={colors.gold} /><Text style={styles.privacyText}>仅你们可见，安全记录每份心意</Text></View>
          </>
        )}
      </View>
      <FairyToast visible={toast.visible} tone={toast.tone} message={toast.message} onHide={() => setToast((value) => ({ ...value, visible: false }))} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 720 },
  intro: { alignItems: 'center', marginTop: spacing.md, marginBottom: spacing.xl },
  introTitle: { color: colors.text, fontSize: 19, fontWeight: '900', textAlign: 'center' },
  introText: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.sm, textAlign: 'center' },
  formCard: { marginBottom: spacing.lg, backgroundColor: 'rgba(255,249,244,0.95)' },
  heroRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, marginBottom: spacing.xl },
  heroCopy: { flex: 1 },
  heroTitle: { color: colors.text, fontSize: 18, fontWeight: '900' },
  heroText: { color: colors.textSoft, lineHeight: 19, fontSize: 12, marginTop: spacing.sm },
  heroImage: { width: 118 },
  fieldLabel: { color: colors.text, fontSize: 15, fontWeight: '900', marginBottom: spacing.sm },
  optionRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginBottom: spacing.xl },
  typeOption: { flexGrow: 1, minWidth: 108, minHeight: 46, paddingHorizontal: spacing.md, borderRadius: 18, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  typeOptionActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  typeText: { color: colors.textSoft, fontSize: 13, fontWeight: '800' },
  typeTextActive: { color: colors.primaryDeep },
  settingRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, paddingVertical: spacing.lg, marginBottom: spacing.lg, borderTopWidth: 1, borderBottomWidth: 1, borderColor: colors.border },
  settingCopy: { flex: 1 },
  settingTitle: { color: colors.text, fontSize: 15, fontWeight: '900' },
  settingText: { color: colors.textSoft, fontSize: 11, marginTop: 4 },
  reminderRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginBottom: spacing.xl },
  reminderOption: { flex: 1, minWidth: 118, minHeight: 44, borderRadius: 17, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  reminderActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  reminderText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  reminderTextActive: { color: colors.primaryDeep },
  coverRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.lg, marginBottom: spacing.xl },
  coverPreview: { width: 96, height: 86, borderRadius: 18, alignItems: 'center', justifyContent: 'center', gap: spacing.sm, borderWidth: 1, borderStyle: 'dashed', borderColor: colors.accent, backgroundColor: colors.background },
  coverPreviewText: { color: colors.textSoft, fontSize: 11, fontWeight: '800' },
  swatches: { flex: 1, flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  swatch: { width: 42, height: 42, borderRadius: 21, alignItems: 'center', justifyContent: 'center', borderWidth: 3, borderColor: colors.card },
  swatchActive: { borderColor: colors.primaryDeep, transform: [{ scale: 1.08 }] },
  privacyRow: { minHeight: 42, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm },
  privacyText: { color: colors.textSoft, fontSize: 12 },
  pressed: { opacity: 0.68 },
});