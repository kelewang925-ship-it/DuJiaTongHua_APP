import { View, Text, TextInput, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import spacing from '../theme/spacing';

if (typeof document !== 'undefined' && !document.getElementById('fairy-input-password-style')) {
  const style = document.createElement('style');
  style.id = 'fairy-input-password-style';
  style.textContent = `
    input::-ms-reveal,
    input::-ms-clear {
      display: none;
    }
  `;
  document.head.appendChild(style);
}

const labelIconMap = {
  邮箱: 'mail-outline',
  密码: 'lock-closed-outline',
  手机号: 'phone-portrait-outline',
  '手机号（可选）': 'phone-portrait-outline',
  你的昵称: 'person-outline',
  我的昵称: 'person-outline',
  伴侣昵称: 'people-outline',
  恋爱起始日: 'calendar-outline',
};

export default function FairyInput({
  label,
  icon,
  error,
  helper,
  multiline = false,
  containerStyle,
  labelStyle,
  labelRowStyle,
  inputWrapStyle,
  inputStyle,
  helperInside = false,
  helperStyle,
  right,
  ...props
}) {
  const isPlainLabel = typeof label === 'string' || typeof label === 'number';
  const resolvedIcon = icon || (isPlainLabel ? labelIconMap[label] : undefined);

  return (
    <View style={[styles.container, containerStyle]}>
      {label ? (
        <View style={[styles.labelRow, labelRowStyle]}>
          {isPlainLabel ? <Text style={[styles.label, labelStyle]}>{label}</Text> : label}
        </View>
      ) : null}
      <View style={[styles.inputWrap, multiline && styles.multilineWrap, error && styles.errorWrap, inputWrapStyle]}>
        {resolvedIcon ? <Ionicons name={resolvedIcon} size={19} color={colors.accent} style={styles.icon} /> : null}
        <TextInput
          {...props}
          multiline={multiline}
          textAlignVertical={multiline ? 'top' : 'center'}
          placeholderTextColor={colors.textSoft}
          style={[styles.input, multiline && styles.multilineInput, inputStyle]}
        />
        {right ? <View style={styles.right}>{right}</View> : null}
        {!error && helper && helperInside ? (
          <Text style={[styles.helperText, styles.helperInsideText, helperStyle]}>{helper}</Text>
        ) : null}
      </View>
      {error ? (
        <Text style={styles.errorText}>{error}</Text>
      ) : helper && !helperInside ? (
        <Text style={[styles.helperText, helperStyle]}>{helper}</Text>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: spacing.lg,
  },
  label: {
    color: colors.text,
    fontSize: 15,
    fontWeight: '800',
  },
  labelRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  inputWrap: {
    minHeight: 50,
    borderRadius: 18,
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
  },
  multilineWrap: {
    minHeight: 128,
    alignItems: 'flex-start',
    paddingTop: spacing.md,
  },
  errorWrap: {
    borderColor: colors.primaryDeep,
    backgroundColor: '#FFF0F2',
  },
  icon: {
    marginRight: spacing.sm,
    marginTop: 1,
  },
  input: {
    flex: 1,
    color: colors.text,
    fontSize: 15,
    lineHeight: 22,
    paddingVertical: 0,
    outlineStyle: 'none',
  },
  right: {
    marginLeft: spacing.sm,
  },
  multilineInput: {
    minHeight: 100,
    paddingTop: 0,
  },
  helperText: {
    color: colors.textSoft,
    fontSize: 12,
    lineHeight: 18,
    marginTop: spacing.xs,
  },
  helperInsideText: {
    position: 'absolute',
    right: spacing.md,
    bottom: spacing.xs,
    marginTop: 0,
  },
  errorText: {
    color: colors.primaryDeep,
    fontSize: 12,
    lineHeight: 18,
    marginTop: spacing.xs,
    fontWeight: '700',
  },
});
