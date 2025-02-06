#This is the 2nd version of the deuwo code because on january 2025 they changed their website/API
import requests
import pandas as pd
import numpy as np
from send_email import send_email
from Gsheet import write
from Gsheet import read

import datetime

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

response = requests.get(url, params=payload, headers=headers)

print(response.url)  # This will show the full request URL with params
print("json response BELLOW-------------------")
print(response.json())  # Assuming the response is in JSON format
#get the response from the website
response = requests.request("POST", url, headers=headers, data=payload)
#get the data from the response in json
data = response.json()
#normalize the json data into a dataframe object and to some cleaning
data_df = pd.DataFrame(data["results"])
data_df = data_df.drop(['images',
                        'titel',
                        'tour_link_360',
                        'wrk_id',
                        'land',
                        'vermarktungsart_miete',
                        'has_video',
                        'preview_img_url',
                        ], axis = 1)

#print(data_df)

data_df['date'] = datetime.datetime.now().strftime("%d/%m/%Y")



data_df['requiresQualificationCertificate'] = data_df['slug'].str.contains(r'\(wbs\)', na=False).astype(int)

data_df['heatingCostsIncluded'] = 0            #data_df['heatingCostsIncluded'].astype(int)  heating costs field was removed
data_df['level'] = 999

#renaming columns to adhere to old standard
data_df.rename(columns={'objektnr_extern': 'id'}, inplace=True)
data_df.rename(columns={'preis': 'price'}, inplace=True)
data_df.rename(columns={'groesse': 'area'}, inplace=True)
data_df.rename(columns={'anzahl_zimmer': 'rooms'}, inplace=True)
data_df.rename(columns={'lat': 'geoLocation.latitude'}, inplace=True)
data_df.rename(columns={'lon': 'geoLocation.longitude'}, inplace=True)
data_df.rename(columns={'strasse': 'address.street'}, inplace=True)
data_df.rename(columns={'plz': 'address.zip'}, inplace=True)
data_df.rename(columns={'ort': 'address.houseNumber'}, inplace=True)

#changing data types
data_df['price'] = data_df['price'].astype(float)

columns_ = ['id',
            'price',
            'requiresQualificationCertificate',
            'area',
            'rooms',
            'level',
            'heatingCostsIncluded',
            'date',
            'geoLocation.latitude',
            'geoLocation.longitude',
            'address.street',
            'address.houseNumber',
            'address.zip']

new_data_df = data_df[columns_].copy()
#add the binary saying that it is currently available
new_data_df['currently.available'] = 1
new_data_df['email.sent'] = 0


#call the function read to get the current information in the Gsheet
old_data_df = pd.DataFrame(read('DeuWo'))
#replaces the columns by the first row 
old_data_df.columns = old_data_df.iloc[0]
old_data_df = old_data_df[1:]
#add the binary saying that it is not currently available
old_data_df['currently.available'] = '0'

#adjustment to the data types coming from gsheets
for x in old_data_df.columns:
    #print(x, [old_data_df[x]])
    old_data_df[x]=old_data_df[x].str.replace(',', '.')
    #print(x, [old_data_df[x]])
    old_data_df[x]=old_data_df[x].astype(new_data_df[x].dtypes.name)

columns_2 = ['id',
            'price',
            'requiresQualificationCertificate',
            'area',
            'rooms',
            'level',
            'heatingCostsIncluded',
            'geoLocation.latitude',
            'geoLocation.longitude',
            'address.street',
            'address.houseNumber',
            'address.zip']

#joining the the 2 tables
merge_df = new_data_df.merge(old_data_df, how = 'left', on = columns_2)

plz_df = pd.DataFrame(read('plz'))

#replaces the columns by the first row 
plz_df.columns = plz_df.iloc[0]
plz_df = plz_df[1:]
plz_df.rename(columns={'plz_code':'address.zip'}, inplace=True)

#print(plz_df)

merge_df = merge_df.merge(plz_df, how = 'left', on = 'address.zip')
merge_df = merge_df.drop_duplicates(subset=['id'],ignore_index=True)

#print(merge_df)

#each new columns added to the merged data base if the filter responsible for sending the emails
merge_df['main_flag'] = [1 if x < 1000 and y > 70 and z == 0 and w != 0 and k == '1' else 0 for (x,y,z,w,k) in 
                    zip(merge_df['price'],merge_df['area'],merge_df['requiresQualificationCertificate'],merge_df['level'],merge_df['Main'])]

merge_df['matias_flag'] = [1 if x < 900 and y > 59 and z == 0 and w == '1' else 0 for (x,y,z,w) in 
                    zip(merge_df['price'],merge_df['area'],merge_df['requiresQualificationCertificate'],merge_df['Matias'])]

merge_df['date_y'] = merge_df['date_y'].replace(np.nan,0)

merge_df['date'] = [y if y != 0 else x for (x,y) in 
                    zip(merge_df['date_x'],merge_df['date_y'])]                

url_base = 'https://www.deutsche-wohnen.com/expose/object/'

count_matias = 0
count_bubu = 0

#the recently joined NULL values coming from the old_data are replaced by 0
merge_df['email.sent_y'] = merge_df['email.sent_y'].replace(np.nan,0)

for index, row in merge_df.iterrows():
    if row['email.sent_y'] == 0 and row['main_flag'] == 1:
        send_email(url_base + row['id'],'sophiagarmatsch@gmail.com')
        #print(url_base + row['id'],'sophiagarmatsch@gmail.com')
        count_bubu = count_bubu + 1 
    if row['email.sent_y'] == 0 and row['matias_flag'] == 1:    
        #send_email(url_base + row['id'],'kalani.mahesh.de@gmail.com')
        #print(url_base + row['id'],'tuuri.matias@gmail.com')
        count_matias = count_matias + 1

print (str(count_bubu) + ' new flat(s) found for bubu')
print (str(count_matias) + ' new flat(s) found for maBOIIIIII')
     
#remove the extra columns to enable adding it to the database
merge_df = merge_df.drop(['email.sent_x','currently.available_y','date_x','date_y','Main','Matias','main_flag','matias_flag'], axis = 1)
#turns on the email sent button to avoid sending it again
merge_df['email.sent_y'] = 1
#rename the columns coming from the merge to allow the connection to the database
merge_df.rename(columns={'currently.available_x': 'currently.available', 'email.sent_y': 'email.sent'}, inplace=True)

#concatenate the old data with the new data and remove the duplicates
concatenation = pd.concat([merge_df,old_data_df],ignore_index=True)
deduplication = concatenation.drop_duplicates(subset=['id'],ignore_index=True)

#print(deduplication)

#prepares the data to go to the Gsheet
final = deduplication.values.tolist()

#call the function to update Gsheet
write(final,"DeuWo!A2")

print('DeuWo updated!')
