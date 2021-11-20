# Oct31, 2021, ms
# gspread_handler.py


from datetime import datetime
import myKeys as mk
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# credentials
SERVICE_ACCOUNT_KEY = mk.service_account_key_json
SPREAD_SHEET_KEY = mk.spread_sheet_key


# access to gspread sheet
def connect_gspread(jsonf, gs_key):
    """
    ref: https://qiita.com/164kondo/items/eec4d1d8fd7648217935
    """
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf,
                                                                   scope)
    gs = gspread.authorize(credentials)
    worksheet = gs.open_by_key(gs_key).sheet1  # the first one
    return worksheet


def next_available_row(worksheet):
    """
    ref: https://stackoverflow.com/questions/40781295/\
        how-to-find-the-first-empty-row-of-a-google-spread-\
        sheet-using-python-gspread/42476314#42476314
    """
    return len(worksheet.get_all_values()) + 1


def timestamp():
    """
    Oct 31, 2021, 15:31:29
    """
    now = datetime.now()
    return now.strftime("%b %d, %Y, %H:%M:%S")


def construct_rows(od_results, user, ser_num):
    """
    put elements in order
    starting read out is set to 0.
    """
    rows = []
    for word, category, definition, example in od_results:
        if definition == 'Not Found':
            continue
        else:
            # ser#, read out, input time stamp, uer,
            # word, lex category, definition, example
            rows.append([ser_num, 0, timestamp(), user,
                         word, category, definition, example])
        ser_num += 1

    return rows


def write_to_ws(ws, row_num, rows):
    """
    specify top left to start cell updating
    the second arg is a list of [row cells].
    -> [[row cells], [row cells],,,]
    """
    ws.update("A{}".format(row_num), rows)  # top left of the range


def register_od_results(od_results, user):
    """
    od_results is a list of (word, category, definition, example)
    """
    # check the row # to start appending
    ws = connect_gspread(SERVICE_ACCOUNT_KEY, SPREAD_SHEET_KEY)
    row_to_start = next_available_row(ws)
    ser_num = row_to_start - 2  # there are 2 header rows
    # row ccnstruction
    rows = construct_rows(od_results, user, ser_num)
    # write to ws
    write_to_ws(ws, row_to_start, rows)

    return len(rows)
