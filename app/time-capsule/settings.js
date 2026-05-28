import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyInput from '../../src/components/FairyInput';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';

const contentTypes = ['日记', '照片', 'AI作品', '纪念日'];

export default function TimeCapsuleSettingsPage() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [unlockDate, setUnlockDate] = useState('');
  const [selectedTypes, setSelectedTypes] = useState(['日记']);
  const [capsules, setCapsules] = useState([]);
  const [error, setError] = useState('');

  const toggleType = (type) => {
    setSelectedTypes((items) => {
      if (items.includes(type)) return items.filter((item) => item !== type);
      return [...items, type];
    });
  };

  const createCapsule = () => {
    if (!title.trim() || !unlockDate.trim()) {
      setError('请先写好标题和解锁日期。');
      return;
    }
    if (!selectedTypes.length) {
      setError('至少选择一种封存内容类型。');
      return;
    }

    setCapsules((items) => [
      {
        id: `capsule-${Date.now()}`,
        title: title.trim(),
        description: description.trim() || '这页故事暂时封存在未来。',
        unlockDate: unlockDate.trim(),
        contentTypes: selectedTypes,
      },
      ...items,
    ]);

    setTitle('');
    setDescription('');
    setUnlockDate('');
    setSelectedTypes(['日记']);
    setError('');
  };

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="记录相关"
        title="时光胶囊设置"
        subtitle="封存一页童话，留给未来的某一天再轻轻翻开。"
        right={<FairyTag tone="gold">{capsules.length} 枚</FairyTag>}
      />

      <FairyCard style={styles.heroCard}>
        <FairyImage name="timeCapsuleCover" height={160} radius={26} />
        <Text style={styles.heroTitle}>封存给未来的心事</Text>
        <Text style={styles.heroText}>把这一天的心情、照片和魔法作品先放进纸页信封，到解锁日再一起拆开。</Text>
      </FairyCard>

      <FairyCard style={styles.formCard}>
        <FairyInput
          label="胶囊标题"
          icon="bookmark-outline"
          value={title}
          onChangeText={(text) => {
            setTitle(text);
            setError('');
          }}
          placeholder="例如：写给一周年后的我们"
        />
        <FairyInput
          label="内容说明"
          icon="create-outline"
          value={description}
          onChangeText={(text) => {
            setDescription(text);
            setError('');
          }}
          placeholder="写一句想留给未来的话"
          multiline
          error={error}
        />
        <FairyInput
          label="解锁日期"
          icon="calendar-outline"
          value={unlockDate}
          onChangeText={(text) => {
            setUnlockDate(text);
            setError('');
          }}
          placeholder="YYYY-MM-DD"
          helper="当前阶段使用 mock 文本日期。"
        />

        <Text style={styles.typeTitle}>封存内容类型</Text>
        <View style={styles.typeRow}>
          {contentTypes.map((type) => {
            const selected = selectedTypes.includes(type);
            return (
              <Pressable key={type} style={[styles.typeChip, selected && styles.typeChipActive]} onPress={() => toggleType(type)}>
                <Text style={[styles.typeText, selected && styles.typeTextActive]}>{type}</Text>
              </Pressable>
            );
          })}
        </View>

        <FairyButton title="封存这页童话" onPress={createCapsule} />
      </FairyCard>

      <Text style={styles.sectionTitle}>胶囊列表</Text>
      {capsules.length ? (
        <View style={styles.list}>
          {capsules.map((capsule) => (
            <FairyCard key={capsule.id} style={styles.itemCard}>
              <View style={styles.itemHead}>
                <Text style={styles.itemTitle}>{capsule.title}</Text>
                <FairyTag tone="gold">{capsule.unlockDate}</FairyTag>
              </View>
              <Text style={styles.itemDesc}>{capsule.description}</Text>
              <View style={styles.tagRow}>
                {capsule.contentTypes.map((type) => <FairyTag key={`${capsule.id}-${type}`}>{type}</FairyTag>)}
              </View>
            </FairyCard>
          ))}
        </View>
      ) : (
        <FairyEmptyState
          imageName="emptyDiary"
          title="还没有封存胶囊"
          description="创建第一枚胶囊，让今天的故事在未来发光。"
        />
      )}
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  heroCard: { backgroundColor: colors.cardPink, marginBottom: spacing.lg },
  heroTitle: { color: colors.text, fontSize: 19, fontWeight: '900', marginTop: spacing.md, textAlign: 'center' },
  heroText: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.sm, textAlign: 'center' },
  formCard: { marginBottom: spacing.xl },
  typeTitle: { color: colors.text, fontWeight: '800', fontSize: 15, marginBottom: spacing.sm },
  typeRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginBottom: spacing.lg },
  typeChip: { borderRadius: 16, paddingHorizontal: spacing.md, paddingVertical: spacing.sm, backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.border },
  typeChipActive: { backgroundColor: colors.primary, borderColor: colors.primary },
  typeText: { color: colors.textSoft, fontWeight: '800' },
  typeTextActive: { color: colors.white },
  sectionTitle: { color: colors.text, fontSize: 18, fontWeight: '900', marginBottom: spacing.md },
  list: { gap: spacing.md },
  itemCard: { padding: spacing.lg },
  itemHead: { flexDirection: 'row', justifyContent: 'space-between', gap: spacing.sm, alignItems: 'center' },
  itemTitle: { flex: 1, color: colors.text, fontSize: 17, fontWeight: '900' },
  itemDesc: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.sm },
  tagRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginTop: spacing.md },
});
