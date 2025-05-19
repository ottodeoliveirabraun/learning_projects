from abc import ABC, abstractmethod
import requests

class APIclient(ABC):
    def __init__(self, url: str, payload: str, headers: dict):
        self.url = url
        self.payload = payload
        self.headers = headers

    def post(self):
        
        response = requests.get(self.url, params=self.payload, headers=self.headers)
        print(response.url)  # This will show the full request URL with params
        print("json response BELLOW-------------------")
        print(response.json())  # Assuming the response is in JSON format
        #get the response from the website
        response = requests.request("POST", self.url, headers=self.headers, data=self.payload)
        #get the data from the response in json
        data = response.json()
    
        return data
    
    @abstractmethod
    def fetch_data(self):
        raise NotImplementedError