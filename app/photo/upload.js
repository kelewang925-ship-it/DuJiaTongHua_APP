import { useState } from 'react';
import { Image, Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import * as ImagePicker from 'expo-image-picker';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyHeader from '@/components/FairyHeader';
import FairyInput from '@/components/FairyInput';
import FairyPage from '@/components/FairyPage';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';
import { getApiMode } from '@/api/client';

const tagOptions = [
  { id: '约会', icon: 'heart-outline' },
  { id: '晚霞', icon: 'partly-sunny-outline' },
  { id: '旅行', icon: 'airplane-outline' },
  { id: '日常', icon: 'cafe-outline' },
  { id: '合照', icon: 'people-outline' },
];

export default function PhotoUploadPage() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const isReal = getApiMode() === 'real';
  const addPhotoRecord = useFairyStore((state) => state.addPhotoRecord);
  const savePhotoCollectionReal = useFairyStore((state) => state.savePhotoCollectionReal);
  const [photos, setPhotos] = useState([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [selectedTags, setSelectedTags] = useState(['约会']);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState({});
  const [toast, setToast] = useState(null);
  const compact = width < 650;

  const pickPhotos = async () => {
    if (isSaving) return;
    try {
      const result = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ['images'], allowsMultipleSelection: true, selectionLimit: 9, quality: 0.82, orderedSelection: true });
      if (result.canceled) return;
      const selected = result.assets.slice(0, 9).map((asset) => ({ uri: asset.uri, width: asset.width, height: asset.height, fileName: asset.fileName || null, mimeType: asset.mimeType || 'image/jpeg' }));
      setPhotos(selected);
      setError((items) => ({ ...items, photos: '' }));
      setToast({ tone: 'success', message: `已选择 ${selected.length} 张照片。` });
    } catch {
      setToast({ tone: 'error', message: '暂时无法打开系统相册，请检查照片访问权限。' });
    }
  };

  const removePhoto = (index) => { if (!isSaving) setPhotos((items) => items.filter((_, itemIndex) => itemIndex !== index)); };
  const toggleTag = (tag) => { if (!isSaving) setSelectedTags((items) => items.includes(tag) ? items.filter((item) => item !== tag) : [...items, tag]); };

  const handleSave = async () => {
    if (isSaving) return;
    const nextError = {};
    if (!photos.length) nextError.photos = '请先从系统相册选择至少 1 张照片。';
    if (!title.trim()) nextError.title = '请给这组照片起一个名字。';
    if (content.trim().length > 200) nextError.content = '备注不能超过 200 字。';
    if (Object.keys(nextError).length) { setError(nextError); setToast({ tone: 'error', message: '还有内容需要补充后才能保存。' }); return; }
    setIsSaving(true);
    const payload = { title, content, tags: selectedTags.length ? selectedTags : ['照片'], photoCount: photos.length, photos };
    const result = isReal ? await savePhotoCollectionReal(payload) : { success: true, data: addPhotoRecord(payload) };
    if (!result.success) { setIsSaving(false); setToast({ tone: 'error', message: result.error?.message || '照片保存失败，请重试。' }); return; }
    const record = result.data;
    setToast({ tone: 'success', message: `《${record.title}》已经放进回忆相册。` });
    setTimeout(() => { setIsSaving(false); router.replace('/photo/album'); }, 650);
  };

  return (
    <FairyPage backgroundName="creamPaper" header={<FairyHeader showBack title="上传照片" />} topSpace={22} bottomSpace={64} contentStyle={styles.pageContent} keyboardShouldPersistTaps="handled" keyboardDismissMode="on-drag" automaticallyAdjustKeyboardInsets showsVerticalScrollIndicator>
      <View style={styles.content}>
        <View style={styles.intro}><Text style={styles.introTitle}>把这一幕贴进回忆册</Text><Text style={styles.introText}>最多选择 9 张照片，保存后会同步成为一组照片记录。</Text></View>
        <FairyCard style={[styles.pickerCard, compact && styles.pickerCardCompact]} padding={spacing.lg}>
          <Pressable accessibilityRole="button" disabled={isSaving} onPress={pickPhotos} style={({ pressed }) => [styles.pickMain, (pressed || isSaving) && styles.pressed]}><View style={styles.cameraIcon}><Ionicons name="camera-outline" size={34} color={colors.primaryDeep} /></View><Text style={styles.pickTitle}>{photos.length ? '重新选择照片' : '添加照片'}</Text><Text style={styles.pickText}>从系统相册选择 1–9 张图片</Text></Pressable>
          <View style={styles.previewGrid}>{Array.from({ length: 9 }).map((_, index) => { const photo = photos[index]; return <View key={photo?.uri || `slot-${index}`} style={styles.previewSlot}>{photo ? <><Image source={{ uri: photo.uri }} resizeMode="cover" style={styles.previewImage} /><Pressable disabled={isSaving} accessibilityLabel={`移除第${index + 1}张照片`} onPress={() => removePhoto(index)} style={styles.removePhoto}><Ionicons name="close" size={15} color={colors.white} /></Pressable></> : <Pressable disabled={isSaving} onPress={pickPhotos} style={styles.emptySlot}><Ionicons name="add" size={22} color={colors.textSoft} /></Pressable>}</View>; })}</View>
          <View style={styles.photoCountRow}><Ionicons name="images-outline" size={18} color={colors.accent} /><Text style={styles.photoCountText}>已选择 <Text style={styles.photoCountStrong}>{photos.length}</Text> / 9 张</Text></View>
          {error.photos ? <Text style={styles.photoError}>{error.photos}</Text> : null}
        </FairyCard>
        <FairyCard style={styles.formCard} padding={spacing.xl}>
          <FairyInput label="照片标题" editable={!isSaving} value={title} onChangeText={(text) => { setTitle(text); setError((items) => ({ ...items, title: '' })); }} maxLength={30} placeholder="给这组照片起个名字吧" error={error.title} />
          <FairyInput label="备注" editable={!isSaving} value={content} onChangeText={(text) => { setContent(text); setError((items) => ({ ...items, content: '' })); }} multiline maxLength={200} placeholder="记录下这些照片背后的故事……" error={error.content} helper={`${content.length}/200`} helperInside />
          <Text style={styles.fieldLabel}>标签</Text><View style={styles.tagRow}>{tagOptions.map((tag) => { const active = selectedTags.includes(tag.id); return <Pressable key={tag.id} disabled={isSaving} accessibilityRole="checkbox" accessibilityState={{ checked: active }} onPress={() => toggleTag(tag.id)} style={({ pressed }) => [styles.tagOption, active && styles.tagOptionActive, (pressed || isSaving) && styles.pressed]}><Ionicons name={tag.icon} size={17} color={active ? colors.primaryDeep : colors.textSoft} /><Text style={[styles.tagText, active && styles.tagTextActive]}>{tag.id}</Text>{active ? <Ionicons name="checkmark-circle" size={16} color={colors.primaryDeep} /> : null}</Pressable>; })}</View>
        </FairyCard>
        <FairyButton title={isSaving ? '正在保存……' : '保存照片'} disabled={isSaving} onPress={handleSave} leftContent={<Ionicons name="heart-outline" size={20} color={colors.white} />} />
        <View style={styles.privacy}><Ionicons name="lock-closed-outline" size={14} color={colors.gold} /><Text style={styles.privacyText}>{isReal ? '照片将上传到当前情侣空间的私有 Storage，仅双方可访问' : 'Mock 模式只保存本地演示记录，不会上传照片'}</Text></View>
      </View>
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 820 }, pressed: { opacity: 0.65 }, intro: { alignItems: 'center', marginBottom: spacing.xl }, introTitle: { color: colors.text, fontSize: 21, fontWeight: '900' }, introText: { color: colors.textSoft, textAlign: 'center', lineHeight: 20, marginTop: spacing.sm },
  pickerCard: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.xl, backgroundColor: 'rgba(255,249,244,0.97)', marginBottom: spacing.lg }, pickerCardCompact: { flexDirection: 'column' }, pickMain: { width: 230, minHeight: 290, alignItems: 'center', justifyContent: 'center', borderRadius: 24, borderWidth: 2, borderStyle: 'dashed', borderColor: colors.primary, backgroundColor: colors.cardPink, padding: spacing.lg }, cameraIcon: { width: 76, height: 76, borderRadius: 30, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border }, pickTitle: { color: colors.text, fontSize: 19, fontWeight: '900', marginTop: spacing.lg }, pickText: { color: colors.textSoft, fontSize: 11, textAlign: 'center', marginTop: spacing.sm }, previewGrid: { flex: 1, minWidth: 260, flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, alignContent: 'center' }, previewSlot: { width: '30%', aspectRatio: 0.78, minWidth: 74, borderRadius: 14, overflow: 'hidden', backgroundColor: colors.background, borderWidth: 1, borderColor: colors.border, position: 'relative' }, previewImage: { width: '100%', height: '100%' }, emptySlot: { flex: 1, alignItems: 'center', justifyContent: 'center' }, removePhoto: { position: 'absolute', top: 4, right: 4, width: 25, height: 25, borderRadius: 13, alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(107,79,79,0.72)' }, photoCountRow: { width: '100%', flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, paddingTop: spacing.md, borderTopWidth: 1, borderTopColor: colors.border }, photoCountText: { color: colors.textSoft, fontSize: 13 }, photoCountStrong: { color: colors.primaryDeep, fontWeight: '900' }, photoError: { width: '100%', color: colors.primaryDeep, fontSize: 12, textAlign: 'center', fontWeight: '700' },
  formCard: { backgroundColor: 'rgba(255,249,244,0.97)', marginBottom: spacing.lg }, fieldLabel: { color: colors.text, fontSize: 15, fontWeight: '800', marginBottom: spacing.sm }, tagRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm }, tagOption: { minHeight: 44, flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: spacing.md, borderRadius: 17, backgroundColor: colors.background, borderWidth: 1, borderColor: colors.border }, tagOptionActive: { backgroundColor: colors.cardPink, borderColor: colors.primaryDeep }, tagText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' }, tagTextActive: { color: colors.primaryDeep }, privacy: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, marginTop: spacing.lg }, privacyText: { flex: 1, color: colors.textSoft, fontSize: 11, textAlign: 'center' },
});
