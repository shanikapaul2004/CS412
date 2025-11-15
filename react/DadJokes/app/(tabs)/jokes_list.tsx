// file: app/(tabs)/jokes_list.tsx
// name: Shanika Paul
// email: shanikap@bu.edu
// date: November 14, 2025
// description: All Jokes screen that displays a list of all jokes from Django REST API and you can pull-to-refresh.

import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, ActivityIndicator, RefreshControl } from 'react-native';
import { styles } from '../../assets/my_styles';

const API_BASE_URL = 'https://cs-webapps.bu.edu/shanikap/dadjokes/api';

interface Joke {
  id: number;
  text: string;
  contributor: string;
  created_at: string;
}

export default function JokeListScreen() {
  const [jokes, setJokes] = useState<Joke[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState('');

  const fetchJokes = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/jokes`);
      const data = await response.json();
      setJokes(data.results || data);
      setError('');
    } catch (error) {
      console.error('Error fetching jokes:', error);
      setError('Failed to fetch jokes');
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchJokes();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchJokes();
  };

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#0000ff" />
        <Text>Loading jokes...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>All Jokes</Text>
      
      {error ? (
        <Text style={styles.errorText}>{error}</Text>
      ) : (
        <FlatList
          data={jokes}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <View style={styles.listItem}>
              <Text style={styles.jokeText}>{item.text}</Text>
              <Text style={styles.contributorText}>- {item.contributor}</Text>
            </View>
          )}
          ItemSeparatorComponent={() => <View style={{ height: 8 }} />}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
          ListEmptyComponent={
            <Text style={{ textAlign: 'center', marginTop: 20 }}>
              No jokes found
            </Text>
          }
        />
      )}
    </View>
  );
}