import { View, Text, StyleSheet, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import shadows from '../theme/shadows';

const iconMap = {
  index: 'book-outline',
  couple: 'heart-outline',
  workshop: 'sparkles-outline',
  mine: 'person-outline',
};

export default function FairyTabBar({ state, descriptors, navigation }) {
  return (
    <View style={styles.safeArea}>
      <View style={styles.container}>
        {state.routes.map((route, index) => {
          const { options } = descriptors[route.key];
          const label = options.title || route.name;
          const isFocused = state.index === index;
          const iconName = iconMap[route.name] || 'ellipse-outline';

          const onPress = () => {
            const event = navigation.emit({
              type: 'tabPress',
              target: route.key,
              canPreventDefault: true,
            });

            if (!isFocused && !event.defaultPrevented) {
              navigation.navigate(route.name, route.params);
            }
          };

          return (
            <Pressable
              key={route.key}
              accessibilityRole="button"
              accessibilityState={isFocused ? { selected: true } : {}}
              accessibilityLabel={options.tabBarAccessibilityLabel}
              testID={options.tabBarTestID}
              onPress={onPress}
              style={({ pressed }) => [styles.item, isFocused && styles.activeItem, pressed && styles.pressed]}
            >
              <View style={[styles.iconWrap, isFocused && styles.activeIconWrap]}>
                <Ionicons name={iconName} size={isFocused ? 22 : 20} color={isFocused ? colors.white : colors.textSoft} />
              </View>
              <Text style={[styles.label, isFocused && styles.activeLabel]} numberOfLines={1}>{label}</Text>
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.md,
    paddingTop: spacing.sm,
    backgroundColor: 'transparent',
  },
  container: {
    minHeight: 76,
    borderRadius: 30,
    backgroundColor: '#FFFAF8',
    borderWidth: 1,
    borderColor: colors.border,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    paddingHorizontal: spacing.sm,
    ...shadows.floating,
  },
  item: {
    flex: 1,
    minHeight: 60,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.xs,
  },
  activeItem: {
    backgroundColor: colors.cardPink,
    transform: [{ translateY: -3 }],
  },
  pressed: {
    opacity: 0.88,
    transform: [{ scale: 0.97 }],
  },
  iconWrap: {
    width: 34,
    height: 30,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 2,
  },
  activeIconWrap: {
    backgroundColor: colors.primaryDeep,
  },
  label: {
    color: colors.textSoft,
    fontSize: 11,
    fontWeight: '700',
  },
  activeLabel: {
    color: colors.text,
    fontWeight: '900',
  },
});
