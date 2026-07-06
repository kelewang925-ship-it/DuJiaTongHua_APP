import { useEffect, useRef } from 'react';
import { Animated, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import FairyCard from './FairyCard';

const toneMap = {
  success: {
    icon: 'checkmark-circle-outline',
    backgroundColor: '#FFF7F4',
    color: colors.accent,
  },
  error: {
    icon: 'alert-circle-outline',
    backgroundColor: '#FFF1F1',
    color: '#B56A6A',
  },
  info: {
    icon: 'sparkles-outline',
    backgroundColor: colors.cardPink,
    color: colors.accent,
  },
};

export default function FairyToast({ visible, message, tone = 'info', onHide, duration = 1800, style }) {
  const config = toneMap[tone] || toneMap.info;
  const opacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (!visible) return undefined;

    opacity.setValue(0);
    Animated.timing(opacity, {
      toValue: 1,
      duration: 160,
      useNativeDriver: true,
    }).start();

    const timer = setTimeout(() => {
      Animated.timing(opacity, {
        toValue: 0,
        duration: 180,
        useNativeDriver: true,
      }).start(() => {
        if (onHide) onHide();
      });
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, message, onHide, opacity, visible]);

  if (!visible || !message) return null;

  return (
    <Animated.View style={[styles.wrap, { opacity }, style]} pointerEvents="none">
      <FairyCard
        shadow="card"
        radius={18}
        padding={0}
        shadowStyle={styles.toastShadow}
        contentStyle={[styles.toast, { backgroundColor: config.backgroundColor }]}
      >
        <Ionicons name={config.icon} size={18} color={config.color} />
        <Text style={styles.message}>{message}</Text>
      </FairyCard>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    position: 'absolute',
    left: spacing.page,
    right: spacing.page,
    bottom: 36,
    alignItems: 'center',
    zIndex: 100,
  },
  toastShadow: {
    maxWidth: '100%',
  },
  toast: {
    maxWidth: '100%',
    minHeight: 44,
    borderRadius: 18,
    borderWidth: 1,
    borderColor: colors.border,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  message: {
    color: colors.text,
    fontSize: 13,
    fontWeight: '800',
  },
});
