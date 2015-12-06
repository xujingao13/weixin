# -*- coding: UTF-8 -*-

#for sleeping assess
import time
import numpy as np
import random as ran
from wechat_response.models import *

def get_data(type_list, start_time, end_time, user=0, type="", subType=""):
    param={'startTime':start_time, 'endTime':end_time, 'user':user}
    if type:
        param["type"] = type
        if subType:
            param["subType"] = subType
    req = requests.get(url='http://wrist.ssast2015.com/bongdata', params=param)
    data = json.loads(req.text)
    return_data = dict()
    for type_name in type_list:
        return_data[type_name] = []
    for val in data:
        for type_name in type_list:
            return_data[type_name].append(val[type_name])
    return return_data


#数据由三层结构构成
#type_list["distance", "score", "wakeNum", "dsNum", "calories", "subType", "nonActTime", "wakeTimes", "steps", "startTime", "actTime", "lsNum", "endTime", "type"]
'''startTime   该区块的开始时间，例如，用户早起跑步的跑步区块从 8:31 开始。
endTime 该区块的结束时间，例如这个用户跑了 20 分钟，那么区块结束时间是 8:51 分。通过块的划分，可以使用户和开发者均能方便对一天的活动状态做出归纳。
type    该区块的类型，用这个来区分bong和非bong状态。如果这个区段是bong态，则返回值是「2」，如果是比较平静的非bong态，则返回值是「3」。
distance    用户在该区段间走过的距离，单位是米。
speed   用户在该区段的平均运动速度，单位是千米每小时。
calories    用户在这段时间内消耗了多少热量，单位是千焦耳。
steps   该区段的步数，单位是步。
subType 该区段的子运动类型，bong态（当上文中提到的 type 为「2」时）下有4个子类型，具体描述见下，非bong态（type 为「3」时）下有2个子类型，具体描述见下。
actTime 该区段用户的活动时间，单位是秒。
nonActTime  该区段用户的非运动时间，单位是秒。
dsNum   深睡眠时长，单位：分钟
lsNum   浅睡眠时长，单位：分钟
wakeNum 清醒时长，单位：分钟
wakeTimes   清醒次数，单位：次
score   睡眠质量评分'''
#type=1(睡眠),type=2(bong),type=3(非bong)
#subType 1: 1 深睡眠 深度睡眠 2 浅睡眠 浅度睡眠 3 清醒 一次睡眠中的清醒状态
#subType 2: 1 热身运动 和字面意思相同，运动强度最轻的一类运动。2 健走 强度稍高。3 运动 球类等运动。4 跑步 有氧跑步运动。5 游泳 游泳等水中运动。6 自行车 骑车等。
#subType 3: 1 静坐  例如坐在椅子上办公。2 散步 速度相当于走路。3 交通工具 开车、乘公交等快速交通工具。4 活动 例如在办公室短时间走动
print(get_data(["wakeNum"], "2015-11-05 10:05:06", "2015-11-05 10:06:06", "1","3"))


# get "num" days list
def get_date_list(num):
    now_time = time.localtime()
    date = list()
    for i in range(num):
        date.append(str(now_time.tm_year) + "." + str(now_time.tm_mon) + "." + str(now_time.tm_mday))
        now_time = time.mktime(now_time)
        now_time -= 86400
        now_time = time.localtime(now_time)
    return date


def transfer_time(time_str):
    time_list = time_str.split(' ')
    year = time_list[0].strip()
    day = time_list[1].strip()
    year = year.split('-')
    day = day.split(':')
    time_list = [int(year[0]), int(year[1]), int(year[2]), int(day[0]), int(day[1]), int(day[2])]
    return time_list


# 把数据按天求和
def integrate_data(data, s_time, e_time):
    length = len(s_time)
    processing_day = list()
    new_day = list()
    new_data = list()
    temp_data = 0

    temp_day = transfer_time(s_time[0])
    processing_day = [temp_day[0], temp_day[1], temp_day[2], 0, 0, 0, 0, 0, 0]
    processing_day = time.mktime(time.struct_time(processing_day))
    new_day = [temp_day[0], temp_day[1], temp_day[2], 0, 0, 0, 0, 0, 0]
    new_day = time.mktime(time.struct_time(new_day))
    j = 0
    for i in range(length):
        temp_day = transfer_time(s_time[i])       
        new_day = time.mktime(time.struct_time([temp_day[0], temp_day[1], temp_day[2], 0, 0, 0, 0, 0, 0]))
        if new_day == processing_day:
            temp_data += data[i]
        else: 
            j += 1
            num_interval = int((new_day - processing_day) / 86400)
            temp_data /= num_interval
            for k in range(num_interval):
                new_data.append(temp_data)
            processing_day = new_day
            temp_data = 0
    length = len(new_data)
    residual = 30 -length
    if length > 0:
        temp_data = new_data[0] / (residual + 1)
        new_data[0] = residual
    else:
        temp_data = 0
    for i in range(residual):
        new_data.insert(0, temp_data)
    return new_data


def process_num(x):
    if x < 10:
        return "0" + str(x)
    else:
        return str(x)


# get sleep data for thirty days
def get_sleep_data(user):
    now_time = time.localtime()
    last_time = time.mktime(time.struct_time([now_time.tm_year, now_time.tm_mon, now_time.tm_mday, 12, 0, 0, 0, 0, 0]))
    last_time -= 86400 * 33
    last_time = time.localtime(last_time)
    start_time = process_num(last_time.tm_year) + "-" + process_num(last_time.tm_mon) + "-" + process_num(last_time.tm_mday) + " " + process_num(last_time.tm_hour) + ":" + process_num(last_time.tm_min) + ":" + process_num(last_time.tm_sec)
    end_time = process_num(now_time.tm_year) + "-" + process_num(now_time.tm_mon) + "-" + process_num(now_time.tm_mday) + " " + process_num(now_time.tm_hour) + ":" + process_num(now_time.tm_min) + ":" + process_num(now_time.tm_sec)
    data = get_data(["user", "dsNum", "lsNum", "startTime", "endTime"], start_time, end_time,  user.id)
    length = len(data["dsNum"])
    data["sleepNum"] = list()
    for i in range(length):
        data["sleepNum"].append(data["dsNum"][i] + data["lsNum"][i])
    data["dsNum"] = integrate_data(data["dsNum"], data["startTime"], data["endTime"])
    data["sleepNum"] = integrate_data(data["sleepNum"], data["startTime"], data["endTime"])
    data["date"] = get_date_list(30)
    return data


def get_exercise_data(user):
    now_time = time.localtime()
    last_time = time.mktime(time.struct_time([now_time.tm_year, now_time.tm_mon, now_time.tm_mday, 12, 0, 0, 0, 0, 0]))
    last_time -= 86400 * 33
    last_time = time.localtime(last_time)
    start_time = process_num(last_time.tm_year) + "-" + process_num(last_time.tm_mon) + "-" + process_num(last_time.tm_mday) + " " + process_num(last_time.tm_hour) + ":" + process_num(last_time.tm_min) + ":" + process_num(last_time.tm_sec)
    end_time = process_num(now_time.tm_year) + "-" + process_num(now_time.tm_mon) + "-" + process_num(now_time.tm_mday) + " " + process_num(now_time.tm_hour) + ":" + process_num(now_time.tm_min) + ":" + process_num(now_time.tm_sec)
    data = get_data(["user", "calories", "steps", "distance", "startTime", "endTime"], start_time, end_time,  user.id)
    #data["speed"] = integrate_data(data["speed"], data["startTime"], data["endTime"])
    data["distance"] = integrate_data(data["distance"], data["startTime"], data["endTime"])
    data["steps"] = integrate_data(data["steps"], data["startTime"], data["endTime"])
    data["calories"] = integrate_data(data["calories"], data["startTime"], data["endTime"])
    data["date"] = get_date_list(30)
    return data


# update the data of the particular user defined by parameter user
def get_save(user):
    last_time = time.localtime(user.last_record)
    start_time = process_num(last_time.tm_year) + "-" + process_num(last_time.tm_mon) + "-" + process_num(last_time.tm_mday) + " " + process_num(last_time.tm_hour) + ":" + process_num(last_time.tm_min) + ":" + process_num(last_time.tm_sec)
    now_time = time.localtime()
    end_time = process_num(now_time.tm_year) + "-" + process_num(now_time.tm_mon) + "-" + process_num(now_time.tm_mday) + " " + process_num(now_time.tm_hour) + ":" + process_num(now_time.tm_min) + ":" + process_num(now_time.tm_sec)
    data = get_data(["user", 'startTime', 'endTime', 'type', 'distance', 'calories', 'steps', 'subType', 'actTime', 'nonActTime', 'dsNum', 'lsNum', 'wakeNum', 'wakeTimes', 'score'], start_time, end_time, user.id)
    time_list = process_time_data(data["startTime"])
    save_data(data, time_list)
    new_record = time.time()
    if RingUser.objects.filter(user_id=user.user_id).exists():
        user_temp = RingUser.objects.filter(user_id=user.user_id)[0]
        user_new = RingUser(
            user_id=user_temp.openid,
            sex=user_temp.sex,
            age=user_temp.age,
            height=user_temp.height,
            weight=user_temp.wight,
            target=user_temp.goal,
            last_record=new_record
        )
        user_new.save()


# save data in the data base
def save_data(data, time_list):
    length = len(data["user"])
    for i in range(length):
        data_model = Record(
            user_name=str(data["user"][i]),
            startTime = time_list[i],
            endTime = time_list[i],
            type = data["type"][i],
            distance = data["distance"][i],
            calories = data["calories"][i],
            steps = data["steps"][i],
            subType = data["subType"][i],
            actTime = data["actTime"][i],
            nonActTime = data["nonActTime"][i],
            dsNum = data["dsNum"][i],
            lsNum = data["lsNum"][i],
            wakeNum = data["wakeNum"][i],
            wakeTimes = data["wakeTimes"][i],
            score = data["score"][i]
        )
        data_model.save()


# get data from the Internet and save in the database
def get_and_save_data(time_list, user_id=0, type="1", subType="1"):
    data = get_data(["user", 'startTime', 'endTime', 'type', 'distance', 'speed', 'calories', 'steps', 'subType', 'actTime', 'nonActTime', 'dsNum', 'lsNum', 'wakeNum', 'wakeTimes', 'score'], start_time, end_time, user_id, type, subType)
    save_data(data, time_list)


# transform the string time to integer time
def process_time_data(time_list):
    new_list = list()
    for val in time_list:
        time_temp = transfer_time(val)
        new_list.append(time.mktime(time.struct_time([time_temp[0], time_temp[1], time_temp[2], time_temp[3], time_temp[4], time_temp[5], 0, 0, 0])))
    return new_list


def assess_sleeping(user_id):
    '''now_time = time.localtime()
    seconds = time.time()
    if now_time[3] < 12:
        modified_time = seconds + (12 - now_time[3]) * 3600 - (now_time[4] * 60) - now_time[5]
        now_time = time.localtime(modified_time)
        yesterday_time = time.localtime(modified_time - 24 * 3600)
        data = get_data(["dsNum", "lsNum"], str(yesterday_time[0])+"-"+str(yesterday_time[1])+"-"+str(yesterday_time[2])+" "+"12:00:00", str(now_time[0])+"-"+str(now_time[1])+"-"+str(now_time[2])+" "+"12:00:00", "1")

    else:
        modified_time = seconds - ((now_time[3] - 12) * 3600 + (now_time[4] * 60) + now_time[5])'''

# get user information
    if RingUser.objects.filter(user_id=openid).exists():
        information = RingUser.objects.filter(user_id=openid)[0]
    else:
        return 0

    data = get_sleep_data(information)

# set variation threshold and fft threshold
    var_threshold = 1
    reg_threshold = 1

# get 30-day sleeping data and 7-day sleeping data
    data = []
    if ran.random() > 0.5:
        for i in range(30):
            data.append(ran.random() * 1.5 + 7)
    else:
        for i in range(30):
            if i % 7:
                data.append(7.2)
            else:
                data.append(5)
    thirty_sleep = np.array(data["sleepNum"][-30:])
    thirty_deep_sleep = np.array(data["dsNum"][-30:])
    seven_sleep = thirty_sleep[-7:]
    seven_deep_sleep = thirty_deep_sleep[-7:]

# computer statistical data
    report = dict()
    report["date"] = data["date"]
    report["30-days-sleep"] = thirty_sleep
    report["30-days-deep-sleep"] = thirty_deep_sleep
    report["30-days-avg"] = np.average(thirty_sleep)
    report["30-days-var"] = np.abs(np.var(thirty_sleep))
    report["30-days-reg"] = np.abs(np.fft.fft(thirty_sleep)[1:])
    report["30-days-deep-avg"] = np.average(thirty_deep_sleep)
    report["30-days-deep-rate"] = np.divide(thirty_deep_sleep, thirty_sleep)
    report["30-days-avg-rate"] = np.average(report["30-days-deep-rate"])

    report["7-days-sleep"] = seven_sleep
    report["7-days-deep-sleep"] = seven_deep_sleep
    report["7-days-max"] = seven_sleep.max()
    report["7-days-min"] = seven_sleep.min()
    report["7-days-avg"] = np.average(seven_sleep)
    report["7-days-var"] = np.abs(np.var(seven_sleep))
    report["7-days-deep-avg"] = np.average(seven_deep_sleep)
    report["7-days-avg-rate"] = np.average(report["30-days-deep-rate"][-7:])

# compare some data and get report
    # whether sleep enough
    if information.age > 60:
        if report["7-days-avg"] > 7:
            report["sleep-time-enough"] = 1
        elif report["7-days-avg"] < 5.5:
            report["sleep-time-enough"] = 2
        else:
            report["sleep-time-enough"] = 3
    elif 30 < information.age <= 60:
        if report["7-days-avg"] > 8:
            report["sleep-time-enough"] = 1
        elif report["7-days-avg"] < 5.5:
            report["sleep-time-enough"] = 2
        else:
            report["sleep-time-enough"] = 3
    elif 13 < information.age <= 30:
        if report["7-days-avg"] > 9:
            report["sleep-time-enough"] = 1
        elif report["7-days-avg"] < 5.5:
            report["sleep-time-enough"] = 2
        else:
            report["sleep-time-enough"] = 3
    elif 4 < information.age <= 13:
        if report["7-days-avg"] > 12:
            report["sleep-time-enough"] = 1
        elif report["7-days-avg"] < 5.5:
            report["sleep-time-enough"] = 2
        else:
            report["sleep-time-enough"] = 3
    elif information.age <= 4:
        report["sleep-time-enough"] = 4

    # 7 days compare with 30 days
    if report["7-days-avg"] < report["30-days-avg"] and report["sleep-time-enough"] == 2:
        report["avg-compare"] = 1
    elif report["7-days-avg"] > report["30-days-avg"] and report["sleep-time-enough"] == 1:
        report["avg-compare"] = 2
    else:
        report["avg-compare"] = 0

    # whether fluctuate severely
    if report["7-days-var"] > var_threshold:
        report["7-days-flac"] = 0
    else:
        report["7-days-flac"] = 1
    if report["30-days-var"] > var_threshold:
        report["30-days-flac"] = 0
    else:
        report["30-days-flac"] = 1

    # whether the deep sleep rate is enough
    if report["30-days-avg-rate"] < 0.25:
        report["30-deep-avg"] = 0
    else:
        report["30-deep-avg"] = 1

    if report["7-days-avg-rate"] < 0.25:
        report["7-deep-avg"] = 0
    else:
        report["7-deep-avg"] = 1

    # whether you're anxious recently
    if report["7-deep-avg"] == 0 and report["30-deep-avg"] == 1:
        report["anxious"] = 1
    elif report["30-deep-avg"] == 0 and report["7-deep-avg"] == 0:
        report["anxious"] = 2
    else:
        report["anxious"] == 0

    # whether sleep regularly
    if report["30-days-reg"] < reg_threshold:
        report["regular"] = 0;
    else:
        report["regular"] = 1;

    # whether you have stark sleeping
    if report["7-days-max"] > 12:
        report["stark-sleep"] = 1
    elif report["7-days-min"] < 3:
        report["stark-sleep"] = 2
    else:
        report["stark-sleep"] = 0


# assess your exercising data
def assess_exercising(user_id):
    information = get_user_information(user_id)
    data = get_exercise_data(user_id)

    report = dict()

# get statical data
    report["date"] = data["date"]
    report["7-days-dis"] = data["distance"][-7:]
    #report["7-days-speed"] = data["speed"][-7:]
    report["7-days-calories"] = data["calories"][-7:]
    report["7-days-steps"] = data["steps"][-7:]
    report["30-days-dis"] = data["distance"][-30:]
    #report["30-days-speed"] = data["speed"][-30:]
    report["30-days-calories"] = data["calories"][-30:]
    report["30-days-steps"] = data["steps"][-30:]

# compute exercising statical data
    report["7-days-dis-avg"] = np.average(data["distance"][-7:])
    #report["7-days-speed-avg"] = np.average(data["speed"][-7:])
    report["7-days-calories-avg"] = np.average(data["calories"][-7:])
    report["7-days-steps-avg"] = np.average(data["steps"][-7:])
    report["30-days-dis-avg"] = np.average(data["distance"])
    #report["30-days-speed-avg"] = np.average(data["speed"])
    report["30-days-calories-avg"] = np.average(data["calories"])
    report["30-days-steps-avg"] = np.average(data["steps"])

# compare data and get report
    # 0 female, 1 male
    if information["sex"] == 1:
        report["BMR"] = 13.7516 * information["weight"] + 5.0033 * information["height"] - 6.7550 * information["age"] + 66.4730
    elif information["sex"] == 0:
        report["BMR"] = 9.5634 * information["weight"] + 1.8496 * information["height"] - 4.6756 * information["age"] + 655.0955
    else:
        report["BMR"] = 0

    # BMR is the number of calories that you need every day if you don't exercise
    # Now compare the calories
    cb_rate = report["calories"][-1] / report["BMR"]
    report["yesterday-intensity"] = calc_intensity(cb_rate)
    cb_rate = report["7-days-calories-avg"][-1] / report["BMR"]
    report["7-days-intensity"] = calc_intensity(cb_rate)


def calc_intensity(cb_rate):
    if cb_rate < 0.2:
        intensity = 0
    elif 0.2 < cb_rate < 0.375:
        intensity = 1
    elif 0.375 < cb_rate < 0.55:
        intensity = 2
    elif 0.55 < cb_rate < 0.725:
        intensity = 3
    elif 0.725 < cb_rate < 0.9:
        intensity = 4
    return intensity

