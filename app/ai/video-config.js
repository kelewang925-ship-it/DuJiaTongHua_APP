import { useState } from 'react';
import { ScrollView, Text, StyleSheet, View, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyInput from '../../src/components/FairyInput';
import FairyTag from '../../src/components/FairyTag';
import useFairyStore from '../../src/store/useFairyStore';

const musicOptions = ['钢琴轻语', '午后风铃', '星光慢歌'];
const durationOptions = ['15 秒', '30 秒', '60 秒'];
const options = [
  ['musical-notes-outline', '音乐', '选择一段温柔的背景音乐'],
  ['text-outline', '字幕', '把日记文案变成影片旁白'],
  ['color-wand-outline', '转场', '使用翻页、淡入和星光显影'],
];

export default function VideoConfigPage() {
  const addCreation = useFairyStore((state) => state.addCreation);
  const [music, setMusic] = useState(musicOptions[0]);
  const [duration, setDuration] = useState(durationOptions[1]);
  const [title, setTitle] = useState('春天散步纪念视频');

  const handleGenerate = () => {
    addCreation({
      type: '视频',
      title,
      source: '照片与日记',
      styleName: `${duration} · ${music}`,
      status: `生成中 · ${duration} · ${music}`,
      icon: 'film-outline',
      progress: 46,
    });
    router.push('/ai/progress');
  };

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
          <FairyTag>{duration}</FairyTag>
        </View>
      </FairyCard>

      <FairyCard style={styles.inputCard}>
        <FairyInput
          label="作品名称"
          icon="film-outline"
          value={title}
          onChangeText={setTitle}
          placeholder="例如：一起散步的春天"
          containerStyle={styles.inputGroup}
        />
      </FairyCard>

      <Text style={styles.section}>选择音乐</Text>
      <View style={styles.row}>
        {musicOptions.map((item) => (
          <Pressable key={item} style={[styles.choice, music === item && styles.activeChoice]} onPress={() => setMusic(item)}>
            <Text style={[styles.choiceText, music === item && styles.activeText]}>{item}</Text>
          </Pressable>
        ))}
      </View>

      <Text style={styles.section}>影片时长</Text>
      <View style={styles.row}>
        {durationOptions.map((item) => (
          <Pressable key={item} style={[styles.choice, duration === item && styles.activeChoice]} onPress={() => setDuration(item)}>
            <Text style={[styles.choiceText, duration === item && styles.activeText]}>{item}</Text>
          </Pressable>
        ))}
      </View>

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

      <FairyButton title="生成纪念视频" onPress={handleGenerate} />
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
  inputCard: { marginBottom: 22 },
  inputGroup: { marginBottom: 0 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 14 },
  row: { flexDirection: 'row', gap: 10, marginBottom: 22 },
  choice: { flex: 1, minHeight: 46, borderRadius: 18, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, paddingHorizontal: 8 },
  activeChoice: { backgroundColor: colors.primary },
  choiceText: { color: colors.text, fontSize: 13, fontWeight: '700', textAlign: 'center' },
  activeText: { color: colors.white },
  option: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14 },
  optionIcon: { width: 42, height: 42, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  optionTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  optionText: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
