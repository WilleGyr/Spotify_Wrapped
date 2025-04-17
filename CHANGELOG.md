# Change Log
All notable changes to this project will be documented in this file.

## [3.0.1] - 2025-04-17

### Changed
- Fixed a bug with tqdm, where an error would appear in the terminal. The listening time progress bars now take the actual amount of iterations into the calculation instead of defaulting to 100.

## [3.0.0] - 2025-04-17

### Added
- Support for multiple spreadsheets, by passing a list of SPREADSHEET_ID's.

## [2.0.0] - 2024-12-12

### Added
- Functions that analyze finds the artist of each song listened to, find the artist's genres and then lists the top 10 most listened to genres.

## [1.1.0] - 2024-12-07

### Changed
- Now calculates the listening minutes by finding each song's exact duration using the **[Spotify Web API](https://developer.spotify.com/documentation/web-api)**. In the prevoius version, we used an average song length of 3.5 minutes.

## [1.0.0] - 2024-12-06

Initial version of the project.