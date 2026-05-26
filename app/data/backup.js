import { ScrollView, Text, StyleSheet, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import useFairyStore from '../../src/store/useFairyStore';

export default function BackupPage() {
  const getStats = useFairyStore((state) => state.getStats);
  const stats = getStats();

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>数据备份</Text>
      <Text style={styles.subtitle}>把你们的日记、照片和 AI 作品，安心收进云端小盒子。</Text>

      <FairyCard style={styles.statusCard}>
        <View style={styles.cloudIcon}>
          <Ionicons name="cloud-done-outline" size={30} color={colors.gold} />
        </View>
        <Text style={styles.statusTitle}>回忆状态良好</Text>
        <Text style={styles.statusText}>上次备份：今天 21:20</Text>
      </FairyCard>

      <View style={styles.grid}>
        <FairyCard style={styles.stat}><Text style={styles.statNum}>{stats.diaryCount}</Text><Text style={styles.statLabel}>日记</Text></FairyCard>
        <FairyCard style={styles.stat}><Text style={styles.statNum}>{stats.photoCount}</Text><Text style={styles.statLabel}>照片</Text></FairyCard>
        <FairyCard style={styles.stat}><Text style={styles.statNum}>{stats.creationCount}</Text><Text style={styles.statLabel}>AI作品</Text></FairyCard>
      </View>

      <FairyButton title="立即备份" />
      <FairyButton title="恢复数据" variant="secondary" style={styles.secondary} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  statusCard: { alignItems: 'center', backgroundColor: colors.cardPink, marginBottom: 18 },
  cloudIcon: { width: 62, height: 62, borderRadius: 24, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 14 },
  statusTitle: { color: colors.text, fontSize: 20, fontWeight: '800' },
  statusText: { color: colors.textSoft, marginTop: 8 },
  grid: { flexDirection: 'row', gap: 12, marginBottom: 22 },
  stat: { flex: 1, alignItems: 'center', padding: 14 },
  statNum: { color: colors.text, fontSize: 22, fontWeight: '800' },
  statLabel: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  secondary: { marginTop: 12 },
});
