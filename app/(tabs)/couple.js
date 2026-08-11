import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import CoupleTimeline from '@/components/CoupleTimeline';
import FairyCard from '@/components/FairyCard';
import FairyPage from '@/components/FairyPage';
import FairySection from '@/components/FairySection';
import FairyTag from '@/components/FairyTag';
import FairyToast from '@/components/FairyToast';
import useFairyStore from '@/store/useFairyStore';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';

const quickLinks = [
  { icon: 'heart-outline', label: '想念你', action: 'miss' },
  { icon: 'calendar-outline', label: '纪念日', href: '/anniversary' },
  { icon: 'hourglass-outline', label: '时光胶囊', href: '/time-capsule/settings' },
  { icon: 'chatbubble-ellipses-outline', label: '留言', href: '/comments' },
];

export default function CouplePage() {
  const couple = useFairyStore((state) => state.couple);
  const timeline = useFairyStore((state) => state.timeline);
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const [toast, setToast] = useState(null);
  const nextAnniversary = anniversaries[0];

  const stats = [
    { label: '恋爱天数', value: couple.loveDays, icon: 'heart-outline' },
    { label: '共同记录', value: records.length, icon: 'library-outline' },
    { label: 'AI 作品', value: creations.length, icon: 'color-wand-outline' },
  ];

  const openQuickLink = (item) => {
    if (item.action === 'miss') {
      setToast({ tone: 'success', message: `一颗“想你”的小爱心已经送给${couple.partnerName}。` });
      return;
    }
    router.push(item.href);
  };

  return (
    <FairyPage tabSafe topSpace={28} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <View style={styles.titleBlock}><Text style={styles.eyebrow}>只属于两个人的私密故事书</Text><Text style={styles.title}>情侣空间</Text></View>

        <FairyCard style={styles.profile} contentStyle={styles.profileContent}>
          <View style={styles.profileOrb} />
          <View style={styles.avatarRow}>
            <View style={styles.avatar}><Text style={styles.avatarText}>{couple.userName?.slice(0, 1) || '我'}</Text></View>
            <View style={styles.heartBridge}><Ionicons name="heart" size={20} color={colors.white} /></View>
            <View style={styles.avatar}><Text style={styles.avatarText}>{couple.partnerName?.slice(0, 1) || 'TA'}</Text></View>
          </View>
          <Text style={styles.names}>{couple.userName} 和 {couple.partnerName}</Text>
          <Text style={styles.desc}>{couple.spaceName} · 第 {couple.loveDays} 天</Text>
          <View style={styles.profileTags}><FairyTag tone="gold">{couple.statusText}</FairyTag><FairyTag>共同记录 {records.length} 条</FairyTag></View>
        </FairyCard>

        <View style={styles.statsRow}>
          {stats.map((item) => (
            <FairyCard key={item.label} style={styles.statCard} padding={spacing.md}>
              <Ionicons name={item.icon} size={18} color={colors.accent} />
              <Text style={styles.statValue}>{item.value}</Text>
              <Text style={styles.statLabel}>{item.label}</Text>
            </FairyCard>
          ))}
        </View>

        <View style={styles.interactions}>
          {quickLinks.map((item) => (
            <Pressable key={item.label} accessibilityRole="button" style={({ pressed }) => [styles.interaction, pressed && styles.pressed]} onPress={() => openQuickLink(item)}>
              <Ionicons name={item.icon} size={21} color={colors.accent} />
              <Text style={styles.interactionText}>{item.label}</Text>
            </Pressable>
          ))}
        </View>

        <Pressable onPress={() => router.push('/anniversary')}>
          <FairyCard style={styles.anniversaryCard} padding={spacing.lg}>
            <View style={styles.anniversaryIcon}><Ionicons name={nextAnniversary?.icon || 'calendar-outline'} size={24} color={colors.primaryDeep} /></View>
            <View style={styles.anniversaryText}>
              <Text style={styles.anniversaryLabel}>纪念日入口</Text>
              <Text style={styles.anniversaryTitle}>{nextAnniversary?.title || '新的重要章节'}</Text>
              <Text style={styles.anniversaryDesc}>{nextAnniversary ? `${nextAnniversary.date} · 第 ${nextAnniversary.days} 天` : '把重要日子写进你们的故事。'}</Text>
            </View>
            <Ionicons name="chevron-forward" size={18} color={colors.accent} />
          </FairyCard>
        </Pressable>

        <FairySection title="双人故事线" description="每一次记录，都会长成新的章节">
          <CoupleTimeline items={timeline} />
        </FairySection>
      </View>
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 960 },
  pressed: { opacity: 0.68 },
  titleBlock: { alignItems: 'center', marginBottom: spacing.xl },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900' },
  profile: { marginBottom: 18, backgroundColor: colors.cardPink, overflow: 'hidden' },
  profileContent: { minHeight: 232, alignItems: 'center', justifyContent: 'center', position: 'relative' },
  profileOrb: { position: 'absolute', width: 230, height: 230, top: -120, right: -70, borderRadius: 115, backgroundColor: '#FAD0D8', opacity: 0.58 },
  avatarRow: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 14 },
  avatar: { width: 58, height: 58, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  avatarText: { color: colors.text, fontWeight: '900', fontSize: 18 },
  heartBridge: { width: 34, height: 34, borderRadius: 14, backgroundColor: colors.primaryDeep, alignItems: 'center', justifyContent: 'center', transform: [{ rotate: '-8deg' }] },
  names: { color: colors.text, fontSize: 20, fontWeight: '900' },
  desc: { color: colors.textSoft, marginTop: 8 },
  profileTags: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', gap: 8, marginTop: 14 },
  statsRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 18 },
  statCard: { flex: 1, minWidth: 160, minHeight: 112, alignItems: 'center', justifyContent: 'center' },
  statValue: { color: colors.text, fontSize: 21, fontWeight: '900', marginTop: 8 },
  statLabel: { color: colors.textSoft, fontSize: 11, marginTop: 3, fontWeight: '700', textAlign: 'center' },
  interactions: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 18 },
  interaction: { width: '47.8%', minHeight: 64, borderRadius: 20, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8 },
  interactionText: { color: colors.text, fontWeight: '800', fontSize: 13 },
  anniversaryCard: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 28, backgroundColor: colors.cardPink },
  anniversaryIcon: { width: 52, height: 52, borderRadius: 20, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' },
  anniversaryText: { flex: 1 },
  anniversaryLabel: { color: colors.accent, fontSize: 12, fontWeight: '900', marginBottom: 4 },
  anniversaryTitle: { color: colors.text, fontSize: 16, fontWeight: '900' },
  anniversaryDesc: { color: colors.textSoft, fontSize: 12, marginTop: 4 },
});
