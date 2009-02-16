#!/usr/bin/env python

"""Some documentation would be nice!"""

from __future__ import with_statement
__author__ = ""
__version__ = "$Id$"

def PrintAllEventsOnDefaultCalendar(calendar_service):
    feed = calendar_service.GetCalendarEventFeed()
    print 'Events on Primary Calendar: %s' % (feed.title.text,)
    for i, an_event in enumerate(feed.entry):
        print '\t%s. %s' % (i, an_event.title.text,)
    for p, a_participant in enumerate(an_event.who):
        print '\t\t%s. %s' % (p, a_participant.email,)
        print '\t\t\t%s' % (a_participant.name,)
        if getattr(a_participant, 'attendee_status', None):
            print '\t\t\t%s' % (a_participant.attendee_status.value,)
