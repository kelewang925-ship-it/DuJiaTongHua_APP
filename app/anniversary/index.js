import { useState } from 'react';
import { Alert, ScrollView, View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';
import FairyInput from '../../src/components/FairyInput';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyImage from '../../src/components/FairyImage';
import useFairyStore from '../../src/store/useFairyStore';

export default function AnniversaryPage() {
  const router = useRouter();
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
        <FairyImage name="anniversaryCover" height={150} radius={26} />
        <View style={styles.heroContent}>
          <FairyTag tone="gold">最近记录</FairyTag>
          <Text style={styles.heroTitle}>{nextAnniversary?.title || '新的重要章节'}</Text>
          <Text style={styles.heroNum}>{nextAnniversary?.days ?? 0} 天</Text>
          <Text style={styles.heroText}>可以提前准备一页专属记录模板。</Text>
        </View>
      </FairyCard>

      <FairyButton
        title={showForm ? '收起添加表单' : '添加新的重要章节'}
        style={styles.button}
        onPress={() => setShowForm((value) => !value)}
      />
      <View style={styles.quickActions}>
        <FairyButton title="去纪念日编辑页" variant="secondary" style={styles.quickBtn} onPress={() => router.push('/anniversary/edit')} />
        <FairyButton title="去专属模板页" variant="secondary" style={styles.quickBtn} onPress={() => router.push('/anniversary/template')} />
      </View>

      {showForm ? (
        <FairyCard style={styles.formCard}>
          <FairyInput
            label="章节名称"
            icon="heart-outline"
            value={title}
            onChangeText={setTitle}
            placeholder="例如：第一次一起看海"
          />
          <FairyInput
            label="日期"
            icon="calendar-outline"
            value={date}
            onChangeText={setDate}
            placeholder="例如：2026.05.20"
          />
          <FairyInput
            label="备注"
            icon="document-text-outline"
            value={note}
            onChangeText={setNote}
            multiline
            placeholder="这一章为什么重要？"
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
          <Text style={styles.editLink} onPress={() => router.push(`/anniversary/edit?id=${item.id}`)}>编辑</Text>
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
  heroContent: { marginTop: 14 },
  heroTitle: { color: colors.text, fontSize: 22, fontWeight: '800', marginTop: 16 },
  heroNum: { color: colors.primaryDeep, fontSize: 34, fontWeight: '900', marginTop: 8 },
  heroText: { color: colors.textSoft, marginTop: 8 },
  button: { marginBottom: 18 },
  quickActions: { flexDirection: 'row', gap: 10, marginBottom: 20 },
  quickBtn: { flex: 1, height: 44 },
  formCard: { marginBottom: 24 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 16 },
  item: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14 },
  icon: { width: 42, height: 42, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  itemTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  itemDate: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  left: { color: colors.accent, fontSize: 12, fontWeight: '700' },
  editLink: { color: colors.primaryDeep, fontSize: 12, fontWeight: '800' },
});
