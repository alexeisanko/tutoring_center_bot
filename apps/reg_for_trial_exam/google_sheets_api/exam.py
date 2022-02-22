import gspread
from pprint import pprint

gc = gspread.service_account('apps/reg_for_trial_exam/google_sheets_api/client_secret.json')
# gc = gspread.service_account('client_secret.json')


sh = gc.open_by_key("1YbHGr9Tt3xo5ri03iZrGi-rnpE_R4_arcGVOckH6unk")


def get_times_sut():
    entrys_st1 = sh.worksheet('СУББОТА').get('B2:B25')
    entrys_st2 = sh.worksheet('СУББОТА').get('D2:D25')
    write_to_exam_st = {
        '08:00 - 10:00': (2, 2, entrys_st1[0:8]),
        '10:00 - 12:00': (2, 10, entrys_st1[8:16]),
        '12:00 - 14:00': (2, 18, entrys_st1[16:24]),
        '14:00 - 16:00': (4, 2, entrys_st2[0:8]),
        '16:00 - 18:00': (4, 10, entrys_st2[8:16]),
    }
    return write_to_exam_st


def get_time_sun():
    entrys_sun1 = sh.worksheet('ВОСКРЕСЕНЬЕ').get('B2:B25')
    entrys_sun2 = sh.worksheet('ВОСКРЕСЕНЬЕ').get('D2:D25')
    write_to_exam_sun = {
        '08:00 - 10:00': (2, 2, entrys_sun1[0:8]),
        '10:00 - 12:00': (2, 10, entrys_sun1[8:16]),
        '12:00 - 14:00': (2, 18, entrys_sun1[16:24]),
        '14:00 - 16:00': (4, 2, entrys_sun2[0:8]),
        '16:00 - 18:00': (4, 10, entrys_sun2[8:16]),
    }
    return write_to_exam_sun


def sign_up_to_exam(data, second=False):
    print(data['name'])

