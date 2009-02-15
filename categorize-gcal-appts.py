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
import icalendar
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
            
total_events = 0
for events in events_by_soft_id.values():
    total_events += len(events)
print total_events, "total events"
print len(events_by_soft_id.keys()), "events, after 'soft' merging"
print

# Keys are the number of UIDs on an event; values are the number of
# events I found that had that many UIDs.
duplications_histogram = collections.defaultdict(lambda: 0)
for events in events_by_soft_id.values():
    duplications_histogram[len(events)] += 1
for num_uuids, num_events in duplications_histogram.iteritems():
    print "%5d events had %2d UIDs." % (num_events, num_uuids)
print


def describe_uid(thing, verbose=False):
    """
    Return a short string -- one of just a few possibilities -- that describes the uid.
    """
    e = None

    if isinstance(thing, Event):
        e = thing
        thing = str(thing.get('UID'))
    elif isinstance(thing, icalendar.prop.vText):
        thing = str(thing)
    
    if not isinstance(thing, str):
        print "OK, I give up: what the hell is %s (type: %s; dir: %s)?" % (thing, type(thing), dir(thing))
        exit(1)
    
    for recognizer, description in [
        (lambda uid: re.match(".*@(google|gmail).com", uid),
         'google_uids'),
        (lambda uid: len(uid) > 100,
         'long_uids'),
        (lambda uid: re.match('{........-....-....-....-............}', uid),
         'curly_brace_uids'),
        (lambda uid: re.match('........-....-....-....-............', uid),
         'bare_uids'),
        ]:
        if recognizer(thing):
            return description
            break

    if verbose:
        print "event %s has funny-lookin' UID %s" % (e, thing)

    return 'unrecognized'

uids_by_description = collections.defaultdict(list)

for soft_id, events in events_by_soft_id.iteritems():
    for e in events:
        uid = e.get('UID')
        uids_by_description[describe_uid(uid)].append(uid)

print "Summary of kinds of UIDs:"
for descr, uids in uids_by_description.iteritems():
    print descr, ":",
    print len(uids)
print


# Test a theory: for every bunch of duplicated events, two qualities
# hold:

# * There is at most one google-flavor UID; and
# * if there is one, it's got the oldest "created" time.
for soft_id, events in events_by_soft_id.iteritems():
    with_google_uids = filter(lambda e: 'google_uids' == describe_uid(e), events)
    if len(with_google_uids) > 1:
        print "Crap, the event with soft_id %s has %d google UIDs" % (soft_id, len(with_google_uids))
        exit(1)

    if len(with_google_uids) == 1:
        events.sort(cmp, lambda e: str(e.get('CREATED')))
        oldest = events[0]
        if with_google_uids[0].get('UID') <> oldest.get('UID'):
            for e in events:
                print e.get('CREATED'),
            print
            print "Crap, the oldest event %s doesn't have the same UID as %s" % (oldest, with_google_uids[0])
            exit(1)

print "Aha!  Zee theory iss korrect!"

# Some day I will translate the "print" statement to a Google API call
# that actually does the deletions.

# See http://code.google.com/apis/calendar/ and
# http://code.google.com/p/gdata-python-client/
# http://code.google.com/apis/calendar/docs/1.0/developers_guide_python.html
with open('uids-of-duplicates', 'w') as fh:
    for soft_id, events in events_by_soft_id.iteritems():
        events.sort(cmp, lambda e: str(e.get('CREATED')))
        if len(events) > 1:
            for dup in events[1:]:
                print >> fh, dup.get('UID')
print "Wrote", fh.name
