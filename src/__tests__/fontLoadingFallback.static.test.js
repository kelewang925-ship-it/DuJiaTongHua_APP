const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.resolve(__dirname, '..', '..', 'app', '_layout.js'), 'utf8');

describe('root font loading fallback', () => {
  test('keeps the custom font registration native-only', () => {
    expect(source).toContain("Platform.OS === 'web'");
    expect(source).toContain("useFonts(Platform.OS === 'web' ? {} : appFontMap);");
    expect(source).not.toContain('injectWebDefaultFont');
  });

  test('does not retain a font-blocking root loading branch', () => {
    expect(source).not.toContain('正在准备你们的童话...');
    expect(source).not.toContain('fontLoadingPage');
  });

  test('uses the system font fallback for the Web first paint', () => {
    expect(source).toContain("if (Platform.OS === 'web') {\n    return;\n  }");
    expect(source).toContain('System typography keeps the application interactive');
  });
});
