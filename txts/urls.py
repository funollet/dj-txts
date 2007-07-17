# -*- coding:utf-8 -*-
from django.conf.urls.defaults import *
from txts.models import Txt, TxtSection

info_dict = { 
    'queryset': Txt.public.all().order_by('-pub_date'), 
}

archive_dict = {
    'date_field': 'pub_date',
    'queryset': Txt.public.all().order_by('-pub_date'),
}
date_dict = dict( archive_dict, month_format='%m', slug_field='easyname' )


urlpatterns = []
urlpatterns += patterns('txts.views',
    (r'^txt-preview/$', 'preview',),
    #
    (r'^(?P<section>[\-\w]+)/$',
        'list_detail_object_list', info_dict,
    ),
    (r'^(?P<section>[\-\w]+)/(?P<slug>[\-\w]+)/$',
        'list_detail_object_detail', dict(info_dict, slug_field='easyname'),
    ),
    # <section>/<year>/<month>/<day>/<easyname>/
    (r'^(?P<section>[\-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\-\w]+)/$',
        'date_based_object_detail', date_dict,
    ),
)

urlpatterns += patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', {
        'queryset': Txt.public.all().filter(section__easyname='blog'
            ).order_by('-pub_date')[:1],
        'template_name': 'txts/home_list.html',
    } ),
    #(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/blog/'}),
)
