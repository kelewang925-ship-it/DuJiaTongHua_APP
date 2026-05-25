import { ScrollView, Text, StyleSheet, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../src/theme/colors';
import FairyBackButton from '../src/components/FairyBackButton';
import FairyCard from '../src/components/FairyCard';

const settings = [
  ['notifications-outline', '通知设置', '纪念日、互动和生成完成提醒'],
  ['lock-closed-outline', '隐私设置', '仅两个人可见的私密空间'],
  ['color-palette-outline', '主题设置', '月白纸感与桃粉童话主题'],
  ['trash-outline', '缓存清理', '释放临时图片与生成缓存'],
];

export default function SettingsPage() {
  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>设置</Text>
      <Text style={styles.subtitle}>调整独家童话的提醒、隐私和视觉体验。</Text>

      {settings.map((item) => (
        <FairyCard key={item[1]} style={styles.item}>
          <View style={styles.iconWrap}>
            <Ionicons name={item[0]} size={21} color={colors.accent} />
          </View>
          <View style={{ flex: 1 }}>
            <Text style={styles.itemTitle}>{item[1]}</Text>
            <Text style={styles.itemText}>{item[2]}</Text>
          </View>
          <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
        </FairyCard>
      ))}

      <Text style={styles.version}>独家童话 v1.0.0</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  item: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14 },
  iconWrap: { width: 42, height: 42, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  itemTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  itemText: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  version: { color: colors.textSoft, textAlign: 'center', marginTop: 26, fontSize: 12 },
});
