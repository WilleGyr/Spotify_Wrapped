import os, requests, sys, csv, math, spotipy
from collections import Counter, defaultdict
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import CLIENT_ID, CLIENT_SECRET
from tqdm import tqdm

# Function to download a Google Sheet as a CSV file
def getGoogleSeet(SPREADSHEET_ID, outDir, outFile):
    # Construct the URL to export the Google Sheet as a CSV file
    url = f'https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv'
    response = requests.get(url)  # Send a GET request to the URL
    
    if response.status_code == 200:
        # If the request is successful, construct the file path
        filepath = os.path.join(outDir, outFile)
        # Open the file in write-binary mode and save the content
        with open(filepath, 'wb') as f:
            f.write(response.content)
            print('CSV file saved to: {}'.format(filepath))
        return filepath  # Return the file path
    else:
        # If the request fails, print an error message and exit
        print(f'Error downloading Google Sheet: {response.status_code}')
        sys.exit(1)

# Function to load a CSV file into a dictionary
def load_csv_to_dict(filepath):
    data = {}  # Initialize an empty dictionary to store the data
    with open(filepath, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)  # Create a CSV reader object
        for i, row in enumerate(csv_reader):
            data[i] = row  # Add each row to the dictionary with the index as the key
    return data  # Return the populated dictionary

def genre_finder(data_dict):
    progress_bar = tqdm(total=100, desc="Calculating genre counts", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    genres = []
    artist_genres = {}

    # Count the total number of songs
    total_songs = len(data_dict)
    
    # Extract the list of unique artists from the data
    unique_artists = list(set(data_dict[i][2] for i in range(total_songs)))
    
    for i in unique_artists:
        artist = i
        results = sp.search(q=f'artist:{artist}', type='artist', limit=1)
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            genres = artist['genres']
            artist_genres[i] = genres
        progress_bar.update(100/len(unique_artists))
    
    # Create a dictionary to store genre counts
    genre_counts = defaultdict(int)
    
    # Iterate through artist_genres and update genre counts
    for artist, genres in artist_genres.items():
        # Find the number of times the artist has been listened to
        listen_count = sum(1 for i in range(total_songs) if data_dict[i][2] == artist)
        for genre in genres:
            genre_counts[genre] += listen_count
    
    # Sort the dictionary by values
    sorted_genre_counts = dict(sorted(genre_counts.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_genre_counts

# Function to write Spotify statistics to a text file
def write(data_dict, sorted_genre_counts, total_songs, unique_songs, unique_artists, listening_time, top_artists, top_songs, type='Yearly', year=str(datetime.now().year)):
    with open('Spotify_Wrapped.txt', 'a', encoding='utf-8') as f:
        # Write the header based on the type of specification
        if type == 'Yearly':
            f.write(f'----- {type} -----\n\nStats:\n')
        elif type.isdigit():
            f.write(f'----- Yearly {type} -----\n\nStats:\n')
        else:
            f.write(f'----- {type} {year} -----\n\nStats:\n')
        
        # Write stats
        f.write(f'Total listenings: {total_songs}\n')                   # Write the total number of listenings
        f.write(f'Unique songs: {len(unique_songs)}\n')                 # Write the number of unique songs
        f.write(f'Unique artists: {len(set(unique_artists))}\n')        # Write the number of unique artists
        if type == 'Yearly':
            f.write(f'Total listening time: {duration_check(data_dict, 1)} minutes\n\n')    # Write the total listening time in minutes
        else:
            f.write(f'Total listening time: {duration_check(data_dict)} minutes\n\n')    # Write the total listening time in minutes

        # Write the top 10 artists
        f.write('Top 10 artists:\n')
        num = 1
        for artist, count in top_artists:
            f.write(f'{num}. {artist}: {count}\n')
            num += 1
        f.write('\n')
        
        # Write the top 10 songs
        f.write('Top 10 songs:\n')
        num = 1
        for song, artist, count in top_songs:
            f.write(f'{num}. {song} ({artist}): {count}\n')
            num += 1
        f.write('\n')

        if type == "Yearly":
            num = 1
            # Write the sorted genre counts
            f.write('\nTop genres:\n')
            for genre, count in list(sorted_genre_counts.items())[:10]:
                f.write(f'{num}. {genre}: {count}\n')
                num += 1
            f.write('\n')
        f.write('\n')

# Function to find duplicate songs in the data dictionary
def duplicates(data_dict):
    unique_songs = set()  # Track unique elements
    duplicate_songs = []  # Track duplicate elements
    
    for i in data_dict:
        element = data_dict[i][1]  # Get the second element of the value
        
        if element in unique_songs:
            duplicate_songs.append(element)  # Add to duplicates if already in unique_songs
        else:
            unique_songs.add(element)  # Add to unique_songs if not already present

    return duplicate_songs, unique_songs

# Function to calculate Spotify Wrapped statistics for a specific year
def yearly_wrapped(data_dict, sorted_genre_counts, year, write_year=None):
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
    write(data_dict, sorted_genre_counts, total_songs, unique_songs, unique_artists, listening_time, top_artists, top_songs,"Yearly", write_year)

# Function to calculate Spotify Wrapped statistics for a specific month
def monthly_wrapped(month, year, data_dict, sorted_genre_counts):
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
    write(month_data, sorted_genre_counts, total_songs, unique_songs, unique_artists, listening_time, top_artists, top_songs, month, year)

# Function to wrap the monthly and yearly functions
def wrapped(data_dict, first=None, second=None):
    sorted_genre_counts = genre_finder(data_dict)
    # If only a year is given
    if first and first.isdigit() and second == None:
        yearly_wrapped(data_dict, sorted_genre_counts, first, first)

    # If only a month is given
    elif first and second == None:
        monthly_wrapped(first, str(datetime.now().year), data_dict, sorted_genre_counts)
    
    # If both a month and year are given
    elif first and not first.isdigit() and second and second.isdigit():
        monthly_wrapped(first, second, data_dict, sorted_genre_counts)
    elif first and first.isdigit() and second and not second.isdigit():
        monthly_wrapped(second, first, data_dict, sorted_genre_counts)
    
    # If neither a month nor year are given
    elif first == None and second == None:
        yearly_wrapped(data_dict, sorted_genre_counts, str(datetime.now().year), str(datetime.now().year))
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        progress_bar = tqdm(total=100, desc="Writing results to CSV file", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")
        for month in months:
            monthly_wrapped(month, str(datetime.now().year), data_dict, sorted_genre_counts)
            progress_bar.update(100/12)
    
    # If invalid arguments are given
    else:
        print('Invalid arguments')
        sys.exit(1)

def duration_check(data_dict, bool=0):
    if bool:
        progress_bar = tqdm(total=100, desc="Calculating total listening time", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")
    
    track_ids = [data_dict[i][3] for i in data_dict]
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Split track_ids into chunks of 50 (maximum allowed by Spotify API)
    chunks = [track_ids[i:i + 50] for i in range(0, len(track_ids), 50)]
    
    duration_ms = 0
    for chunk in chunks:
        track_uris = ["spotify:track:" + track_id for track_id in chunk]
        track_infos = sp.tracks(track_uris)
        
        for track_info in track_infos['tracks']:
            duration_ms += track_info.get('duration_ms', 0)
        if bool:
            progress_bar.update(100/len(chunks))
    
    duration_ms = duration_ms // 60000
    
    return duration_ms