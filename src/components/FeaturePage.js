import { ScrollView, View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import FairyBackButton from './FairyBackButton';
import FairyButton from './FairyButton';
import FairyCard from './FairyCard';
import FairyIllustration from './FairyIllustration';
import FairyTag from './FairyTag';

export default function FeaturePage({
  title,
  subtitle,
  eyebrow,
  scene = 'cover',
  tag,
  heroTitle,
  heroText,
  sections = [],
  primaryAction,
  secondaryAction,
}) {
  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      {eyebrow ? <Text style={styles.eyebrow}>{eyebrow}</Text> : null}
      <Text style={styles.title}>{title}</Text>
      {subtitle ? <Text style={styles.subtitle}>{subtitle}</Text> : null}

      <FairyCard style={styles.hero}>
        <FairyIllustration scene={scene} height={142} />
        {tag ? <FairyTag tone={tag.tone}>{tag.label}</FairyTag> : null}
        <Text style={styles.heroTitle}>{heroTitle || title}</Text>
        {heroText ? <Text style={styles.heroText}>{heroText}</Text> : null}
      </FairyCard>

      {sections.map((section) => (
        <FairyCard key={section.title} style={styles.sectionCard}>
          <View style={styles.sectionHeader}>
            <View style={styles.iconWrap}>
              <Ionicons name={section.icon || 'sparkles-outline'} size={20} color={colors.accent} />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.sectionTitle}>{section.title}</Text>
              {section.text ? <Text style={styles.sectionText}>{section.text}</Text> : null}
            </View>
            {section.badge ? <FairyTag>{section.badge}</FairyTag> : null}
          </View>
        </FairyCard>
      ))}

      {primaryAction ? <FairyButton title={primaryAction} style={styles.action} /> : null}
      {secondaryAction ? <FairyButton title={secondaryAction} variant="secondary" /> : null}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 44 },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  hero: { backgroundColor: colors.cardPink, marginBottom: 18 },
  heroTitle: { color: colors.text, fontSize: 22, fontWeight: '900', marginTop: 12 },
  heroText: { color: colors.textSoft, marginTop: 8, lineHeight: 22 },
  sectionCard: { marginBottom: 14 },
  sectionHeader: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  iconWrap: { width: 42, height: 42, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  sectionTitle: { color: colors.text, fontWeight: '900', fontSize: 15 },
  sectionText: { color: colors.textSoft, marginTop: 4, fontSize: 12, lineHeight: 18 },
  action: { marginTop: 8, marginBottom: 12 },
});
