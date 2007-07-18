#!/usr/bin/env python
# -*- coding:utf-8 -*-
# tags-extractor.py

"""Pre-upgrade script, transition from 'tags' application to 'django-tagging'.
Works with 'tags-loader.py' and 'txts_migra.sql'. Saves a dictionary containing
txts_txt objects id and tags.

Run it *BEFORE* modifying tables with './manage.py dbshell < txts_migra.sql'.

  $ cd txts/migration/
  $ ./tags-extractor.py
  $ ../../manage.py dbshell < txts_migra.sql
  $ ./tags_loader.py
"""

from txts.models import Txt
import pickle

def txt_to_taglist (txt_item):
    """
    >>> txt_to_taglist(Txt.objects.get(id=4))
    [4, 'un dos tres no-son-etiquetes']
    """
    tgs = [ tg.value for tg in txt_item.tags.order_by('id') ]
    return [ txt_item.id, ' '.join( tgs ) ]


def get_all_tags():
    """
    >>> data = get_all_tags()
    >>> data[4]
    'un dos tres no-son-etiquetes'
    """
    return dict([txt_to_taglist(t) for t in Txt.objects.all()])


def main():
    f = file('tags.pckl', 'w')
    pickle.dump(get_all_tags(), f)
    f.close()
    

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    #_test()
    main()