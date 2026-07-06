import { StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import FairyCard from '../../components/FairyCard';
import FairyPage from '../../components/FairyPage';
import colors from '../../theme/colors';
import spacing from '../../theme/spacing';
import typography from '../../theme/typography';
import { devUIRuntimeInfo } from '../runtime/env';
import { navigateTo } from '../runtime/router';

const modules = [
  {
    title: 'Page Explorer',
    subtitle: '页面调试',
    description: '打开已注册页面，并附带 query 参数。',
    icon: 'map-outline',
    path: '/dev-ui-lab/page-explorer',
  },
  {
    title: 'Component Lab',
    subtitle: '组件调试',
    description: '独立预览组件，实时编辑 props。',
    icon: 'cube-outline',
    path: '/dev-ui-lab/component-lab',
  },
  {
    title: 'Mock Center',
    subtitle: '数据调试',
    description: '切换接口 mock 和页面状态模拟。',
    icon: 'flask-outline',
    path: '/dev-ui-lab/mock-center',
  },
];

export default function DevHome() {
  return (
    <FairyPage
      backgroundName="creamPaper"
      topSpace={36}
      bottomSpace={36}
      contentStyle={styles.content}
      showsVerticalScrollIndicator
    >
      <FairyCard radius={28} padding={0} contentStyle={styles.hero}>
        <View style={styles.badge}>
          <Text style={styles.badgeText}>DEV</Text>
        </View>
        <Text style={styles.kicker}>Dev UI Lab v1</Text>
        <Text style={styles.title}>开发调试 UI 实验室</Text>
        <Text style={styles.description}>页面、组件、mock 数据和状态模拟，都在这里脱离业务流程独立检查。</Text>
        <Text style={styles.runtimeText}>
          env: {devUIRuntimeInfo.nodeEnv} / platform: {devUIRuntimeInfo.platform} / force:{' '}
          {devUIRuntimeInfo.forceDevUI ? 'on' : 'off'}
        </Text>
      </FairyCard>

      <View style={styles.grid}>
        {modules.map((item) => (
          <FairyCard
            key={item.path}
            onPress={() => navigateTo(item.path)}
            radius={24}
            padding={0}
            contentStyle={styles.card}
          >
            <View style={styles.cardTop}>
              <View style={styles.iconWrap}>
                <Ionicons name={item.icon} size={24} color={colors.accent} />
              </View>
              <View style={styles.cornerBadge}>
                <Text style={styles.cornerBadgeText}>DEV</Text>
              </View>
            </View>
            <Text style={styles.cardTitle}>{item.title}</Text>
            <Text style={styles.cardSubtitle}>{item.subtitle}</Text>
            <Text style={styles.cardDescription}>{item.description}</Text>
          </FairyCard>
        ))}
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  content: {
    gap: spacing.xl,
  },
  hero: {
    backgroundColor: 'rgba(255, 249, 244, 0.88)',
    borderRadius: 28,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.xxl,
  },
  badge: {
    alignSelf: 'flex-start',
    backgroundColor: '#FFF5DF',
    borderColor: colors.gold,
    borderWidth: 1,
    borderRadius: 12,
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    marginBottom: spacing.md,
  },
  badgeText: {
    color: colors.pencilBrown,
    fontSize: 11,
    fontWeight: '900',
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
    marginTop: spacing.md,
  },
  runtimeText: {
    color: colors.gold,
    fontSize: 11,
    fontWeight: '900',
    marginTop: spacing.md,
  },
  grid: {
    gap: spacing.lg,
  },
  card: {
    backgroundColor: 'rgba(255, 249, 244, 0.94)',
    borderRadius: 24,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.xl,
    minHeight: 156,
  },
  cardTop: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: spacing.md,
  },
  iconWrap: {
    width: 46,
    height: 46,
    borderRadius: 18,
    backgroundColor: '#FFF0F2',
    alignItems: 'center',
    justifyContent: 'center',
  },
  cornerBadge: {
    borderRadius: 10,
    borderWidth: 1,
    borderColor: colors.border,
    paddingHorizontal: spacing.sm,
    paddingVertical: 3,
    backgroundColor: '#FFF5DF',
  },
  cornerBadgeText: {
    color: colors.gold,
    fontSize: 10,
    fontWeight: '900',
  },
  cardTitle: {
    color: colors.text,
    fontSize: 20,
    fontWeight: '900',
  },
  cardSubtitle: {
    color: colors.accent,
    fontSize: 14,
    fontWeight: '800',
    marginTop: spacing.xs,
  },
  cardDescription: {
    ...typography.body,
    color: colors.textSoft,
    marginTop: spacing.sm,
  },
});
