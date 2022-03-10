import gspread
from ..google_api import drive


def connect_to_sheet():
    gc = gspread.service_account('apps/reg_for_trial_exam/google_api/client_secret.json')
    # gc = gspread.service_account('client_secret.json')
    sh = gc.open_by_key(drive.CURRENT_SHEETS_ID)
    return sh


def get_times_sut():
    sh = connect_to_sheet()
    entrys_st1 = sh.worksheet('СУББОТА').get('B2:B25')
    entrys_st2 = sh.worksheet('СУББОТА').get('D2:D25')
    write_to_exam_st = {
        '08:00 - 10:00': (2, 2, entrys_st1[0:8]),
        '10:00 - 12:00': (2, 10, entrys_st1[8:16]),
        '12:00 - 14:00': (2, 18, entrys_st1[16:24]),
        '14:00 - 16:00': (4, 2, entrys_st2[0:8]),
        '16:00 - 18:00': (4, 10, entrys_st2[8:16]),
    }
    return choice_free(write_to_exam_st)


def get_time_sun():
    sh = connect_to_sheet()
    entrys_sun1 = sh.worksheet('ВОСКРЕСЕНЬЕ').get('B2:B25')
    entrys_sun2 = sh.worksheet('ВОСКРЕСЕНЬЕ').get('D2:D25')
    write_to_exam_sun = {
        '08:00 - 10:00': (2, 2, entrys_sun1[0:8]),
        '10:00 - 12:00': (2, 10, entrys_sun1[8:16]),
        '12:00 - 14:00': (2, 18, entrys_sun1[16:24]),
        '14:00 - 16:00': (4, 2, entrys_sun2[0:8]),
        '16:00 - 18:00': (4, 10, entrys_sun2[8:16]),
    }
    return choice_free(write_to_exam_sun)


def choice_free(data: dict):
    need_delete = []
    for i, j in data.items():
        if j[2].count([]) == 0 and len(j[2]) == 8:
            need_delete.append(i)
    for delete in need_delete:
        data.pop(delete)
    return data


def sign_up_to_exam(data, second=False):
    sh = connect_to_sheet()
    first_column = data['first_free_places'][data['first_time']][0]
    first_begin_row = data['first_free_places'][data['first_time']][1]
    try:
        additive = data['first_free_places'][data['first_time']][2].index([])
    except ValueError:
        additive = len(data['first_free_places'][data['first_time']][2])
    first_row = first_begin_row + additive
    if not second:
        text = f"{data['name']} ({data['first_subject']} {data['type_exam'].upper()})"
        sh.worksheet(data['first_day'].upper()).update_cell(first_row, first_column, text)
        return

    second_column = data['second_free_places'][data['second_time']][0]
    second_begin_row = data['second_free_places'][data['second_time']][1]
    try:
        additive = data['second_free_places'][data['second_time']][2].index([])
    except ValueError:
        additive = len(data['second_free_places'][data['second_time']][2])
    second_row = second_begin_row + additive
    if first_column == second_column and first_row == second_row and data['first_day'] == data['second_day']:
        text = f"{data['name']} ({data['first_subject']} + {data['second_subject']}  {data['type_exam'].upper()})"
        sh.worksheet(data['first_day'].upper()).update_cell(first_row, first_column, text)
    else:
        first_text = f"{data['name']} ({data['first_subject']} {data['type_exam'].upper()})"
        sh.worksheet(data['first_day'].upper()).update_cell(first_row, first_column, first_text)
        second_text = f"{data['name']} ({data['second_subject']} {data['type_exam'].upper()})"
        sh.worksheet(data['second_day'].upper()).update_cell(second_row, second_column, second_text)


if __name__ == '__main__':
    pass
