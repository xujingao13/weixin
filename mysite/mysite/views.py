# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from wechat_sdk import WechatBasic
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from database_request import *
from wechat.models import *
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)


@csrf_exempt
def index(request):
# 下面这些变量均假设已由 Request 中提取完毕
    WECHAT_TOKEN = 'sheep94lion'
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
            if message.type == 'click':
                if message.key == 'STEP_COUNT':
                    print 1
                    #steplist = get_data("step", "234")
                    print 3
                    #step = steplist[0][0]
                    #print step
                    print 2
                    stepi = Record.objects.get(user = u"oFX57wUb4ud1w9Naf2BXIBclGiSs")
                    step = stepi.step
                    response = wechat.response_text(u'跑了' + str(step) + u'步咯')#里面的数字应由其他函数获取
                    return HttpResponse(response)
                if message.key == 'CHART':
                    
                    print message.source
        response = wechat.response_text(u'sheep94lion')
        return HttpResponse(response)
        #print (request.POST['signature'])
    # 对签名进行校验
    """
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
        wechat.parse_data(data=request.body)
        # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
        message = wechat.get_message()

        response = None
        if message.type == 'text':
            if message.content == 'wechat':
                response = wechat.response_text(u'^_^')
            else:
                response = wechat.response_text(u'文字')
        elif message.type == 'image':
            response = wechat.response_text(u'图片')
        else:
            response = wechat.response_text(u'未知')
        return HttpResponse(response)
    else: return HttpResponse('wrong')
    """
