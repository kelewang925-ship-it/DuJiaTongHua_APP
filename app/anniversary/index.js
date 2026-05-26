import { useState } from 'react';
import { Alert, ScrollView, View, Text, TextInput, StyleSheet, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';
import FairyBackButton from '../../src/components/FairyBackButton';
import useFairyStore from '../../src/store/useFairyStore';

export default function AnniversaryPage() {
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const addAnniversary = useFairyStore((state) => state.addAnniversary);
  const [showForm, setShowForm] = useState(false);
  const [title, setTitle] = useState('');
  const [date, setDate] = useState('');
  const [note, setNote] = useState('');

  const nextAnniversary = anniversaries[0];

  const handleAdd = () => {
    if (!title.trim()) {
      Alert.alert('还没有章节标题', '给这个重要日子起一个名字吧。');
      return;
    }

    addAnniversary({ title, date, note });
    setTitle('');
    setDate('');
    setNote('');
    setShowForm(false);
  };

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>重要章节</Text>
      <Text style={styles.subtitle}>每个特别的日子，都是你们童话里的一章。</Text>

      <FairyCard style={styles.hero}>
        <FairyTag tone="gold">最近记录</FairyTag>
        <Text style={styles.heroTitle}>{nextAnniversary?.title || '新的重要章节'}</Text>
        <Text style={styles.heroNum}>{nextAnniversary?.days ?? 0} 天</Text>
        <Text style={styles.heroText}>可以提前准备一页专属记录模板。</Text>
      </FairyCard>

      <FairyButton
        title={showForm ? '收起添加表单' : '添加新的重要章节'}
        style={styles.button}
        onPress={() => setShowForm((value) => !value)}
      />

      {showForm ? (
        <FairyCard style={styles.formCard}>
          <Text style={styles.label}>章节名称</Text>
          <TextInput
            style={styles.input}
            value={title}
            onChangeText={setTitle}
            placeholder="例如：第一次一起看海"
            placeholderTextColor={colors.textSoft}
          />
          <Text style={styles.label}>日期</Text>
          <TextInput
            style={styles.input}
            value={date}
            onChangeText={setDate}
            placeholder="例如：2026.05.20"
            placeholderTextColor={colors.textSoft}
          />
          <Text style={styles.label}>备注</Text>
          <TextInput
            style={styles.note}
            value={note}
            onChangeText={setNote}
            multiline
            textAlignVertical="top"
            placeholder="这一章为什么重要？"
            placeholderTextColor={colors.textSoft}
          />
          <FairyButton title="保存章节" onPress={handleAdd} />
        </FairyCard>
      ) : null}

      <Text style={styles.section}>全部纪念日</Text>
      {anniversaries.map((item) => (
        <FairyCard key={item.id} style={styles.item}>
          <View style={styles.icon}><Ionicons name={item.icon || 'heart-outline'} size={20} color={colors.accent} /></View>
          <View style={{ flex: 1 }}>
            <Text style={styles.itemTitle}>{item.title}</Text>
            <Text style={styles.itemDate}>{item.date}</Text>
          </View>
          <Text style={styles.left}>{item.days ? `已记录 ${item.days} 天` : '刚添加'}</Text>
        </FairyCard>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  hero: { backgroundColor: colors.cardPink, marginBottom: 16 },
  heroTitle: { color: colors.text, fontSize: 22, fontWeight: '800', marginTop: 16 },
  heroNum: { color: colors.primaryDeep, fontSize: 34, fontWeight: '900', marginTop: 8 },
  heroText: { color: colors.textSoft, marginTop: 8 },
  button: { marginBottom: 18 },
  formCard: { marginBottom: 24 },
  label: { color: colors.text, fontWeight: '800', fontSize: 15, marginBottom: 10 },
  input: { minHeight: 46, color: colors.text, fontSize: 16, marginBottom: 18 },
  note: { minHeight: 96, color: colors.text, fontSize: 15, lineHeight: 23, marginBottom: 18 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 16 },
  item: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14 },
  icon: { width: 42, height: 42, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  itemTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  itemDate: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  left: { color: colors.accent, fontSize: 12, fontWeight: '700' },
});
