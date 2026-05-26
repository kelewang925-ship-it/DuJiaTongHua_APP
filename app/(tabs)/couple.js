import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyHeroImage from '../../src/components/FairyHeroImage';
import CoupleTimeline from '../../src/components/CoupleTimeline';
import useFairyStore from '../../src/store/useFairyStore';

export default function CouplePage() {
  const couple = useFairyStore((state) => state.couple);
  const timeline = useFairyStore((state) => state.timeline);

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <Text style={styles.eyebrow}>双人宇宙</Text>
      <Text style={styles.title}>情侣空间</Text>

      <FairyCard style={styles.profile}>
        <FairyHeroImage imageKey="coupleHero" height={140} />
        <View style={styles.avatarRow}>
          <View style={styles.avatar}><Text style={styles.avatarText}>满</Text></View>
          <View style={styles.heartBridge}>
            <Ionicons name="heart" size={20} color={colors.white} />
          </View>
          <View style={styles.avatar}><Text style={styles.avatarText}>河</Text></View>
        </View>
        <Text style={styles.names}>{couple.userName} 和 {couple.partnerName}</Text>
        <Text style={styles.desc}>{couple.spaceName} · 第 {couple.loveDays} 天</Text>
      </FairyCard>

      <View style={styles.interactions}>
        <Pressable style={styles.interaction}>
          <Ionicons name="heart-outline" size={21} color={colors.primaryDeep} />
          <Text style={styles.interactionText}>互相喜欢</Text>
        </Pressable>
        <Pressable style={styles.interaction}>
          <Ionicons name="chatbubble-ellipses-outline" size={21} color={colors.accent} />
          <Text style={styles.interactionText}>悄悄留言</Text>
        </Pressable>
      </View>

      <View style={styles.sectionRow}>
        <View>
          <Text style={styles.section}>双人故事线</Text>
          <Text style={styles.sectionHint}>每一次记录，都会长成新的章节</Text>
        </View>
        <View style={styles.stickerMark}>
          <Ionicons name="flower-outline" size={18} color={colors.accent} />
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
  profile: { alignItems: 'center', marginBottom: 18, backgroundColor: colors.cardPink },
  avatarRow: { flexDirection: 'row', alignItems: 'center', gap: 12, marginTop: 4, marginBottom: 14 },
  avatar: { width: 58, height: 58, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  avatarText: { color: colors.text, fontWeight: '900', fontSize: 18 },
  heartBridge: { width: 34, height: 34, borderRadius: 14, backgroundColor: colors.primaryDeep, alignItems: 'center', justifyContent: 'center', transform: [{ rotate: '-8deg' }] },
  names: { color: colors.text, fontSize: 20, fontWeight: '900' },
  desc: { color: colors.textSoft, marginTop: 8 },
  interactions: { flexDirection: 'row', gap: 12, marginBottom: 28 },
  interaction: { flex: 1, height: 58, borderRadius: 20, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8 },
  interactionText: { color: colors.text, fontWeight: '800', fontSize: 13 },
  sectionRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 4 },
  sectionHint: { color: colors.textSoft, fontSize: 12 },
  stickerMark: { width: 38, height: 38, borderRadius: 16, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, transform: [{ rotate: '8deg' }] },
});
