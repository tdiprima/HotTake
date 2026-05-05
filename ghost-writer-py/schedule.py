"""
Schedules daily automated article generation at 09:00 AM.
"""

import logging
import time

import schedule
from app import run_automation

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

schedule.every().day.at("09:00").do(run_automation)

while True:
    schedule.run_pending()
    time.sleep(60)
