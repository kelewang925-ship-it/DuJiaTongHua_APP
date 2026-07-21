import { StyleSheet, Text, TextInput, View } from 'react-native';

import colors from '@/theme/colors';

export default function TitleStickyNote({ value, onChangeText, maxLength = 30 }) {
  return (
    <View style={styles.wrap}>
      <View style={styles.tape} />
      <TextInput
        value={value}
        onChangeText={onChangeText}
        placeholder="给今天起个温暖的名字..."
        placeholderTextColor={colors.textSoft}
        maxLength={maxLength}
        multiline
        style={styles.input}
      />
      <Text style={styles.counter}>{value.length}/{maxLength}</Text>
      <Text style={styles.pen}>✎</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    position: 'relative',
    minHeight: 92,
    padding: 18,
    marginBottom: 18,
    borderRadius: 10,
    backgroundColor: '#FFF8DC',
    transform: [{ rotate: '1deg' }],
    shadowColor: '#8B7355',
    shadowOpacity: 0.16,
    shadowRadius: 8,
    elevation: 3,
  },
  tape: {
    position: 'absolute',
    width: 58,
    height: 22,
    top: -9,
    left: '38%',
    backgroundColor: 'rgba(255,255,255,0.65)',
    transform: [{ rotate: '-5deg' }],
  },
  input: {
    minHeight: 42,
    padding: 0,
    color: colors.text,
    fontSize: 16,
    fontWeight: '700',
  },
  counter: {
    alignSelf: 'flex-end',
    color: colors.textSoft,
    fontSize: 11,
  },
  pen: {
    position: 'absolute',
    left: 12,
    bottom: 8,
    color: colors.primaryDeep,
  },
});
