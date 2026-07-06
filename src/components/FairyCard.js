import { Pressable, View, StyleSheet } from 'react-native';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import shadowTokens from '../theme/shadowTokens';

export default function FairyCard({
  children,
  style,
  shadowStyle,
  contentStyle,
  shadow = 'card',
  shadowBackgroundColor,
  radius = 24,
  padding = spacing.xl,
  backgroundColor = colors.card,
  borderColor = colors.border,
  borderWidth = 1,
  onPress,
  ...props
}) {
  const tokenStyle = shadowTokens?.[shadow] || shadowTokens.card;

  const styleParts = getCardStyleParts(style);
  const contentFlatStyle = StyleSheet.flatten([
    styleParts.content,
    contentStyle,
  ]);

  const resolvedRadius = contentFlatStyle?.borderRadius ?? radius;

  const outerStyle = [
    styles.shadowLayer,
    tokenStyle,
    {
      borderRadius: resolvedRadius,
    },
    styleParts.layout,
    shadowStyle,
  ];

  const pressableStyle = ({ pressed }) => [
    outerStyle,
    pressed && styles.pressed,
  ];

  const content = (
    <View
      style={[
        styles.contentLayer,
        {
          borderRadius: resolvedRadius,
          padding,
          backgroundColor,
          borderColor,
          borderWidth,
        },
        styleParts.content,
        contentStyle,
      ]}
    >
      {children}
    </View>
  );

  if (onPress) {
    return (
      <Pressable {...props} onPress={onPress} style={pressableStyle}>
        {content}
      </Pressable>
    );
  }

  return (
    <View {...props} style={outerStyle}>
      {content}
    </View>
  );
}

const styles = StyleSheet.create({
  shadowLayer: {
    overflow: 'visible',
  },
  contentLayer: {
    overflow: 'hidden',
  },
  pressed: {
    opacity: 0.9,
  },
});

function getCardStyleParts(style) {
  const flatStyle = StyleSheet.flatten(style);

  if (!flatStyle) return { layout: null, content: null };

  const keys = [
    'width',
    'minWidth',
    'maxWidth',
    'height',
    'minHeight',
    'maxHeight',
    'flex',
    'flexBasis',
    'flexGrow',
    'flexShrink',
    'alignSelf',
    'aspectRatio',
    'margin',
    'marginTop',
    'marginRight',
    'marginBottom',
    'marginLeft',
    'marginHorizontal',
    'marginVertical',
    'position',
    'top',
    'right',
    'bottom',
    'left',
    'zIndex',
    'transform',
  ];

  const layoutStyle = {};
  const contentStyle = { ...flatStyle };

  keys.forEach((key) => {
    if (flatStyle[key] !== undefined) {
      layoutStyle[key] = flatStyle[key];
      delete contentStyle[key];
    }
  });

  return { layout: layoutStyle, content: contentStyle };
}