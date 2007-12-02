# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from txts.models import Txt, TxtSection


urlpatterns = []
urlpatterns += patterns('',
    (r'^tag/(?P<tag>[^/]+(?u))/$', 'tagging.views.tagged_object_list', 
        dict( model=Txt, allow_empty=True, template_name='txts/tag_list.html', ),
    )
)
urlpatterns += patterns('txts.views',
    (r'^preview/$', 'preview',),
    #
    (r'^(?P<section>[\-\w]+)/$', 'list_detail_object_list',
        dict( queryset=Txt.public.all(), ),
    ),
    (r'^(?P<section>[\-\w]+)/(?P<slug>[\-\w]+)/$', 'list_detail_object_detail',
         dict( queryset=Txt.public.all(), slug_field='easyname', ),
    ),
    # <section>/<year>/<month>/<day>/<easyname>/
    (r'^(?P<section>[\-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\-\w]+)/$',
        'date_based_object_detail',
        dict( queryset=Txt.public.all(), date_field='pub_date', month_format='%m', 
            slug_field='easyname', ),
    ),
)
