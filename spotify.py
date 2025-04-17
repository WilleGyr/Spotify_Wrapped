import sys, time, os
from spotify_utils import getGoogleSheets, load_csv_to_dict, wrapped
from credentials import SPREADSHEET_ID
from datetime import datetime

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

start_time = time.time()

# Reset the Spotify_Stats.txt file
with open('Spotify_Wrapped.txt', 'w') as f:
    f.write('----- Spotify Wrapped -----\n\n')

# Download the CSV file from Google Sheets and load it into a dictionary
csv_filepath = getGoogleSheets(SPREADSHEET_ID, '', "spotify.csv")
data_dict = load_csv_to_dict(csv_filepath)

# Prompt the user for input
print(f"Specify year, month or month of year. Otherwise leave blank for the complete {datetime.now().year} wrapped:")
#user_input = input("")
user_input = ""
print("Preparing Spotify Wrapped...")

# Split the input and handle cases where the input is blank or has only one value
inputs = user_input.split()
first = inputs[0] if len(inputs) > 0 else None
second = inputs[1] if len(inputs) > 1 else None

# Capitalize the first and second values if they are not digits
if first and not first.isdigit():
    first = first.capitalize()
if second and not second.isdigit():
    second = second.capitalize()

# Call the wrapped function with the appropriate arguments
if first and not second:
    wrapped(data_dict, first)
elif first and second:
    wrapped(data_dict, first, second)
else:
    wrapped(data_dict)

# Exit the program
print("Spotify Wrapped has been successfully generated in the file Spotify_Wrapped.txt!")
print("Process finished --- %s seconds ---" % (time.time() - start_time))
sys.exit(0)