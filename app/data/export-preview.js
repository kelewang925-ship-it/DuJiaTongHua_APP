import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';

const sections = [
  { key: 'diary', label: '日记纸页', icon: 'book-outline' },
  { key: 'photo', label: '照片贴纸', icon: 'images-outline' },
  { key: 'ai', label: '童话工坊', icon: 'sparkles-outline', tone: 'gold' },
  { key: 'anniversary', label: '纪念日章节', icon: 'calendar-outline' },
];

export default function ExportPreviewPage() {
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const [included, setIncluded] = useState({ diary: true, photo: true, ai: true, anniversary: true });
  const [styleName, setStyleName] = useState('奶油纸绘本');
  const [exported, setExported] = useState(false);
  const [toastVisible, setToastVisible] = useState(false);

  const counts = useMemo(
    () => ({
      diary: records.filter((item) => item.type === '日记').length,
      photo: records.filter((item) => item.type === '照片').reduce((sum, item) => sum + (item.photoCount || 3), 0),
      ai: creations.length,
      anniversary: anniversaries.length,
    }),
    [anniversaries.length, creations.length, records]
  );

  const selectedCount = sections.reduce((sum, section) => (included[section.key] ? sum + counts[section.key] : sum), 0);
  const previewPages = Math.max(4, Math.ceil(selectedCount / 2) + 2);

  const toggleSection = (key) => {
    setIncluded((value) => ({ ...value, [key]: !value[key] }));
    setExported(false);
  };

  const confirmExport = () => {
    setExported(true);
    setToastVisible(true);
  };

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="数据管理"
        title="导出预览"
        subtitle="在生成 PDF 前，先翻看这本回忆册的封面、目录和章节。"
        right={<FairyTag tone="gold">{previewPages} 页预览</FairyTag>}
      />

      <FairyCard style={styles.coverCard}>
        <FairyImage name="exportCover" height={210} radius={26} />
        <Text style={styles.coverTitle}>我们的恋爱回忆册</Text>
        <Text style={styles.coverText}>{styleName} · 预计收录 {selectedCount} 枚回忆印记</Text>
        <View style={styles.coverTags}>
          <FairyTag>封面</FairyTag>
          <FairyTag>目录</FairyTag>
          <FairyTag tone="gold">章节页</FairyTag>
        </View>
      </FairyCard>

      <Text style={styles.sectionTitle}>选择要装订的章节</Text>
      <View style={styles.sectionGrid}>
        {sections.map((section) => (
          <Pressable key={section.key} onPress={() => toggleSection(section.key)} style={styles.sectionItemWrap}>
            <FairyCard style={[styles.sectionItem, included[section.key] && styles.sectionItemActive]}>
              <View style={[styles.sectionIcon, section.tone === 'gold' && styles.goldIcon]}>
                <Ionicons name={section.icon} size={22} color={section.tone === 'gold' ? colors.gold : colors.accent} />
              </View>
              <Text style={styles.sectionLabel}>{section.label}</Text>
              <Text style={styles.sectionCount}>{counts[section.key]} 项</Text>
              <View style={[styles.checkDot, included[section.key] && styles.checkDotActive]}>
                {included[section.key] ? <Ionicons name="checkmark" size={14} color={colors.white} /> : null}
              </View>
            </FairyCard>
          </Pressable>
        ))}
      </View>

      <Text style={styles.sectionTitle}>绘本样式</Text>
      <View style={styles.styleRow}>
        {['奶油纸绘本', '玫瑰手帐'].map((item) => (
          <Pressable
            key={item}
            onPress={() => {
              setStyleName(item);
              setExported(false);
            }}
            style={[styles.styleChip, styleName === item && styles.styleChipActive]}
          >
            <Text style={[styles.styleChipText, styleName === item && styles.styleChipTextActive]}>{item}</Text>
          </Pressable>
        ))}
      </View>

      <FairyCard style={styles.timelineCard}>
        <Text style={styles.timelineTitle}>预览目录</Text>
        {[
          '封面 · 独家童话',
          included.diary ? '第一章 · 被写下的日常' : null,
          included.photo ? '第二章 · 贴在纸上的照片' : null,
          included.ai ? '第三章 · 魔法发生的地方' : null,
          included.anniversary ? '附录 · 重要日子的金色书签' : null,
        ].filter(Boolean).map((item, index) => (
          <View key={item} style={styles.timelineRow}>
            <Text style={styles.timelineIndex}>{index + 1}</Text>
            <Text style={styles.timelineText}>{item}</Text>
          </View>
        ))}
      </FairyCard>

      {exported ? (
        <FairyCard style={styles.doneCard}>
          <Ionicons name="checkmark-circle-outline" size={26} color={colors.gold} />
          <Text style={styles.doneText}>导出任务已放进 mock 队列，等真实 PDF 能力接入后就会在这里生成文件。</Text>
        </FairyCard>
      ) : null}

      <View style={styles.actions}>
        <FairyButton title="确认装订这本回忆册" onPress={confirmExport} disabled={selectedCount === 0} />
        <FairyButton title="返回修改导出配置" variant="secondary" onPress={() => setExported(false)} />
      </View>
      <FairyToast visible={toastVisible} tone="success" message="导出任务已加入队列，稍后会在回忆册记录里出现。" onHide={() => setToastVisible(false)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  coverCard: { backgroundColor: colors.cardPink, marginBottom: spacing.xl, overflow: 'hidden' },
  coverTitle: { color: colors.text, fontSize: 22, fontWeight: '900', marginTop: spacing.md, textAlign: 'center' },
  coverText: { color: colors.textSoft, lineHeight: 21, textAlign: 'center', marginTop: spacing.sm },
  coverTags: { flexDirection: 'row', justifyContent: 'center', gap: spacing.sm, marginTop: spacing.lg },
  sectionTitle: { color: colors.text, fontSize: 18, fontWeight: '900', marginBottom: spacing.md },
  sectionGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md, marginBottom: spacing.xl },
  sectionItemWrap: { width: '47%' },
  sectionItem: { minHeight: 142, padding: spacing.md },
  sectionItemActive: { backgroundColor: '#FFF3F5' },
  sectionIcon: { width: 44, height: 44, borderRadius: 17, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink, marginBottom: spacing.md },
  goldIcon: { backgroundColor: '#FFF5DF' },
  sectionLabel: { color: colors.text, fontWeight: '900' },
  sectionCount: { color: colors.textSoft, marginTop: spacing.xs },
  checkDot: { position: 'absolute', right: spacing.md, top: spacing.md, width: 24, height: 24, borderRadius: 12, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' },
  checkDotActive: { backgroundColor: colors.primary, borderColor: colors.primary },
  styleRow: { flexDirection: 'row', gap: spacing.sm, marginBottom: spacing.xl },
  styleChip: { flex: 1, alignItems: 'center', borderRadius: 18, paddingVertical: spacing.md, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border },
  styleChipActive: { backgroundColor: colors.primary, borderColor: colors.primary },
  styleChipText: { color: colors.textSoft, fontWeight: '800' },
  styleChipTextActive: { color: colors.white },
  timelineCard: { marginBottom: spacing.lg },
  timelineTitle: { color: colors.text, fontSize: 17, fontWeight: '900', marginBottom: spacing.md },
  timelineRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, marginBottom: spacing.sm },
  timelineIndex: { width: 26, height: 26, borderRadius: 13, backgroundColor: colors.cardPink, color: colors.accent, textAlign: 'center', lineHeight: 26, fontWeight: '900', overflow: 'hidden' },
  timelineText: { flex: 1, color: colors.textSoft, lineHeight: 20 },
  doneCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, backgroundColor: '#FFF5DF', marginBottom: spacing.lg },
  doneText: { flex: 1, color: colors.text, lineHeight: 21 },
  actions: { gap: spacing.md },
});
