# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns
from txts.models import Txt


date_based_params = {
    'queryset': Txt.public.all(), 
    'date_field': 'pub_date',
}


urlpatterns = []
urlpatterns += patterns('',
    (r'^tag/(?P<tag>[^/]+(?u))/$', 'tagging.views.tagged_object_list', 
        dict( model=Txt, allow_empty=True, template_name='txts/tag_list.html', ),
    )
)


urlpatterns += patterns('txts.views',
    (r'^preview/$', 'preview',),        # works if dj-txts URL is  / 
    (r'^txts/preview/$', 'preview',),   # works if dj-txts URL is  /txts/
    #
    # Date-based archives.
    (r'^(?P<section>[\-\w]+)/(?P<year>\d{4})/$',
        'date_based.archive_year', date_based_params,
    ),
    (r'^(?P<section>[\-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        'date_based.archive_month', dict( date_based_params, month_format='%m', ), 
    ),
    (r'^(?P<section>[\-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        'date_based.archive_day', dict( date_based_params, month_format='%m', ), 
    ),
    #
    # List-based views.
    (r'^(?P<section>[\-\w]+)/$', 'list_detail.object_list',
        dict( queryset=Txt.public.all(), ),
    ),
    (r'^(?P<section>[\-\w]+)/(?P<slug>[\-\w]+)/$', 'list_detail.object_detail',
         dict( queryset=Txt.public.all(), slug_field='easyname', ),
    ),

)
