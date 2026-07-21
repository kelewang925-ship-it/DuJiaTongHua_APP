import { Image, Pressable, StyleSheet, Text, View } from 'react-native';

export default function PhotoCollage({ attachments = [], onAdd, onRemove }) {
  return (
    <View style={styles.container}>
      {attachments.length === 0 ? (
        <Pressable onPress={onAdd} style={styles.empty}>
          <Text style={styles.icon}>📷</Text>
          <Text style={styles.text}>贴上照片</Text>
        </Pressable>
      ) : (
        attachments.map((item, index) => (
          <Pressable key={item.uri} onLongPress={() => onRemove?.(index)} style={styles.photo}>
            <Image source={{ uri: item.uri }} style={styles.image} />
          </Pressable>
        ))
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  empty: {
    width: 150,
    height: 120,
    borderWidth: 1,
    borderStyle: 'dashed',
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  icon: { fontSize: 28 },
  text: { marginTop: 6, fontWeight: '800' },
  photo: {
    width: 120,
    height: 120,
    backgroundColor: '#fff',
    padding: 8,
    transform: [{ rotate: '-2deg' }],
    elevation: 3,
  },
  image: { width: '100%', height: '100%' },
});
