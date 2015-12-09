from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest
from wechat_response.models import *
import json
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def register(request):
	user_sex = request.POST.get("sex")
	user_age = request.POST.get("age")
	user_height = request.POST.get("height")
	user_wight = request.POST.get("weight")
	user_goal = request.POST.get("goal_step")
	user_openid = request.POST.get("openid")
	print user_openid
	if RingUser.objects.filter(user_id=user_openid).exists():
		user = RingUser.objects.filter(user_id=user_openid)[0]
		user.sex = user_sex
		user.age=user_age
		user.height=user_height
		user.weight=user_wight
		user.target=user_goal
		user.save()
	else:
		user_new = RingUser(
			user_id=user_openid,
			sex=user_sex,
			age=user_age,
			height=user_height,
			weight=user_wight,
			target=user_goal,
			last_record=0
		)
		user_new.save()
	return HttpResponse("add info successfully")


def sleepData(request, openid):
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
