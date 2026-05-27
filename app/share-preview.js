import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import FairyButton from '../src/components/FairyButton';
import FairyCard from '../src/components/FairyCard';
import FairyHeader from '../src/components/FairyHeader';
import FairyPage from '../src/components/FairyPage';
import FairyTag from '../src/components/FairyTag';
import FairyToast from '../src/components/FairyToast';
import colors from '../src/theme/colors';
import spacing from '../src/theme/spacing';
import useFairyStore from '../src/store/useFairyStore';

const privacyOptions = ['显示昵称', '显示日期', '显示地点'];

export default function SharePreviewPage() {
  const records = useFairyStore((state) => state.records);
  const latest = records[0];
  const [selected, setSelected] = useState(['显示昵称', '显示日期']);
  const [style, setStyle] = useState('绘本卡片');
  const [toastVisible, setToastVisible] = useState(false);

  const toggleOption = (option) => {
    setSelected((items) => (items.includes(option) ? items.filter((item) => item !== option) : [...items, option]));
  };

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="特殊页面"
        title="分享预览"
        subtitle="先看看对外展示的样子，再把这一页温柔地分享出去。"
        right={<FairyTag tone="gold">隐私优先</FairyTag>}
      />

      <FairyCard style={styles.previewCard}>
        <View style={styles.cardTape} />
        <Text style={styles.cardTitle}>我们的一页童话</Text>
        <Text style={styles.cardDesc}>{latest?.content || '每段回忆，都值得被收藏。'}</Text>
        <View style={styles.metaRow}>
          <FairyTag>{latest?.type || '日记'}</FairyTag>
          <FairyTag tone="gold">{style}</FairyTag>
        </View>
      </FairyCard>

      <Text style={styles.sectionTitle}>分享样式</Text>
      <View style={styles.row}>
        {['绘本卡片', '拍立得拼贴'].map((item) => (
          <Pressable
            key={item}
            style={[styles.chip, style === item && styles.activeChip]}
            onPress={() => setStyle(item)}
          >
            <Text style={[styles.chipText, style === item && styles.activeText]}>{item}</Text>
          </Pressable>
        ))}
      </View>

      <Text style={styles.sectionTitle}>隐私控制</Text>
      <View style={styles.optionList}>
        {privacyOptions.map((option) => {
          const active = selected.includes(option);
          return (
            <Pressable key={option} style={styles.optionItem} onPress={() => toggleOption(option)}>
              <View style={[styles.checkDot, active && styles.checkDotActive]}>
                {active ? <Ionicons name="checkmark" size={12} color={colors.white} /> : null}
              </View>
              <Text style={styles.optionText}>{option}</Text>
            </Pressable>
          );
        })}
      </View>

      <View style={styles.actions}>
        <FairyButton title="生成分享图（mock）" onPress={() => setToastVisible(true)} />
        <FairyButton title="返回继续调整内容" variant="secondary" onPress={() => {}} />
      </View>

      <FairyToast
        visible={toastVisible}
        tone="success"
        message="分享图已加入 mock 生成队列。"
        onHide={() => setToastVisible(false)}
      />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  previewCard: {
    backgroundColor: colors.cardPink,
    marginBottom: spacing.xl,
    overflow: 'hidden',
  },
  cardTape: {
    position: 'absolute',
    width: 76,
    height: 18,
    borderRadius: 8,
    top: 12,
    right: 16,
    backgroundColor: 'rgba(216, 179, 132, 0.2)',
  },
  cardTitle: {
    color: colors.text,
    fontSize: 20,
    fontWeight: '900',
    marginTop: 8,
  },
  cardDesc: {
    color: colors.textSoft,
    lineHeight: 21,
    marginTop: 8,
  },
  metaRow: {
    flexDirection: 'row',
    gap: spacing.sm,
    marginTop: spacing.lg,
  },
  sectionTitle: {
    color: colors.text,
    fontSize: 17,
    fontWeight: '900',
    marginBottom: spacing.sm,
  },
  row: {
    flexDirection: 'row',
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  chip: {
    flex: 1,
    borderRadius: 16,
    paddingVertical: spacing.sm,
    alignItems: 'center',
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
  },
  activeChip: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
  chipText: {
    color: colors.textSoft,
    fontWeight: '700',
  },
  activeText: {
    color: colors.white,
  },
  optionList: {
    gap: spacing.sm,
    marginBottom: spacing.xl,
  },
  optionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    padding: spacing.md,
    borderRadius: 14,
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
  },
  checkDot: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: colors.border,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.cardPink,
  },
  checkDotActive: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
  optionText: {
    color: colors.text,
    fontWeight: '700',
  },
  actions: {
    gap: spacing.md,
  },
});
