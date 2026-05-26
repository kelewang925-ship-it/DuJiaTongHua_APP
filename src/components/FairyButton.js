import { Pressable, Text, StyleSheet } from 'react-native';
import colors from '../theme/colors';

export default function FairyButton({ title, variant = 'primary', onPress, style, disabled = false }) {
  const isPrimary = variant === 'primary';
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.button,
        isPrimary ? styles.primary : styles.secondary,
        pressed && !disabled && styles.pressed,
        disabled && styles.disabled,
        style,
      ]}
    >
      <Text style={[styles.text, isPrimary ? styles.primaryText : styles.secondaryText, disabled && styles.disabledText]}>
        {title}
      </Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    height: 52,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
  },
  primary: {
    backgroundColor: colors.primary,
  },
  secondary: {
    backgroundColor: colors.secondary,
    borderWidth: 1,
    borderColor: colors.border,
  },
  pressed: {
    transform: [{ scale: 0.97 }],
    opacity: 0.9,
  },
  disabled: {
    opacity: 0.48,
  },
  text: {
    fontSize: 16,
    fontWeight: '700',
  },
  primaryText: {
    color: colors.white,
  },
  secondaryText: {
    color: colors.text,
  },
  disabledText: {
    color: colors.textSoft,
  },
});
