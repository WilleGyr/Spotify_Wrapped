import os
import json

def load_credentials():
    #user_home = os.path.expanduser("~")  # Home directory
    credentials_path = os.path.join("spotifywrapped_credentials.json")

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"Credentials file not found. Please create {credentials_path} based on the template."
        )

    with open(credentials_path, 'r', encoding='utf-8') as f:
        creds = json.load(f)

    # Validation (optional but professional)
    if not isinstance(creds.get("SPREADSHEET_ID"), list):
        raise ValueError("SPREADSHEET_ID must be a list.")
    if not creds.get("CLIENT_ID") or not creds.get("CLIENT_SECRET"):
        raise ValueError("CLIENT_ID and CLIENT_SECRET must be set.")

    return creds
