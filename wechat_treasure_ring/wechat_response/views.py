# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_response.models import *
from wechat_treasure_ring.settings import *
from wechat_sdk.messages import (
    EventMessage
)
import urllib2
import json
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')


@csrf_exempt
def weixin(request):
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
            create_menu()
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

                elif message.key == 'RANK_LIST':
                    response = RESPONSE_RANKLIST % (message.source, message.target)
                    return HttpResponse(response)  

                elif message.key == '2048':
                    response = we_chat.response_news([{
                            'title': u'Let us play 2048 together',
                            'description': 'a simple but interesting game',
                            'picurl': 'http://7xn2s5.com1.z0.glb.clouddn.com/2048.jpg',
                            'url': 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+AppID+'&redirect_uri=http%3a%2f%2f'+LOCAL_IP+'%2f2048.html'+'&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'}])
                    return HttpResponse(response)

                elif message.key == 'FLAPPY':
                    response = we_chat.response_news([{
                            'title': u'Let us play Flappy Bird together',
                            'description': 'a simple but interesting game',
                            'picurl': 'http://7xn2s5.com1.z0.glb.clouddn.com/flappy_bird.jpg',
                            'url': 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+AppID+'&redirect_uri=http%3a%2f%2f'+LOCAL_IP+'%2fbird.html'+'&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'}])
                    return HttpResponse(response)

                elif message.key == 'CHART':
                    response = we_chat.response_news([{
                        'title': u'Today\'s amount of exercise',
                        'description': 'data analysis',
                        'picurl': 'http://7xn2s5.com1.z0.glb.clouddn.com/info.jpg',
                        'url': 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+AppID+'&redirect_uri=http%3a%2f%2f'+LOCAL_IP+'%2fsleepAnalysis.html'+'&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'}])
                    return HttpResponse(response)

                elif message.key == 'CHEER':
                    response = we_chat.response_text(u'We are family!')
                    return HttpResponse(response)
            return HttpResponse('OK')


def get_openid(request, code):
    get_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(AppID,AppSecret,code)
    f = urllib2.urlopen(get_url)
    string_json = f.read()
    openid = json.loads(string_json)['openid']
    print openid
    return HttpResponse(json.dumps(openid))


@csrf_exempt
def create_menu():
    get_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID,AppSecret)
    f = urllib2.urlopen(get_url)
    string_json = f.read()
    access_token = json.loads(string_json)['access_token']
    post_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token
    request = urllib2.urlopen(post_url, (MENU % (USER_URL,RANK_URL)).encode('utf-8'))
    print request.read()
