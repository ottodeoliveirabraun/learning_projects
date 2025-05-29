from ..models.apartment import ApartmentListing 
from .deuwo import DeuwoAPIClient
from .howoge import HowogeAPIClient

class ResponseMerger():
    def __init__(self):
        self.responses = [
            DeuwoAPIClient(),
            HowogeAPIClient()
        ]

        all_responses = []
        for response in self.responses:
            all_responses = all_responses + response.fetch_data()
    
        self.data = all_responses