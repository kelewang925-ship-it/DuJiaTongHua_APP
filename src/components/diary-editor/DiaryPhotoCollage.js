import { Pressable, StyleSheet, Text, View } from 'react-native';

import colors from '@/theme/colors';
import spacing from '@/theme/spacing';

export default function DiaryPhotoCollage({ photos = [], onAddPhoto, onRemovePhoto }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>照片拼贴</Text>

      <View style={styles.content}>
        {photos.map((photo, index) => (
          <Pressable
            key={`${photo}-${index}`}
            style={styles.photo}
            onLongPress={() => onRemovePhoto?.(index)}
          >
            <Text style={styles.photoText}>照片</Text>
          </Pressable>
        ))}

        <Pressable style={styles.add} onPress={onAddPhoto}>
          <Text style={styles.icon}>📷</Text>
          <Text style={styles.addText}>贴上照片</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: spacing.md,
    padding: spacing.md,
    backgroundColor: '#FFF9F0',
    borderRadius: 18,
  },
  title: {
    color: colors.text,
    fontSize: 15,
    marginBottom: spacing.sm,
  },
  content: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
  },
  photo: {
    width: 90,
    height: 110,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  photoText: {
    color: colors.textSecondary,
  },
  add: {
    width: 90,
    height: 110,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderStyle: 'dashed',
    borderColor: colors.border,
  },
  icon: {
    fontSize: 24,
  },
  addText: {
    marginTop: spacing.xs,
    color: colors.textSecondary,
  },
});
