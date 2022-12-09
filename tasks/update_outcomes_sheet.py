# update_outcomes_list.py
from canvas_api import canvas_get
import gspread
from google.oauth2 import service_account
from datetime import datetime

##################################################### 
# 
# Update sheet with the courses/CPAs outcomes
#
#####################################################

def update_outcomes_sheet(sheet_name,outcomes_list):

    # create a client to interact with the Google Drive / Sheets API
    scopes = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file('cp-gradebook-aafe3e0a7cbc.json',scopes=scopes)
    client = gspread.authorize(credentials)

    # open the google sheet document
    ss = client.open(sheet_name)
    sheetName = '[DATA]'
    tab = ss.worksheet(sheetName)

    # update data
    sheetName = '[DATA]'
    data_tab = ss.worksheet(sheetName)

    sheetId = data_tab._properties['sheetId'] # clear the tab
    body = {
        "requests": [
            {
                "deleteRange": {
                    "range": {
                        "sheetId": sheetId,
                    },
                    "shiftDimension": "ROWS"
                }
            }
        ]
    }
    ss.batch_update(body)

    # add the new values to the tab
    ss.values_update(
        sheetName+'!A1', 
        params={'valueInputOption': 'USER_ENTERED'}, 
        body={'values': outcomes_list}
    )

    return 'SUCCESS'