import { Modal, View, Text, StyleSheet, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import shadows from '../theme/shadows';
import FairyButton from './FairyButton';

export default function FairyDialog({
  visible,
  title,
  description,
  icon = 'heart-outline',
  confirmText = '确认',
  cancelText = '取消',
  onConfirm,
  onCancel,
  children,
}) {
  return (
    <Modal visible={visible} transparent animationType="fade" onRequestClose={onCancel}>
      <View style={styles.overlay}>
        <View style={styles.dialog}>
          <Pressable style={styles.close} onPress={onCancel}>
            <Ionicons name="close" size={18} color={colors.textSoft} />
          </Pressable>
          <View style={styles.iconWrap}>
            <Ionicons name={icon} size={28} color={colors.accent} />
          </View>
          <Text style={styles.title}>{title}</Text>
          {description ? <Text style={styles.description}>{description}</Text> : null}
          {children ? <View style={styles.children}>{children}</View> : null}
          <View style={styles.actions}>
            <FairyButton title={cancelText} variant="secondary" style={styles.action} onPress={onCancel} />
            <FairyButton title={confirmText} style={styles.action} onPress={onConfirm} />
          </View>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(107, 79, 79, 0.22)',
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.page,
  },
  dialog: {
    width: '100%',
    borderRadius: 30,
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.xxl,
    alignItems: 'center',
    ...shadows.floating,
  },
  close: {
    position: 'absolute',
    top: 14,
    right: 14,
    width: 34,
    height: 34,
    borderRadius: 14,
    backgroundColor: colors.cardPink,
    alignItems: 'center',
    justifyContent: 'center',
  },
  iconWrap: {
    width: 66,
    height: 66,
    borderRadius: 26,
    backgroundColor: colors.cardPink,
    borderWidth: 1,
    borderColor: colors.border,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.lg,
  },
  title: {
    color: colors.text,
    fontSize: 20,
    fontWeight: '900',
    textAlign: 'center',
  },
  description: {
    color: colors.textSoft,
    textAlign: 'center',
    lineHeight: 22,
    marginTop: spacing.sm,
  },
  children: {
    alignSelf: 'stretch',
    marginTop: spacing.lg,
  },
  actions: {
    flexDirection: 'row',
    gap: spacing.md,
    marginTop: spacing.xxl,
    alignSelf: 'stretch',
  },
  action: {
    flex: 1,
  },
});
