import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyTag from '../../src/components/FairyTag';

const menu = [
  ['calendar-outline', '纪念日管理', '重要章节都在这里', '/anniversary'],
  ['archive-outline', '数据备份', '守护你们的回忆', null],
  ['document-text-outline', 'PDF导出', '把故事装订成册', null],
  ['settings-outline', '设置', '账号、通知与隐私', null],
];

export default function Page() {
  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <Text style={styles.title}>我的</Text>
      <FairyCard style={styles.profile}>
        <View style={styles.avatar}><Text style={styles.avatarText}>可</Text></View>
        <View style={{ flex: 1 }}>
          <Text style={styles.name}>王可乐</Text>
          <Text style={styles.desc}>正在书写第 428 天的童话</Text>
        </View>
        <FairyTag tone="gold">童话会员</FairyTag>
      </FairyCard>

      <View style={styles.stats}>
        <FairyCard style={styles.stat}><Text style={styles.statNum}>36</Text><Text style={styles.statLabel}>日记</Text></FairyCard>
        <FairyCard style={styles.stat}><Text style={styles.statNum}>128</Text><Text style={styles.statLabel}>照片</Text></FairyCard>
        <FairyCard style={styles.stat}><Text style={styles.statNum}>8</Text><Text style={styles.statLabel}>漫画</Text></FairyCard>
      </View>

      <Text style={styles.section}>私人收藏册</Text>
      {menu.map((item) => (
        <Pressable key={item[1]} onPress={() => item[3] && router.push(item[3])}>
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
  title: { color: colors.text, fontSize: 30, fontWeight: '800', marginBottom: 24 },
  profile: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 18, backgroundColor: colors.cardPink },
  avatar: { width: 58, height: 58, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  avatarText: { color: colors.text, fontWeight: '800', fontSize: 20 },
  name: { color: colors.text, fontWeight: '800', fontSize: 18 },
  desc: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  stats: { flexDirection: 'row', gap: 12, marginBottom: 28 },
  stat: { flex: 1, alignItems: 'center', padding: 14 },
  statNum: { color: colors.text, fontSize: 22, fontWeight: '800' },
  statLabel: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 16 },
  menuItem: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14 },
  menuIcon: { width: 40, height: 40, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  menuTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  menuDesc: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
