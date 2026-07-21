import { Pressable, StyleSheet, Text, View } from 'react-native';

const DEFAULT_TAGS = [
  { id: '约会', icon: '💕' },
  { id: '旅行', icon: '✈️' },
  { id: '日常', icon: '🏠' },
];

export default function DiaryTagSticker({ values = [], onChange, tags = DEFAULT_TAGS }) {
  const toggleTag = (id) => {
    const next = values.includes(id)
      ? values.filter((item) => item !== id)
      : [...values, id];

    onChange?.(next);
  };

  return (
    <View style={styles.container}>
      {tags.map((item, index) => (
        <Pressable
          key={item.id}
          onPress={() => toggleTag(item.id)}
          style={[
            styles.tag,
            { transform: [{ rotate: `${index % 2 ? -2 : 2}deg` }] },
            values.includes(item.id) && styles.selected,
          ]}
        >
          <Text>{item.icon}</Text>
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
    gap: 10,
  },
  tag: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    paddingHorizontal: 14,
    borderRadius: 20,
    backgroundColor: '#fffdf7',
    borderWidth: 1,
    borderColor: '#e7cdb8',
  },
  selected: {
    backgroundColor: '#ffe8dc',
  },
  text: {
    marginLeft: 4,
    color: '#6b4d3d',
    fontSize: 12,
    fontWeight: '700',
  },
});
