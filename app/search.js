import { useMemo, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import FairyCard from '../src/components/FairyCard';
import FairyEmptyState from '../src/components/FairyEmptyState';
import FairyHeader from '../src/components/FairyHeader';
import FairyInput from '../src/components/FairyInput';
import FairyPage from '../src/components/FairyPage';
import FairyTag from '../src/components/FairyTag';
import colors from '../src/theme/colors';
import spacing from '../src/theme/spacing';
import useFairyStore from '../src/store/useFairyStore';

export default function SearchPage() {
  const records = useFairyStore((state) => state.records);
  const [keyword, setKeyword] = useState('');

  const result = useMemo(() => {
    const key = keyword.trim();
    if (!key) return [];
    return records.filter((item) => {
      const text = `${item.title || ''} ${item.content || ''} ${(item.tags || []).join(' ')}`;
      return text.includes(key);
    });
  }, [keyword, records]);

  return (
    <FairyPage>
      <FairyHeader showBack eyebrow="特殊页面" title="记录搜索" subtitle="按关键词找回某一页故事。" />

      <FairyCard style={styles.searchCard}>
        <FairyInput
          label="关键词"
          icon="search-outline"
          value={keyword}
          onChangeText={setKeyword}
          placeholder="例如：海边、热可可、第一次旅行"
          containerStyle={styles.inputWrap}
        />
      </FairyCard>

      {!keyword.trim() ? (
        <FairyEmptyState imageName="emptySearch" title="输入关键词开始查找" description="会匹配日记标题、正文和标签。" />
      ) : result.length ? (
        <View style={styles.list}>
          {result.map((item) => (
            <FairyCard key={item.id} style={styles.item}>
              <Text style={styles.title}>{item.title}</Text>
              <Text style={styles.content}>{item.content}</Text>
              <View style={styles.meta}>
                <FairyTag tone="gold">{item.type}</FairyTag>
                <Text style={styles.time}>{item.date}</Text>
              </View>
            </FairyCard>
          ))}
        </View>
      ) : (
        <FairyEmptyState imageName="emptySearch" title="没有找到相关内容" description="换个词试试看，故事可能藏在别的章节里。" />
      )}
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  searchCard: { marginBottom: spacing.lg },
  inputWrap: { marginBottom: 0 },
  list: { gap: spacing.md },
  item: { padding: spacing.lg },
  title: { color: colors.text, fontSize: 16, fontWeight: '900' },
  content: { color: colors.textSoft, marginTop: spacing.sm, lineHeight: 21 },
  meta: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginTop: spacing.md },
  time: { color: colors.textSoft, fontSize: 12 },
});
