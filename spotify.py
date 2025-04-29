import sys, time, os
from spotify_utils import getGoogleSheets, load_csv_to_dict, populate_months_dropdown, OnGenerateButtonClicked, on_tab_changed, update_month_dropdown, update_type_dropdown, update_image_label, on_dropdown_changed
from credentials import SPREADSHEET_ID
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout

# Clear the terminal
#os.system('cls' if os.name == 'nt' else 'clear')
start_time = time.time()

# Start the mainwindow.ui
app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi("mainwindow.ui")
window.setWindowTitle("Spotify Wrapped")

window.show()

window.WaitLabel.setVisible(False)
window.DoneLabel.setVisible(False)

if os.path.exists("Spotify_Logo.png"):
    logo_pixmap = QPixmap("Spotify_Logo.png")
    window.SpotifyLogoLabel.setPixmap(logo_pixmap)
    window.SpotifyLogoLabel.setScaledContents(True)

# Reset the Spotify_Stats.txt file
with open('Spotify_Wrapped.txt', 'w') as f:
    f.write('----- Spotify Wrapped -----\n\n')

# Download the CSV file from Google Sheets and load it into a dictionary
csv_filepath = getGoogleSheets(SPREADSHEET_ID, '', "spotify.csv")
data_dict = load_csv_to_dict(csv_filepath)

# Call the function to populate the MonthsDropdown
populate_months_dropdown(data_dict, window.MonthsDropdown)
update_month_dropdown(window)
update_type_dropdown(window)
update_image_label(window)

#window.GenerateButton.clicked.connect(OnGenerateButtonClicked)
window.GenerateButton.clicked.connect(lambda: OnGenerateButtonClicked(window))
window.tabWidget.currentChanged.connect(lambda index: on_tab_changed(1, window))

window.Vis_TypeDropDown.currentIndexChanged.connect(lambda: update_image_label(window))
window.Vis_MonthDropDown.currentIndexChanged.connect(lambda: on_dropdown_changed(window))



# Start the event loop to keep the application running
sys.exit(app.exec_())