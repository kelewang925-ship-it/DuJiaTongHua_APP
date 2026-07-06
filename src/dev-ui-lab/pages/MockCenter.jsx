import { useEffect, useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import FairyCard from '../../components/FairyCard';
import FairyPage from '../../components/FairyPage';
import colors from '../../theme/colors';
import spacing from '../../theme/spacing';
import typography from '../../theme/typography';
import { devMocks, devPageStates } from '../config/devMocks';
import { getAllMockStates, mockStates, subscribeMockStates, switchMock } from '../runtime/mock';
import { getAllPageStates, pageStates, setPageState, subscribePageStates } from '../runtime/state';

function SegmentedRow({ options, value, onChange }) {
  return (
    <View style={styles.segmentRow}>
      {options.map((option) => {
        const active = option === value;
        return (
          <Pressable
            key={option}
            onPress={() => onChange(option)}
            style={[styles.segment, active && styles.segmentActive]}
          >
            <Text style={[styles.segmentText, active && styles.segmentTextActive]}>{option}</Text>
          </Pressable>
        );
      })}
    </View>
  );
}

export default function MockCenter() {
  const [mockSnapshot, setMockSnapshot] = useState(getAllMockStates());
  const [pageSnapshot, setPageSnapshot] = useState(getAllPageStates());

  useEffect(() => subscribeMockStates(setMockSnapshot), []);
  useEffect(() => subscribePageStates(setPageSnapshot), []);

  const mockRows = useMemo(
    () => devMocks.map((item) => ({ ...item, state: mockSnapshot[item.apiName] || item.defaultState || 'normal' })),
    [mockSnapshot]
  );
  const pageRows = useMemo(
    () =>
      devPageStates.map((item) => ({
        ...item,
        state: pageSnapshot[item.pageName] || item.defaultState || 'hasData',
      })),
    [pageSnapshot]
  );

  return (
    <FairyPage
      backgroundName="creamPaper"
      topSpace={32}
      bottomSpace={36}
      contentStyle={styles.content}
      showsVerticalScrollIndicator
    >
      <View style={styles.header}>
        <Text style={styles.kicker}>Mock Center</Text>
        <Text style={styles.title}>数据模拟</Text>
        <Text style={styles.description}>切换接口 mock 状态，也可以强制指定页面展示状态。</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>接口状态</Text>
        {mockRows.map((item) => (
          <FairyCard key={item.apiName} radius={22} padding={0} contentStyle={styles.rowCard}>
            <View style={styles.rowHeader}>
              <Text style={styles.rowTitle}>{item.label}</Text>
              <Text style={styles.rowKey}>{item.apiName}</Text>
            </View>
            <SegmentedRow
              options={mockStates}
              value={item.state}
              onChange={(state) => switchMock(item.apiName, state)}
            />
          </FairyCard>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>State Simulator</Text>
        {pageRows.map((item) => (
          <FairyCard key={item.pageName} radius={22} padding={0} contentStyle={styles.rowCard}>
            <View style={styles.rowHeader}>
              <Text style={styles.rowTitle}>{item.label}</Text>
              <Text style={styles.rowKey}>{item.pageName}</Text>
            </View>
            <SegmentedRow
              options={pageStates}
              value={item.state}
              onChange={(state) => setPageState(item.pageName, state)}
            />
          </FairyCard>
        ))}
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  content: {
    gap: spacing.lg,
  },
  header: {
    marginBottom: spacing.xs,
  },
  kicker: {
    color: colors.accent,
    fontSize: 13,
    fontWeight: '900',
  },
  title: {
    ...typography.title,
    color: colors.text,
    fontWeight: '900',
    marginTop: spacing.xs,
  },
  description: {
    ...typography.body,
    color: colors.textSoft,
    marginTop: spacing.sm,
  },
  section: {
    gap: spacing.md,
  },
  sectionTitle: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '900',
  },
  rowCard: {
    borderRadius: 22,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: 'rgba(255, 249, 244, 0.94)',
    padding: spacing.lg,
    gap: spacing.md,
  },
  rowHeader: {
    gap: 3,
  },
  rowTitle: {
    color: colors.text,
    fontSize: 16,
    fontWeight: '900',
  },
  rowKey: {
    color: colors.textSoft,
    fontSize: 12,
    fontWeight: '700',
  },
  segmentRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
  },
  segment: {
    minHeight: 36,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: colors.border,
    paddingHorizontal: spacing.md,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.card,
  },
  segmentActive: {
    backgroundColor: colors.primary,
    borderColor: colors.primaryDeep,
  },
  segmentText: {
    color: colors.textSoft,
    fontSize: 12,
    fontWeight: '900',
  },
  segmentTextActive: {
    color: colors.white,
  },
});
