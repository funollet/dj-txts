#!/usr/bin/env python
# -*- coding:utf-8 -*-
# tags_loader.py

"""Post-upgrade script, transition from 'tags' application to 'django-tagging'.
Works with 'tags-extractor.py' and 'txts_migra.sql'.
Loads a dictionary containing txts_txt objects id and tags. Insert this as django-tagging objects.
"""
import pickle
from tagging.models import Tag, TaggedItem
from txts.models import Txt

def main():
    f = file('tags.pckl')
    data = pickle.load(f)
    f.close()
    
    for txt_id, tag_names in data.items():
        txt_item = Txt.objects.get(id=txt_id)
        txt_item.tags = tag_names
        txt_item.save()
        
if __name__ == '__main__':
    main()
    