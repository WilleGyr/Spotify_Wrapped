import os
import requests
import sys
import csv

# Function to download a Google Sheet as a CSV file
def getGoogleSeet(SPREADSHEET_ID, outDir, outFile):
    url = f'https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv'
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(outDir, outFile)
        with open(filepath, 'wb') as f:
            f.write(response.content)
            print('CSV file saved to: {}'.format(filepath))
        return filepath
    else:
        print(f'Error downloading Google Sheet: {response.status_code}')
        sys.exit(1)

# Function to load a CSV file into a dictionary
def load_csv_to_dict(filepath):
    data = {}
    with open(filepath, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            data[i] = row
    return data

# Function to write Spotify statistics to a text file
def write(total_songs, unique_songs, unique_artists, listening_time, top_artists, top_songs):
    with open('Spotify_Stats.txt', 'w', encoding='utf-8') as f:
        f.write(f'----- Spotify Wrapped -----\n\nStats:\n')
        f.write(f'Total listenings: {total_songs}\n')
        f.write(f'Unique songs: {len(unique_songs)}\n')
        f.write(f'Unique artists: {len(set(unique_artists))}\n')
        f.write(f'Total listening time: {listening_time} minutes\n')
        f.write('\n')
        f.write('Top 10 artists:\n')
        num = 1
        for artist, count in top_artists:
            f.write(f'{num}. {artist}: {count}\n')
            num += 1
        f.write('\n')
        f.write('Top 10 songs:\n')
        num = 1
        for song, artist, count in top_songs:
            f.write(f'{num}. {song} ({artist}): {count}\n')
            num += 1

# Function to find duplicate songs in the data dictionary
def duplicates(data_dict):
    # Initialize a set to track unique elements
    unique_songs = set()
    duplicate_songs = []
    for i in data_dict:
        element = data_dict[i][1]
        if element in unique_songs:
            duplicate_songs.append(element)
        else:
            unique_songs.add(element)

    return duplicate_songs, unique_songs