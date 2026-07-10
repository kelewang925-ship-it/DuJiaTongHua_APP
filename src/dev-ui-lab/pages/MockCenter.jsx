import { useEffect, useMemo, useState } from 'react';
import { Alert, Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import FairyCard from '../../components/FairyCard';
import FairyPage from '../../components/FairyPage';
import useFairyStore, { FAIRY_STORE_STORAGE_KEY } from '../../store/useFairyStore';
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

const mockStateDescriptions = [
  { state: 'empty', description: '模拟接口成功返回，但数据为空，用来检查空状态页面。' },
  { state: 'normal', description: '模拟接口正常返回数据，是默认的常规展示状态。' },
  { state: 'loading', description: '模拟接口请求中，用来检查加载态和骨架屏。' },
  { state: 'error', description: '模拟接口请求失败，用来检查错误提示和重试入口。' },
];

export default function MockCenter() {
  const [resetting, setResetting] = useState(false);
  const [mockSnapshot, setMockSnapshot] = useState(getAllMockStates());
  const [pageSnapshot, setPageSnapshot] = useState(getAllPageStates());
  const clearPersistedData = useFairyStore((state) => state.clearPersistedData);

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

  const handleResetStore = async () => {
    if (resetting) return;

    setResetting(true);
    try {
      await clearPersistedData();
      Alert.alert('已重置', '本地持久化数据已清理，并恢复为最新 mockData 初始数据。');
    } finally {
      setResetting(false);
    }
  };

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
        <Text style={styles.description}>
          切换接口 mock 状态，也可以强制指定页面展示状态和重置本地数据。
        </Text>
      </View>

      <FairyCard radius={24} padding={0} contentStyle={styles.toolCard}>
        <View style={styles.toolHeader}>
          <View style={styles.iconWrap}>
            <Ionicons name="refresh-circle-outline" size={24} color={colors.accent} />
          </View>
          <View style={styles.toolTextWrap}>
            <Text style={styles.rowTitle}>重置本地数据</Text>
            <Text style={styles.rowKey}>AsyncStorage</Text>
          </View>
        </View>
        <Text style={styles.cardDescription}>
          清理 {FAIRY_STORE_STORAGE_KEY}，并重新载入当前 mockData。
        </Text>
        <Pressable
          onPress={handleResetStore}
          disabled={resetting}
          style={[styles.resetButton, resetting && styles.resetButtonDisabled]}
        >
          <Text style={styles.resetButtonText}>{resetting ? '正在重置...' : '重置本地数据'}</Text>
        </Pressable>
      </FairyCard>

      <View style={styles.section}>
        <FairyCard radius={22} padding={0} contentStyle={styles.stateHelpCard}>
          <Text style={styles.stateHelpTitle}>状态说明</Text>
          {mockStateDescriptions.map((item) => (
            <View key={item.state} style={styles.stateHelpRow}>
              <Text style={styles.stateHelpBadge}>{item.state}</Text>
              <Text style={styles.stateHelpText}>{item.description}</Text>
            </View>
          ))}
        </FairyCard>
        <Text style={styles.sectionTitle}>接口状态</Text>
        {mockRows.map((item) => (
          <FairyCard key={item.apiName} radius={22} padding={0} contentStyle={styles.rowCard}>
            <View style={styles.rowHeader}>
              <Text style={styles.rowTitle}>{item.label}</Text>
              <Text style={styles.rowKey}>{item.apiName}</Text>
              {item.description ? <Text style={styles.rowDescription}>{item.description}</Text> : null}
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
  stateHelpCard: {
    borderRadius: 22,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: 'rgba(255, 249, 244, 0.94)',
    padding: spacing.lg,
    gap: spacing.sm,
  },
  stateHelpTitle: {
    color: colors.text,
    fontSize: 15,
    fontWeight: '900',
    marginBottom: spacing.xs,
  },
  stateHelpRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: spacing.sm,
  },
  stateHelpBadge: {
    minWidth: 58,
    color: colors.accent,
    fontSize: 12,
    fontWeight: '900',
  },
  stateHelpText: {
    flex: 1,
    color: colors.textSoft,
    fontSize: 12,
    lineHeight: 18,
  },
  toolCard: {
    backgroundColor: 'rgba(255, 249, 244, 0.94)',
    borderRadius: 24,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.xl,
    gap: spacing.md,
  },
  toolHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  toolTextWrap: {
    flex: 1,
  },
  iconWrap: {
    width: 46,
    height: 46,
    borderRadius: 18,
    backgroundColor: '#FFF0F2',
    alignItems: 'center',
    justifyContent: 'center',
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
  rowDescription: {
    color: colors.textSoft,
    fontSize: 13,
    lineHeight: 20,
    marginTop: spacing.xs,
  },
  cardDescription: {
    ...typography.body,
    color: colors.textSoft,
    marginTop: spacing.sm,
  },
  resetButton: {
    minHeight: 42,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primaryDeep,
    paddingHorizontal: spacing.lg,
  },
  resetButtonDisabled: {
    opacity: 0.62,
  },
  resetButtonText: {
    color: colors.white,
    fontSize: 14,
    fontWeight: '900',
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
