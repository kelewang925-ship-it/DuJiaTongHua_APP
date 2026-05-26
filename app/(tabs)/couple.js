import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyIllustration from '../../src/components/FairyIllustration';
import FairyTag from '../../src/components/FairyTag';
import useFairyStore from '../../src/store/useFairyStore';

export default function CouplePage() {
  const couple = useFairyStore((state) => state.couple);
  const timeline = useFairyStore((state) => state.timeline);

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <Text style={styles.eyebrow}>双人宇宙</Text>
      <Text style={styles.title}>情侣空间</Text>

      <FairyCard style={styles.profile}>
        <FairyIllustration scene="cover" height={140} />
        <View style={styles.avatarRow}>
          <View style={styles.avatar}><Text style={styles.avatarText}>满</Text></View>
          <Ionicons name="heart" size={22} color={colors.primaryDeep} />
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

      <Text style={styles.section}>最近动态</Text>
      <View style={styles.timeline}>
        {timeline.map((item, index) => (
          <View key={item.id} style={styles.storyRow}>
            <View style={styles.rail}>
              <View style={styles.storyIcon}><Ionicons name={item.icon} size={18} color={colors.accent} /></View>
              {index < timeline.length - 1 ? <View style={styles.line} /> : null}
            </View>
            <FairyCard style={styles.story}>
              <View style={{ flex: 1 }}>
                <View style={styles.storyHeader}>
                  <Text style={styles.storyTitle}>{item.title}</Text>
                  <FairyTag>{item.tag}</FairyTag>
                </View>
                <Text style={styles.storyTime}>{item.time}</Text>
                <Text style={styles.storyDesc}>{item.description}</Text>
              </View>
            </FairyCard>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 64, paddingBottom: 110 },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900', marginBottom: 24 },
  profile: { alignItems: 'center', marginBottom: 18, backgroundColor: colors.cardPink },
  avatarRow: { flexDirection: 'row', alignItems: 'center', gap: 16, marginTop: 4, marginBottom: 14 },
  avatar: { width: 58, height: 58, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  avatarText: { color: colors.text, fontWeight: '900', fontSize: 18 },
  names: { color: colors.text, fontSize: 20, fontWeight: '900' },
  desc: { color: colors.textSoft, marginTop: 8 },
  interactions: { flexDirection: 'row', gap: 12, marginBottom: 28 },
  interaction: { flex: 1, height: 58, borderRadius: 20, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8 },
  interactionText: { color: colors.text, fontWeight: '800', fontSize: 13 },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 16 },
  timeline: { gap: 0 },
  storyRow: { flexDirection: 'row', alignItems: 'stretch' },
  rail: { width: 42, alignItems: 'center' },
  storyIcon: { width: 36, height: 36, borderRadius: 15, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, zIndex: 2 },
  line: { flex: 1, width: 2, backgroundColor: '#EAD6D1', marginVertical: 4 },
  story: { flex: 1, marginBottom: 14, padding: 16 },
  storyHeader: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  storyTitle: { flex: 1, color: colors.text, fontWeight: '900', fontSize: 15 },
  storyTime: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  storyDesc: { color: colors.textSoft, marginTop: 8, fontSize: 12, lineHeight: 18 },
});
