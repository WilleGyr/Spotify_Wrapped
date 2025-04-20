[![License: MIT](https://img.shields.io/badge/License-MIT-maroon.svg)](LICENSE) ![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/WilleGyr/Spotify_Wrapped?label=Total%20commits&color=%2313A15C) [![Last Commit](https://img.shields.io/github/last-commit/WilleGyr/Spotify_Wrapped?color=orange&label=Last%20Commit)](https://github.com/WilleGyr/Spotify_Wrapped/commits/main) [![made-with-python](https://img.shields.io/badge/Language-Python%203.11.2-1f425f.svg?logo=python)](https://www.python.org/) [![Release](https://img.shields.io/badge/Release-v6.0.0-blue)](https://github.com/WilleGyr/Spotify_Wrapped/releases/tag/v6.0.0) ![Status](https://img.shields.io/badge/Status-Active-darkgreen.svg)



> ⚠️ **Notice**:  
> This is the README for the experimental **version 6.0.1-beta** (updates to the GUI, including raw data viewer).  
> If you want the latest stable release, please download **v6.0.0** from the [Releases page](https://github.com/WilleGyr/Spotify_Wrapped/releases) or check out the [Stable branch](https://github.com/WilleGyr/Spotify_Wrapped/tree/stable).

# Custom Spotify Wrapped
*Flexible, personal, and fully under your control.*

This is a personal project I've been building during my free time:
a custom version of Spotify's Wrapped feature, fully under my own control.

Instead of being limited to what Spotify chooses to show,
this tool lets me generate and explore exactly the statistics and charts I want —
from top artists and songs to total listening time, monthly trends, and even genre breakdowns.

It basically tracks and analyzes your Spotify listening data and creates a custom Spotify Wrapped for you.

*The **[latest version](https://github.com/WilleGyr/Spotify_Wrapped/releases/latest)** requires a **[Spotify Developer account](https://developer.spotify.com/)**. If you don't have access to one, please download **[version 1.0.0](https://github.com/WilleGyr/Spotify_Wrapped/releases/tag/v1.0.0)**. View the **[CHANGELOG](CHANGELOG)** for more information.

![Alt text](Images/Interface_Showcase.gif)

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

2. Install **[Requests](https://pypi.org/project/requests/)**, **[Spotipy](https://spotipy.readthedocs.io/en/2.24.0/)**, **[tqdm](https://github.com/tqdm/tqdm)**, **[matplotlib](https://matplotlib.org/)** and **[PyQt5](https://pypi.org/project/PyQt5/)** by running the following in the command line:
    ```
    $ pip install requests
    $ pip install spotipy
    $ pip install tqdm
    $ pip install matplotlib
    $ pip install PyQt5
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
1. <b>Run `spotify.py` </b><br>
Launch the program to start.
2. <b>View your Spotify Wrapped graphs</b><br>
On the right side of the window, a graph will be visible immediately.<br>
You can change which graph you want to view using the filters:
    - <b>Time period</b>
        - Any available month
        - Whole year overview
    - <b>Types</b>
        - Basic Stats
        - Top Artists
        - Top Songs
        - Listening Activity per Month (only available for "Whole Year")
        - Top Genres (Only for "Whole Year")
3. <b>Generate new charts</b><br>
To create fresh charts based on the latest data:
    - Select the desired time period.
    - (Optional) Check the box if you want Genre charts included.
    - Click the "Generate" button in the bottom right corner.

## Roadmap
- [x] Add genre analysis
- [x] Optimize genre calculations
- [x] Add progress bars
- [x] Support multiple spreadsheets
- [x] GUI with chart viewer
- [] Genre Explorer
    - [] List of all genres
    - [] Every artist per genre
- [] Raw Data Explorer
    - [] View the whole csv file
    - [] Filter by artist, genres songs and months

## License
Distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.