from .base import Notifier
from ..models.apartment import ApartmentListing

class SophiaNotifier(Notifier):
    def __init__(self,
                 apartment_list: list[ApartmentListing],
                 #user_email= "sophiagarmatsch@gmail.com",
                 user_email= "ottoobraun@gmail.com",
                 price_filter= 1000,
                 size_filter= 70
                 ):
        super().__init__(apartment_list=apartment_list,
                         user_email=user_email,
                         price_filter=price_filter,
                         size_filter=size_filter)