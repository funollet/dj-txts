# -*- coding:utf-8 -*-
from django.db import models
from djapps.misc.markup import markup_help, parse_markup
from djapps.tags.models import Tag
from djapps.tags import fields


################################################################################

STATUS_CHOICES = (
    ('hid', _('hidden')),
    ('drf', _('draft')),
    ('rvs', _('revision')),
    ('pbl', _('public')),
    )

################################################################################

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
    
    permalink = models.SlugField (_('permalink'),
        unique=True,
        prepopulate_from=('name',),
        help_text = _('Easy-to-link name (good, if short, twice good).'),
        )

    pub_date = models.DateTimeField (_('publication date'), auto_now=True,)


    class Meta:
        verbose_name = _('txt section')
        verbose_name_plural = _('txt sections')
        ordering = ['priority']
    class Admin:
        fields = (
            (None, {'fields': ('name', 'description_markup', 'priority',),}),
            (_('Advanced'), {
                'fields': ('permalink', 'pub_date',), 
                'classes': 'collapse',
            } ),
        )

    
    def __str__ (self):
        return self.name

    def save (self):
        parse_markup (self)
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
    pub_date = models.DateTimeField (_('publication date'), )
    last_modif = models.DateTimeField (_('last modification date'), auto_now=True,)
    permalink = models.SlugField (_('permalink'),
        prepopulate_from = ('name',),
        unique = True,
        help_text = _('Easy-to-link name (good, if short, twice good).'),
    )


    class Meta:
        verbose_name = _('txt')
        verbose_name_plural = _('txts')
        order_with_respect_to = 'section'
        ordering = ['pub_date']

    class Admin:
        list_display = ('name', 'pub_date',)
        list_filter = ('status', 'section',)
        search_fields = ('name',)
        fields = (
            (None, {'fields': (('name', 'section',),
                'body_markup', 'tags',),}),
            (_('Abstract'), {'fields': ('abstract_markup',),
                'classes': 'collapse',}),
            (None, {'fields': ('status',), }),
            (_('Advanced'), {'fields': ('permalink','pub_date',),
                'classes': 'collapse',}),
        )

    
    objects = models.Manager()
    public = PublicManager()
    
    
    def save (self):
        parse_markup (self)
        super(Txt, self).save()

    def __str__ (self):
        return self.name

    def get_abstract (self):
        pass
    
    def get_absolute_url(self):
        pass
    

