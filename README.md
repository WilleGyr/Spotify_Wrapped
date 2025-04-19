![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/WilleGyr/Spotify_Wrapped?label=Total%20commits&color=%2313A15C) [![made-with-python](https://img.shields.io/badge/Language-Python%203.11.2-1f425f.svg?logo=python)](https://www.python.org/) [![GitHub Release](https://img.shields.io/github/v/release/WilleGyr/Spotify_Wrapped)](https://github.com/WilleGyr/Spotify_Wrapped/releases/tag/v4.0.1)



> ⚠️ **Notice**:  
> This is the README for the experimental **version 6.0.0-beta** (major update with a gui for the application).  
> If you want the latest stable release, please download **v5.0.0** from the [Releases page](https://github.com/yourname/yourrepo/releases) or check out the [Stable branch](https://github.com/WilleGyr/Spotify_Wrapped/tree/stable).

# Spotify Wrapped

This is a small project I'm working on a bit during my free time. It's my own version of Spotify's Wrapped feature, where I have complete control of the stats I want to see.

It basically tracks and analyzes your Spotify listening data and creates a custom Spotify Wrapped for you.

*The **[latest version](https://github.com/WilleGyr/Spotify_Wrapped/releases/latest)** requires a **[Spotify Developer account](https://developer.spotify.com/)**. If you don't have access to one, please download **[version 1.0.0](https://github.com/WilleGyr/Spotify_Wrapped/releases/tag/v1.0.0)**. View the **[CHANGELOG](CHANGELOG)** for more information.

## Table of Contents
- [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Google Sheet Setup](#google-sheet-setup)
    - [Spotipy Setup](#spotipy-setup)
    - [Usage](#usage)
- [Roadmap](#roadmap)
- [License](#license)

## Getting Started
### Installation
1. Make sure you have **[Python 3.11.2](https://www.python.org/downloads/)** installed.<br>
Compatibility with other versions is not guaranteed

2. Install **[Requests](https://pypi.org/project/requests/)**, **[Spotipy](https://spotipy.readthedocs.io/en/2.24.0/)**, **[tqdm](https://github.com/tqdm/tqdm)** and **[matplotlib](https://matplotlib.org/)** by running the following in the command line:
    ```
    $ pip install requests
    $ pip install spotipy
    $ pip install tqdm
    $ pip install matplotlib
    ```
3. **Google Sheet** connected to your **Spotify** account through **[this IFTTT applet](https://ifttt.com/applets/nin7BxVm-keep-a-log-of-your-recently-played-tracks)**. (**Guide below**)
4. An active **[Spotify Developer account](https://developer.spotify.com/)**
 
### Google Sheet Setup
1. Sign up and connect **[this IFTTT applet](https://ifttt.com/applets/nin7BxVm-keep-a-log-of-your-recently-played-tracks)** to your Spotify account and Google Drive.
2. Wait for the applet to create your Google Sheet (may take up to an hour) and make the sheet public for those with access to the link.
3. Find your **SPREADSHEET_ID** from the Google Sheets url:<br>
h<span>ttps://docs.goo</span>gle.com/spreadsheets/d/**SPREADSHEET_ID**/edit?gid=0#gid=0
4. Paste your **SPREADSHEET_ID** into `credentials.py`

### Spotipy Setup
1. Browse to **[Spotify for developers](https://developer.spotify.com/dashboard/applications)**
2. Log in with your Spotify account
3. Click on **'Create an app'** and provide the required information
4. After creation, you see your **CLIENT_ID** and you can click on ‘Show client secret` to unhide your **CLIENT_SECRET**
5. Paste your **CLIENT_ID** and **SECRET_ID** into `credentials.py`

### Usage
1. Run `spotify.py`
2. You will be prompted to specify your wrapped by entering a **month,** **year,** or **month and year** (in any order). Leave blank for complete wrapped for the current year.<br>
Examples:
    ```
    $ March 2024
    $ 2025 January
    $ 2024
    $ July
    ```
3. The script will download your Spotify data from the Google Sheet, analyze it, and generate two files:
    - **spotify.csv**: A CSV file containing your Spotify listening data.
    - **Spotify_Wrapped.txt**: A text file summarizing your Spotify Wrapped statistics.
4. Open `Spotify_Wrapped.txt` to view your personalized Spotify Wrapped summary.

## Roadmap
- [x] Add genre analysis
- [x] Optimize genre calculations
- [x] Add progress bars
- [x] Support multiple spreadsheets
- [ ] Add heatmaps
- [ ] Add playlist maker

## License
Distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.