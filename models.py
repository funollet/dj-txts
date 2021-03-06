# -*- coding:utf-8 -*-
from django.db import models, connection
from tagging.fields import TagField
from datetime import datetime
from django.utils.translation import ugettext as _


################################################################################

STATUS_CHOICES = (
    ('hid', _('hidden')),
    ('drf', _('draft')),
    ('rvs', _('revision')),
    ('pbl', _('public')),
    )

################################################################################

markup_help = {
    'markdown': _('''<div class="markup_help"><pre>
[un link][1]    *italica*    **negreta**    Titol     - un punt d'una llista
                                            -----     - segon punt
[1]: http://www.un.link.com                            - llista indentada
</pre>(<a href="http://daringfireball.net/projects/markdown/basics">Markdown syntax)</a></div>'''),
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



class TxtCategory (models.Model):

    def priority_default (increment=10):
        """Returns next suitable value for 'priority' field."""
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(priority) FROM txts_txtcategory ;")
        row = cursor.fetchone()
        try:
            return row[0] + increment
        except:
            return increment
    
    name = models.CharField (_('name'), max_length=200, )
    
    description= models.TextField (_('description'),
        blank=True,
        help_text = markup_help['markdown'],
    )
    
    priority = models.PositiveIntegerField (_('priority'),
        unique = True,
        help_text = _('Categories will be sorted by this field.'),
        default = priority_default,
    )
    
    easyname = models.SlugField (_('easyname'),
        unique=True,
        prepopulate_from=('name',),
        help_text = _('Easy-to-link name (good, if short, twice good).'),
    )
    
    pub_date = models.DateTimeField (_('publication date'), default=datetime.now,)
    modif_date = models.DateTimeField (_('modification date'), default=datetime.now, editable=False,)
    crea_date = models.DateTimeField (_('creation date'), editable=False,)

    hidden = models.BooleanField(_('hidden category'), default=False,
        help_text = 'Exclude this category from listings.',
    )

    class Meta:
        verbose_name = _('txt category')
        verbose_name_plural = _('txt categories')
        ordering = ['priority']

    
    def __unicode__ (self):
        return self.name

    def save (self):
        if not self.id:
            self.crea_date = datetime.now()
        super(LinkCategory, self).save()



class TxtSection (models.Model):
    name = models.CharField (_('name'), max_length=200, )
    
    description= models.TextField (_('description'),
        blank=True,
        help_text = markup_help['markdown'],
    )
    
    priority = models.PositiveIntegerField (_('priority'),
        unique = True,
        help_text = _('Categories will be sorted by this field.')
    )
    
    easyname = models.SlugField (_('easyname'),
        unique=True,
        prepopulate_from=('name',),
        help_text = _('Easy-to-link name (good, if short, twice good).'),
    )

    pub_date = models.DateTimeField (_('publication date'), default=datetime.now,)
    modif_date = models.DateTimeField (_('modification date'), default=datetime.now, editable=False,)
    crea_date = models.DateTimeField (_('creation date'), editable=False,)


    class Meta:
        verbose_name = _('txt section')
        verbose_name_plural = _('txt sections')
        ordering = ['priority']
    class Admin:
        list_display = ['name', 'priority']
        fields = (
            (None, {'fields': ('name', 'description', 'priority',),}),
            (_('Advanced'), {
                'fields': ('easyname', 'pub_date',), 
                'classes': 'collapse',
            } ),
        )

    
    def __unicode__ (self):
        return self.name

    def save (self):
        if not self.id:
            self.crea_date = datetime.now()
        super(TxtSection, self).save()

    def get_absolute_url (self):
        pass


################################################################################

class PublicManager (models.Manager):
    def get_query_set (self):
        return super(PublicManager, self).get_query_set().filter(status='pbl')


class Txt (models.Model):

    status = models.CharField (_('status'), max_length=3, 
        choices=STATUS_CHOICES,
        default='pbl',
        radio_admin=True,
        )
    section = models.ForeignKey( TxtSection,
        verbose_name=_('section'),
    )
    category = models.ForeignKey( TxtCategory,
        verbose_name=_('category'),
        blank = True, null=True,
    )
    name = models.CharField (_('name'), max_length=200, )
    abstract = models.TextField (_('abstract'),
        blank = True,
        help_text = markup_help['markdown'],
    )
    body = models.TextField (_('body'),
        blank = True,
        help_text = markup_help['markdown'],
    )
    tags = TagField()
    pub_date = models.DateTimeField (_('publication date'), default=datetime.now,)
    modif_date = models.DateTimeField (_('modification date'), default=datetime.now, editable=False)
    crea_date = models.DateTimeField (_('creation date'), editable=False,)
    easyname = models.SlugField (_('easyname'),
        prepopulate_from = ('name',),
        unique = True,
        help_text = _('Easy-to-link name (good, if short, twice good).'),
    )
    author_name = models.CharField ( _("Author's name"), 
        blank=True,
        max_length=75,
    )
    comments_closed = models.BooleanField ( _('Comments closed'),
        default = False,
        help_text = _('Closes comments for this post.'),
    )

    class Meta:
        verbose_name = _('txt')
        verbose_name_plural = _('txts')
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    class Admin:
        list_display = ('name', 'section', 'pub_date',)
        list_filter = ('status', 'section',)
        search_fields = ('name',)
        ordering = ['-pub_date']
        fields = (
            (None, {'fields': (('name', 'section',),
                'body', 'tags',),}),
            (_('Abstract'), {'fields': ('abstract',),
                'classes': 'collapse',}),
            (None, {'fields': ('status',), }),
            (_('Advanced'), {'fields': ('easyname', 'pub_date', 'author_name', 'comments_closed',),
                'classes': 'collapse',}),
        )

    
    objects = models.Manager()
    public = PublicManager()
    
    
    def save (self):
        if not self.id:
            self.crea_date = datetime.now()
        super(Txt, self).save()

    def __unicode__ (self):
        return self.name

    def get_absolute_url(self):
        pass
    

