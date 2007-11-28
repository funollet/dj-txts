from django import template
from txts.models import Txt, TxtSection


class BlogLastNode (template.Node):
    def __init__(self):
        try:
            self.last = Txt.public.filter(section__easyname='blog').latest('modif_date')
        except (Txt.DoesNotExist, TxtSection.DoesNotExist):
            self.last = None
        
    def render(self, context):
        context['blog_last'] = self.last
        return ''



def get_blog_last (parser, token):
    """
    {% get_blog_last %}
    
    Get the Txt from section 'blog' object with the most recent 'date_modified'.
    Put it in the context as 'blog_last'.
    """
    return BlogLastNode()

register = template.Library()
register.tag(get_blog_last)
