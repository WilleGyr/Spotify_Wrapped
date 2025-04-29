import sys, time, os
from spotifywrapped.spotify_utils import (
    getGoogleSheets,
    load_csv_to_dict,
    populate_months_dropdown,
    OnGenerateButtonClicked,
    on_tab_changed,
    update_month_dropdown,
    update_type_dropdown,
    update_image_label,
    on_dropdown_changed
)
from spotifywrapped.credentials import SPREADSHEET_ID
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QVBoxLayout

def main():
    # Clear the terminal
    #os.system('cls' if os.name == 'nt' else 'clear')
    start_time = time.time()

    # Start the mainwindow.ui
    app = QtWidgets.QApplication(sys.argv)
    base_path = os.path.dirname(__file__)

    # Load UI
    ui_path = os.path.join(base_path, "MainWindow.ui")
    window = uic.loadUi(ui_path)

    # Load logo
    logo_path = os.path.join(base_path, "Spotify_Logo.png")
    if os.path.exists(logo_path):
        logo_pixmap = QPixmap(logo_path)
        window.SpotifyLogoLabel.setPixmap(logo_pixmap)
        window.SpotifyLogoLabel.setScaledContents(True)

    # Set window icon
    icon_path = os.path.join(base_path, "Spotify_Wrapped_Icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))


    window.WaitLabel.setVisible(False)
    window.DoneLabel.setVisible(False)
    window.setWindowTitle("Spotify Wrapped")
    window.show()

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

if __name__ == "__main__":
    main()