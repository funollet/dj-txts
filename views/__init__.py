# -*- coding:utf-8 -*-
"""
Generic views wrapped to implement per-section treatment: only renders items from
the section selected and uses a custom template for this section.

If the section name is on the 'settings.SECTIONS_WITH_CUST_TMPL' list, the template_name
will be overwriten with '<app_label>/<section_name>_xxx.html' instead of '<app_label>/<model_name>_xxx.html'. This template **must** exist.
"""


from django.conf import settings


def section_aware (func):
    """Generic view's decorator. Restrict to entries in the given section
    and use a custom template.
    """

    def filter_and_custom_template (*args, **k):
        
        # Maps wrapped function name to suffix that should be used
        # for template name.
        overwrite_suffix = {
            'object_list': 'list',
            'object_detail': 'detail',
            'archive_index': 'archive',
        }
        
        # No section? Do nothing.
        if k.has_key('section'):
            # Add filter to queryset, get only this section's items.
            k['queryset'] = k['queryset'].filter( section__easyname = k['section'] )
            # Should this section have an special template?
            if k['section'] in cust_tmpl:
                # Use a custom template name for this section.
                suffix = func.__name__
                if overwrite_suffix.has_key(suffix):
                    suffix = overwrite_suffix[suffix]
                    
                app_label = k['queryset'].model._meta.app_label
                
                k['template_name'] = u'%s/%s_%s.html' % (app_label, k['section'], suffix)
            
            # Generic views doesn't expect a 'section' argument.
            del k['section']

        return func(*args, **k)


    cust_tmpl = getattr (settings, 'SECTIONS_WITH_CUST_TMPL', [])
    return filter_and_custom_template




from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
import markdown


@user_passes_test(lambda u: u.is_staff)
def preview (request):
    """Parses the value of the 'markup' field (POST). Used on the Admin
    preview button.
    """
    
    html = markdown.markdown ( request.POST['markup'] )
    return HttpResponse (html)
