import { useMemo, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import FairyCard from '../../components/FairyCard';
import FairyPage from '../../components/FairyPage';
import colors from '../../theme/colors';
import spacing from '../../theme/spacing';
import typography from '../../theme/typography';
import { devComponents } from '../config/devComponents';

function renderPreview(Component, props) {
  const normalizedProps = { ...props };

  if (typeof normalizedProps.children === 'string') {
    normalizedProps.children = <Text style={styles.childText}>{normalizedProps.children}</Text>;
  }

  return <Component {...normalizedProps} />;
}

export default function ComponentLab() {
  const [activeIndex, setActiveIndex] = useState(0);
  const activeItem = devComponents[activeIndex];
  const [propsTextByName, setPropsTextByName] = useState(() =>
    devComponents.reduce((result, item) => {
      result[item.name] = JSON.stringify(item.props || {}, null, 2);
      return result;
    }, {})
  );
  const propsText = propsTextByName[activeItem.name] || '{}';
  const parsed = useMemo(() => {
    try {
      return { props: JSON.parse(propsText), error: '' };
    } catch (error) {
      return { props: activeItem.props || {}, error: error.message };
    }
  }, [activeItem.props, propsText]);
  const ActiveComponent = activeItem.component;

  return (
    <FairyPage
      backgroundName="creamPaper"
      topSpace={32}
      bottomSpace={36}
      contentStyle={styles.content}
      showsVerticalScrollIndicator
    >
      <View style={styles.header}>
        <Text style={styles.kicker}>Component Lab</Text>
        <Text style={styles.title}>组件调试</Text>
        <Text style={styles.description}>选择组件后编辑 JSON props，右侧预览会实时刷新。</Text>
      </View>

      <FairyCard radius={26} padding={0} contentStyle={styles.labPanel}>
        <View>
          <Text style={styles.panelTitle}>组件列表</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.componentList}>
            {devComponents.map((item, index) => {
              const active = index === activeIndex;
              return (
                <Pressable
                  key={item.name}
                  onPress={() => setActiveIndex(index)}
                  style={[styles.componentPill, active && styles.componentPillActive]}
                >
                  <Text style={[styles.componentPillText, active && styles.componentPillTextActive]}>{item.name}</Text>
                </Pressable>
              );
            })}
          </ScrollView>
        </View>

        <View>
          <Text style={styles.panelTitle}>实时预览</Text>
          <View style={styles.previewBox}>{renderPreview(ActiveComponent, parsed.props)}</View>
        </View>

        <View>
          <View style={styles.editorHeader}>
            <Text style={styles.panelTitle}>Props 编辑器</Text>
            <Text style={styles.editorHint}>JSON</Text>
          </View>
          <TextInput
            multiline
            value={propsText}
            onChangeText={(text) =>
              setPropsTextByName((current) => ({
                ...current,
                [activeItem.name]: text,
              }))
            }
            autoCapitalize="none"
            autoCorrect={false}
            spellCheck={false}
            textAlignVertical="top"
            style={[styles.editor, parsed.error && styles.editorError]}
          />
          {parsed.error ? <Text style={styles.errorText}>{parsed.error}</Text> : null}
        </View>
      </FairyCard>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  content: {
    gap: spacing.lg,
  },
  header: {
    marginBottom: spacing.xs,
  },
  kicker: {
    color: colors.accent,
    fontSize: 13,
    fontWeight: '900',
  },
  title: {
    ...typography.title,
    color: colors.text,
    fontWeight: '900',
    marginTop: spacing.xs,
  },
  description: {
    ...typography.body,
    color: colors.textSoft,
    marginTop: spacing.sm,
  },
  labPanel: {
    borderRadius: 26,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: 'rgba(255, 249, 244, 0.94)',
    padding: spacing.lg,
    gap: spacing.lg,
  },
  panelTitle: {
    color: colors.text,
    fontSize: 15,
    fontWeight: '900',
  },
  componentList: {
    gap: spacing.sm,
    paddingTop: spacing.md,
    paddingRight: spacing.md,
  },
  componentPill: {
    minHeight: 40,
    borderRadius: 16,
    paddingHorizontal: spacing.md,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
  },
  componentPillActive: {
    backgroundColor: colors.primary,
    borderColor: colors.primaryDeep,
  },
  componentPillText: {
    color: colors.textSoft,
    fontSize: 13,
    fontWeight: '800',
  },
  componentPillTextActive: {
    color: colors.white,
  },
  previewBox: {
    minHeight: 190,
    borderRadius: 22,
    borderWidth: 1,
    borderStyle: 'dashed',
    borderColor: colors.border,
    backgroundColor: '#FFFDF9',
    padding: spacing.lg,
    justifyContent: 'center',
    marginTop: spacing.md,
  },
  editorHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  editorHint: {
    color: colors.gold,
    fontSize: 12,
    fontWeight: '900',
  },
  editor: {
    minHeight: 220,
    borderRadius: 18,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: '#FFFDF9',
    color: colors.text,
    fontSize: 13,
    lineHeight: 20,
    padding: spacing.md,
    marginTop: spacing.md,
  },
  editorError: {
    borderColor: colors.primaryDeep,
    backgroundColor: '#FFF0F2',
  },
  errorText: {
    color: colors.primaryDeep,
    fontSize: 12,
    fontWeight: '800',
    marginTop: spacing.sm,
  },
  childText: {
    color: colors.text,
    fontSize: 15,
    lineHeight: 23,
  },
});
