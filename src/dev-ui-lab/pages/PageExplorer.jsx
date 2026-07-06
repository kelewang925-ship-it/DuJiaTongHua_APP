import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import FairyPage from '../../components/FairyPage';
import colors from '../../theme/colors';
import spacing from '../../theme/spacing';
import typography from '../../theme/typography';
import shadows from '../../theme/shadows';
import { devPages, devPageStatusMeta } from '../config/devPages';
import { navigateTo } from '../runtime/router';

export default function PageExplorer() {
  return (
    <FairyPage
      backgroundName="creamPaper"
      topSpace={32}
      bottomSpace={36}
      contentStyle={styles.content}
      showsVerticalScrollIndicator
    >
      <View style={styles.header}>
        <Text style={styles.kicker}>Page Explorer</Text>
        <Text style={styles.title}>页面调试</Text>
        <Text style={styles.description}>点击页面即可用配置里的 query 参数进入目标路由。</Text>
      </View>

      {devPages.map((page) => {
        const status = devPageStatusMeta[page.uiStatus] || devPageStatusMeta.pending;

        return (
          <Pressable
            key={`${page.name}-${page.path}`}
            onPress={() => navigateTo(page.path, page.query)}
            style={({ pressed }) => [styles.pageCard, pressed && styles.pressed]}
          >
            <View style={styles.pageText}>
              <View style={styles.metaRow}>
                <Text style={styles.moduleName}>{page.module}</Text>
                <View style={[styles.statusBadge, { backgroundColor: status.backgroundColor }]}>
                  <Text style={[styles.statusText, { color: status.color }]}>{status.label}</Text>
                </View>
              </View>
              <Text style={styles.pageName}>{page.name}</Text>
              <Text style={styles.pagePath}>{page.path}</Text>
              <Text style={styles.filePath}>{page.file}</Text>
              {page.design ? <Text style={styles.designPath}>{page.design}</Text> : null}
              {page.note ? <Text style={styles.note}>{page.note}</Text> : null}
              {page.query ? <Text style={styles.query}>query: {JSON.stringify(page.query)}</Text> : null}
            </View>
            <Ionicons name="chevron-forward" size={22} color={colors.textSoft} />
          </Pressable>
        );
      })}
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  content: {
    gap: spacing.md,
  },
  header: {
    marginBottom: spacing.sm,
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
  pageCard: {
    minHeight: 146,
    borderRadius: 22,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: 'rgba(255, 249, 244, 0.94)',
    padding: spacing.lg,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.md,
    ...shadows.card,
  },
  pressed: {
    transform: [{ scale: 0.98 }],
    opacity: 0.88,
  },
  pageText: {
    flex: 1,
    gap: 4,
  },
  metaRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.sm,
    marginBottom: 2,
  },
  moduleName: {
    color: colors.gold,
    fontSize: 12,
    fontWeight: '900',
    flex: 1,
  },
  statusBadge: {
    minHeight: 24,
    borderRadius: 10,
    paddingHorizontal: spacing.sm,
    alignItems: 'center',
    justifyContent: 'center',
  },
  statusText: {
    fontSize: 11,
    fontWeight: '900',
  },
  pageName: {
    color: colors.text,
    fontSize: 17,
    fontWeight: '900',
  },
  pagePath: {
    color: colors.accent,
    fontSize: 12,
    fontWeight: '800',
  },
  filePath: {
    color: colors.text,
    fontSize: 12,
    fontWeight: '700',
  },
  designPath: {
    color: colors.textSoft,
    fontSize: 11,
  },
  note: {
    color: colors.textSoft,
    fontSize: 12,
    lineHeight: 18,
  },
  query: {
    color: colors.textSoft,
    fontSize: 12,
  },
});
