from django.db import models

ENGINE_CHOICES = (
    ('23hq', '23hq'),
    ('flickr', 'flickr'),
)
# flickr: untested.
    
class PhotoStream(models.Model):
    nick = models.CharField (_('nick'),
        maxlength=200,
        unique = True,
        help_text = _('Short and easy to remember name.'),
    )
    name = models.CharField( _('name'),
        maxlength=200,
        blank = True,
    )
    feed_url = models.URLField( _('feed url'),
        unique = True,
    )
    home_url = models.URLField(_('home url'),
        help_text = 'Webpage showing those photos.',
        blank = True,
    )
    engine = models.CharField(maxlength=200,
        choices = ENGINE_CHOICES,
        default = '23hq',
    )
    is_defunct = models.BooleanField()
    crea_date = models.DateTimeField (_('creation date'), default=models.LazyDate(),)

    class Admin:
        list_display = ('nick', 'name', 'feed_url',)
        list_filter = ('engine',)
        search_fields = ('nick', 'name',)

    def __str__(self):
        return self.nick



class PhotoStreamItem(models.Model):
    feed = models.ForeignKey(PhotoStream)
    
    title = models.CharField(maxlength=200)
    link = models.URLField()
    modif_date = models.DateTimeField()
    guid = models.CharField(maxlength=200, unique=True, db_index=True)

    class Meta:
        ordering = ("-modif_date",)

    def __str__(self):
        return self.link
    