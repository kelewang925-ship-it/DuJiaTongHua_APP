import React from 'react';
import { Stack } from 'expo-router';
import { useFonts } from 'expo-font';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, TextInput } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import AuthGate from '../src/components/AuthGate';
import { FairyMessageProvider } from '../src/components/FairyMessage';

const appFontFamily = 'AnJingChenShouShuFangSong';
const appFontStyle = {
  fontFamily: appFontFamily,
  fontWeight: '400',
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
        style: StyleSheet.flatten([origin.props.style, appFontStyle]),
      });
    };
  } else {
    Component.defaultProps = Component.defaultProps || {};
    Component.defaultProps.style = StyleSheet.flatten([
      Component.defaultProps.style,
      appFontStyle,
    ]);
  }

  Component.defaultFontFamily = appFontFamily;
};

applyDefaultFont(Text);
applyDefaultFont(TextInput);

export default function RootLayout() {
  const [fontsLoaded] = useFonts({
    [appFontFamily]: require('../assets/fonts/AnJingChenShouShuFangSong（Xin）-2.ttf'),
  });

  if (!fontsLoaded) {
    return null;
  }

  return (
    <SafeAreaProvider>
      <AuthGate>
        <FairyMessageProvider>
          <StatusBar style="dark" />
          <Stack screenOptions={{ headerShown: false }} />
        </FairyMessageProvider>
      </AuthGate>
    </SafeAreaProvider>
  );
}
