import { ScrollView, StyleSheet, View } from 'react-native';
import colors from '../theme/colors';
import spacing from '../theme/spacing';

export default function FairyPage({
  children,
  scroll = true,
  style,
  contentStyle,
  tabSafe = false,
  topSpace = 54,
  bottomSpace = 44,
}) {
  const contentStyles = [
    styles.content,
    { paddingTop: topSpace, paddingBottom: tabSafe ? 124 : bottomSpace },
    contentStyle,
  ];

  if (!scroll) {
    return <View style={[styles.page, styles.staticContent, style]}>{children}</View>;
  }

  return (
    <ScrollView style={[styles.page, style]} contentContainerStyle={contentStyles} showsVerticalScrollIndicator={false}>
      {children}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    paddingHorizontal: spacing.page,
  },
  staticContent: {
    paddingHorizontal: spacing.page,
  },
});
