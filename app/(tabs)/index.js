import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import MemoryCard from '../../src/components/MemoryCard';

export default function IndexPage() {
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
        <Text style={styles.heroTitle}>已经一起走过 428 天</Text>
        <Text style={styles.heroText}>今天也被好好爱着。</Text>
      </FairyCard>

      <Text style={styles.section}>今天想记录什么？</Text>
      <View style={styles.actions}>
        <Pressable style={styles.action} onPress={() => router.push('/diary/editor')}><Ionicons name="create-outline" size={24} color={colors.accent} /><Text style={styles.actionText}>写日记</Text></Pressable>
        <Pressable style={styles.action} onPress={() => router.push('/photo/upload')}><Ionicons name="image-outline" size={24} color={colors.accent} /><Text style={styles.actionText}>传照片</Text></Pressable>
        <Pressable style={styles.action} onPress={() => router.push('/ai/comic-config')}><Ionicons name="sparkles-outline" size={24} color={colors.accent} /><Text style={styles.actionText}>工坊</Text></Pressable>
      </View>

      <FairyButton title="把今天写进童话" style={styles.cta} onPress={() => router.push('/diary/editor')} />

      <Text style={styles.section}>最近的故事</Text>
      <MemoryCard type="日记" title="一起散步的傍晚" date="今天 20:18" icon="book-outline" content="晚风很轻，普通的一天也像被温柔收藏起来。" />
      <MemoryCard type="照片" title="奶油蛋糕和你" date="昨天 16:42" icon="camera-outline" content="上传了 3 张照片，准备把这一天变成漫画。" />
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
