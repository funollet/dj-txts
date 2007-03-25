from django.conf.urls.defaults import *
from photostream.models import PhotoStream

photostream_dict = { 'queryset': PhotoStream.objects.filter(is_defunct=False) }

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', 'object_list', photostream_dict),
)

