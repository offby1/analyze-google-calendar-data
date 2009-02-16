#!/usr/bin/env python

"""Some documentation would be nice!"""

from __future__ import with_statement
__author__ = ""
__version__ = "$Id$"

def PrintAllEventsOnDefaultCalendar(calendar_service, *args, **kwargs):
    feed = calendar_service.GetCalendarEventFeed(*args, **kwargs)
    print 'Events on Primary Calendar: %s' % (feed.title.text,)
    for i, an_event in enumerate(feed.entry):
        print '\t%s. %s' % (i, an_event.title.text,)

        print "event:"
        print an_event
        print
        
        print "That event's ID:"
        print an_event.id
        print

        break

    kwargs['uri'] = feed.GetNextLink().href
    print "Next:"
    PrintAllEventsOnDefaultCalendar(calendar_service, *args, **kwargs)
    
