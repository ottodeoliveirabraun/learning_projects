import pandas as pd
import numpy as np
from send_email import send_email
from Gsheet import write
from Gsheet import read
import requests
import datetime

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

response = requests.request("POST", url, headers=headers, data=payload)
#get the data from the response in json
data = response.json()

data = data['immoobjects']
#print(data)
#normalize the json data into a dataframe object and to some cleaning
data_df = pd.json_normalize(data)
data_df = data_df.drop(['image','features','district','icon','favorite','notice'], axis = 1)
#print(data_df)
data_df[['address','address2']] = data_df.title.str.split(',',expand = True)
#data_df[['zipcode','city']] = data_df.address2.str.split(' ',expand = True)
zipcode = data_df.address2.str.split(' ').str[1]
data_df['zipcode'] = zipcode
city = data_df.address2.str.split(' ').str[2]
data_df['city'] = city
data_df = data_df[data_df['city'] == 'Berlin']
data_df = data_df.drop(['city'], axis = 1)
data_df['date'] = datetime.datetime.now().strftime("%d/%m/%Y")
data_df['coordinates.lat'] = data_df['coordinates.lat'].astype(float)
data_df['coordinates.lng'] = data_df['coordinates.lng'].astype(float)

columns_ = ['uid',
            'rent',
            'area',
            'rooms',
            'wbs',
            'link',
            'coordinates.lat',
            'coordinates.lng',
            'address',
            'zipcode',
            'date']

new_data_df = data_df[columns_].copy()

#add the binary saying that it is currently available
new_data_df['currently.available'] = 1
new_data_df['email.sent'] = 0

#print(new_data_df.dtypes)

#call the function read to get the current information in the Gsheet
old_data_df = pd.DataFrame(read('Howoge'))
#replaces the columns by the first row 
old_data_df.columns = old_data_df.iloc[0]
old_data_df = old_data_df[1:]
#add the binary saying that it is not currently available
old_data_df['currently.available'] = '0'


#adjustment to the data types coming from gsheets
for x in old_data_df.columns:
    #print(x, [old_data_df[x]])
    old_data_df[x]=old_data_df[x].str.replace(',', '.')
    if x == 'area': 
        old_data_df[x]=old_data_df[x].astype('float64')
    else:
        old_data_df[x]=old_data_df[x].astype(new_data_df[x].dtypes.name)


columns_merge = ['uid',
                'rent',
                'area',
                'rooms',
                'wbs',
                'link',
                'coordinates.lat',
                'coordinates.lng',
                'address',
                'zipcode']

#print(old_data_df)
#print(new_data_df)

#joining the the 2 tables
merge_df = new_data_df.merge(old_data_df, how = 'left', on = columns_merge)

plz_df = pd.DataFrame(read('plz'))

#replaces the columns by the first row 
plz_df.columns = plz_df.iloc[0]
plz_df = plz_df[1:]
plz_df.rename(columns={'plz_code':'zipcode'}, inplace=True)

#print(plz_df)

merge_df = merge_df.merge(plz_df, how = 'left', on = 'zipcode')
merge_df = merge_df.drop_duplicates(subset=['uid'],ignore_index=True)

#each new columns added to the merged data base if the filter responsible for sending the emails
merge_df['main_flag'] = [1 if x < 1000 and y > 70 and z == 'nein' and w == '1' else 0 for (x,y,z,w) in 
                    zip(merge_df['rent'],merge_df['area'],merge_df['wbs'],merge_df['Main'])]

merge_df['matias_flag'] = [1 if x < 900 and (y == 1.5 or y == 2) and z == 'nein' and w =='1' else 0 for (x,y,z,w) in 
                    zip(merge_df['rent'],merge_df['rooms'],merge_df['wbs'],merge_df['Matias'])]

url_base = 'https://www.howoge.de'

count_matias = 0
count_bubu = 0

print(merge_df[['date_x','date_y']])
merge_df['email.sent_y'] = merge_df['email.sent_y'].replace(np.nan,0)
merge_df['date_y'] = merge_df['date_y'].replace(np.nan,datetime.datetime.now().strftime("%d/%m/%Y"))
print(merge_df)

for index, row in merge_df.iterrows():
    #print(row['uid'], row['email.sent_y'], row['main_flag'], row['matias_flag'])
    if row['email.sent_y'] == 1 and row['main_flag'] == 1:
        send_email(url_base + row['link'],'sophiagarmatsch@gmail.com')
        #print(url_base + row['link'],'sophiagarmatsch@gmail.com')
        count_bubu = count_bubu + 1 
    if row['email.sent_y'] == 1 and row['matias_flag'] == 1:    
        #send_email(url_base + row['link'],'tuuri.matias@gmail.com')
        #print(url_base + row['link'],'tuuri.matias@gmail.com')
        count_matias = count_matias + 1

print (str(count_bubu) + ' new flat(s) found for bubu')
print (str(count_matias) + ' new flat(s) found for maBOIIIIII')
     
#remove the extra columns to enable adding it to the database
merge_df = merge_df.drop(['email.sent_x','currently.available_y','date_x','main_flag','matias_flag','Main','Matias'], axis = 1)
#turns on the email sent button to avoid sending it again
merge_df['email.sent_y'] = 1
#rename the columns coming from the merge to allow the connection to the database
merge_df.rename(columns={'date_y':'date','currently.available_x': 'currently.available', 'email.sent_y': 'email.sent'}, inplace=True)

#concatenate the old data with the new data and remove the duplicates
concatenation = pd.concat([merge_df,old_data_df],ignore_index=True)
deduplication = concatenation.drop_duplicates(subset=['uid'],ignore_index=True)

#print(deduplication)
#prepares the data to go to the Gsheet
final = deduplication.values.tolist()


write(final,"Howoge!A2")

print('Howoge updated!')
