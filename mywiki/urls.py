from django.conf.urls.defaults import *
import os

urlpatterns = patterns('',
                       (r'^$', 'mywiki.gui.views.index'),
                       (r'^(?P<lang>.*?)/searchbar/$', 'mywiki.gui.views.searchbar'),
                       (r'^search-dict/$', 'mywiki.gui.views.searchdict'),
                       (r'^search-dict-defines/$', 'mywiki.gui.views.searchdict_def'),
                       (r'^search-dict-matching/$', 'mywiki.gui.views.searchdict_match'),
                       (r'^(?P<lang>.*?)/keyword/(?P<article>.+?)/?$', 'mywiki.gui.views.keyword'),
                       (r'^(?P<lang>.*?)/search/(?P<article>.+?)/?$', 'mywiki.gui.views.search'),
                       (r'^(?P<lang>.*?)/article/(?P<article>.+?)/?$', 'mywiki.gui.views.article'),
                       (r'^(search-)?dict/(?P<path>.*\.(css|js|ttf))$', 'django.views.static.serve', 
                        {'document_root': os.path.expanduser("~/src/ahd")}),
                       (r'^dict/dict-imagesx/(?P<path>.*)$', 'django.views.static.serve', 
                        {'document_root': os.path.expanduser("~/src/ahd/dict-imagesx")}),
                       (r'^(search-)?dict/(?P<entry>.+)$', 'mywiki.gui.views.do_dict'),
                       (r'^(search-)?dict-defines/(?P<entry>.+?)/?$', 'mywiki.gui.views.do_dict_defs'),
                       (r'^(search-)?dict-matching/(?P<entry>.+)$', 'mywiki.gui.views.do_dict_matching'),
                       (r'^dict-defines-sub/(?P<entry>.+?)/(?P<sub_entry>.*?)/?$', 'mywiki.gui.views.do_dict_defs_sub'),
                       (r'^dict-matching-sub/(?P<entry>.+?)/(?P<sub_entry>.*?)/?$', 'mywiki.gui.views.do_dict_matching_sub'),
                       (r'^dict-images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../../dict/JPG/'}),

                       (r'^dict-intro/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../../dict/extra/'}),
                       (r'^scripts/images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../mediawiki_sa/images/'}),
                       (r'^scripts/skins/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../mediawiki_sa/skins/'}),
                       )
