import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyHeader from '../../src/components/FairyHeader';
import FairyInput from '../../src/components/FairyInput';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';

export default function TagsPage() {
  const records = useFairyStore((state) => state.records);
  const [newTagName, setNewTagName] = useState('');
  const [newTagType, setNewTagType] = useState('日记');
  const [localTags, setLocalTags] = useState([]);
  const [activeTag, setActiveTag] = useState(null);
  const [error, setError] = useState('');

  const tagStats = useMemo(() => {
    const bucket = {};
    records.forEach((record) => {
      (record.tags || []).forEach((tagName) => {
        if (!bucket[tagName]) {
          bucket[tagName] = {
            name: tagName,
            count: 0,
            types: {},
          };
        }
        bucket[tagName].count += 1;
        bucket[tagName].types[record.type] = true;
      });
    });

    localTags.forEach((item) => {
      if (!bucket[item.name]) {
        bucket[item.name] = {
          name: item.name,
          count: 0,
          types: {},
        };
      }
      bucket[item.name].types[item.relatedType] = true;
    });

    return Object.values(bucket)
      .map((item) => ({
        name: item.name,
        count: item.count,
        relatedTypes: Object.keys(item.types),
      }))
      .sort((a, b) => {
        if (b.count !== a.count) return b.count - a.count;
        return a.name.localeCompare(b.name, 'zh-Hans-CN');
      });
  }, [localTags, records]);

  const filteredRecords = useMemo(() => {
    if (!activeTag) return records;
    return records.filter((record) => (record.tags || []).includes(activeTag));
  }, [activeTag, records]);

  const addMockTag = () => {
    const name = newTagName.trim();
    if (!name) {
      setError('先给这枚标签取一个名字吧。');
      return;
    }
    if (tagStats.some((tag) => tag.name === name)) {
      setError('这枚标签已经在索引里了。');
      return;
    }

    setLocalTags((items) => [...items, { id: `local-${Date.now()}`, name, relatedType: newTagType }]);
    setNewTagName('');
    setError('');
  };

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="记录相关"
        title="标签管理"
        subtitle="把心情、地点和章节线索整理成索引，找回某一页会更快。"
        right={<FairyTag tone="gold">{tagStats.length} 枚标签</FairyTag>}
      />

      <FairyCard style={styles.editorCard}>
        <FairyInput
          label="新增标签"
          icon="pricetag-outline"
          value={newTagName}
          onChangeText={(text) => {
            setNewTagName(text);
            setError('');
          }}
          placeholder="例如：雨后散步、热可可、想念"
          error={error}
        />
        <View style={styles.typeRow}>
          {['日记', '照片', '漫画', '纪念日'].map((item) => (
            <Pressable
              key={item}
              style={[styles.typeChip, newTagType === item && styles.typeChipActive]}
              onPress={() => setNewTagType(item)}
            >
              <Text style={[styles.typeText, newTagType === item && styles.typeTextActive]}>{item}</Text>
            </Pressable>
          ))}
        </View>
        <FairyButton title="贴进索引页" onPress={addMockTag} />
      </FairyCard>

      {tagStats.length ? (
        <View style={styles.tagList}>
          {tagStats.map((tag) => (
            <Pressable key={tag.name} onPress={() => setActiveTag((prev) => (prev === tag.name ? null : tag.name))}>
              <FairyCard style={[styles.tagCard, activeTag === tag.name && styles.tagCardActive]}>
                <View style={styles.tagHead}>
                  <Text style={styles.tagName}>{tag.name}</Text>
                  <FairyTag tone={tag.count ? 'gold' : undefined}>{tag.count} 次</FairyTag>
                </View>
                <View style={styles.metaRow}>
                  <Ionicons name="library-outline" size={15} color={colors.accent} />
                  <Text style={styles.metaText}>关联类型：{tag.relatedTypes.join(' / ') || '未关联'}</Text>
                </View>
                <Text style={styles.metaHint}>{activeTag === tag.name ? '再次点击可取消筛选' : '点击筛选相关记录'}</Text>
              </FairyCard>
            </Pressable>
          ))}
        </View>
      ) : (
        <FairyEmptyState
          compact
          icon="pricetag-outline"
          title="索引页还没有标签"
          description="先写一篇日记或上传照片，再来给故事贴上第一枚标签。"
        />
      )}

      <Text style={styles.sectionTitle}>{activeTag ? `与“${activeTag}”相关的记录` : '全部记录预览'}</Text>
      {filteredRecords.length ? (
        <View style={styles.recordList}>
          {filteredRecords.slice(0, 6).map((record) => (
            <FairyCard key={record.id} style={styles.recordCard}>
              <Text style={styles.recordTitle}>{record.title}</Text>
              <View style={styles.recordMeta}>
                <FairyTag>{record.type}</FairyTag>
                <Text style={styles.recordText}>{record.date || '最近'}</Text>
              </View>
            </FairyCard>
          ))}
        </View>
      ) : (
        <FairyEmptyState
          compact
          icon="book-outline"
          title="还没有匹配到相关记录"
          description="换一个标签试试看，故事会在另一页被找到。"
        />
      )}
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  editorCard: {
    marginBottom: spacing.lg,
  },
  typeRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  typeChip: {
    borderRadius: 16,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    backgroundColor: colors.cardPink,
    borderWidth: 1,
    borderColor: colors.border,
  },
  typeChipActive: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
  typeText: {
    color: colors.textSoft,
    fontWeight: '800',
  },
  typeTextActive: {
    color: colors.white,
  },
  tagList: {
    gap: spacing.md,
  },
  tagCard: {
    padding: spacing.lg,
  },
  tagCardActive: {
    backgroundColor: '#FFF3F5',
  },
  tagHead: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.md,
  },
  tagName: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '900',
  },
  metaRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    marginTop: spacing.sm,
  },
  metaText: {
    color: colors.textSoft,
  },
  metaHint: {
    color: colors.accent,
    fontSize: 12,
    marginTop: spacing.sm,
  },
  sectionTitle: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '900',
    marginTop: spacing.xl,
    marginBottom: spacing.md,
  },
  recordList: {
    gap: spacing.sm,
  },
  recordCard: {
    padding: spacing.md,
  },
  recordTitle: {
    color: colors.text,
    fontWeight: '800',
    fontSize: 15,
  },
  recordMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginTop: spacing.sm,
  },
  recordText: {
    color: colors.textSoft,
    fontSize: 12,
  },
});
