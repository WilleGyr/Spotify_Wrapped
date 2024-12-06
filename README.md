![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/WilleGyr/Spotify_Wrapped?label=Total%20commits&color=%2313A15C) [![made-with-python](https://img.shields.io/badge/Language-Python%203.12.4-1f425f.svg?logo=python)](https://www.python.org/)

# Spotify Wrapped

Tracks and analyzes your Spotify listening data and creates a custom Spotify Wrapped for you.
<br>
<br>

## Getting Started
### Installation
1. Make sure you have **[Python](https://www.python.org/downloads/)** installed
2. Install **[pandas](https://pandas.pydata.org/)** by running `pip install pandas` in the terminal
3. **Google Sheet** connected to your **Spotify account** through **[this IFTTT applet](https://ifttt.com/applets/nin7BxVm-keep-a-log-of-your-recently-played-tracks)**. (**Guide below**)
<br>

### Usage
1. Run `spotify.py`
2. The script will download your Spotify data from the Google Sheet, analyze it, and generate two files:
    - **spotify.csv**: A CSV file containing your Spotify listening data.
    - **Spotify_Stats.txt**: A text file summarizing your Spotify Wrapped statistics.
3. Open `Spotify_Stats.txt` to view your personalized Spotify Wrapped summary.
<br>

### Google Sheet Setup
1. Sign up and connect **[this IFTTT applet](https://ifttt.com/applets/nin7BxVm-keep-a-log-of-your-recently-played-tracks)** to your Spotify account and Google Drive.
2. Wait for the applet to create your Google Sheet (may take up to an hour) and make the sheet public for those with access to the link.
3. Find your **SPREADSHEET_ID** from the Google Sheets url:<br>
h<span>ttps://docs.goo</span>gle.com/spreadsheets/d/**SPREADSHEET_ID**/edit?gid=0#gid=0
4. Paste your **SPREADSHEET_ID** into the `credentials.py`
<br>

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.