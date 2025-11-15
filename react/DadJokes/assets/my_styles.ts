// file: assets/my_styles.ts
// name: Shanika Paul
// email: shanikap@bu.edu
// date: November 14, 2025
// description: Stylesheet for all of the shared screens in DadJokes.

import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
    padding: 16,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5F5F5',
  },
  titleText: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginVertical: 20,
    color: '#333',
  },
  jokeCard: {
    backgroundColor: '#FFFFFF',
    padding: 20,
    borderRadius: 12,
    marginVertical: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  jokeText: {
    fontSize: 18,
    lineHeight: 26,
    color: '#333',
    marginBottom: 10,
  },
  contributorText: {
    fontSize: 14,
    fontStyle: 'italic',
    color: '#666',
    textAlign: 'right',
  },
  pictureContainer: {
    alignItems: 'center',
    marginVertical: 20,
  },
  picture: {
    width: 300,
    height: 300,
    borderRadius: 12,
    resizeMode: 'cover',
  },
  input: {
    height: 50,
    borderColor: '#DDD',
    borderWidth: 1,
    marginBottom: 16,
    paddingHorizontal: 12,
    borderRadius: 8,
    backgroundColor: '#FFF',
    fontSize: 16,
  },
  textArea: {
    height: 120,
    textAlignVertical: 'top',
    paddingTop: 12,
  },
  button: {
    backgroundColor: '#007AFF',
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonDisabled: {
    backgroundColor: '#CCC',
  },
  buttonText: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
  errorText: {
    color: '#D8000C',
    fontSize: 16,
    textAlign: 'center',
    backgroundColor: '#FFC0CB',
    padding: 12,
    borderRadius: 8,
    marginVertical: 10,
  },
  listItem: {
    backgroundColor: '#FFF',
    padding: 16,
    borderRadius: 8,
    marginBottom: 12,
  },
});