import os, requests, sys, csv, math
from collections import Counter
from datetime import datetime

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
def write(total_songs, unique_songs, unique_artists, listening_time, top_artists, top_songs, type='Yearly', year=str(datetime.now().year)):
    with open('Spotify_Stats.txt', 'a', encoding='utf-8') as f:
        if type == 'Yearly':
            f.write(f'----- {type} -----\n\nStats:\n')
        elif type.isdigit():
            f.write(f'----- Yearly {type} -----\n\nStats:\n')
        else:
            f.write(f'----- {type} {year} -----\n\nStats:\n')
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
        f.write('\n\n')

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

def yearly_wrapped(data_dict, year, write_year=None):
    # Filter the data for the specified month and year
    filtered_data = {key: data_dict[key] for key in data_dict if year in data_dict[key][0]}
    
    # Re-index the filtered data starting from 0
    year_data = {index: value for index, (key, value) in enumerate(filtered_data.items())}
    
    # Count the total number of songs
    total_songs = len(year_data)

    # Estimate the total listening time (assuming an average song length of 3.5 minutes)
    average_song_length = 3.5
    listening_time = math.ceil(average_song_length * total_songs)

    # Extract the list of unique artists from the data
    unique_artists = [year_data[i][2] for i in range(total_songs)]

    # Count the occurrences of each song
    song_counts = Counter([year_data[i][1] for i in range(total_songs)])

    # Count the occurrences of each artist
    artist_counts = Counter(unique_artists)

    # Find duplicate and unique songs
    duplicate_songs, unique_songs = duplicates(year_data)

    # Get the top 10 artists and songs by count
    top_artists = artist_counts.most_common(10)
    top_songs = [(song, year_data[next(i for i in year_data if year_data[i][1] == song)][2], count) for song, count in song_counts.most_common(10)]

    # Write the results to a text file
    write(total_songs, unique_songs, unique_artists, listening_time, top_artists, top_songs, write_year)

def monthly_wrapped(month, year, data_dict):
    # Filter the data for the specified month and year
    filtered_data = {key: data_dict[key] for key in data_dict if month in data_dict[key][0] and year in data_dict[key][0]}
    
    # Re-index the filtered data starting from 0
    month_data = {index: value for index, (key, value) in enumerate(filtered_data.items())}
    
    # Count the total number of songs
    total_songs = len(month_data)
    
    # Estimate the total listening time (assuming an average song length of 3.5 minutes)
    average_song_length = 3.5
    listening_time = round(average_song_length * total_songs)

    # Extract the list of unique artists from the data
    unique_artists = [month_data[i][2] for i in range(total_songs)]
    
    # Count the occurrences of each song
    song_counts = Counter([month_data[i][1] for i in range(total_songs)])
    
    # Count the occurrences of each artist
    artist_counts = Counter(unique_artists)
    
    # Find duplicate and unique songs
    duplicate_songs, unique_songs = duplicates(month_data)
    
    # Get the top 10 artists and songs by count
    top_artists = artist_counts.most_common(10)
    top_songs = [(song, month_data[next(i for i in month_data if month_data[i][1] == song)][2], count) for song, count in song_counts.most_common(10)]
    
    # Write the results to a text file
    write(total_songs, unique_songs, unique_artists, listening_time, top_artists, top_songs, month, year)

def wrapped(data_dict, first=None, second=None):
    if first and first.isdigit() and second == None:
        yearly_wrapped(data_dict, first, first)
    elif first and second == None:
        monthly_wrapped(first, str(datetime.now().year), data_dict)
    elif first and not first.isdigit() and second and second.isdigit():
        monthly_wrapped(first, second, data_dict)
    elif first and first.isdigit() and second and not second.isdigit():
        monthly_wrapped(second, first, data_dict)
    elif first == None and second == None:
        yearly_wrapped(data_dict, str(datetime.now().year), str(datetime.now().year))
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        for month in months:
            monthly_wrapped(month, str(datetime.now().year), data_dict)
    else:
        print('Invalid arguments')
        sys.exit(1)