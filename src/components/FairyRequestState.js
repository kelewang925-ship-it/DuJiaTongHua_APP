import { ActivityIndicator, StyleSheet, Text, View } from 'react-native';
import FairyButton from './FairyButton';
import FairyCard from './FairyCard';
import colors from '../theme/colors';
import spacing from '../theme/spacing';

function copyForError(error) {
  const code = error?.code;
  if (code === 'SESSION_EXPIRED' || code === 'AUTH_REQUIRED') {
    return { title: '登录状态已失效', description: '请重新登录后，再继续打开这页故事。' };
  }
  if (code === 'PERMISSION_DENIED') {
    return { title: '暂时无法查看这页', description: '当前账号没有访问这段情侣故事的权限。' };
  }
  if (code === 'NETWORK_ERROR') {
    return { title: '网络暂时走丢了', description: '检查网络连接后，再重新加载一次。' };
  }
  return { title: '这页故事暂时没打开', description: error?.message || '请稍后重试。' };
}

export default function FairyRequestState({ loading, error, onRetry, compact = false }) {
  if (!loading && !error) return null;

  if (loading) {
    return (
      <FairyCard style={[styles.card, compact && styles.compactCard]}>
        <ActivityIndicator color={colors.primaryDeep} />
        <Text style={styles.title}>正在翻开这一页...</Text>
        <Text style={styles.description}>正在同步只属于你们的故事。</Text>
      </FairyCard>
    );
  }

  const copy = copyForError(error);
  return (
    <FairyCard style={[styles.card, compact && styles.compactCard]}>
      <Text style={styles.title}>{copy.title}</Text>
      <Text style={styles.description}>{copy.description}</Text>
      {onRetry ? <FairyButton title="重新加载" variant="secondary" onPress={onRetry} style={styles.retry} /> : null}
    </FairyCard>
  );
}

const styles = StyleSheet.create({
  card: { alignItems: 'center', marginBottom: spacing.lg, backgroundColor: colors.cardPink },
  compactCard: { paddingVertical: spacing.lg },
  title: { marginTop: spacing.sm, color: colors.text, fontSize: 16, fontWeight: '900', textAlign: 'center' },
  description: { marginTop: spacing.xs, color: colors.textSoft, lineHeight: 20, textAlign: 'center' },
  retry: { marginTop: spacing.md, alignSelf: 'stretch' },
});
