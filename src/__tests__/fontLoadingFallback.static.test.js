const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.resolve(__dirname, '..', '..', 'app', '_layout.js'), 'utf8');

describe('root font loading fallback', () => {
  test('loads the custom font only once on web', () => {
    expect(source).toContain("Platform.OS === 'web'");
    expect(source).toContain('? { [appFontFamily]: appFontSource }');
  });

  test('does not return a blank screen while the web font is loading', () => {
    expect(source).toContain('if (!fontsLoaded) {');
    expect(source).toContain('正在准备你们的童话...');
    expect(source).toContain('<ActivityIndicator');
    expect(source).not.toContain('if (!fontsLoaded) {\n    return null;');
  });
});
