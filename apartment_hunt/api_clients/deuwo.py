from .base import APIclient
import pandas as pd
import numpy as np
from dataclasses import fields
import logging
import datetime
from ..models.apartment import ApartmentListing


class DeuwoAPIClient(APIclient):
    def __init__(self):
        url = "https://www.wohnraumkarte.de/api/getImmoList?rentType=miete&city=Berlin&immoType=wohnung&minRooms=Beliebig&floor=Beliebig&bathtub=0&bathwindow=0&bathshower=0&furnished=0&kitchenEBK=0&toiletSeparate=0&disabilityAccess=egal&seniorFriendly=0&balcony=egal&subsidizedHousingPermit=egal&limit=150&offset=0&orderBy=dist_asc&userCookieValue=37cdf01355c3a9e20992dae5340c614e3c1c7b48&dataSet=deuwo"
        payload = {}
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://www.deutsche-wohnen.com',
            'Referer': 'https://www.deutsche-wohnen.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Cookie': 'PHPSESSID=7gr0vh4d4q8v2e8jfcr6l5esh2'
        }
        # Call the parent constructor
        super().__init__(url=url, payload=payload, headers=headers)
        # all the post method 
        self.data = self.post()

    def dropping_distant_columns(self, full_df: pd.DataFrame) -> pd.DataFrame:
        return full_df.drop(['images',
                        'titel',
                        'tour_link_360',
                        'land',
                        'vermarktungsart_miete',
                        'has_video',
                        'preview_img_url',
                        ], axis = 1)
    
    def fetch_data(self):
        data = self.data

        #normalize the json data into a dataframe object and to some cleaning
        data_df = pd.DataFrame(data["results"])

        data_df = self.dropping_distant_columns(data_df)

        #print(data_df)
        # From here there are some minor column transformations that are needed since these fields are not longer available
        data_df['date'] = datetime.datetime.now().strftime("%d/%m/%Y")

        data_df['wbs'] = data_df['slug'].str.contains(r'\(wbs\)', na=False).astype(int)

        data_df['heatingCostsIncluded'] = 0            #data_df['heatingCostsIncluded'].astype(int)  heating costs field was removed
        data_df['level'] = 999

        url_base = 'https://www.deutsche-wohnen.com/mieten/mietangebote/'

        data_df['url'] = url_base + data_df['slug'].astype(str) + '-' + data_df['wrk_id'].astype(str)

        #renaming columns to adhere to old standard
        data_df.rename(columns={'objektnr_extern': 'id'}, inplace=True)
        data_df.rename(columns={'preis': 'price'}, inplace=True)
        data_df.rename(columns={'groesse': 'size'}, inplace=True)
        data_df.rename(columns={'anzahl_zimmer': 'rooms'}, inplace=True)
        data_df.rename(columns={'lat': 'latitude'}, inplace=True)
        data_df.rename(columns={'lon': 'longitude'}, inplace=True)
        data_df.rename(columns={'strasse': 'address'}, inplace=True)
        data_df.rename(columns={'plz': 'zipcode'}, inplace=True)
        data_df.rename(columns={'ort': 'hood'}, inplace=True)

        #changing data types
        data_df['price'] = data_df['price'].astype(float)
        data_df['size'] = data_df['size'].astype(float)
        data_df['rooms'] = data_df['rooms'].astype(float)
        data_df['latitude'] = data_df['latitude'].astype(str)
        data_df['longitude'] = data_df['longitude'].astype(str)
        

        #adding new fields
        data_df['currently_available'] = 1
        data_df['email_sent'] = 0
        data_df['source'] = 'Deutsche Wohnen'

        # Get valid field names from the dataclass
        valid_fields = {f.name for f in fields(ApartmentListing)}

        # Filter each row to only contain expected fields
        filtered_rows = [
            {k: row.get(k, None) for k in valid_fields}
            for row in data_df.to_dict(orient='records')
        ]

        # Instantiate dataclass safely
        apartments = [ApartmentListing(**row) for row in filtered_rows]
        logging.info("Deutsche Wohnen pulled.")
        return apartments


# deuwoAPIClient().fetch_data() # testing fetch_data

