from googleapiclient.discovery import build 
from google.oauth2 import service_account
import pandas as pd
import numpy as np
import json
import os

with open("keys.json", "r") as f:
    SERVICE_ACCOUNT_FILE = json.load(f)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
#SERVICE_ACCOUNT_FILE = 'keys.json' # When using local keys.json file

creds = None
creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def write(data,target_cell):
    

    #print("Pasting data into Gsheets")


    # The ID and range of a sample spreadsheet.
    SHEET_ID = '1re7-5x7wF2_kN_sFYXoOQ1or_6FJt7_y7Av2VbGcasY'


    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    #result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            #range="Testing!A1:S55").execute()

    #values = result.get('values', [])
    request = sheet.values().update(spreadsheetId=SHEET_ID,
                        range=target_cell, valueInputOption="USER_ENTERED", body={"values": data}).execute()
    

    print('WOW')
    #print(request)

def read(tab_code):

    # The ID and range of a sample spreadsheet.
    SHEET_ID = '1re7-5x7wF2_kN_sFYXoOQ1or_6FJt7_y7Av2VbGcasY'

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    deuwo = sheet.values().get(spreadsheetId=SHEET_ID,
                            range="DeuWo!A:O").execute()
    
    howoge = sheet.values().get(spreadsheetId=SHEET_ID,
                            range="Howoge!A:M").execute()
    
    plz = sheet.values().get(spreadsheetId=SHEET_ID,
                            range="plz!D:F").execute()
    
    if tab_code == 'DeuWo' :
        return deuwo.get('values', [])
    elif tab_code == 'Howoge' :
        return howoge.get('values', [])
    elif tab_code == 'plz' :
        return plz.get('values', [])
    else: 
        return print("Tab " + tab_code + " not found")
