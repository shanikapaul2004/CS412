// file: app/(tabs)/index.tsx
// name: Shanika Paul
// email: shanikap@bu.edu
// date: November 14, 2025
// description: Random screen that displays a random joke and picture fetched from Django REST API.

import React, { useState, useEffect } from 'react';
import { View, Text, Image, ActivityIndicator, ScrollView, RefreshControl } from 'react-native';
import { styles } from '../../assets/my_styles';

const API_BASE_URL = 'https://cs-webapps.bu.edu/shanikap/dadjokes/api';

interface Joke {
  id: number;
  text: string;
  contributor: string;
  created_at: string;
}

interface Picture {
  id: number;
  image_url: string;
  contributor: string;
  created_at: string;
}

export default function IndexScreen() {
  const [joke, setJoke] = useState<Joke | null>(null);
  const [picture, setPicture] = useState<Picture | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState('');

  const fetchData = async () => {
    try {
      // Fetch random joke
      const jokeResponse = await fetch(`${API_BASE_URL}/random`);
      const jokeData = await jokeResponse.json();
      setJoke(jokeData);

      // Fetch random picture
      const pictureResponse = await fetch(`${API_BASE_URL}/random_picture`);
      const pictureData = await pictureResponse.json();
      setPicture(pictureData);

      setError('');
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Failed to fetch data');
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchData();
  };

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#0000ff" />
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <Text style={styles.titleText}>Dad Jokes</Text>

      {error ? (
        <Text style={styles.errorText}>{error}</Text>
      ) : (
        <>
          {joke && (
            <View style={styles.jokeCard}>
              <Text style={styles.jokeText}>{joke.text}</Text>
              <Text style={styles.contributorText}>- {joke.contributor}</Text>
            </View>
          )}

          {picture && (
            <View style={styles.pictureContainer}>
              <Image
                source={{ uri: picture.image_url }}
                style={styles.picture}
              />
              <Text style={styles.contributorText}>
                Picture by: {picture.contributor}
              </Text>
            </View>
          )}
        </>
      )}
    </ScrollView>
  );
}