from dataclasses import asdict, fields
import datetime
import pandas as pd
from typing import List
from ..models.apartment import ApartmentListing
from ..notifications.distribuitor import NotifierManager  
from ..storage.Gsheet import read, write
from ..api_clients.merger import ResponseMerger
import numpy as np
from ..send_email import send_email

class Processor():
    def __init__(self):
        self.new_apartments = ResponseMerger().data

    def listings_to_df(self, listings: List[ApartmentListing]) -> pd.DataFrame:
        return pd.DataFrame([asdict(listing) for listing in listings])
    
    def df_to_listings(self, df: pd.DataFrame) -> List[ApartmentListing]:
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

        
        dtype_map = {f.name: f.type for f in fields(ApartmentListing)}

        for col, target_type in dtype_map.items():
            if col not in old_data_df.columns:
                continue

            try:
                # Try convert to the appropriate type
                if target_type == int:
                    old_data_df[col] = pd.to_numeric(old_data_df[col], errors='coerce').fillna(0).astype(int)
                elif target_type == float:
                    old_data_df[col] = (
                        old_data_df[col]
                        .astype(str)
                        .str.replace(',', '.', regex=False)
                        .replace('', '0')
                    )
                    old_data_df[col] = pd.to_numeric(old_data_df[col], errors='coerce').fillna(0.0)
                else:
                    # Fallback
                    old_data_df[col] = old_data_df[col].astype(str)
            except Exception as e:
                print(f"Error casting column {col}: {e}")


        # Set index to the merge key (use a subset if needed, but assume 'id' is unique enough)
        new_data_df.set_index('id', inplace=True)
        old_data_df.set_index('id', inplace=True)

        # Use combine_first to get values from new_data_df first, then old_data_df
        merge_df = old_data_df.combine_first(new_data_df)

        # Tag records that are present in new_data_df
        merge_df['currently_available'] = merge_df.index.isin(new_data_df.index).astype(int)

        #email notification goes here
        NotifierManager(self.df_to_listings(merge_df))
        merge_df['email_sent'] = 1


        # Reset index to return 'id' as a column
        merge_df.reset_index(inplace=True)

        #print(merge_df)

        write(merge_df.replace(np.nan, '').values.tolist(), "Apartments!A2")
        print('Apartments updated!')


        """         
        # Load PLZ and clean
        plz_df = pd.DataFrame(read('plz'))
        plz_df.columns = plz_df.iloc[0]
        plz_df = plz_df[1:]
        plz_df.rename(columns={'plz_code': 'zipcode'}, inplace=True)

        # Merge PLZ on zipcode using combine_first
        merge_df = merge_df.set_index('zipcode')
        plz_df = plz_df.set_index('zipcode')
        merge_df = merge_df.combine_first(plz_df)
        merge_df.reset_index(inplace=True) """




#Processor(ResponseMerger().data).transformations()
