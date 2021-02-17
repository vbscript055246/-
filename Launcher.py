import os

from PyQt5.QtWidgets import QMainWindow, QApplication
import sys

from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

from Layout import *
import subprocess
import pandas as pd
import hashlib
import base64
import random
import pymongo
import webbrowser
from webbrowser import Chrome
import datetime
from win32api import ShellExecute

class WinForm(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(WinForm, self).__init__(parent)
        self.setupUi(self)

        self.startButton.clicked.connect(self.startServer)
        self.stopButton.clicked.connect(self.stopServer)
        self.makePWButton.clicked.connect(self.create_ID_PW)
        self.extractDBBtn.clicked.connect(self.backUpDataBase)
        self.restoreDBBtn.clicked.connect(self.restoreCollection)
        self.extractDBBtn2xlsx.clicked.connect(self.DB2xlsx)
        self.portBtn.clicked.connect(self.setPort)
        self.timerBtn.clicked.connect(self.setTimer)


        self.setWindowTitle("伺服器未啟動:port=8888")
        self.port = 8888
        self.timer = 600
        self.p = None

    def setTimer(self):

        try:
            if self.timerText.text().isalnum():
                self.timer = self.timerText.text()
                self.setWindowTitle("伺服器未啟動:port=" + str(self.port) + ", 作答時間: " + str(self.timer) + "秒")
        except:
            pass


    def setPort(self):
        try:
            if self.portText.text().isalnum():
                self.port = self.portText.text()
                self.setWindowTitle("伺服器未啟動:port=" + str(self.port) + ", 作答時間: " + str(self.timer) + "秒")
        except:
            pass

    def DB2xlsx(self):
        DBserver = pymongo.MongoClient('mongodb://localhost:27017/')
        DB = DBserver['DataDB']
        collection = DB['usermsgs']

        # 'username', 'mode', 'quiz_class', 'quiz_no', 'quiz_ans', 'Msgdate'
        # "編號", "執行順序", "遠1單雙", "遠2單雙", "吸管單雙", "寶特瓶單雙", "遠1得分", "遠2得分", "遠3得分", "吸管流暢", "吸管變通", "吸管獨創", "寶特瓶流暢", "寶特瓶變通", "寶特瓶獨創"

        output = {}
        for item in collection.find():
            datestr = (item['Msgdate'] + datetime.timedelta(hours=8)).strftime("%Y/%m/%d, %H")
            if output.get(datestr, -1) == -1:
                output[datestr] = []

            if ILLEGAL_CHARACTERS_RE.search(item['username']):
                print((item['Msgdate'] + datetime.timedelta(hours=8)).strftime("%Y/%m/%d, %H:%M:%S"))
                print(item['username'], 'username', sep=';')
            if ILLEGAL_CHARACTERS_RE.search(item['quiz_ans']):
                print((item['Msgdate'] + datetime.timedelta(hours=8)).strftime("%Y/%m/%d, %H:%M:%S"))
                print(item['quiz_ans'], 'quiz_ans', sep=';')

            data = [item['username'], item['mode'], item['quiz_class'], item['quiz_no'], item['quiz_ans'],
                    (item['Msgdate'] + datetime.timedelta(hours=8)).strftime("%Y/%m/%d, %H:%M:%S")]
            output[datestr].append(data)

        if not os.path.exists('./output'):
            os.mkdir('output')
        if not os.path.exists('./output/Data ' + datetime.date.today().strftime("%Y.%m.%d")):
            os.mkdir('./output/Data ' + datetime.date.today().strftime("%Y.%m.%d"))

        for datestr in output.keys():
            file = pd.DataFrame(output[datestr],
                                columns=["UserName", "Single/Double Mode", "Quiz Class", "Quiz #", "Ans", "Time"])
            s = './output/Data ' + datetime.date.today().strftime("%Y.%m.%d") + '/' + \
                (datestr.replace(", ", "-").replace("/", "-")) + '.xlsx'
            # print(s)
            file.to_excel(s, engine='xlsxwriter')
        print("done~")
        # ============================================================================================================================

        # output = []
        # counter = 0
        # preUN = ""
        # preMode = ""
        # pre
        # for item in collection.find():
        #
        # file = pd.DataFrame(output, columns=["UserName", "Single/Double Mode", "Quiz Class", "Quiz #", "Ans", "Time"])
        #


    def restoreCollection(self):
        try:
            command = 'mongorestore -h 127.0.0.1:27017 -d DataDB -dir ./DB-backup/DataDB'
            subprocess.Popen(command, shell=True)
        except:
            pass

    def backUpDataBase(self):
        try:
            command = 'mongodump -h 127.0.0.1:27017 -d DataDB -c usermsgs -o ./DB-backup/'
            subprocess.Popen(command, shell=True)
        except:
            pass


    def create_ID_PW(self):
        user = []
        DBserver = pymongo.MongoClient('mongodb://localhost:27017/')
        DB = DBserver['DataDB']
        collection = DB['users']
        if collection.count_documents({}):
            collection.drop()
        if collection.count_documents({'username': 'admin'}) == 0:
            collection.insert_one({'username': 'admin', 'password': 'admin'})

        for user_No in range(0, 1001):
            prefix = 'S'
            ID = prefix + str(user_No).zfill(3)
            hasher = hashlib.sha256(ID.encode())
            st = random.randint(0, len(hasher.digest()) - 4)
            PW = base64.b64encode(hasher.digest()[st:st + 4]).decode()
            collection.insert_one({'username': ID, 'password': PW})
            user.append([ID, PW])
        file = pd.DataFrame(user, columns=["Username", "Password"])
        file.to_excel('account.xlsx')


    def startServer(self):

        with open('./NodejsWebApp1/server.js', 'r', encoding='utf8') as f:
            file = f.readlines()
        file[0] = "port = " + str(self.port) + ";\n"
        for i in range(len(file)):
            if "startTimer(" in file[i] and "function" not in file[i]:
                file[i] = "\t\tstartTimer(" + str(self.timer) + ");\n"
                break

        # file[243] = "\t\tstartTimer(" +  str(self.timer) +");\n"    # TODO
        with open('./NodejsWebApp1/server.js', 'w', encoding='utf8') as f:
            f.writelines(file)

        if "1" in (subprocess.check_output('sc query "mongodb"').decode('utf-8').split('\r\n')[3]):
            ShellExecute(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c ' + "sc start MongoDB")

        command = 'node ./NodejsWebApp1/server.js'  # /NodejsWebApp1
        #self.p.communicate(command)
        self.p = subprocess.Popen(command, shell=True)
        webbrowser.register('chrome', Chrome('chrome'))
        webbrowser.open('http://localhost:'+ str(self.port) + '/admin')
        self.setWindowTitle("伺服器已啟動:port=" + str(self.port) + ", 作答時間: " + str(self.timer) + "秒")

    def stopServer(self):
        self.setWindowTitle("伺服器未啟動:port=" + str(self.port) + ", 作答時間: " + str(self.timer) + "秒")
        #self.p.kill()

        command = 'taskkill /pid ' + str(self.p.pid) + ' /T /f '
        subprocess.Popen(command, shell=True)


# pyinstaller -F -i .\[icon].ico .\Launcher.py
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = WinForm()
    form.show()
    sys.exit(app.exec_())