from dataclasses import asdict
import pandas as pd
from typing import List
from ..models.apartment import ApartmentListing  
from ..Gsheet import read, write
from ..api_clients import deuwo,howoge
import numpy as np
from ..send_email import send_email

class Processor():
    def __init__(self, new_apartments: list[ApartmentListing]):
        self.new_apartments = new_apartments

    def listings_to_df(self, listings: List[ApartmentListing]) -> pd.DataFrame:
        return pd.DataFrame([asdict(listing) for listing in listings])
    
    def df_to_listings(df: pd.DataFrame) -> List[ApartmentListing]:
        return [ApartmentListing(**row) for row in df.to_dict(orient='records')]
    
    def transformations(self):
        
        #transforming listings to df
        new_data_df = self.listings_to_df(self.new_apartments)
        #getting old apartments
        old_data_df = pd.DataFrame(read('Apartments'))
        #replaces the columns by the first row 
        old_data_df.columns = old_data_df.iloc[0]
        old_data_df = old_data_df[1:]
        #add the binary saying that it is not currently available
        old_data_df['currently_available'] = '0'
        #adjustment to the data types coming from gsheets
        for x in old_data_df.columns:
            #print(x, [old_data_df[x]])
            old_data_df[x]=old_data_df[x].str.replace(',', '.')
            #print(x, [old_data_df[x]])
            old_data_df[x]=old_data_df[x].astype(new_data_df[x].dtypes.name)

        merging_columns = ['id',
                           'address',
                           'zipcode',
                           'hood',
                           'price',
                           'size',
                           'rooms',
                           'wbs',
                           'url',
                           'latitude',
                           'longitude',
                           'source']

        merge_df = new_data_df.merge(old_data_df, how = 'left', on = merging_columns)

        #zipcode logic not working yet
        plz_df = pd.DataFrame(read('plz'))

        #replaces the columns by the first row 
        plz_df.columns = plz_df.iloc[0]
        plz_df = plz_df[1:]
        plz_df.rename(columns={'plz_code':'zipcode'}, inplace=True)

        #print(plz_df) 

        merge_df = merge_df.merge(plz_df, how = 'left', on = 'zipcode')

        merge_df = merge_df.drop_duplicates(subset=['id'],ignore_index=True)

        #each new columns added to the merged data base if the filter responsible for sending the emails
        merge_df['main_flag'] = [1 if x < 1000 and y > 70 and z == 0 and k == '1' else 0 for (x,y,z,k) in 
                            zip(merge_df['price'],merge_df['size'],merge_df['wbs'],merge_df['Main'])]

        merge_df['matias_flag'] = [1 if x < 900 and y > 59 and z == 0 and w == '1' else 0 for (x,y,z,w) in 
                            zip(merge_df['price'],merge_df['size'],merge_df['wbs'],merge_df['Matias'])]

        merge_df['date_y'] = merge_df['date_y'].replace(np.nan,0)

        merge_df['date'] = [y if y != 0 else x for (x,y) in 
                            zip(merge_df['date_x'],merge_df['date_y'])]                

        url_base = 'https://www.deutsche-wohnen.com/expose/object/'

        count_matias = 0
        count_bubu = 0

        #the recently joined NULL values coming from the old_data are replaced by 0
        merge_df['email_sent_y'] = merge_df['email_sent_y'].replace(np.nan,0)

        for index, row in merge_df.iterrows():
            if row['email_sent_y'] == 0 and row['main_flag'] == 1:
                send_email(url_base + row['id'],'sophiagarmatsch@gmail.com')
                print(url_base + row['id'],'sophiagarmatsch@gmail.com')
                count_bubu = count_bubu + 1 
            if row['email_sent_y'] == 0 and row['matias_flag'] == 1:    
                #send_email(url_base + row['id'],'kalani.mahesh.de@gmail.com')
                #print(url_base + row['id'],'tuuri.matias@gmail.com')
                count_matias = count_matias + 1

        print (str(count_bubu) + ' new flat(s) found for bubu')
        print (str(count_matias) + ' new flat(s) found for maBOIIIIII')
                
        print(merge_df.columns.tolist())


        #remove the extra columns to enable adding it to the database
        merge_df = merge_df.drop(['email_sent_x','currently_available_y','date_x','date_y','Main','Matias','main_flag','matias_flag'], axis = 1)
        #turns on the email sent button to avoid sending it again
        merge_df['email_sent_y'] = 1
        #rename the columns coming from the merge to allow the connection to the database
        merge_df.rename(columns={'currently_available_x': 'currently_available', 'email_sent_y': 'email_sent'}, inplace=True)

        #concatenate the old data with the new data and remove the duplicates
        concatenation = pd.concat([merge_df,old_data_df],ignore_index=True)
        deduplication = concatenation.drop_duplicates(subset=['id'],ignore_index=True)

        #print(deduplication)

        #prepares the data to go to the Gsheet
        final = deduplication.values.tolist()

        #call the function to update Gsheet
        write(final,"Apartments!A2")

        print('Apartments updated!')


Processor(howoge.howogeAPIClient().fetch_data()).transformations()
Processor(deuwo.deuwoAPIClient().fetch_data()).transformations()
