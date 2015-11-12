from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^hello', 'mysite.views.hello'),
    url(r'^weixin', 'mysite.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chart/(.*)', 'mysite.views.chart'),
    url(r'^goal/', 'mysite.views.goal'),
]


