import { StyleSheet, Text, TextInput, View } from 'react-native';

import colors from '@/theme/colors';

export default function DiaryTitleStickyNote({
  value,
  onChangeText,
  maxLength = 30,
}) {
  return (
    <View style={styles.wrapper}>
      <View style={styles.tape} />
      <Text style={styles.label}>给今天起个温暖的名字</Text>
      <TextInput
        value={value}
        onChangeText={onChangeText}
        multiline
        maxLength={maxLength}
        placeholder="写下这一页故事的标题..."
        placeholderTextColor={colors.textSoft}
        style={styles.input}
      />
      <Text style={styles.counter}>
        {(value || '').length}/{maxLength}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    position: 'relative',
    backgroundColor: '#FFF8E8',
    paddingHorizontal: 16,
    paddingTop: 22,
    paddingBottom: 12,
    marginBottom: 18,
    borderRadius: 4,
    transform: [{ rotate: '-1deg' }],
    shadowColor: '#000',
    shadowOpacity: 0.08,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 4 },
    elevation: 2,
  },
  tape: {
    position: 'absolute',
    width: 70,
    height: 18,
    top: -8,
    left: '38%',
    backgroundColor: '#EFD7B5',
    opacity: 0.8,
  },
  label: {
    fontSize: 12,
    color: colors.textSoft,
    marginBottom: 8,
  },
  input: {
    minHeight: 40,
    fontSize: 16,
    color: colors.text,
    padding: 0,
    fontWeight: '700',
  },
  counter: {
    marginTop: 8,
    textAlign: 'right',
    fontSize: 11,
    color: colors.textSoft,
  },
});