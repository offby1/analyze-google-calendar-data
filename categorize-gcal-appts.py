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

uids_by_description = collections.defaultdict(list)

freaks_printed = 0
for summary, events in events_by_summary.iteritems():
    for e in events:
        uid = e.get('UID')
        for recognizer, description in [
            (lambda uid: re.match(".*@(google|gmail).com", uid), 'google_uids'),
            (lambda uid: len(uid) > 100, 'long_uids'),
            (lambda uid: re.match('{........-....-....-....-............}', uid), 'curly_brace_uids'),
            (lambda uid: re.match('........-....-....-....-............', uid), 'bare_uids'),
            (lambda uid: True , 'unknown')
            ]:
            if recognizer(uid):
                uids_by_description[description].append(uid)
                break

for descr, uids in uids_by_description.iteritems():
    print descr, ":",
    if descr == 'unknown':
        print uids
    else:
        print len(uids)

print "A sample duplicated event:"
summary, events = events_by_summary.popitem()
print summary
for e in events:
    print e.get('UID')
