# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat.models import *
from settings import *
from wechat_sdk.messages import (
    EventMessage
)
import urllib2
import json
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')


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
                            'url': SERVER_IP + '2048'}])
                    return HttpResponse(response)

                elif message.key == 'FLAPPY':
                    response = we_chat.response_news([{
                            'title': u'Let us play Flappy Bird together',
                            'description': 'a simple but interesting game',
                            'picurl': 'http://7xn2s5.com1.z0.glb.clouddn.com/flappy_bird.jpg',
                            'url': SERVER_IP + 'flappy_bird'}])
                    return HttpResponse(response)
                elif message.key == 'USER_INFO':
                    print message.source
                    response = we_chat.response_news([{
                            'title': u'Welcome to Treasure Ring',
                            'description': 'a userful ring',
                            'picurl': 'http://7xn2s5.com1.z0.glb.clouddn.com/info.jpg',
                            'url': SERVER_IP + 'register/' + message.source}])
                    return HttpResponse(response)

                elif message.key == 'CHART':
                    step_array = Record.objects.filter(user=message.source)
                    if step_array:
                        response = we_chat.response_news([{
                            'title': u'Today\'s amount of exercise',
                            'description': 'data analysis',
                            'picurl': 'http://7xn2s5.com1.z0.glb.clouddn.com/ez.png',
                            'url': SERVER_IP + 'TodayChart/' + message.source}])
                        return HttpResponse(response)
                    else:
                        response = we_chat.response_text(u'Sorry, there\' no data about you in our database.')
                        return HttpResponse(response)


@csrf_exempt
def play_game(request):
    return render_to_response('2048.html')


def play_bird(request):
    return render_to_response('bird.html')


@csrf_exempt
def register(request):
    if request.method == 'GET':
        return render_to_response('register.html')
    else:
        user_sex = request.POST.get("sex")
        user_age = request.POST.get("age")
        user_height = request.POST.get("height")
        user_wight = request.POST.get("weight")
        user_goal = request.POST.get("goal_step")
        user_info = RingUser(
            user_id=1,
            sex=user_sex,
            age=user_age,
            height=user_height,
            weight=user_wight,
            target=user_goal,
            last_record=0
        )
        user_info.save()
        return HttpResponse("add book successfully")


def create_menu():
    get_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID,AppSecret)
    f = urllib2.urlopen(get_url)
    string_json = f.read()
    access_token = json.loads(string_json)['access_token']
    post_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token
    print post_url
    request = urllib2.urlopen(post_url, (MENU % SERVER_IP).encode('utf-8'))
    print request.read()
