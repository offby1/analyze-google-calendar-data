#!/usr/bin/env python

"""Some documentation would be nice!"""

from __future__ import with_statement
__author__ = ""
__version__ = "$Id$"

import auth
import os
import re
import snag_events

def _PrintOwnCalendars(calendar_service):
  feed = calendar_service.GetOwnCalendarsFeed()
  print feed.title.text
  for i, a_calendar in enumerate(feed.entry):
    print '\t%s. %s' % (i, a_calendar.title.text,)

def _snag_local_auth_info():
    data = {}
    with open(os.path.join(os.getenv("HOME"), ".gmail-test-account-auth-info")) as fh:
        for line in fh:
            m = re.match("(.*?): (.*)", line)
            if m:
                data[m.group(1)] = m.group(2)
    print data
    return data

if __name__ == "__main__":
    auth_data = _snag_local_auth_info()
    cs = auth.auth(auth_data['username'], auth_data['password'])
    print "I guess it worked:", cs
    _PrintOwnCalendars(cs)
