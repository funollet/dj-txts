from django.conf.urls.defaults import *
from django.conf import settings
from txts.feeds import *

feeds = {
    'blog': BlogEntries,
    'badopi': TagBadopi,
}


urlpatterns = patterns('',
    (r'^r/', include('django.conf.urls.shortcut')),
    (r'^admin/', include('django.contrib.admin.urls')),
    #
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^links/', include('links.urls')),
    (r'^events/', include('events.urls')),
    (r'^optics/', 'optics.views.search_optics' ),
    (r'^photoplanet/', include('photoplanet.urls')),
    (r'^preview/', 'misc.views.parse_markup_fields'),
    (r'^', include('txts.urls')),
)


if settings.LOCAL_DEV:
    urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT,
       'show_indexes': True, }),
) + urlpatterns


