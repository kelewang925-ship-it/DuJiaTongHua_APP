import { useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyInput from '../../src/components/FairyInput';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';

const moods = ['温柔', '活泼', '沉静', '俏皮'];
const outfits = ['校园风', '日常风', '旅行风'];

export default function CharacterProfilePage() {
  const [heroName, setHeroName] = useState('林小满');
  const [partnerName, setPartnerName] = useState('陆星河');
  const [relationshipTone, setRelationshipTone] = useState(moods[0]);
  const [outfitStyle, setOutfitStyle] = useState(outfits[0]);
  const [summary, setSummary] = useState('喜欢散步、热可可和把普通日子写成故事。');
  const [toastVisible, setToastVisible] = useState(false);

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.eyebrow}>AI创作相关</Text>
      <Text style={styles.title}>AI 人设管理</Text>
      <Text style={styles.subtitle}>先定义你们在绘本里的样子，再去生成漫画会更稳定。</Text>

      <FairyCard style={styles.heroCard}>
        <View style={styles.heroIcon}>
          <Ionicons name="people-outline" size={24} color={colors.gold} />
        </View>
        <Text style={styles.heroText}>当前是本地 mock 人设配置，不会接真实后端，适合先验证页面体验与文案节奏。</Text>
      </FairyCard>

      <FairyCard style={styles.formCard}>
        <FairyInput label="主角昵称" icon="person-outline" value={heroName} onChangeText={setHeroName} />
        <FairyInput label="伴侣昵称" icon="person-circle-outline" value={partnerName} onChangeText={setPartnerName} />
        <FairyInput
          label="角色说明"
          icon="create-outline"
          value={summary}
          onChangeText={setSummary}
          multiline
          placeholder="写一句角色描述，帮助 AI 更稳定地生成气质。"
        />

        <Text style={styles.fieldTitle}>关系氛围</Text>
        <View style={styles.row}>
          {moods.map((item) => (
            <Pressable
              key={item}
              style={[styles.chip, relationshipTone === item && styles.activeChip]}
              onPress={() => setRelationshipTone(item)}
            >
              <Text style={[styles.chipText, relationshipTone === item && styles.activeText]}>{item}</Text>
            </Pressable>
          ))}
        </View>

        <Text style={styles.fieldTitle}>默认服装风格</Text>
        <View style={styles.row}>
          {outfits.map((item) => (
            <Pressable
              key={item}
              style={[styles.chip, outfitStyle === item && styles.activeChip]}
              onPress={() => setOutfitStyle(item)}
            >
              <Text style={[styles.chipText, outfitStyle === item && styles.activeText]}>{item}</Text>
            </Pressable>
          ))}
        </View>
      </FairyCard>

      <FairyCard style={styles.previewCard}>
        <Text style={styles.previewTitle}>本次生成将使用</Text>
        <View style={styles.previewRow}>
          <FairyTag tone="gold">{heroName}</FairyTag>
          <FairyTag tone="gold">{partnerName}</FairyTag>
          <FairyTag>{relationshipTone}</FairyTag>
          <FairyTag>{outfitStyle}</FairyTag>
        </View>
      </FairyCard>

      <FairyButton title="保存人设（mock）" onPress={() => setToastVisible(true)} />
      <FairyToast
        visible={toastVisible}
        tone="success"
        message="人设已保存到本地 mock 配置。"
        onHide={() => setToastVisible(false)}
      />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  heroCard: { flexDirection: 'row', gap: 12, backgroundColor: colors.cardPink, marginBottom: 16 },
  heroIcon: {
    width: 44,
    height: 44,
    borderRadius: 16,
    backgroundColor: '#FFF5DF',
    borderWidth: 1,
    borderColor: colors.border,
    alignItems: 'center',
    justifyContent: 'center',
  },
  heroText: { flex: 1, color: colors.textSoft, lineHeight: 21 },
  formCard: { marginBottom: 16 },
  fieldTitle: { color: colors.text, fontSize: 15, fontWeight: '800', marginBottom: 8 },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 16 },
  chip: {
    borderRadius: 16,
    paddingHorizontal: 12,
    paddingVertical: 8,
    backgroundColor: colors.cardPink,
    borderWidth: 1,
    borderColor: colors.border,
  },
  activeChip: { backgroundColor: colors.primary, borderColor: colors.primary },
  chipText: { color: colors.textSoft, fontWeight: '700' },
  activeText: { color: colors.white },
  previewCard: { marginBottom: 22 },
  previewTitle: { color: colors.text, fontSize: 15, fontWeight: '800', marginBottom: 10 },
  previewRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
});
