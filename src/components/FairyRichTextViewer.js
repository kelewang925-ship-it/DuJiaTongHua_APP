import { StyleSheet, Text, View } from 'react-native';
import colors from '../theme/colors';
import { richTextToPlainText } from '../utils/richText';

const stripTags = (html) => richTextToPlainText(html || '');

const parseInline = (html, baseStyle) => {
  const parts = [];
  const pattern = /<(strong|b|em|i|u|s|strike|del)>(.*?)<\/\1>/gis;
  let lastIndex = 0;
  let match;

  while ((match = pattern.exec(html))) {
    if (match.index > lastIndex) {
      parts.push({ text: stripTags(html.slice(lastIndex, match.index)), style: baseStyle });
    }

    const tag = match[1].toLowerCase();
    const tagStyle = {
      strong: styles.bold,
      b: styles.bold,
      em: styles.italic,
      i: styles.italic,
      u: styles.underline,
      s: styles.strike,
      strike: styles.strike,
      del: styles.strike,
    }[tag];

    parts.push({ text: stripTags(match[2]), style: [baseStyle, tagStyle] });
    lastIndex = pattern.lastIndex;
  }

  if (lastIndex < html.length) {
    parts.push({ text: stripTags(html.slice(lastIndex)), style: baseStyle });
  }

  return parts.filter((part) => part.text.length > 0);
};

const normalizeList = (html, tagName, markerForIndex) =>
  html.replace(new RegExp(`<${tagName}[^>]*>([\\s\\S]*?)<\\/${tagName}>`, 'gi'), (_, listContent) => {
    let index = 0;
    const lines = listContent.replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, (_, itemContent) => {
      index += 1;
      return `\n${markerForIndex(index)} ${itemContent.trim()}`;
    });

    return `\n${lines}\n`;
  });

const normalizeHtml = (html) =>
  normalizeList(normalizeList(html || '', 'ol', (index) => `${index}.`), 'ul', () => '-')
    .replace(/<blockquote[^>]*>([\s\S]*?)<\/blockquote>/gi, '\n> $1\n')
    .replace(/<div[^>]*>/gi, '\n')
    .replace(/<\/div>/gi, '\n')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n')
    .replace(/<p[^>]*>/gi, '')
    .replace(/<img[^>]*alt="([^"]*)"[^>]*>/gi, '[图片: $1]')
    .replace(/<img[^>]*>/gi, '[图片]');

export default function FairyRichTextViewer({ html, fallback, style, textStyle }) {
  const source = normalizeHtml(html || fallback || '');
  const lines = source.split(/\n+/).filter((line) => line.trim().length > 0);

  if (!lines.length) {
    return <Text style={[styles.paragraph, textStyle, style]}>{fallback}</Text>;
  }

  return (
    <View style={style}>
      {lines.map((line, index) => {
        const trimmed = line.trim();
        const isQuote = trimmed.startsWith('&gt; ') || trimmed.startsWith('> ');
        const isBullet = trimmed.startsWith('- ');
        const isNumbered = /^\d+\.\s/.test(trimmed);
        const content = trimmed
          .replace(/^(&gt;|>)\s/, '')
          .replace(/^-\s/, '')
          .replace(/^\d+\.\s/, '');

        return (
          <View key={`${trimmed}-${index}`} style={[styles.line, isQuote && styles.quoteLine]}>
            {isBullet ? <Text style={[styles.marker, textStyle]}>•</Text> : null}
            {isNumbered ? <Text style={[styles.marker, textStyle]}>{`${trimmed.match(/^\d+/)?.[0]}.`}</Text> : null}
            <Text style={[styles.paragraph, textStyle, isQuote && styles.quoteText]}>
              {parseInline(content, [styles.paragraph, textStyle]).map((part, partIndex) => (
                <Text key={`${part.text}-${partIndex}`} style={part.style}>
                  {part.text}
                </Text>
              ))}
            </Text>
          </View>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  line: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginTop: 10,
  },
  paragraph: {
    flex: 1,
    color: colors.text,
    fontSize: 16,
    lineHeight: 27,
  },
  marker: {
    color: colors.text,
    fontSize: 16,
    lineHeight: 27,
    marginRight: 8,
  },
  bold: {
    fontWeight: '900',
  },
  italic: {
    fontStyle: 'italic',
  },
  underline: {
    textDecorationLine: 'underline',
  },
  strike: {
    textDecorationLine: 'line-through',
  },
  quoteLine: {
    borderLeftWidth: 3,
    borderLeftColor: colors.secondary,
    paddingLeft: 10,
  },
  quoteText: {
    color: colors.textSoft,
  },
});
