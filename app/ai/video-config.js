import { ScrollView, Text, StyleSheet, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyTag from '../../src/components/FairyTag';

const options = [
  ['musical-notes-outline', '音乐', '选择一段温柔的背景音乐'],
  ['text-outline', '字幕', '把日记文案变成影片旁白'],
  ['color-wand-outline', '转场', '使用翻页、淡入和星光显影'],
];

export default function VideoConfigPage() {
  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>回忆放映机</Text>
      <Text style={styles.subtitle}>选择照片、音乐和字幕，让回忆开始播放。</Text>

      <FairyCard style={styles.hero}>
        <View style={styles.magicIcon}>
          <Ionicons name="videocam-outline" size={28} color={colors.gold} />
        </View>
        <Text style={styles.heroTitle}>AI 短视频配置</Text>
        <Text style={styles.heroText}>适合纪念日、旅行、约会和日常碎片整理。</Text>
        <View style={styles.tags}>
          <FairyTag>绘本转场</FairyTag>
          <FairyTag tone="gold">温柔字幕</FairyTag>
          <FairyTag>30秒</FairyTag>
        </View>
      </FairyCard>

      {options.map((item) => (
        <FairyCard key={item[1]} style={styles.option}>
          <View style={styles.optionIcon}>
            <Ionicons name={item[0]} size={22} color={colors.accent} />
          </View>
          <View style={{ flex: 1 }}>
            <Text style={styles.optionTitle}>{item[1]}</Text>
            <Text style={styles.optionText}>{item[2]}</Text>
          </View>
          <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
        </FairyCard>
      ))}

      <FairyButton title="生成纪念视频" />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  hero: { backgroundColor: colors.cardPink, marginBottom: 18 },
  magicIcon: { width: 54, height: 54, borderRadius: 22, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 16 },
  heroTitle: { color: colors.text, fontSize: 22, fontWeight: '800' },
  heroText: { color: colors.textSoft, marginTop: 8, lineHeight: 22 },
  tags: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 16 },
  option: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14 },
  optionIcon: { width: 42, height: 42, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  optionTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  optionText: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
