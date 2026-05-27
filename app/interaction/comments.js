import { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyInput from '../../src/components/FairyInput';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';

const seed = [
  { id: 'c1', user: '林小满', text: '今天的晚风真的很好闻。', time: '刚刚' },
  { id: 'c2', user: '陆星河', text: '下次还走这条路。', time: '18 分钟前' },
];

export default function CommentsPage() {
  const [list, setList] = useState(seed);
  const [text, setText] = useState('');

  const send = () => {
    const value = text.trim();
    if (!value) return;
    setList((items) => [{ id: `c-${Date.now()}`, user: '我', text: value, time: '刚刚' }, ...items]);
    setText('');
  };

  return (
    <FairyPage>
      <FairyHeader showBack eyebrow="互动相关" title="评论列表" subtitle="所有温柔回应，都收在这一页。" right={<FairyTag>{list.length} 条</FairyTag>} />

      <FairyCard style={styles.editor}>
        <FairyInput
          label="写一句回应"
          icon="chatbubble-ellipses-outline"
          value={text}
          onChangeText={setText}
          placeholder="用一句短短的话接住这段回忆"
          multiline
          containerStyle={styles.inputWrap}
        />
        <FairyButton title="发送评论" onPress={send} />
      </FairyCard>

      <View style={styles.list}>
        {list.map((item) => (
          <FairyCard key={item.id} style={styles.item}>
            <Text style={styles.user}>{item.user}</Text>
            <Text style={styles.content}>{item.text}</Text>
            <Text style={styles.time}>{item.time}</Text>
          </FairyCard>
        ))}
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  editor: { marginBottom: spacing.lg },
  inputWrap: { marginBottom: spacing.md },
  list: { gap: spacing.md },
  item: { padding: spacing.lg },
  user: { color: colors.text, fontWeight: '900' },
  content: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.xs },
  time: { color: colors.textSoft, marginTop: spacing.sm, fontSize: 12 },
});
