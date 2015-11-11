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
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)


@csrf_exempt
def index(request):
# 下面这些变量均假设已由 Request 中提取完毕
    AppID = ''
    AppSecret = ''
 
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
            print message.source
            if message.type == 'click':
                if message.key == 'STEP_COUNT':
                    stepi = Record.objects.filter(user = message.source)
                    step = stepi[len(stepi) - 1].step
                    response = wechat.response_text(u'跑了' + str(step) + u'步咯')#里面的数字应由其他函数获取
                    return HttpResponse(response)
                if message.key == 'CHART':
                    response = wechat.response_news([{'title': message.source, 
                                        'description':'data analysis', 
                                        'picurl': 'http://7xn2s5.com1.z0.glb.clouddn.com/ez.png', 
                                        'url': SERVER_IP + 'chart/' + message.source}])
                    return HttpResponse(response)
        response = wechat.response_text(u'sheep94lion')
        return HttpResponse(response)

@csrf_exempt
def chart(request, user):
    AppID = ''
    AppSecret = ''
 
    # 实例化 WechatBasic
    wechat = WechatBasic(
        token=WECHAT_TOKEN,
        appid=AppID,
        appsecret=AppSecret
    )
    data = Record.objects.filter(user=user)
    print(user)
    last = len(data) - 1
    print last
    accuStep = data[last].step
    mostRecent =data[last].time.time()
    leastRecent = data[0].time.time()
    fstTime = data[0].time
    info = []
    print mostRecent
    for i in range(0, last + 1):
        if i == 0:
            info.append([0, data[0].step])
        else:
            info.append([(data[i].time - fstTime).seconds, data[i].step - data[i - 1].step])
    return render_to_response('index.html', {
        "user":user,
        "data":data,
        "info":info,
        "accuStep":accuStep,
        "leastRecent":leastRecent,
        "mostRecent":mostRecent,
    },context_instance=RequestContext(request))
