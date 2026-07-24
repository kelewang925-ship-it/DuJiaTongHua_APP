import { Ionicons } from '@expo/vector-icons';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import colors from '@/theme/colors';
import spacing from '@/theme/spacing';

const DEFAULT_MOODS = [
  { id: '开心', icon: 'sunny-outline' },
  { id: '想念', icon: 'heart-outline' },
  { id: '温柔', icon: 'flower-outline' },
  { id: '小确幸', icon: 'star-outline' },
];

export default function DiaryMoodSticker({ value, onChange, moods = DEFAULT_MOODS }) {
  return (
    <View style={styles.container}>
      {moods.map((item, index) => {
        const selected = value === item.id;
        return (
          <Pressable
            key={item.id}
            accessibilityRole="radio"
            accessibilityState={{ selected }}
            onPress={() => onChange?.(item.id)}
            style={[
              styles.sticker,
              { transform: [{ rotate: `${index % 2 ? 3 : -3}deg` }, ...(selected ? [{ scale: 1.06 }] : [])] },
              selected && styles.selected,
            ]}
          >
            <View style={[styles.iconFrame, selected && styles.iconFrameSelected]}>
              <Ionicons name={item.icon} size={24} color={selected ? colors.text.primary : colors.text.accent} />
            </View>
            <Text style={styles.text}>{item.id}</Text>
            {selected ? <Ionicons name="checkmark-circle" size={15} color={colors.text.primary} /> : null}
          </Pressable>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md },
  sticker: {
    minWidth: 116,
    flexGrow: 1,
    minHeight: 92,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md,
    borderRadius: 18,
    backgroundColor: colors.surface.card,
    borderWidth: 1,
    borderColor: colors.border.default,
    alignItems: 'center',
    shadowColor: colors.text.primary,
    shadowOpacity: 0.12,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 3 },
    elevation: 2,
  },
  selected: { backgroundColor: colors.surface.cardPink, borderColor: colors.border.focus, shadowOpacity: 0.2 },
  iconFrame: { width: 42, height: 42, borderRadius: 21, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.bg.secondary },
  iconFrameSelected: { backgroundColor: colors.text.inverse },
  text: { marginTop: 4, color: colors.text.primary, fontSize: 13, fontWeight: '700' },
});
