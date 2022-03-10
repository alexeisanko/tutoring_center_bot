from pprint import pprint
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread
import datetime

# SERVICE_ACCOUNT_FILE = 'client_secret.json'
SERVICE_ACCOUNT_FILE = 'apps/reg_for_trial_exam/google_api/client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
CURRENT_SHEETS_ID = '1FbTL-j9cDHIxqT82ILTdDInIF4-xHSTajKFCUFAMrtM'
FORMAT_SHEETS_ID = '1FbTL-j9cDHIxqT82ILTdDInIF4-xHSTajKFCUFAMrtM'
FOLDER_ARCH_ID = '1YiPHC_J1O760CKZqg1Qb37TY1vHeFHxp'


def connect_api():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    return service


def copy_to_archive():
    gc = gspread.service_account(SERVICE_ACCOUNT_FILE)
    sh = gc.open_by_key(CURRENT_SHEETS_ID)
    arch_name = f'{sh.title.split()[-1]} архив'
    gc.copy(file_id=CURRENT_SHEETS_ID,
            title=f'{arch_name}',
            folder_id=FOLDER_ARCH_ID)
    gc.del_spreadsheet(CURRENT_SHEETS_ID)


def make_current_workbook():
    gc = gspread.service_account(SERVICE_ACCOUNT_FILE)
    near_saturday = datetime.datetime.now() + datetime.timedelta(days=(5 - datetime.datetime.now().weekday()))
    need_name = f'Запись на пробный экз на {near_saturday.strftime("%d.%m.%y")}'
    try:
        sh = gc.open(title=need_name)
        global CURRENT_SHEETS_ID
        CURRENT_SHEETS_ID = sh.id
    except:
        new_sh = gc.copy(file_id=FORMAT_SHEETS_ID,
                         title=need_name)
        new_sh.worksheet('СУББОТА').update_cell(1, 1, f'СУББОТА {near_saturday.strftime("%d.%m")}')
        new_sh.worksheet('ВОСКРЕСЕНЬЕ').update_cell(1,
                                                    1,
                                                    f'ВОСКРЕСЕНЬЕ {(near_saturday + datetime.timedelta(days=1)).strftime("%d.%m")}'
                                                    )
        global CURRENT_SHEETS_ID
        CURRENT_SHEETS_ID = new_sh.id
    return CURRENT_SHEETS_ID


if __name__ == '__main__':
    service = connect_api()
    results = service.files().list(pageSize=10,
                                   fields="nextPageToken, files(id, name, mimeType)").execute()
    nextPageToken = results.get('nextPageToken')
    while nextPageToken:
        nextPage = service.files().list(pageSize=10,
                                        fields="nextPageToken, files(id, name, mimeType, parents)",
                                        pageToken=nextPageToken).execute()
        nextPageToken = nextPage.get('nextPageToken')
        results['files'] = results['files'] + nextPage['files']
    pprint(results)
