import { useState } from 'react';
import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyInput from '../../src/components/FairyInput';
import FairyTag from '../../src/components/FairyTag';
import FairyBackButton from '../../src/components/FairyBackButton';
import useFairyStore from '../../src/store/useFairyStore';

const stylesList = ['童话绘本', '暖色漫画', '手帐贴纸'];
const sources = ['选择日记', '选择照片', '自由输入'];

export default function ComicConfigPage() {
  const addCreation = useFairyStore((state) => state.addCreation);
  const [source, setSource] = useState(sources[0]);
  const [styleName, setStyleName] = useState(stylesList[0]);
  const [title, setTitle] = useState('第一次约会的小漫画');

  const handleGenerate = () => {
    addCreation({
      type: '漫画',
      title,
      source,
      styleName,
      status: `生成中 · ${styleName}`,
      icon: 'albums-outline',
      progress: 64,
    });
    router.push('/ai/progress');
  };

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>恋爱漫画</Text>
      <Text style={styles.subtitle}>选择素材和画风，生成一组属于你们的童话漫画。</Text>

      <LinearGradient colors={['#FFF9F4', '#FFF0F2']} style={styles.hero}>
        <View style={styles.magic}><Ionicons name="sparkles" size={28} color={colors.gold} /></View>
        <Text style={styles.heroTitle}>把故事画成漫画</Text>
        <Text style={styles.heroText}>当前是前端 mock 流程，创建后会进入生成进度页并同步到工坊历史。</Text>
      </LinearGradient>

      <FairyCard style={styles.inputCard}>
        <FairyInput
          label="作品名称"
          icon="albums-outline"
          value={title}
          onChangeText={setTitle}
          placeholder="例如：一起看海的那天"
          helper="留空会自动生成一个作品名。"
          containerStyle={styles.inputGroup}
        />
      </FairyCard>

      <Text style={styles.section}>选择素材</Text>
      <View style={styles.row}>
        {sources.map((item) => (
          <Pressable key={item} style={[styles.choice, source === item && styles.activeChoice]} onPress={() => setSource(item)}>
            <Text style={[styles.choiceText, source === item && styles.activeText]}>{item}</Text>
          </Pressable>
        ))}
      </View>

      <Text style={styles.section}>漫画风格</Text>
      <View style={styles.row}>
        {stylesList.map((item) => (
          <Pressable key={item} style={[styles.choice, styleName === item && styles.activeChoice]} onPress={() => setStyleName(item)}>
            <Text style={[styles.choiceText, styleName === item && styles.activeText]}>{item}</Text>
          </Pressable>
        ))}
      </View>

      <FairyCard style={styles.roleCard}>
        <Pressable onPress={() => router.push('/ai/character-profile')}>
          <View style={styles.roleHeader}>
            <Ionicons name="people-outline" size={22} color={colors.accent} />
            <Text style={styles.roleTitle}>人设管理</Text>
            <FairyTag tone="gold">默认情侣人设</FairyTag>
          </View>
          <Text style={styles.roleText}>当前使用温柔绘本风双人角色，点击进入可调整昵称、氛围和服装风格。</Text>
        </Pressable>
      </FairyCard>

      <FairyCard style={styles.promptCard}>
        <Text style={styles.roleTitle}>生成提示</Text>
        <Text style={styles.roleText}>当前素材：{source} · 当前风格：{styleName}。建议选择有情绪、有场景的小片段。</Text>
      </FairyCard>

      <FairyButton title="开始生成童话漫画" onPress={handleGenerate} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  hero: { borderRadius: 30, padding: 22, borderWidth: 1, borderColor: colors.border, marginBottom: 18 },
  magic: { width: 54, height: 54, borderRadius: 22, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 16 },
  heroTitle: { color: colors.text, fontSize: 24, fontWeight: '800' },
  heroText: { color: colors.textSoft, marginTop: 10, lineHeight: 22 },
  inputCard: { marginBottom: 22 },
  inputGroup: { marginBottom: 0 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 14 },
  row: { flexDirection: 'row', gap: 10, marginBottom: 24 },
  choice: { flex: 1, minHeight: 48, borderRadius: 18, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, paddingHorizontal: 8 },
  activeChoice: { backgroundColor: colors.primary },
  choiceText: { color: colors.text, fontSize: 13, fontWeight: '700', textAlign: 'center' },
  activeText: { color: colors.white },
  roleCard: { marginBottom: 16 },
  roleHeader: { flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: 10, marginBottom: 12 },
  roleTitle: { color: colors.text, fontSize: 16, fontWeight: '800' },
  roleText: { color: colors.textSoft, lineHeight: 22 },
  promptCard: { marginBottom: 22, backgroundColor: colors.cardPink },
});
