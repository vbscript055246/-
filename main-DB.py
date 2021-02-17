import pymongo
import pandas as pd
import datetime
import sys
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
DBserver = pymongo.MongoClient('mongodb://localhost:27017/')
DB = DBserver['ir']
collection = DB['usermsgs']


output = []
df = pd.DataFrame(columns=['name', 'time_slot', 'mode', 'type', 'quiz_number', 'action_number'])

quiz_set_four = {1, 2, 4, 5}
quiz_set_six = {1, 2, 3, 4, 5, 6}

name_set = set(sorted([int(item['username']) for item in collection.find()]))
print(len(name_set))
print(name_set)

quiz_item = []

for name in name_set:

    class_flag = -1
    cut_flag = 0
    temp_set = set()
    temp_item = []
    for item in collection.find({'username': f"{str(name)}"}):

        if class_flag != item['quiz_class']:

            if not len(quiz_set_four.symmetric_difference(temp_set)):
                print("SET class flag")
                cut_flag = 1
            elif not len(quiz_set_six.symmetric_difference(temp_set)):
                print("SET class flag")
                cut_flag = 1

            if item['quiz_class'] == 3 or item['quiz_class'] == 6:
                temp_set.add(item['quiz_class'])
                class_flag = item['quiz_class']
                continue

            if cut_flag == 1:
                print("CUT")
                temp_set.clear()
                cut_flag = 0
                # input("pause")

            temp_set.add(item['quiz_class'])
            class_flag = item['quiz_class']

        temp_item.append(item)

    quiz_item.append(temp_item)
    print("End")
    # input("pause")

time_slot = []


for ind, item in enumerate(quiz_item):
    if len(time_slot) == 0:
        time_slot.append([ind])
        continue
    flag=1
    for j, current_time in enumerate(time_slot):
        if quiz_item[current_time[0]][0]['Msgdate'] - datetime.timedelta(minutes=8) <= item[0]['Msgdate'] <= quiz_item[current_time[0]][0]['Msgdate'] + datetime.timedelta(minutes=8):
            time_slot[j].append(ind)
            flag = 0
            break
    if flag:
        time_slot.append([ind])

print("number",len(time_slot))

[print(item) for item in time_slot]