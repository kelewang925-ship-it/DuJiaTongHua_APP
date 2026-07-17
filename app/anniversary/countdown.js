import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Switch, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyPage from '../../src/components/FairyPage';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';

function DetailRow({ icon, label, value, onPress, children }) {
  const content = (
    <>
      <View style={styles.detailIcon}>
        <Ionicons name={icon} size={20} color={colors.primaryDeep} />
      </View>
      <View style={styles.detailText}>
        <Text style={styles.detailLabel}>{label}</Text>
        {value ? <Text style={styles.detailValue}>{value}</Text> : null}
      </View>
      {children}
      {onPress ? <Ionicons name="chevron-forward" size={18} color={colors.textSoft} /> : null}
    </>
  );

  if (onPress) {
    return (
      <Pressable accessibilityRole="button" onPress={onPress} style={({ pressed }) => [styles.detailRow, pressed && styles.rowPressed]}>
        {content}
      </Pressable>
    );
  }

  return <View style={styles.detailRow}>{content}</View>;
}

export default function AnniversaryCountdownPage() {
  const { width } = useWindowDimensions();
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const initialTarget = anniversaries[1] || anniversaries[0];
  const [selectedId, setSelectedId] = useState(initialTarget?.id);
  const [reminderEnabled, setReminderEnabled] = useState(true);
  const target = anniversaries.find((item) => item.id === selectedId) || initialTarget;
  const compact = width < 380;

  const days = useMemo(() => {
    const value = Number(target?.days);
    return Number.isFinite(value) && value > 0 ? value : 24;
  }, [target]);

  const togetherDays = Number(anniversaries[0]?.days) || 0;

  return (
    <FairyPage
      backgroundName="creamPaper"
      topSpace={28}
      bottomSpace={56}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
    >
      <View style={styles.content}>
        <FairyHeader
          showBack
          eyebrow="重要章节"
          title="纪念日详情"
          subtitle="每一个重要的日子，都值得被珍藏。"
        />

        <View style={styles.selector}>
          {anniversaries.map((item) => {
            const active = item.id === target?.id;
            return (
              <Pressable
                accessibilityRole="button"
                accessibilityState={{ selected: active }}
                key={item.id}
                onPress={() => setSelectedId(item.id)}
                style={[styles.selectorChip, active && styles.selectorChipActive]}
              >
                <Ionicons name={item.icon || 'heart-outline'} size={15} color={active ? colors.white : colors.accent} />
                <Text numberOfLines={1} style={[styles.selectorText, active && styles.selectorTextActive]}>{item.title}</Text>
              </Pressable>
            );
          })}
        </View>

        <FairyCard padding={0} radius={32} style={styles.heroCard} contentStyle={styles.heroContent}>
          <FairyImage name="anniversaryCover" height={compact ? 210 : 252} radius={28} framed={false} resizeMode="cover" />
          <View style={styles.heroTint} />
          <View style={styles.countdownPanel}>
            <Text style={styles.heroKicker}>我们一起期待的日子</Text>
            <View style={styles.countRow}>
              <Text style={[styles.count, compact && styles.countCompact]}>{days}</Text>
              <Text style={styles.unit}>天</Text>
            </View>
            <Text style={styles.heroTitle}>{target?.title || '第一次一起旅行'}</Text>
          </View>
          <View pointerEvents="none" style={styles.heroSparkles}>
            <Ionicons name="sparkles" size={23} color="#EAB765" />
            <Ionicons name="heart" size={18} color="#EFA09C" />
          </View>
        </FairyCard>

        <FairyCard padding={0} radius={28} contentStyle={styles.detailsCard}>
          <DetailRow icon="heart-circle-outline" label="纪念日名称" value={target?.title || '新的重要章节'} onPress={() => router.push(`/anniversary/edit?id=${target?.id || ''}`)} />
          <DetailRow icon="calendar-outline" label="纪念日日期" value={target?.date || '待设置日期'} onPress={() => router.push(`/anniversary/edit?id=${target?.id || ''}`)} />
          <DetailRow icon="leaf-outline" label="已经一起经历" value={`${togetherDays} 天`} />
          <DetailRow icon="notifications-outline" label="提醒状态">
            <View style={styles.reminderControl}>
              <Text style={styles.reminderText}>{reminderEnabled ? '已开启' : '已关闭'}</Text>
              <Switch
                accessibilityLabel="纪念日提醒"
                value={reminderEnabled}
                onValueChange={setReminderEnabled}
                trackColor={{ false: '#E7D9D4', true: '#F2B5B8' }}
                thumbColor={reminderEnabled ? '#FFF9F4' : '#F8F6F2'}
              />
            </View>
          </DetailRow>
        </FairyCard>

        <Pressable
          accessibilityRole="button"
          onPress={() => router.push('/anniversary/template')}
          style={({ pressed }) => [styles.relatedCard, pressed && styles.rowPressed]}
        >
          <View style={styles.relatedIcon}><Ionicons name="book-outline" size={24} color={colors.primaryDeep} /></View>
          <View style={styles.relatedText}>
            <Text style={styles.relatedTitle}>相关记录</Text>
            <Text style={styles.relatedSubtitle}>一起记录的点滴回忆</Text>
          </View>
          <Text style={styles.relatedCount}>6 条</Text>
          <Ionicons name="chevron-forward" size={20} color={colors.textSoft} />
        </Pressable>

        <View style={styles.actions}>
          <FairyButton
            title="写一篇纪念日记录"
            leftContent={<Ionicons name="create-outline" size={20} color={colors.white} />}
            onPress={() => router.push('/anniversary/template')}
          />
          <FairyButton
            title="生成分享封面"
            leftContent={<Ionicons name="color-wand-outline" size={20} color={colors.primaryDeep} />}
            variant="secondary"
            onPress={() => router.push('/share-preview')}
          />
        </View>
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: {
    alignItems: 'center',
  },
  content: {
    width: '100%',
    maxWidth: 720,
  },
  selector: {
    marginTop: spacing.lg,
    marginBottom: spacing.lg,
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
  },
  selectorChip: {
    maxWidth: '100%',
    minHeight: 38,
    paddingHorizontal: spacing.md,
    borderRadius: 18,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: 'rgba(255, 249, 244, 0.9)',
  },
  selectorChipActive: {
    backgroundColor: colors.primaryDeep,
    borderColor: colors.primaryDeep,
  },
  selectorText: {
    flexShrink: 1,
    color: colors.textSoft,
    fontSize: 12,
    fontWeight: '800',
  },
  selectorTextActive: {
    color: colors.white,
  },
  heroCard: {
    marginBottom: spacing.lg,
    overflow: 'hidden',
    backgroundColor: colors.card,
  },
  heroContent: {
    minHeight: 360,
    padding: spacing.sm,
  },
  heroTint: {
    position: 'absolute',
    left: spacing.sm,
    right: spacing.sm,
    bottom: spacing.sm,
    height: 154,
    borderRadius: 26,
    backgroundColor: 'rgba(255, 249, 244, 0.93)',
  },
  countdownPanel: {
    marginTop: -44,
    minHeight: 164,
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.lg,
    borderRadius: 26,
    alignItems: 'center',
    backgroundColor: 'rgba(255, 249, 244, 0.96)',
    borderWidth: 1,
    borderColor: 'rgba(216, 179, 132, 0.24)',
  },
  heroKicker: {
    color: colors.textSoft,
    fontSize: 14,
    fontWeight: '800',
  },
  countRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    justifyContent: 'center',
  },
  count: {
    color: '#E98188',
    fontSize: 68,
    lineHeight: 76,
    fontWeight: '900',
  },
  countCompact: {
    fontSize: 60,
  },
  unit: {
    marginLeft: spacing.sm,
    marginBottom: 10,
    color: colors.text,
    fontSize: 22,
    fontWeight: '800',
  },
  heroTitle: {
    color: colors.text,
    fontSize: 20,
    fontWeight: '900',
    textAlign: 'center',
  },
  heroSparkles: {
    position: 'absolute',
    top: spacing.xl,
    right: spacing.xl,
    gap: spacing.sm,
  },
  detailsCard: {
    paddingHorizontal: spacing.lg,
    backgroundColor: 'rgba(255, 249, 244, 0.96)',
  },
  detailRow: {
    minHeight: 74,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: 'rgba(176, 138, 143, 0.22)',
  },
  detailIcon: {
    width: 38,
    height: 38,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.cardPink,
  },
  detailText: {
    flex: 1,
    gap: 4,
  },
  detailLabel: {
    color: colors.text,
    fontSize: 14,
    fontWeight: '900',
  },
  detailValue: {
    color: colors.textSoft,
    fontSize: 13,
  },
  reminderControl: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  reminderText: {
    color: colors.primaryDeep,
    fontSize: 12,
    fontWeight: '800',
  },
  relatedCard: {
    minHeight: 92,
    marginTop: spacing.lg,
    paddingHorizontal: spacing.lg,
    borderRadius: 26,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    backgroundColor: 'rgba(255, 240, 242, 0.9)',
    borderWidth: 1,
    borderColor: colors.border,
  },
  relatedIcon: {
    width: 48,
    height: 48,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.card,
  },
  relatedText: {
    flex: 1,
  },
  relatedTitle: {
    color: colors.text,
    fontSize: 16,
    fontWeight: '900',
  },
  relatedSubtitle: {
    marginTop: 4,
    color: colors.textSoft,
    fontSize: 12,
  },
  relatedCount: {
    color: colors.text,
    fontWeight: '800',
  },
  actions: {
    marginTop: spacing.xl,
    gap: spacing.md,
  },
  rowPressed: {
    opacity: 0.82,
  },
});
