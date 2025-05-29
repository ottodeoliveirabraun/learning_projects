from dataclasses import dataclass, field
from typing import Optional
import datetime

@dataclass
class ApartmentListing:
    id: str = ""
    address: str = ""
    zipcode: int = 0
    hood: str = ""
    price: float = 0.0
    size: float = 0.0
    rooms: float = 0.0
    wbs: int = 0
    url: str = ""
    latitude: str = ""
    longitude: str = ""
    source: str = ""
    currently_available: int = 0  # 0 = False, 1 = True
    email_sent: int = 0
    date: datetime.date = field(default_factory=datetime.date.today)

