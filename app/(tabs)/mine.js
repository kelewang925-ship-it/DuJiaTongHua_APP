import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyIllustration from '../../src/components/FairyIllustration';
import FairyTag from '../../src/components/FairyTag';
import useFairyStore from '../../src/store/useFairyStore';

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

  const coupleStats = [
    ['恋爱天数', `${couple.loveDays} 天`],
    ['双人空间', couple.spaceName],
    ['今日状态', couple.statusText],
  ];

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <Text style={styles.eyebrow}>私人收藏册</Text>
      <Text style={styles.title}>我的</Text>

      <FairyCard style={styles.profile}>
        <View style={styles.profileTop}>
          <View style={styles.avatar}><Text style={styles.avatarText}>{couple.userName?.slice(0, 1) || '我'}</Text></View>
          <View style={styles.profileText}>
            <Text style={styles.name}>{couple.userName}</Text>
            <Text style={styles.desc}>正在和 {couple.partnerName} 书写第 {couple.loveDays} 天的童话</Text>
          </View>
          <FairyTag tone="gold">童话会员</FairyTag>
        </View>
        <FairyIllustration scene="anniversary" height={132} />
      </FairyCard>

      <Text style={styles.section}>情侣统计</Text>
      <View style={styles.coupleStats}>
        {coupleStats.map(([label, value]) => (
          <FairyCard key={label} style={styles.coupleStat}>
            <Text style={styles.coupleStatLabel}>{label}</Text>
            <Text style={styles.coupleStatValue}>{value}</Text>
          </FairyCard>
        ))}
      </View>

      <Text style={styles.section}>我的统计</Text>
      <View style={styles.stats}>
        {statItems.map(([icon, label, key]) => (
          <FairyCard key={key} style={styles.stat}>
            <View style={styles.statIcon}>
              <Ionicons name={icon} size={18} color={colors.accent} />
            </View>
            <Text style={styles.statNum}>{stats[key]}</Text>
            <Text style={styles.statLabel}>{label}</Text>
          </FairyCard>
        ))}
      </View>

      <Text style={styles.section}>收藏与管理</Text>
      {menu.map((item) => (
        <Pressable key={item[1]} onPress={() => router.push(item[3])}>
          <FairyCard style={styles.menuItem}>
            <View style={styles.menuIcon}><Ionicons name={item[0]} size={20} color={colors.accent} /></View>
            <View style={styles.menuText}>
              <Text style={styles.menuTitle}>{item[1]}</Text>
              <Text style={styles.menuDesc}>{item[2]}</Text>
            </View>
            <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
          </FairyCard>
        </Pressable>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 64, paddingBottom: 110 },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900', marginBottom: 24 },
  profile: { marginBottom: 26, backgroundColor: colors.cardPink },
  profileTop: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 8 },
  avatar: { width: 58, height: 58, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  avatarText: { color: colors.text, fontWeight: '900', fontSize: 20 },
  profileText: { flex: 1 },
  name: { color: colors.text, fontWeight: '900', fontSize: 18 },
  desc: { color: colors.textSoft, marginTop: 4, fontSize: 12, lineHeight: 18 },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 16 },
  coupleStats: { gap: 12, marginBottom: 28 },
  coupleStat: { padding: 16 },
  coupleStatLabel: { color: colors.textSoft, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  coupleStatValue: { color: colors.text, fontSize: 16, fontWeight: '900' },
  stats: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 28 },
  stat: { width: '47.8%', alignItems: 'center', padding: 14 },
  statIcon: { width: 38, height: 38, borderRadius: 15, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center', marginBottom: 8 },
  statNum: { color: colors.text, fontSize: 24, fontWeight: '900' },
  statLabel: { color: colors.textSoft, marginTop: 4, fontSize: 12, fontWeight: '800' },
  menuItem: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14 },
  menuIcon: { width: 40, height: 40, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  menuText: { flex: 1 },
  menuTitle: { color: colors.text, fontWeight: '900', fontSize: 15 },
  menuDesc: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
