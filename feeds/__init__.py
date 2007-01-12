from django.contrib.syndication.feeds import Feed
from txts.models import Txt
from django.utils.feedgenerator import Atom1Feed


class BlogEntries (Feed):
    title = "terraquis.net"
    link = "/blog/"
    description = "De terricoles i xarxes"
    feed_type = Atom1Feed

    def items(self):
        return Txt.public.filter(section__name='blog').order_by('-pub_date')[:15]



class TagBadopi(Feed):
    title = "terraquis.net"
    link = "/blog/"
    description = "Tagged with: badopi"
    feed_type = Atom1Feed

    def items(self):
        return Txt.public.filter(section__name='blog').filter(tags__value='badopi').order_by('-pub_date')[:15]
