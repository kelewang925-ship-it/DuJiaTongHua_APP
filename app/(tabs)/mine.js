import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import { signOut } from '@/api/authApi';
import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyDialog from '@/components/FairyDialog';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyIllustration from '@/components/FairyIllustration';
import FairyPage from '@/components/FairyPage';
import FairyRequestState from '@/components/FairyRequestState';
import FairyToast from '@/components/FairyToast';
import useFairyStore from '@/store/useFairyStore';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import { getApiMode } from '@/api/client';

const menu = [
  ['create-outline', '草稿箱', '查看当前设备草稿', '/drafts'],
  ['calendar-outline', '纪念日管理', '重要章节都在这里', '/anniversary'],
  ['time-outline', '时光胶囊', '封存一页未来再打开', '/time-capsule/settings'],
  ['pricetag-outline', '标签管理', '整理回忆索引与筛选', '/tags'],
  ['notifications-outline', '互动通知', '查看真实通知与提醒', '/notifications'],
  ['document-text-outline', 'PDF 导出', '把故事装订成册', '/data/pdf-export'],
  ['archive-outline', '数据备份', '查看可用备份能力', '/data/backup'],
  ['save-outline', '存储空间', '查看真实占用与缓存', '/data/storage'],
  ['share-social-outline', '分享预览', '生成可用分享卡片', '/share-preview'],
  ['sparkles-outline', '会员中心', '查看真实会员状态与方案', '/membership'],
  ['search-outline', '记录搜索', '按关键词找回故事', '/search'],
  ['help-circle-outline', '帮助反馈', '问题与建议入口', '/help-feedback'],
  ['settings-outline', '设置', '账号、通知与隐私', '/settings'],
];

export default function MinePage() {
  const { width } = useWindowDimensions();
  const compact = width < 700;
  const isReal = getApiMode() === 'real';
  const coupleState = useFairyStore((state) => state.couple);
  const profile = useFairyStore((state) => state.profile);
  const loading = useFairyStore((state) => Boolean(state.loading?.bootstrap));
  const loadError = useFairyStore((state) => state.errors?.bootstrap || null);
  const refreshCoreData = useFairyStore((state) => state.refreshCoreData);
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const stats = useMemo(() => ({
    diaryCount: (records || []).filter((item) => item.type === '日记').length,
    photoCount: (records || []).filter((item) => item.type === '照片').reduce((sum, item) => sum + (item.photoCount || 0), 0),
    creationCount: (creations || []).length,
    anniversaryCount: (anniversaries || []).length,
  }), [anniversaries, creations, records]);
  const [showSignOut, setShowSignOut] = useState(false);
  const [toast, setToast] = useState(null);

  const relation = isReal ? coupleState?.couple : coupleState;
  const currentProfile = isReal ? profile || coupleState?.user : { nickname: coupleState?.userName };
  const partnerProfile = isReal ? coupleState?.partner : { nickname: coupleState?.partnerName };
  const userName = currentProfile?.nickname || '';
  const partnerName = partnerProfile?.nickname || '';
  const startedAt = relation?.startedAt;
  const loveDays = startedAt ? calculateDays(startedAt) : null;
  const bound = isReal ? Boolean(relation?.id && relation?.status === 'active' && partnerProfile?.id) : Boolean(coupleState);

  const handleSignOut = async () => {
    setShowSignOut(false);
    const result = await signOut();
    if (!result.success) { setToast({ tone: 'error', message: result.error?.message || '退出登录失败。' }); return; }
    router.replace('/login');
  };

  return (
    <FairyPage backgroundName="creamPaper" tabSafe topSpace={28} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <View style={styles.titleBlock}><Text style={styles.eyebrow}>账号资料与收藏管理</Text><Text style={styles.title}>我的童话</Text></View>
        {isReal ? <FairyRequestState loading={loading} error={loadError} onRetry={refreshCoreData} /> : null}
        {!loading && !loadError ? (
          <>
            <FairyCard style={[styles.profile, !compact && styles.profileWide]}>
              <View style={styles.profileCopy}>
                <View style={styles.profileTop}>
                  <View style={styles.avatar}><Text style={styles.avatarText}>{userName ? userName.slice(0, 1) : '?'}</Text></View>
                  <View style={styles.profileText}><Text style={styles.name}>{userName || '昵称未提供'}</Text><Text style={styles.desc}>{bound ? `与 ${partnerName || '伴侣昵称未提供'} 共同记录` : '尚未完成情侣绑定'}</Text></View>
                </View>
                <FairyButton title="查看会员状态" onPress={() => router.push('/membership')} style={styles.memberButton} leftContent={<Ionicons name="sparkles-outline" size={18} color={colors.white} />} />
              </View>
              <View style={[styles.profileArt, compact && styles.profileArtCompact]}><FairyIllustration scene="anniversary" height={compact ? 150 : 210} /></View>
            </FairyCard>

            {bound ? <><Text style={styles.section}>情侣状态</Text><View style={styles.coupleStats}><FairyCard style={styles.coupleStat}><Text style={styles.coupleStatLabel}>恋爱天数</Text><Text style={styles.coupleStatValue}>{loveDays == null ? '未提供' : `${loveDays} 天`}</Text></FairyCard><FairyCard style={styles.coupleStat}><Text style={styles.coupleStatLabel}>伴侣昵称</Text><Text style={styles.coupleStatValue}>{partnerName || '未提供'}</Text></FairyCard><FairyCard style={styles.coupleStat}><Text style={styles.coupleStatLabel}>关系状态</Text><Text style={styles.coupleStatValue}>{relation?.status || '未提供'}</Text></FairyCard></View></> : <FairyEmptyState compact icon="people-outline" title="尚未绑定情侣关系" description="后端确认绑定后才会展示伴侣资料和情侣统计。" actionTitle="去邀请" onAction={() => router.push('/account/invite')} />}

            <Text style={styles.section}>真实数据统计</Text>
            <View style={styles.stats}><Stat label="日记" value={stats.diaryCount} icon="book-outline" /><Stat label="照片" value={stats.photoCount} icon="images-outline" /><Stat label="AI 作品" value={stats.creationCount} icon="sparkles-outline" /><Stat label="纪念日" value={stats.anniversaryCount} icon="heart-outline" /></View>

            <Text style={styles.section}>收藏与管理</Text>
            <View style={styles.menuGrid}>{menu.map((item) => <Pressable key={item[1]} onPress={() => router.push(item[3])} style={({ pressed }) => [styles.menuPressable, !compact && styles.menuPressableWide, pressed && styles.pressed]}><FairyCard style={styles.menuItem}><View style={styles.menuIcon}><Ionicons name={item[0]} size={20} color={colors.accent} /></View><View style={styles.menuText}><Text style={styles.menuTitle}>{item[1]}</Text><Text style={styles.menuDesc}>{item[2]}</Text></View><Ionicons name="chevron-forward" size={18} color={colors.textSoft} /></FairyCard></Pressable>)}</View>
            <Pressable onPress={() => setShowSignOut(true)}><FairyCard style={[styles.menuItem, styles.signOutItem]}><View style={styles.menuIcon}><Ionicons name="log-out-outline" size={20} color={colors.accent} /></View><View style={styles.menuText}><Text style={styles.menuTitle}>退出登录</Text><Text style={styles.menuDesc}>退出当前账号</Text></View></FairyCard></Pressable>
          </>
        ) : null}
      </View>
      <FairyDialog visible={showSignOut} title="要退出登录吗？" description="退出后将清除当前会话展示状态，不承诺未同步的本地内容已上传。" icon="log-out-outline" confirmText="退出登录" onCancel={() => setShowSignOut(false)} onConfirm={handleSignOut} />
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function calculateDays(value) {
  const start = new Date(`${value}T00:00:00`);
  if (Number.isNaN(start.getTime()) || start.getTime() > Date.now()) return null;
  return Math.floor((Date.now() - start.getTime()) / 86400000) + 1;
}

function Stat({ label, value, icon }) {
  return <FairyCard style={styles.stat}><View style={styles.statIcon}><Ionicons name={icon} size={18} color={colors.accent} /></View><Text style={styles.statNum}>{Number.isFinite(value) ? value : 0}</Text><Text style={styles.statLabel}>{label}</Text></FairyCard>;
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 980 }, pressed: { opacity: 0.68 }, titleBlock: { alignItems: 'center', marginBottom: spacing.xl }, eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 }, title: { color: colors.text, fontSize: 30, fontWeight: '900' }, profile: { marginBottom: 26, backgroundColor: colors.cardPink }, profileWide: { flexDirection: 'row', alignItems: 'center', gap: spacing.xxl, padding: spacing.xxl }, profileCopy: { flex: 1 }, profileArt: { width: '44%', minWidth: 280 }, profileArtCompact: { width: '100%', minWidth: 0 }, profileTop: { flexDirection: 'row', alignItems: 'center', gap: 14 }, avatar: { width: 58, height: 58, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center' }, avatarText: { color: colors.text, fontWeight: '900', fontSize: 20 }, profileText: { flex: 1 }, name: { color: colors.text, fontWeight: '900', fontSize: 18 }, desc: { color: colors.textSoft, marginTop: 4, fontSize: 12 }, memberButton: { marginTop: spacing.lg }, section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 16 }, coupleStats: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 28 }, coupleStat: { flex: 1, minWidth: 180, padding: 16 }, coupleStatLabel: { color: colors.textSoft, fontSize: 12, marginBottom: 6 }, coupleStatValue: { color: colors.text, fontSize: 16, fontWeight: '900' }, stats: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 28 }, stat: { width: '47.8%', alignItems: 'center', padding: 14 }, statIcon: { width: 38, height: 38, borderRadius: 15, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center', marginBottom: 8 }, statNum: { color: colors.text, fontSize: 24, fontWeight: '900' }, statLabel: { color: colors.textSoft, marginTop: 4, fontSize: 12 }, menuGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md, marginBottom: spacing.lg }, menuPressable: { width: '100%' }, menuPressableWide: { width: '48.5%', flexGrow: 1 }, menuItem: { flex: 1, flexDirection: 'row', alignItems: 'center', gap: 14 }, signOutItem: { backgroundColor: colors.cardPink }, menuIcon: { width: 40, height: 40, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' }, menuText: { flex: 1 }, menuTitle: { color: colors.text, fontWeight: '900', fontSize: 15 }, menuDesc: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
