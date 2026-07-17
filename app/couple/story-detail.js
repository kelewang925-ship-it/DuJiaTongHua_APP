import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyHeader from '../../src/components/FairyHeader';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';
import { getApiMode } from '../../src/api/client';

export default function CoupleStoryDetailPage() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const storyId = Array.isArray(params.id) ? params.id[0] : params.id;
  const timeline = useFairyStore((state) => state.timeline);
  const story = useMemo(() => storyId ? timeline.find((item) => item.id === storyId) : null, [storyId, timeline]);
  const [liked, setLiked] = useState(false);
  const [toast, setToast] = useState(null);

  const toggleLike = () => {
    if (getApiMode() === 'real') {
      setToast({ message: 'Real 模式暂未接入动态喜欢写入，不会模拟成功。', tone: 'info' });
      return;
    }
    setLiked((value) => !value);
  };

  const commentTarget = story?.recordId ? { id: story.recordId, type: story.tag === '照片' ? 'photo' : 'diary' } : null;

  return (
    <FairyPage header={<FairyHeader showBack eyebrow="互动相关" title={story ? '情侣动态详情' : '动态不存在'} subtitle={story ? '按真实记录读取这一页内容。' : storyId ? '这条动态可能已被删除或无权访问。' : '缺少动态 ID，无法确定要展示的记录。'} />}>
      {story ? (
        <>
          <FairyCard style={styles.card}>
            <Text style={styles.title}>{story.title || '未提供标题'}</Text>
            {story.time ? <Text style={styles.time}>{story.time}</Text> : <Text style={styles.time}>未提供时间</Text>}
            <Text style={styles.desc}>{story.description || '未提供文字内容'}</Text>
            <View style={styles.meta}>
              {story.tag ? <FairyTag tone="gold">{story.tag}</FairyTag> : null}
              <Pressable onPress={toggleLike}><FairyTag>{liked ? '已喜欢' : '喜欢'}</FairyTag></Pressable>
            </View>
          </FairyCard>
          <View style={styles.actions}>
            <FairyButton title={commentTarget ? '查看评论' : '评论目标不可用'} disabled={!commentTarget} onPress={() => commentTarget && router.push({ pathname: '/comments', params: commentTarget })} />
            <FairyButton title="回到情侣空间" variant="secondary" onPress={() => router.replace('/(tabs)/couple')} />
          </View>
        </>
      ) : (
        <FairyEmptyState imageName="emptyDiary" title={storyId ? '没有找到这条动态' : '缺少动态参数'} description={storyId ? '它可能已经被删除，或当前账号无权访问。' : '请从情侣空间中的真实故事线进入详情。'} actionTitle="返回情侣空间" onAction={() => router.replace('/(tabs)/couple')} />
      )}
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  card: { marginBottom: spacing.xl }, title: { color: colors.text, fontSize: 20, fontWeight: '900' }, time: { color: colors.textSoft, marginTop: 6, fontSize: 12 }, desc: { color: colors.textSoft, marginTop: spacing.md, lineHeight: 22 }, meta: { flexDirection: 'row', gap: spacing.sm, marginTop: spacing.md }, actions: { gap: spacing.md },
});