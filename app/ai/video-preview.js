import { ScrollView, Text, StyleSheet, View, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyTag from '../../src/components/FairyTag';
import useFairyStore from '../../src/store/useFairyStore';

export default function VideoPreviewPage() {
  const creations = useFairyStore((state) => state.creations);
  const latestVideo = creations.find((item) => item.type === '视频') || creations[0];

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>视频预览 / 编辑</Text>
      <Text style={styles.subtitle}>在导出前确认封面、字幕、音乐和转场。</Text>

      <FairyCard style={styles.playerCard}>
        <View style={styles.playerMock}>
          <Ionicons name="play-circle" size={62} color={colors.white} />
          <Text style={styles.playerTitle}>{latestVideo?.title || '回忆放映机预览'}</Text>
        </View>
        <View style={styles.metaRow}>
          <FairyTag tone="gold">{latestVideo?.type || '视频'}</FairyTag>
          <Text style={styles.status}>{latestVideo?.status || '等待生成'}</Text>
        </View>
      </FairyCard>

      <FairyCard style={styles.timelineCard}>
        <Text style={styles.sectionTitle}>时间线</Text>
        {['封面显影', '日记旁白', '照片翻页', '结尾字幕'].map((item, index) => (
          <View key={item} style={styles.clipRow}>
            <View style={styles.clipDot}><Text style={styles.clipNum}>{index + 1}</Text></View>
            <View style={{ flex: 1 }}>
              <Text style={styles.clipTitle}>{item}</Text>
              <Text style={styles.clipText}>{index === 0 ? '选择最温柔的一帧作为封面' : '可继续调整字幕、节奏和转场'}</Text>
            </View>
          </View>
        ))}
      </FairyCard>

      <FairyCard style={styles.editCard}>
        <Text style={styles.sectionTitle}>编辑项目</Text>
        <View style={styles.editGrid}>
          {[
            ['text-outline', '字幕'],
            ['musical-notes-outline', '音乐'],
            ['color-wand-outline', '转场'],
            ['image-outline', '封面'],
          ].map((item) => (
            <Pressable key={item[1]} style={styles.editItem}>
              <Ionicons name={item[0]} size={22} color={colors.accent} />
              <Text style={styles.editText}>{item[1]}</Text>
            </Pressable>
          ))}
        </View>
      </FairyCard>

      <FairyButton title="保存成品" onPress={() => router.replace('/(tabs)/workshop')} />
      <FairyButton title="重新生成" variant="secondary" style={styles.secondary} onPress={() => router.push('/ai/video-config')} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  playerCard: { backgroundColor: colors.cardPink, marginBottom: 16 },
  playerMock: { height: 220, borderRadius: 26, backgroundColor: colors.accent, alignItems: 'center', justifyContent: 'center', marginBottom: 16, overflow: 'hidden' },
  playerTitle: { color: colors.white, fontWeight: '800', fontSize: 18, marginTop: 14, textAlign: 'center' },
  metaRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  status: { color: colors.textSoft, fontSize: 12, flex: 1, textAlign: 'right' },
  timelineCard: { marginBottom: 16 },
  sectionTitle: { color: colors.text, fontSize: 17, fontWeight: '800', marginBottom: 14 },
  clipRow: { flexDirection: 'row', gap: 12, marginBottom: 14 },
  clipDot: { width: 30, height: 30, borderRadius: 12, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  clipNum: { color: colors.accent, fontWeight: '800', fontSize: 12 },
  clipTitle: { color: colors.text, fontWeight: '800', fontSize: 14 },
  clipText: { color: colors.textSoft, marginTop: 3, fontSize: 12, lineHeight: 18 },
  editCard: { marginBottom: 22 },
  editGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  editItem: { width: '47%', height: 82, borderRadius: 22, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  editText: { color: colors.text, fontWeight: '800', marginTop: 8 },
  secondary: { marginTop: 12 },
});
