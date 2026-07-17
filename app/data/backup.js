import { useMemo, useState } from 'react';
import { ActivityIndicator, Pressable, StyleSheet, Switch, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyDialog from '../../src/components/FairyDialog';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyPage from '../../src/components/FairyPage';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';
import { hasCapability } from '../../src/config/capabilities';

const frequencies = ['每天', '每周', '手动'];
const initialHistory = [
  { id: 'backup-today', time: '今天 20:18', type: '手动备份', tone: 'pink' },
  { id: 'backup-yesterday', time: '昨天 22:06', type: '自动备份', tone: 'gold' },
  { id: 'backup-june', time: '06.08 21:30', type: '自动备份', tone: 'gold' },
];

export default function BackupPage() {
  const getStats = useFairyStore((state) => state.getStats);
  const stats = getStats();
  const [autoBackup, setAutoBackup] = useState(true);
  const [frequency, setFrequency] = useState('每天');
  const [backingUp, setBackingUp] = useState(false);
  const [restoreVisible, setRestoreVisible] = useState(false);
  const [toast, setToast] = useState({ visible: false, message: '', tone: 'success' });
  const [history, setHistory] = useState(initialHistory);

  const totalItems = useMemo(
    () => stats.diaryCount + stats.photoCount + stats.creationCount,
    [stats.creationCount, stats.diaryCount, stats.photoCount]
  );
  const usedStorage = Math.min(4.6, 0.74 + stats.photoCount * 0.03 + stats.creationCount * 0.08);
  const storagePercent = Math.max(8, Math.round((usedStorage / 5) * 100));

  const showToast = (message, tone = 'success') => setToast({ visible: true, message, tone });

  const handleBackup = () => {
    if (!hasCapability('cloudBackup')) { showToast('Real 模式暂未开放备份功能。', 'info'); return; }
    if (backingUp) return;
    setBackingUp(true);
    setTimeout(() => {
      setBackingUp(false);
      setHistory((items) => [
        { id: `backup-${Date.now()}`, time: '刚刚', type: '手动备份', tone: 'pink' },
        ...items.slice(0, 2),
      ]);
      showToast('所有故事都已安心收好。');
    }, 700);
  };

  const handleRestore = () => {
    if (!hasCapability('cloudBackup')) { setRestoreVisible(false); showToast('Real 模式暂未开放备份恢复。', 'info'); return; }
    setRestoreVisible(false);
    showToast('已模拟恢复最近一次备份，当前数据没有被覆盖。', 'info');
  };

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
          <View style={styles.syncedBadge}>
            <Ionicons name="checkmark-circle" size={17} color={colors.white} />
            <Text style={styles.syncedText}>已同步</Text>
          </View>
          <View style={styles.heroCopy}>
            <Text style={styles.lastBackup}>上次备份 · 今天 20:18</Text>
            <Text style={styles.heroTitle}>所有故事都安静收好</Text>
            <Text style={styles.heroDescription}>共 {totalItems} 份回忆内容，正在本地 Mock 云端中被温柔守护。</Text>
          </View>
          <FairyImage name="exportCover" height={230} radius={26} framed={false} resizeMode="contain" style={styles.heroImage} />
        </FairyCard>

        <View style={styles.actionGrid}>
          <FairyCard radius={26} style={styles.actionCard}>
            <View style={styles.actionIcon}><Ionicons name="cloud-upload-outline" size={27} color={colors.primaryDeep} /></View>
            <Text style={styles.actionTitle}>立即备份</Text>
            <Text style={styles.actionDescription}>将当前所有故事安全收进云端回忆盒。</Text>
            <FairyButton
              title={backingUp ? '正在备份…' : '立即备份'}
              disabled={backingUp}
              leftContent={backingUp ? <ActivityIndicator size="small" color={colors.white} /> : <Ionicons name="cloud-upload-outline" size={18} color={colors.white} />}
              onPress={handleBackup}
            />
          </FairyCard>
          <FairyCard radius={26} style={styles.actionCard}>
            <View style={[styles.actionIcon, styles.restoreIcon]}><Ionicons name="refresh-circle-outline" size={28} color={colors.gold} /></View>
            <Text style={styles.actionTitle}>从备份恢复</Text>
            <Text style={styles.actionDescription}>预览确认后，再恢复最近一次保存的故事。</Text>
            <FairyButton
              title="从备份恢复"
              variant="secondary"
              leftContent={<Ionicons name="refresh-outline" size={18} color={colors.primaryDeep} />}
              onPress={() => setRestoreVisible(true)}
            />
          </FairyCard>
        </View>

        <FairyCard padding={0} radius={28} contentStyle={styles.settingsCard}>
          <View style={styles.settingRow}>
            <View style={styles.settingIcon}><Ionicons name="star-outline" size={21} color={colors.gold} /></View>
            <View style={styles.settingCopy}>
              <Text style={styles.settingTitle}>自动备份</Text>
              <Text style={styles.settingDescription}>开启后，会按选定频率自动收好新故事。</Text>
            </View>
            <Switch
              accessibilityLabel="自动备份"
              value={autoBackup}
              onValueChange={setAutoBackup}
              trackColor={{ false: '#E7D9D4', true: '#F2B5B8' }}
              thumbColor="#FFF9F4"
            />
          </View>
          <View style={styles.frequencyRow}>
            <View style={styles.settingIcon}><Ionicons name="calendar-outline" size={21} color={colors.primaryDeep} /></View>
            <View style={styles.frequencyCopy}>
              <Text style={styles.settingTitle}>备份频率</Text>
              <Text style={styles.settingDescription}>选择自动守护回忆的频率。</Text>
            </View>
            <View style={styles.frequencyOptions}>
              {frequencies.map((item) => {
                const active = item === frequency;
                return (
                  <Pressable
                    accessibilityRole="button"
                    accessibilityState={{ selected: active }}
                    key={item}
                    onPress={() => setFrequency(item)}
                    style={[styles.frequencyChip, active && styles.frequencyChipActive]}
                  >
                    <Text style={[styles.frequencyText, active && styles.frequencyTextActive]}>{item}</Text>
                  </Pressable>
                );
              })}
            </View>
          </View>
        </FairyCard>

        <FairyCard radius={26} style={styles.storageCard}>
          <View style={styles.storageHeader}>
            <Text style={styles.storageTitle}>当前备份占用空间</Text>
            <Text style={styles.storageValue}>{usedStorage.toFixed(2)} GB / 5 GB</Text>
          </View>
          <View style={styles.progressTrack}>
            <View style={[styles.progressFill, { width: `${storagePercent}%` }]} />
          </View>
          <Text style={styles.storageHint}>空间充足，可以安心保存更多回忆。</Text>
        </FairyCard>

        <FairyCard padding={0} radius={28} contentStyle={styles.historyCard}>
          <View style={styles.historyHeader}>
            <Text style={styles.historyTitle}>最近备份记录</Text>
            <Ionicons name="sparkles-outline" size={17} color={colors.gold} />
          </View>
          {history.map((item) => (
            <View key={item.id} style={styles.historyRow}>
              <View style={styles.historyIcon}><Ionicons name="cloud-upload-outline" size={20} color={colors.primaryDeep} /></View>
              <View style={styles.historyCopy}>
                <Text style={styles.historyTime}>{item.time}</Text>
                <Text style={styles.historyType}>{item.type}</Text>
              </View>
              <View style={[styles.historyBadge, item.tone === 'gold' && styles.historyBadgeGold]}>
                <Text style={styles.historyBadgeText}>已同步</Text>
              </View>
            </View>
          ))}
          <Text style={styles.footerNote}>每一次备份，都是我们给未来的温柔礼物。</Text>
        </FairyCard>
      </View>

      <FairyDialog
        visible={restoreVisible}
        icon="refresh-circle-outline"
        title="恢复最近一次备份？"
        description="当前阶段只会展示恢复成功状态，不会覆盖本机上的日记、照片或作品。"
        confirmText="确认恢复"
        cancelText="先不恢复"
        onConfirm={handleRestore}
        onCancel={() => setRestoreVisible(false)}
      />
      <FairyToast
        visible={toast.visible}
        message={toast.message}
        tone={toast.tone}
        onHide={() => setToast((current) => ({ ...current, visible: false }))}
      />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 760 },
  heroCard: { marginTop: spacing.xl, marginBottom: spacing.lg, overflow: 'hidden' },
  heroContent: { minHeight: 308, padding: spacing.xl, backgroundColor: 'rgba(255,249,244,0.94)' },
  syncedBadge: { alignSelf: 'flex-start', minHeight: 32, paddingHorizontal: spacing.md, borderRadius: 15, flexDirection: 'row', alignItems: 'center', gap: 5, backgroundColor: '#E69094' },
  syncedText: { color: colors.white, fontSize: 12, fontWeight: '900' },
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
  settingsCard: { paddingHorizontal: spacing.lg, backgroundColor: 'rgba(255,249,244,0.96)' },
  settingRow: { minHeight: 84, flexDirection: 'row', alignItems: 'center', gap: spacing.md, borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: colors.border },
  frequencyRow: { minHeight: 112, paddingVertical: spacing.md, flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: spacing.md },
  settingIcon: { width: 42, height: 42, borderRadius: 17, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  settingCopy: { flex: 1 },
  frequencyCopy: { flexGrow: 1, flexBasis: 170 },
  settingTitle: { color: colors.text, fontSize: 15, fontWeight: '900' },
  settingDescription: { marginTop: 4, color: colors.textSoft, fontSize: 12, lineHeight: 18 },
  frequencyOptions: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  frequencyChip: { minHeight: 36, paddingHorizontal: spacing.md, borderRadius: 17, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border },
  frequencyChipActive: { backgroundColor: colors.primaryDeep, borderColor: colors.primaryDeep },
  frequencyText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  frequencyTextActive: { color: colors.white },
  storageCard: { marginTop: spacing.lg },
  storageHeader: { flexDirection: 'row', justifyContent: 'space-between', gap: spacing.md },
  storageTitle: { flex: 1, color: colors.text, fontSize: 15, fontWeight: '900' },
  storageValue: { color: colors.text, fontSize: 13, fontWeight: '800' },
  progressTrack: { height: 12, marginTop: spacing.lg, borderRadius: 6, overflow: 'hidden', backgroundColor: '#F0E3D8' },
  progressFill: { height: '100%', borderRadius: 6, backgroundColor: '#E99197' },
  storageHint: { marginTop: spacing.sm, color: colors.textSoft, fontSize: 12 },
  historyCard: { marginTop: spacing.lg, padding: spacing.lg, backgroundColor: 'rgba(255,249,244,0.96)' },
  historyHeader: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginBottom: spacing.sm },
  historyTitle: { color: colors.text, fontSize: 18, fontWeight: '900' },
  historyRow: { minHeight: 68, flexDirection: 'row', alignItems: 'center', gap: spacing.md, borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: colors.border },
  historyIcon: { width: 40, height: 40, borderRadius: 16, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  historyCopy: { flex: 1 },
  historyTime: { color: colors.text, fontSize: 14, fontWeight: '900' },
  historyType: { marginTop: 3, color: colors.textSoft, fontSize: 11 },
  historyBadge: { minHeight: 28, paddingHorizontal: spacing.md, borderRadius: 13, alignItems: 'center', justifyContent: 'center', backgroundColor: '#FCE1E1' },
  historyBadgeGold: { backgroundColor: '#FFF1D8' },
  historyBadgeText: { color: colors.text, fontSize: 11, fontWeight: '800' },
  footerNote: { marginTop: spacing.lg, color: colors.textSoft, fontSize: 12, textAlign: 'center' },
});
