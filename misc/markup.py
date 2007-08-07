# markup.py
# -*- coding: utf-8 -*-
"""parse_markup() introspects every markup field from your model and
saves it parsed. If you're using Docutils it's called with a custom Writer cleaner
than the default 'html4css1'.

Usage
-----

On your models define two fields: one to be edited and one to save parsed text.
Parse automagically before saving.

    from yourproject.misc.markup import parse_markup
    
    class Article (models.Model):
        body = models.TextField (_('body_html'), editable=False,)
        body_markup = models.TextField (_('body'), blank=True, )
    
        def save (self):
            parse_markup (self)
            super(LinkCategory, self).save()

On your templates, just use the parsed and cached text.
Something like {{ object.body }} gives you HTML.



Optional settings
-----------------

    settings.MARKUP:
        Name of markup parser. Options: 'docutils', 'markdown', 'textile'.
        Default: 'docutils'
    settings.MARKUP_FIELD_TAIL:
        Name ending that identifies fields containing markup.
        Default: '_markup'
    settings.RESTRUCTUREDTEXT_FILTER_SETTINGS:
        Dictionary passed as 'settings_overrides' parameter to docutils writer.
        Also used by Django's templatetag 'restructuredtext'.
        Default: {}
"""

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from docutils import writers
from docutils.writers import html4css1



# Not really needed but it's usefull having this predefined to use on models
# as help_text.
markup_help = {
    'markdown': _('''<div class="markup_help">
    Use <a href="http://daringfireball.net/projects/markdown/basics">Markdown</a> Syntax</div>'''),
    'textile':  _('''<div class="markup_help">
    Use <a href="http://daringfireball.net/projects/markdown/basics">Textile</a> Syntax</div>'''),
    'docutils': _('''
    <div class="markup_help"><pre>
`un link`_    *italica*    **negreta**    Titol     - un punt d'una llista
                                          -----     - segon punt
.. _`un link`: http://www.google.com                 - llista indentada
</pre>(<a href="http://docutils.sourceforge.net/docs/user/rst/quickstart.html">reST syntax</a>: documentation).
    </div>'''),
}



def textile(value):
    import textile
    return textile.textile(value, encoding=settings.DEFAULT_CHARSET, output=settings.DEFAULT_CHARSET)

def markdown(value):
    import markdown
    return markdown.markdown(value)


def restructuredtext(value):
    from docutils.core import publish_parts
    
    docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
    djangowriter = DjangoWriter()     # use a custom writer
    parts = publish_parts(source=value, writer=djangowriter, settings_overrides=docutils_settings)
    return parts["fragment"].encode('utf-8')


class DjangoWriter(html4css1.Writer):
    """Customized docutils writer. Default html4ccs1 writer creates
    ugly tables with border=1 and a self-decided width.
    """
    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = DjangoHTMLTranslator


class DjangoHTMLTranslator(html4css1.HTMLTranslator):
    def visit_table(self, node):
        # Avoid the ugly-ugly-ugly border="1" from default writer.
        self.body.append(
            self.starttag(node, 'table', CLASS='docutils'))

    def write_colspecs(self):
        # Tables doesn't need a pre-calculated width, but default Writer
        # thinks otherwise.
        idx = 0
        for node in self.colspecs:
            self.body.append(self.starttag(node, 'col', CLASS=u'col-%s' % idx))
            idx += 1 
        self.colspecs = []




def parser(*args, **kwargs):
    # Callback functions for every parser, so we could automatically select this.
    # If you need a new parser, implement the function and add to this dictionary.
    parser_callbacks = {
        'docutils': restructuredtext,
        'markdown': markdown,
        'textile': textile,
    }
    
    # Markup to use.
    MARKUP = getattr(settings, 'MARKUP', 'docutils') 
    return parser_callbacks[MARKUP](*args, **kwargs)
    

def parse_markup (obj):
    """Parses markup attributes and pre-saves as HTML.
    
    Reads all obj.xxx_markup attributes and saves at obj.xxx,
    transformed into HTML. Uses a bit of instrospection. Allows
    choosing which markup to use.

    ``obj``:              object to parse
    """

    # Suffix for names of attributes containing markup.
    TAIL = getattr( settings, 'MARKUP_FIELD_TAIL', '_markup')

    def conditions (s):
        """Select non-hidden %s-ended strings""" % TAIL
        return ( s.endswith(TAIL) and not s.startswith('_') )

    markup_fields = [field for field in dir(obj) if conditions(field)]

    for longname in markup_fields :
        shortname = longname[:-len(TAIL)]       # Example: longname = 'first_part_markup'
        markup_source = getattr(obj, longname)  # Example: shortname = 'first_part'
        setattr(obj, shortname, parser(markup_source))
        # Example: self.first_part = parse (self.first_part_markup)

