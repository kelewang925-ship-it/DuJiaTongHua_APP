import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyImage from '../../src/components/FairyImage';
import MemoryWall from '../../src/components/MemoryWall';
import useFairyStore from '../../src/store/useFairyStore';

const actions = [
  ['create-outline', '写日记', '/diary/editor'],
  ['camera-outline', '传照片', '/photo/upload'],
  ['color-wand-outline', '童话工坊', '/ai/comic-config'],
];

export default function IndexPage() {
  const couple = useFairyStore((state) => state.couple);
  const records = useFairyStore((state) => state.records);

  const openRecord = (record) => {
    if (record.type === '日记') {
      router.push('/diary/detail');
      return;
    }
    if (record.type === '照片') {
      router.push('/photo/album');
      return;
    }
    router.push('/(tabs)/workshop');
  };

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <View>
          <Text style={styles.date}>2026年5月25日</Text>
          <Text style={styles.title}>独家童话</Text>
        </View>
        <Pressable style={styles.iconBtn} onPress={() => router.push('/photo/album')}>
          <Ionicons name="images-outline" size={22} color={colors.text} />
        </Pressable>
      </View>

      <FairyCard style={styles.hero}>
        <View style={styles.heroTextWrap}>
          <Text style={styles.badge}>今天的恋爱绘本</Text>
          <Text style={styles.heroTitle}>已经一起走过 {couple.loveDays} 天</Text>
          <Text style={styles.heroText}>{couple.statusText}</Text>
        </View>
        <FairyImage name="homeCover" height={168} />
      </FairyCard>

      <Text style={styles.section}>今天想记录什么？</Text>
      <View style={styles.actions}>
        {actions.map(([icon, label, href]) => (
          <Pressable key={label} style={styles.action} onPress={() => router.push(href)}>
            <Ionicons name={icon} size={25} color={colors.accent} />
            <Text style={styles.actionText}>{label}</Text>
          </Pressable>
        ))}
      </View>

      <FairyButton title="把今天写进童话" style={styles.cta} onPress={() => router.push('/diary/editor')} />

      <View style={styles.sectionRow}>
        <View>
          <Text style={styles.section}>最近的故事</Text>
          <Text style={styles.sectionHint}>像贴在纸上的回忆碎片</Text>
        </View>
        <View style={styles.stickerMark}>
          <Ionicons name="sparkles-outline" size={18} color={colors.gold} />
        </View>
      </View>
      <MemoryWall records={records} onPress={openRecord} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 62, paddingBottom: 124 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 },
  date: { color: colors.textSoft, fontSize: 12, marginBottom: 4 },
  title: { color: colors.text, fontSize: 31, fontWeight: '900' },
  iconBtn: { width: 44, height: 44, borderRadius: 18, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center' },
  hero: { marginBottom: 24, backgroundColor: colors.cardPink, paddingBottom: 18 },
  heroTextWrap: { marginBottom: 6 },
  badge: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 10 },
  heroTitle: { color: colors.text, fontSize: 25, fontWeight: '900', lineHeight: 32 },
  heroText: { color: colors.textSoft, marginTop: 8, fontSize: 14 },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 4 },
  sectionHint: { color: colors.textSoft, fontSize: 12 },
  sectionRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18 },
  stickerMark: { width: 38, height: 38, borderRadius: 16, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, transform: [{ rotate: '8deg' }] },
  actions: { flexDirection: 'row', gap: 12, marginBottom: 16 },
  action: { flex: 1, height: 94, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  actionText: { marginTop: 8, color: colors.text, fontWeight: '800', fontSize: 12 },
  cta: { marginBottom: 26 },
});
