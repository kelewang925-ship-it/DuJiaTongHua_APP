import { Pressable, StyleSheet, Text, View } from 'react-native';

const DEFAULT_MOODS = [
  { id: '开心', icon: '😊' },
  { id: '想念', icon: '🥰' },
  { id: '温柔', icon: '🌸' },
  { id: '小确幸', icon: '⭐' },
];

export default function DiaryMoodSticker({ value, onChange, moods = DEFAULT_MOODS }) {
  return (
    <View style={styles.container}>
      {moods.map((item, index) => {
        const selected = value === item.id;
        return (
          <Pressable
            key={item.id}
            onPress={() => onChange?.(item.id)}
            style={[
              styles.sticker,
              { transform: [{ rotate: `${index % 2 ? 3 : -3}deg` }] },
              selected && styles.selected,
            ]}
          >
            <Text style={styles.icon}>{item.icon}</Text>
            <Text style={styles.text}>{item.id}</Text>
          </Pressable>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  sticker: {
    minWidth: 72,
    paddingVertical: 10,
    paddingHorizontal: 12,
    borderRadius: 14,
    backgroundColor: '#fff8ee',
    alignItems: 'center',
    shadowColor: '#8f6b55',
    shadowOpacity: 0.12,
    shadowRadius: 6,
    elevation: 2,
  },
  selected: {
    transform: [{ scale: 1.08 }],
  },
  icon: {
    fontSize: 24,
  },
  text: {
    marginTop: 4,
    fontSize: 12,
    color: '#6b4d3d',
    fontWeight: '700',
  },
});
