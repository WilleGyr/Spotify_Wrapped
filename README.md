![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/WilleGyr/Spotify_Wrapped?label=Total%20commits&color=%2313A15C) [![made-with-python](https://img.shields.io/badge/Language-Python%203.12.4-1f425f.svg?logo=python)](https://www.python.org/)

# Spotify Wrapped

Tracks and analyzes your Spotify listening data and creates a custom Spotify Wrapped for you.

## Installation
1. Make sure you have **[Python](https://www.python.org/downloads/)** installed
2. Install **[pandas](https://pandas.pydata.org/)** by running `pip install pandas` in the terminal
3. **[Google Sheet](https://workspace.google.com/products/drive/)** connected to your **[Spotify account](https://open.spotify.com/)** through **[this IFTTT applet](https://ifttt.com/applets/nin7BxVm-keep-a-log-of-your-recently-played-tracks)**. (**Guide below**)
4. 

## Spreadsheet Setup
1. Sign up and connect **[this IFTTT applet](https://ifttt.com/applets/nin7BxVm-keep-a-log-of-your-recently-played-tracks)** to your Spotify account and Google Drive account.
2. Wait for the applet to create your Google Sheet (may take up to an hour) and make the sheet public for those with the link.
3. Find your SPREADSHEET_ID from the Google Sheets link:<br>
h<span>ttps://docs.goo</span>gle.com/spreadsheets/d/**SPREADSHEET_ID**/edit?gid=0#gid=0
4. Paste your SPREADSHEET_ID into the `credentials.py`