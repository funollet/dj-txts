# -*- coding:utf-8 -*-
"""
Generic views wrapped to implement per-section treatment: only renders items from
the section selected and uses a custom template for this section.

If the section name is on the 'settings.SECTIONS_WITH_CUST_TMPL' list, the template_name
will be overwriten with '<app_label>/<section_name>_xxx.html' instead of '<app_label>/<model_name>_xxx.html'. This template **must** exist.
"""


from django.views.generic import date_based, list_detail
from django.conf import settings
from misc.markup import parser
from django.shortcuts import render_to_response


# Map wrapped function name to suffix that should be used
# for template name.
template_view_suffix = {
    'list_detail_object_list': 'list',
    'list_detail_object_detail': 'detail',
    'date_based_archive_index': 'archive',
    'date_based_archive_year': 'archive_year',
    'date_based_archive_month': 'archive_month',
    'date_based_archive_week': 'archive_week',
    'date_based_archive_day': 'archive_day',
    'date_based_archive_today': 'archive_today',
    'date_based_object_detail': 'detail',
}


def section_filter (func):
    """Generic view's decorator. Filters entries for some section
    and uses a custom template.
    """

    def filter_some_sections (*args, **k):
        
        # No section? Do nothing.
        if k.has_key('section'):
            # Add filter to queryset, get only this section items.
            k['queryset'] = k['queryset'].filter( section__name = k['section'] )
            # Should this section have an special template?
            if k['section'] in cust_tmpl:
                # Use a custom template name for this section.
                app_label = k['queryset'].model._meta.app_label
                suffix = template_view_suffix[func.__name__]
                k['template_name'] = '%s/%s_%s.html' % (app_label, k['section'], suffix)
            
            # Generic views doesn't expect a 'section' argument.
            del k['section']

        return func(*args, **k)

    cust_tmpl = getattr (settings, 'SECTIONS_WITH_CUST_TMPL', [])
    return filter_some_sections


# object_detail generic views

@section_filter
def list_detail_object_list (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return list_detail.object_list (request, **kwargs)

@section_filter
def list_detail_object_detail (request, **kwargs):
    return list_detail.object_detail (request, **kwargs)

# date_based generic views

@section_filter
def date_based_archive_index (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.archive_index (request, **kwargs)

@section_filter
def date_based_archive_year (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.archive_year (request, **kwargs)

@section_filter
def date_based_archive_month (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.archive_month (request, **kwargs)

@section_filter
def date_based_archive_week (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.archive_week (request, **kwargs)

@section_filter
def date_based_archive_day (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.archive_day (request, **kwargs)

@section_filter
def date_based_archive_today (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.archive_today (request, **kwargs)

@section_filter
def date_based_object_detail (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.object_detail (request, **kwargs)




def preview (request):
    """Renders a preview of some object; returns HTML wich will be inserted into Admin."""
    c = {}
    if request.has_key('name'): 
        c['name'] = request['name']
    if request.has_key('abstract_markup'): 
        c['abstract'] = parser(request['abstract_markup'])
    if request.has_key('body_markup'): 
        c['body'] = parser(request['body_markup'])
    
    return render_to_response ('txts/preview.html', c)