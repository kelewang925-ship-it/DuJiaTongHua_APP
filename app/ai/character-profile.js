import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyInput from '../../src/components/FairyInput';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import { getApiMode } from '../../src/api/client';
import { hasCapability } from '../../src/config/capabilities';
import colors from '../../src/theme/colors';

const moods = ['温柔', '活泼', '沉静', '俏皮'];
const outfits = ['校园风', '日常风', '旅行风'];

export default function CharacterProfilePage() {
  const [heroName, setHeroName] = useState('林小满');
  const [partnerName, setPartnerName] = useState('陆星河');
  const [relationshipTone, setRelationshipTone] = useState(moods[0]);
  const [outfitStyle, setOutfitStyle] = useState(outfits[0]);
  const [summary, setSummary] = useState('喜欢散步、热可可和把普通日子写成故事。');
  const [toast, setToast] = useState(null);
  const mode = getApiMode();
  const canSaveCharacterProfile = hasCapability('aiGeneration', mode);

  const handleSave = () => {
    if (!canSaveCharacterProfile) {
      setToast({
        tone: 'info',
        message: '真实人设保存尚未开放。当前配置不会写入云端，也不会模拟保存成功。',
      });
      return;
    }

    setToast({
      tone: 'success',
      message: '人设已保存到本地 mock 配置。',
    });
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      topSpace={24}
      bottomSpace={48}
      contentStyle={styles.content}
      keyboardShouldPersistTaps="handled"
      header={<FairyHeader showBack title="AI 人设管理" />}
    >
      <View style={styles.intro}>
        <Text style={styles.eyebrow}>AI创作相关</Text>
        <Text style={styles.subtitle}>先定义你们在绘本里的样子，再去生成漫画会更稳定。</Text>
      </View>

      <FairyCard style={styles.heroCard}>
        <View style={styles.heroIcon}>
          <Ionicons name="people-outline" size={24} color={colors.gold} />
        </View>
        <Text style={styles.heroText}>
          {canSaveCharacterProfile
            ? '当前为本地 mock 人设配置，仅用于验证页面体验与文案节奏。'
            : 'Real 模式暂未开放 AI 人设云端保存。你仍可预览配置，但不会写入本地成功状态。'}
        </Text>
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

      <FairyButton
        title={canSaveCharacterProfile ? '保存人设（mock）' : '真实人设保存未开放'}
        onPress={handleSave}
      />
      <FairyToast
        visible={Boolean(toast)}
        tone={toast?.tone}
        message={toast?.message}
        onHide={() => setToast(null)}
      />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 720, alignSelf: 'center' },
  intro: { marginBottom: 20 },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  subtitle: { color: colors.textSoft, lineHeight: 22 },
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
