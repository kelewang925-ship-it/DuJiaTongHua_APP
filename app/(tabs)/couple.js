import { ScrollView, View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyTag from '../../src/components/FairyTag';
import useFairyStore from '../../src/store/useFairyStore';

export default function Page() {
  const couple = useFairyStore((state) => state.couple);
  const timeline = useFairyStore((state) => state.timeline);

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <Text style={styles.title}>情侣空间</Text>
      <FairyCard style={styles.profile}>
        <View style={styles.avatarRow}>
          <View style={styles.avatar}><Text style={styles.avatarText}>你</Text></View>
          <Ionicons name="heart" size={22} color={colors.primaryDeep} />
          <View style={styles.avatar}><Text style={styles.avatarText}>TA</Text></View>
        </View>
        <Text style={styles.names}>{couple.userName} 和 {couple.partnerName}</Text>
        <Text style={styles.desc}>双人宇宙已经运行 {couple.loveDays} 天</Text>
      </FairyCard>

      <Text style={styles.section}>最近动态</Text>
      {timeline.map((item) => (
        <FairyCard key={item.id} style={styles.story}>
          <View style={styles.storyIcon}><Ionicons name={item.icon} size={20} color={colors.accent} /></View>
          <View style={{ flex: 1 }}>
            <Text style={styles.storyTitle}>{item.title}</Text>
            <Text style={styles.storyTime}>{item.time}</Text>
            <Text style={styles.storyDesc}>{item.description}</Text>
          </View>
          <FairyTag>{item.tag}</FairyTag>
        </FairyCard>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 64, paddingBottom: 110 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800', marginBottom: 24 },
  profile: { alignItems: 'center', marginBottom: 28, backgroundColor: colors.cardPink },
  avatarRow: { flexDirection: 'row', alignItems: 'center', gap: 16, marginBottom: 14 },
  avatar: { width: 58, height: 58, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  avatarText: { color: colors.text, fontWeight: '800' },
  names: { color: colors.text, fontSize: 20, fontWeight: '800' },
  desc: { color: colors.textSoft, marginTop: 8 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 16 },
  story: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 14 },
  storyIcon: { width: 40, height: 40, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  storyTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  storyTime: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  storyDesc: { color: colors.textSoft, marginTop: 6, fontSize: 12, lineHeight: 18 },
});
