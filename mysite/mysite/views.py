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
from settings import WECHAT_TOKEN, SERVER_IP
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import *
import time
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)


@csrf_exempt
def index(request):
# 下面这些变量均假设已由 Request 中提取完毕
    AppID = 'wxbda096a619be4dd0'
    AppSecret = 'd4624c36b6795d1d99dcf0547af5443d'
 
    # 实例化 WechatBasic
    wechat = WechatBasic(
        token=WECHAT_TOKEN,
        appid=AppID,
        appsecret=AppSecret
    )
    if request.method == "GET":
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if not wechat.check_signature(signature = signature, timestamp = timestamp, nonce = nonce):
            return HttpResponse("Verify failed")
        else:
            return HttpResponse(request.GET.get('echostr'), content_type="text/plain")
    else:
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if False:#not wechat.check_signature(signature = signature, timestamp = timestamp, nonce = nonce):
            return HttpResponse("Verify failed")
        try:
            wechat.parse_data(data = request.body)
        except ParseError:
            return HttpResponseBadRequest('Invalid XML Data')
        message = wechat.get_message()
        if isinstance(message, EventMessage):
            if message.type == 'click':
                if message.key == 'STEP_COUNT':
                    stepi = Record.objects.filter(user = message.source)
                    if stepi:
                        step = stepi[len(stepi) - 1].step
                        response = wechat.response_text(u'跑了' + str(step) + u'步咯')#里面的数字应由其他函数获取
                        return HttpResponse(response)
                    else:
                        response = wechat.response_text(u'Sorry, there\' no data about you in our database.')
                        return HttpResponse(response)
                if message.key == 'CHART':
                    print 1
                    #userinfo = wechat.get_user_info(message.source)
                    #print userinfo
                    response = wechat.response_news([{'title':u'Today\'s amount of exercise',
                                        'description':'data analysis', 
                                        'picurl': 'http://7xn2s5.com1.z0.glb.clouddn.com/ez.png', 
                                        'url': SERVER_IP + 'TodayChart/' + message.source}])
                    return HttpResponse(response)
        response = wechat.response_text(u'Cheer up!')
        return HttpResponse(response)

@csrf_exempt
def TodayChart(request, user):
    AppID = ''
    AppSecret = ''
 
    # 实例化 WechatBasic
    wechat = WechatBasic(
        token=WECHAT_TOKEN,
        appid=AppID,
        appsecret=AppSecret
    )
    data = Record.objects.filter(user=user)
    i = 0
    length = len(data)
    if length > 0:
        last = length - 1
        Today = data[last].time.day
        while(i < length):
            if data[i].time.day == Today:
                Today_Start = i
                break
            i += 1

        accuStep = data[last].step - data[Today_Start].step
        mostRecent =data[last].time.time().strftime("%H:%M:%S")
        leastRecent =  data[Today_Start].time.time().strftime("%H:%M:%S")
        fstTime = data[Today_Start].time
        data = data[Today_Start:length]
        info = []
        length = len(data)
        for i in range(0, length):
            if i == 0:
                info.append([0, data[0].step])
            else:
                info.append([(data[i].time - fstTime).seconds, data[i].step - data[i - 1].step])
        return render_to_response('TodayChart.html', {
            "user":user,
            "data":data,
            "info":info,
            "accuStep":accuStep,
            "leastRecent":leastRecent,
            "mostRecent":mostRecent,
        },context_instance=RequestContext(request))
    else:
        return render_to_response('noData.html', {
            "user":user,
        },context_instance=RequestContext(request))

def YesterdayChart(request, user):
    AppID = ''
    AppSecret = ''

    # 实例化 WechatBasic
    wechat = WechatBasic(
        token=WECHAT_TOKEN,
        appid=AppID,
        appsecret=AppSecret
    )
    data = Record.objects.filter(user=user)
    i = 0
    length = len(data)
    if length > 0:
        last = length - 1
        Yesterday = data[last].time.day - 2
        flag = 0
        while(i < length):
            if data[i].time.day == Yesterday and flag == 0:
                Yesterday_Start = i
                flag = 1
            elif data[i].time.day != Yesterday and flag == 1:
                last = i
                break;
            i += 1

        accuStep = data[last].step - data[Yesterday_Start].step
        endTime =data[last].time.time().strftime("%H:%M:%S")
        startTime =  data[Yesterday_Start].time.time().strftime("%H:%M:%S")
        fstTime = data[Yesterday_Start].time
        data = data[Yesterday_Start:last]
        info = []
        length = len(data)
        for i in range(0, length):
            if i == 0:
                info.append([0, data[0].step])
            else:
                info.append([(data[i].time - fstTime).seconds, data[i].step - data[i - 1].step])
        return render_to_response('YesterdayChart.html', {
            "user":user,
            "data":data,
            "info":info,
            "accuStep":accuStep,
            "startTime":startTime,
            "endTime":endTime,
        },context_instance=RequestContext(request))
    else:
        return render_to_response('noData.html', {
            "user":user,
        },context_instance=RequestContext(request))

def LastWeekChart(request, user):
    AppID = ''
    AppSecret = ''

    # 实例化 WechatBasic
    wechat = WechatBasic(
        token=WECHAT_TOKEN,
        appid=AppID,
        appsecret=AppSecret
    )
    data = Record.objects.filter(user=user)
    info = []
    i = 0
    length = len(data)
    if length > 0:
        last = length - 1
        lastToday = data[last].time.day - 2
        while i < length:
            if data[i].time.day == lastToday:
                startDay = i
                break
            i += 1
        accuStep = data[last].step - data[startDay].step
        j = 0
        i = startDay
        day = lastToday
        while i < length and j < 7:
            lastDayStep = data[i].step
            while data[i].time.day == day and i < length - 1:
                i += 1
            j += 1
            day += 1
            info.append([j, data[i].step - lastDayStep])

        return render_to_response('LastWeekChart.html', {
            "user":user,
            "info":info,
            "data":data,
            "accuStep":accuStep,
        },context_instance=RequestContext(request))
    else:
        return render_to_response('noData.html', {
            "user":user,
        },context_instance=RequestContext(request))