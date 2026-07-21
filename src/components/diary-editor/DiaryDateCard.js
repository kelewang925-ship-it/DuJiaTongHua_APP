import { StyleSheet, Text, View } from 'react-native';

import colors from '@/theme/colors';

export default function DiaryDateCard({ dateText }) {
  return (
    <View style={styles.card}>
      <View style={styles.tape} />
      <Text style={styles.date}>{dateText}</Text>
      <Text style={styles.tip}>把今天折进故事书里 ✨</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    position: 'relative',
    width: '100%',
    padding: 20,
    borderRadius: 16,
    backgroundColor: '#FFF9E9',
    borderWidth: 1,
    borderStyle: 'dashed',
    borderColor: colors.textSoft,
    shadowColor: '#000',
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 2,
    alignItems: 'center',
    marginBottom: 16,
  },
  tape: {
    position: 'absolute',
    width: 70,
    height: 22,
    top: -10,
    backgroundColor: 'rgba(255,255,255,0.65)',
    transform: [{ rotate: '-5deg' }],
  },
  date: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '900',
  },
  tip: {
    marginTop: 8,
    color: colors.textSoft,
    fontSize: 12,
  },
});
