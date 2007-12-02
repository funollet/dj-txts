from django.views.generic import list_detail
from txts.views import section_aware

@section_aware
def object_list (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return list_detail.object_list (request, **kwargs)

@section_aware
def object_detail (request, **kwargs):
    return list_detail.object_detail (request, **kwargs)

