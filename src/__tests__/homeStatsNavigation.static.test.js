import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'app/(tabs)/index.js'), 'utf8');

describe('home statistics navigation', () => {
  test('makes diary and photo statistics explicit navigation actions', () => {
    expect(source).toContain("{ label: '日记', value: diaryCount, icon: 'book-outline', href: '/diary' }");
    expect(source).toContain("{ label: '照片', value: photoCount, icon: 'images-outline', href: '/photo/album' }");
    expect(source).toContain('accessibilityLabel={`查看${item.label}`}');
    expect(source).toContain('onPress={() => router.push(item.href)}');
  });

  test('keeps the full statistic card as the accessible press target', () => {
    expect(source).toContain('style={({ pressed }) => [styles.statPressable, !compact && styles.statPressableWide, pressed && styles.pressed]}');
    expect(source).toContain('statPressable:');
    expect(source).toContain("statCard: { width: '100%'");
  });
});
