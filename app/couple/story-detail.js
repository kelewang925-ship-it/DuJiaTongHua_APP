import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';
import { getApiMode } from '../../src/api/client';

export default function CoupleStoryDetailPage() {
  const timeline = useFairyStore((state) => state.timeline);
  const first = timeline[0];
  const [liked, setLiked] = useState(false);
  const [toast, setToast] = useState(null);

  const toggleLike = () => {
    if (getApiMode() === 'real') {
      setToast({ message: 'Real 模式暂未接入动态喜欢写入，不会模拟成功。', tone: 'info' });
      return;
    }
    setLiked((value) => !value);
  };

  return (
    <FairyPage
      header={<FairyHeader showBack eyebrow="互动相关" title="情侣动态详情" subtitle="把这一天当作故事章节来阅读，而不是信息流。" />}
    >
      <FairyCard style={styles.card}>
        <Text style={styles.title}>{first?.title || '第 428 天的小故事'}</Text>
        <Text style={styles.time}>{first?.time || '刚刚'}</Text>
        <Text style={styles.desc}>{first?.description || '今天的动态会在这里展示详情。'}</Text>
        <View style={styles.meta}>
          <FairyTag tone="gold">{first?.tag || '日常'}</FairyTag>
          <Pressable onPress={toggleLike}>
            <FairyTag>{liked ? '已喜欢' : '喜欢'}</FairyTag>
          </Pressable>
        </View>
      </FairyCard>

      <View style={styles.actions}>
        <FairyButton title="查看评论" onPress={() => router.push('/comments')} />
        <FairyButton title="回到情侣空间" variant="secondary" onPress={() => router.push('/(tabs)/couple')} />
      </View>
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  card: { marginBottom: spacing.xl },
  title: { color: colors.text, fontSize: 20, fontWeight: '900' },
  time: { color: colors.textSoft, marginTop: 6, fontSize: 12 },
  desc: { color: colors.textSoft, marginTop: spacing.md, lineHeight: 22 },
  meta: { flexDirection: 'row', gap: spacing.sm, marginTop: spacing.md },
  actions: { gap: spacing.md },
});
