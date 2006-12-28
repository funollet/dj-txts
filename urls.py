from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^r/', include('django.conf.urls.shortcut')),
    (r'^admin/', include('django.contrib.admin.urls')),
)


if settings.LOCAL_DEV:
    urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT,
       'show_indexes': True, }),
) + urlpatterns


