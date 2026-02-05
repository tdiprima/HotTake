"""
Logs generated article metadata to a Google Sheets spreadsheet.
"""

import gspread
from google.oauth2.service_account import Credentials


def log_article(title, keywords):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file("../creds.json", scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("Blog Stats").sheet1
    sheet.append_row([title, ", ".join(keywords)])
