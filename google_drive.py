import os
import json
import gspread
from settings import ANSWER_TYPE_FREE, ANSWER_TYPE_OK
from oauth2client.service_account import ServiceAccountCredentials


class Sheet:
    scopes = ['https://spreadsheets.google.com/feeds']
    sheets = dict()

    def __init__(self):
        self.json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
        self.creds_dict = json.loads(self.json_creds)
        self.creds_dict["private_key"] = self.creds_dict["private_key"].replace("\\\\n", "\n")
        self.creds = ServiceAccountCredentials.from_json_keyfile_dict(self.creds_dict, self.scopes)
        self.client = gspread.authorize(self.creds)

    def open_sheet(self, **kwargs):
        if not 'sheet_link' in kwargs:
            return False

        self.spreadsheet = self.client.open_by_url(kwargs['sheet_link'])
        return self

    def get_first_list(self, **kwargs):
        self.sheets['1'] = self.spreadsheet.sheet1
        records = self.sheets['1'].get_all_records()
        items = []
        help_items = []
        result = ''

        for record in records:
            if not 'column' in kwargs:
                for line in record:
                    if str(record[kwargs['column']]) != '':
                        items.append(str(record[line]))
                        result += str(record[line])
                    break
            else:
                if str(record[kwargs['column']]) != '':
                    items.append(str(record[kwargs['column']]))
                    result += str(record[kwargs['column']])

                if 'help_column' in kwargs:
                    column_name = kwargs['column'] + kwargs['help_column']
                    if str(record[column_name]) != '':
                        help_items.append(str(record[column_name]))

        if 'return_test' in kwargs:
            return result
        if 'return_items' in kwargs:
            if 'help_column' in kwargs:
                return {'items': items, 'help_items': help_items, }
            return items
        if 'return_records' in kwargs:
            return records

        return self.sheets['1']


def get_column_type_options():
    return [ANSWER_TYPE_FREE, ANSWER_TYPE_OK]
