from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^hello', 'mysite.views.hello'),
    url(r'^weixin', 'mysite.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^TodayChart/(.*)', 'mysite.views.today_chart'),
    url(r'^YesterdayChart/(.*)', 'mysite.views.yesterday_chart'),
    url(r'^LastWeekChart/(.*)', 'mysite.views.last_week_chart'),
]


