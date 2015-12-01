from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest
from wechat_response.models import *
import json
def ifregistered(request, openid):
	if RingUser.objects.filter(user_id=openid).exists():
		user = RingUser.objects.filter(user_id=openid)[0]
		user_info = {
			"ifregistered": True,
			"sex": user.sex,
			"age": user.age,
			"height": user.height,
			"weight": user.weight,
			"goal_step": user.target,	
		}
		return HttpResponse(json.dumps(user_info))
	else:
		user_info = {"ifregistered": False}
		return HttpResponse(json.dumps(user_info))

# Create your views here.
