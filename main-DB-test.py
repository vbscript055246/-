import pymongo
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
DBserver = pymongo.MongoClient('mongodb://localhost:27017/')
DB = DBserver['ir']
collection = DB['usermsgs']

quiz_set_four = {1, 2, 4, 5}
quiz_set_six = {1, 2, 3, 4, 5, 6}

name_set = set(sorted([int(item['username']) for item in collection.find()]))
# print(len(name_set))
# print(name_set)

quiz_item = []
for name in name_set:

    class_flag = -1
    cut_flag = 0
    temp_set = set()
    temp_item = []
    for item in collection.find({'username': f"{str(name)}"}):

        if class_flag != item['quiz_class']:

            if not len(quiz_set_four.symmetric_difference(temp_set)):
                # print("SET class flag")
                cut_flag = 1
            elif not len(quiz_set_six.symmetric_difference(temp_set)):
                # print("SET class flag")
                cut_flag = 1

            if item['quiz_class'] == 3 or item['quiz_class'] == 6:
                temp_set.add(item['quiz_class'])
                class_flag = item['quiz_class']
                continue

            if cut_flag == 1:
                # print("CUT")
                temp_set.clear()
                cut_flag = 0
                # input("pause")

            temp_set.add(item['quiz_class'])
            class_flag = item['quiz_class']

        temp_item.append(item)

    quiz_item.append(temp_item)
    # print("End")
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


# df = pd.DataFrame(columns=['name', 'time_slot', 'mode', 'type', 'quiz_number', 'text'])
output = []
simple_stack = []
for ind, item in enumerate(time_slot):
    for i in sorted(item):
        simple_stack.append(i)
        if len(simple_stack)>1:
            if simple_stack[-1]%2-1 == simple_stack[-2]%2:
                temp_output=quiz_item[i]
                temp_output+=quiz_item[i-1]
                output.append(temp_output)
                simple_stack.pop()
                simple_stack.pop()


    while len(simple_stack):
        output.append(quiz_item[simple_stack[-1]])
        simple_stack.pop()

# for i in output:
#     print(i)

#  4 5 6 遠距 遠距聯想測驗.xlsx
raw = pd.read_excel('遠距聯想測驗.xlsx')
# print(raw[raw['版本'] == 1]['答案'][0])
# output = output[1:]
for item in output:
    _score = [0, 0]
    _record_score = [[], []]
    _record_time = [[], []]
    class_flag = -1

    if item[0]['Msgdate'] < datetime.datetime(year=2020, month=6, day=8):
        continue

    s = sorted(item, key=lambda x: x['Msgdate'])
    for i in range(len(item)):
        print(item[i]['Msgdate'], item[i]['username'], s[i]['Msgdate'], s[i]['username'])
    for ind, i in enumerate(s):
        if i['quiz_class'] > 3:
            if class_flag == -1:
                class_flag = i['quiz_class']

            if class_flag != i['quiz_class']:
                print(_score[0], _score[1])
                print(_record_score[0], _record_score[1])
                print(_record_time[0], _record_time[1])

                # ========================================================================

                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=10))
                plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=90)
                # Plot
                plt.plot(_record_time[0], _record_score[0], 'r-^')
                plt.plot(_record_time[1], _record_score[1], 'g-^')
                plt.show()

                _score = [0, 0]
                _record_score = [[], []]
                _record_time = [[], []]
                class_flag = -1
            else:
                try:
                    _tmp = raw[raw['版本'] == i['quiz_class']-3]['答案'].values[i['quiz_no']]
                except:
                    print(i['Msgdate'])
                    break
                # print(_tmp.strip())
                _score[int(i['username'])%2] += int(_tmp.strip() == i['quiz_ans'])
                _record_score[int(i['username'])%2].append(_score[int(i['username'])%2])
                _record_time[int(i['username'])%2].append(i['Msgdate'].strftime("%H:%M:%S"))
                class_flag = i['quiz_class']
    # d = {
    #         'name':[item['username']],
    #         'time_slot':[],
    #         'mode':[],
    #         'type':[],
    #         'quiz_number':[],
    #         'action_number':[]
    #     }
    # df.append(d)

    # print(datestr)

    # print(type(item))
# print(time_slot)
# print(len(time_slot))





