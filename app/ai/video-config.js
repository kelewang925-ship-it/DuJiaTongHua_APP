import { useState } from 'react';
import { Pressable, StyleSheet, Switch, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyInput from '../../src/components/FairyInput';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';
import { getApiMode } from '../../src/api/client';
import { hasCapability } from '../../src/config/capabilities';

const sourceOptions = ['照片', '日记', 'AI 漫画'];
const styleOptions = ['绘本影片', '慢慢回忆', '纪念日'];
const durationOptions = ['15 秒', '30 秒', '60 秒'];
const musicOptions = ['钢琴轻语', '午后风铃', '星光慢歌'];
const mockDraft = {
  title: '春天散步纪念视频',
  source: sourceOptions[0],
  styleName: styleOptions[0],
  duration: durationOptions[1],
  music: musicOptions[0],
};

export default function VideoConfigPage() {
  const addCreation = useFairyStore((state) => state.addCreation);
  const mode = getApiMode();
  const isMockMode = mode === 'mock';
  const canGenerate = hasCapability('aiGeneration', mode);
  const [title, setTitle] = useState(isMockMode ? mockDraft.title : '');
  const [source, setSource] = useState(isMockMode ? mockDraft.source : null);
  const [styleName, setStyleName] = useState(isMockMode ? mockDraft.styleName : null);
  const [duration, setDuration] = useState(isMockMode ? mockDraft.duration : null);
  const [music, setMusic] = useState(isMockMode ? mockDraft.music : null);
  const [autoCaption, setAutoCaption] = useState(isMockMode);
  const [softMusic, setSoftMusic] = useState(isMockMode);
  const [toast, setToast] = useState(null);

  const handleGenerate = () => {
    if (!canGenerate) {
      setToast({ message: 'Real 模式暂未开放 AI 视频生成，不会创建本地模拟任务。', tone: 'info' });
      return;
    }
    if (!title.trim() || !source || !styleName || !duration) {
      setToast({ message: '请先完成 Mock 视频配置。', tone: 'error' });
      return;
    }
    const creation = addCreation({
      type: '视频',
      title: title.trim(),
      source,
      styleName: `${styleName} · ${duration}${softMusic && music ? ` · ${music}` : ''}`,
      status: '生成中 · Mock 视频流程演示',
      icon: 'film-outline',
      progress: 46,
    });
    if (!creation) {
      setToast({ message: '当前模式无法创建本地模拟任务。', tone: 'error' });
      return;
    }
    router.push('/ai/progress');
  };

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="AI 短视频" right={<Ionicons name={canGenerate ? 'help-circle-outline' : 'lock-closed-outline'} size={24} color={colors.textSoft} />} />}
      topSpace={18}
      bottomSpace={64}
    >
      <View style={styles.content}>
        <FairyCard style={styles.heroCard}>
          <FairyImage name="workshopCover" height={210} radius={22} framed={false} />
          <View style={styles.heroCopy}>
            <FairyTag tone="gold">回忆放映机</FairyTag>
            <Text style={styles.heroTitle}>{isMockMode ? '把回忆剪成一段 Mock 小电影' : '真实 AI 视频生成暂未开放'}</Text>
            <Text style={styles.heroText}>{isMockMode ? '当前配置只用于验证页面和本地演示任务。' : 'Real 模式不会预填虚构标题、素材、音乐或封面，也不会承诺生成和自动保存。'}</Text>
          </View>
        </FairyCard>

        <FairyCard style={[styles.formCard, !canGenerate && styles.disabledCard]}>
          <FairyInput
            label="作品名称"
            icon="film-outline"
            value={title}
            onChangeText={setTitle}
            editable={canGenerate}
            maxLength={30}
            placeholder={canGenerate ? '例如：一起散步的春天' : '真实生成能力接入后填写'}
            containerStyle={styles.inputGroup}
          />
          <ChoiceSection title="选择回忆素材" options={sourceOptions} value={source} onChange={setSource} disabled={!canGenerate} />
          <ChoiceSection title="视频风格" options={styleOptions} value={styleName} onChange={setStyleName} disabled={!canGenerate} />
          <ChoiceSection title="视频时长" options={durationOptions} value={duration} onChange={setDuration} disabled={!canGenerate} />
          <Text style={styles.sectionTitle}>声音与字幕</Text>
          <SettingRow title="自动字幕" detail={canGenerate ? 'Mock 配置项，不代表真实识别服务' : '真实字幕服务尚未接入'} value={autoCaption} onValueChange={setAutoCaption} disabled={!canGenerate} />
          <SettingRow title="轻音乐" detail={canGenerate ? 'Mock 配置项，不代表真实音乐授权' : '真实音乐服务尚未接入'} value={softMusic} onValueChange={setSoftMusic} disabled={!canGenerate} />
          {canGenerate && softMusic ? <ChoiceSection title="背景音乐" options={musicOptions} value={music} onChange={setMusic} /> : null}
        </FairyCard>

        <FairyButton
          title={canGenerate ? '创建 Mock 视频任务' : 'AI 视频生成未开放'}
          disabled={!canGenerate}
          onPress={handleGenerate}
          leftContent={<Ionicons name={canGenerate ? 'color-wand' : 'lock-closed-outline'} size={20} color={colors.white} />}
        />
        <Text style={styles.estimate}>{canGenerate ? '仅创建本地 Mock 流程，不代表真实 AI 已开始处理' : 'Real 模式不会创建任务、作品或成功状态'}</Text>
      </View>
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function ChoiceSection({ title, options, value, onChange, disabled = false }) {
  return (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      <View style={styles.optionRow}>
        {options.map((item) => {
          const active = value === item;
          return (
            <Pressable
              key={item}
              disabled={disabled}
              onPress={() => onChange(item)}
              style={({ pressed }) => [styles.option, active && styles.optionActive, (pressed || disabled) && styles.optionMuted]}
            >
              <Text style={[styles.optionText, active && styles.optionTextActive]}>{item}</Text>
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}

function SettingRow({ title, detail, value, onValueChange, disabled }) {
  return (
    <View style={styles.settingRow}>
      <View style={styles.settingCopy}><Text style={styles.settingTitle}>{title}</Text><Text style={styles.settingDetail}>{detail}</Text></View>
      <Switch disabled={disabled} value={value} onValueChange={onValueChange} trackColor={{ false: colors.secondary, true: colors.primary }} thumbColor={colors.white} />
    </View>
  );
}

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 760, alignSelf: 'center' },
  heroCard: { marginBottom: spacing.lg, backgroundColor: colors.cardPink },
  heroCopy: { marginTop: spacing.md },
  heroTitle: { marginTop: spacing.md, color: colors.text, fontSize: 20, lineHeight: 28, fontWeight: '900' },
  heroText: { marginTop: spacing.xs, color: colors.textSoft, fontSize: 12, lineHeight: 20 },
  formCard: { marginBottom: spacing.lg },
  disabledCard: { opacity: 0.72 },
  inputGroup: { marginBottom: spacing.xl },
  section: { marginBottom: spacing.xl },
  sectionTitle: { color: colors.text, fontSize: 17, fontWeight: '900', marginBottom: spacing.md },
  optionRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  option: { flexGrow: 1, minWidth: 100, minHeight: 46, alignItems: 'center', justifyContent: 'center', paddingHorizontal: spacing.md, borderRadius: 18, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background },
  optionActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  optionMuted: { opacity: 0.58 },
  optionText: { color: colors.textSoft, fontSize: 13, fontWeight: '800' },
  optionTextActive: { color: colors.primaryDeep },
  settingRow: { flexDirection: 'row', alignItems: 'center', minHeight: 66, gap: spacing.md, borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: colors.border },
  settingCopy: { flex: 1, minWidth: 0 },
  settingTitle: { color: colors.text, fontSize: 14, fontWeight: '900' },
  settingDetail: { marginTop: 3, color: colors.textSoft, fontSize: 10, lineHeight: 16 },
  estimate: { marginTop: spacing.md, textAlign: 'center', color: colors.textSoft, fontSize: 11 },
});