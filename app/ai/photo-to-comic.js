import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';
import { hasCapability } from '../../src/config/capabilities';
import { getApiMode } from '../../src/api/client';

const mockPhotoOptions = [
  { id: 'rain', image: 'homeCover', label: '雨天散步' },
  { id: 'city', image: 'albumCover', label: '城市晴空' },
  { id: 'flowers', image: 'anniversaryCover', label: '花束纪念' },
  { id: 'lamp', image: 'coupleCover', label: '晚风路灯' },
];
const styleOptions = ['绘本风', '手绘漫画', '水彩童话'];
const moodOptions = ['温柔', '明亮', '复古'];
const detailOptions = ['柔和', '适中', '精细'];

export default function PhotoToComicPage() {
  const isReal = getApiMode() === 'real';
  const addCreation = useFairyStore((state) => state.addCreation);
  const records = useFairyStore((state) => state.records) || [];
  const realPhotos = records.filter((item) => item.type === '照片' && item.id && (item.coverUrl || item.imageUrl || item.url));
  const photoOptions = isReal ? realPhotos.map((item) => ({ id: item.id, uri: item.coverUrl || item.imageUrl || item.url, label: item.title || '标题未提供' })) : mockPhotoOptions;
  const [selectedPhotos, setSelectedPhotos] = useState(isReal ? [] : mockPhotoOptions.slice(0, 3).map((item) => item.id));
  const [styleName, setStyleName] = useState(styleOptions[0]);
  const [mood, setMood] = useState(moodOptions[0]);
  const [detail, setDetail] = useState(detailOptions[1]);
  const [toast, setToast] = useState(null);
  const canGenerate = hasCapability('aiGeneration');
  const selectedItems = useMemo(() => photoOptions.filter((item) => selectedPhotos.includes(item.id)), [photoOptions, selectedPhotos]);

  const togglePhoto = (id) => setSelectedPhotos((current) => current.includes(id) ? current.filter((item) => item !== id) : current.length >= 6 ? current : [...current, id]);

  const generate = () => {
    if (!canGenerate || isReal) { setToast({ message: 'Real 模式暂未开放照片转漫画接口，不会创建本地模拟任务。', tone: 'info' }); return; }
    if (!selectedPhotos.length) { setToast({ message: '请至少选择一张照片', tone: 'error' }); return; }
    const creation = addCreation({ type: '漫画', title: '照片漫画 Mock 任务', source: selectedPhotos, styleName: `${styleName} · ${mood} · ${detail}`, status: '生成中 · Mock 演示任务', icon: 'images-outline', progress: 62 });
    if (!creation) { setToast({ message: '无法创建 Mock 任务。', tone: 'error' }); return; }
    router.push('/ai/progress');
  };

  return (
    <FairyPage backgroundName="creamPaper" header={<FairyHeader showBack title="照片转漫画" />} topSpace={18} bottomSpace={64}>
      <View style={styles.content}>
        {isReal && !realPhotos.length ? <FairyEmptyState imageName="emptyAlbum" title="暂无可用照片" description="当前相册没有返回带真实图片地址的照片，页面不会使用设计图冒充用户照片。" actionTitle="去相册" onAction={() => router.push('/photo/album')} /> : (
          <>
            <FairyCard style={styles.photoCard}>
              <Text style={styles.sectionTitle}>选择照片</Text>
              <Text style={styles.sectionNote}>已选 {selectedPhotos.length} 张</Text>
              <View style={styles.photoGrid}>{photoOptions.map((item) => { const active = selectedPhotos.includes(item.id); return <Pressable key={item.id} onPress={() => togglePhoto(item.id)} style={({ pressed }) => [styles.photoTile, active && styles.photoTileActive, pressed && styles.pressed]}>{item.image ? <FairyImage name={item.image} height={118} radius={16} framed={false} /> : <View style={styles.remotePlaceholder}><Ionicons name="image-outline" size={28} color={colors.textSoft} /><Text style={styles.remoteText}>真实图片地址已返回，当前组件尚未接入远程渲染</Text></View>}<Text style={styles.photoLabel}>{item.label}</Text>{active ? <Ionicons name="checkmark-circle" size={22} color={colors.primaryDeep} style={styles.check} /> : null}</Pressable>; })}</View>
            </FairyCard>
            <FairyCard style={styles.optionCard}>
              <OptionGroup title="漫画风格" options={styleOptions} value={styleName} onChange={setStyleName} />
              <OptionGroup title="画面氛围" options={moodOptions} value={mood} onChange={setMood} />
              <OptionGroup title="细节强度" options={detailOptions} value={detail} onChange={setDetail} />
            </FairyCard>
            <FairyCard style={styles.previewCard}>
              <Text style={styles.sectionTitle}>{isReal ? '真实预览尚未生成' : 'Mock 漫画预览'}</Text>
              {!isReal ? <View style={styles.previewGrid}>{selectedItems.slice(0, 4).map((item) => <FairyImage key={item.id} name={item.image} height={104} radius={12} framed={false} style={styles.previewImage} />)}</View> : <Text style={styles.previewText}>Real Mode 不使用设计图作为用户照片或生成结果。</Text>}
              <FairyTag tone="gold">{styleName} · {mood} · {detail}</FairyTag>
            </FairyCard>
            <FairyButton title={canGenerate && !isReal ? '生成 Mock 漫画' : 'AI 生成未开放'} onPress={generate} />
            <Text style={styles.estimate}>{isReal ? '不会在网络请求缺失时模拟生成成功' : 'Mock 模式仅演示本地流程'}</Text>
          </>
        )}
      </View>
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function OptionGroup({ title, options, value, onChange }) { return <View style={styles.optionGroup}><Text style={styles.sectionTitle}>{title}</Text><View style={styles.optionRow}>{options.map((item) => <Pressable key={item} onPress={() => onChange(item)} style={({ pressed }) => [styles.option, value === item && styles.optionActive, pressed && styles.pressed]}><Text style={[styles.optionText, value === item && styles.optionTextActive]}>{item}</Text></Pressable>)}</View></View>; }

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 760, alignSelf: 'center' }, photoCard: { marginBottom: spacing.lg }, sectionTitle: { color: colors.text, fontSize: 17, fontWeight: '900', marginBottom: spacing.md }, sectionNote: { color: colors.primaryDeep, fontSize: 12, fontWeight: '800', marginBottom: spacing.md }, photoGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md }, photoTile: { position: 'relative', width: '47.8%', borderRadius: 20, padding: spacing.xs, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border }, photoTileActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink }, photoLabel: { paddingVertical: spacing.sm, textAlign: 'center', color: colors.text, fontSize: 12, fontWeight: '800' }, check: { position: 'absolute', top: 4, right: 4 }, remotePlaceholder: { minHeight: 118, borderRadius: 16, alignItems: 'center', justifyContent: 'center', padding: spacing.sm, backgroundColor: colors.background }, remoteText: { marginTop: spacing.sm, color: colors.textSoft, textAlign: 'center', fontSize: 10 }, optionCard: { marginBottom: spacing.lg }, optionGroup: { marginBottom: spacing.lg }, optionRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm }, option: { flex: 1, minWidth: 90, minHeight: 44, alignItems: 'center', justifyContent: 'center', borderRadius: 16, borderWidth: 1, borderColor: colors.border }, optionActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink }, optionText: { color: colors.textSoft, fontSize: 13, fontWeight: '700' }, optionTextActive: { color: colors.primaryDeep, fontWeight: '900' }, previewCard: { marginBottom: spacing.xl, backgroundColor: colors.cardPink }, previewGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginBottom: spacing.md }, previewImage: { width: '48.8%' }, previewText: { color: colors.textSoft, lineHeight: 20, marginBottom: spacing.md }, estimate: { marginTop: spacing.md, textAlign: 'center', color: colors.textSoft, fontSize: 11 }, pressed: { opacity: 0.68 },
});