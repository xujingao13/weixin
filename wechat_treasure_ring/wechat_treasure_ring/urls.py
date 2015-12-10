"""wechat_treasure_ring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^weixin', 'wechat_response.views.weixin'),
    url(r'^data/getuserinfo', 'wechat_response.views.get_userinfo'),
    url(r'^data/register$', 'web_data.views.register'),
    url(r'^data/ifregistered/(.*)', 'web_data.views.ifregistered'),
    url(r'^data/sleepData', 'web_data.views.getSleepData'),
    url(r'^data/gamerank', 'web_data.views.game_rank'),
    url(r'^data/stepsinfo', 'web_data.views.steps_info'),
    url(r'^data/getsleepdata', 'web_data.views.get_sleepdata'),
    url(r'^data/getsportsdata', 'web_data.views.get_sportsdata')
]
