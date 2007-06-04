from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from misc.markup import parser


@user_passes_test(lambda u: u.is_staff)
def parse_markup_fields (request):
    """For every field received via POST and with a name ending in '_markup',
    parses the value and renders with "txts/preview.html" template.
    
    objects: list of parsed objects (dicts) given to the template.
    
    objects.items() keys are ('name', 'data').
    """
    
    parsed_fields = []
    for k,v in request.POST.items():
        # Parse fields containing markup (and not voids).
        if '_markup' in k and request[k] != '':
            parsed_fields.append ({ 'name': k[:-7], 'data': parser(v) })
    
    return render_to_response ('txts/preview.html', {'objects': parsed_fields})
