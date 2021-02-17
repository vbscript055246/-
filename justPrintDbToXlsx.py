import datetime
import os

import pandas as pd
import pymongo
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
try:
    DBserver = pymongo.MongoClient('mongodb://localhost:27017/')
    DB = DBserver['DataDB']     # 'DataDB' 'ir'
    collection = DB['usermsgs']
except Exception as e:
    print(e)
    print("DB連線失敗")
    os.system("pause")
    exit(1)

# 'username', 'mode', 'quiz_class', 'quiz_no', 'quiz_ans', 'Msgdate'
# "編號", "執行順序", "遠1單雙", "遠2單雙", "吸管單雙", "寶特瓶單雙", "遠1得分", "遠2得分", "遠3得分", "吸管流暢", "吸管變通", "吸管獨創", "寶特瓶流暢", "寶特瓶變通", "寶特瓶獨創"
try:
    output = []
    for item in collection.find():

        if ILLEGAL_CHARACTERS_RE.search(item['username']):
            print((item['Msgdate'] + datetime.timedelta(hours=8)).strftime("%Y/%m/%d, %H:%M:%S"))
            print(item['username'], 'username', sep=';')
        if ILLEGAL_CHARACTERS_RE.search(item['quiz_ans']):
            print((item['Msgdate'] + datetime.timedelta(hours=8)).strftime("%Y/%m/%d, %H:%M:%S"))
            print(item['quiz_ans'], 'quiz_ans', sep=';')

        data = [item['username'], item['mode'], item['quiz_class'], item['quiz_no'], item['quiz_ans'],
                (item['Msgdate'] + datetime.timedelta(hours=8)).strftime("%Y/%m/%d, %H:%M:%S")]

        output.append(data)
except Exception as e:
    print(e)
    print("DB讀取失敗")
    os.system("pause")
    exit(2)
try:
    if not os.path.exists('./output'):
        os.mkdir('output')
    if not os.path.exists('./output/Data ' + datetime.date.today().strftime("%Y.%m.%d")):
        os.mkdir('./output/Data ' + datetime.date.today().strftime("%Y.%m.%d"))

    file = pd.DataFrame(output, columns=["UserName", "Single/Double Mode", "Quiz Class", "Quiz #", "Ans", "Time"])
    s = './output/Data ' + datetime.date.today().strftime("%Y.%m.%d") + '/output.xlsx'

    file.to_excel(s, engine='xlsxwriter')
    print("done~")
    os.system("pause")
except Exception as e:
    print(e)
    print("資料寫入失敗")
    os.system("pause")
    exit(3)
# pyinstaller -F --clean --hidden-import xlsxwriter -i .\down.ico .\justPrintDbToXlsx.py