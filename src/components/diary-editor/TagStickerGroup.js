import { Pressable, StyleSheet, Text, View } from 'react-native';

const DEFAULT_TAGS = [
  { id: '约会', icon: '💕' },
  { id: '旅行', icon: '✈️' },
  { id: '日常', icon: '🏠' },
  { id: '纪念日', icon: '🎂' },
];

export default function TagStickerGroup({ selectedTags = [], onToggle }) {
  return (
    <View style={styles.container}>
      {DEFAULT_TAGS.map((tag) => {
        const active = selectedTags.includes(tag.id);
        return (
          <Pressable key={tag.id} onPress={() => onToggle?.(tag.id)} style={[styles.tag, active && styles.active]}>
            <Text>{tag.icon}</Text>
            <Text style={styles.text}>{tag.id}</Text>
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
    gap: 10,
  },
  tag: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 14,
    paddingVertical: 9,
    borderRadius: 18,
    backgroundColor: '#FFF9F4',
    borderWidth: 1,
    borderStyle: 'dashed',
    borderColor: '#C7A98A',
  },
  active: {
    backgroundColor: '#FFE6EC',
    transform: [{ rotate: '1deg' }],
  },
  text: {
    marginLeft: 4,
    fontWeight: '800',
  },
});
