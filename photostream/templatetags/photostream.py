
from django import template
from terraquis.photostream.models import PhotoStream, PhotoStreamItem


class PhotoStreamLastNode (template.Node):
    def __init__(self, format_string):
        self.nick = format_string
        try:
            self.last = PhotoStream.objects.get(nick=self.nick).photostreamitem_set.latest('modif_date')
        except (PhotoStream.DoesNotExist, PhotoStreamItem.DoesNotExist):
            self.last = None
        
    def render(self, context):
        context['photostream_last'] = self.last
        return ''



def get_photostream_last (parser, token):
    """
    {% get_photostream_last <nick> %}
    
    For the PhotoStream with the suggested nick, get the PhotoStreamItem with the most recent 'date_modified'.
    Put it in the context as 'photostream_last'.
    
    More concisely: get the last photo in a selected feed.
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents[0]
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return PhotoStreamLastNode(format_string[1:-1])

register = template.Library()
register.tag(get_photostream_last)
