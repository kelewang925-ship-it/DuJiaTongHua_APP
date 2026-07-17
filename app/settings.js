import { useState } from 'react';
import { Pressable, StyleSheet, Switch, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '../src/components/FairyButton';
import FairyCard from '../src/components/FairyCard';
import FairyDialog from '../src/components/FairyDialog';
import FairyHeader from '../src/components/FairyHeader';
import FairyPage from '../src/components/FairyPage';
import FairyToast from '../src/components/FairyToast';
import baseColors from '../src/theme/colors';
import spacing from '../src/theme/spacing';

const colors = {
  ...baseColors,
  roseDeep: baseColors.primaryDeep,
  roseSoft: baseColors.primary,
  roseMist: baseColors.cardPink,
  textMuted: baseColors.textSoft,
  paper: baseColors.card,
};

const themeOptions = ['月白纸感', '桃粉童话', '奶油暖光'];

function SettingRow({ icon, title, description, onPress, children, isLast = false }) {
  const content = (
    <>
      <View style={styles.iconWrap}>
        <Ionicons name={icon} size={21} color={colors.roseDeep} />
      </View>
      <View style={styles.rowCopy}>
        <Text style={styles.rowTitle}>{title}</Text>
        {description ? <Text style={styles.rowDescription}>{description}</Text> : null}
      </View>
      {children ?? <Ionicons name="chevron-forward" size={19} color={colors.textMuted} />}
    </>
  );
  if (onPress) {
    return (
      <Pressable accessibilityRole="button" onPress={onPress} style={({ pressed }) => [styles.row, !isLast && styles.rowDivider, pressed && styles.rowPressed]}>
        {content}
      </Pressable>
    );
  }
  return <View style={[styles.row, !isLast && styles.rowDivider]}>{content}</View>;
}

function SectionTitle({ children }) {
  return <Text style={styles.sectionTitle}>{children}</Text>;
}

export default function SettingsScreen() {
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [privateSpace, setPrivateSpace] = useState(true);
  const [themeExpanded, setThemeExpanded] = useState(false);
  const [selectedTheme, setSelectedTheme] = useState(themeOptions[0]);
  const [logoutVisible, setLogoutVisible] = useState(false);
  const [toast, setToast] = useState(null);

  const updateTheme = (theme) => {
    setSelectedTheme(theme);
    setToast({ message: `已切换为「${theme}」`, tone: 'success' });
  };

  return (
    <FairyPage backgroundName="creamPaper" topSpace={28} bottomSpace={64}>
      <View style={styles.pageContent}>
        <FairyHeader showBack eyebrow="更多功能" title="设置" subtitle="把这座只属于你们的小小世界，调整成最舒服的样子。" />

        <SectionTitle>账号与关系</SectionTitle>
        <FairyCard style={styles.sectionCard}>
          <SettingRow icon="person-circle-outline" title="账号信息" description="查看绑定方式与个人资料" onPress={() => router.push('/account/couple-info')} />
          <SettingRow icon="heart-circle-outline" title="情侣关系" description="查看你们的专属关系信息" onPress={() => router.push('/account/couple-info')} isLast />
        </FairyCard>

        <SectionTitle>提醒与隐私</SectionTitle>
        <FairyCard style={styles.sectionCard}>
          <SettingRow icon="notifications-outline" title="消息提醒" description="纪念日、互动与故事更新">
            <Switch accessibilityLabel="消息提醒" value={notificationsEnabled} onValueChange={setNotificationsEnabled} trackColor={{ false: colors.border, true: colors.roseSoft }} thumbColor={notificationsEnabled ? colors.roseDeep : colors.paper} />
          </SettingRow>
          <SettingRow icon="lock-closed-outline" title="私密空间" description="仅你和伴侣可以看到故事" isLast>
            <Switch
              accessibilityLabel="私密空间"
              value={privateSpace}
              onValueChange={(value) => {
                setPrivateSpace(value);
                setToast({ message: value ? '已开启双人私密空间' : '已关闭私密空间', tone: 'info' });
              }}
              trackColor={{ false: colors.border, true: colors.roseSoft }}
              thumbColor={privateSpace ? colors.roseDeep : colors.paper}
            />
          </SettingRow>
        </FairyCard>

        <SectionTitle>外观与存储</SectionTitle>
        <FairyCard style={styles.sectionCard}>
          <SettingRow icon="color-palette-outline" title="页面主题" description={selectedTheme} onPress={() => setThemeExpanded((value) => !value)}>
            <Ionicons name={themeExpanded ? 'chevron-up' : 'chevron-down'} size={19} color={colors.textMuted} />
          </SettingRow>
          {themeExpanded ? (
            <View style={styles.themePicker}>
              {themeOptions.map((theme, index) => {
                const active = theme === selectedTheme;
                return (
                  <Pressable key={theme} accessibilityRole="button" onPress={() => updateTheme(theme)} style={({ pressed }) => [styles.themeChip, active && styles.themeChipActive, pressed && styles.rowPressed]}>
                    <View style={[styles.themeDot, styles[`themeDot${index}`]]} />
                    <Text style={[styles.themeChipText, active && styles.themeChipTextActive]}>{theme}</Text>
                    {active ? <Ionicons name="checkmark" size={17} color={colors.roseDeep} /> : null}
                  </Pressable>
                );
              })}
            </View>
          ) : null}
          <SettingRow icon="folder-open-outline" title="存储空间" description="管理缓存与本地内容" onPress={() => router.push('/data/storage')} isLast />
        </FairyCard>

        <SectionTitle>支持</SectionTitle>
        <FairyCard style={styles.sectionCard}>
          <SettingRow icon="cloud-upload-outline" title="数据备份" description="保存和恢复你们的故事" onPress={() => router.push('/data/backup')} />
          <SettingRow icon="help-buoy-outline" title="帮助与反馈" description="常见问题、建议与版本信息" onPress={() => router.push('/help-feedback')} isLast />
        </FairyCard>

        <FairyButton
          variant="secondary"
          title="退出当前账号"
          onPress={() => setLogoutVisible(true)}
          leftContent={<Ionicons name="log-out-outline" size={20} color={colors.roseDeep} />}
          style={styles.logoutButton}
        />
        <Text style={styles.version}>独家童话 · 当前体验版本</Text>
      </View>

      <FairyDialog
        visible={logoutVisible}
        title="要暂时离开吗？"
        message="退出后不会删除本机的故事与设置，下次登录还可以继续回来。"
        confirmText="确认退出"
        cancelText="再等等"
        onCancel={() => setLogoutVisible(false)}
        onConfirm={() => {
          setLogoutVisible(false);
          router.replace('/login');
        }}
      />
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { width: '100%', maxWidth: 720, alignSelf: 'center', paddingHorizontal: spacing.lg },
  sectionTitle: { marginTop: spacing.xl, marginBottom: spacing.sm, marginLeft: spacing.xs, color: colors.textMuted, fontSize: 13, fontWeight: '700', letterSpacing: 1.2 },
  sectionCard: { paddingVertical: 0, paddingHorizontal: spacing.md, overflow: 'hidden' },
  row: { minHeight: 76, flexDirection: 'row', alignItems: 'center', paddingVertical: spacing.md, gap: spacing.md },
  rowDivider: { borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: colors.border },
  rowPressed: { opacity: 0.66 },
  iconWrap: { width: 42, height: 42, borderRadius: 15, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.roseMist },
  rowCopy: { flex: 1, minWidth: 0 },
  rowTitle: { color: colors.text, fontSize: 16, fontWeight: '700' },
  rowDescription: { marginTop: 4, color: colors.textMuted, fontSize: 12, lineHeight: 18 },
  themePicker: { paddingVertical: spacing.md, borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: colors.border, gap: spacing.sm },
  themeChip: { minHeight: 46, flexDirection: 'row', alignItems: 'center', paddingHorizontal: spacing.md, borderRadius: 16, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.paper, gap: spacing.sm },
  themeChipActive: { borderColor: colors.roseSoft, backgroundColor: colors.roseMist },
  themeChipText: { flex: 1, color: colors.textMuted, fontSize: 14, fontWeight: '600' },
  themeChipTextActive: { color: colors.text },
  themeDot: { width: 18, height: 18, borderRadius: 9, borderWidth: 2, borderColor: colors.paper },
  themeDot0: { backgroundColor: '#F7F2E8' },
  themeDot1: { backgroundColor: '#E8A5AF' },
  themeDot2: { backgroundColor: '#E8C88E' },
  logoutButton: { marginTop: spacing.xl },
  version: { marginTop: spacing.md, textAlign: 'center', color: colors.textMuted, fontSize: 12 },
});
