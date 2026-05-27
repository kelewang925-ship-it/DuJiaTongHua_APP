import { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import FairyButton from '../src/components/FairyButton';
import FairyCard from '../src/components/FairyCard';
import FairyHeader from '../src/components/FairyHeader';
import FairyInput from '../src/components/FairyInput';
import FairyPage from '../src/components/FairyPage';
import FairyToast from '../src/components/FairyToast';
import colors from '../src/theme/colors';
import spacing from '../src/theme/spacing';

export default function HelpFeedbackPage() {
  const [content, setContent] = useState('');
  const [toastVisible, setToastVisible] = useState(false);

  return (
    <FairyPage>
      <FairyHeader showBack eyebrow="特殊页面" title="帮助与反馈" subtitle="遇到问题或有新的想法，都可以在这里告诉我们。" />

      <FairyCard style={styles.card}>
        <Text style={styles.sectionTitle}>常见问题</Text>
        <Text style={styles.item}>1. 如何绑定情侣空间：登录后进入邀请页，输入邀请码即可。</Text>
        <Text style={styles.item}>2. 作品为什么还在生成中：当前是 mock 状态，可在进度页模拟完成。</Text>
      </FairyCard>

      <FairyCard style={styles.card}>
        <FairyInput
          label="反馈内容"
          icon="chatbubble-ellipses-outline"
          value={content}
          onChangeText={setContent}
          multiline
          placeholder="例如：某个页面按钮不好点、文案想更温柔一些。"
          containerStyle={styles.inputWrap}
        />
        <View style={styles.actions}>
          <FairyButton title="提交反馈（mock）" onPress={() => setToastVisible(true)} />
        </View>
      </FairyCard>

      <FairyToast visible={toastVisible} tone="success" message="反馈已收到，感谢你一起打磨这本童话。" onHide={() => setToastVisible(false)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  card: { marginBottom: spacing.lg },
  sectionTitle: { color: colors.text, fontSize: 16, fontWeight: '900', marginBottom: spacing.sm },
  item: { color: colors.textSoft, lineHeight: 21, marginBottom: spacing.xs },
  inputWrap: { marginBottom: spacing.md },
  actions: { gap: spacing.md },
});
