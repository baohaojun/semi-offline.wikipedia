from django.conf.urls import url
import os
from . import views
from django.views.static import serve

urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<lang>.*?)/searchbar/$', views.searchbar),
    url(r'^(?P<lang>.*?)/keyword/(?P<article>.+?)/?$', views.keyword),
    url(r'^(?P<lang>.*?)/search/(?P<article>.+?)/?$', views.search),
    url(r'^(?P<lang>.*?)/article/(?P<article>.+?)/?$', views.article),
    url(r'^dict/(?P<path>.*\.(css|js|ttf))$', serve, {'document_root': os.path.expanduser("~/src/github/ahd")}),
    url(r'^dict/dict-imagesx/(?P<path>.*)$', serve, {'document_root': os.path.expanduser("~/src/github/ahd/dict-imagesx")}),
    url(r'^dict/(?P<entry>.+)$', views.do_dict),
    url(r'^scripts/images/(?P<path>.*)$', serve, {'document_root': '../mediawiki_sa/images/'}),
    url(r'^scripts/skins/(?P<path>.*)$', serve, {'document_root': '../mediawiki_sa/skins/'}),
]
