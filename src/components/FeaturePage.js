import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import FairyButton from './FairyButton';
import FairyCard from './FairyCard';
import FairyHeader from './FairyHeader';
import FairyIllustration from './FairyIllustration';
import FairyPage from './FairyPage';
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
    <FairyPage>
      <FairyHeader showBack eyebrow={eyebrow} title={title} subtitle={subtitle} />

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
    </FairyPage>
  );
}

const styles = StyleSheet.create({
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
