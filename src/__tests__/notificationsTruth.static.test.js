import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'app/notifications/index.js'), 'utf8');
const store = fs.readFileSync(path.join(process.cwd(), 'src/store/useFairyStore.js'), 'utf8');

describe('notifications real-data truth guards', () => {
  test('unknown backend notification types are not relabeled as interaction', () => {
    expect(source).toContain("return '其他';");
    expect(source).not.toContain(": '互动',\n    read:");
  });

  test('missing subjects and timestamps stay absent instead of receiving story copy', () => {
    expect(source).toContain("subject: item.targetType || ''");
    expect(source).toContain("if (!value) return '';");
    expect(source).not.toContain("item.targetType || '互动消息'");
  });

  test('non-navigable real notices do not display a false navigation affordance', () => {
    expect(source).toContain("item.target ? <Ionicons");
    expect(source).toContain('仅通知');
  });

  test('loading state does not claim the inbox is fully read', () => {
    expect(source).toContain('!loading && !loadError ? <View style={styles.intro}>');
    expect(source).toContain('当前没有未读通知');
  });

  test('mark-all avoids a backend write when nothing is unread', () => {
    expect(source).toContain('if (!unreadCount)');
    expect(source).toContain('暂时没有新的未读通知。');
  });

  test('loads current-user notifications when the real notification page opens', () => {
    expect(source).toContain('const refreshNotifications = useFairyStore((state) => state.refreshNotifications)');
    expect(source).toContain('if (isReal) refreshNotifications();');
    expect(source).toContain('onRetry={refreshNotifications}');
    expect(store).toContain('refreshNotifications: async () =>');
    expect(store).toContain('notifications: result.data || []');
  });
});
