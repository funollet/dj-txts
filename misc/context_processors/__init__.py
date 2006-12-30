from django.conf import settings


def siteroot(request):
    """Makes available site_url and media_url on context, based on settings.SITE_URL
    and settings.MEDIA_URL.
    
    Usage:
      <a href="{{ site_url }}photos/"><img src="{{ media_url }}images/photo.gif" /></a>
    """
    context = {}

    try:
        context['site_url'] = settings.SITE_URL.strip()
    except AttributeError:
        try:
            from django.contrib.sites.models import Site
            context['site_url'] = Site.objects.get_current().domain
            if context['site_url'][-1] != '/':
                context['site_url'] += '/'
            if not context['site_url'].startswith('http://'):
                context['site_url'] = 'http://' + context['site_url']
        except ImportError:
            context['site_url'] = '/'

    try:
        context['media_url'] = settings.MEDIA_URL
    except AttributeError:
        context['media_url'] = ''

    return context
