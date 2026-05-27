import { useEffect, useMemo, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyInput from '../../src/components/FairyInput';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';

const templateMap = {
  firstMeet: {
    title: '第一次见面纪念日',
    note: '那天的天气、表情和第一句话都很值得写下。',
  },
  travel: {
    title: '第一次旅行纪念日',
    note: '把路线、照片和那顿饭的味道都留在这一页。',
  },
  birthday: {
    title: '生日纪念章节',
    note: '写下你准备的小惊喜和那天的愿望。',
  },
};

export default function AnniversaryEditPage() {
  const router = useRouter();
  const { id, template } = useLocalSearchParams();
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const addAnniversary = useFairyStore((state) => state.addAnniversary);

  const target = useMemo(() => anniversaries.find((item) => item.id === id), [anniversaries, id]);
  const templatePreset = useMemo(() => (template ? templateMap[template] : null), [template]);
  const isEditMode = Boolean(target);

  const [title, setTitle] = useState('');
  const [date, setDate] = useState('');
  const [note, setNote] = useState('');
  const [error, setError] = useState('');
  const [toast, setToast] = useState({ visible: false, message: '', tone: 'success' });

  useEffect(() => {
    if (target) {
      setTitle(target.title || '');
      setDate(target.date || '');
      setNote(target.note || '');
      return;
    }
    if (templatePreset) {
      setTitle(templatePreset.title);
      setNote(templatePreset.note);
    }
  }, [target, templatePreset]);

  const save = () => {
    if (!title.trim()) {
      setError('请写下这一章的标题。');
      return;
    }
    if (!date.trim()) {
      setError('请补充纪念日日期。');
      return;
    }

    if (isEditMode) {
      setToast({
        visible: true,
        message: '已完成 mock 编辑预览。后续接入 update 接口后会真正保存修改。',
        tone: 'info',
      });
      return;
    }

    addAnniversary({
      title: title.trim(),
      date: date.trim(),
      note: note.trim(),
    });

    setToast({ visible: true, message: '新的纪念章节已经写进故事册。', tone: 'success' });
    setTimeout(() => router.push('/anniversary'), 500);
  };

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="纪念日相关"
        title={isEditMode ? '编辑纪念章节' : '新增纪念章节'}
        subtitle="把一个重要日子写成童话章节，未来每次翻到都会心软。"
        right={<FairyTag tone="gold">{isEditMode ? '编辑中' : '新建'}</FairyTag>}
      />

      <FairyCard style={styles.tipCard}>
        <Text style={styles.tipTitle}>这一页会出现在纪念日时间线</Text>
        <Text style={styles.tipText}>建议标题用故事语气，比如“第一次一起看海”，会比普通事件名更有收藏感。</Text>
      </FairyCard>

      <FairyCard style={styles.formCard}>
        <FairyInput
          label="章节标题"
          icon="book-outline"
          value={title}
          onChangeText={(text) => {
            setTitle(text);
            setError('');
          }}
          placeholder="例如：第一次一起看海"
        />
        <FairyInput
          label="纪念日日期"
          icon="calendar-outline"
          value={date}
          onChangeText={(text) => {
            setDate(text);
            setError('');
          }}
          placeholder="YYYY-MM-DD"
        />
        <FairyInput
          label="章节备注"
          icon="create-outline"
          value={note}
          onChangeText={(text) => {
            setNote(text);
            setError('');
          }}
          placeholder="写一句只属于这一天的注释"
          multiline
          error={error}
        />
        <View style={styles.actions}>
          <FairyButton title={isEditMode ? '保存编辑（mock）' : '保存纪念日'} onPress={save} />
          <FairyButton title="去选记录模板" variant="secondary" onPress={() => router.push('/anniversary/template')} />
        </View>
      </FairyCard>

      <FairyToast
        visible={toast.visible}
        tone={toast.tone}
        message={toast.message}
        onHide={() => setToast((value) => ({ ...value, visible: false }))}
      />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  tipCard: {
    backgroundColor: colors.cardPink,
    marginBottom: spacing.lg,
  },
  tipTitle: {
    color: colors.text,
    fontSize: 17,
    fontWeight: '900',
  },
  tipText: {
    color: colors.textSoft,
    lineHeight: 21,
    marginTop: spacing.sm,
  },
  formCard: {
    marginBottom: spacing.lg,
  },
  actions: {
    gap: spacing.md,
  },
});
