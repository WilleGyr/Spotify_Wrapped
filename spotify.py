import sys
from collections import Counter
import math
from spotify_utils import getGoogleSeet, load_csv_to_dict, write, duplicates
from credentials import SPREADSHEET_ID

# Download the CSV file from Google Sheets and load it into a dictionary
csv_filepath = getGoogleSeet(SPREADSHEET_ID, '', "spotify.csv")
data_dict = load_csv_to_dict(csv_filepath)

# Count the total number of songs
total_songs = len(data_dict)

# Estimate the total listening time (assuming an average song length of 3.5 minutes)
average_song_length = 3.5
listening_time = math.ceil(average_song_length * total_songs)

# Extract the list of unique artists from the data
unique_artists = [data_dict[i][2] for i in range(total_songs)]

# Count the occurrences of each song
song_counts = Counter([data_dict[i][1] for i in range(total_songs)])

# Count the occurrences of each artist
artist_counts = Counter(unique_artists)

# Find duplicate and unique songs
duplicate_songs, unique_songs = duplicates(data_dict)

# Get the top 10 artists and songs by count
top_artists = artist_counts.most_common(10)
top_songs = [(song, data_dict[next(i for i in data_dict if data_dict[i][1] == song)][2], count) for song, count in song_counts.most_common(10)]

# Write the results to a text file
write(total_songs, unique_songs, unique_artists, listening_time, top_artists, top_songs)

# Exit the program
sys.exit(0)