from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^$', 'mywiki.gui.views.index'),
    (r'^searchbar/$', 'mywiki.gui.views.searchbar'),
    (r'^keyword/(?P<article>.+?)/?$', 'mywiki.gui.views.keyword'),
    (r'^search/(?P<article>.+?)/?$', 'mywiki.gui.views.search'),
    (r'^article/(?P<article>.+)$', 'mywiki.gui.views.article'),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../mediawiki_sa/images/math'}),

    # Uncomment this for admin:
    #(r'^admin/', include('django.contrib.admin.urls')),
)
