from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from misc.markup import parser


@user_passes_test(lambda u: u.is_staff)
def parse_markup (request):
    """Parses the value of the 'markup' field (POST).
    """
    html = parser( request.POST['markup'] )
    return HttpResponse (html)
