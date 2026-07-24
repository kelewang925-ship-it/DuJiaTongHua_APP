import { Ionicons } from '@expo/vector-icons';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import colors from '@/theme/colors';
import spacing from '@/theme/spacing';

const DEFAULT_TAGS = [
  { id: '约会', icon: 'calendar-outline' },
  { id: '旅行', icon: 'briefcase-outline' },
  { id: '日常', icon: 'home-outline' },
];

export default function DiaryTagSticker({ tags = DEFAULT_TAGS, values = [], onChange }) {
  const toggleTag = (id) => {
    const next = values.includes(id) ? values.filter((item) => item !== id) : [...values, id];
    onChange?.(next);
  };

  return (
    <View style={styles.container}>
      {tags.map((item, index) => {
        const selected = values.includes(item.id);
        return (
          <Pressable
            key={item.id}
            accessibilityRole="checkbox"
            accessibilityState={{ checked: selected }}
            onPress={() => toggleTag(item.id)}
            style={[
              styles.tag,
              { transform: [{ rotate: `${index % 2 ? -2 : 2}deg` }] },
              selected && styles.selected,
            ]}
          >
            <Ionicons name={item.icon} size={17} color={selected ? colors.text.primary : colors.text.accent} />
            <Text style={styles.text}>{item.id}</Text>
            {selected ? <Ionicons name="checkmark" size={15} color={colors.text.primary} /> : null}
          </Pressable>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  tag: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md,
    borderRadius: 20,
    backgroundColor: colors.surface.card,
    borderWidth: 1,
    borderColor: colors.border.default,
  },
  selected: { backgroundColor: colors.surface.cardPink, borderColor: colors.border.focus },
  text: { marginLeft: spacing.xs, color: colors.text.primary, fontSize: 12, fontWeight: '700' },
});
