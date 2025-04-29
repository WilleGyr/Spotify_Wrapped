from spotifywrapped.credentials_loader import load_credentials

creds = load_credentials()
SPREADSHEET_ID = creds["SPREADSHEET_ID"]
CLIENT_ID = creds["CLIENT_ID"]
CLIENT_SECRET = creds["CLIENT_SECRET"]
import os, requests, sys, csv, math, spotipy
from collections import Counter, defaultdict
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials
#from spotifywrapped.credentials import CLIENT_ID, CLIENT_SECRET, SPREADSHEET_ID
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from io import BytesIO
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
import matplotlib as mpl
import matplotlib.pyplot as plt  # Make sure this is also imported!

# Function to download a Google Sheet as a CSV file
def getGoogleSheets(spreadsheet_ids, outDir, outFile):
    if outDir:
        os.makedirs(outDir, exist_ok=True)
    
    filepath = os.path.join(outDir, outFile) if outDir else outFile
    
    with open(filepath, 'w', newline='', encoding='utf-8') as outfile:
        writer = None
        
        for i, SPREADSHEET_ID in enumerate(spreadsheet_ids):
            url = f'https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv'
            response = requests.get(url)
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                reader = csv.reader(content.splitlines())
                
                header = next(reader)
                
                if writer is None:
                    writer = csv.writer(outfile)
                    writer.writerow(header)

                for row in reader:
                    writer.writerow(row)

                print(f'Successfully added data from spreadsheet {i+1}/{len(spreadsheet_ids)}')
            else:
                print(f'Error downloading Google Sheet with ID {SPREADSHEET_ID}: {response.status_code}')
                sys.exit(1)
    
    print('All sheets combined and saved to: {}'.format(filepath))
    return filepath

# Function to load a CSV file into a dictionary
def load_csv_to_dict(filepath):
    data = {}  # Initialize an empty dictionary to store the data
    with open(filepath, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)  # Create a CSV reader object
        for i, row in enumerate(csv_reader):
            data[i] = row  # Add each row to the dictionary with the index as the key
    return data  # Return the populated dictionary

def fetch_artist_image(sp, artist_name, data_dict):
    try:
        # Find the first song for the given artist
        for key, value in data_dict.items():
            song_name = value[1]  # Column 2 = song name
            song_artist = value[2]  # Column 3 = artist name
            if song_artist.lower() == artist_name.lower():
                # Search for the song on Spotify
                results = sp.search(q=f'track:{song_name} artist:{artist_name}', type='track', limit=1)
                tracks = results['tracks']['items']
                if tracks and tracks[0]['album']['images']:
                    return tracks[0]['album']['images'][0]['url']  # Get the first (largest) album image
                break  # Only look for the first match
    except Exception as e:
        print(f"Error fetching image for artist {artist_name}: {e}")
    return None


def fetch_song_image(sp, song_name, artist_name):
    try:
        results = sp.search(q=f'track:{song_name} artist:{artist_name}', type='track', limit=1)
        items = results['tracks']['items']
        if items and items[0]['album']['images']:
            return items[0]['album']['images'][0]['url']
    except Exception:
        pass
    return None

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

def calculate_monthly_listening(data_dict):
    monthly_counts = defaultdict(int)
    for row in data_dict.values():
        if len(row) >= 1:
            date_str = row[0].strip().strip('"')  # Första fältet är datumet
            try:
                dt = datetime.strptime(date_str, "%B %d, %Y at %I:%M%p")
                monthly_counts[dt.month] += 1
            except ValueError:
                pass  # Hoppa över felaktiga datum
    return monthly_counts

def write(data_dict, sorted_genre_counts, total_songs, unique_songs, unique_artists, listening_time, top_artists, top_songs, type='Yearly', year=str(datetime.now().year)):
    creds = load_credentials()
    CLIENT_ID = creds["CLIENT_ID"]
    CLIENT_SECRET = creds["CLIENT_SECRET"]
    mpl.rcParams['text.antialiased'] = True
    os.makedirs('Spotify_Wrapped_Charts', exist_ok=True)

    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # --- Basic Statistics ---
    fig, ax = plt.subplots(figsize=(10.8, 6.6), dpi=100)
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')
    for spine in ax.spines.values():
        spine.set_visible(False)

    stats_labels = ['Total Listenings', 'Unique Songs', 'Unique Artists', 'Total Listening Time (minutes)']
    stats_values = [
        total_songs,
        len(unique_songs),
        len(set(unique_artists)),
        listening_time if type != 'Yearly' else duration_check(data_dict, 1)
    ]

    ax.bar(stats_labels, stats_values, color='#1DB954')
    for i, v in enumerate(stats_values):
        ax.text(i, v + max(stats_values)*0.01, str(v), ha='center', va='bottom', fontsize=9, color='white')

    ax.set_ylabel('Amount', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.title.set_color('white')
    plt.title(f"Spotify {type} Stats {year}")
    plt.xticks(rotation=20)
    ax.grid(False)
    plt.tight_layout()
    plt.savefig(f'Spotify_Wrapped_Charts/{type}_basic_stats.png', dpi=300, facecolor=fig.get_facecolor())
    plt.close()

    # --- Top 10 Artists ---
    if top_artists:
        artists, counts = zip(*top_artists)
        fig, ax = plt.subplots(figsize=(10.8, 6.6), dpi=100)
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        for spine in ax.spines.values():
            spine.set_visible(False)

        y_positions = range(len(artists))[::-1]
        ax.barh(y_positions, counts[::1], color='#1DB954')
        ax.set_yticks([])

        for i, artist in enumerate(artists[::1]):
            y = y_positions[i]
            ax.text(-max(counts)*0.02, y, artist, va='center', ha='right', fontsize=11, color='white')

            img_url = fetch_artist_image(sp, artist, data_dict)
            if img_url:
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content))
                imagebox = OffsetImage(img, zoom=0.05)
                ab = AnnotationBbox(imagebox, (-max(counts)*0.015, y), frameon=False, box_alignment=(0,0.5))
                ax.add_artist(ab)

        for i, v in enumerate(counts[::1]):
            ax.text(v + max(counts)*0.01, y_positions[i], str(v), va='center', fontsize=9, color='white')

        ax.set_xlim(-max(counts)*0.2, max(counts)*1.2)
        ax.xaxis.label.set_color('white')
        #ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='x', bottom=False, labelbottom=False)
        plt.xlabel('Listenings')
        plt.title(f"Top 10 Artists - {type} {year}", color='white')
        ax.grid(False)
        plt.tight_layout()
        plt.savefig(f'Spotify_Wrapped_Charts/{type}_top_artists_with_images.png', dpi=300, facecolor=fig.get_facecolor())
        plt.close()

    # --- Top 10 Songs ---
    if top_songs:
        songs = [f"{song} ({artist})" for song, artist, count in top_songs]
        counts = [count for song, artist, count in top_songs]
        fig, ax = plt.subplots(figsize=(10.8, 6.6), dpi=100)
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        for spine in ax.spines.values():
            spine.set_visible(False)

        y_positions = range(len(songs))[::-1]
        ax.barh(y_positions, counts[::1], color='#1DB954')
        ax.set_yticks([])

        for i, (song_artist, (song_name, artist_name, _)) in enumerate(zip(songs[::1], top_songs[::1])):
            y = y_positions[i]
            ax.text(-max(counts)*0.02, y, song_artist, va='center', ha='right', fontsize=9, color='white')

            img_url = fetch_song_image(sp, song_name, artist_name)
            if img_url:
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content))
                imagebox = OffsetImage(img, zoom=0.05)
                ab = AnnotationBbox(imagebox, (-max(counts)*0.015, y), frameon=False, box_alignment=(0,0.5))
                ax.add_artist(ab)

        for i, v in enumerate(counts[::1]):
            ax.text(v + max(counts)*0.01, y_positions[i], str(v), va='center', fontsize=9, color='white')

        ax.set_xlim(-max(counts)*0.2, max(counts)*1.2)
        ax.xaxis.label.set_color('white')
        #ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='x', bottom=False, labelbottom=False)
        plt.xlabel('Listenings')
        plt.title(f"Top 10 Songs - {type} {year}", color='white')
        ax.grid(False)
        plt.tight_layout()
        plt.savefig(f'Spotify_Wrapped_Charts/{type}_top_songs_with_images.png', dpi=300, facecolor=fig.get_facecolor())
        plt.close()

    # --- Top Genres (if Yearly) ---
    if type == 'Yearly' and sorted_genre_counts:
        genres, counts = zip(*list(sorted_genre_counts.items())[:10])
        fig, ax = plt.subplots(figsize=(10.8, 6.6), dpi=100)
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        for spine in ax.spines.values():
            spine.set_visible(False)

        y_positions = range(len(genres))[::1]
        ax.barh(y_positions, counts[::1], color='#1DB954')
        ax.set_yticks(y_positions)
        ax.set_yticklabels(genres[::1], color='white')

        for i, v in enumerate(counts[::1]):
            ax.text(v + max(counts)*0.01, y_positions[i], str(v), va='center', fontsize=9, color='white')

        ax.xaxis.label.set_color('white')
        #ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='x', bottom=False, labelbottom=False)
        plt.xlabel('Listenings')
        plt.title(f"Top Genres - {year}", color='white')
        ax.grid(False)
        plt.tight_layout()
        plt.savefig(f'Spotify_Wrapped_Charts/{type}_top_genres.png', dpi=300, facecolor=fig.get_facecolor())
        plt.close()

    # --- Listening Activity per Month (if Yearly) ---
    if type == 'Yearly':
        monthly_listening = calculate_monthly_listening(data_dict)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        counts = [monthly_listening.get(i, 0) for i in range(1, 13)]

        fig, ax = plt.subplots(figsize=(10.8, 6.6), dpi=100)
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.plot(months, counts, marker='o', color='white')
        for i, v in enumerate(counts):
            ax.text(i, v + max(counts)*0.02, str(v), ha='center', va='bottom', fontsize=9, color='white')

        ax.set_xlabel('Month', color='white')
        ax.set_ylabel('Listenings', color='white')
        ax.tick_params(axis='both', colors='white')
        plt.title(f"Listening Activity per Month - {year}", color='white')
        ax.grid(False)
        plt.tight_layout()
        plt.savefig(f'Spotify_Wrapped_Charts/{type}_listening_per_month.png', dpi=300, facecolor=fig.get_facecolor())
        plt.close()

# Function to write Spotify statistics to a text file
def write_to_txt(data_dict, sorted_genre_counts, total_songs, unique_songs, unique_artists, listening_time, top_artists, top_songs, type='Yearly', year=str(datetime.now().year)):
    with open('Spotify_Wrapped.txt', 'a', encoding='utf-8') as f:
        # Write the header based on the type of specification
        if type == 'Yearly':
            f.write(f'----- {type} -----\n\nStats:\n')
        elif type.isdigit():
            f.write(f'----- Yearly {type} -----\n\nStats:\n')
        else:
            f.write(f'----- {type} {year} -----\n\nStats:\n')
        
        # Write stats
        f.write(f"Total listenings: {'{:,.0f}'.format(total_songs).replace(',', ' ')}\n")       # Write the total number of listenings
        f.write(f"Unique songs: {'{:,.0f}'.format(len(unique_songs)).replace(',', ' ')}\n")     # Write the number of unique songs
        f.write(f'Unique artists: {len(set(unique_artists))}\n')        # Write the number of unique artists
        if type == 'Yearly':
            f.write(f"Total listening time: {'{:,.0f}'.format(duration_check(data_dict, 1)).replace(',', ' ')} minutes\n\n")    # Write the total listening time in minutes
            # I want to store the days since the beginning of the year
            days = datetime.now().timetuple().tm_yday
            print(f"Predicted total listening time: {'{:,.0f}'.format(round(duration_check(data_dict, 1) / days * 365)).replace(',', ' ')} minutes")
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
            if sorted_genre_counts:
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
    write_to_txt(data_dict, sorted_genre_counts, total_songs, unique_songs, unique_artists, listening_time, top_artists, top_songs,"Yearly", write_year)

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
    write_to_txt(month_data, sorted_genre_counts, total_songs, unique_songs, unique_artists, listening_time, top_artists, top_songs, month, year)

# Function to wrap the monthly and yearly functions
def wrapped(data_dict, first=None, second=None, check_genres=True):
    if check_genres:
        sorted_genre_counts = genre_finder(data_dict)
    else:
        sorted_genre_counts = None

    if first and first.isdigit() and second is None:
        yearly_wrapped(data_dict, sorted_genre_counts, first, first)

    elif first and second is None:
        monthly_wrapped(first, str(datetime.now().year), data_dict, sorted_genre_counts)

    elif first and not first.isdigit() and second and second.isdigit():
        monthly_wrapped(first, second, data_dict, sorted_genre_counts)

    elif first and first.isdigit() and second and not second.isdigit():
        monthly_wrapped(second, first, data_dict, sorted_genre_counts)

    elif first is None and second is None:
        yearly_wrapped(data_dict, sorted_genre_counts, str(datetime.now().year), str(datetime.now().year))
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        progress_bar = tqdm(total=100, desc="Writing results to .txt file", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")
        for month in months:
            monthly_wrapped(month, str(datetime.now().year), data_dict, sorted_genre_counts)
            progress_bar.update(100/12)
        progress_bar.close()

    else:
        print('Invalid arguments')
        sys.exit(1)

def duration_check(data_dict, bool=0):
    track_ids = [data_dict[i][3] for i in data_dict]
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Split track_ids into chunks of 50 (maximum allowed by Spotify API)
    chunks = [track_ids[i:i + 50] for i in range(0, len(track_ids), 50)]

    if bool:
        progress_bar = tqdm(total=len(chunks), desc="Calculating total listening time", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")
    
    duration_ms = 0
    for chunk in chunks:
        track_uris = ["spotify:track:" + track_id for track_id in chunk]
        track_infos = sp.tracks(track_uris)
        
        for track_info in track_infos['tracks']:
            duration_ms += track_info.get('duration_ms', 0)
        
        if bool:
            progress_bar.update(1)

    if bool:
        progress_bar.close()

    duration_ms = duration_ms // 60000
    
    return duration_ms

def populate_months_dropdown(data_dict, dropdown):
    """Populate the dropdown with unique months sorted in calendar order."""
    months = set()
    for entry in data_dict.values():
        # Assuming the date is the first element in the list
        date_str = entry[0] if len(entry) > 0 else None
        if date_str:
            try:
                # Parse the date using the new format
                month = datetime.strptime(date_str, "%B %d, %Y at %I:%M%p").strftime("%B")
                months.add(month)
            except ValueError:
                pass  # Skip invalid date formats

    # Sort months in the order they appear in a year
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    sorted_months = sorted(months, key=lambda m: month_order.index(m))
    dropdown.addItems(sorted_months)

def OnGenerateButtonClicked(window):
    window.WaitLabel.setVisible(True)
    window.DoneLabel.setVisible(False)
    QtWidgets.QApplication.processEvents()

    selected_month = window.MonthsDropdown.currentText()
    print(f"Generating Spotify Wrapped for: {selected_month} 2025")

    # Re-download the CSV
    csv_filepath = getGoogleSheets(SPREADSHEET_ID, '', "spotify.csv")
    data_dict = load_csv_to_dict(csv_filepath)

    # Re-run the wrapped generation
    is_checked = window.GenreCheckBox.isChecked()

    if selected_month == "Whole Year":
        wrapped(data_dict, check_genres=is_checked)
    else:
        wrapped(data_dict, selected_month, "2025", check_genres=is_checked)

    print("Generation complete!")
    window.WaitLabel.setVisible(False)
    window.DoneLabel.setVisible(True)

def update_image_label(window):
    window.ImageLabel.setStyleSheet("""
    QLabel {
        background-color: #121212;
        border: 2px solid #1DB954;
        border-radius: 10px;
        padding: 5px;
        color: white;
        font-size: 16px;
        qproperty-alignment: AlignCenter;
    }
    """)

    directory = 'Spotify_Wrapped_Charts'
    if not os.path.exists(directory):
        window.ImageLabel.setText("Directory does not exist")
        return

    selected_month = window.Vis_MonthDropDown.currentText()
    selected_type = window.Vis_TypeDropDown.currentText()

    type_suffixes = {
        'Basic Stats': 'basic_stats',
        'Top Artists': 'top_artists_with_images',
        'Top Songs': 'top_songs_with_images',
        'Per Month': 'listening_per_month',
        'Top Genres': 'top_genres'
    }

    type_suffix = type_suffixes.get(selected_type, '')

    # If 'Whole Year' selected, use 'Yearly' instead of month
    if selected_month.lower() == 'whole year':
        month_part = 'yearly'
    else:
        month_part = selected_month.lower()

    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    found_file = None

    for file in image_files:
        file_lower = file.lower()
        if month_part in file_lower and type_suffix in file_lower:
            found_file = file
            break

    if found_file:
        image_path = os.path.join(directory, found_file)
        pixmap = QPixmap(image_path)
        window.ImageLabel.setPixmap(pixmap)
        window.ImageLabel.setScaledContents(True)
    else:
        window.ImageLabel.setText(f"No image found for {selected_month} - {selected_type}")

def on_tab_changed(index, window):
    update_month_dropdown(window)
    update_type_dropdown(window)
    if index == 0:  # If it's the first tab (Visuals tab)
        update_image_label(window)

def update_month_dropdown(window):
    window.Vis_MonthDropDown.clear()

    directory = 'Spotify_Wrapped_Charts'
    if not os.path.exists(directory):
        return

    files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    valid_months = set()

    for month in month_names:
        # Find all files containing this month
        month_files = [f for f in files if month.lower() in f.lower()]
        
        if not month_files:
            continue  # No files at all for this month

        # Check if there are files besides Basic Stats
        has_other_types = False
        for f in month_files:
            if not 'basic_stats' in f.lower():
                has_other_types = True
                break
        
        if has_other_types:
            valid_months.add(month)

    # Also check if Whole Year has more than just Basic Stats
    year_files = [f for f in files if 'yearly' in f.lower()]
    has_other_types_year = False
    for f in year_files:
        if not 'basic_stats' in f.lower():
            has_other_types_year = True
            break

    if has_other_types_year:
        window.Vis_MonthDropDown.addItem("Whole Year")

    for month in month_names:
        if month in valid_months:
            window.Vis_MonthDropDown.addItem(month)

def update_type_dropdown(window):
    window.Vis_TypeDropDown.clear()
    window.Vis_TypeDropDown.addItems(["Basic Stats", "Top Artists", "Top Songs"])
    if window.Vis_MonthDropDown.currentText() == "Whole Year":
        window.Vis_TypeDropDown.addItems(["Per Month", "Top Genres"])

def on_dropdown_changed(window):
    update_type_dropdown(window)  # (if you want types to change based on month)
    update_image_label(window)     # always update the image
