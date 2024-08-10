import json
import datetime

START_DATE = datetime.date(2024,11,1)
ORIGIN = 'BER'
END_DATE = datetime.date(2025,1,30)
TRIP_DURATION_DAYS = 60
DESTINATION = 'SAO'


def read_secrets(filename="secrets.json") -> dict:
    try:
        with open(filename, "r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}


secrets = read_secrets()
FIREFOX_BINARY_LOCATION = r"/Applications/Firefox.app"
DAYS_TO_SAVE_BACKUP = 30
CSV_BACKUP_FOLDER = r"/Users/otto.braun/Documents/crawler_project/flight_data"
#EMAIL_LOGIN = secrets["EMAIL_LOGIN"]
#EMAIL_PASSWORD = secrets["EMAIL_PASSWORD"]
