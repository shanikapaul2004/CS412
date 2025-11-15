// file: app/(tabs)/add_joke.tsx
// name: Shanika Paul
// email: shanikap@bu.edu
// date: November 14, 2025
// description: Add Joke screen with form to POST new jokes to Django REST API.

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { styles } from '../../assets/my_styles';

const API_BASE_URL = 'https://cs-webapps.bu.edu/shanikap/dadjokes/api';

export default function AddJokeScreen() {
  const [jokeText, setJokeText] = useState('');
  const [contributor, setContributor] = useState('');
  const [isPosting, setIsPosting] = useState(false);
  const [error, setError] = useState('');

  const addJoke = async () => {
    if (!jokeText.trim() || !contributor.trim()) {
      setError('Please fill in both fields');
      return;
    }

    setIsPosting(true);
    setError('');

    try {
      console.log('Posting joke to API...');
      const response = await fetch(`${API_BASE_URL}/jokes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: jokeText,
          contributor: contributor,
        }),
      });

      console.log('Response status:', response.status);
      
      if (response.ok) {
        const newJoke = await response.json();
        console.log('New joke created:', newJoke);
        
        Alert.alert('Success!', 'Your joke has been added!');
        setJokeText('');
        setContributor('');
      } else {
        setError('Failed to add joke. Please try again.');
      }
    } catch (error) {
      console.error('Error adding joke:', error);
      setError('Failed to add joke. Check your connection.');
    } finally {
      setIsPosting(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.titleText}>Add a New Joke</Text>

      {error ? <Text style={styles.errorText}>{error}</Text> : null}

      <TextInput
        style={styles.input}
        placeholder="Your Name / Username"
        value={contributor}
        onChangeText={setContributor}
        editable={!isPosting}
      />

      <TextInput
        style={[styles.input, styles.textArea]}
        placeholder="Enter your joke here..."
        value={jokeText}
        onChangeText={setJokeText}
        multiline
        numberOfLines={4}
        editable={!isPosting}
      />

      <TouchableOpacity
        style={[styles.button, isPosting && styles.buttonDisabled]}
        onPress={addJoke}
        disabled={isPosting}
      >
        <Text style={styles.buttonText}>
          {isPosting ? 'Adding...' : 'Add Joke'}
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}