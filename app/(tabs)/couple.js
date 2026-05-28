import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyImage from '../../src/components/FairyImage';
import FairySticker from '../../src/components/FairySticker';
import FairyTag from '../../src/components/FairyTag';
import CoupleTimeline from '../../src/components/CoupleTimeline';
import useFairyStore from '../../src/store/useFairyStore';

const quickLinks = [
  { icon: 'create-outline', label: '写日记', href: '/diary/editor' },
  { icon: 'images-outline', label: '传照片', href: '/photo/upload' },
  { icon: 'sparkles-outline', label: '做漫画', href: '/ai/comic-config' },
  { icon: 'calendar-outline', label: '纪念日', href: '/anniversary' },
];

export default function CouplePage() {
  const couple = useFairyStore((state) => state.couple);
  const timeline = useFairyStore((state) => state.timeline);
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const anniversaries = useFairyStore((state) => state.anniversaries);

  const stats = [
    { label: '恋爱天数', value: couple.loveDays, icon: 'heart-outline' },
    { label: '共同记录', value: records.length, icon: 'library-outline' },
    { label: 'AI 作品', value: creations.length, icon: 'color-wand-outline' },
  ];
  const nextAnniversary = anniversaries[0];

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <Text style={styles.eyebrow}>双人宇宙</Text>
      <Text style={styles.title}>情侣空间</Text>

      <FairyCard style={styles.profile}>
        <FairySticker name="flower" size={44} rotate="-8deg" style={styles.flowerSticker} />
        <FairySticker name="heart" size={36} rotate="10deg" style={styles.heartSticker} />
        <FairyImage name="coupleCover" height={140} />
        <View style={styles.avatarRow}>
          <View style={styles.avatar}><Text style={styles.avatarText}>满</Text></View>
          <View style={styles.heartBridge}>
            <Ionicons name="heart" size={20} color={colors.white} />
          </View>
          <View style={styles.avatar}><Text style={styles.avatarText}>河</Text></View>
        </View>
        <Text style={styles.names}>{couple.userName} 和 {couple.partnerName}</Text>
        <Text style={styles.desc}>{couple.spaceName} · 第 {couple.loveDays} 天</Text>
        <View style={styles.profileTags}>
          <FairyTag tone="gold">{couple.statusText}</FairyTag>
          <FairyTag>共同记录 {records.length} 条</FairyTag>
        </View>
      </FairyCard>

      <View style={styles.statsRow}>
        {stats.map((item) => (
          <FairyCard key={item.label} style={styles.statCard}>
            <Ionicons name={item.icon} size={18} color={colors.accent} />
            <Text style={styles.statValue}>{item.value}</Text>
            <Text style={styles.statLabel}>{item.label}</Text>
          </FairyCard>
        ))}
      </View>

      <View style={styles.interactions}>
        {quickLinks.map((item) => (
          <Pressable key={item.label} style={styles.interaction} onPress={() => router.push(item.href)}>
            <Ionicons name={item.icon} size={21} color={colors.accent} />
            <Text style={styles.interactionText}>{item.label}</Text>
          </Pressable>
        ))}
      </View>

      <FairyCard style={styles.anniversaryCard}>
        <View style={styles.anniversaryIcon}>
          <Ionicons name={nextAnniversary?.icon || 'calendar-outline'} size={24} color={colors.primaryDeep} />
        </View>
        <View style={styles.anniversaryText}>
          <Text style={styles.anniversaryLabel}>纪念日入口</Text>
          <Text style={styles.anniversaryTitle}>{nextAnniversary?.title || '新的重要章节'}</Text>
          <Text style={styles.anniversaryDesc}>{nextAnniversary ? `${nextAnniversary.date} · 第 ${nextAnniversary.days} 天` : '把重要日子写进你们的故事。'}</Text>
        </View>
        <Pressable style={styles.anniversaryBtn} onPress={() => router.push('/anniversary')}>
          <Ionicons name="chevron-forward" size={18} color={colors.accent} />
        </Pressable>
      </FairyCard>

      <View style={styles.sectionRow}>
        <View>
          <Text style={styles.section}>双人故事线</Text>
          <Text style={styles.sectionHint}>每一次记录，都会长成新的章节</Text>
        </View>
        <View style={styles.stickerMark}>
          <FairySticker name="star" size={30} rotate="8deg" style={styles.inlineSticker} />
        </View>
      </View>
      <CoupleTimeline items={timeline} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 64, paddingBottom: 124 },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900', marginBottom: 24 },
  profile: { alignItems: 'center', marginBottom: 18, backgroundColor: colors.cardPink, overflow: 'visible' },
  flowerSticker: { top: -16, left: 20 },
  heartSticker: { top: 118, right: 20 },
  avatarRow: { flexDirection: 'row', alignItems: 'center', gap: 12, marginTop: 4, marginBottom: 14 },
  avatar: { width: 58, height: 58, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  avatarText: { color: colors.text, fontWeight: '900', fontSize: 18 },
  heartBridge: { width: 34, height: 34, borderRadius: 14, backgroundColor: colors.primaryDeep, alignItems: 'center', justifyContent: 'center', transform: [{ rotate: '-8deg' }] },
  names: { color: colors.text, fontSize: 20, fontWeight: '900' },
  desc: { color: colors.textSoft, marginTop: 8 },
  profileTags: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', gap: 8, marginTop: 14 },
  statsRow: { flexDirection: 'row', gap: 10, marginBottom: 18 },
  statCard: { flex: 1, minHeight: 112, alignItems: 'center', justifyContent: 'center', padding: 12 },
  statValue: { color: colors.text, fontSize: 21, fontWeight: '900', marginTop: 8 },
  statLabel: { color: colors.textSoft, fontSize: 11, marginTop: 3, fontWeight: '700', textAlign: 'center' },
  interactions: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 18 },
  interaction: { width: '47.8%', height: 64, borderRadius: 20, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8 },
  interactionText: { color: colors.text, fontWeight: '800', fontSize: 13 },
  anniversaryCard: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 28, backgroundColor: colors.cardPink },
  anniversaryIcon: { width: 52, height: 52, borderRadius: 20, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' },
  anniversaryText: { flex: 1 },
  anniversaryLabel: { color: colors.accent, fontSize: 12, fontWeight: '900', marginBottom: 4 },
  anniversaryTitle: { color: colors.text, fontSize: 16, fontWeight: '900' },
  anniversaryDesc: { color: colors.textSoft, fontSize: 12, marginTop: 4 },
  anniversaryBtn: { width: 36, height: 36, borderRadius: 14, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' },
  sectionRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 4 },
  sectionHint: { color: colors.textSoft, fontSize: 12 },
  stickerMark: { width: 38, height: 38, borderRadius: 16, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, transform: [{ rotate: '8deg' }] },
  inlineSticker: { position: 'relative' },
});
