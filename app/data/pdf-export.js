import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyPage from '@/components/FairyPage';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';
import { hasCapability } from '@/config/capabilities';
import { message } from '@/components/FairyMessage';

const rangeOptions = [
  { key: 'all', label: '全部回忆' },
  { key: 'custom', label: '自定义' },
  { key: 'timeline', label: '按时间线' },
];

const contentOptions = [
  { key: 'diary', label: '日记', icon: 'book-outline' },
  { key: 'photo', label: '照片', icon: 'images-outline' },
  { key: 'anniversary', label: '纪念日', icon: 'calendar-outline' },
  { key: 'ai', label: 'AI 作品', icon: 'sparkles-outline' },
];

const coverOptions = [
  { key: 'romance', label: '浪漫手绘', image: 'pdfMemoryBookCover' },
  { key: 'stars', label: '星空童话', image: 'anniversaryShareCover' },
  { key: 'garden', label: '复古花园', image: 'sharePreviewCover' },
  { key: 'watercolor', label: '清新水彩', image: 'albumCover' },
  { key: 'journal', label: '简约手帐', image: 'homeCover' },
];

function getRecordTime(item) {
  const value = item?.date || item?.anniversaryDate || item?.createdAt || item?.updatedAt;
  const time = value ? new Date(value).getTime() : Number.NaN;
  return Number.isFinite(time) ? time : null;
}

function formatRangeDate(time) {
  if (!Number.isFinite(time)) return null;
  const date = new Date(time);
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`;
}

export default function PdfExportPage() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const [range, setRange] = useState('all');
  const [contents, setContents] = useState({ diary: true, photo: true, anniversary: true, ai: true });
  const [cover, setCover] = useState('romance');
  const [paper, setPaper] = useState('A4');
  const [quality, setQuality] = useState('高清');
  const wide = width >= 760;
  const counts = useMemo(() => ({
    diary: records.filter((item) => item.type === '日记').length,
    photo: records.filter((item) => item.type === '照片').reduce((sum, item) => sum + (Number.isFinite(item.photoCount) ? item.photoCount : 0), 0),
    anniversary: anniversaries.length,
    ai: creations.length,
  }), [anniversaries.length, creations.length, records]);
  const selectedCount = contentOptions.reduce((sum, item) => contents[item.key] ? sum + counts[item.key] : sum, 0);
  const activeCover = coverOptions.find((item) => item.key === cover) || coverOptions[0];
  const loadedRange = useMemo(() => {
    const times = [...records, ...creations, ...anniversaries].map(getRecordTime).filter(Number.isFinite).sort((a, b) => a - b);
    if (!times.length) return null;
    return `${formatRangeDate(times[0])} ～ ${formatRangeDate(times[times.length - 1])}`;
  }, [anniversaries, creations, records]);
  const rangeLabel = range === 'all'
    ? (loadedRange || '当前没有可计算的记录日期')
    : range === 'timeline'
      ? '按已加载记录的时间顺序编排'
      : '尚未选择自定义日期';

  const openPreview = () => {
    if (selectedCount === 0) { message.info('当前选择中没有可导出的真实内容。'); return; }
    if (range === 'custom') { message.info('请先选择自定义日期范围。'); return; }
    if (!hasCapability('pdfExport')) { message.info('Real 模式暂未开放 PDF 生成。'); return; }
    const included = contentOptions.filter((item) => contents[item.key] && counts[item.key] > 0).map((item) => item.key).join(',');
    router.push({ pathname: '/data/export-preview', params: { range, included, cover, paper, quality } });
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="导出回忆绘本" />}
      topSpace={28}
      bottomSpace={60}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
    >
      <View style={styles.content}>
        <View style={styles.intro}>
          <Text style={styles.introTitle}>将我们的点滴回忆，编织成一本专属绘本</Text>
          <Text style={styles.introText}>选择内容、封面和清晰度，先生成预览再确认导出。</Text>
        </View>

        <FairyCard padding={0} radius={30} style={styles.heroCard} contentStyle={styles.heroContent}>
          <FairyImage name={activeCover.image} height={wide ? 310 : 240} radius={28} framed={false} resizeMode="cover" />
          <View style={styles.heroShade} />
          <View style={styles.heroCopy}>
            <Text style={styles.heroKicker}>我们的独家童话</Text>
            <Text style={styles.heroTitle}>恋爱回忆绘本</Text>
            <Text style={styles.heroText}>{selectedCount > 0 ? `预计收录 ${selectedCount} 枚回忆印记` : '当前选择中没有可导出的回忆'}</Text>
          </View>
        </FairyCard>

        <FairyCard style={styles.configCard}>
          <ConfigTitle icon="calendar-outline" title="导出范围" subtitle="选择要包含的回忆范围" />
          <View style={styles.segmented}>
            {rangeOptions.map((item) => <OptionChip key={item.key} label={item.label} active={range === item.key} onPress={() => setRange(item.key)} />)}
          </View>
          <Pressable accessibilityRole="button" onPress={() => setRange('custom')} style={({ pressed }) => [styles.datePicker, pressed && styles.pressed]}>
            <Ionicons name="calendar-number-outline" size={20} color={colors.primaryDeep} />
            <Text style={styles.dateText}>{rangeLabel}</Text>
            <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
          </Pressable>

          <View style={styles.divider} />
          <ConfigTitle icon="file-tray-full-outline" title="内容类型" subtitle="选择要包含的内容" />
          <View style={styles.contentOptions}>
            {contentOptions.map((item) => {
              const active = contents[item.key];
              const unavailable = counts[item.key] === 0;
              return (
                <Pressable
                  key={item.key}
                  disabled={unavailable}
                  onPress={() => setContents((value) => ({ ...value, [item.key]: !value[item.key] }))}
                  style={({ pressed }) => [styles.contentOption, active && !unavailable && styles.contentOptionActive, unavailable && styles.contentOptionDisabled, pressed && styles.pressed]}
                >
                  <View style={[styles.checkbox, active && !unavailable && styles.checkboxActive]}>{active && !unavailable ? <Ionicons name="checkmark" size={15} color={colors.white} /> : null}</View>
                  <Ionicons name={item.icon} size={18} color={active && !unavailable ? colors.primaryDeep : colors.textSoft} />
                  <Text style={[styles.contentOptionText, active && !unavailable && styles.contentOptionTextActive]}>{item.label}</Text>
                  <Text style={styles.contentCount}>{counts[item.key]}</Text>
                </Pressable>
              );
            })}
          </View>

          <View style={styles.divider} />
          <ConfigTitle icon="book-outline" title="封面样式" subtitle="选择绘本封面风格" />
          <View style={styles.coverGrid}>
            {coverOptions.map((item) => {
              const active = cover === item.key;
              return (
                <Pressable key={item.key} onPress={() => setCover(item.key)} style={({ pressed }) => [styles.coverOption, wide && styles.coverOptionWide, active && styles.coverOptionActive, pressed && styles.pressed]}>
                  <FairyImage name={item.image} height={wide ? 138 : 118} radius={14} framed={false} resizeMode="cover" />
                  <Text numberOfLines={1} style={[styles.coverLabel, active && styles.coverLabelActive]}>{item.label}</Text>
                  {active ? <View style={styles.coverCheck}><Ionicons name="checkmark" size={17} color={colors.white} /></View> : null}
                </Pressable>
              );
            })}
          </View>

          <View style={styles.divider} />
          <ConfigTitle icon="documents-outline" title="纸张与清晰度" subtitle="选择输出规格" />
          <View style={styles.specRow}>
            <View style={styles.specGroup}>
              <Text style={styles.specLabel}>纸张尺寸</Text>
              <View style={styles.specOptions}>{['A4', 'A5', '正方形'].map((item) => <OptionChip key={item} label={item} active={paper === item} onPress={() => setPaper(item)} compact />)}</View>
            </View>
            <View style={styles.specGroup}>
              <Text style={styles.specLabel}>清晰度</Text>
              <View style={styles.specOptions}>{['标准', '高清', '超清'].map((item) => <OptionChip key={item} label={item} active={quality === item} onPress={() => setQuality(item)} compact />)}</View>
            </View>
          </View>
        </FairyCard>

        <FairyCard style={styles.memberCard} padding={spacing.lg}>
          <View style={styles.memberIcon}><Ionicons name="diamond-outline" size={23} color={colors.gold} /></View>
          <View style={styles.memberCopy}>
            <Text style={styles.memberTitle}>PDF 导出能力</Text>
            <Text style={styles.memberText}>{hasCapability('pdfExport') ? '可根据已加载的真实记录生成预览。' : 'Real 模式暂未开放 PDF 生成、下载和分享。'}</Text>
          </View>
          <Ionicons name={hasCapability('pdfExport') ? 'chevron-forward' : 'lock-closed-outline'} size={18} color={colors.textSoft} />
        </FairyCard>

        <FairyButton title={selectedCount > 0 ? '生成预览' : '没有可导出内容'} disabled={selectedCount === 0} onPress={openPreview} leftContent={<Ionicons name={selectedCount > 0 ? 'color-wand-outline' : 'lock-closed-outline'} size={20} color={colors.white} />} />
        <Text style={styles.footerNote}>{hasCapability('pdfExport') ? '输出规格以生成结果为准' : '当前仅展示配置，不会生成真实文件'}</Text>
      </View>
    </FairyPage>
  );
}

function ConfigTitle({ icon, title, subtitle }) {
  return <View style={styles.configTitleRow}><View style={styles.configIcon}><Ionicons name={icon} size={20} color={colors.primaryDeep} /></View><View><Text style={styles.configTitle}>{title}</Text><Text style={styles.configSubtitle}>{subtitle}</Text></View></View>;
}

function OptionChip({ label, active, onPress, compact = false }) {
  return <Pressable accessibilityRole="button" accessibilityState={{ selected: active }} onPress={onPress} style={({ pressed }) => [styles.optionChip, compact && styles.optionChipCompact, active && styles.optionChipActive, pressed && styles.pressed]}><Text style={[styles.optionChipText, active && styles.optionChipTextActive]}>{label}</Text></Pressable>;
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 860 },
  intro: { alignItems: 'center', marginTop: spacing.md, marginBottom: spacing.xl },
  introTitle: { color: colors.text, fontSize: 18, fontWeight: '900', textAlign: 'center' },
  introText: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.sm, textAlign: 'center' },
  heroCard: { marginBottom: spacing.xl, overflow: 'hidden' },
  heroContent: { padding: spacing.sm },
  heroShade: { position: 'absolute', left: spacing.sm, right: spacing.sm, bottom: spacing.sm, height: 108, borderRadius: 24, backgroundColor: 'rgba(82,52,47,0.32)' },
  heroCopy: { position: 'absolute', left: spacing.xl, right: spacing.xl, bottom: spacing.xl, alignItems: 'center' },
  heroKicker: { color: colors.white, fontSize: 12, fontWeight: '800' },
  heroTitle: { color: colors.white, fontSize: 25, fontWeight: '900', marginTop: 3 },
  heroText: { color: 'rgba(255,255,255,0.88)', fontSize: 12, marginTop: 4 },
  configCard: { marginBottom: spacing.lg },
  configTitleRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, marginBottom: spacing.md },
  configIcon: { width: 42, height: 42, borderRadius: 16, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  configTitle: { color: colors.text, fontSize: 17, fontWeight: '900' },
  configSubtitle: { color: colors.textSoft, fontSize: 11, marginTop: 3 },
  segmented: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  optionChip: { minHeight: 40, flexGrow: 1, paddingHorizontal: spacing.lg, borderRadius: 17, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  optionChipCompact: { minHeight: 36, paddingHorizontal: spacing.md },
  optionChipActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  optionChipText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  optionChipTextActive: { color: colors.primaryDeep },
  datePicker: { minHeight: 52, marginTop: spacing.md, paddingHorizontal: spacing.lg, borderRadius: 18, flexDirection: 'row', alignItems: 'center', gap: spacing.md, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  dateText: { flex: 1, color: colors.text, fontSize: 13, fontWeight: '800' },
  divider: { height: 1, backgroundColor: colors.border, marginVertical: spacing.xl },
  contentOptions: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  contentOption: { minWidth: 138, flex: 1, minHeight: 48, paddingHorizontal: spacing.md, borderRadius: 17, flexDirection: 'row', alignItems: 'center', gap: spacing.sm, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  contentOptionActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  contentOptionDisabled: { opacity: 0.48 },
  checkbox: { width: 22, height: 22, borderRadius: 7, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card },
  checkboxActive: { borderColor: colors.primaryDeep, backgroundColor: colors.primaryDeep },
  contentOptionText: { flex: 1, color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  contentOptionTextActive: { color: colors.text },
  contentCount: { color: colors.primaryDeep, fontSize: 11, fontWeight: '900' },
  coverGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  coverOption: { width: '31.4%', minWidth: 102, position: 'relative', padding: spacing.xs, borderRadius: 17, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  coverOptionWide: { width: '18.8%' },
  coverOptionActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  coverLabel: { color: colors.textSoft, fontSize: 10, fontWeight: '800', textAlign: 'center', paddingVertical: spacing.sm },
  coverLabelActive: { color: colors.primaryDeep },
  coverCheck: { position: 'absolute', top: -6, right: -6, width: 26, height: 26, borderRadius: 13, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.primaryDeep, borderWidth: 2, borderColor: colors.white },
  specRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.lg },
  specGroup: { flex: 1, minWidth: 230 },
  specLabel: { color: colors.textSoft, fontSize: 12, fontWeight: '800', marginBottom: spacing.sm },
  specOptions: { flexDirection: 'row', gap: spacing.sm },
  memberCard: { marginBottom: spacing.lg, flexDirection: 'row', alignItems: 'center', gap: spacing.md, backgroundColor: '#FFF8E8' },
  memberIcon: { width: 46, height: 46, borderRadius: 18, alignItems: 'center', justifyContent: 'center', backgroundColor: '#FFF0C9' },
  memberCopy: { flex: 1 },
  memberTitle: { color: colors.text, fontSize: 15, fontWeight: '900' },
  memberText: { color: colors.textSoft, fontSize: 11, lineHeight: 17, marginTop: 4 },
  footerNote: { color: colors.textSoft, fontSize: 11, textAlign: 'center', marginTop: spacing.md },
  pressed: { opacity: 0.68 },
});