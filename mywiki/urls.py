from django.conf.urls import patterns, url, include
import os

urlpatterns = patterns('',
                       (r'^$', 'mywiki.gui.views.index'),
                       (r'^(?P<lang>.*?)/searchbar/$', 'mywiki.gui.views.searchbar'),
                       (r'^(?P<lang>.*?)/keyword/(?P<article>.+?)/?$', 'mywiki.gui.views.keyword'),
                       (r'^(?P<lang>.*?)/search/(?P<article>.+?)/?$', 'mywiki.gui.views.search'),
                       (r'^(?P<lang>.*?)/article/(?P<article>.+?)/?$', 'mywiki.gui.views.article'),
                       (r'^dict/(?P<path>.*\.(css|js|ttf))$', 'django.views.static.serve', {'document_root': os.path.expanduser("~/src/github/ahd")}),
                       (r'^dict/dict-imagesx/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.expanduser("~/src/github/ahd/dict-imagesx")}),
                       (r'^dict/(?P<entry>.+)$', 'mywiki.gui.views.do_dict'),
                       (r'^scripts/images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../mediawiki_sa/images/'}),
                       (r'^scripts/skins/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../mediawiki_sa/skins/'}),
                       )
