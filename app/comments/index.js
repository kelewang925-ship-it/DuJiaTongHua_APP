import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyInput from '@/components/FairyInput';
import FairyPage from '@/components/FairyPage';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';

const initialComments = [
  { id: 'comment-001', author: '小满', time: '今天 21:38', content: '这天的风真的很温柔。', replies: [{ id: 'reply-001', author: '阿舟', time: '今天 21:40', content: '下次还要走这条路 ✨' }] },
  { id: 'comment-002', author: '阿舟', time: '今天 21:42', content: '已经收藏进故事书啦。', replies: [{ id: 'reply-002', author: '小满', time: '今天 21:44', content: '耶耶！这页很重要。' }] },
  { id: 'comment-003', author: '小满', time: '今天 21:45', content: '希望每个傍晚我们都能这样散步。', replies: [] },
];

export default function CommentsPage() {
  const [comments, setComments] = useState(initialComments);
  const [content, setContent] = useState('');
  const [replyTo, setReplyTo] = useState(null);
  const [likedIds, setLikedIds] = useState([]);
  const [toast, setToast] = useState(null);

  const handleSend = () => {
    const text = content.trim();
    if (!text) {
      setToast({ tone: 'info', message: '先写下一句悄悄话吧。' });
      return;
    }
    if (replyTo) {
      setComments((current) => current.map((item) => item.id === replyTo.id ? { ...item, replies: [...item.replies, { id: `reply-${Date.now()}`, author: '我', time: '刚刚', content: text }] } : item));
    } else {
      setComments((current) => [{ id: `comment-${Date.now()}`, author: '我', time: '刚刚', content: text, replies: [] }, ...current]);
    }
    setContent('');
    setReplyTo(null);
    setToast({ tone: 'success', message: replyTo ? '回复已经贴到这页回忆里。' : '评论已经轻轻落在纸页上。' });
  };

  const toggleLike = (id) => setLikedIds((ids) => ids.includes(id) ? ids.filter((item) => item !== id) : [...ids, id]);

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="评论" right={<Pressable accessibilityRole="button" onPress={() => setToast({ tone: 'info', message: '更多评论管理功能会在后续业务阶段接入。' })} style={({ pressed }) => [styles.headerAction, pressed && styles.pressed]}><Ionicons name="ellipsis-horizontal" size={23} color={colors.text} /></Pressable>} />}
      topSpace={28}
      bottomSpace={60}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
      keyboardShouldPersistTaps="handled"
      keyboardDismissMode="on-drag"
      automaticallyAdjustKeyboardInsets
    >
      <View style={styles.content}>
        <FairyCard style={styles.memoryCard} padding={spacing.md}>
          <View style={styles.memoryImage}><FairyImage name="homeCover" height={132} radius={18} framed={false} resizeMode="cover" /></View>
          <View style={styles.memoryCopy}>
            <Text style={styles.memoryTitle}>晚霞散步</Text>
            <Text style={styles.memoryMeta}>2026.06.09 · 日记</Text>
            <View style={styles.memoryDivider} />
            <Text numberOfLines={3} style={styles.memoryText}>我们踩着还没干透的小路慢慢走，路灯把影子拉得很长。</Text>
          </View>
        </FairyCard>

        <View style={styles.sectionRow}><Text style={styles.sectionTitle}>全部评论</Text><Text style={styles.count}>{comments.length} 条</Text></View>
        {comments.length ? (
          <View style={styles.list}>
            {comments.map((item) => {
              const liked = likedIds.includes(item.id);
              return (
                <FairyCard key={item.id} style={styles.commentCard} padding={spacing.lg}>
                  <View style={styles.commentTop}>
                    <View style={styles.avatar}><Text style={styles.avatarText}>{item.author.slice(0, 1)}</Text></View>
                    <View style={styles.authorCopy}><Text style={styles.author}>{item.author}</Text><Text style={styles.time}>{item.time}</Text></View>
                    <Ionicons name="star-outline" size={18} color={colors.gold} />
                  </View>
                  <View style={styles.bubble}><Text style={styles.commentText}>{item.content}</Text></View>
                  <View style={styles.actionRow}>
                    <Pressable onPress={() => setReplyTo(item)} style={({ pressed }) => [styles.smallAction, pressed && styles.pressed]}><Ionicons name="chatbubble-outline" size={16} color={colors.text} /><Text style={styles.smallActionText}>回复</Text></Pressable>
                    <Pressable onPress={() => toggleLike(item.id)} style={({ pressed }) => [styles.smallAction, pressed && styles.pressed]}><Ionicons name={liked ? 'heart' : 'heart-outline'} size={17} color={liked ? colors.primaryDeep : colors.text} /><Text style={[styles.smallActionText, liked && styles.likedText]}>{liked ? '已喜欢' : '喜欢'}</Text></Pressable>
                  </View>
                  {item.replies.length ? <View style={styles.replies}>{item.replies.map((reply) => <View key={reply.id} style={styles.replyRow}><View style={styles.replyAvatar}><Text style={styles.replyAvatarText}>{reply.author.slice(0, 1)}</Text></View><View style={styles.replyCopy}><View style={styles.replyMeta}><Text style={styles.replyAuthor}>{reply.author}</Text><Text style={styles.replyTime}>{reply.time}</Text></View><Text style={styles.replyText}>{reply.content}</Text></View></View>)}</View> : null}
                </FairyCard>
              );
            })}
          </View>
        ) : <FairyEmptyState compact icon="chatbubble-outline" title="还没有留言" description="写下第一句回应，让这段回忆有两个人的声音。" />}

        <View style={styles.privateNote}><Ionicons name="lock-closed-outline" size={14} color={colors.gold} /><Text style={styles.privateText}>只有我们能看到的悄悄话</Text></View>
        <FairyCard style={styles.editorCard} padding={spacing.lg}>
          {replyTo ? <View style={styles.replying}><Text style={styles.replyingText}>正在回复 {replyTo.author}</Text><Pressable onPress={() => setReplyTo(null)}><Ionicons name="close" size={19} color={colors.textSoft} /></Pressable></View> : null}
          <FairyInput value={content} onChangeText={setContent} multiline placeholder={replyTo ? `回复 ${replyTo.author}……` : '写一句悄悄话……'} maxLength={180} helper={`${content.length}/180`} containerStyle={styles.inputWrap} />
          <FairyButton title={replyTo ? '发送回复' : '发送评论'} onPress={handleSend} leftContent={<Ionicons name="paper-plane-outline" size={18} color={colors.white} />} />
        </FairyCard>
      </View>
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 760 },
  headerAction: { width: 44, height: 44, alignItems: 'center', justifyContent: 'center' }, pressed: { opacity: 0.65 },
  memoryCard: { marginBottom: spacing.xl, flexDirection: 'row', gap: spacing.lg }, memoryImage: { width: 148 }, memoryCopy: { flex: 1, paddingVertical: spacing.sm },
  memoryTitle: { color: colors.text, fontSize: 20, fontWeight: '900' }, memoryMeta: { color: colors.textSoft, fontSize: 12, marginTop: spacing.xs }, memoryDivider: { height: 1, backgroundColor: colors.border, marginVertical: spacing.md }, memoryText: { color: colors.text, lineHeight: 21 },
  sectionRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: spacing.md }, sectionTitle: { color: colors.text, fontSize: 20, fontWeight: '900' }, count: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  list: { gap: spacing.md }, commentCard: { backgroundColor: 'rgba(255,249,244,0.95)' }, commentTop: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  avatar: { width: 48, height: 48, borderRadius: 20, backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' }, avatarText: { color: colors.primaryDeep, fontSize: 18, fontWeight: '900' }, authorCopy: { flex: 1 }, author: { color: colors.text, fontSize: 15, fontWeight: '900' }, time: { color: colors.textSoft, fontSize: 11, marginTop: 3 },
  bubble: { marginTop: spacing.md, padding: spacing.md, borderRadius: 18, backgroundColor: colors.background, borderWidth: 1, borderColor: colors.border }, commentText: { color: colors.text, lineHeight: 22 },
  actionRow: { flexDirection: 'row', gap: spacing.lg, marginTop: spacing.md }, smallAction: { minHeight: 34, flexDirection: 'row', alignItems: 'center', gap: 5, paddingHorizontal: spacing.sm }, smallActionText: { color: colors.text, fontSize: 12, fontWeight: '800' }, likedText: { color: colors.primaryDeep },
  replies: { marginTop: spacing.md, padding: spacing.md, borderRadius: 18, backgroundColor: colors.cardPink }, replyRow: { flexDirection: 'row', gap: spacing.sm }, replyAvatar: { width: 34, height: 34, borderRadius: 14, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card }, replyAvatarText: { color: colors.accent, fontSize: 12, fontWeight: '900' }, replyCopy: { flex: 1 }, replyMeta: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm }, replyAuthor: { color: colors.text, fontSize: 12, fontWeight: '900' }, replyTime: { color: colors.textSoft, fontSize: 10 }, replyText: { color: colors.text, lineHeight: 19, marginTop: 3 },
  privateNote: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, marginVertical: spacing.xl }, privateText: { color: colors.textSoft, fontSize: 12 },
  editorCard: { backgroundColor: colors.cardPink }, replying: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: spacing.sm }, replyingText: { color: colors.primaryDeep, fontSize: 12, fontWeight: '900' }, inputWrap: { marginBottom: spacing.md },
});
