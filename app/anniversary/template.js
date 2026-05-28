import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyPage from '../../src/components/FairyPage';
import FairySticker from '../../src/components/FairySticker';
import FairyTag from '../../src/components/FairyTag';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';

const templates = [
  { id: 'firstMeet', name: '初见章节模板', subtitle: '记录第一眼、第一句话和那天的小细节。', includes: ['日记引导', '照片位 x2', '一句纪念语'], tone: undefined },
  { id: 'travel', name: '旅行章节模板', subtitle: '适合路线、风景和同日回忆拼贴。', includes: ['路线卡片', '照片位 x4', '地点标签'], tone: 'gold' },
  { id: 'birthday', name: '生日章节模板', subtitle: '把惊喜、愿望和心愿小纸条封存起来。', includes: ['愿望区', '照片位 x3', 'AI 祝福入口'], tone: undefined },
];

export default function AnniversaryTemplatePage() {
  const router = useRouter();
  const [selectedId, setSelectedId] = useState(templates[0].id);
  const selected = templates.find((item) => item.id === selectedId);

  const createWithTemplate = () => {
    router.push(`/anniversary/edit?template=${selectedId}`);
  };

  return (
    <FairyPage backgroundName="creamPaper">
      <FairyHeader
        showBack
        eyebrow="纪念日相关"
        title="专属记录模板"
        subtitle="提前排好这一页版式，等纪念日当天只需要把故事填进去。"
        right={<FairyTag tone="gold">{templates.length} 套</FairyTag>}
      />

      <FairyCard style={styles.coverCard}>
        <FairySticker name="tapeCream" size={72} rotate="-8deg" style={styles.tapeSticker} />
        <FairyImage name="anniversaryShareCover" height={220} radius={26} />
        <Text style={styles.coverTitle}>纪念日分享封面</Text>
        <Text style={styles.coverText}>选好模板后，可以把这一章生成成一张温柔分享卡。</Text>
      </FairyCard>

      {templates.length ? (
        <View style={styles.list}>
          {templates.map((item) => {
            const active = item.id === selectedId;
            return (
              <Pressable key={item.id} onPress={() => setSelectedId(item.id)}>
                <FairyCard style={[styles.card, active && styles.cardActive]}>
                  <View style={styles.cardHead}>
                    <Text style={styles.cardTitle}>{item.name}</Text>
                    <FairyTag tone={item.tone}>{active ? '已选中' : '可使用'}</FairyTag>
                  </View>
                  <Text style={styles.cardSubtitle}>{item.subtitle}</Text>
                  <View style={styles.includeRow}>
                    {item.includes.map((includeText) => (
                      <View key={includeText} style={styles.includeItem}>
                        <Ionicons name="sparkles-outline" size={14} color={colors.accent} />
                        <Text style={styles.includeText}>{includeText}</Text>
                      </View>
                    ))}
                  </View>
                </FairyCard>
              </Pressable>
            );
          })}
        </View>
      ) : (
        <FairyEmptyState imageName="emptyDiary" title="还没有模板" description="下一版会先补充初见、旅行和生日三类模板。" />
      )}

      <FairyCard style={styles.previewCard}>
        <Text style={styles.previewTitle}>当前模板预览</Text>
        <Text style={styles.previewName}>{selected?.name}</Text>
        <Text style={styles.previewDesc}>{selected?.subtitle}</Text>
      </FairyCard>

      <View style={styles.actions}>
        <FairyButton title="使用这个模板" onPress={createWithTemplate} />
        <FairyButton title="直接新建纪念日" variant="secondary" onPress={() => router.push('/anniversary/edit')} />
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  coverCard: { backgroundColor: colors.cardPink, marginBottom: spacing.xl, overflow: 'visible' },
  tapeSticker: { top: -22, left: 28 },
  coverTitle: { color: colors.text, fontSize: 20, fontWeight: '900', marginTop: spacing.md },
  coverText: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.xs },
  list: { gap: spacing.md },
  card: { padding: spacing.lg },
  cardActive: { backgroundColor: '#FFF3F5' },
  cardHead: { flexDirection: 'row', justifyContent: 'space-between', gap: spacing.md, alignItems: 'center' },
  cardTitle: { flex: 1, color: colors.text, fontSize: 17, fontWeight: '900' },
  cardSubtitle: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.sm },
  includeRow: { gap: spacing.xs, marginTop: spacing.md },
  includeItem: { flexDirection: 'row', alignItems: 'center', gap: spacing.xs },
  includeText: { color: colors.accent, fontSize: 12, fontWeight: '700' },
  previewCard: { marginTop: spacing.xl, marginBottom: spacing.lg, backgroundColor: colors.cardPink },
  previewTitle: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  previewName: { color: colors.text, fontSize: 20, fontWeight: '900', marginTop: spacing.sm },
  previewDesc: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.xs },
  actions: { gap: spacing.md },
});
