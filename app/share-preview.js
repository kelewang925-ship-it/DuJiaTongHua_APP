import { useMemo, useState } from 'react';
import { Pressable, Share, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams, useRouter } from 'expo-router';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyPage from '@/components/FairyPage';
import FairySticker from '@/components/FairySticker';
import FairyTag from '@/components/FairyTag';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';
import { richTextToPlainText } from '@/utils/richText';
import { hasCapability } from '@/config/capabilities';

const privacyOptions = [
  { id: 'nickname', label: '显示昵称', icon: 'people-outline' },
  { id: 'date', label: '显示日期', icon: 'calendar-outline' },
  { id: 'place', label: '显示地点', icon: 'location-outline' },
];
const shareStyles = [
  { id: 'daily', label: '温柔日常', imageName: 'sharePreviewCover', detail: '完整绘本封面' },
  { id: 'anniversary', label: '纪念日', imageName: 'anniversaryShareCover', detail: '适合重要日期' },
  { id: 'comic', label: '漫画风', imageName: 'aiComicTriptych', detail: '三联故事分镜' },
  { id: 'paper', label: '极简纸感', imageName: 'homeCover', detail: '留白与短句' },
];

export default function SharePreviewPage() {
  const router = useRouter();
  const { id, type } = useLocalSearchParams();
  const targetId = Array.isArray(id) ? id[0] : id;
  const targetType = Array.isArray(type) ? type[0] : type;
  const { width } = useWindowDimensions();
  const records = useFairyStore((state) => state.records) || [];
  const creations = useFairyStore((state) => state.creations) || [];
  const profile = useFairyStore((state) => state.profile) || null;
  const couple = useFairyStore((state) => state.couple) || null;
  const target = useMemo(() => {
    if (!targetId || !targetType) return null;
    if (targetType === 'comic' || targetType === 'video') {
      return creations.find((item) => item.id === targetId && (targetType === 'video' ? item.type === '视频' : item.type !== '视频')) || null;
    }
    return records.find((item) => item.id === targetId) || null;
  }, [creations, records, targetId, targetType]);
  const [selectedPrivacy, setSelectedPrivacy] = useState(['nickname', 'date']);
  const [styleId, setStyleId] = useState(targetType === 'comic' ? 'comic' : 'daily');
  const [saved, setSaved] = useState(false);
  const [sharing, setSharing] = useState(false);
  const [toast, setToast] = useState(null);
  const compact = width < 640;
  const canPersistShareCard = hasCapability('shareCardPersistence');
  const canSystemShare = hasCapability('systemShare');
  const activeStyle = shareStyles.find((item) => item.id === styleId) || shareStyles[0];
  const description = useMemo(() => richTextToPlainText(target?.content || target?.resultSummary || target?.description), [target]);
  const displayName = couple?.displayName || profile?.nickname || target?.authorName || '';
  const displayDate = target?.date || target?.createdAt || '';
  const displayPlace = target?.location || target?.place || '';

  if (!target) {
    return (
      <FairyPage backgroundName="creamPaper" header={<FairyHeader showBack title="分享预览" />} topSpace={28} bottomSpace={64}>
        <FairyEmptyState icon="share-social-outline" title="没有找到要分享的内容" description="这条内容可能已被删除，或当前分享链接已经失效。" actionTitle="返回上一页" onAction={() => router.back()} />
      </FairyPage>
    );
  }

  const togglePrivacy = (privacyId) => setSelectedPrivacy((items) => items.includes(privacyId) ? items.filter((item) => item !== privacyId) : [...items, privacyId]);
  const visibleMeta = [
    selectedPrivacy.includes('nickname') ? displayName : '',
    selectedPrivacy.includes('date') ? displayDate : '',
    selectedPrivacy.includes('place') ? displayPlace : '',
  ].filter(Boolean);

  const saveCard = () => {
    if (!canPersistShareCard) {
      setToast({ tone: 'info', message: 'Real 模式暂未开放分享卡收藏，不会模拟保存成功。' });
      return;
    }
    setSaved(true);
    setToast({ tone: 'success', message: '分享卡已收藏到应用内，随时可以再次分享。' });
  };

  const shareCard = async () => {
    if (!canSystemShare || sharing) return;
    setSharing(true);
    try {
      const title = target.title?.trim() || '未命名内容';
      const result = await Share.share({ title, message: `《${title}》${description ? `\n${description.slice(0, 110)}` : ''}${visibleMeta.length ? `\n${visibleMeta.join(' · ')}` : ''}` });
      if (result?.action === Share.dismissedAction) {
        setToast({ tone: 'info', message: '已取消分享，没有内容被发送。' });
        return;
      }
      if (result?.action !== Share.sharedAction) {
        setToast({ tone: 'info', message: '分享面板已关闭，未确认内容是否发送。' });
        return;
      }
      setToast({ tone: 'success', message: '已交给系统分享目标处理。' });
    } catch {
      setToast({ tone: 'error', message: '这次没有打开分享面板，请稍后再试。' });
    } finally {
      setSharing(false);
    }
  };

  return (
    <FairyPage backgroundName="creamPaper" header={<FairyHeader showBack title="分享预览" right={<Pressable accessibilityRole="button" onPress={saveCard} style={({ pressed }) => [styles.headerSave, pressed && styles.pressed]}><Text style={styles.headerSaveText}>{saved ? '已保存' : canPersistShareCard ? '保存' : '未开放'}</Text></Pressable>} />} topSpace={24} bottomSpace={64} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <FairyCard style={styles.previewCard} padding={spacing.md}>
          <FairySticker name="tapeCream" size={74} rotate="-6deg" style={styles.cardTape} />
          <FairySticker name="polaroidCorner" size={48} rotate="8deg" style={styles.cornerSticker} />
          <View style={styles.coverWrap}><FairyImage name={target.previewImageName || activeStyle.imageName} height={compact ? 330 : 470} radius={26} framed={false} resizeMode="cover" /></View>
          <View style={styles.previewCopy}>
            <Text style={styles.kicker}>属于我们的每一天，都是独一无二的童话</Text>
            <Text style={styles.cardTitle}>{target.title?.trim() || '未命名内容'}</Text>
            {description ? <Text numberOfLines={4} style={styles.cardDesc}>{description}</Text> : null}
            {visibleMeta.length ? <View style={styles.metaRow}>{visibleMeta.map((item, index) => <FairyTag key={`${item}-${index}`} tone={index === 1 ? 'gold' : 'default'}>{item}</FairyTag>)}</View> : null}
          </View>
        </FairyCard>

        <View style={styles.sectionHeading}><Ionicons name="heart-outline" size={17} color={colors.primaryDeep} /><Text style={styles.sectionTitle}>选择分享风格</Text><Ionicons name="heart-outline" size={17} color={colors.primaryDeep} /></View>
        <View style={styles.styleGrid}>{shareStyles.map((item) => { const active = styleId === item.id; return <Pressable key={item.id} accessibilityRole="button" accessibilityState={{ selected: active }} onPress={() => setStyleId(item.id)} style={({ pressed }) => [styles.styleOption, compact && styles.styleOptionCompact, active && styles.styleOptionActive, pressed && styles.pressed]}><FairyImage name={item.imageName} height={112} radius={16} framed={false} resizeMode="cover" /><Text style={[styles.styleLabel, active && styles.styleLabelActive]}>{item.label}</Text><Text style={styles.styleDetail}>{item.detail}</Text>{active ? <View style={styles.selectedBadge}><Ionicons name="checkmark" size={16} color={colors.white} /></View> : null}</Pressable>; })}</View>

        <FairyCard style={styles.privacyCard} padding={spacing.lg}>
          <View style={styles.privacyTitleRow}><View><Text style={styles.privacyTitle}>隐私控制</Text><Text style={styles.privacySubtitle}>只分享你愿意展示的信息</Text></View><Ionicons name="shield-checkmark-outline" size={26} color={colors.gold} /></View>
          <View style={styles.optionList}>{privacyOptions.map((option) => { const available = option.id === 'nickname' ? Boolean(displayName) : option.id === 'date' ? Boolean(displayDate) : Boolean(displayPlace); const active = available && selectedPrivacy.includes(option.id); return <Pressable key={option.id} disabled={!available} accessibilityRole="checkbox" accessibilityState={{ checked: active, disabled: !available }} onPress={() => togglePrivacy(option.id)} style={({ pressed }) => [styles.optionItem, active && styles.optionItemActive, !available && styles.disabled, pressed && styles.pressed]}><View style={styles.optionIcon}><Ionicons name={option.icon} size={19} color={active ? colors.primaryDeep : colors.textSoft} /></View><Text style={styles.optionText}>{option.label}</Text><View style={[styles.checkDot, active && styles.checkDotActive]}>{active ? <Ionicons name="checkmark" size={13} color={colors.white} /> : null}</View></Pressable>; })}</View>
        </FairyCard>

        <View style={[styles.actions, compact && styles.actionsCompact]}>
          <FairyButton title={saved ? '已保存到收藏' : canPersistShareCard ? '保存分享卡' : '分享卡收藏未开放'} variant="secondary" disabled={saved} onPress={saveCard} style={styles.action} leftContent={<Ionicons name={saved ? 'checkmark-circle-outline' : 'download-outline'} size={19} color={colors.text} />} />
          <FairyButton title={!canSystemShare ? '系统分享未开放' : sharing ? '正在打开分享…' : '分享给 TA'} disabled={!canSystemShare || sharing} onPress={shareCard} style={styles.action} leftContent={<Ionicons name="paper-plane-outline" size={19} color={colors.white} />} />
        </View>
        <Pressable onPress={() => router.back()} style={({ pressed }) => [styles.backLink, pressed && styles.pressed]}><Ionicons name="create-outline" size={16} color={colors.accent} /><Text style={styles.backLinkText}>返回继续调整内容</Text></Pressable>
      </View>
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 760 }, pressed: { opacity: 0.65 }, disabled: { opacity: 0.38 },
  headerSave: { width: 64, minHeight: 44, alignItems: 'flex-end', justifyContent: 'center' }, headerSaveText: { color: colors.text, fontSize: 14, fontWeight: '900' },
  previewCard: { backgroundColor: 'rgba(255,249,244,0.97)', marginBottom: spacing.xxl, overflow: 'visible' }, cardTape: { top: -22, left: 28 }, cornerSticker: { top: 258, right: 24 }, coverWrap: { overflow: 'hidden', borderRadius: 26 }, previewCopy: { alignItems: 'center', paddingHorizontal: spacing.lg, paddingVertical: spacing.xl }, kicker: { color: colors.textSoft, fontSize: 12, textAlign: 'center' }, cardTitle: { color: colors.text, fontSize: 28, lineHeight: 36, fontWeight: '900', textAlign: 'center', marginTop: spacing.md }, cardDesc: { maxWidth: 560, color: colors.textSoft, lineHeight: 22, textAlign: 'center', marginTop: spacing.md }, metaRow: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', gap: spacing.sm, marginTop: spacing.lg },
  sectionHeading: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.md, marginBottom: spacing.lg }, sectionTitle: { color: colors.text, fontSize: 19, fontWeight: '900' },
  styleGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md, marginBottom: spacing.xxl }, styleOption: { width: '23%', minWidth: 150, flexGrow: 1, padding: spacing.sm, borderRadius: 22, backgroundColor: colors.card, borderWidth: 2, borderColor: 'transparent', position: 'relative' }, styleOptionCompact: { width: '46%', minWidth: 130 }, styleOptionActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink }, styleLabel: { color: colors.text, fontSize: 14, fontWeight: '900', textAlign: 'center', marginTop: spacing.sm }, styleLabelActive: { color: colors.primaryDeep }, styleDetail: { color: colors.textSoft, fontSize: 10, textAlign: 'center', marginTop: 3 }, selectedBadge: { position: 'absolute', right: -7, bottom: -7, width: 29, height: 29, borderRadius: 15, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.primaryDeep, borderWidth: 2, borderColor: colors.white },
  privacyCard: { marginBottom: spacing.xl, backgroundColor: 'rgba(255,249,244,0.96)' }, privacyTitleRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.md }, privacyTitle: { color: colors.text, fontSize: 18, fontWeight: '900' }, privacySubtitle: { color: colors.textSoft, fontSize: 11, marginTop: 4 }, optionList: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginTop: spacing.lg }, optionItem: { minWidth: 160, flex: 1, minHeight: 52, flexDirection: 'row', alignItems: 'center', gap: spacing.sm, paddingHorizontal: spacing.md, borderRadius: 17, backgroundColor: colors.background, borderWidth: 1, borderColor: colors.border }, optionItemActive: { backgroundColor: colors.cardPink, borderColor: colors.primaryDeep }, optionIcon: { width: 28, alignItems: 'center' }, optionText: { flex: 1, color: colors.text, fontWeight: '800' }, checkDot: { width: 22, height: 22, borderRadius: 11, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card }, checkDotActive: { backgroundColor: colors.primaryDeep, borderColor: colors.primaryDeep },
  actions: { flexDirection: 'row', gap: spacing.md }, actionsCompact: { flexDirection: 'column' }, action: { flex: 1 }, backLink: { minHeight: 48, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, marginTop: spacing.md }, backLinkText: { color: colors.accent, fontSize: 12, fontWeight: '800' },
});
