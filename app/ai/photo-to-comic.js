import { useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyInput from '../../src/components/FairyInput';
import FairyTag from '../../src/components/FairyTag';
import colors from '../../src/theme/colors';
import useFairyStore from '../../src/store/useFairyStore';

const stylesList = ['童话绘本', '暖色漫画', '手帐贴纸'];

export default function PhotoToComicPage() {
  const addCreation = useFairyStore((state) => state.addCreation);
  const [title, setTitle] = useState('奶油蛋糕和你');
  const [styleName, setStyleName] = useState(stylesList[0]);
  const [count, setCount] = useState('3');

  const generate = () => {
    addCreation({
      type: '漫画',
      title: `${title}（照片转漫画）`,
      source: `照片素材 ${count} 张`,
      styleName,
      status: `生成中 · ${styleName}`,
      icon: 'albums-outline',
      progress: 62,
    });
    router.push('/ai/progress');
  };

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>照片转漫画</Text>
      <Text style={styles.subtitle}>选几张照片，把真实瞬间画成一页绘本。</Text>

      <FairyCard style={styles.form}>
        <FairyInput label="作品标题" icon="albums-outline" value={title} onChangeText={setTitle} />
        <FairyInput label="照片数量（mock）" icon="images-outline" value={count} onChangeText={setCount} />
        <Text style={styles.sectionTitle}>画风选择</Text>
        <View style={styles.row}>
          {stylesList.map((item) => (
            <Pressable key={item} style={[styles.chip, styleName === item && styles.chipActive]} onPress={() => setStyleName(item)}>
              <Text style={[styles.chipText, styleName === item && styles.chipTextActive]}>{item}</Text>
            </Pressable>
          ))}
        </View>
        <View style={styles.tip}>
          <Ionicons name="sparkles-outline" size={16} color={colors.gold} />
          <Text style={styles.tipText}>当前为 mock 素材选择，不会读真实相册。</Text>
        </View>
      </FairyCard>

      <FairyButton title="开始生成漫画" onPress={generate} />
      <FairyButton title="切换到文字转漫画" variant="secondary" style={styles.secondary} onPress={() => router.push('/ai/text-to-comic')} />
      <FairyTag style={styles.footerTag}>回忆魔法屋</FairyTag>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 22, lineHeight: 22 },
  form: { marginBottom: 20 },
  sectionTitle: { color: colors.text, fontSize: 15, fontWeight: '800', marginBottom: 8 },
  row: { flexDirection: 'row', gap: 8, marginBottom: 14 },
  chip: { flex: 1, borderRadius: 16, paddingVertical: 8, alignItems: 'center', backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.border },
  chipActive: { backgroundColor: colors.primary, borderColor: colors.primary },
  chipText: { color: colors.textSoft, fontWeight: '700', fontSize: 12 },
  chipTextActive: { color: colors.white },
  tip: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  tipText: { color: colors.textSoft, fontSize: 12 },
  secondary: { marginTop: 12 },
  footerTag: { marginTop: 16 },
});
