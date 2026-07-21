import { Pressable, StyleSheet, Text, View } from 'react-native';

const MOODS = [
  { id: '开心', icon: '😊' },
  { id: '想念', icon: '🥰' },
  { id: '温柔', icon: '🌸' },
  { id: '小确幸', icon: '⭐' },
  { id: '平静', icon: '💭' },
  { id: '小低落', icon: '🌧️' },
];

export default function MoodStickerGroup({ value, onChange }) {
  return (
    <View style={styles.container}>
      {MOODS.map((item) => (
        <Pressable
          key={item.id}
          onPress={() => onChange(item.id)}
          style={[styles.sticker, value === item.id && styles.active]}
        >
          <Text style={styles.icon}>{item.icon}</Text>
          <Text style={styles.text}>{item.id}</Text>
        </Pressable>
      ))}
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
    minWidth: 78,
    paddingVertical: 10,
    paddingHorizontal: 12,
    borderRadius: 24,
    backgroundColor: '#FFF9F4',
    borderWidth: 2,
    borderColor: '#FFFFFF',
    alignItems: 'center',
    shadowColor: '#8B7355',
    shadowOpacity: 0.12,
    shadowRadius: 5,
    elevation: 2,
  },
  active: {
    transform: [{ scale: 1.08 }],
    backgroundColor: '#FBE1E6',
  },
  icon: {
    fontSize: 22,
  },
  text: {
    marginTop: 3,
    fontSize: 12,
    fontWeight: '700',
  },
});
