#!/usr/bin/env python

"""
Authenticate against Google's Calendar APIs.  This requires that you
download and install
http://gdata-python-client.googlecode.com/files/gdata.py-1.2.4.tar.gz
or something quite similar.
"""

from __future__ import with_statement
__author__ = ""
__version__ = "$Id$"

from xml.etree import ElementTree
import atom
import atom.service
import gdata.calendar
import gdata.calendar.service
import gdata.service
import getopt
import os
import re
import string
import sys
import time

def auth(email, password):
    calendar_service = gdata.calendar.service.CalendarService()
    calendar_service.email = email
    calendar_service.password = password
    calendar_service.source = "eric.hanchrow-gcaldeduplicator-version0"
    calendar_service.ProgrammaticLogin()

    return calendar_service

def snag_local_auth_info():
    with open(os.path.join(os.getenv("HOME"), ".imap-authinfo")) as fh:
        for line in fh:
            m = re.match(".*login (.*?) password \"(.*)\".*", line)
            if m:
                return list(m.groups())
    return None

def PrintOwnCalendars(calendar_service):
  feed = calendar_service.GetOwnCalendarsFeed()
  print feed.title.text
  for i, a_calendar in enumerate(feed.entry):
    print '\t%s. %s' % (i, a_calendar.title.text,)

if __name__ == "__main__":
    cs = auth(*snag_local_auth_info())
    print "I guess it worked:", cs
    PrintOwnCalendars(cs)

