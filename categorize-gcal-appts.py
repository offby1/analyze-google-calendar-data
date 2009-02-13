#!/usr/bin/env python

"""
Examine my Google calendar data (which I downloaded from
http://www.google.com/calendar/ical/eric.hanchrow%40gmail.com/private-LOTSA-SEKRIT-DIGITS/basic.ics),
and categorize the various UID fields.

I'm doing this because I seem to have a lot of "duplicate" events:
four events that all have the same summary, times, etc., and differ
only in their UIDs.  I suspect "Google Calendar Sync" of having
created them ... and I also suspect I'd be better off without them.
"""

from __future__ import with_statement
__author__ = ""
__version__ = "$Id$"

from icalendar import Calendar, Event
import collections
import re

def soft_id(event):
    """
    Returns a value that is basically a hash of the more interesting
    bits of an event.  In particular, it ignores the UID, but it
    includes the summary, description, and some of the dates.  The
    idea is that if two events have the same soft_id, then I won't
    care if all but one of them vanishes.
    """
    return "-".join([str(event.get(field)) for field in ['DTSTART', 'DTEND', 'RRULE', 'DESCRIPTION', 'LOCATION', 'SUMMARY']])

events_by_soft_id = collections.defaultdict(list)

with open("gcal.ics") as fh:
    cal = Calendar.from_string(fh.read())
    for component in cal.walk():
        if component.name == 'VEVENT':
            events_by_soft_id[soft_id(component)].append(component)
            
print len(events_by_soft_id.keys()), "events, after 'soft' merging"
total_events = 0
for events in events_by_soft_id.values():
    total_events += len(events)
print total_events, "events"
print

# Keys are the number of UIDs on an event; values are the number of
# events I found that had that many UIDs.
duplications_histogram = collections.defaultdict(lambda: 0)
for events in events_by_soft_id.values():
    duplications_histogram[len(events)] += 1
for num_uuids, num_events in duplications_histogram.iteritems():
    print "%5d events had %2d UIDs." % (num_events, num_uuids)
print


uids_by_description = collections.defaultdict(list)

for soft_id, events in events_by_soft_id.iteritems():
    for e in events:
        uid = e.get('UID')
        for recognizer, description in [
            (lambda uid: re.match(".*@(google|gmail).com", uid),
             'google_uids'),
            (lambda uid: len(uid) > 100,
             'long_uids'),
            (lambda uid: re.match('{........-....-....-....-............}', uid),
             'curly_brace_uids'),
            (lambda uid: re.match('........-....-....-....-............', uid),
             'bare_uids'),
            (lambda uid: True,
             'unknown'),
            ]:
            if recognizer(uid):
                uids_by_description[description].append(uid)
                break

print "Summary of kinds of UIDs:"
for descr, uids in uids_by_description.iteritems():
    print descr, ":",
    if descr == 'unknown':
        print uids
    else:
        print len(uids)
print

print "A sample duplicated event:"
soft_id, events = events_by_soft_id.popitem()
print "soft_id:", soft_id
for e in events:
    print "uid:", e.get('UID')
