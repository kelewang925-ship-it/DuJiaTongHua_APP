import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import MemoryCard from '../../src/components/MemoryCard';
import useFairyStore from '../../src/store/useFairyStore';

export default function IndexPage() {
  const couple = useFairyStore((state) => state.couple);
  const records = useFairyStore((state) => state.records);

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <View>
          <Text style={styles.date}>2026.05.25</Text>
          <Text style={styles.title}>独家童话</Text>
        </View>
        <Pressable style={styles.iconBtn} onPress={() => router.push('/photo/album')}>
          <Ionicons name="images-outline" size={22} color={colors.text} />
        </Pressable>
      </View>

      <FairyCard style={styles.hero}>
        <Text style={styles.badge}>恋爱绘本</Text>
        <Text style={styles.heroTitle}>已经一起走过 {couple.loveDays} 天</Text>
        <Text style={styles.heroText}>{couple.statusText}</Text>
      </FairyCard>

      <Text style={styles.section}>今天想记录什么？</Text>
      <View style={styles.actions}>
        <Pressable style={styles.action} onPress={() => router.push('/diary/editor')}>
          <Ionicons name="create-outline" size={24} color={colors.accent} />
          <Text style={styles.actionText}>写日记</Text>
        </Pressable>
        <Pressable style={styles.action} onPress={() => router.push('/photo/upload')}>
          <Ionicons name="image-outline" size={24} color={colors.accent} />
          <Text style={styles.actionText}>传照片</Text>
        </Pressable>
        <Pressable style={styles.action} onPress={() => router.push('/ai/comic-config')}>
          <Ionicons name="sparkles-outline" size={24} color={colors.accent} />
          <Text style={styles.actionText}>工坊</Text>
        </Pressable>
      </View>

      <FairyButton title="把今天写进童话" style={styles.cta} onPress={() => router.push('/diary/editor')} />

      <Text style={styles.section}>最近的故事</Text>
      {records.map((record) => (
        <MemoryCard
          key={record.id}
          type={record.type}
          title={record.title}
          date={record.date}
          icon={record.icon}
          content={record.content}
        />
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 62, paddingBottom: 110 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 },
  date: { color: colors.textSoft, fontSize: 12, marginBottom: 4 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  iconBtn: { width: 44, height: 44, borderRadius: 18, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center' },
  hero: { marginBottom: 24, backgroundColor: colors.cardPink },
  badge: { color: colors.accent, fontSize: 12, marginBottom: 10 },
  heroTitle: { color: colors.text, fontSize: 25, fontWeight: '800' },
  heroText: { color: colors.textSoft, marginTop: 8, fontSize: 14 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 16 },
  actions: { flexDirection: 'row', gap: 12, marginBottom: 16 },
  action: { flex: 1, height: 92, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  actionText: { marginTop: 8, color: colors.text, fontWeight: '700', fontSize: 12 },
  cta: { marginBottom: 26 },
});
