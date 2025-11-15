// file: app/(tabs)/_layout.tsx
// name: Shanika Paul
// email: shanikap@bu.edu
// date: November 14, 2025
// description: Layout for the navigation tab for all three screens I am building (AddJokes, index, JokesList)

import React from 'react';
import FontAwesome from '@expo/vector-icons/FontAwesome';
import { Tabs } from 'expo-router';
import { useColorScheme } from '@/components/useColorScheme';
import { useClientOnlyValue } from '@/components/useClientOnlyValue';
import Colors from '@/constants/Colors';


function TabBarIcon(props: {
  name: React.ComponentProps<typeof FontAwesome>['name'];
  color: string;
}) {
  return <FontAwesome size={28} style={{ marginBottom: -3 }} {...props} />;
}

export default function TabLayout() {
  const colorScheme = useColorScheme();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        headerShown: useClientOnlyValue(false, true),
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Random',
          tabBarIcon: ({ color }) => <TabBarIcon name="random" color={color} />,
        }}
      />
      <Tabs.Screen
        name="jokes_list"
        options={{
          title: 'All Jokes',
          tabBarIcon: ({ color }) => <TabBarIcon name="list" color={color} />,
        }}
      />
      <Tabs.Screen
        name="add_joke"
        options={{
          title: 'Add Joke',
          tabBarIcon: ({ color }) => <TabBarIcon name="plus-circle" color={color} />,
        }}
      />
    </Tabs>
  );
}