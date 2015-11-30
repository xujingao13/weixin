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
            #create_menu()
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
                            'url': 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+AppID+'&redirect_uri=http%3a%2f%2f'+LOCAL_IP+'%2fregister.html'+'&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'}])
                            #'url': SERVER_IP + 'register.html'}])
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

                elif message.key == 'CHEER':
                    response = we_chat.response_text(u'We are family!')
                    return HttpResponse(response)

def get_openid(request, code):
    get_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(AppID,AppSecret,code)
    f = urllib2.urlopen(get_url)
    string_json = f.read()
    print  string_json
    openid = json.loads(string_json)['openid']
    print openid
    return HttpResponse(json.dumps(openid))
@csrf_exempt
def get_chart(request, user, dayFlag):
    data = Record.objects.filter(user=user)
    i = 0
    html = "noData.html"
    length = len(data)
    if length > 0:
        last = length - 1
        if dayFlag == "today":
            day = data[last].time.day
            html = "TodayChart.html"
        elif dayFlag == "yesterday":
            day = data[last].time.day - 2
            html = "YesterdayChart.html"

        flag = 0
        #'start' variable is the item in the database which stores the data whose day is the variable 'day' first
        while i < length:
            if data[i].time.day == day and flag == 0:
                start = i
                flag = 1
            elif data[i].time.day != day and flag == 1:
                break;
            i += 1
        last = i - 1
        #'last'variable is the item in the database which stores the data whose day is the variable 'day' last
        all_steps = data[last].step - data[start].step
        end_time = data[last].time.time().strftime("%H:%M:%S")
        start_time = data[start].time.time().strftime("%H:%M:%S")
        first_time = data[start].time
        data = data[start:last]
        info = []
        length = len(data)
        for i in range(0, length):
            if i == 0:
                info.append([0, data[0].step])
            else:
                info.append([(data[i].time - first_time).seconds, data[i].step - data[i - 1].step])
        return render_to_response(html, {
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


def today_chart(request, user):
    return get_chart(request, user, "today")


def play_game(request):
    return render_to_response('2048.html')


def play_bird(request):
    return render_to_response('bird.html')

@csrf_exempt
def register(request):
    user_sex = request.POST.get("sex")
    user_age = request.POST.get("age")
    user_height = request.POST.get("height")
    user_wight = request.POST.get("weight")
    user_goal = request.POST.get("goal_step")
    user_openid = request.POST.get("openid")
    print user_openid
    user_info = RingUser(
        user_id=user_openid,
        sex=user_sex,
        age=user_age,
        height=user_height,
        weight=user_wight,
        target=user_goal,
        last_record=0
    )
    user_info.save()
    return HttpResponse("add info successfully")





def yesterday_chart(request, user):
    return get_chart(request, user, "yesterday")


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


def create_menu():
    get_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID,AppSecret)
    f = urllib2.urlopen(get_url)
    string_json = f.read()
    access_token = json.loads(string_json)['access_token']
    post_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token
    print post_url
    request = urllib2.urlopen(post_url, (MENU % SERVER_IP).encode('utf-8'))
    print request.read()
