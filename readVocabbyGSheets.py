# Dec11, 12, 2021
# readVocabbyGSheets.py
# MEMO: THIS IS FOR GitHub

# env on my laptop: pysimplegui: py=3.7.7

# run this code on raspberry pi 3Bp1
# python3 = 3.7.3
# - pip3 install gspread
# - pip3 install oauth2client
# REF: https://qiita.com/164kondo/items/eec4d1d8fd7648217935

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import myKeys as mk
import requests
import time


# globals
HOW_MANY_TO_READ = 3
MAX_READ_TIME = 3
INTERVAL = 25  # seconds


def connectGSWorkSheet(json_file, sheet_key, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file,
                                                                   scope)
    gc = gspread.authorize(credentials)
    wb = gc.open_by_key(sheet_key)  # like a workbook on excel
    ws = wb.worksheet(sheet_name)  # this is the sheet to me

    return ws


def pickRows(rows):
    picked = []
    ws_row_nums = []
    # MEMO: idx + 2 is the ws row num.  idx=2 -> row 5 (A5, B5, C5,,,)
    for i, row in enumerate(rows):
        # check the column B (read out)
        if int(row[1]) < MAX_READ_TIME:
            picked.append(row)
            ws_row_nums.append(i + 3)
        if len(picked) == HOW_MANY_TO_READ:
            return picked, ws_row_nums


def getRowsForToday(ws):
    # get all rows in list of list
    rows = ws.get_values()
    # select today's rows
    # NOTE: skip 2 header rows
    rows_to_read, ws_row_nums = pickRows(rows[2:])

    return rows_to_read, ws_row_nums


def updateWS(ws, rows_to_read, row_nums):
    """
    increment "read out" column(B) value by 1
    REF: https://docs.gspread.org/en/latest/user-guide.html#updating-cells
    """
    for row, row_num in zip(rows_to_read, row_nums):
        # method 1: with row, col coodinates. update_cell(row, col, value)
        # ws.update_cell(row_num, 2, int(row[1]) + 1)
        # method 2: with cell notation. e.g. update(B3, value)
        ws.update("B{}".format(row_num), int(row[1]) + 1)
    return 'ws updating done!'


def sendMsgTo3B1(msg):
    """
    ask google home to announce
    node-red is working on 3Bp1
    """
    # TODO: raspi ip is needed
    host = "http://<YOUR RASBPI IP>/xxxxx"
    lang = 'en-US'  # only ja for now.
    myData = {'message': msg, 'language': lang}
    print('[debug sendMsgTo3B1()] posting:', msg)
    res = requests.post(host, data=myData)
    print('[debug sendMsgTo3B1()] response:', res)

    return 'sending message done!'


def openingAnnouncement():
    msg = "Hello, everyone, I am Vocabby. It's time for voccaby today. "
    msg += "Please get ready."
    done = sendMsgTo3B1(msg)

    return done


def closingAnnouncement():
    msg = "How was it? I've updated the read count on google sheets. "
    msg += "See you tomorrow."
    done = sendMsgTo3B1(msg)

    return done


def msgConstruction(row):
    word = row[4]
    cat = row[5]
    definition = row[6]
    example = row[7]
    msg = word + ', ' + cat + ', definition: ' + definition + '. '
    msg += 'example: ' + example

    return msg


def readTodaysVocab(rows_to_read):
    """
    send msg to google home via Node-Red on 3B1
    """
    for row in rows_to_read:
        msg = msgConstruction(row)
        done = sendMsgTo3B1(msg)
        print('[debug] speeping ' + str(INTERVAL) + ' sec...')
        time.sleep(INTERVAL)
        print('[debug] woke up!')
        print()

    return done


def main():
    json_file = mk.service_account_key_json
    sheet_key = mk.spread_sheet_key
    # get worksheet
    ws = connectGSWorkSheet(json_file, sheet_key, "test")

    # select today's content
    rows_to_read, row_nums = getRowsForToday(ws)
    print('[debug]', 'rows to read:', rows_to_read)
    print('[debug]', 'row nums:', row_nums)

    # opening announcement
    done = openingAnnouncement()
    print('[debug] openingAnnouncement()', done)
    print('[debug] speeping 15 sec...')
    time.sleep(15)
    print('[debug] woke up!')
    print()
    # read them one by one
    done = readTodaysVocab(rows_to_read)
    print('[debug] readTodaysVocab()', done)
    # update ws
    done = updateWS(ws, rows_to_read, row_nums)
    print('[debug] updateWS()', done)

    # closing announcement
    done = closingAnnouncement()
    print('[debug] closingAnnouncement()', done)


if __name__ == '__main__':
    main()
