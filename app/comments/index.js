import { useState } from 'react';
import { View, Text, StyleSheet, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import FairyPage from '../../src/components/FairyPage';
import FairyHeader from '../../src/components/FairyHeader';
import FairyCard from '../../src/components/FairyCard';
import FairyInput from '../../src/components/FairyInput';
import FairyButton from '../../src/components/FairyButton';
import FairyEmptyState from '../../src/components/FairyEmptyState';

const initialComments = [
  {
    id: 'comment-001',
    author: '小童话',
    time: '刚刚',
    content: '这一章我也很喜欢，像偷偷夹在书里的花瓣。',
  },
  {
    id: 'comment-002',
    author: '王可乐',
    time: '今天 21:18',
    content: '下次我们可以把这一天也生成成漫画。',
  },
];

export default function CommentsPage() {
  const [comments, setComments] = useState(initialComments);
  const [content, setContent] = useState('');

  const handleSend = () => {
    const text = content.trim();
    if (!text) return;
    setComments((current) => [
      {
        id: `comment-${Date.now()}`,
        author: '我',
        time: '刚刚',
        content: text,
      },
      ...current,
    ]);
    setContent('');
  };

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="情侣互动"
        title="评论列表"
        subtitle="两个人围绕某一段回忆留下的小回应。"
      />

      <FairyCard style={styles.editorCard}>
        <FairyInput
          label="写一条温柔留言"
          icon="chatbubble-ellipses-outline"
          value={content}
          onChangeText={setContent}
          multiline
          placeholder="例如：这一刻我也记得。"
          containerStyle={styles.inputWrap}
        />
        <FairyButton title="发送评论" onPress={handleSend} />
      </FairyCard>

      <View style={styles.sectionRow}>
        <Text style={styles.section}>全部评论</Text>
        <Text style={styles.count}>{comments.length} 条</Text>
      </View>

      {comments.length === 0 ? (
        <FairyEmptyState
          compact
          icon="chatbubble-outline"
          title="还没有留言"
          description="写下第一句回应，让这段回忆有两个人的声音。"
        />
      ) : (
        <View style={styles.list}>
          {comments.map((item, index) => (
            <FairyCard key={item.id} style={[styles.commentCard, index === 0 && styles.firstCard]}>
              <View style={styles.avatar}>
                <Text style={styles.avatarText}>{item.author.slice(0, 1)}</Text>
              </View>
              <View style={{ flex: 1 }}>
                <View style={styles.nameRow}>
                  <Text style={styles.author}>{item.author}</Text>
                  <Text style={styles.time}>{item.time}</Text>
                </View>
                <Text style={styles.commentText}>{item.content}</Text>
                <View style={styles.actionRow}>
                  <Pressable style={styles.smallAction}>
                    <Ionicons name="heart-outline" size={13} color={colors.primaryDeep} />
                    <Text style={styles.smallActionText}>喜欢</Text>
                  </Pressable>
                  <Pressable style={styles.smallAction}>
                    <Ionicons name="return-up-forward-outline" size={13} color={colors.accent} />
                    <Text style={styles.smallActionText}>回复</Text>
                  </Pressable>
                </View>
              </View>
            </FairyCard>
          ))}
        </View>
      )}
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  editorCard: { marginBottom: spacing.xl, backgroundColor: colors.cardPink },
  inputWrap: { marginBottom: spacing.md },
  sectionRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: spacing.md },
  section: { color: colors.text, fontSize: 20, fontWeight: '900' },
  count: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  list: { gap: spacing.md },
  commentCard: { flexDirection: 'row', gap: spacing.md, padding: spacing.md },
  firstCard: { backgroundColor: '#FFF7EF' },
  avatar: { width: 42, height: 42, borderRadius: 17, backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' },
  avatarText: { color: colors.text, fontWeight: '900' },
  nameRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm },
  author: { color: colors.text, fontSize: 15, fontWeight: '900' },
  time: { color: colors.textSoft, fontSize: 11 },
  commentText: { color: colors.text, fontSize: 14, lineHeight: 22, marginTop: spacing.sm },
  actionRow: { flexDirection: 'row', gap: spacing.sm, marginTop: spacing.md },
  smallAction: { flexDirection: 'row', alignItems: 'center', gap: 4, paddingHorizontal: spacing.sm, paddingVertical: 5, borderRadius: 14, backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.border },
  smallActionText: { color: colors.textSoft, fontSize: 11, fontWeight: '800' },
});
