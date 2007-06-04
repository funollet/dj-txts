# -*- coding:utf-8 -*-
from django.conf.urls.defaults import *
from txts.models import Txt, TxtSection

info_dict = { 
    'queryset': Txt.public.all(), 
}

archive_dict = {
    'date_field': 'pub_date',
    'queryset': Txt.public.all(),
}
date_dict = dict( archive_dict, month_format='%m', slug_field='permalink' )

urlpatterns = patterns('txts.views',
    (r'^(?P<section>[\-\w]+)/$',
        'list_detail_object_list', info_dict,
    ),
    (r'^(?P<section>[\-\w]+)/(?P<slug>[\-\w]+)/$',
        'list_detail_object_detail', dict(info_dict, slug_field="permalink"),
    ),
    # <section>/<year>/<month>/<day>/<permalink>/
    (r'^(?P<section>[\-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\-\w]+)/$',
        'date_based_object_detail', date_dict,
    ),
)

urlpatterns += patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/blog/'}),
)
