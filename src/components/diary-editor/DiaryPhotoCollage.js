import { Ionicons } from '@expo/vector-icons';
import { Image, Pressable, StyleSheet, Text, View } from 'react-native';

import colors from '@/theme/colors';
import spacing from '@/theme/spacing';

export default function DiaryPhotoCollage({ images = [], onAdd, onRemove }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>我的回忆照片</Text>
      <View style={styles.content}>
        {images.map((photo, index) => (
          <View key={`${photo.uri || photo}-${index}`} style={styles.photo}>
            <Image source={{ uri: photo.uri || photo }} resizeMode="cover" style={styles.photoImage} />
            <Pressable
              accessibilityRole="button"
              accessibilityLabel={`移除第${index + 1}张照片`}
              hitSlop={6}
              onPress={() => onRemove?.(index)}
              style={styles.remove}
            >
              <Ionicons name="close" size={14} color={colors.text.inverse} />
            </Pressable>
          </View>
        ))}
        <Pressable accessibilityRole="button" onPress={onAdd} style={styles.add}>
          <Ionicons name="images-outline" size={25} color={colors.text.primary} />
          <Text style={styles.addText}>贴上照片</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginVertical: spacing.md, padding: spacing.md, backgroundColor: colors.surface.card, borderRadius: 18, borderWidth: 1, borderColor: colors.border.default },
  title: { color: colors.text.primary, fontSize: 15, fontWeight: '900', marginBottom: spacing.sm },
  content: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  photo: { position: 'relative', width: 92, height: 108, borderRadius: 12, backgroundColor: colors.text.inverse },
  photoImage: { width: '100%', height: '100%', borderRadius: 12 },
  remove: { position: 'absolute', top: -7, right: -7, width: 24, height: 24, borderRadius: 12, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.text.accent },
  add: { width: 92, height: 108, borderRadius: 12, justifyContent: 'center', alignItems: 'center', borderWidth: 1, borderStyle: 'dashed', borderColor: colors.border.focus, backgroundColor: colors.surface.cardPink },
  addText: { marginTop: spacing.xs, color: colors.text.primary, fontSize: 12, fontWeight: '800' },
});
