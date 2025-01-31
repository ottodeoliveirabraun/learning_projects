from dataclasses import dataclass
from datetime import date, time
from scraping_flights.utils import util_datetime


@dataclass
class Flight:
    airline: str
    airport_from: str
    airport_to: str
    price: float
    date_departure: str
    time_departure: time
    date_arrival: str
    time_arrival: time
    stopover: int
    duration: int
    scraped_timestamp: str

