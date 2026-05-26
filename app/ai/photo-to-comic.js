import { useMemo, useState } from 'react';
import { View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import FairyPage from '../../src/components/FairyPage';
import FairyHeader from '../../src/components/FairyHeader';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyInput from '../../src/components/FairyInput';
import FairyTag from '../../src/components/FairyTag';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import useFairyStore from '../../src/store/useFairyStore';

const comicStyles = ['童话绘本', '暖色漫画', '手账贴纸'];

export default function PhotoToComicPage() {
  const records = useFairyStore((state) => state.records);
  const addCreation = useFairyStore((state) => state.addCreation);
  const photoRecords = useMemo(() => records.filter((item) => item.type === '照片'), [records]);
  const [selectedId, setSelectedId] = useState(photoRecords[0]?.id);
  const [styleName, setStyleName] = useState(comicStyles[0]);
  const [title, setTitle] = useState(photoRecords[0] ? `${photoRecords[0].title} · 漫画版` : '照片生成的小漫画');

  const selectedPhoto = photoRecords.find((item) => item.id === selectedId) || photoRecords[0];

  const handleGenerate = () => {
    if (!selectedPhoto) return;
    addCreation({
      type: '漫画',
      title: title.trim() || `${selectedPhoto.title} · 漫画版`,
      status: `生成中 · 照片转漫画 · ${styleName}`,
      icon: 'color-palette-outline',
    });
    router.push('/ai/progress');
  };

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="照片魔法"
        title="照片转漫画"
        subtitle="选择一组照片，把真实瞬间画成一页恋爱漫画。"
      />

      {photoRecords.length === 0 ? (
        <FairyEmptyState
          scene="album"
          title="还没有可以生成的照片"
          description="先上传一组约会、旅行或日常照片，再把它变成童话漫画。"
          actionTitle="去上传照片"
          onAction={() => router.push('/photo/upload')}
        />
      ) : (
        <>
          <FairyCard style={styles.heroCard}>
            <View style={styles.heroIcon}>
              <Ionicons name="images-outline" size={28} color={colors.accent} />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.heroTitle}>选择一组回忆</Text>
              <Text style={styles.heroText}>AI 会保留照片里的情绪，把它重新画成绘本分镜。</Text>
            </View>
          </FairyCard>

          <Text style={styles.section}>照片组</Text>
          <View style={styles.photoList}>
            {photoRecords.map((item) => {
              const active = item.id === selectedPhoto?.id;
              return (
                <Pressable key={item.id} onPress={() => {
                  setSelectedId(item.id);
                  setTitle(`${item.title} · 漫画版`);
                }}>
                  <FairyCard style={[styles.photoCard, active && styles.activePhotoCard]}>
                    <View style={[styles.photoMock, active && styles.activePhotoMock]}>
                      <Ionicons name="image-outline" size={26} color={active ? colors.white : colors.accent} />
                      <Text style={[styles.photoCount, active && styles.activePhotoCount]}>{item.photoCount || 3} 张</Text>
                    </View>
                    <View style={{ flex: 1 }}>
                      <Text style={styles.photoTitle}>{item.title}</Text>
                      <Text style={styles.photoDesc} numberOfLines={2}>{item.content}</Text>
                      <View style={styles.tagRow}>
                        {(item.tags || ['照片']).slice(0, 2).map((tag) => <FairyTag key={tag}>{tag}</FairyTag>)}
                      </View>
                    </View>
                  </FairyCard>
                </Pressable>
              );
            })}
          </View>

          <FairyCard style={styles.configCard}>
            <FairyInput
              label="作品名称"
              icon="sparkles-outline"
              value={title}
              onChangeText={setTitle}
              placeholder="例如：奶油蛋糕和你 · 漫画版"
            />
            <Text style={styles.configLabel}>漫画风格</Text>
            <View style={styles.styleRow}>
              {comicStyles.map((item) => (
                <Pressable key={item} style={[styles.styleChoice, styleName === item && styles.activeStyle]} onPress={() => setStyleName(item)}>
                  <Text style={[styles.styleText, styleName === item && styles.activeStyleText]}>{item}</Text>
                </Pressable>
              ))}
            </View>
          </FairyCard>

          <FairyButton title="生成照片漫画" onPress={handleGenerate} />
        </>
      )}
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  heroCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, marginBottom: spacing.xl, backgroundColor: colors.cardPink },
  heroIcon: { width: 54, height: 54, borderRadius: 22, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  heroTitle: { color: colors.text, fontSize: 18, fontWeight: '900' },
  heroText: { color: colors.textSoft, lineHeight: 21, marginTop: 6, fontSize: 13 },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: spacing.md },
  photoList: { gap: spacing.md, marginBottom: spacing.xl },
  photoCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.md },
  activePhotoCard: { backgroundColor: '#FFF4F1', borderColor: colors.primaryDeep },
  photoMock: { width: 72, height: 72, borderRadius: 22, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  activePhotoMock: { backgroundColor: colors.primaryDeep },
  photoCount: { color: colors.textSoft, fontSize: 11, marginTop: 4, fontWeight: '700' },
  activePhotoCount: { color: colors.white },
  photoTitle: { color: colors.text, fontSize: 15, fontWeight: '900' },
  photoDesc: { color: colors.textSoft, fontSize: 12, lineHeight: 18, marginTop: 4 },
  tagRow: { flexDirection: 'row', gap: spacing.xs, marginTop: spacing.sm, flexWrap: 'wrap' },
  configCard: { marginBottom: spacing.xl },
  configLabel: { color: colors.text, fontWeight: '900', marginBottom: spacing.sm },
  styleRow: { flexDirection: 'row', gap: spacing.sm },
  styleChoice: { flex: 1, minHeight: 44, borderRadius: 16, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' },
  activeStyle: { backgroundColor: colors.primaryDeep, borderColor: colors.primaryDeep },
  styleText: { color: colors.text, fontSize: 12, fontWeight: '800' },
  activeStyleText: { color: colors.white },
});
