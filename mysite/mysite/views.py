# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from wechat_sdk import WechatBasic
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from database_request import *
from wechat.models import *
from django.template.loader import get_template
from django.template import Context
from settings import WECHAT_TOKEN, SERVER_IP, AppID, AppSecret
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import *
import time
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)


@csrf_exempt
def index(request):
 
    # 实例化 We_chat_Basic
    we_chat = WechatBasic(
        token=WECHAT_TOKEN,
        appid=AppID,
        appsecret=AppSecret
    )
    if request.method == "GET":
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if not we_chat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponse("Verify failed")
        else:
            return HttpResponse(request.GET.get("echostr"), content_type="text/plain")
    else:
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if not we_chat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponse("Verify failed")
        try:
            we_chat.parse_data(data=request.body)
        except ParseError:
            return HttpResponseBadRequest('Invalid XML Data')
        message = we_chat.get_message()
        if isinstance(message, EventMessage):
            if message.type == 'click':
                if message.key == 'STEP_COUNT':
                    step_array = Record.objects.filter(user=message.source)
                    if step_array:
                        step = step_array[len(step_array) - 1].step
                        response = we_chat.response_text(u'跑了' + str(step) + u'步咯')
                        # 里面的数字应由其他函数获取
                        return HttpResponse(response)
                    else:
                        response = we_chat.response_text(u'Sorry, there\' no data about you in our database.')
                        return HttpResponse(response)
                if message.key == 'CHART':
                    print 1
                    response = we_chat.response_news([{
                        'title': u'Today\'s amount of exercise',
                        'description': 'data analysis',
                        'picurl': 'http://7xn2s5.com1.z0.glb.clouddn.com/ez.png',
                        'url': SERVER_IP + 'TodayChart/' + message.source}])
                    return HttpResponse(response)
        response = we_chat.response_text(u'Cheer up!')
        return HttpResponse(response)


@csrf_exempt
def today_chart(request, user):
    data = Record.objects.filter(user=user)
    i = 0
    length = len(data)
    if length > 0:
        last = length - 1
        today = data[last].time.day
        while i < length:
            if data[i].time.day == today:
                today_start = i
                break
            i += 1

        all_steps = data[last].step - data[today_start].step
        most_recent = data[last].time.time().strftime("%H:%M:%S")
        least_recent = data[today_start].time.time().strftime("%H:%M:%S")
        first_time = data[today_start].time
        data = data[today_start:length]
        info = []
        length = len(data)
        for i in range(0, length):
            if i == 0:
                info.append([0, data[0].step])
            else:
                info.append([(data[i].time - first_time).seconds, data[i].step - data[i - 1].step])
        return render_to_response('TodayChart.html', {
            "user": user,
            "data": data,
            "info": info,
            "all_steps": all_steps,
            "least_recent": least_recent,
            "most_recent": most_recent,
        }, context_instance=RequestContext(request))
    else:
        return render_to_response('noData.html', {
            "user":user,
        }, context_instance=RequestContext(request))


def yesterday_chart(request, user):
    data = Record.objects.filter(user=user)
    i = 0
    length = len(data)
    if length > 0:
        last = length - 1
        yesterday = data[last].time.day - 2
        flag = 0
        while i < length:
            if data[i].time.day == yesterday and flag == 0:
                yesterday_start = i
                flag = 1
            elif data[i].time.day != yesterday and flag == 1:
                last = i
                break;
            i += 1

        all_steps = data[last].step - data[yesterday_start].step
        end_time = data[last].time.time().strftime("%H:%M:%S")
        start_time = data[yesterday_start].time.time().strftime("%H:%M:%S")
        first_time = data[yesterday_start].time
        data = data[yesterday_start:last]
        info = []
        length = len(data)
        for i in range(0, length):
            if i == 0:
                info.append([0, data[0].step])
            else:
                info.append([(data[i].time - first_time).seconds, data[i].step - data[i - 1].step])
        return render_to_response('YesterdayChart.html', {
            "user": user,
            "data": data,
            "info": info,
            "all_steps": all_steps,
            "start_time": start_time,
            "end_time": end_time,
        }, context_instance=RequestContext(request))
    else:
        return render_to_response('noData.html', {
            "user":user,
        }, context_instance=RequestContext(request))


def last_week_chart(request, user):
    data = Record.objects.filter(user=user)
    info = []
    i = 0
    length = len(data)
    if length > 0:
        last = length - 1
        last_today = data[last].time.day - 2
        while i < length:
            if data[i].time.day == last_today:
                start_day = i
                break
            i += 1
        all_steps = data[last].step - data[start_day].step
        j = 0
        i = start_day
        day = last_today
        while i < length and j < 7:
            last_day_step = data[i].step
            while data[i].time.day == day and i < length - 1:
                i += 1
            j += 1
            day += 1
            info.append([j, data[i].step - last_day_step])

        return render_to_response('LastWeekChart.html', {
            "user": user,
            "info": info,
            "data": data,
            "all_steps": all_steps,
        }, context_instance=RequestContext(request))
    else:
        return render_to_response('noData.html', {
            "user": user,
        }, context_instance=RequestContext(request))