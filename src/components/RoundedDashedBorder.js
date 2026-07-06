import { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import Svg, { Rect } from 'react-native-svg';

export default function RoundedDashedBorder({
  children,
  style,
  radius = 20,
  strokeColor = '#333',
  strokeWidth = 2,
  dashArray = '8 6',
}) {
  const [size, setSize] = useState({ width: 0, height: 0 });

  return (
    <View
      style={[styles.container, { borderRadius: radius }, style]}
      onLayout={({ nativeEvent }) => {
        const { width, height } = nativeEvent.layout;
        setSize((currentSize) => (
          currentSize.width === width && currentSize.height === height
            ? currentSize
            : { width, height }
        ));
      }}
    >
      {size.width > 0 && size.height > 0 ? (
        <Svg
          pointerEvents="none"
          width={size.width}
          height={size.height}
          style={styles.border}
        >
          <Rect
            x={strokeWidth / 2}
            y={strokeWidth / 2}
            width={size.width - strokeWidth}
            height={size.height - strokeWidth}
            rx={radius}
            ry={radius}
            fill="none"
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            strokeDasharray={dashArray}
          />
        </Svg>
      ) : null}
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'relative',
  },
  border: {
    ...StyleSheet.absoluteFillObject,
  },
});
