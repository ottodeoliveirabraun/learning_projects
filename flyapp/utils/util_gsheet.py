def write(data, target_cell):
    from googleapiclient.discovery import build 
    from google.oauth2 import service_account

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'keys.json'

    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)


    # The ID and range of a sample spreadsheet.
    SHEET_ID = '1cC9sl2KbXB-4L7ukM9prMczKyhpb172Yw29z1UBGPyc'


    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    #result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            #range="Testing!A1:S55").execute()

    #values = result.get('values', [])
    #request = sheet.values().update(spreadsheetId=SHEET_ID,
                        #range=target_cell, valueInputOption="USER_ENTERED", body={"values": data}).execute()

    request = sheet.values().append(
        spreadsheetId=SHEET_ID,
        range=target_cell,
        body={"values": data},
        valueInputOption="USER_ENTERED"
    ).execute()


    print('WOW')
    print(request)

def read(tab_code):
    from googleapiclient.discovery import build 
    from google.oauth2 import service_account
    import pandas as pd
    import numpy as np

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = '../keys.json'

    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)


    # The ID and range of a sample spreadsheet.
    SHEET_ID = '1cC9sl2KbXB-4L7ukM9prMczKyhpb172Yw29z1UBGPyc'

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    deuwo = sheet.values().get(spreadsheetId=SHEET_ID,
                            range="DeuWo!A:O").execute()
    
    howoge = sheet.values().get(spreadsheetId=SHEET_ID,
                            range="Howoge!A:M").execute()
    
    plz = sheet.values().get(spreadsheetId=SHEET_ID,
                            range="plz!D:F").execute()
    
    if tab_code == 'wow' :
        return deuwo.get('values', [])
    elif tab_code == 'Howoge' :
        return howoge.get('values', [])
    elif tab_code == 'plz' :
        return plz.get('values', [])
    else: 
        return print("Tab " + tab_code + " not found")
