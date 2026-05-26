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

const stylesList = ['童话绘本', '暖色漫画', '手账贴纸'];

export default function TextToComicPage() {
  const addCreation = useFairyStore((state) => state.addCreation);
  const records = useFairyStore((state) => state.records);
  const latestDiary = records.find((item) => item.type === '日记');
  const [storyText, setStoryText] = useState(latestDiary?.content || '');
  const [styleName, setStyleName] = useState(stylesList[0]);

  const handleGenerate = () => {
    addCreation({
      type: '漫画',
      title: latestDiary ? `${latestDiary.title} · 漫画版` : '文字魔法生成的小漫画',
      status: `生成中 · 文本转漫画 · ${styleName}`,
      icon: 'color-palette-outline',
    });
    router.push('/ai/progress');
  };

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>文本转漫画</Text>
      <Text style={styles.subtitle}>输入一段故事，让它变成温柔的绘本分镜。</Text>

      <FairyCard style={styles.hero}>
        <View style={styles.magicIcon}>
          <Ionicons name="document-text-outline" size={28} color={colors.gold} />
        </View>
        <Text style={styles.heroTitle}>把文字变成童话画面</Text>
        <Text style={styles.heroText}>可以使用最近日记，也可以自由输入一段想被画出来的回忆。</Text>
        {latestDiary ? <FairyTag tone="gold">已填入最近日记</FairyTag> : null}
      </FairyCard>

      <FairyCard style={styles.editorCard}>
        <FairyInput
          label="故事文本"
          icon="document-text-outline"
          value={storyText}
          onChangeText={setStoryText}
          multiline
          placeholder="例如：那天傍晚，我们一起走在很轻的风里……"
          helper="越具体的场景越容易生成稳定分镜。"
          containerStyle={styles.inputGroup}
        />
      </FairyCard>

      <Text style={styles.section}>漫画风格</Text>
      <View style={styles.row}>
        {stylesList.map((item) => (
          <Pressable key={item} style={[styles.choice, styleName === item && styles.activeChoice]} onPress={() => setStyleName(item)}>
            <Text style={[styles.choiceText, styleName === item && styles.activeText]}>{item}</Text>
          </Pressable>
        ))}
      </View>

      <FairyCard style={styles.tipCard}>
        <Text style={styles.tipTitle}>生成建议</Text>
        <Text style={styles.tipText}>地点、动作、情绪和一句想保留的话，都可以写进去。</Text>
      </FairyCard>

      <FairyButton title="生成童话漫画" onPress={handleGenerate} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  hero: { backgroundColor: colors.cardPink, marginBottom: 16 },
  magicIcon: { width: 56, height: 56, borderRadius: 22, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 16 },
  heroTitle: { color: colors.text, fontSize: 22, fontWeight: '800' },
  heroText: { color: colors.textSoft, marginTop: 8, marginBottom: 14, lineHeight: 22 },
  editorCard: { marginBottom: 22 },
  inputGroup: { marginBottom: 0 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 14 },
  row: { flexDirection: 'row', gap: 10, marginBottom: 22 },
  choice: { flex: 1, minHeight: 48, borderRadius: 18, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  activeChoice: { backgroundColor: colors.primary },
  choiceText: { color: colors.text, fontSize: 13, fontWeight: '700' },
  activeText: { color: colors.white },
  tipCard: { marginBottom: 22 },
  tipTitle: { color: colors.text, fontWeight: '800', fontSize: 16, marginBottom: 8 },
  tipText: { color: colors.textSoft, lineHeight: 22 },
});
