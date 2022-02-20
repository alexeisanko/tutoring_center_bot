from pprint import pprint

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'client_secret.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1YbHGr9Tt3xo5ri03iZrGi-rnpE_R4_arcGVOckH6unk'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

