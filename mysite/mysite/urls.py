from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^weixin', 'mysite.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^2048', 'mysite.views.play_game'),
    url(r'^flappy_bird', 'mysite.views.play_bird'),
]


