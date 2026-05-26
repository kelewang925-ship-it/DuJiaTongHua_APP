import { Tabs } from 'expo-router';
import FairyTabBar from '../../src/components/FairyTabBar';

export default function TabsLayout() {
  return (
    <Tabs
      tabBar={(props) => <FairyTabBar {...props} />}
      screenOptions={{
        headerShown: false,
      }}
    >
      <Tabs.Screen name="index" options={{ title: '首页' }} />
      <Tabs.Screen name="couple" options={{ title: '情侣空间' }} />
      <Tabs.Screen name="workshop" options={{ title: '童话工坊' }} />
      <Tabs.Screen name="mine" options={{ title: '我的' }} />
    </Tabs>
  );
}
