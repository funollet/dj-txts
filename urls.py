from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^r/', include('django.conf.urls.shortcut')),
    (r'^admin/', include('django.contrib.admin.urls')),
    #
    (r'^links/', include('djapps.links.urls')),
    (r'^events/', include('djapps.events.urls')),
    (r'^', include('djapps.txts.urls')),
)


if settings.LOCAL_DEV:
    urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT,
       'show_indexes': True, }),
) + urlpatterns


