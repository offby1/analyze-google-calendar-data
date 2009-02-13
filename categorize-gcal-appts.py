#!/usr/bin/env python

"""Some documentation would be nice!"""

from __future__ import with_statement
__author__ = ""
__version__ = "$Id$"

from icalendar import Calendar, Event
import collections
import re

events_by_summary = collections.defaultdict(list)

with open("gcal.ics") as fh:
    cal = Calendar.from_string(fh.read())
    for component in cal.walk():
        if component.name == 'VEVENT':
            events_by_summary[component.get('SUMMARY')].append(component)

# Delete entries that aren't duplicates.
for summary in events_by_summary.keys():
    events = events_by_summary[summary]
    if len(events) == 1:
        del events_by_summary[summary]

print len(events_by_summary.keys()), "summaries"
total_events = 0
for events in events_by_summary.values():
    total_events += len(events)
print total_events, "events"

google_uids = 0
long_uids = 0
curly_brace_uids = 0
freaks_printed = 0
for summary, events in events_by_summary.iteritems():
    for e in events:
        uid = e.get('UID')
        if re.match(".*@(google|gmail).com", uid):
            google_uids += 1
        elif len(uid) > 100:
            long_uids += 1
        elif re.match('{........-....-....-....-............}', uid):
            curly_brace_uids += 1
        else:
            if freaks_printed == 0:
                print "Here's an event with neither a Google-flavor nor a really long UID:"
                print e
                freaks_printed += 1

print google_uids, "google uids;", long_uids, "long uids"

print "A sample duplicated event:"
summary, events = events_by_summary.popitem()
print summary
for e in events:
    print e.get('UID')
