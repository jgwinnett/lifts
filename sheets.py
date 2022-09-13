import gspread
import logging
from typing import List

class Sheets(object):
    def __init__(self, creds_path: str):
        self.creds_path = creds_path

    def auth(self):
        self.gc = gspread.service_account(filename=self.creds_path)
    
    def get_sheet_by_key(self, key: str) ->  gspread.spreadsheet.Spreadsheet:
        if (self.gc):
            return self.gc.open_by_key(key)
        else:
            try:
                self.auth()
                return self.gc.open_by_key(key)
            except(gspread.exceptions.APIError) as e:
                logging.exception(e)

    def get_0th_worksheet(self, spreadsheet: gspread.spreadsheet.Spreadsheet) ->  gspread.worksheet.Worksheet:
        return spreadsheet.get_worksheet(0)

    def get_all_worksheets(self, spreadsheet: gspread.spreadsheet.Spreadsheet) -> List[ gspread.worksheet.Worksheet]:
        return spreadsheet.worksheets()

    def getWorkSheet(self):
        self.auth()
        sheet = self.get_sheet_by_key('1XmPko5pbcw0HdvPZeL7Fw8tfX4zhvxREUDGISC54jwk')
        return self.get_0th_worksheet(sheet)  