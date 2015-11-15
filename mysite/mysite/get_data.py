# -*- coding: UTF-8 -*-

import requests
import json

def get_data(type_list, start_time, end_time, type="", subType=""):
    param={'startTime':start_time, 'endTime':end_time}
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