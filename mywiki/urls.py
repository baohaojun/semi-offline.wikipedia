from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$', 'mywiki.gui.views.index'),
                       (r'^(?P<lang>.*?)/searchbar/$', 'mywiki.gui.views.searchbar'),
                       (r'^(?P<lang>.*?)/keyword/(?P<article>.+?)/?$', 'mywiki.gui.views.keyword'),
                       (r'^(?P<lang>.*?)/search/(?P<article>.+?)/?$', 'mywiki.gui.views.search'),
                       (r'^(?P<lang>.*?)/article/(?P<article>.+?)/?$', 'mywiki.gui.views.article'),
                       (r'^dict/(?P<entry>.+)$', 'mywiki.gui.views.do_dict'),
                       (r'^dict-defines/(?P<entry>.+?)/?$', 'mywiki.gui.views.do_dict_defs'),
                       (r'^dict-defines-sub/(?P<entry>.+?)/(?P<sub_entry>.*?)/?$', 'mywiki.gui.views.do_dict_defs_sub'),
                       (r'^dict-images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../../dict/res/'}),
                       (r'^scripts/images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../mediawiki_sa/images/'}),
                       (r'^scripts/skins/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../mediawiki_sa/skins/'}),
                       )
