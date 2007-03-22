#!/usr/bin/env python

"""
Update feeds for Django community page.  Requires Mark Pilgrim's excellent
Universal Feed Parser (http://feedparser.org)
"""

import os
import time
import optparse
import datetime
import feedparser

def update_feeds():
    from photostream.models import PhotoStream, PhotoStreamItem
    for feed in PhotoStream.objects.filter(is_defunct=False):
        parsed_feed = feedparser.parse(feed.feed_url)
        for entry in parsed_feed.entries:
            title = entry.title.encode(parsed_feed.encoding, "xmlcharrefreplace")
            guid = entry.get("id", entry.link).encode(parsed_feed.encoding, "xmlcharrefreplace")
            link = entry.link.encode(parsed_feed.encoding, "xmlcharrefreplace")

            if entry.has_key('modified_parsed'):
                modif_date = datetime.datetime.fromtimestamp(time.mktime(entry.modified_parsed))
            elif parsed_feed.feed.has_key('modified_parsed'):
                modif_date = datetime.datetime.fromtimestamp(time.mktime(parsed_feed.feed.modified_parsed))
            elif parsed_feed.has_key('modified'):
                modif_date = datetime.datetime.fromtimestamp(time.mktime(parsed_feed.modified))
            else:
                modif_date = datetime.datetime.now()

            try:
                # Already aggregated; do nothing.
                feed.photostreamitem_set.get(guid=guid)
            except PhotoStreamItem.DoesNotExist:
                feed.photostreamitem_set.create(title=title, link=link, guid=guid, modif_date=modif_date)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--settings')
    options, args = parser.parse_args()
    if options.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = options.settings
    update_feeds()
