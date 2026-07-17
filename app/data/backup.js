import { StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyPage from '../../src/components/FairyPage';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';
import { hasCapability } from '../../src/config/capabilities';

export default function BackupPage() {
  const backupAvailable = hasCapability('cloudBackup');
  const getStats = useFairyStore((state) => state.getStats);
  const stats = getStats();
  const totalItems = stats.diaryCount + stats.photoCount + stats.creationCount;

  return (
    <FairyPage
      backgroundName="creamPaper"
      topSpace={28}
      bottomSpace={64}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
      header={<FairyHeader showBack eyebrow="数据管理" title="备份与恢复" subtitle="把一起写下的点点滴滴，轻轻守护在回忆盒子里。" />}
    >
      <View style={styles.content}>
        <FairyCard padding={0} radius={30} style={styles.heroCard} contentStyle={styles.heroContent}>
          <View style={[styles.statusBadge, !backupAvailable && styles.unavailableBadge]}>
            <Ionicons name={backupAvailable ? 'cloud-done-outline' : 'lock-closed'} size={17} color={colors.white} />
            <Text style={styles.statusText}>{backupAvailable ? '服务已接入' : 'Real 未开放'}</Text>
          </View>
          <View style={styles.heroCopy}>
            <Text style={styles.lastBackup}>{backupAvailable ? '等待真实备份记录' : '当前没有真实云端备份记录'}</Text>
            <Text style={styles.heroTitle}>{backupAvailable ? '备份服务已准备' : '云备份仍在准备中'}</Text>
            <Text style={styles.heroDescription}>本机已有 {totalItems} 份回忆内容。没有真实服务响应前，不会显示同步、容量或恢复成功。</Text>
          </View>
          <FairyImage name="exportCover" height={230} radius={26} framed={false} resizeMode="contain" style={styles.heroImage} />
        </FairyCard>

        <View style={styles.actionGrid}>
          <FairyCard radius={26} style={styles.actionCard}>
            <View style={styles.actionIcon}><Ionicons name="cloud-upload-outline" size={27} color={colors.primaryDeep} /></View>
            <Text style={styles.actionTitle}>立即备份</Text>
            <Text style={styles.actionDescription}>{backupAvailable ? '真实备份 API 尚未返回可执行状态。' : 'Real 模式尚未接入云端备份服务。'}</Text>
            <FairyButton title="暂未开放" disabled leftContent={<Ionicons name="lock-closed-outline" size={18} color={colors.white} />} />
          </FairyCard>
          <FairyCard radius={26} style={styles.actionCard}>
            <View style={[styles.actionIcon, styles.restoreIcon]}><Ionicons name="refresh-circle-outline" size={28} color={colors.gold} /></View>
            <Text style={styles.actionTitle}>从备份恢复</Text>
            <Text style={styles.actionDescription}>{backupAvailable ? '没有真实备份记录可供恢复。' : 'Real 模式尚未接入云端恢复服务。'}</Text>
            <FairyButton title="暂未开放" disabled variant="secondary" leftContent={<Ionicons name="lock-closed-outline" size={18} color={colors.primaryDeep} />} />
          </FairyCard>
        </View>

        <FairyCard radius={26} style={styles.summaryCard}>
          <View style={styles.summaryRow}>
            <View style={styles.summaryIcon}><Ionicons name="albums-outline" size={21} color={colors.primaryDeep} /></View>
            <View style={styles.summaryCopy}><Text style={styles.summaryTitle}>本机内容</Text><Text style={styles.summaryText}>{totalItems} 份已加载回忆</Text></View>
          </View>
          <View style={styles.summaryRow}>
            <View style={styles.summaryIcon}><Ionicons name="cloud-offline-outline" size={21} color={colors.gold} /></View>
            <View style={styles.summaryCopy}><Text style={styles.summaryTitle}>云端状态</Text><Text style={styles.summaryText}>没有可验证的备份记录或容量数据</Text></View>
          </View>
          <View style={[styles.summaryRow, styles.summaryRowLast]}>
            <View style={styles.summaryIcon}><Ionicons name="shield-checkmark-outline" size={21} color={colors.primaryDeep} /></View>
            <View style={styles.summaryCopy}><Text style={styles.summaryTitle}>数据安全</Text><Text style={styles.summaryText}>当前页面不会上传、覆盖或恢复任何本机数据</Text></View>
          </View>
        </FairyCard>

        <FairyCard padding={0} radius={28} contentStyle={styles.historyCard}>
          <View style={styles.historyHeader}><Text style={styles.historyTitle}>最近备份记录</Text><Ionicons name="cloud-offline-outline" size={18} color={colors.textSoft} /></View>
          <View style={styles.emptyHistory}><Ionicons name="file-tray-outline" size={26} color={colors.textSoft} /><Text style={styles.emptyHistoryText}>目前没有来自真实备份服务的记录。完成真实备份后，这里才会展示时间和状态。</Text></View>
          <Text style={styles.footerNote}>不会使用固定日期、模拟容量或延时动画伪造成功。</Text>
        </FairyCard>
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 760 },
  heroCard: { marginTop: spacing.xl, marginBottom: spacing.lg, overflow: 'hidden' },
  heroContent: { minHeight: 308, padding: spacing.xl, backgroundColor: 'rgba(255,249,244,0.94)' },
  statusBadge: { alignSelf: 'flex-start', minHeight: 32, paddingHorizontal: spacing.md, borderRadius: 15, flexDirection: 'row', alignItems: 'center', gap: 5, backgroundColor: '#E69094' },
  unavailableBadge: { backgroundColor: colors.textSoft },
  statusText: { color: colors.white, fontSize: 12, fontWeight: '900' },
  heroCopy: { width: '56%', marginTop: spacing.xl, zIndex: 2 },
  lastBackup: { color: colors.textSoft, fontSize: 13, fontWeight: '700' },
  heroTitle: { marginTop: spacing.sm, color: colors.text, fontSize: 25, lineHeight: 34, fontWeight: '900' },
  heroDescription: { marginTop: spacing.sm, color: colors.textSoft, fontSize: 13, lineHeight: 21 },
  heroImage: { position: 'absolute', right: -28, bottom: -4, width: '62%' },
  actionGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md, marginBottom: spacing.lg },
  actionCard: { flexGrow: 1, flexBasis: 260, minHeight: 274, justifyContent: 'space-between' },
  actionIcon: { width: 54, height: 54, borderRadius: 22, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  restoreIcon: { backgroundColor: '#FFF5DF' },
  actionTitle: { marginTop: spacing.md, color: colors.text, fontSize: 20, fontWeight: '900' },
  actionDescription: { flex: 1, marginVertical: spacing.sm, color: colors.textSoft, fontSize: 13, lineHeight: 20 },
  summaryCard: { marginBottom: spacing.lg },
  summaryRow: { minHeight: 72, flexDirection: 'row', alignItems: 'center', gap: spacing.md, borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: colors.border },
  summaryRowLast: { borderBottomWidth: 0 },
  summaryIcon: { width: 42, height: 42, borderRadius: 17, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  summaryCopy: { flex: 1 },
  summaryTitle: { color: colors.text, fontSize: 14, fontWeight: '900' },
  summaryText: { marginTop: 4, color: colors.textSoft, fontSize: 12, lineHeight: 18 },
  historyCard: { padding: spacing.lg, backgroundColor: 'rgba(255,249,244,0.96)' },
  historyHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm, marginBottom: spacing.sm },
  historyTitle: { color: colors.text, fontSize: 18, fontWeight: '900' },
  emptyHistory: { minHeight: 112, alignItems: 'center', justifyContent: 'center', gap: spacing.sm },
  emptyHistoryText: { maxWidth: 480, color: colors.textSoft, fontSize: 12, lineHeight: 19, textAlign: 'center' },
  footerNote: { marginTop: spacing.lg, color: colors.textSoft, fontSize: 12, textAlign: 'center' },
});