"""
Logs generated article metadata to a Google Sheets spreadsheet.
"""

import logging

import gspread
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)


def log_article(title, keywords):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    try:
        creds = Credentials.from_service_account_file("../creds.json", scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open("Blog Stats").sheet1
        sheet.append_row([title, ", ".join(keywords)])
        logger.info("Logged article to Google Sheets: %s", title)
    except Exception as e:
        logger.error("Failed to log to Google Sheets: %s", e)
