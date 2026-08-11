import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import { signOut } from '@/api/authApi';
import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyDialog from '@/components/FairyDialog';
import FairyPage from '@/components/FairyPage';
import FairyTag from '@/components/FairyTag';
import FairySection from '@/components/FairySection';
import useFairyStore from '@/store/useFairyStore';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';

const menu = [
  ['create-outline', '草稿箱', '继续编辑还没有写完的故事', '/drafts'],
  ['calendar-outline', '纪念日管理', '重要章节都在这里', '/anniversary'],
  ['time-outline', '时光胶囊', '封存一页未来再打开', '/time-capsule/settings'],
  ['pricetag-outline', '标签管理', '整理回忆索引与筛选', '/tags'],
  ['notifications-outline', '互动通知', '查看点赞评论和提醒', '/notifications'],
  ['document-text-outline', 'PDF 导出', '把故事装订成册', '/data/pdf-export'],
  ['book-outline', '导出预览', '确认章节与样式', '/data/export-preview'],
  ['archive-outline', '数据备份', '守护你们的回忆', '/data/backup'],
  ['save-outline', '存储空间', '查看占用并清理缓存', '/data/storage'],
  ['share-social-outline', '分享预览', '生成私密分享卡片', '/share-preview'],
  ['sparkles-outline', '童话会员', '查看会员权益与方案', '/membership'],
  ['search-outline', '记录搜索', '按关键词找回故事', '/search'],
  ['help-circle-outline', '帮助反馈', '问题与建议入口', '/help-feedback'],
  ['settings-outline', '设置', '账号、通知与隐私', '/settings'],
];

const statItems = [
  ['book-outline', '日记', 'diaryCount'],
  ['images-outline', '照片', 'photoCount'],
  ['sparkles-outline', 'AI 作品', 'creationCount'],
  ['heart-outline', '纪念日', 'anniversaryCount'],
];

export default function MinePage() {
  const couple = useFairyStore((state) => state.couple);
  const diaryCount = useFairyStore((state) => state.getStats().diaryCount);
  const photoCount = useFairyStore((state) => state.getStats().photoCount);
  const creationCount = useFairyStore((state) => state.getStats().creationCount);
  const anniversaryCount = useFairyStore((state) => state.getStats().anniversaryCount);
  const stats = { diaryCount, photoCount, creationCount, anniversaryCount };
  const [showSignOut, setShowSignOut] = useState(false);

  const handleSignOut = async () => {
    setShowSignOut(false);
    const result = await signOut();
    if (result.success) router.replace('/login');
  };

  return (
    <FairyPage tabSafe topSpace={28} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <View style={styles.titleBlock}><Text style={styles.eyebrow}>把边角功能也做成温柔的小信箱</Text><Text style={styles.title}>我的童话</Text></View>

        <FairyCard style={styles.profile} contentStyle={styles.profileContent}>
          <View style={styles.profileTop}>
            <View style={styles.avatar}><Text style={styles.avatarText}>{couple.userName?.slice(0, 1) || '我'}</Text></View>
            <View style={styles.profileText}>
              <Text style={styles.name}>{couple.userName}</Text>
              <Text style={styles.desc}>正在和 {couple.partnerName} 书写第 {couple.loveDays} 天的童话</Text>
            </View>
            <Pressable accessibilityRole="button" onPress={() => router.push('/membership')}><FairyTag tone="gold">童话会员</FairyTag></Pressable>
          </View>
          <FairyButton title="查看会员权益" onPress={() => router.push('/membership')} style={styles.memberButton} leftContent={<Ionicons name="sparkles-outline" size={18} color={colors.white} />} />
        </FairyCard>

        <FairySection title="情侣统计">
          <View style={styles.coupleStats}>
            <FairyCard style={styles.coupleStat}><Text style={styles.coupleStatLabel}>恋爱天数</Text><Text style={styles.coupleStatValue}>{couple.loveDays} 天</Text></FairyCard>
            <FairyCard style={styles.coupleStat}><Text style={styles.coupleStatLabel}>双人空间</Text><Text style={styles.coupleStatValue} numberOfLines={1}>{couple.spaceName}</Text></FairyCard>
            <FairyCard style={styles.coupleStat}><Text style={styles.coupleStatLabel}>今日状态</Text><Text style={styles.coupleStatValue} numberOfLines={1}>{couple.statusText}</Text></FairyCard>
          </View>
        </FairySection>

        <FairySection title="我的统计">
          <View style={styles.stats}>
            {statItems.map(([icon, label, key]) => (
              <FairyCard key={key} style={styles.stat} padding={spacing.md}>
                <View style={styles.statIcon}><Ionicons name={icon} size={18} color={colors.accent} /></View>
                <Text style={styles.statNum}>{stats[key]}</Text>
                <Text style={styles.statLabel}>{label}</Text>
              </FairyCard>
            ))}
          </View>
        </FairySection>

        <FairySection title="收藏与管理">
          <View style={styles.menuGrid}>
            {menu.map((item) => (
              <Pressable key={item[1]} onPress={() => router.push(item[3])} style={({ pressed }) => [styles.menuPressable, pressed && styles.pressed]}>
                <FairyCard style={styles.menuItem} padding={spacing.md}>
                  <View style={styles.menuIcon}><Ionicons name={item[0]} size={20} color={colors.accent} /></View>
                  <View style={styles.menuText}><Text style={styles.menuTitle}>{item[1]}</Text><Text style={styles.menuDesc} numberOfLines={2}>{item[2]}</Text></View>
                  <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
                </FairyCard>
              </Pressable>
            ))}
          </View>
        </FairySection>

        <Pressable onPress={() => setShowSignOut(true)} style={({ pressed }) => pressed && styles.pressed}>
          <FairyCard style={[styles.menuItem, styles.signOutItem]} padding={spacing.md}>
            <View style={styles.menuIcon}><Ionicons name="log-out-outline" size={20} color={colors.accent} /></View>
            <View style={styles.menuText}><Text style={styles.menuTitle}>退出登录</Text><Text style={styles.menuDesc}>回到登录页，稍后再继续写童话</Text></View>
            <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
          </FairyCard>
        </Pressable>
      </View>
      <FairyDialog visible={showSignOut} title="要退出登录吗？" description="本地保存的童话数据不会因此清除，下次登录还能继续书写。" icon="log-out-outline" confirmText="退出登录" onCancel={() => setShowSignOut(false)} onConfirm={handleSignOut} />
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
  profile: { marginBottom: 26, backgroundColor: colors.cardPink },
  profileContent: { minHeight: 150 },
  profileTop: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  avatar: { width: 58, height: 58, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  avatarText: { color: colors.text, fontWeight: '900', fontSize: 20 },
  profileText: { flex: 1, minWidth: 0 },
  name: { color: colors.text, fontWeight: '900', fontSize: 18 },
  desc: { color: colors.textSoft, marginTop: 4, fontSize: 12, lineHeight: 18 },
  memberButton: { marginTop: spacing.lg },
  coupleStats: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  coupleStat: { flex: 1, minWidth: 180, padding: 16 },
  coupleStatLabel: { color: colors.textSoft, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  coupleStatValue: { color: colors.text, fontSize: 16, fontWeight: '900' },
  stats: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  stat: { width: '47.8%', flexGrow: 1, minWidth: 130, alignItems: 'center' },
  statIcon: { width: 38, height: 38, borderRadius: 15, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center', marginBottom: 8 },
  statNum: { color: colors.text, fontSize: 24, fontWeight: '900' },
  statLabel: { color: colors.textSoft, marginTop: 4, fontSize: 12, fontWeight: '800' },
  menuGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md },
  menuPressable: { width: '47.8%', flexGrow: 1, minWidth: 260 },
  menuItem: { flex: 1, flexDirection: 'row', alignItems: 'center', gap: 14 },
  signOutItem: { marginTop: spacing.lg, backgroundColor: colors.cardPink },
  menuIcon: { width: 40, height: 40, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  menuText: { flex: 1, minWidth: 0 },
  menuTitle: { color: colors.text, fontWeight: '900', fontSize: 15 },
  menuDesc: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
