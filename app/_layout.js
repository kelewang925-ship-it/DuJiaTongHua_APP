import React from 'react';
import { Stack } from 'expo-router';
import { useFonts } from 'expo-font';
import { StatusBar } from 'expo-status-bar';
import { ActivityIndicator, Platform, StyleSheet, Text, TextInput, View } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import AuthGate from '../src/components/AuthGate';
import { FairyMessageProvider } from '../src/components/FairyMessage';
import { useDevUI } from '../src/dev-ui-lab/hook/useDevUI';
import AppErrorFallback from '../src/components/AppErrorFallback';

const appFontFamily = 'AnJingChenShouShuFangSong';
const appFontSource = require('../assets/fonts/AnJingChenShouShuFangSong（Xin）-2.ttf');
const appFontWeights = ['100', '200', '300', '400', '500', '600', '700', '800', '900'];
const iconFontPattern = /Ionicons|Material|FontAwesome|Feather|Entypo|Octicons|Zocial|Foundation|EvilIcons/i;

const appFontFamilyByWeight = appFontWeights.reduce((families, weight) => ({
  ...families,
  [weight]: `${appFontFamily}-${weight}`,
}), {});

// Web uses the base family for every weight. Registering the same 10 MB file
// under every native weight makes the first Web render wait for redundant font
// requests before AuthGate can mount.
const appFontMap = Platform.OS === 'web'
  ? { [appFontFamily]: appFontSource }
  : appFontWeights.reduce(
    (fonts, weight) => ({
      ...fonts,
      [appFontFamilyByWeight[weight]]: appFontSource,
    }),
    { [appFontFamily]: appFontSource },
  );

const normalizeFontWeight = (fontWeight) => {
  if (!fontWeight || fontWeight === 'normal') {
    return '400';
  }
  if (fontWeight === 'bold') {
    return '700';
  }

  const numericWeight = Number(fontWeight);
  if (!Number.isFinite(numericWeight)) {
    return '400';
  }

  const nearestWeight = Math.min(900, Math.max(100, Math.round(numericWeight / 100) * 100));
  return String(nearestWeight);
};

const shouldKeepOriginalFont = (style) => {
  const fontFamily = StyleSheet.flatten(style)?.fontFamily;
  return typeof fontFamily === 'string' && iconFontPattern.test(fontFamily);
};

const withAppFont = (style) => {
  if (shouldKeepOriginalFont(style)) {
    return style;
  }

  const fontWeight = normalizeFontWeight(StyleSheet.flatten(style)?.fontWeight);

  if (Platform.OS === 'web') {
    return StyleSheet.flatten([style, { fontFamily: appFontFamily }]);
  }

  return StyleSheet.flatten([
    style,
    {
      fontFamily: appFontFamilyByWeight[fontWeight] || appFontFamily,
      fontWeight: '400',
    },
  ]);
};

const injectWebDefaultFont = () => {
  if (Platform.OS !== 'web' || typeof document === 'undefined') {
    return;
  }

  const styleId = 'dujia-tonghua-default-font';
  if (document.getElementById(styleId)) {
    return;
  }

  const styleElement = document.createElement('style');
  styleElement.id = styleId;
  styleElement.textContent = `
    [class*="css-text-"]:not([style*="font-family"]),
    [class*="css-textHasAncestor-"]:not([style*="font-family"]) {
      font-family: "${appFontFamily}" !important;
    }
  `;
  document.head.appendChild(styleElement);
};

const applyDefaultFont = (Component) => {
  if (Component.defaultFontFamily === appFontFamily) {
    return;
  }

  if (typeof Component.render === 'function') {
    const originalRender = Component.render;

    Component.render = function renderWithDefaultFont(...args) {
      const origin = originalRender.call(this, ...args);
      if (!React.isValidElement(origin)) {
        return origin;
      }

      return React.cloneElement(origin, {
        style: withAppFont(origin.props.style),
      });
    };
  } else {
    Component.defaultProps = Component.defaultProps || {};
    Component.defaultProps.style = withAppFont(Component.defaultProps.style);
  }

  Component.defaultFontFamily = appFontFamily;
};

applyDefaultFont(Text);
applyDefaultFont(TextInput);

export function ErrorBoundary({ error, retry }) {
  return <AppErrorFallback error={error} retry={retry} />;
}

export default function RootLayout() {
  const [fontsLoaded] = useFonts(appFontMap);

  const devUIHandlers = useDevUI();

  if (!fontsLoaded) {
    return (
      <View style={styles.fontLoadingPage}>
        <ActivityIndicator color="#C8897A" />
        <Text style={styles.fontLoadingText}>正在准备你们的童话...</Text>
      </View>
    );
  }

  injectWebDefaultFont();

  return (
    <SafeAreaProvider>
      <AuthGate>
        <FairyMessageProvider>
          <StatusBar style="dark" />
          <View style={styles.rootTouchLayer} {...devUIHandlers}>
            <Stack screenOptions={{ headerShown: false }} />
          </View>
        </FairyMessageProvider>
      </AuthGate>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  rootTouchLayer: {
    flex: 1,
  },
  fontLoadingPage: {
    flex: 1,
    backgroundColor: '#FFF7F2',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
  },
  fontLoadingText: {
    color: '#8D7770',
    fontSize: 13,
    fontWeight: '700',
  },
});
