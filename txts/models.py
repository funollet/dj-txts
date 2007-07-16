# -*- coding:utf-8 -*-
from django.db import models
from misc.markup import markup_help, parse_markup
from tags.models import Tag
from tags import fields
from datetime import datetime


################################################################################

STATUS_CHOICES = (
    ('hid', _('hidden')),
    ('drf', _('draft')),
    ('rvs', _('revision')),
    ('pbl', _('public')),
    )

################################################################################

class TxtCategory (models.Model):

    name = models.CharField (_('name'), maxlength=200, )
    
    description= models.TextField (_('description'), editable=False,)
    description_markup = models.TextField (_('description'), 
        blank=True,
        help_text = markup_help['docutils'],
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

    hidden = models.BooleanField(_('hidden category'), default=False,
        help_text = 'Exclude this category from listings.',
    )

    class Meta:
        verbose_name = _('txt category')
        verbose_name_plural = _('txt categories')
        ordering = ['priority']
    #class Admin:
        #fields = (
            #(None, {'fields': ('name', 'description_markup', 'priority',),}),
            #(_('Advanced'), {
                #'fields': ('easyname', 'pub_date', 'hidden'), 
                #'classes': 'collapse',
            #} ),
        #)
        #list_display = ('name', 'priority',)

    
    def __str__ (self):
        return self.name

    def save (self):
        parse_markup (self)
        if not self.id:
            self.crea_date = datetime.now()
        super(LinkCategory, self).save()

    #def get_absolute_url (self):
        #pass


class TxtSection (models.Model):
    name = models.CharField (_('name'), maxlength=200, )
    
    description= models.TextField (_('description'), editable=False,)
    description_markup = models.TextField (_('description'), 
        blank=True,
        help_text = markup_help['docutils'],
    )
    
    priority = models.PositiveIntegerField (_('priority'),
        unique = True,
        help_text = _('Categories will be sorted by this field.')
    )
    
    easylink = models.SlugField (_('easylink'),
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
            (None, {'fields': ('name', 'description_markup', 'priority',),}),
            (_('Advanced'), {
                'fields': ('easylink', 'pub_date',), 
                'classes': 'collapse',
            } ),
        )

    
    def __str__ (self):
        return self.name

    def save (self):
        parse_markup (self)
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

    status = models.CharField (_('status'), maxlength=3, 
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
    
    name = models.CharField (_('name'), maxlength=200, )

    abstract = models.TextField (_('abstract_html'), editable=False,)
    abstract_markup = models.TextField (_('abstract'), 
        blank = True,
        help_text = markup_help['docutils'],
    )
    
    body = models.TextField (_('body_html'), editable=False,)
    body_markup = models.TextField (_('body'), 
        blank = True,
        help_text = markup_help['docutils'],
    )

    tags = fields.TagsField( Tag, blank = True, )
    pub_date = models.DateTimeField (_('publication date'), default=datetime.now,)
    modif_date = models.DateTimeField (_('modification date'), default=datetime.now, editable=False)
    crea_date = models.DateTimeField (_('creation date'), editable=False,)
    easylink = models.SlugField (_('easylink'),
        prepopulate_from = ('name',),
        unique = True,
        help_text = _('Easy-to-link name (good, if short, twice good).'),
    )
    author_name = models.CharField ( _("Author's name"), 
        blank=True,
        maxlength=75,
    )
    comments_closed = models.BooleanField ( _('Comments closed'),
        default = False,
        help_text = _('Closes comments for this post.'),
    )

    class Meta:
        verbose_name = _('txt')
        verbose_name_plural = _('txts')
        order_with_respect_to = 'section'
        ordering = ['pub_date']

    class Admin:
        list_display = ('name', 'section', 'pub_date',)
        list_filter = ('status', 'section',)
        search_fields = ('name',)
        ordering = ['-pub_date']
        fields = (
            (None, {'fields': (('name', 'section',),
                'body_markup', 'tags',),}),
            (_('Abstract'), {'fields': ('abstract_markup',),
                'classes': 'collapse',}),
            (None, {'fields': ('status',), }),
            (_('Advanced'), {'fields': ('easylink', 'pub_date', 'author_name', 'comments_closed',),
                'classes': 'collapse',}),
        )

    
    objects = models.Manager()
    public = PublicManager()
    
    
    def save (self):
        parse_markup (self)
        if not self.id:
            self.crea_date = datetime.now()
        super(Txt, self).save()

    def __str__ (self):
        return self.name

    def get_absolute_url(self):
        pass
    

