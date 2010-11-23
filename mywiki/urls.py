from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$', 'mywiki.gui.views.index'),
                       (r'^searchbar/$', 'mywiki.gui.views.searchbar'),
                       (r'^keyword/(?P<article>.+?)/?$', 'mywiki.gui.views.keyword'),
                       (r'^search/(?P<article>.+?)/?$', 'mywiki.gui.views.search'),
                       (r'^article/(?P<article>.+)$', 'mywiki.gui.views.article'),
                       (r'^scripts/images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../mediawiki_sa/images/'}),
                       (r'^scripts/skins/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../mediawiki_sa/skins/'}),
                       )
