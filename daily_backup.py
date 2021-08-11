import csv
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

dateToday = datetime.datetime.now() - datetime.timedelta(hours = 4) ## timezone, DST
updateDate = dateToday.strftime('%Y-%m-%d')
updateTime = dateToday.strftime('%Y-%m-%d %I:%M%p')
header = [["Last updated: " + updateTime]]


fileName = "Phase 1 Backup " + updateDate
bu = client.copy("1PAL7z9LPNHznS7ecE05MgDHn-w_nUKCSl6Chq6l18TQ",
                 title = fileName,
                 copy_permissions = True)

with open("itemized.csv") as infile: ## locally created snapshot of raw data
    reader = csv.reader(infile)
    items = [row for row in reader]

singleFile = header + items

bu.values_update('A1', params={'valueInputOption': 'USER_ENTERED'},
                    body={'values': singleFile})
