from .base import APIclient
import pandas as pd
import numpy as np
from dataclasses import fields
import datetime
from ..models.apartment import ApartmentListing


class howogeAPIClient(APIclient):
    def __init__(self):
        url = "https://www.howoge.de/?type=999&tx_howsite_json_list[action]=immoList"
        payload = "tx_howsite_json_list%5Bpage%5D=1&tx_howsite_json_list%5Blimit%5D=12&tx_howsite_json_list%5Blang%5D=&tx_howsite_json_list%5Brent%5D=&tx_howsite_json_list%5Barea%5D=&tx_howsite_json_list%5Brooms%5D=egal&tx_howsite_json_list%5Bwbs%5D=all-offers"
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': '__cmpcc=1; __cmpconsent10543=BPpMtMFPpMtMFAfHIBDEDXAAAAAAAA; __cmpcvcu10543=__s974_U__; __cmpcpcu10543=__51_54__; _pk_id.1.d253=4e600cea00fe25d6.1679732404.; PHPSESSID=g06s5o0biudpjtfnif3515tklb; HOW_enable_osmap=true; _pk_ref.1.d253=%5B%22%22%2C%22%22%2C1679739725%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.1.d253=1',
            'Origin': 'https://www.howoge.de',
            'Referer': 'https://www.howoge.de/wohnungen-gewerbe/wohnungssuche.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        # Call the parent constructor
        super().__init__(url=url, payload=payload, headers=headers)
        # all the post method 
        self.data = self.post()

    def wbs_to_int(self, series):
        """
        Convert a pandas Series containing 'ja'/'nein' strings to 1/0 integers.
        
        Parameters:
        series (pd.Series): Series with values 'ja' or 'nein'
        
        Returns:
        pd.Series: Series with 1 for 'ja', 0 for 'nein', and NaN for others
        """
        return series.map({'ja': 1, 'nein': 0})

    
    def fetch_data(self):
        data = self.data

        data = data['immoobjects']

        #normalize the json data into a dataframe object and to some cleaning
        data_df = pd.json_normalize(data)
        data_df = data_df.drop(['image','features','district','icon','favorite','notice'], axis = 1)

        data_df[['address','address2']] = data_df.title.str.split(',',expand = True)
        #data_df[['zipcode','city']] = data_df.address2.str.split(' ',expand = True)
        zipcode = data_df.address2.str.split(' ').str[1]
        data_df['zipcode'] = zipcode
        city = data_df.address2.str.split(' ').str[2]
        data_df['city'] = city
        data_df = data_df[data_df['city'] == 'Berlin']
        data_df = data_df.drop(['city'], axis = 1)
        data_df['wbs'] = self.wbs_to_int(data_df['wbs'])
        data_df['date'] = datetime.datetime.now().strftime("%d/%m/%Y")

        print(data_df)

        print(data_df.columns.tolist())

        

        #print(data_df)
        # From here there are some minor column transformations that are needed since these fields are not longer available


        #renaming columns to adhere to old standard
        data_df.rename(columns={'uid': 'id'}, inplace=True)
        data_df.rename(columns={'rent': 'price'}, inplace=True)
        data_df.rename(columns={'area': 'size'}, inplace=True)
        data_df.rename(columns={'rooms': 'rooms'}, inplace=True)
        data_df.rename(columns={'coordinates.lat': 'latitude'}, inplace=True)
        data_df.rename(columns={'coordinates.lng': 'longitude'}, inplace=True)
        data_df.rename(columns={'address': 'address'}, inplace=True)
        data_df.rename(columns={'zipcode': 'zipcode'}, inplace=True)
        data_df.rename(columns={'link': 'url'}, inplace=True)

        #changing data types
        data_df['id'] = data_df['id'].astype(str)
        data_df['latitude'] = data_df['latitude'].astype(str)
        data_df['longitude'] = data_df['longitude'].astype(str)
        data_df['price'] = data_df['price'].astype(float)
        data_df['rooms'] = data_df['rooms'].astype(float)
        data_df['size'] = data_df['size'].astype(float)
        

        #adding new fields
        data_df['currently_available'] = 1
        data_df['email_sent'] = 0
        data_df['source'] = 'Howoge'

        # Get valid field names from the dataclass
        valid_fields = {f.name for f in fields(ApartmentListing)}

        # Filter each row to only contain expected fields
        filtered_rows = [
            {k: row.get(k, None) for k in valid_fields}
            for row in data_df.to_dict(orient='records')
        ]

        # Instantiate dataclass safely
        apartments = [ApartmentListing(**row) for row in filtered_rows]
        
        #print(apartments)
        return apartments


#howogeAPIClient().fetch_data() # testing fetch_data
    
        #print(data_df)