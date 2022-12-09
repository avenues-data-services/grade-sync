# get_terms.py
import asyncio
from aiohttp import ClientSession
from canvas_api import canvas_get
import gspread
from google.cloud import secretmanager
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
import asyncio
import aiohttp
from aiohttp import ClientSession
import time

##################################################### 
# 
# Update sheet with the CPA results
#
#####################################################

def update_sheet(sheet_name,results,model_tab,grade):

    # filter grade results and organize them by subject
    results_by_subject = []
    for r in results:
        if r['student_grade'] == grade:
            s_results = {'subject': r['subject'], 'results': []}
            if s_results not in results_by_subject:
                results_by_subject.append(s_results)

    for r in results:
        if r['student_grade'] == grade:
            for s in results_by_subject:
                if (r['subject'] == s['subject']):
                    s['results'].append(r)

    # create a client to interact with the Google Drive / Sheets API
    scopes = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file('cp-gradebook-aafe3e0a7cbc.json',scopes=scopes)
    client = gspread.authorize(credentials)

    # open the google sheet document
    ss = client.open(sheet_name)

    # get model tab ID
    tabs = ss.worksheets()
    for t in tabs:
        if t.title == model_tab:
            model_tab_id = t.id

    # create tabs for each course (in case they don't exist)
    for s in results_by_subject:
        print(s['subject'])
        new_tab = True
        for t in tabs:
            if t.title == s['subject']:
                new_tab = False
        if new_tab:
            # copy model's tab
            copy_tab(ss,model_tab_id,s['subject'],grade)
            # insert course name
            ss_tab = ss.worksheet(s['subject'])
            ss_tab.update('D1', s['subject'])

    # order tabs alphabetically
    tabs = ss.worksheets()
    tabs.sort(key=lambda x: x.title, reverse=False)
    count = 4
    for t in tabs:

        new_index = count
        if t.title ==  '[DATA]':
            new_index = 1
        elif t.title ==  '[MODEL]':
            new_index = 2
        elif t.title ==  '[ALL]':
            new_index = 3

        body = {
            "requests": [
                {
                    'updateSheetProperties': {
                        'properties': {
                            'sheetId': t.id,
                            'index': new_index
                        },
                        "fields": "index"
                    }
                }
            ]
        }
        ss.batch_update(body)
        if t.title !=  '[DATA]' and t.title !=  '[MODEL]' and t.title !=  '[ALL]':
            count += 1

    # update results data
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
    
    adj_results = []
    adj_results.append([
        'Subject',
        'Course ID',
        'Course Name',
        'Assignment ID',
        'Assignment Date',
        'Student ID',
        'Student Name',
        'Student Section',
        'Student Grade',
        'Outcome ID',
        'Outcome Title',
        'Result',
        'CPA #',
        'Type',
    ])
    for s in results_by_subject:
        sorted_s = sorted(s['results'], key=lambda r: r['assignment_id'])
        sorted_s = sorted(s['results'], key=lambda r: (r['assignment_date'] is None, r['assignment_date']))
        sorted_s = sorted(s['results'], key=lambda r: r['subject'])
        for r in sorted_s: # adjust results array
            adj_results.append([
                r['subject'],
                r['course_id'],
                r['course_name'],
                r['assignment_id'],
                r['assignment_date'],
                r['student_id'],
                r['student_name'],
                r['student_section'],
                r['student_grade'],
                r['outcome_id'],
                r['outcome_title'],
                r['result'],
                r['cpa'],
                r['type']
            ])
    ss.values_update( # add the new values to the tab
        sheetName+'!A1', 
        params={'valueInputOption': 'USER_ENTERED'}, 
        body={'values': adj_results}
    )

    return 'SUCCESS'


def copy_tab(sheet,source,title,grade):
    # create new tab
    n_tab = sheet.add_worksheet(title=title, rows="151", cols="52")
    target = n_tab.id
    # copy model's tab content to the new tab
    body = {
        "requests": [
            {
                "copyPaste": {
                    "source": {
                        "sheetId": source,
                    },
                    "destination": {
                        "sheetId": target,
                    },
                    "pasteType": "PASTE_NORMAL"
                }
            },
            # hide VX ID column
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": 1
                    },
                    "properties": {
                        "hiddenByUser": True,
                    },
                    "fields": "hiddenByUser"
                }
            },
            # # hide Section column
            # {
            #     "updateDimensionProperties": {
            #         "range": {
            #             "sheetId": target,
            #             "dimension": "COLUMNS",
            #             "startIndex": 2,
            #             "endIndex": 3
            #         },
            #         "properties": {
            #             "hiddenByUser": True,
            #         },
            #         "fields": "hiddenByUser"
            #     }
            # },
            
            # adjust columns width
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": 1
                    },
                    "properties": {
                        "pixelSize": 70,
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target,
                        "dimension": "COLUMNS",
                        "startIndex": 1,
                        "endIndex": 2
                    },
                    "properties": {
                        "pixelSize": 250
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target,
                        "dimension": "COLUMNS",
                        "startIndex": 2,
                        "endIndex": 3
                    },
                    "properties": {
                        "pixelSize": 120
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target,
                        "dimension": "COLUMNS",
                        "startIndex": 3,
                        "endIndex": 11
                    },
                    "properties": {
                        "pixelSize": 40
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target,
                        "dimension": "COLUMNS",
                        "startIndex": 11,
                        "endIndex": 14
                    },
                    "properties": {
                        "pixelSize": 120
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target,
                        "dimension": "COLUMNS",
                        "startIndex": 14,
                        "endIndex": 15
                    },
                    "properties": {
                        "pixelSize": 320
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target,
                        "dimension": "COLUMNS",
                        "startIndex": 15,
                        "endIndex": 91
                    },
                    "properties": {
                        "pixelSize": 125
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target,
                        "dimension": "COLUMNS",
                        "startIndex": 91,
                        "endIndex": 92
                    },
                    "properties": {
                        "pixelSize": 19
                    },
                    "fields": "pixelSize"
                }
            },
            # adjust rows height
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target,
                        "dimension": "ROWS",
                        "startIndex": 0,
                        "endIndex": 1
                    },
                    "properties": {
                        "pixelSize": 220
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target,
                        "dimension": "ROWS",
                        "startIndex": 1,
                        "endIndex": 2
                    },
                    "properties": {
                        "pixelSize": 50
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target,
                        "dimension": "ROWS",
                        "startIndex": 2,
                        "endIndex": 7
                    },
                    "properties": {
                        "pixelSize": 35
                    },
                    "fields": "pixelSize"
                }
            },
            # freeze name/section columns
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": target,
                        "gridProperties": { 
                           "frozenColumnCount": 3 
                        }
                    },
                    "fields": "gridProperties.frozenColumnCount"
                }
            },
            # freeze outcomes rows 
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": target,
                        "gridProperties": { 
                           "frozenRowCount": 4 
                        }
                    },
                    "fields": "gridProperties.frozenRowCount"
                }
            },
        ]
    }
    sheet.batch_update(body)

    # hide letter grade columns 
    if grade == '6th Grade' or grade == '7th Grade':
        body = {
            "requests": [
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": target,
                            "dimension": "COLUMNS",
                            "startIndex": 12,
                            "endIndex": 14
                        },
                        "properties": {
                            "hiddenByUser": True,
                        },
                        "fields": "hiddenByUser"
                    }
                }
            ]
        }
    else:
        # hide semester proficiency column
        body = {
            "requests": [
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": target,
                            "dimension": "COLUMNS",
                            "startIndex": 11,
                            "endIndex": 12
                        },
                        "properties": {
                            "hiddenByUser": True,
                        },
                        "fields": "hiddenByUser"
                    }
                }
            ]
        }  
    sheet.batch_update(body)

    # create slicer
    body = {
        "requests": [
            {
                "addSlicer": {
                    "slicer": {
                        "spec": {
                            "dataRange": { 
                                "sheetId": target,
                                "startRowIndex": 3,
                                "endRowIndex": 147,
                                "startColumnIndex": 0,
                                "endColumnIndex": 92
                            },
                            "columnIndex": 2,
                            "title": "Section",
                        },
                        "position": {
                            "overlayPosition": {
                                "anchorCell": {
                                    "sheetId": target,
                                    "rowIndex": 0,
                                    "columnIndex": 0
                                },
                                "offsetXPixels": 40,
                                "offsetYPixels": 95,
                                "widthPixels": 290,
                                "heightPixels": 30
                            },
                        }
                    }
                }
            }
        ]
    }
    sheet.batch_update(body)
