import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';

const tabIcon = (name) => ({ color, size }) => (
  <Ionicons name={name} size={size} color={color} />
);

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: colors.primaryDeep,
        tabBarInactiveTintColor: colors.text,
        tabBarStyle: {
          backgroundColor: '#FFFAF8',
          borderTopWidth: 0,
          height: 78,
          paddingTop: 8,
          paddingBottom: 12,
          shadowColor: colors.accent,
          shadowOpacity: 0.12,
          shadowRadius: 16,
          shadowOffset: { width: 0, height: -4 },
          elevation: 12,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '700',
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: '首页',
          tabBarIcon: tabIcon('book-outline'),
        }}
      />
      <Tabs.Screen
        name="couple"
        options={{
          title: '情侣空间',
          tabBarIcon: tabIcon('heart-outline'),
        }}
      />
      <Tabs.Screen
        name="workshop"
        options={{
          title: '童话工坊',
          tabBarIcon: tabIcon('sparkles-outline'),
        }}
      />
      <Tabs.Screen
        name="mine"
        options={{
          title: '我的',
          tabBarIcon: tabIcon('person-outline'),
        }}
      />
    </Tabs>
  );
}
