from ..models.apartment import ApartmentListing 
from .customers import SophiaNotifier

class NotifierManager:
    def __init__(self, apartment_list: list[ApartmentListing]):
        self.notifiers = [
            SophiaNotifier(apartment_list),
        ]

        for notifier in self.notifiers:
            notifier.process_notifications()