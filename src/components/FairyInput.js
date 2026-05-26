import { View, Text, TextInput, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import spacing from '../theme/spacing';

export default function FairyInput({
  label,
  icon,
  error,
  helper,
  multiline = false,
  containerStyle,
  inputStyle,
  ...props
}) {
  return (
    <View style={[styles.container, containerStyle]}>
      {label ? <Text style={styles.label}>{label}</Text> : null}
      <View style={[styles.inputWrap, multiline && styles.multilineWrap, error && styles.errorWrap]}>
        {icon ? <Ionicons name={icon} size={19} color={colors.accent} style={styles.icon} /> : null}
        <TextInput
          {...props}
          multiline={multiline}
          textAlignVertical={multiline ? 'top' : 'center'}
          placeholderTextColor={colors.textSoft}
          style={[styles.input, multiline && styles.multilineInput, inputStyle]}
        />
      </View>
      {error ? <Text style={styles.errorText}>{error}</Text> : helper ? <Text style={styles.helperText}>{helper}</Text> : null}
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
  errorText: {
    color: colors.primaryDeep,
    fontSize: 12,
    lineHeight: 18,
    marginTop: spacing.xs,
    fontWeight: '700',
  },
});
