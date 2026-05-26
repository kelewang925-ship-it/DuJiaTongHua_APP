import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyIllustration from '../../src/components/FairyIllustration';
import FairyTag from '../../src/components/FairyTag';
import useFairyStore from '../../src/store/useFairyStore';

const menu = [
  ['calendar-outline', '纪念日管理', '重要章节都在这里', '/anniversary'],
  ['archive-outline', '数据备份', '守护你们的回忆', '/data/backup'],
  ['document-text-outline', 'PDF导出', '把故事装订成册', '/data/pdf-export'],
  ['settings-outline', '设置', '账号、通知与隐私', '/settings'],
];

export default function MinePage() {
  const couple = useFairyStore((state) => state.couple);
  const getStats = useFairyStore((state) => state.getStats);
  const stats = getStats();

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <Text style={styles.eyebrow}>私人收藏册</Text>
      <Text style={styles.title}>我的</Text>
      <FairyCard style={styles.profile}>
        <View style={styles.profileTop}>
          <View style={styles.avatar}><Text style={styles.avatarText}>满</Text></View>
          <View style={{ flex: 1 }}>
            <Text style={styles.name}>{couple.userName}</Text>
            <Text style={styles.desc}>正在书写第 {couple.loveDays} 天的童话</Text>
          </View>
          <FairyTag tone="gold">童话会员</FairyTag>
        </View>
        <FairyIllustration scene="anniversary" height={132} />
      </FairyCard>

      <View style={styles.stats}>
        <FairyCard style={styles.stat}><Text style={styles.statNum}>{stats.diaryCount}</Text><Text style={styles.statLabel}>日记</Text></FairyCard>
        <FairyCard style={styles.stat}><Text style={styles.statNum}>{stats.photoCount}</Text><Text style={styles.statLabel}>照片</Text></FairyCard>
        <FairyCard style={styles.stat}><Text style={styles.statNum}>{stats.creationCount}</Text><Text style={styles.statLabel}>作品</Text></FairyCard>
      </View>

      <Text style={styles.section}>收藏与管理</Text>
      {menu.map((item) => (
        <Pressable key={item[1]} onPress={() => router.push(item[3])}>
          <FairyCard style={styles.menuItem}>
            <View style={styles.menuIcon}><Ionicons name={item[0]} size={20} color={colors.accent} /></View>
            <View style={{ flex: 1 }}>
              <Text style={styles.menuTitle}>{item[1]}</Text>
              <Text style={styles.menuDesc}>{item[2]}</Text>
            </View>
            <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
          </FairyCard>
        </Pressable>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 64, paddingBottom: 110 },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900', marginBottom: 24 },
  profile: { marginBottom: 18, backgroundColor: colors.cardPink },
  profileTop: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 8 },
  avatar: { width: 58, height: 58, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  avatarText: { color: colors.text, fontWeight: '900', fontSize: 20 },
  name: { color: colors.text, fontWeight: '900', fontSize: 18 },
  desc: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  stats: { flexDirection: 'row', gap: 12, marginBottom: 28 },
  stat: { flex: 1, alignItems: 'center', padding: 14 },
  statNum: { color: colors.text, fontSize: 22, fontWeight: '900' },
  statLabel: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 16 },
  menuItem: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14 },
  menuIcon: { width: 40, height: 40, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  menuTitle: { color: colors.text, fontWeight: '900', fontSize: 15 },
  menuDesc: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
