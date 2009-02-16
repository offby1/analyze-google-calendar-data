#!/usr/bin/env python

"""Some documentation would be nice!"""

from __future__ import with_statement
__author__ = ""
__version__ = "$Id$"

def EventIterator(calendar_service, *args, **kwargs):
    kwargs = kwargs.copy()

    while True:
        print "Getting", kwargs
        feed = calendar_service.GetCalendarEventFeed(*args, **kwargs)
        for i, an_event in enumerate(feed.entry):
            print "Top yield"
            yield an_event

        next_link = feed.GetNextLink()
        if not next_link:
            return

        kwargs['uri'] = next_link.href
